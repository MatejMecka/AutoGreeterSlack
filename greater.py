# -*- coding: utf-8 -*-
from slackclient import SlackClient
import time
import logging
from config import *

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

handler = logging.FileHandler(log_file)
handler.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

logger.addHandler(handler)

sc = SlackClient(slack_token)

if sc.rtm_connect():
    while True:
        for slack_message in sc.rtm_read():
            logger.info(slack_message)
            message = slack_message.get("type")
            channelslack = slack_message.get("channel")
            user = slack_message.get("user")
            if not message or not user:
                continue
            if message == "member_joined_channel":
                sc.api_call("chat.postMessage",channel=user,as_user=True,text=welcomemessagedm)
                if welcomemessagechannel == "":
                    logger.info("No Message specified for channel to post")
                else:
                    sc.api_call("chat.postMessage", channel=channelslack, as_user=True, text=welcomemessagechannel)

            time.sleep(2)

else:
    logger.error("There is a problem connecting to Slack. Check your Internet connection or you might have problems with the API key.")
