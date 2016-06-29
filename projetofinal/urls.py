from django.conf.urls import include, url, patterns, handler404
from . import views
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from .forms import CadastroPaciente,CadastroConjuge,CadastroPai,CadastroMae,CadastroAvoPaterno,CadastroAvoPaterna,\
    CadastroAvoMaterno, CadastroAvoMaterna,EdicaoPaciente, CadastroPsicologoForm
from .views import CadastroWizard, EditarCadastro, PsicologoPaciente, CadastroPsicologoWizard,\
    InserirAnalise,InserirAnaliseRelacionamento,InserirAnaliseIndiferenciacao,InserirAnaliseSeletiva,InserirAnaliseInterventiva,\
    ConsultarAnalise, ConsultandoAnalise,AnalisePaciente, ConsultandoAnalisePaciente,\
    ProsseguirAnalise, ProsseguindoAnalise,Recomendacoes,RecomendacaoAreaAfetiva

handler404="views.erro404"

urlpatterns = [

    # Paciente
    url(r'^$', views.Home),
    url(r'^home$', views.Home),
    url(r'^sair$', views.LogoutView),
    url(r'^erro404$', views.Erro404),
    url(r'^cadastro$', CadastroWizard.as_view([CadastroPaciente,CadastroConjuge,CadastroPai,CadastroMae,CadastroAvoPaterno,CadastroAvoPaterna,CadastroAvoMaterno,CadastroAvoMaterna]), name="cadastro"),
    url(r'^cadastrado$', views.CadastroRealizado),
    url(r'^editado$', views.EdicaoRealizada),
    url(r'^login$', views.LoginPaciente),
    url(r'^cadastro/editar/(?P<paciente_id>\d+)/$', EditarCadastro.as_view([EdicaoPaciente,CadastroConjuge,CadastroPai,CadastroMae,CadastroAvoPaterno,CadastroAvoPaterna,CadastroAvoMaterno,CadastroAvoMaterna]), name="editar"),
    url(r'^recover/(?P<signature>.+)/$', views.recover_done,
        name='password_reset_sent'),
    url(r'^recover$', views.recover, name='password_reset_recover'),
    url(r'^reset/done/$', views.reset_done, name='password_reset_done'),
    url(r'^reset/(?P<token>[\w:-]+)/$', views.reset,
        name='password_reset_reset'),
    url(r'^analise/inserir/(?P<paciente_id>\d+)/$', InserirAnalise.as_view()),
    url(r'^analise/inserir/(?P<paciente_id>\d+)/(?P<analise_id>\d+)/recomendacao/areaafetiva$', RecomendacaoAreaAfetiva.as_view(template_name="projetofinal/analise/areaAfetiva.html")),
    url(r'^analise/inserir/(?P<paciente_id>\d+)/(?P<analise_id>\d+)/relacionamentos$', InserirAnaliseRelacionamento.as_view()),
    url(r'^analise/inserir/(?P<paciente_id>\d+)/(?P<analise_id>\d+)/indiferenciacao$', InserirAnaliseIndiferenciacao.as_view()),
    url(r'^analise/inserir/(?P<paciente_id>\d+)/(?P<analise_id>\d+)/seletiva$', InserirAnaliseSeletiva.as_view()),
    url(r'^analise/inserir/(?P<paciente_id>\d+)/(?P<analise_id>\d+)/interventiva$', InserirAnaliseInterventiva.as_view()),
    url(r'^analise/iniciada$', views.AnaliseFinalizada),
    url(r'^analise/consultar/(?P<paciente_id>\d+)/$', ConsultarAnalise.as_view(), name="consultar"),
    url(r'^analise/consultar/(?P<paciente_id>\d+)/(?P<analise_id>\d+)$', ConsultandoAnalise.as_view(), name="consultando"),
    url(r'^analise/prosseguir/(?P<paciente_id>\d+)/$', ProsseguirAnalise.as_view(), name="prosseguir"),
    url(r'^analise/prosseguir/(?P<paciente_id>\d+)/(?P<analise_id>\d+)$', views.ProsseguindoAnalise, name="prosseguindo"),
    url(r'^analise/prosseguir/(?P<paciente_id>\d+)/remover$', views.RemoverAnalise, name="remover"),
    url(r'^analise/consultar/(?P<paciente_id>\d+)/remover$', views.RemoverAnalise, name="remover"),
    url(r'^analise/recomendacao/(?P<paciente_id>\d+)/$', Recomendacoes.as_view()),
    url(r'^analise/recomendacao/(?P<paciente_id>\d+)/(?P<analise_id>\d+)/areaafetiva$', RecomendacaoAreaAfetiva.as_view(template_name="projetofinal/analise/recomendacao/areaAfetiva.html")),

    #Psicólogo
    url(r'^psicologo/administracao$', views.PsicologoAdministracao),
    url(r'^psicologo/login$', views.LoginPsicologo),
    url(r'^psicologo/home$', views.PsicologoHome),
    url(r'^psicologo/cadastro$', CadastroPsicologoWizard.as_view([CadastroPsicologoForm]), name="cadastroPsicologo"),
    url(r'^psicologo/cadastrado$', views.CadastroPsicologoRealizado),
    url(r'^psicologo/paciente/(?P<paciente_id>\d+)/$', PsicologoPaciente.as_view()),
    url(r'^psicologo/sair$', views.LogoutPsicologo),
    url(r'^psicologo/paciente/(?P<paciente_id>\d+)/analise$', view=AnalisePaciente.as_view()),
    url(r'^psicologo/paciente/(?P<paciente_id>\d+)/(?P<analise_id>\d+)$', ConsultandoAnalisePaciente.as_view(), name="consultar")

]
