import os
from dotenv import load_dotenv
from telethon.sync import TelegramClient, utils, events

# Carica le variabili d'ambiente dal file .env
load_dotenv()

# Leggi le variabili d'ambiente
api_id = os.getenv("API_ID")
api_hash = os.getenv("API_HASH")
phone_number = os.getenv("PHONE_NUMBER")

# Crea un dizionario per mappare gli ID dei canali di origine agli ID dei canali di destinazione
channel_mapping = {
    -1002022962931: -1002091907058,  # Sostituisci gli ID dei canali con i tuoi
}

# Funzione per inoltrare i messaggi da un canale all'altro
async def forward_message(event):
    message = event.message
    print("Ciao")
    channel_id_destination = channel_mapping.get(event.chat_id)
    if channel_id_destination:
        print(channel_id_destination)
        await event.message.forward_to(channel_id_destination)

async def main():
    async with TelegramClient(phone_number, api_id, api_hash) as client:
        # Aggiungi un gestore di eventi per catturare i nuovi messaggi nei canali di origine
        for channel_id_source, channel_id_destination in channel_mapping.items():
            client.add_event_handler(forward_message, events.NewMessage(chats=channel_id_source))

        # Avvia il client
        await client.run_until_disconnected()

if __name__ == '__main__':
    import asyncio
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
