from django.urls import include, path
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('projetofinal.urls')),
    path('', include('password_reset.urls')),
    path('chaining/', include('smart_selects.urls')),
]
