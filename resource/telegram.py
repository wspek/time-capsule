import logging
import os
from datetime import datetime, timedelta

import humanize
from telethon.errors.rpcerrorlist import FileReferenceExpiredError
from telethon.sync import TelegramClient
from tqdm import tqdm

from config import config
from .resource import Resource
from utils import file_exists_on_disk

logging.getLogger('telethon').setLevel(logging.WARNING)


class TelegramResource(Resource):
    type = 'Telegram'

    def download_all(self):
        logging.info('Opening connection with Telegram client.')

        with TelegramClient('timecapsule', self.connection_data['api_id'], self.connection_data['api_hash']) as client:
            self._download_messages(client)

        logging.info(f"Sending report to {','.join(config['email']['mailinglist'])}")

        self._report.email(config['email']['mailinglist'])

    def _download_messages(self, client):
        for channel in self.download_data['channels']:
            logging.info(f'Retrieving messages for channel: {channel}')
            self._download_channel_messages(client, channel)

    def _download_channel_messages(self, client, channel):
        tomorrow = datetime.now() + timedelta(days=1)

        logging.info(f'Retrieving all messages older than {str(tomorrow)}')

        for i, msg in enumerate(tqdm(client.iter_messages(channel, offset_date=tomorrow))):
            message_date = msg.date.strftime('%Y%m%d')
            folder = os.path.join(self.out_folder, message_date, 'telegram', channel)
            filename = str(msg.id)

            if not file_exists_on_disk(folder, filename):
                path = f'{folder}/{filename}'
                self._download_and_report_message(msg, channel, path)
            else:
                logging.debug(f'Skipping {msg.id} (already downloaded)')
                continue

    def _download_and_report_message(self, msg, channel_name, path) -> None:
        logging.debug(f'Attempting to download: {msg.id}')

        try:
            saved_path = msg.download_media(file=path)
        except FileReferenceExpiredError:
            logging.debug(f'File reference expired.')
            return

        if saved_path:
            content = f'{saved_path} ({humanize.naturalsize(msg.file.size)})'

            logging.debug(f'Saved: {content}')

            self._report.add_content(
                msg.date.strftime('%Y%m%d'),
                channel_name,
                content=content,
            )
        else:
            logging.debug('Not a media file.')
