from django.conf.urls import url
from . import paciente,psicologo,analise
from .forms import CadastroPaciente,CadastroConjuge,CadastroPai,CadastroMae,CadastroAvoPaterno,CadastroAvoPaterna,\
    CadastroAvoMaterno, CadastroAvoMaterna,EdicaoPaciente, CadastroPsicologoForm
from .paciente import Home,CadastroWizard, EditarCadastro,AtualizarChave
from .psicologo import PsicologoPaciente, CadastroPsicologoWizard,AnalisePaciente, ConsultandoAnalisePaciente, GenogramaPaciente

from .analise import InserirAnalise,InserirAnaliseRelacionamento,InserirAnaliseIndiferenciacao,InserirAnaliseSeletiva,InserirAnaliseInterventiva,\
    AnaliseFinalizada,ConsultarAnalise, ConsultandoAnalise,\
    ProsseguirAnalise,Recomendacoes,ConsultandoRecomendacoes, RecomendacaoAreaAfetiva, RecomendacaoIndiferenciacao,\
    RecomendacaoSeletiva,RecomendacaoTarefas, RecomendacaoInterventiva,\
    ResumoAreaAfetiva, ResumoRelacionamento, ResumoSeletiva,ResumoTarefas, ResumoExercicios, ResumoInterventiva

handler404="paciente.erro404"

