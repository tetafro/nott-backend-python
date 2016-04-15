from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^register$', views.user_auth, name='register'),
    url(r'^login$', views.user_auth, name='login'),
    url(r'^logout$', views.user_logout, name='logout'),
    url(r'^users$', views.userlist, name='userlist'),
    url(r'^users/me$', views.profile, {'user_id': 'me'}, name='profile'),
    url(r'^users/(?P<user_id>\d+)$', views.profile, name='profile'),
    url(r'^users/me/edit$', views.profile_edit, name='profile_edit')
]
