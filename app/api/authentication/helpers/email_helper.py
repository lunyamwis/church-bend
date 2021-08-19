from django.template.loader import render_to_string
from django.conf import settings
from ...helpers.tasks import send_mail_


def template_email(*args, **kwargs):
    """
    Function to template email and send it
    Args:
        subject (str): email subject
        args (list): list of possible arguments
        kwargs (dict): key worded arguments
    Returns:
        None
    """
    template_name, recipient, subject, message = args
    body = render_to_string(template_name, kwargs)
    send_mail_.delay(
        subject=subject,
        message=message,
        from_email=settings.EMAIL_SENDER,
        recipient_list=[recipient],
        html_message=body,
        fail_silently=False,)
