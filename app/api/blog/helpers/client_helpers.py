
from ..models import Client


def get_default_client_status():
    '''
    Get default client options
    Returns:
        data (dict): client options
    '''
    data = {
        "statusOptions": {
            k: str(v) for k, v in dict(Client.STATUS_CHOICES).items()}

    }
    return data
