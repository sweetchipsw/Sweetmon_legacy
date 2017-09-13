from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout, views
from django.conf import settings
from django.conf.urls.static import static
import monitor.views as monview


urlpatterns = [
	url(r'^$',include('monitor.urls'), name='index'),
    url(r'^admin/', include(admin.site.urls)),
	url(r'^fuzzer/$', monview.fuzzer_list, name='fuzzers'),  # machine list
	url(r'^fuzzer/(?P<idx>\d+)/$', monview.fuzzer_details, name='fuzzer_details'),  # machine list
	url(r'^crash/$', monview.crash_list, name='crash_list'),  # crashlist
	url(r'^crash/(?P<idx>\d+)/$', monview.crash_details, name='crash_detail'),
	url(r'^crash/(?P<idx>\d+)/dup$', monview.crash_details_dupcrash, name='crash_details_dupcrash'),
	url(r'^crash/(?P<idx>\d+)/modify$', monview.crash_details_modify, name='modify'),
	url(r'^settings/$', monview.settings_page, name='settings'),
	url(r'^fuzz/', include('fuzz.urls')),
    url(r'^testcase/', include('testcase.urls')),
    url(r'^issue/', include('track.urls')),
    url(r'^account/login/',auth_views.login,name='login',kwargs={'template_name': 'login.html'}),
    url(r'^account/logout/',auth_views.logout,name='logout',kwargs={'next_page': settings.LOGIN_URL,}),
]

if settings.DEBUG is True:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)