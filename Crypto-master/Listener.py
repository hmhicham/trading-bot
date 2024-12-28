from telethon import TelegramClient, events
import pickle
from datetime import datetime
from message import Message 

from T_binance import *


api_id = '18899893'
api_hash = 'e3e894d4a1b01f483be171e33e8e9677'
phone_number = '213549851815'

client_T = TelegramClient('session_name', api_id, api_hash)
client_T.start(phone=phone_number)

# List of channel IDs
channel_ids = [-1002472647736] 



@client_T.on(events.NewMessage(chats=channel_ids))
async def handler(event):
    message = Message(
        id=event.message.id, 
        reply_id=event.message.reply_to_msg_id if event.message.reply_to_msg_id else -1, 
        text=event.message.text, 
        date=event.message.date.isoformat()
    )
    channel_id = event.chat_id
    enterTrade(message)
    #print(parse_coin_data(message.text))

client_T.run_until_disconnected()
print("Listen On Chanel")

