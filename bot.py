import json
import pytz
import asyncio
import datetime
import websockets

from bs4 import BeautifulSoup as bs
from slacker import Slacker

from conf import *

tz = pytz.timezone('Asia/Seoul')
slack = Slacker(TOKEN)

response = slack.rtm.start()
sock_endpoint = response.body['url']

def post_to_channel(idx, msg):
    slack.chat.post_message(CHANNELS[idx], msg, as_user=True)

def extract_message(msg):
    check_cmd = msg.split(' ', 1)
    if CMD_PREFIX != check_cmd[0]:
        return 'not command'

    post_to_channel(0, 'show me the money')

# Get message from slack channel
async def execute_bot():
    ws = await websockets.connect(sock_endpoint)
    while True:
        msg = await ws.recv()
        ext_msg = json.loads(msg)

        if ext_msg['type'] == 'message':
            extract_message(ext_msg['text'])

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
asyncio.get_event_loop().run_until_complete(execute_bot())
asyncio.get_event_loop().run_forever()
