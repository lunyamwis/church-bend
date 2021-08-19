from graphql import GraphQLError

from .validation_errors import error_dict


def validate_object_id(id, model, entity, agency=None):
    '''
    Checks if an object that ID exists in the db
    Args:
        id (str): object id
        model (obj): client model object
        entity (str): entity name
        agency (obj): agency object
    Raise:
        raise GraphQLError if the object does not exist
    Return:
        obj (obj): model object
    '''
    if not id:
        raise GraphQLError(error_dict['empty_field'].format('id field'))
    try:
        obj = model.objects.get(id=id)
        if agency:
            obj = model.objects.get(id=id, agency=agency)
    except model.DoesNotExist:
        raise GraphQLError(error_dict['does_not_exist'].format(entity))
    return obj
