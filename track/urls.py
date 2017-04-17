from django.conf.urls import url

from . import views

urlpatterns = [
	# views.py

    url(r'^issue/$', views.index, name='index'),
    url(r'^issue/(?P<idx>\d+)/$', views.issue_details, name='detail'),
]