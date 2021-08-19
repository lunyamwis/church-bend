'''JWT token generation'''
from datetime import datetime, timedelta
import jwt
from django.conf import settings
from .jwt_errors import error_dict as jwt_errors


def generate_jwt(email, agency_id, password_reset=False, username=None):
    """
    Encoding of the token using the user email
    Args:
        email (str): user email
        agency_id (str): insurance agency ID
    Return:
        (str): encoded token
    """
    payload = {
        'email': email,
        'agency_id': agency_id,
        'exp': datetime.utcnow() + timedelta(minutes=60)
    }
    if password_reset:
        del payload['email']
        payload['username'] = username
    return jwt.encode(payload, settings.SECRET_KEY,
                      algorithm='HS256').decode('utf-8')


def decode_jwt(token):
    """
    Decode the token to get the payload
    Args:
        email (str): user email
    Return:
        payload (str): encoded token
    """
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=['HS256'],
            options={
                'verify_signature': True,
                'verify_exp': True
            })
    except (
        ValueError,
        TypeError,
        jwt.ExpiredSignatureError,
        jwt.DecodeError,
        jwt.InvalidSignatureError,
        jwt.InvalidAlgorithmError,
        jwt.InvalidIssuerError,
    ) as error:
        exception_mapper = {
            ValueError: (jwt_errors['SERVER_ERROR_MESSAGE'], 500),
            TypeError: (jwt_errors['SERVER_ERROR_MESSAGE'], 500),
            jwt.ExpiredSignatureError: (jwt_errors['EXPIRED_TOKEN_MSG'],
                                        401),
            jwt.DecodeError: (jwt_errors['INVALID_TOKEN_MSG'], 401),
            jwt.InvalidIssuerError: (jwt_errors['ISSUER_ERROR'], 401),
            jwt.InvalidAlgorithmError: (jwt_errors['ALGORITHM_ERROR'],
                                        401),
            jwt.InvalidSignatureError: (jwt_errors['SIGNATURE_ERROR'], 500)
        }
        message, status_code = exception_mapper.get(
            type(error), (jwt_errors['SERVER_ERROR_MESSAGE'], 500))
        return {'message': message}, status_code

    return payload, 200
