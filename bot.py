import json
import asyncio
import websockets

from slacker import Slacker

from conf import *

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
            post_to_channel(1, 'Can I help you?')
        elif cmd[1] == 'test':
            post_to_channel(1, 'Show me the money')
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
