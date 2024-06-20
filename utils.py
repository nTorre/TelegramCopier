# TODO: Sistemare codice, migliorie:
import os
from dotenv import load_dotenv
from telethon import errors, TelegramClient
from telethon.tl.patched import MessageService
from telethon.tl.types import MessageActionTopicCreate

load_dotenv()

api_id = os.getenv("API_ID")
api_hash = os.getenv("API_HASH")
phone_number = os.getenv("PHONE_NUMBER")


# Funzione per ottenere l'ID di un gruppo dato il nome
async def get_group_id_by_name(client, group_name):
    to_ret = []
    try:
        dialogs = await client.get_dialogs()
        for dialog in dialogs:
            if dialog.name == group_name:
                to_ret.append(dialog)
        return to_ret
    except errors.RPCError as e:
        print(f"RPCError: {e}")
    return None


'''async def get_group_dialogs(client, group_name):

    # Ottieni l'ID del gruppo di origine
    groups = await get_group_id_by_name(client, group_name)

    for dialog in groups:
        print(dialog)
'''

async def get_last_10_messages(client: TelegramClient, group_id: int, group_name, topic_name, limit=10):
    # Ottieni i messaggi
    messages = await client.get_messages(group_id, limit=limit)

    topic_id = -1

    # Stampa gli ultimi 10 messaggi
    for message in messages:

        if isinstance(message, MessageService):
            if isinstance(message.action, MessageActionTopicCreate):
                topic_id = message.id

                print(f"[{group_name}][gid {group_id}][mid {message.id}][TOPIC CREATION EVENT][{message.action.title}>{message.id}]")
            '''else:
                print(f"[{group_name}][gid {group_id}][mid {message.id}][EVENT]")'''

        #### Additional information
        elif message.reply_to is None:
            pass
            #print(f"[{group_name}][gid {group_id}][mid {message.id}][NOT TOPIC, NOT REPLY]: {message.text}")

        elif not message.reply_to.forum_topic:
            pass
            #print(f"[{group_name}][gid {group_id}][mid {message.id}][NOT TOPIC, REPLY]: {message.text}")

        elif message.reply_to.forum_topic:
            if message.reply_to.reply_to_top_id is None:
                if message.reply_to.reply_to_msg_id == 79997:
                    print(f"[{group_name}][gid {group_id}][tid: {message.reply_to.reply_to_msg_id}][mid {message.id}][TOPIC, NOT REPLY]: {message.text}")
            else:
                if message.reply_to.reply_to_top_id == 79997:
                    print(f"[{group_name}][gid {group_id}][tid: {message.reply_to.reply_to_top_id}][mid {message.id}][TOPIC, REPLY]: {message.text}")


    if topic_id != -1:
        print("\n")
        print("FOUND TOPIC CREATION")
        print(f"{group_name}>{topic_name} = {group_id}>{topic_id}")


async def get_formatted_string(group_name, topic_name):
    async with TelegramClient(phone_number, api_id, api_hash) as client:
        dialogs = await get_group_id_by_name(client, group_name)
        for dialog in dialogs:
            print("\n")
            print("-" * 100)
            print("\n")
            await get_last_10_messages(client, dialog.id, group_name, topic_name)


async def main():
    group_name = input("Group name:")
    topic_name = input("Topic name:")
    async with TelegramClient(phone_number, api_id, api_hash) as client:
        dialogs = await get_group_id_by_name(client, group_name)
        for dialog in dialogs:
            print("\n")
            print("-" * 100)
            print("\n")
            print(f"{group_name} {dialog.id}")
            await get_last_10_messages(client, dialog.id, group_name, topic_name)



if __name__ == '__main__':
    import asyncio

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())


