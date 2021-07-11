import configparser
import pandas as pd
import sys
import logging
from telethon.sync import TelegramClient
from telethon import TelegramClient, events, sync


# Initializing logging handler
logger = logging.getLogger()
logger.setLevel(logging.INFO)
stdout_handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter(
    '[%(asctime)s] p%(process)s {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s', '%m-%d %H:%M:%S')

stdout_handler.setFormatter(formatter)
logger.addHandler(stdout_handler)


# Reading and returning the config as dict
def read_config():
    logger.info("Reading config")
    config = configparser.ConfigParser()
    config.read("config.ini")
    config_dict = dict(config['Telegram'])
    return config_dict


def main():
    logging.info("Inside main")
    config_dict = read_config()
    name, api_id, api_hash, chat = config_dict.get(
        'username'), config_dict.get('api_id'), config_dict.get('api_hash'), config_dict.get('chat')
    messages_list = []
    try:
        with TelegramClient(name, api_id, api_hash) as client:
            for message in client.iter_messages(chat):
                messages_list.append({"sender_id": message.sender_id,
                                      "message": message.text})

            client.disconnect()
    except Exception as e:
        logger.error("Exception occurred ", exc_info=True)
        logger.error(e)
    pd.DataFrame(messages_list).to_csv("Messages_text.csv", index=False)


if __name__ == "__main__":
    main()
