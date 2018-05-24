from django.urls import include, path
from django.contrib import admin

from . import paciente,psicologo,analise
from .forms import CadastroPaciente,CadastroConjuge,CadastroPai,CadastroMae,CadastroAvoPaterno,CadastroAvoPaterna,\
    CadastroAvoMaterno, CadastroAvoMaterna,EdicaoPaciente, CadastroPsicologoForm, CadastroPsicologoForm2
from .paciente import Home,CadastroWizard, EditarCadastro,EdicaoRealizada,AtualizarChave,ChaveAtualizada,\
    HabilitarPsicologoBusca,HabilitarPsicologo,PsicologoHabilitado, BuscarPsicologo, PsicologoLista, PsicologoPagina
from .psicologo import PsicologoPaciente, CadastroPsicologoWizard,EdicaoRealizadaPsicologo,EditarCadastroPsicologo,\
    AnalisePaciente, ConsultandoAnalisePaciente, GenogramaPaciente, Relatorio, RelatorioPaciente
from .analise import InserirAnalise,InserirAnaliseRelacionamento,InserirAnaliseIndiferenciacao,InserirAnaliseSeletiva,InserirAnaliseInterventiva,\
    AnaliseFinalizada,ConsultarAnalise, ConsultandoAnalise,\
    ProsseguirAnalise,Recomendacoes,ConsultandoRecomendacoes, RecomendacaoAreaAfetiva, RecomendacaoIndiferenciacao,\
    RecomendacaoSeletiva,RecomendacaoTarefas, RecomendacaoInterventiva,\
    ResumoAreaAfetiva, ResumoRelacionamento, ResumoSeletiva,ResumoTarefas, ResumoExercicios, ResumoInterventiva

handler404="paciente.erro404"

