import yagmail

from config import config


def send_email(to, subject, body):
    sender_config = config['email']['sender']

    yag = yagmail.SMTP(user=sender_config['address'], password=sender_config['password'])
    yag.send(to=to, subject=subject, contents=body)
