import os
from datetime import datetime, timedelta

# https://tl.telethon.dev/
from telethon.sync import TelegramClient, functions, types
from tqdm import tqdm

# These example values won't work. You must get your own api_id and
# api_hash from https://my.telegram.org, under API Development.
API_ID = 7506606
API_HASH = '3afbd4f428986541c1c02476765a0e7a'
TELEGRAM_CHANNEL = 'maddogholland'

FOLDER = '/media/wspek/W&S_SSD/Photos & Videos/Time_Capsule_COVID/'


def get_messages(client):
    result = client(functions.messages.GetHistoryRequest(
        peer=client.get_entity(TELEGRAM_CHANNEL),
        offset_id=0,
        offset_date=datetime(2021, 8, 13),
        add_offset=0,
        limit=0,
        max_id=0,
        min_id=0,
        hash=0
    ))
    return result


def id_already_downloaded(date, channel, id):
    try:
        dirlist = os.listdir(f'{FOLDER}/{date}/telegram/{channel}')
        ids = [int(entry.split('.')[0]) for entry in dirlist]

        return id in ids
    except FileNotFoundError:
        return False


def main():
    # The first parameter is the .session file name (absolute paths allowed)
    with TelegramClient('timecapsule', API_ID, API_HASH) as client:
        tomorrow = datetime.now() + timedelta(days=1)

        for i, msg in enumerate(tqdm(client.iter_messages(TELEGRAM_CHANNEL, offset_date=tomorrow))):
            message_date = msg.date.strftime('%Y%m%d')

            if not id_already_downloaded(message_date, TELEGRAM_CHANNEL, msg.id):
                path = os.path.join(FOLDER, message_date, 'telegram', TELEGRAM_CHANNEL, f'{msg.id}')
                print(path)
                msg.download_media(file=path)


if __name__ == '__main__':
    main()
