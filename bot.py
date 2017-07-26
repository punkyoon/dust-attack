import re
import json
import asyncio
import websockets

from slacker import Slacker

from conf import *
from dust import Dust

slack = Slacker(TOKEN)

response = slack.rtm.start()
sock_endpoint = response.body['url']

def post_to_channel(idx, msg):
    slack.chat.post_message(CHANNELS[idx], msg, as_user=True)

# Send message to slack channel
def extract_message(msg):
    cmd = msg.split(' ')
    if CMD_PREFIX != cmd[0]:
        return 'not command'

    if 1 < len(cmd):
        if cmd[1] == 'help':
            post_to_channel(1, '@dust-attack <지역>')
        elif bool(re.match('[가-힣]+', cmd[1])):
            dust = Dust(API_KEY)
            location = dust.getLocation(cmd[1])
            if location == None:
                post_to_channel(1, '잘못된 지역입니다.')
            else:
                aqi = dust.getDust(location)
                post_to_channel(1, aqi)
        else:
            post_to_channel(1, '????')
    else:
        post_to_channel(1, '@dust-attack help')


# Get message from slack channel
async def execute_bot():
    ws = await websockets.connect(sock_endpoint)
    while True:
        msg = await ws.recv()
        ext_msg = json.loads(msg)

        try:
            if ext_msg['type'] == 'message':
                extract_message(ext_msg['text'])
        except:
            pass

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
asyncio.get_event_loop().run_until_complete(execute_bot())
asyncio.get_event_loop().run_forever()
