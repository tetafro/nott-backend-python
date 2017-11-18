from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render


@user_passes_test(lambda u: u.is_admin)
def adminpanel(request):
    """Main page of admin panel"""

    context = {}
    return render(request, 'admin/adminpanel.html', context)
