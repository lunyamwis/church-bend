from django.http import HttpResponse
from django.template.loader import render_to_string

from ..helpers.jwt_helper import decode_jwt
from .models import User


def activate_account(request, token):
    """
    Function to activate user account
    Args:
        request (obj): request object
        token (str): user JWT token

    """
    DEFAULT_PARAMS = {
        'status_code': 403,
        "message": "Something went wrong.",
        "status": "Unauthorized"
    }
    payload, status_code = decode_jwt(token)
    if status_code != 200:
        rendered = render_to_string('unauthorized-403.html', DEFAULT_PARAMS)
        response = HttpResponse(rendered)
        return response
    user = User.objects.filter(email=payload['email']).first()
    if not user:
        if User.objects.deleted_only().filter(
                email=payload['email']).first():
            params = DEFAULT_PARAMS.copy()
            params['message'] = 'Account deactivated'
            rendered = render_to_string('unauthorized-403.html', params)
            response = HttpResponse(rendered)
        else:
            params = DEFAULT_PARAMS.copy()
            params['status_code'] = 500
            params['status'] = 'Error'
            rendered = render_to_string('unauthorized-403.html', params)
            response = HttpResponse(rendered)
        return response
    if not user.is_active:
        if user.is_superuser:
            user.is_password_set = True
        user.is_active = True
        user.save()
        params = {
            'message': 'Your account has been activated successfully'
        }
        rendered = render_to_string('custom-actions.html', params)
        response = HttpResponse(rendered)
    elif user and user.is_active:
        params = {
            'message': 'Your account is currently active'
        }
        rendered = render_to_string('custom-actions.html', params)
        response = HttpResponse(rendered)
    return response