urlpatterns = [

    # Paciente
    url(r'^$', Home.as_view()),
    url(r'^home/(?P<paciente_id>\d+)/$', Home.as_view()),
    url(r'^sair$', paciente.LogoutView),
    url(r'^erro404$', paciente.Erro404),
    url(r'^cadastro$', CadastroWizard.as_view([CadastroPaciente,CadastroConjuge,CadastroPai,CadastroMae,CadastroAvoPaterno,CadastroAvoPaterna,CadastroAvoMaterno,CadastroAvoMaterna]), name="cadastro"),
    url(r'^cadastrado$', paciente.CadastroRealizado),
    url(r'^editado$', paciente.EdicaoRealizada),
    url(r'^login$', paciente.LoginPaciente),
    url(r'^cadastro/editar/(?P<paciente_id>\d+)/$', EditarCadastro.as_view([EdicaoPaciente,CadastroConjuge,CadastroPai,CadastroMae,CadastroAvoPaterno,CadastroAvoPaterna,CadastroAvoMaterno,CadastroAvoMaterna]), name="editar"),
    url(r'^atualizar_chave/(?P<paciente_id>\d+)/$', AtualizarChave.as_view()),
    url(r'^recover/(?P<signature>.+)/$', paciente.recover_done,
        name='password_reset_sent'),
    url(r'^recover$', paciente.recover, name='password_reset_recover'),
    url(r'^reset/done/$', paciente.reset_done, name='password_reset_done'),
    url(r'^reset/(?P<token>[\w:-]+)/$', paciente.reset,
        name='password_reset_reset'),

    # Análise
    url(r'^analise/resumo/(?P<paciente_id>\d+)/areaafetiva$', ResumoAreaAfetiva.as_view()),
    url(r'^analise/resumo/(?P<paciente_id>\d+)/(?P<analise_id>\d+)/relacionamentos$', ResumoRelacionamento.as_view()),
    url(r'^analise/resumo/(?P<paciente_id>\d+)/(?P<analise_id>\d+)/seletiva$', ResumoSeletiva.as_view()),
    url(r'^analise/resumo/(?P<paciente_id>\d+)/(?P<analise_id>\d+)/tarefas$', ResumoTarefas.as_view()),
    url(r'^analise/resumo/(?P<paciente_id>\d+)/(?P<analise_id>\d+)/exercicios$', ResumoExercicios.as_view()),
    url(r'^analise/resumo/(?P<paciente_id>\d+)/(?P<analise_id>\d+)/interventiva$', ResumoInterventiva.as_view()),
    url(r'^analise/inserir/(?P<paciente_id>\d+)/$', InserirAnalise.as_view()),
    url(r'^analise/inserir/(?P<paciente_id>\d+)/(?P<analise_id>\d+)/recomendacao/areaafetiva$', RecomendacaoAreaAfetiva.as_view(template_name="projetofinal/analise/areaAfetiva.html")),
    url(r'^analise/inserir/(?P<paciente_id>\d+)/(?P<analise_id>\d+)/relacionamentos$', InserirAnaliseRelacionamento.as_view()),
    url(r'^analise/inserir/(?P<paciente_id>\d+)/(?P<analise_id>\d+)/indiferenciacao$', InserirAnaliseIndiferenciacao.as_view()),
    url(r'^analise/inserir/(?P<paciente_id>\d+)/(?P<analise_id>\d+)/recomendacao/indiferenciacao$', RecomendacaoIndiferenciacao.as_view(template_name="projetofinal/analise/indiferenciacao.html")),
    url(r'^analise/inserir/(?P<paciente_id>\d+)/(?P<analise_id>\d+)/seletiva$', InserirAnaliseSeletiva.as_view()),
    url(r'^analise/inserir/(?P<paciente_id>\d+)/(?P<analise_id>\d+)/interventiva$', InserirAnaliseInterventiva.as_view()),
    url(r'^analise/inserir/(?P<paciente_id>\d+)/(?P<analise_id>\d+)/recomendacao/interventiva$', RecomendacaoInterventiva.as_view(template_name="projetofinal/analise/interventiva.html")),
    url(r'^analise/finalizada/(?P<paciente_id>\d+)$', AnaliseFinalizada.as_view()),
    url(r'^analise/consultar/(?P<paciente_id>\d+)/$', ConsultarAnalise.as_view(), name="consultar"),
    url(r'^analise/consultar/(?P<paciente_id>\d+)/(?P<analise_id>\d+)$', ConsultandoAnalise.as_view(), name="consultando"),
    url(r'^analise/prosseguir/(?P<paciente_id>\d+)/$', ProsseguirAnalise.as_view(), name="prosseguir"),
    url(r'^analise/prosseguir/(?P<paciente_id>\d+)/(?P<analise_id>\d+)$', analise.ProsseguindoAnalise, name="prosseguindo"),
    url(r'^analise/prosseguir/(?P<paciente_id>\d+)/remover$', analise.RemoverAnalise, name="remover"),
    url(r'^analise/consultar/(?P<paciente_id>\d+)/remover$', analise.RemoverAnalise, name="remover"),
    url(r'^analise/recomendacao/(?P<paciente_id>\d+)/$', Recomendacoes.as_view()),
    url(r'^analise/recomendacao/(?P<paciente_id>\d+)/(?P<analise_id>\d+)/$', ConsultandoRecomendacoes.as_view()),
    url(r'^analise/recomendacao/(?P<paciente_id>\d+)/remover$', analise.RemoverAnalise, name="remover"),
    url(r'^analise/recomendacao/(?P<paciente_id>\d+)/(?P<analise_id>\d+)/areaafetiva$', RecomendacaoAreaAfetiva.as_view(template_name="projetofinal/analise/recomendacao/areaAfetiva.html")),
    url(r'^analise/recomendacao/(?P<paciente_id>\d+)/(?P<analise_id>\d+)/indiferenciacao$', RecomendacaoIndiferenciacao.as_view(template_name="projetofinal/analise/recomendacao/indiferenciacao.html")),
    url(r'^pdf/(?P<paciente_id>\d+)/(?P<analise_id>\d+)$', analise.pdf_view),
    url(r'^analise/recomendacao/(?P<paciente_id>\d+)/(?P<analise_id>\d+)/seletiva$', RecomendacaoSeletiva.as_view(template_name="projetofinal/analise/seletiva.html")),
    url(r'^analise/recomendacao/(?P<paciente_id>\d+)/(?P<analise_id>\d+)/tarefas$', RecomendacaoTarefas.as_view(template_name="projetofinal/analise/tarefas.html")),
    url(r'^analise/recomendacao/(?P<paciente_id>\d+)/(?P<analise_id>\d+)/interventiva$', RecomendacaoInterventiva.as_view(template_name="projetofinal/analise/recomendacao/interventiva.html")),


    #Psicólogo
    url(r'^psicologo/administracao$', psicologo.PsicologoAdministracao),
    url(r'^psicologo/login$', psicologo.LoginPsicologo),
    url(r'^psicologo/home$', psicologo.PsicologoHome),
    url(r'^psicologo/cadastro$', CadastroPsicologoWizard.as_view([CadastroPsicologoForm]), name="cadastroPsicologo"),
    url(r'^psicologo/cadastrado$', psicologo.CadastroPsicologoRealizado),
    url(r'^psicologo/paciente/(?P<paciente_id>\d+)/$', PsicologoPaciente.as_view()),
    url(r'^psicologo/sair$', psicologo.LogoutPsicologo),
    url(r'^psicologo/paciente/(?P<paciente_id>\d+)/analise$', view=AnalisePaciente.as_view()),
    url(r'^psicologo/paciente/(?P<paciente_id>\d+)/(?P<analise_id>\d+)$', ConsultandoAnalisePaciente.as_view(), name="consultar"),
    url(r'^psicologo/paciente/(?P<paciente_id>\d+)/genograma$', view=GenogramaPaciente.as_view()),
]
