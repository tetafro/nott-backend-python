from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^register/$', views.user_auth, name='register'),
    url(r'^login/$', views.user_auth, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^$', views.index, name='index'),
    url(r'^users/$', views.userlist, name='userlist'),
]
