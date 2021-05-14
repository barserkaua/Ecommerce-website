from urllib import request

from django.conf.urls import url

from . import views

app_name = 'search'
urlpatterns = [
    url(r'^$', views.ESearchView.as_view(), name='search_result'),
]