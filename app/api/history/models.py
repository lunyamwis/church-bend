import re

from django.dispatch import receiver
from simple_history.signals import (post_create_historical_record,
                                    pre_create_historical_record)








@receiver(pre_create_historical_record)
def pre_create_historical_record_callback(*args, **kwargs):
    """
    Callback to create model history
    """
    history = kwargs.get("history_instance", '')
    if history.history_type == "+":
        model = re.sub(r'(?<!^)(?=[A-Z])', ' ',
                       kwargs.get("instance").__class__.__name__)
        history.history_change_reason = [f"Created {model}"]


@receiver(post_create_historical_record)
def post_create_historical_record_callback(*args, **kwargs):
    history = kwargs.get("history_instance", '')
    if history.prev_record and not history.history_change_reason:
        history.delete()
