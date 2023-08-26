import os
import logging
from datetime import datetime, timedelta

# https://tl.telethon.dev/
from telethon.sync import TelegramClient
from telethon.errors.rpcerrorlist import FileReferenceExpiredError
from tqdm import tqdm
import humanize

from config import config
from .resource import Resource


logging.getLogger('telethon').setLevel(logging.WARNING)


def id_already_downloaded(folder, date, channel, id):
    try:
        dirlist = os.listdir(f'{folder}/{date}/telegram/{channel}')
        ids = [int(entry.split('.')[0]) for entry in dirlist]

        return id in ids
    except FileNotFoundError:
        return False


class TelegramResource(Resource):
    type = 'Telegram'

    def connect(self):
        raise NotImplementedError

    def download_all(self):
        logging.info('Opening connection with Telegram client.')

        with TelegramClient('timecapsule', self.connection_data['api_id'], self.connection_data['api_hash']) as client:
            tomorrow = datetime.now() + timedelta(days=1)

            logging.info(f'Retrieving all messages older than {str(tomorrow)}')

            for channel in self.download_data['channels']:
                logging.info(f'Retrieving messages for channel: {channel}')

                for i, msg in enumerate(tqdm(client.iter_messages(channel, offset_date=tomorrow))):
                    message_date = msg.date.strftime('%Y%m%d')

                    if not id_already_downloaded(self.out_folder, message_date, channel, msg.id):
                        logging.debug(f'Attempting to download: {msg.id}')

                        path = os.path.join(self.out_folder, message_date, 'telegram', channel, f'{msg.id}')

                        try:
                            saved_path = msg.download_media(file=path)
                        except FileReferenceExpiredError:
                            logging.debug(f'File reference expired.')
                            continue

                        if saved_path:
                            content = f'{saved_path} ({humanize.naturalsize(msg.file.size)})'

                            logging.debug(f'Saved: {content}')

                            self._report.add_content(
                                message_date,
                                channel,
                                content=content,
                            )
                        else:
                            logging.debug('Not a media file.')
                            continue
                    else:
                        logging.debug(f'Skipping {msg.id} (already downloaded)')

        logging.info(f"Sending report to {','.join(config['email']['mailinglist'])}")

        self._report.email(config['email']['mailinglist'])
