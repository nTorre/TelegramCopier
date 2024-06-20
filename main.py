import os
from dotenv import load_dotenv
from telethon.sync import TelegramClient, events
from telethon.tl import types

# Carica le variabili d'ambiente dal file .env
load_dotenv()

# Leggi le variabili d'ambiente
api_id = os.getenv("API_ID")
api_hash = os.getenv("API_HASH")
phone_number = os.getenv("PHONE_NUMBER")


async def copy_and_send_message(event):

    message = event.message

    try:
        chat_id = message.chat_id
        if chat_id is None:
            chat_id = message.peer_id.chat_id
    except:
        chat_id = message.peer_id.channel_id


    # controllo se arriva da un topic

    if message.reply_to and message.reply_to.forum_topic:
        # get topic id
        topic_id = message.reply_to.reply_to_msg_id
        if message.reply_to.reply_to_top_id is not None:
            topic_id = message.reply_to.reply_to_top_id

        print(topic_id)
        channel_id_destination = channel_mapping.get(str(chat_id) + ">" + str(topic_id))

    else:
        channel_id_destination = channel_mapping.get(int(abs(float(chat_id))))

    print(message)



    if channel_id_destination:
        print(int(abs(float(channel_id_destination))))

        text = None
        element = None

        if message.media:
            # se media inoltro
            # Sostituisci con l'ID effettivo del chat
            element = await event.client.forward_messages(int(abs(float(channel_id_destination))),
                                                          messages=message)

        elif message.text:
            sender = await event.get_sender()
            text = "**"
            if hasattr(sender, 'first_name') and sender.first_name is not None:
                text += sender.first_name

            if hasattr(sender, 'last_name') and sender.last_name is not None:
                if text != "":
                    text += " "
                text += " " + sender.last_name

            if hasattr(sender, 'username') and sender.username is not None:
                if text != "":
                    text += " | "
                text += sender.username

            text += "**\n\n"
            text += message.text

            # Se il messaggio è una risposta a un altro messaggio, includi il testo del messaggio originale
            if message.is_reply and message.reply_to_msg_id in ids_map:
                element = await event.client.send_message(int(abs(float(channel_id_destination))),
                                                          text,
                                                          reply_to=ids_map[message.reply_to_msg_id],
                                                          parse_mode='markdown')
            else:
                element = await event.client.send_message(int(abs(float(channel_id_destination))), text, parse_mode='markdown')
        elif not message.is_reply:
            element = await event.client.send_message(int(abs(float(channel_id_destination))), text, parse_mode='markdown')

        ids_map[message.id] = element.id


async def main():
    async with TelegramClient(phone_number, api_id, api_hash) as client:
        await setup_channels(client)

        # Aggiungi un gestore di eventi per catturare i nuovi messaggi nei canali di origine
        for channel_id_source, channel_id_destination in channel_mapping.items():
            if str(channel_id_source).find('>') != -1:
                target = channel_id_source.split('>')[0]
                client.add_event_handler(copy_and_send_message, events.NewMessage(chats=int(abs(float(target)))))
            else:
                client.add_event_handler(copy_and_send_message, events.NewMessage(chats=int(abs(float(channel_id_source)))))

        # Avvia il client
        await client.run_until_disconnected()



def get_entity_id_from_dialog(client, dialog):
    try:
        # Ottieni l'entità associata al Dialog
        entity = dialog.entity

        # Verifica il tipo di entità e restituisci l'ID corrispondente
        if isinstance(entity, types.User):
            return entity.id
        elif isinstance(entity, types.Chat):
            return entity.id
        elif isinstance(entity, types.Channel):
            return entity.id
        else:
            return None

    except Exception as e:
        print(f"Errore durante il recupero dell'ID dell'entità: {e}")
        return None

async def get_group_id_by_name(client, group_name):
    dialogs = await client.get_dialogs()
    for dialog in dialogs:
        if dialog.name == group_name:
            entity_id = get_entity_id_from_dialog(client, dialog)
            return entity_id
    return None

async def setup_channels(client):
    import csv


    with open('connections.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:

            print(row)

            channel_src = row['channel_source'].split(">")
            if len(channel_src) == 1:
                channel_src_name = channel_src[0]

                channel_src_id = await get_group_id_by_name(client, channel_src_name)
                if channel_src_id is None:
                    print("Attention: " + channel_src_name + " not in your chats")
                    continue

                channel_dest_id = await get_group_id_by_name(client, row['channel_destination'])
                if channel_dest_id is None:
                    print("Attention: " + row['channel_destination'] + " not in your chats")
                    continue

                key = int(str(channel_src_id).replace('-', ''))
                channel_mapping[key] = int(abs(float(channel_dest_id)))


            if len(row['channel_source'].split(">")) == 2:
                # prendo il topic id
                channel_src_group_id = row['channel_source'].split(">")[0]
                channel_src_topic_id = row['channel_source'].split(">")[1]

                key = (str(channel_src_group_id) + ">" + str(channel_src_topic_id))
                channel_mapping[key] = int(abs(float(channel_dest_id)))

            elif len(row['channel_source'].split(">")) >= 3:
                print("Errore, i gruppi non possono contenere il carattere '>'")
                continue

    print(channel_mapping)

if __name__ == '__main__':

    # setup channel_map
    print("1. Setup channels...")
    channel_mapping = {}

    print("2. Starting listeners...")
    print("3. Started")

    # mappa per mappare gli id dei messaggi .original -> new
    ids_map = {}
    import asyncio
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
