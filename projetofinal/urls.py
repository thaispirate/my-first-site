from django.conf.urls import include, url, patterns, handler404
from . import views
from .forms import Cadastro1Form, Cadastro2Form, Cadastro3Form, Cadastro4Form, Cadastro5Form, Cadastro6Form, Cadastro7Form, Cadastro8Form, Cadastro9Form
from .views import CadastroRealizado,CadastroWizard, EditarCadastro, PacienteNaoExiste

handler404="views.erro404"

urlpatterns = [
    url(r'^$', views.home),
    url(r'^home$', views.home),
    url(r'^erro404$', views.erro404),
    url(r'^cadastro$', CadastroWizard.as_view([Cadastro1Form,Cadastro2Form,Cadastro3Form,Cadastro4Form,Cadastro5Form,Cadastro6Form,Cadastro7Form,Cadastro8Form]), name="cadastro"),
    url(r'^cadastrado$', CadastroRealizado.as_view(), name="cadastro_realizado"),
    url(r'^paciente_invalido$', PacienteNaoExiste.as_view(), name="paciente_invalido"),
    url(r'^login$', 'django.contrib.auth.views.login', {'template_name':'projetofinal/login.html'}, name='login'),
    url(r'^cadastro/editar/(?P<paciente_id>\d+)/$', EditarCadastro.as_view([Cadastro9Form,Cadastro2Form,Cadastro3Form,Cadastro4Form,Cadastro5Form,Cadastro6Form,Cadastro7Form,Cadastro8Form]), name="editar"),
    url(r'^sair/$', 'django.contrib.auth.views.logout_then_login', name='logout'),
    # url(r'^password_reset$', 'django.contrib.auth.views.password_reset',  {'post_reset_redirect' : 'password/reset/done/'}, name='password_reset'),
    # url(r'^password/reset/done/$','django.contrib.auth.views.password_reset_done'),
    # url(r'^password/reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$','django.contrib.auth.views.password_reset_confirm',{'post_reset_redirect' : 'password/done/'}),
    # url(r'^password/done/$','django.contrib.auth.views.password_reset_complete'),
    url(r'^recover/(?P<signature>.+)/$', views.recover_done,
        name='password_reset_sent'),
    url(r'^recover$', views.recover, name='password_reset_recover'),
    url(r'^reset/done/$', views.reset_done, name='password_reset_done'),
    url(r'^reset/(?P<token>[\w:-]+)/$', views.reset,
        name='password_reset_reset'),
]
