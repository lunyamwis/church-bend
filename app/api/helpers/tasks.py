import json
import logging

from app import celery_app
from django.conf import settings
from django.core.mail import send_mail
from twilio.rest import Client


@celery_app.task(name="send mail")
def send_mail_(*args, **kwargs):
    """
    handle sending of mails to users
    Args:
        args (list): a list of possible arguments
        kwargs (dict): key worded arguments
    Return:
        None
    """
    try:
        send_mail(**kwargs)
    except Exception as e:
        logging.warning(e)


@celery_app.task(name="send text message")
def send_sms(message, phone_numbers):
    """
    send sms using twilio
    Args:
        message (str): sms body
        phone_numbers (list): recipient phone numbers
    Return:
        None
    """

    ACCOUNT_SID = settings.TWILIO_ACC_SID
    AUTH_TOKEN = settings.TWILIO_ACC_AUTH_TOKEN
    NOTIFY_SERVICE_SID = settings.TWILIO_NOTIFY_SERVICE_SID

    client = Client(ACCOUNT_SID, AUTH_TOKEN)

    bindings = list(map(lambda number: json.dumps(
        {'binding_type': 'sms', 'address': number}), phone_numbers))

    try:
        client.notify.services(NOTIFY_SERVICE_SID).notifications.create(
            to_binding=bindings,
            body=message)
    except Exception as e:
        logging.warning(e)
