from telethon import TelegramClient
import asyncio

api_id = 23163683
api_hash = ''
phone = '+'

client = TelegramClient('session_name', api_id, api_hash)

async def main():
    await client.start(phone)
    print("Logged in successfully!")

    invite_link = 'https://t.me/+oCbJHZNl7LExMDVl'
    
    # Get the channel/group from the invite link
    chat = await client.get_entity(invite_link)
    
    print(f"Scraping members from: {chat.title}")
    
    members = []
    async for user in client.iter_participants(chat, limit=5):
        members.append(user.username or user.id)

    print(f"Collected {len(members)} users:")
    print(members)

asyncio.run(main())
