# Standard modules
import json

# Validation exceptions
from django.core.exceptions import ValidationError, NON_FIELD_ERRORS
from django.db import IntegrityError

from django.http import HttpResponse


def object_required(ObjectClass):
    """ Checking if object with given id exists """

    def decorator(fn):
        def wrapped(self, request, *args, **kwargs):
            id_field = ObjectClass.__name__.lower() + '_id'
            if id_field not in kwargs:
                response = {'error': 'Bad request'}
                return ajax_response(response, 400)

            obj_id = kwargs[id_field]
            if not ObjectClass.objects.filter(id=obj_id).exists():
                response = {'error': 'Not found'}
                return ajax_response(response, 400)

            return fn(self, request, *args, **kwargs)

        return wrapped

    return decorator


def object_save(obj):
    """ Full clean, save and return errors if occured """

    try:
        obj.full_clean()
    except ValidationError as e:
        error_message = ', '.join(e.message_dict[NON_FIELD_ERRORS])
        response = {'error': error_message}
        return response, 400

    try:
        obj.save()
    except IntegrityError as e:
        response = {'error': 'Bad request'}
        return response, 400

    return True


def ajax_response(response, status):
    return HttpResponse(
        json.dumps(response),
        status=status,
        content_type='application/json'
    )