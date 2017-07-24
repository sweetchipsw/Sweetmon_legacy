from django.conf.urls import url

from . import views

urlpatterns = [
    # url(r'^fuzz/', include('monitor.urls')),
    # url(r'^register/', include('register.urls')),
    # url(r'^report/', include('report.urls')),

    url(r'^ping$', views.ping, name='ping'),
    url(r'^testcase$', views.status, name='status'),
    url(r'^crash$', views.crash, name='crash'),
    url(r'^register$', views.register, name='register'),

    url(r'^geturl$', views.generateToken, name='geturl'),
    url(r'^download$', views.downloadFileByToken, name='download'),
    url(r'^alert$', views.alert, name='alert'),
    url(r'^alert_test$', views.alert_test, name='alert_test'),

]