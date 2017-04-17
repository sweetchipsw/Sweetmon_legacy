from django.conf.urls import url

from . import views

urlpatterns = [
	# views.py
    url(r'^$', views.index, name='index'),
    url(r'^fuzzer/$', views.fuzzer_list, name='fuzzers'), # machine list
    url(r'^fuzzer/(?P<idx>\d+)/$', views.fuzzer_details, name='fuzzer_details'), # machine list
    url(r'^crash/$', views.crash_list, name='crash_list'), # crashlist
    url(r'^crash/(?P<idx>\d+)/$', views.crash_details, name='crash_detail'),
    url(r'^crash/(?P<idx>\d+)/modify$', views.crash_details_modify, name='modify'),
]