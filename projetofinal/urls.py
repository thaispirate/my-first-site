from django.conf.urls import include, url, patterns, handler404
from . import views
from .forms import Cadastro1Form, Cadastro2Form, Cadastro3Form, Cadastro4Form, Cadastro5Form, Cadastro6Form, Cadastro7Form, Cadastro8Form, Cadastro9Form, EmailAuthenticationForm
from .views import CadastroWizard, EditarCadastro, PsicologoPaciente

handler404="views.erro404"

urlpatterns = [
    url(r'^$', views.Home),
    url(r'^home$', views.Home),
    url(r'^administracao$', views.LoginPsicologo),
    url(r'^psicologo$', views.Psicologo),
    url(r'^sair$', views.LogoutView),
    url(r'^erro404$', views.Erro404),
    url(r'^cadastro$', CadastroWizard.as_view([Cadastro1Form,Cadastro2Form,Cadastro3Form,Cadastro4Form,Cadastro5Form,Cadastro6Form,Cadastro7Form,Cadastro8Form]), name="cadastro"),
    url(r'^cadastrado$', views.CadastroRealizado),
    url(r'^editado$', views.EdicaoRealizada),
    url(r'^login$', 'django.contrib.auth.views.login', {'template_name':'projetofinal/login.html','authentication_form': EmailAuthenticationForm}, name='login'),
    url(r'^cadastro/editar/(?P<paciente_id>\d+)/$', EditarCadastro.as_view([Cadastro9Form,Cadastro2Form,Cadastro3Form,Cadastro4Form,Cadastro5Form,Cadastro6Form,Cadastro7Form,Cadastro8Form]), name="editar"),
    url(r'^psicologo/paciente/(?P<paciente_id>\d+)/$', PsicologoPaciente.as_view()),
    url(r'^recover/(?P<signature>.+)/$', views.recover_done,
        name='password_reset_sent'),
    url(r'^recover$', views.recover, name='password_reset_recover'),
    url(r'^reset/done/$', views.reset_done, name='password_reset_done'),
    url(r'^reset/(?P<token>[\w:-]+)/$', views.reset,
        name='password_reset_reset'),
]
