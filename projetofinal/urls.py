from django.conf.urls import include, url, patterns
from . import views
from .views import CadastrarPaciente, CadastroRealizado

urlpatterns = [
    url(r'^home$', views.home),
    url(r'^cadastro$', CadastrarPaciente.as_view(), name="cadastro"),
    url(r'^cadastrado$', CadastroRealizado.as_view(), name="cadastro_realizado"),
    url(r'^$', 'django.contrib.auth.views.login', {'template_name':'projetofinal/base.html'}, name='login'),
    url(r'^sair/$', 'django.contrib.auth.views.logout_then_login', name='logout')
]
