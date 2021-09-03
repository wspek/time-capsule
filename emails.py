import yagmail

from config import config


def send_email(to, subject, body):
    sender_config = config['email']['sender']

    yag = yagmail.SMTP({sender_config['address']: sender_config['name']}, sender_config['password'])
    yag.send(
        to=to,
        subject=subject,
        contents=body,
    )
