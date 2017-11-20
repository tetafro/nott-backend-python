from django.contrib.auth.decorators import user_passes_test
from django.db.models import Count
from django.shortcuts import render

from .models import Config
from ..users.models import User


@user_passes_test(lambda u: u.is_admin)
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
        if 'lock' in request.POST:
            # TODO: Add code
            pass
        elif 'remove' in request.POST:
            # TODO: Add code
            pass

    context = {'users': users, 'configs': configs}
    return render(request, 'admin/adminpanel.html', context)
