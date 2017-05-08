from django.conf.urls import include, url, patterns
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'', include('projetofinal.urls')),
    url(r'', include('password_reset.urls')),
#    url(r'^autocomplete/', include('autocomplete_light.urls')),
]