urlpatterns = [
    # Paciente
    path('', Home.as_view()),
    path('home/<paciente_id>/', Home.as_view()),
    path('sair/', paciente.LogoutView),
    path('erro404/', paciente.Erro404),
    path('cadastro/', CadastroWizard.as_view([CadastroPaciente,CadastroConjuge,CadastroPai,CadastroMae,CadastroAvoPaterno,CadastroAvoPaterna,CadastroAvoMaterno,CadastroAvoMaterna]), name="cadastro"),
    path('cadastrado/', paciente.CadastroRealizado),
    path('editado/<paciente_id>/', EdicaoRealizada.as_view()),
    path('login/', paciente.LoginPaciente),
    path('cadastro/editar/<paciente_id>/', EditarCadastro.as_view([EdicaoPaciente,CadastroConjuge,CadastroPai,CadastroMae,CadastroAvoPaterno,CadastroAvoPaterna,CadastroAvoMaterno,CadastroAvoMaterna]), name="editar"),
    # path('atualizar_chave/<paciente_id>/', AtualizarChave.as_view()),
    # path('chave/atualizada/<paciente_id>/', ChaveAtualizada.as_view()),
    path('habilitar_psicologo/<paciente_id>/', HabilitarPsicologoBusca.as_view()),
    path('habilitar_psicologo/<paciente_id>/<psicologo_id>', HabilitarPsicologo.as_view(), name="habilitar"),
    path('habilitado/<paciente_id>/', PsicologoHabilitado.as_view()),
    path('buscar_psicologo/<paciente_id>/',BuscarPsicologo.as_view()),
    path('buscar_psicologo/<paciente_id>/<estado>/<municipio>/',PsicologoLista.as_view()),
    path('buscar_psicologo/<psicologo>/<psicologo_id>/',PsicologoPagina.as_view()),

    path('recover/<signature>/', paciente.recover_done, name='password_reset_sent'),
    path('recover/', paciente.recover, name='password_reset_recover'),
    path('reset/done/', paciente.reset_done, name='password_reset_done'),
    path('reset/<token>/', paciente.reset, name='password_reset_reset'),

    # Análise
    path('analise/resumo/<paciente_id>/areaafetiva/', ResumoAreaAfetiva.as_view()),
    path('analise/resumo/<paciente_id>/<analise_id>/relacionamentos/', ResumoRelacionamento.as_view()),
    path('analise/resumo/<paciente_id>/<analise_id>/seletiva/', ResumoSeletiva.as_view()),
    path('analise/resumo/<paciente_id>/<analise_id>/tarefas/', ResumoTarefas.as_view()),
    path('analise/resumo/<paciente_id>/<analise_id>/exercicios/', ResumoExercicios.as_view()),
    path('analise/resumo/(<paciente_id>/<analise_id>/interventiva/', ResumoInterventiva.as_view()),
    path('analise/inserir/<paciente_id>/', InserirAnalise.as_view()),
    path('analise/inserir/<paciente_id>/<analise_id>/recomendacao/areaafetiva/', RecomendacaoAreaAfetiva.as_view(template_name="projetofinal/analise/areaAfetiva.html")),
    path('analise/inserir/<paciente_id>/<analise_id>/relacionamentos/', InserirAnaliseRelacionamento.as_view()),
    path('analise/inserir/<paciente_id>/<analise_id>/indiferenciacao/', InserirAnaliseIndiferenciacao.as_view()),
    path('analise/inserir/<paciente_id>/<analise_id>/recomendacao/indiferenciacao/', RecomendacaoIndiferenciacao.as_view(template_name="projetofinal/analise/indiferenciacao.html")),
    path('analise/inserir/<paciente_id>/<analise_id>/seletiva/', InserirAnaliseSeletiva.as_view()),
    path('analise/inserir/<paciente_id>/<analise_id>/interventiva/', InserirAnaliseInterventiva.as_view()),
    path('analise/inserir/<paciente_id>/<analise_id>/recomendacao/interventiva/', RecomendacaoInterventiva.as_view(template_name="projetofinal/analise/interventiva.html")),
    path('analise/finalizada/<paciente_id>/', AnaliseFinalizada.as_view()),
    path('analise/consultar/<paciente_id>/', ConsultarAnalise.as_view(), name="consultar"),
    path('analise/consultar/<paciente_id>/<analise_id>/', ConsultandoAnalise.as_view(), name="consultando"),
    path('analise/prosseguir/<paciente_id>/', ProsseguirAnalise.as_view(), name="prosseguir"),
    path('analise/prosseguir/<paciente_id>/<analise_id>/', analise.ProsseguindoAnalise, name="prosseguindo"),
    path('analise/prosseguir/<paciente_id>/remover', analise.RemoverAnalise, name="remover"),
    path('analise/consultar/<paciente_id>/remover', analise.RemoverAnalise, name="remover"),
    path('analise/recomendacao/<paciente_id>/', Recomendacoes.as_view()),
    path('analise/recomendacao/<paciente_id>/<analise_id>/', ConsultandoRecomendacoes.as_view()),
    path('analise/recomendacao/<paciente_id>/remover', analise.RemoverAnalise, name="remover"),
    path('analise/recomendacao/<paciente_id>/<analise_id>/areaafetiva/', RecomendacaoAreaAfetiva.as_view(template_name="projetofinal/analise/recomendacao/areaAfetiva.html")),
    path('analise/recomendacao/<paciente_id>/<analise_id>/indiferenciacao/', RecomendacaoIndiferenciacao.as_view(template_name="projetofinal/analise/recomendacao/indiferenciacao.html")),
    path('pdf/<paciente_id>/<analise_id>/', analise.pdf_view),
    path('analise/recomendacao/<paciente_id>/<analise_id>/seletiva/', RecomendacaoSeletiva.as_view(template_name="projetofinal/analise/seletiva.html")),
    path('analise/recomendacao/<paciente_id>/<analise_id>/tarefas/', RecomendacaoTarefas.as_view(template_name="projetofinal/analise/tarefas.html")),
    path('analise/recomendacao/<paciente_id>/<analise_id>/interventiva/', RecomendacaoInterventiva.as_view(template_name="projetofinal/analise/recomendacao/interventiva.html")),


    #Psicólogo
    path('psicologo/administracao/', psicologo.PsicologoAdministracao),
    path('psicologo/login/', psicologo.LoginPsicologo),
    path('psicologo/home/', psicologo.PsicologoHome),
    path('psicologo/cadastro/', CadastroPsicologoWizard.as_view([CadastroPsicologoForm,CadastroPsicologoForm2]), name="cadastroPsicologo"),
    path('psicologo/cadastrado/', psicologo.CadastroPsicologoRealizado),
    path('psicologo/cadastro/editar/<psicologo_id>/', EditarCadastroPsicologo.as_view(), name="editar"),
    path('psicologo/editado/<psicologo_id>/', EdicaoRealizadaPsicologo.as_view()),
    path('psicologo/paciente/<paciente_id>/', PsicologoPaciente.as_view()),
    path('psicologo/sair/', psicologo.LogoutPsicologo),
    path('psicologo/paciente/<paciente_id>/analise/', view=AnalisePaciente.as_view()),
    path('psicologo/paciente/<paciente_id>/<analise_id>', ConsultandoAnalisePaciente.as_view(), name="consultar"),
    path('psicologo/paciente/<paciente_id>/genograma/', view=GenogramaPaciente.as_view()),
    path('psicologo/paciente/<paciente_id>/relatorio/', view=RelatorioPaciente.as_view()),
    path('psicologo/pdf/<paciente_id>/<analise_id>/',psicologo.Relatorio),
    path('psicologo/recover/<signature>/', psicologo.recover_done, name='psicologo/password_reset_sent'),
    path('psicologo/recover/', psicologo.recover, name='psicologo/password_reset_recover'),
    path('psicologo/reset/done/', psicologo.reset_done, name='psicologo/password_reset_done'),
    path('psicologo/reset/<token>/', psicologo.reset, name='psicologo/password_reset_reset'),
]
