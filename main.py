import os
from dotenv import load_dotenv
from telethon.sync import TelegramClient, utils, events
from telethon.tl import types

# Carica le variabili d'ambiente dal file .env
load_dotenv()

# Leggi le variabili d'ambiente
api_id = os.getenv("API_ID")
api_hash = os.getenv("API_HASH")
phone_number = os.getenv("PHONE_NUMBER")


async def copy_and_send_message(event):
    message = event.message
    print(message)

    channel_id_destination = channel_mapping.get(event.chat_id)

    if channel_id_destination:
        text = None
        element = None

        if message.media:
            # se media inoltro
            # Sostituisci con l'ID effettivo del chat
            element = await event.client.forward_messages(channel_id_destination,
                                                          messages=message)

        elif message.text:
            sender = await event.get_sender()
            text = ""
            if hasattr(sender, 'first_name'):
                text = "**" + sender.first_name + " " + sender.last_name + " | " + sender.username + "**\n\n"

            text += message.text

            # Se il messaggio è una risposta a un altro messaggio, includi il testo del messaggio originale
            if message.is_reply and message.reply_to_msg_id in ids_map:
                element = await event.client.send_message(channel_id_destination,
                                                          text,
                                                          reply_to=ids_map[message.reply_to_msg_id],
                                                          parse_mode='markdown')
            else:
                element = await event.client.send_message(channel_id_destination, text, parse_mode='markdown')
        elif not message.is_reply:
            element = await event.client.send_message(channel_id_destination, text, parse_mode='markdown')

        ids_map[message.id] = element.id


async def main():
    async with TelegramClient(phone_number, api_id, api_hash) as client:
        await setup_channels(client)

        # Aggiungi un gestore di eventi per catturare i nuovi messaggi nei canali di origine
        for channel_id_source, channel_id_destination in channel_mapping.items():
            client.add_event_handler(copy_and_send_message, events.NewMessage(chats=channel_id_source))

        # Avvia il client
        await client.run_until_disconnected()

async def setup_channels(client):
    import csv

    id_channel_map = {}
    async for dialog in client.iter_dialogs():
        id_channel_map[dialog.name] = dialog.id

    with open('connections.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['channel_source'] not in id_channel_map:
                print("Attention: " + row['channel_source'] + " not in your chats")
            elif row['channel_destination'] not in id_channel_map:
                print("Attention: " + row['channel_destination'] + " not in your chats")
            else:
                channel_mapping[id_channel_map[row['channel_source']]] = id_channel_map[row['channel_destination']]


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
