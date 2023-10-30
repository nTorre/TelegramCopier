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

        if message.text:
            text = message.text

        if text and message.is_reply:

            # Se il messaggio è una risposta a un altro messaggio, includi il testo del messaggio originale
            original_message = await event.client.get_messages(event.chat_id, ids=message.reply_to_msg_id)
            text = f"{original_message.text}\n-----------\n{text}"
        await event.client.send_message(channel_id_destination, text)


async def main():
    async with TelegramClient(phone_number, api_id, api_hash) as client:
        # Aggiungi un gestore di eventi per catturare i nuovi messaggi nei canali di origine
        for channel_id_source, channel_id_destination in channel_mapping.items():
            client.add_event_handler(copy_and_send_message, events.NewMessage(chats=channel_id_source))

        # Avvia il client
        await client.run_until_disconnected()

def setup_channels():
    import csv

    id_channel_map = {}
    client = TelegramClient('torre_session2', api_id, api_hash).start()
    for dialog in client.iter_dialogs():
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
    setup_channels()

    print("2. Starting listeners...")
    print("3. Started")
    import asyncio
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
