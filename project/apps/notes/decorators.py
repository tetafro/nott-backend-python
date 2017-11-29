from django.http import JsonResponse


def object_required(ObjectClass):
    """ Checking if object with given id exists """

    def decorator(fn):
        def wrapped(self, request, *args, **kwargs):
            try:
                obj_id = kwargs['id']
            except KeyError:
                response = {'error': 'No id provided'}
                return JsonResponse(response, status=400)

            if not ObjectClass.objects.filter(id=obj_id).exists():
                response = {'error': 'Object not found'}
                return JsonResponse(response, status=404)

            return fn(self, request, *args, **kwargs)

        return wrapped

    return decorator
