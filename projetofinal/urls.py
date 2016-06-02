from django.conf.urls import include, url, patterns, handler404
from . import views
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from .forms import Cadastro1Form, Cadastro2Form, Cadastro3Form, Cadastro4Form, Cadastro5Form, Cadastro6Form, \
    Cadastro7Form, Cadastro8Form, Cadastro9Form, CadastroPsicologoForm, IniciarAreaAfetiva, ConsultarAreaAfetiva
from .views import CadastroWizard, EditarCadastro, PsicologoPaciente, CadastroPsicologoWizard,\
    InserirAnalise, ConsultarAnalise, ConsultandoAnalise,AnalisePaciente, ConsultandoAnalisePaciente, RemoverAnalise

handler404="views.erro404"

urlpatterns = [

    # Paciente
    url(r'^$', views.Home),
    url(r'^home$', views.Home),
    url(r'^sair$', views.LogoutView),
    url(r'^erro404$', views.Erro404),
    url(r'^cadastro$', CadastroWizard.as_view([Cadastro1Form,Cadastro2Form,Cadastro3Form,Cadastro4Form,Cadastro5Form,Cadastro6Form,Cadastro7Form,Cadastro8Form]), name="cadastro"),
    url(r'^cadastrado$', views.CadastroRealizado),
    url(r'^editado$', views.EdicaoRealizada),
    url(r'^login$', views.LoginPaciente),
    url(r'^cadastro/editar/(?P<paciente_id>\d+)/$', EditarCadastro.as_view([Cadastro9Form,Cadastro2Form,Cadastro3Form,Cadastro4Form,Cadastro5Form,Cadastro6Form,Cadastro7Form,Cadastro8Form]), name="editar"),
    url(r'^recover/(?P<signature>.+)/$', views.recover_done,
        name='password_reset_sent'),
    url(r'^recover$', views.recover, name='password_reset_recover'),
    url(r'^reset/done/$', views.reset_done, name='password_reset_done'),
    url(r'^reset/(?P<token>[\w:-]+)/$', views.reset,
        name='password_reset_reset'),
    url(r'^analise/inserir/(?P<paciente_id>\d+)/$', InserirAnalise.as_view([IniciarAreaAfetiva])),
    url(r'^analise/iniciada$', views.AnaliseIniciada),
    url(r'^analise/consultar/(?P<paciente_id>\d+)/$', ConsultarAnalise.as_view(), name="consultar"),
    url(r'^analise/consultar/(?P<paciente_id>\d+)/(?P<analise_id>\d+)$', ConsultandoAnalise.as_view([ConsultarAreaAfetiva]), name="consultando"),
    url(r'^analise/consultar/(?P<paciente_id>\d+)/remover$', views.RemoverAnalise, name="remover"),

    #Psicólogo
    url(r'^psicologo/administracao$', views.PsicologoAdministracao),
    url(r'^psicologo/login$', views.LoginPsicologo),
    url(r'^psicologo/home$', views.PsicologoHome),
    url(r'^psicologo/cadastro$', CadastroPsicologoWizard.as_view([CadastroPsicologoForm]), name="cadastroPsicologo"),
    url(r'^psicologo/cadastrado$', views.CadastroPsicologoRealizado),
    url(r'^psicologo/paciente/(?P<paciente_id>\d+)/$', PsicologoPaciente.as_view()),
    url(r'^psicologo/sair$', views.LogoutPsicologo),
    url(r'^psicologo/paciente/(?P<paciente_id>\d+)/analise$', view=AnalisePaciente.as_view()),
    url(r'^psicologo/paciente/(?P<paciente_id>\d+)/(?P<analise_id>\d+)$', ConsultandoAnalisePaciente.as_view([ConsultarAreaAfetiva]), name="consultar")

]
