import os
from dotenv import load_dotenv
from telethon import TelegramClient, events
import csv

# Carica le variabili d'ambiente dal file .env
load_dotenv()

# Leggi le variabili d'ambiente
api_id = os.getenv("API_ID")
api_hash = os.getenv("API_HASH")
phone_number = os.getenv("PHONE_NUMBER")

# Crea un dizionario per mappare i canali di origine ai canali di destinazione
channel_mapping = {}

# Leggi i canali da un file CSV
with open('connections.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        channel_mapping[row['channel_source']] = row['channel_destination']


# Funzione per inoltrare i messaggi da un canale all'altro
async def forward_message(event):
    message = event.message
    if not message.sender_id == event.chat_id:  # Evita l'inoltro di messaggi propri
        channel_username_destination = channel_mapping.get(event.chat.username)
        if channel_username_destination:
            # Utilizza get_input_entity per ottenere l'entità del canale privato
            destination_entity = await client.get_input_entity(channel_username_destination)
            await event.message.forward_to(destination_entity)


async def main():
    async with TelegramClient(phone_number, api_id, api_hash) as client:
        for channel_source, channel_destination in channel_mapping.items():
            # Utilizza get_input_entity per ottenere l'entità del canale privato
            source_entity = await client.get_input_entity(channel_source)
            # Aggiungi un gestore di eventi per catturare i nuovi messaggi nel canale di origine
            client.add_event_handler(forward_message, events.NewMessage(chats=source_entity))

        # Avvia il client
        await client.run_until_disconnected()


if __name__ == '__main__':
    import asyncio

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
