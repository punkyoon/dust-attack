import datetime
import pytz

from bs4 import BeautifulSoup as bs
from slacker import Slacker

from conf import *

timezone = pytz.timezone('Asia/Seoul')
slack = Slacker(TOKEN)

def post_to_channel(idx, msg):
    slack.chat.post_message(CHANNELS[idx], msg, as_user=True)

def handler(event, context):
    ch = event['channel']
    msg = event['message']

    slack.chat.post_message(ch, msg)

if __name__ == '__main__':
    event = {};
    event['channel'] = '#general'
    event['message'] = 'test1'

    handler(event, None)
