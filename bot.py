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

# Send message to slack channel
def extract_message(channel, msg):
    cmd = msg.split(' ')
    if CMD_PREFIX != cmd[0]:
        return 'not command'

    if 1 < len(cmd):
        if cmd[1] == 'help':
            slack.chat.post_message(channel, '@dust-attack <지역>', as_user=True)
        elif bool(re.match('[가-힣]+', cmd[1])):
            dust = Dust(API_KEY)
            location = dust.getLocation(cmd[1])
            if location == None:
                slack.chat.post_message(channel, '잘못된 지역입니다.', as_user=True)
            else:
                aqi = dust.getDust(location)
                slack.chat.post_message(channel, aqi, as_user=True)
        else:
            slack.chat.post_message(channel, '????', as_user=True)
    else:
        slack.chat.post_message(channel, '@dust-attack help', as_user=True)


# Get message from slack channel
async def execute_bot():
    ws = await websockets.connect(sock_endpoint)
    while True:
        msg = await ws.recv()
        ext_msg = json.loads(msg)

        try:
            if ext_msg['type'] == 'message':
                extract_message(ext_msg['channel'], ext_msg['text'])
        except:
            pass

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
asyncio.get_event_loop().run_until_complete(execute_bot())
asyncio.get_event_loop().run_forever()
