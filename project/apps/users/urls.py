from django.conf.urls import url

from core.api import token_required
from .views import LoginView, RegisterView, LogoutView, UserView


urlpatterns = [
    url(r'^register/?$', RegisterView.as_view(), name='register'),
    url(r'^login$/?', LoginView.as_view(), name='login'),
    url(r'^logout$/?', token_required(LogoutView.as_view()), name='logout'),
    url(r'^users/?$', token_required(UserView.as_view())),
    url(r'^users/(?P<id>\d+)/?$', token_required(UserView.as_view())),
]
