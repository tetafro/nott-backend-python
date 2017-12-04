from django.conf import settings
from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import ValidationError
from django.db import models, IntegrityError
from django.db.models import Count
from django.shortcuts import render

from core.errors import Http400
from apps.users.models import User
from .models import Config


@user_passes_test(lambda u: u.is_authenticated() and u.is_admin)
def adminpanel(request):
    """Main page of admin panel"""

    configs = Config.objects.all()
    users = User.objects.\
        annotate(folders_count=Count(
            'folders',
            distinct=True
        )).\
        annotate(notepads_count=Count(
            'folders__notepads',
            distinct=True
        )).\
        annotate(notes_count=Count(
            'folders__notepads__notes',
            distinct=True
        )).\
        all()

    if request.method == 'POST':
        for field, value in request.POST.items():
            if field == 'csrfmiddlewaretoken':
                continue

            try:
                config = Config.objects.get(code=field)
            except Config.DoesNotExist:
                raise Http400
            config.value = value
            try:
                config.full_clean()
            except ValidationError as e:
                raise Http400
            try:
                config.save()
            except IntegrityError:
                raise Http400

    context = {
        'users': users,
        'configs': configs,
        'version': settings.VERSION
    }
    return render(request, 'admin/adminpanel.html', context)
