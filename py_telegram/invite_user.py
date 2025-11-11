# invite_users.py
from telethon import TelegramClient
from telethon.tl.functions.channels import InviteToChannelRequest
import asyncio

api_id = 23163683
api_hash = ''
phone = '+'  # your phone
group_username = 'your_public_group_username'  # the group you own or can invite to

async def main():
    client = TelegramClient('session_name', api_id, api_hash)
    await client.start(phone)
    print("Logged in successfully!")

    # Load users from file
    with open("users_list.txt", "r") as f:
        users = [line.strip() for line in f.readlines()]

    # Only invite first 5 users for testing
    users_to_invite = users[:5]

    try:
        await client(InviteToChannelRequest(
            channel=group_username,
            users=users_to_invite
        ))
        print(f"Invited {len(users_to_invite)} users successfully!")
    except Exception as e:
        print("Error inviting users:", e)

    await client.disconnect()

asyncio.run(main())
