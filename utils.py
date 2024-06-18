import os
from dotenv import load_dotenv
from telethon.sync import TelegramClient, utils, events
from telethon.tl import types
from telethon import functions, types, errors
from telethon.tl.types import MessageActionTopicCreate

# Carica le variabili d'ambiente dal file .env
load_dotenv()

# Leggi le variabili d'ambiente
api_id = os.getenv("API_ID")
api_hash = os.getenv("API_HASH")
phone_number = os.getenv("PHONE_NUMBER")

# Dizionario delle regole di inoltro
forwarding_rules = {
    "Provolona>Provola topic": "TestReceiver",
}




# Funzione per ottenere l'ID di un gruppo dato il nome
async def get_group_id_by_name(client, group_name):
    try:
        dialogs = await client.get_dialogs()
        for dialog in dialogs:
            if dialog.name == group_name:
                return dialog.id
    except errors.RPCError as e:
        print(f"RPCError: {e}")
    return None


# Funzione principale
async def get_topic_id(client, string):
    from_group_name, topic_id = string.split('>')

    # Ottieni l'ID del gruppo di origine
    from_group_id = await get_group_id_by_name(client, from_group_name)
    if from_group_id is None:
        print(f"Cannot find group with name '{from_group_name}'")
        return None

    # Ottieni l'ID del gruppo di destinazione

    try:
        # Trova i messaggi che contengono il topic_id nel gruppo from_group_id
        messages = await client(functions.messages.SearchRequest(
            peer=from_group_id,
            q=topic_id,
            filter=types.InputMessagesFilterEmpty(),
            min_date=None,
            max_date=None,
            offset_id=0,
            add_offset=0,
            limit=100,
            max_id=0,
            min_id=0,
            hash=0
        ))

        # Inoltra i messaggi trovati al gruppo di destinazione
        for message in messages.messages:
            # Verifica se il tipo di azione è MessageActionTopicCreate
            if isinstance(message.action, MessageActionTopicCreate):
                return message.id
        return None

    except errors.FloodWaitError as e:
        print(f"FloodWaitError: {e}")
    except errors.RPCError as e:
        print(f"RPCError: {e}")

    return None
