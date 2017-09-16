import datetime
import math
from datetime import datetime, timedelta
import json
from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.models import User, Group
from .forms import ConsultarAreaAfetiva, PerguntasAreaAfetiva,\
    RelacionamentoAvosMaternos, RelacionamentoAvoMaternoAntes, RelacionamentoAvoMaternaAntes, RelacionamentoAvosMaternosDepois,\
    RelacionamentoAvosPaternos, RelacionamentoAvoPaternoAntes, RelacionamentoAvoPaternaAntes, RelacionamentoAvosPaternosDepois,\
    RelacionamentoPais, RelacionamentoPaiAntes,RelacionamentoMaeAntes,RelacionamentoPaisDepois, RelacionamentoPaciente,\
    RelacionamentoPacienteAntes, RelacionamentoConjugeAntes, RelacionamentoPacienteDepois,GrauDeIndeferenciacao,\
    PerguntasSeletivas, ConsultarPerguntasSeletivas,\
    PerguntasInterventivas, ConsultarPerguntasInterventivas

from .models import Paciente, Chave, User,Familia, Psicologo, AreaAfetiva, Anamnesia, PerguntaAreaAfetiva,RespostaAreaAfetiva,\
    Relacionamento,GrauIndiferenciacao, GrauIndiferenciacaoPaciente,\
    Seletiva, PerguntaSeletiva,RespostaSeletiva, PerguntaSeletiva,\
    Interventiva, PerguntaInterventiva, Recomendacao
from formtools.wizard.views import SessionWizardView
from django.http import Http404, HttpResponseRedirect, HttpResponse, FileResponse
from django.template import RequestContext
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator
from django.conf import settings
from django.core import signing
from django.core.mail import send_mail
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render_to_response
from django.template import loader
from django.utils import timezone
from django.views import generic
from django.views.decorators.debug import sensitive_post_parameters
import simplejson
from collections import OrderedDict
try:
    from django.contrib.sites.shortcuts import get_current_site
except ImportError:
    from django.contrib.sites.models import get_current_site

from .forms import PasswordRecoveryForm, PasswordResetForm
from .signals import user_recovers_password
from .utils import get_user_model, get_username
from django.contrib.auth import logout
from .genograma import main

# Create your views here.
#Views da Análise


class ResumoAreaAfetiva(TemplateView):
    template_name = "projetofinal/analise/resumo/areaAfetiva.html"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ResumoAreaAfetiva, self).dispatch(*args, **kwargs)


    def paciente(self):
        if 'paciente_id' in self.kwargs:
            paciente_id = self.kwargs['paciente_id']
        paciente = Paciente.objects.get(usuario_id=paciente_id)
        return paciente

class ResumoRelacionamento(TemplateView):
    template_name = "projetofinal/analise/resumo/relacionamento.html"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ResumoRelacionamento, self).dispatch(*args, **kwargs)

    def anamnesia(self):
        if 'paciente_id' in self.kwargs:
            paciente_id = self.kwargs['paciente_id']
        paciente = Paciente.objects.get(usuario_id=paciente_id)

        if 'analise_id' in self.kwargs:
            analise_id = self.kwargs['analise_id']
        anamnesia = Anamnesia.objects.get(id=analise_id)
        return anamnesia

    def paciente(self):
        if 'paciente_id' in self.kwargs:
            paciente_id = self.kwargs['paciente_id']
        paciente = Paciente.objects.get(usuario_id=paciente_id)
        return paciente


class ResumoSeletiva(TemplateView):
    template_name = "projetofinal/analise/resumo/seletiva.html"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ResumoSeletiva, self).dispatch(*args, **kwargs)

    def anamnesia(self):
        if 'paciente_id' in self.kwargs:
            paciente_id = self.kwargs['paciente_id']
        paciente = Paciente.objects.get(usuario_id=paciente_id)

        if 'analise_id' in self.kwargs:
            analise_id = self.kwargs['analise_id']
        anamnesia = Anamnesia.objects.get(id=analise_id)
        return anamnesia

    def paciente(self):
        if 'paciente_id' in self.kwargs:
            paciente_id = self.kwargs['paciente_id']
        paciente = Paciente.objects.get(usuario_id=paciente_id)
        return paciente

class ResumoExercicios(TemplateView):
    template_name = "projetofinal/analise/resumo/exercicios.html"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ResumoExercicios, self).dispatch(*args, **kwargs)

    def anamnesia(self):
        if 'paciente_id' in self.kwargs:
            paciente_id = self.kwargs['paciente_id']
        paciente = Paciente.objects.get(usuario_id=paciente_id)

        if 'analise_id' in self.kwargs:
            analise_id = self.kwargs['analise_id']
        anamnesia = Anamnesia.objects.get(id=analise_id)
        return anamnesia

    def paciente(self):
        if 'paciente_id' in self.kwargs:
            paciente_id = self.kwargs['paciente_id']
        paciente = Paciente.objects.get(usuario_id=paciente_id)
        return paciente

class ResumoInterventiva(TemplateView):
    template_name = "projetofinal/analise/resumo/interventiva.html"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ResumoInterventiva, self).dispatch(*args, **kwargs)

    def anamnesia(self):
        if 'paciente_id' in self.kwargs:
            paciente_id = self.kwargs['paciente_id']
        paciente = Paciente.objects.get(usuario_id=paciente_id)

        if 'analise_id' in self.kwargs:
            analise_id = self.kwargs['analise_id']
        anamnesia = Anamnesia.objects.get(id=analise_id)
        return anamnesia

    def paciente(self):
        if 'paciente_id' in self.kwargs:
            paciente_id = self.kwargs['paciente_id']
        paciente = Paciente.objects.get(usuario_id=paciente_id)
        return paciente

class ResumoTarefas(TemplateView):
    template_name = "projetofinal/analise/resumo/tarefas.html"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ResumoTarefas, self).dispatch(*args, **kwargs)

    def anamnesia(self):
        if 'paciente_id' in self.kwargs:
            paciente_id = self.kwargs['paciente_id']
        paciente = Paciente.objects.get(usuario_id=paciente_id)

        if 'analise_id' in self.kwargs:
            analise_id = self.kwargs['analise_id']
        anamnesia = Anamnesia.objects.get(id=analise_id)
        return anamnesia

    def paciente(self):
        if 'paciente_id' in self.kwargs:
            paciente_id = self.kwargs['paciente_id']
        paciente = Paciente.objects.get(usuario_id=paciente_id)
        return paciente

class InserirAnalise(SessionWizardView):
    template_name = "projetofinal/analise/inserir.html"
    form_list = [PerguntasAreaAfetiva]

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(InserirAnalise, self).dispatch(*args, **kwargs)


    def passos(self):
        return 1

    def get_form_step_data(self, form):
        paciente_id = self.kwargs['paciente_id']
        paciente = Paciente.objects.get(usuario_id=paciente_id)

        if form.data['inserir_analise-current_step'] == '0':
            anamnesia = Anamnesia()
            anamnesia.paciente = paciente
            A={'0':0}
            for item in form.data:
                if item[0] == "0":
                    pergunta = PerguntaAreaAfetiva.objects.get(numero=item.split("-")[1])
                    resposta = RespostaAreaAfetiva.objects.get(pergunta_id=pergunta.id,letra=form.data[item])
                    A[item.split("A")[1]]=resposta.valor

            afetivoRelacional=(A['01']+A['02']+A['04']+A['06']+A['09']+A['13']+A['15']+A['17']+A['19']+A['20']+A['21']+A['22']+A['23']+A['25']+A['28'])/15
            produtividade=(A['05']+A['16']+A['20']+A['22']+A['23'])/5
            organico=(A['07']+A['12']+A['14']+A['27']+A['29'])/5
            espiritual=(A['03']+A['11']+A['18']+A['24']+A['26'])/5
            socioCultural=(A['08']+A['10']+A['20']+A['22']+A['23'])/5

            lista = [(organico,"a"),(produtividade, "b"),(afetivoRelacional,"c"),(socioCultural,"d"),(espiritual,"e")]
            minimo = min(lista, key=lambda x: x[0])
            if minimo[0] == afetivoRelacional:
                anamnesia.areaAfetiva = "AfetivoRelacional"
            if minimo[0] == produtividade:
                anamnesia.areaAfetiva = "Produtividade"
            if minimo[0] == organico:
                anamnesia.areaAfetiva = "Organico"
            if minimo[0] ==  espiritual:
                anamnesia.areaAfetiva = "Espiritual"
            if minimo[0] == socioCultural:
                anamnesia.areaAfetiva = "SocioCultural"

            # if paciente.retornos == 0:
            inicio=anamnesia.inicio=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            anamnesia.retornos=1
            anamnesia.save()
            anamnesia = Anamnesia.objects.get(inicio=inicio)
            self.initial_dict['anamnesia_id']=anamnesia.id

            for item in form.data:
                if item[0] == "0":
                    pergunta = PerguntaAreaAfetiva.objects.get(numero=item.split("-")[1])
                    resposta = RespostaAreaAfetiva.objects.get(pergunta_id=pergunta.id,letra=form.data[item])
                    areaAfetiva = AreaAfetiva()
                    areaAfetiva.paciente = paciente
                    areaAfetiva.resposta = resposta
                    areaAfetiva.anamnesia = anamnesia
                    areaAfetiva.save()
            paciente = Paciente.objects.get(usuario_id=paciente_id)
            paciente.retornos = 1
            paciente.save()
        if Anamnesia.objects.filter(paciente_id=paciente.id).exists():
            anamnesia = Anamnesia.objects.filter(paciente_id=paciente.id).last()
            agora=datetime.now()
            inicio =anamnesia.inicio
            tempo=agora-inicio
            paciente.tempo= 30 - tempo.days
            paciente.save()

        return form.data

    def paciente(self):
        if 'paciente_id' in self.kwargs:
            paciente_id = self.kwargs['paciente_id']
        paciente = Paciente.objects.get(usuario_id=paciente_id)
        return paciente

    def done(self, form_list, form_dict, **kwargs):
        paciente_id = self.kwargs['paciente_id']
        return HttpResponseRedirect('/analise/inserir/'+paciente_id+'/'+str(self.initial_dict['anamnesia_id'])+'/recomendacao/areaafetiva')

class InserirAnaliseRelacionamento(SessionWizardView):
    template_name = "projetofinal/analise/inserir.html"
    form_list = [RelacionamentoAvosMaternos,
                 RelacionamentoAvoMaternoAntes,RelacionamentoAvoMaternaAntes,
                 RelacionamentoAvosMaternosDepois,RelacionamentoAvosPaternos,
                 RelacionamentoAvoPaternoAntes,RelacionamentoAvoPaternaAntes,
                 RelacionamentoAvosPaternosDepois,RelacionamentoPais,
                 RelacionamentoPaiAntes,RelacionamentoMaeAntes,
                 RelacionamentoPaisDepois,RelacionamentoPaciente,
                 RelacionamentoPacienteAntes,RelacionamentoConjugeAntes,
                 RelacionamentoPacienteDepois]

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):

        self.initial_dict['passo'] = 2

        self.form_list.clear()
        self.form_list.update({'0':RelacionamentoAvosMaternos})
        self.form_list.update({'1':RelacionamentoAvoMaternoAntes})
        self.form_list.update({'2':RelacionamentoAvoMaternaAntes})
        self.form_list.update({'3':RelacionamentoAvosMaternosDepois})
        self.form_list.update({'4':RelacionamentoAvosPaternos})
        self.form_list.update({'5':RelacionamentoAvoPaternoAntes})
        self.form_list.update({'6':RelacionamentoAvoPaternaAntes})
        self.form_list.update({'7':RelacionamentoAvosPaternosDepois})
        self.form_list.update({'8':RelacionamentoPais})
        self.form_list.update({'9':RelacionamentoPaiAntes})
        self.form_list.update({'10':RelacionamentoMaeAntes})
        self.form_list.update({'11':RelacionamentoPaisDepois})
        self.form_list.update({'12':RelacionamentoPaciente})
        self.form_list.update({'13':RelacionamentoPacienteAntes})
        self.form_list.update({'14':RelacionamentoConjugeAntes})
        self.form_list.update({'15':RelacionamentoPacienteDepois})

        if 'paciente_id' in self.kwargs:
            paciente_id = self.kwargs['paciente_id']
            try:
                paciente = Paciente.objects.get(usuario_id=paciente_id)
            except Paciente.DoesNotExist:
                raise Http404("Paciente não existe")
            if 'analise_id' in self.kwargs:
                analise_id = self.kwargs['analise_id']
            try:
                analise = Anamnesia.objects.get(id=analise_id)
            except Anamnesia.DoesNotExist:
                raise Http404("Atendimento não existe")


        relacionamentos = Relacionamento.objects.filter(anamnesia_id = analise_id)
        for relacionamento in relacionamentos:
            if relacionamento.parente == "AvoMaterno":
                for key, value in self.form_list.items():
                    if value == RelacionamentoAvosMaternos:
                        self.form_list.pop(key)
                        self.initial_dict['passo'] = 3

                if (relacionamento.filhosAntes is None and relacionamento.relacaoAntes == "Não")\
                        or (relacionamento.relacaoAntes == "Sim" and relacionamento.filhosAntes is not None):
                    for key, value in self.form_list.items():
                        if value == RelacionamentoAvoMaternoAntes:
                            self.form_list.pop(key)
                            self.initial_dict['passo'] = 4

            if relacionamento.parente == "AvoMaterna":
                if(relacionamento.filhosAntes is None and relacionamento.relacaoAntes == "Não")\
                        or (relacionamento.relacaoAntes == "Sim" and relacionamento.filhosAntes is not None):
                    for key, value in self.form_list.items():
                        if value == RelacionamentoAvoMaternaAntes:
                            self.form_list.pop(key)
                            self.initial_dict['passo'] = 5
                if(relacionamento.filhosDepois is None and (relacionamento.relacao == "Casados" or relacionamento.relacao == "Moram junto"))\
                        or ((relacionamento.relacao == "Separados" or relacionamento.relacao == "Divorciados") and relacionamento.filhosDepois is not None):
                    for key, value in self.form_list.items():
                        if value == RelacionamentoAvosMaternosDepois:
                            self.form_list.pop(key)
                            self.initial_dict['passo'] = 6

            if relacionamento.parente == "AvoPaterno":
                for key, value in self.form_list.items():
                    if value == RelacionamentoAvosPaternos:
                        self.form_list.pop(key)
                        self.initial_dict['passo'] = 7
                if (relacionamento.filhosAntes is None and relacionamento.relacaoAntes == "Não")\
                        or (relacionamento.relacaoAntes == "Sim" and relacionamento.filhosAntes is not None):
                    for key, value in self.form_list.items():
                        if value == RelacionamentoAvoPaternoAntes:
                            self.form_list.pop(key)
                            self.initial_dict['passo'] = 8
            if relacionamento.parente == "AvoPaterna":
                if(relacionamento.filhosAntes is None and relacionamento.relacaoAntes == "Não")\
                        or (relacionamento.relacaoAntes == "Sim" and relacionamento.filhosAntes is not None):
                    for key, value in self.form_list.items():
                        if value == RelacionamentoAvoPaternaAntes:
                            self.form_list.pop(key)
                            self.initial_dict['passo'] = 9
                if(relacionamento.filhosDepois is None and (relacionamento.relacao == "Casados" or relacionamento.relacao == "Moram junto"))\
                        or ((relacionamento.relacao == "Separados" or relacionamento.relacao == "Divorciados") and relacionamento.filhosDepois is not None):
                    for key, value in self.form_list.items():
                        if value == RelacionamentoAvosPaternosDepois:
                            self.form_list.pop(key)
                            self.initial_dict['passo'] = 10

            if relacionamento.parente == "Pai":
                for key, value in self.form_list.items():
                    if value == RelacionamentoPais:
                        self.form_list.pop(key)
                        self.initial_dict['passo'] = 11
                if (relacionamento.filhosAntes is None and relacionamento.relacaoAntes == "Não")\
                        or (relacionamento.relacaoAntes == "Sim" and relacionamento.filhosAntes is not None):
                    for key, value in self.form_list.items():
                        if value == RelacionamentoPaiAntes:
                            self.form_list.pop(key)
                            self.initial_dict['passo'] = 12
            if relacionamento.parente == "Mae":
                if(relacionamento.filhosAntes is None and relacionamento.relacaoAntes == "Não")\
                        or (relacionamento.relacaoAntes == "Sim" and relacionamento.filhosAntes is not None):
                    for key, value in self.form_list.items():
                        if value == RelacionamentoMaeAntes:
                            self.form_list.pop(key)
                            self.initial_dict['passo'] = 13
                if(relacionamento.filhosDepois is None and (relacionamento.relacao == "Casados" or relacionamento.relacao == "Moram junto"))\
                        or ((relacionamento.relacao == "Separados" or relacionamento.relacao == "Divorciados") and relacionamento.filhosDepois is not None):
                    for key, value in self.form_list.items():
                        if value == RelacionamentoPaisDepois:
                            self.form_list.pop(key)
                            self.initial_dict['passo'] = 14

            if relacionamento.parente == "Paciente":
                for key, value in self.form_list.items():
                    if value == RelacionamentoPaciente:
                        self.form_list.pop(key)
                        self.initial_dict['passo'] = 15
                if (relacionamento.filhosAntes is None and relacionamento.relacaoAntes == "Não")\
                        or (relacionamento.relacaoAntes == "Sim" and relacionamento.filhosAntes is not None):
                    for key, value in self.form_list.items():
                        if value == RelacionamentoPacienteAntes:
                            self.form_list.pop(key)
                            self.initial_dict['passo'] = 16
            if relacionamento.parente == "Conjuge":
                if(relacionamento.filhosAntes is None and (relacionamento.relacaoAntes == "Não" or relacionamento.relacaoAntes == "Não se aplica" ))\
                        or (relacionamento.relacaoAntes == "Sim" and relacionamento.filhosAntes is not None):
                    for key, value in self.form_list.items():
                        if value == RelacionamentoConjugeAntes:
                            self.form_list.pop(key)
                            self.initial_dict['passo'] = 17
                if(relacionamento.filhosDepois is None and (relacionamento.relacao == "Casado(a)" or relacionamento.relacao == "Mora junto" or relacionamento.relacao == "Solteiro(a)"))\
                        or ((relacionamento.relacao == "Separado(a)" or relacionamento.relacao == "Divorciado(a)") and relacionamento.filhosDepois is not None):
                    for key, value in self.form_list.items():
                        if value == RelacionamentoPacienteDepois:
                            self.form_list.pop(key)
                            self.initial_dict['passo'] = 18

        return super(InserirAnaliseRelacionamento, self).dispatch(*args, **kwargs)

    def get_form(self, step=None, data=None, files=None):
        form = super(InserirAnaliseRelacionamento, self).get_form(step, data, files)

        if 'paciente_id' in self.kwargs:
            paciente_id = self.kwargs['paciente_id']
            try:
                paciente = Paciente.objects.get(usuario_id=paciente_id)
            except Paciente.DoesNotExist:
                raise Http404("Paciente não existe")
        if step is None:
            step = self.steps.current
        if step == "0":
            self.initial_dict['passo']=2
        if step == "1":
            self.initial_dict['passo']=3
        if step == "2":
            self.initial_dict['passo']=4
        if step == "3":
            self.initial_dict['passo']=5
        if step == "4":
            self.initial_dict['passo']=6
        if step == "5":
            self.initial_dict['passo']=7
        if step == "6":
            self.initial_dict['passo']=8
        if step == "7":
            self.initial_dict['passo']=9
        if step == "8":
            form = RelacionamentoPais(paciente_sexo=paciente.sexo,step=step,data=data)
            self.initial_dict['passo']=10
        if step == "9":
            self.initial_dict['passo']=11
        if step == "10":
            self.initial_dict['passo']=12
        if step == "11":
            self.initial_dict['passo']=13
        if step == "12":
            self.initial_dict['passo']=14
        if step == "13":
            self.initial_dict['passo']=15
        if step == "14":
            self.initial_dict['passo']=16
        if step == "15":
            self.initial_dict['passo']=17
        return form

    def get_form_step_data(self, form):
        paciente_id = self.kwargs['paciente_id']
        paciente = Paciente.objects.get(usuario_id=paciente_id)
        analise_id =  self.kwargs['analise_id']

        if form.data['inserir_analise_relacionamento-current_step'] == '0':
            if form.data['0-relacaoAvoMaternoAntes'] == "Não":
                for key, value in self.form_list.items():
                    if value == RelacionamentoAvoMaternoAntes:
                        self.form_list.pop(key)
            if form.data['0-relacaoAvoMaternaAntes'] == "Não":
                for key, value in self.form_list.items():
                    if value == RelacionamentoAvoMaternaAntes:
                        self.form_list.pop(key)
            if (form.data['0-relacao'] == "Casados") or (form.data['0-relacao'] == "Moram junto"):
                for key, value in self.form_list.items():
                    if value == RelacionamentoAvosMaternosDepois:
                        self.form_list.pop(key)
        if form.data['inserir_analise_relacionamento-current_step'] == '4':
            if form.data['4-relacaoAvoPaternoAntes'] == "Não":
                for key, value in self.form_list.items():
                    if value == RelacionamentoAvoPaternoAntes:
                        self.form_list.pop(key)
            if form.data['4-relacaoAvoPaternaAntes'] == "Não":
                for key, value in self.form_list.items():
                    if value == RelacionamentoAvoPaternaAntes:
                        self.form_list.pop(key)
            if (form.data['4-relacao'] == "Casados") or (form.data['4-relacao'] == "Moram junto"):
                for key, value in self.form_list.items():
                    if value == RelacionamentoAvosPaternosDepois:
                        self.form_list.pop(key)
        if form.data['inserir_analise_relacionamento-current_step'] == '8':
            if form.data['8-relacaoPaiAntes'] == "Não":
                for key, value in self.form_list.items():
                    if value == RelacionamentoPaiAntes:
                        self.form_list.pop(key)
            if form.data['8-relacaoMaeAntes'] == "Não":
                for key, value in self.form_list.items():
                    if value == RelacionamentoMaeAntes:
                        self.form_list.pop(key)
            if (form.data['8-relacao'] == "Casados") or (form.data['8-relacao'] == "Moram junto"):
                for key, value in self.form_list.items():
                    if value == RelacionamentoPaisDepois:
                        self.form_list.pop(key)
        if form.data['inserir_analise_relacionamento-current_step'] == '12':
            for key, value in self.form_list.items():
                if value == RelacionamentoPais:
                    self.form_list.pop(key)
            if form.data['12-relacaoPacienteAntes'] == "Não":
                for key, value in self.form_list.items():
                    if value == RelacionamentoPacienteAntes:
                        self.form_list.pop(key)
            if form.data['12-relacaoConjugeAntes'] == "Não" or form.data['12-relacaoConjugeAntes'] == "Não se aplica":
                for key, value in self.form_list.items():
                    if value == RelacionamentoConjugeAntes:
                        self.form_list.pop(key)
            if (form.data['12-relacao'] == "Casado(a)") or (form.data['12-relacao'] == "Mora junto") or (form.data['12-relacao'] == "Solteiro(a)"):
                for key, value in self.form_list.items():
                    if value == RelacionamentoPacienteDepois:
                        self.form_list.pop(key)

        steps =[]
        for i in range(0,16):
            steps.append(str(i))
        avoM =[]
        for i in range(0,4):
            avoM.append(str(i))
        avoP =[]
        for i in range(4,8):
            avoP.append(str(i))
        pais =[]
        for i in range(8,12):
            pais.append(str(i))
        pac =[]
        for i in range(12,16):
            pac.append(str(i))

        if form.data['inserir_analise_relacionamento-current_step'] in avoM:
            contador = 0
        if form.data['inserir_analise_relacionamento-current_step'] in avoP:
            contador = 2
        if form.data['inserir_analise_relacionamento-current_step'] in pais:
            contador = 4
        if form.data['inserir_analise_relacionamento-current_step'] in pac:
            contador = 6
        parentes = ["AvoMaterno","AvoMaterna","AvoPaterno","AvoPaterna","Pai","Mae","Paciente","Conjuge"]

        if paciente.tempo != 0:
            if form.data['inserir_analise_relacionamento-current_step'] in steps:
                item = form.data['inserir_analise_relacionamento-current_step']
                if item+"-"+"relacao" in form.data:
                    relacionamento = Relacionamento()
                    relacionamento.paciente = paciente
                    relacionamento.anamnesia = Anamnesia.objects.get(id = analise_id,paciente_id=paciente.id)
                    relacionamento.parente=parentes[contador]
                    relacionamento.relacao = form.data[item+"-"+"relacao"]
                    relacionamento.filhos = form.data[item+"-"+"filhos"]
                    relacionamento.filhas = form.data[item+"-"+"filhas"]
                    relacionamento.relacaoAntes = form.data[item+"-"+"relacao"+parentes[contador]+"Antes"]
                    relacionamento.save()

                    relacionamento = Relacionamento()
                    relacionamento.paciente = paciente
                    relacionamento.anamnesia = Anamnesia.objects.get(id = analise_id,paciente_id=paciente.id)
                    relacionamento.parente=parentes[contador+1]
                    relacionamento.relacao = form.data[item+"-"+"relacao"]
                    relacionamento.filhos = form.data[item+"-"+"filhos"]
                    relacionamento.filhas = form.data[item+"-"+"filhas"]
                    relacionamento.relacaoAntes = form.data[item+"-"+"relacao"+parentes[contador+1]+"Antes"]
                    relacionamento.save()

                if item+"-"+"filhos"+parentes[contador]+"Antes" in form.data:
                    relacionamento = Relacionamento.objects.get(paciente_id = paciente.id, anamnesia_id = analise_id,parente = parentes[contador])
                    relacionamento.filhosAntes = form.data[item+"-"+"filhos"+parentes[contador]+"Antes"]
                    relacionamento.filhasAntes = form.data[item+"-"+"filhas"+parentes[contador]+"Antes"]
                    relacionamento.save()
                if item+"-"+"filhos"+parentes[contador+1]+"Antes" in form.data:
                    relacionamento = Relacionamento.objects.get(paciente_id = paciente.id, anamnesia_id = analise_id,parente = parentes[contador+1])
                    relacionamento.filhosAntes = form.data[item+"-"+"filhos"+parentes[contador+1]+"Antes"]
                    relacionamento.filhasAntes = form.data[item+"-"+"filhas"+parentes[contador+1]+"Antes"]
                    relacionamento.save()

                if item+"-"+"filhos"+parentes[contador] in form.data:
                    relacionamento = Relacionamento.objects.get(paciente_id = paciente.id, anamnesia_id = analise_id,parente = parentes[contador])
                    relacionamento.filhosDepois = form.data[item+"-"+"filhos"+parentes[contador]]
                    relacionamento.filhasDepois = form.data[item+"-"+"filhas"+parentes[contador]]
                    relacionamento.save()
                if item+"-"+"filhos"+parentes[contador+1] in form.data:
                    relacionamento = Relacionamento.objects.get(paciente_id = paciente.id, anamnesia_id = analise_id,parente = parentes[contador+1])
                    relacionamento.filhosDepois = form.data[item+"-"+"filhos"+parentes[contador+1]]
                    relacionamento.filhasDepois = form.data[item+"-"+"filhas"+parentes[contador+1]]
                    relacionamento.save()

        return form.data

    def passos(self):
        return self.initial_dict['passo']

    def paciente(self):
        if 'paciente_id' in self.kwargs:
            paciente_id = self.kwargs['paciente_id']
        paciente = Paciente.objects.get(usuario_id=paciente_id)
        return paciente

    def done(self, form_list, form_dict, **kwargs):
        paciente_id = self.kwargs['paciente_id']
        analise_id = self.kwargs['analise_id']
        return HttpResponseRedirect('/analise/inserir/'+paciente_id+'/'+analise_id+'/indiferenciacao')

class InserirAnaliseIndiferenciacao(SessionWizardView):
    template_name = "projetofinal/analise/inserir.html"
    form_list = [GrauDeIndeferenciacao]

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(InserirAnaliseIndiferenciacao, self).dispatch(*args, **kwargs)

    def passos(self):
        return 18

    def get_form_step_data(self, form):
        paciente_id = self.kwargs['paciente_id']
        paciente = Paciente.objects.get(usuario_id=paciente_id)
        analise_id =  self.kwargs['analise_id']

        if paciente.tempo != 0:
            if form.data['inserir_analise_indiferenciacao-current_step'] == '0':
                anamnesia = Anamnesia.objects.get(id=analise_id)
                respostasIndiferenciacao = []
                adaptativo = 0
                reativo = 0
                criativo = 0
                if "0-grauIndiferenciacao" in form.data:
                    respostasIndiferenciacao = form.data.getlist('0-grauIndiferenciacao')
                for item in respostasIndiferenciacao:
                    indiferenciacao = GrauIndiferenciacaoPaciente()
                    indiferenciacao.paciente=paciente
                    indiferenciacao.anamnesia=anamnesia
                    indiferenciacao.resposta = GrauIndiferenciacao.objects.get(id=int(item))
                    if indiferenciacao.resposta.padrao == "adaptativo":
                        adaptativo = adaptativo+1
                    if indiferenciacao.resposta.padrao == "reativo":
                        reativo = reativo+1
                    if indiferenciacao.resposta.padrao == "criativo":
                        criativo = criativo+1
                    indiferenciacao.save()

                lista = [(adaptativo,"a"),(reativo,"b"),(criativo, "c")]
                minimo = min(lista, key=lambda x: x[0])
                if minimo[0] == adaptativo:
                    anamnesia.padrao = "adaptativo"
                if minimo[0] == reativo:
                    anamnesia.padrao = "reativo"
                if minimo[0] ==  criativo:
                    anamnesia.padrao = "criativo"
                anamnesia.save()
                indiferenciacao.save()

        return form.data

    def paciente(self):
        if 'paciente_id' in self.kwargs:
            paciente_id = self.kwargs['paciente_id']
        paciente = Paciente.objects.get(usuario_id=paciente_id)
        return paciente

    def done(self, form_list, form_dict, **kwargs):
        paciente_id = self.kwargs['paciente_id']
        analise_id = self.kwargs['analise_id']
        return HttpResponseRedirect('/analise/inserir/'+paciente_id+'/'+analise_id+'/recomendacao/indiferenciacao')

class InserirAnaliseSeletiva(SessionWizardView):
    template_name = "projetofinal/analise/inserir.html"
    form_list = [PerguntasSeletivas]

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(InserirAnaliseSeletiva, self).dispatch(*args, **kwargs)

    def passos(self):
        return 19

    def get_form(self, step=None, data=None, files=None):
        form = super(InserirAnaliseSeletiva, self).get_form(step, data, files)
        if 'paciente_id' in self.kwargs:
            paciente_id = self.kwargs['paciente_id']
        if 'analise_id' in self.kwargs:
            analise_id = self.kwargs['analise_id']

        relacionamento = Relacionamento.objects.get(anamnesia_id= analise_id,parente= "Paciente")
        relacao = relacionamento.relacao
        form = PerguntasSeletivas(relacao=relacao, data=data)
        return form

    def get_form_step_data(self, form):
        paciente_id = self.kwargs['paciente_id']
        paciente = Paciente.objects.get(usuario_id=paciente_id)
        analise_id =  self.kwargs['analise_id']

        if paciente.tempo != 0:
            if form.data['inserir_analise_seletiva-current_step'] == '0':
                anamnesia = Anamnesia.objects.get(id=analise_id)
                seletivas = {}
                if "S01" in form.data:
                    for item in form.data:
                        if item[0] == "S":
                            seletivas.update({item:form.data[item]})
                    for perguntas in seletivas:
                        if perguntas != "S03" and perguntas != "S04":
                            seletiva = Seletiva()
                            seletiva.paciente = paciente
                            seletiva.anamnesia = anamnesia
                            pergunta = PerguntaSeletiva.objects.get(numero=perguntas)
                            seletiva.resposta = RespostaSeletiva.objects.get(pergunta_id=pergunta.id,letra=seletivas[perguntas])
                            seletiva.save()
                        else:
                            seletivas[perguntas] = form.data.getlist(perguntas)
                            for resposta in seletivas[perguntas]:
                                seletiva = Seletiva()
                                seletiva.paciente = paciente
                                seletiva.anamnesia = anamnesia
                                pergunta = PerguntaSeletiva.objects.get(numero=perguntas)
                                seletiva.resposta = RespostaSeletiva.objects.get(pergunta_id=pergunta.id,letra=resposta)
                                seletiva.save()

        return form.data

    def paciente(self):
        if 'paciente_id' in self.kwargs:
            paciente_id= self.kwargs['paciente_id']
        paciente = Paciente.objects.get(usuario_id=paciente_id)
        return paciente

    def done(self, form_list, form_dict, **kwargs):
        paciente_id = self.kwargs['paciente_id']
        analise_id = self.kwargs['analise_id']
        return HttpResponseRedirect('/analise/recomendacao/'+paciente_id+'/'+analise_id+'/seletiva')

class InserirAnaliseInterventiva(SessionWizardView):
    template_name = "projetofinal/analise/inserir.html"
    form_list = [PerguntasInterventivas]

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(InserirAnaliseInterventiva, self).dispatch(*args, **kwargs)

    def passos(self):
        return 20

    def get_form_step_data(self, form):
        paciente_id = self.kwargs['paciente_id']
        paciente = Paciente.objects.get(usuario_id=paciente_id)
        analise_id =  self.kwargs['analise_id']

        if paciente.tempo != 0:
            if form.data['inserir_analise_interventiva-current_step'] == '0':
                anamnesia = Anamnesia.objects.get(id=analise_id)
                interventivas = {}
                if "0-I01" in form.data:
                    for item in form.data:
                        if item[0] == "0":
                            interventivas.update({item.split("-")[1]:form.data[item]})
                    for perguntas in interventivas:
                        interventiva = Interventiva()
                        interventiva.paciente = paciente
                        interventiva.anamnesia = anamnesia
                        pergunta = PerguntaInterventiva.objects.get(numero=perguntas)
                        interventiva.resposta = interventivas[perguntas]
                        interventiva.pergunta = pergunta
                        interventiva.save()
                        anamnesia.fim = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        anamnesia.save()

        return form.data

    def paciente(self):
        if 'paciente_id' in self.kwargs:
            paciente_id = self.kwargs['paciente_id']
        paciente = Paciente.objects.get(usuario_id=paciente_id)
        return paciente

    def done(self, form_list, form_dict, **kwargs):
        paciente_id = self.kwargs['paciente_id']
        analise_id = self.kwargs['analise_id']
        return HttpResponseRedirect('/analise/finalizada/'+ paciente_id )

class AnaliseFinalizada(TemplateView):
    template_name = "projetofinal/analise/inserida.html"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(AnaliseFinalizada, self).dispatch(*args, **kwargs)

    def paciente(self):
        if 'paciente_id' in self.kwargs:
            paciente_id = self.kwargs['paciente_id']
        paciente = Paciente.objects.get(usuario_id=paciente_id)
        return paciente


class ConsultarAnalise(TemplateView):
    template_name="projetofinal/analise/consultar.html"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ConsultarAnalise, self).dispatch(*args, **kwargs)

    def anamnesia(self):
        if 'paciente_id' in self.kwargs:
            paciente_id = self.kwargs['paciente_id']
        paciente = Paciente.objects.get(usuario_id=paciente_id)
        anamnesia = Anamnesia.objects.filter(paciente_id=paciente.id)

        return anamnesia

    def indiferenciacao(self):
        indiferenciacao=0
        if 'paciente_id' in self.kwargs:
            paciente_id = self.kwargs['paciente_id']
        paciente = Paciente.objects.get(usuario_id=paciente_id)
        anamnesia = Anamnesia.objects.filter(paciente_id=paciente.id)
        for analise in anamnesia:
            if GrauIndiferenciacaoPaciente.objects.filter(anamnesia_id=analise.id).exists():
                indiferenciacao=1
        return indiferenciacao

    def paciente(self):
        if 'paciente_id' in self.kwargs:
            paciente_id = self.kwargs['paciente_id']
        paciente = Paciente.objects.get(usuario_id=paciente_id)
        return paciente

    def grafico(self):
        if 'paciente_id' in self.kwargs:
            paciente_id = self.kwargs['paciente_id']
        paciente = Paciente.objects.get(usuario_id=paciente_id)
        dados = {
        }
        anamnesia = Anamnesia.objects.filter(paciente_id=paciente.id)
        for analise in anamnesia:
            area= AreaAfetiva.objects.filter(anamnesia_id=analise.id).order_by('resposta_id')
            A=[0]
            for respostas in area:
                resposta = RespostaAreaAfetiva.objects.get(id=respostas.resposta_id)
                A.append(resposta.valor)
            afetivoRelacional=((A[1]+A[2]+A[4]+A[6]+A[9]+A[13]+A[15]+A[17]+A[19]+A[20]+A[21]+A[22]+A[23]+A[25]+A[28])/15)
            produtividade=((A[5]+A[16]+A[20]+A[22]+A[23])/5)
            organico=((A[7]+A[12]+A[14]+A[27]+A[29])/5)
            espiritual=((A[3]+A[11]+A[18]+A[24]+A[26])/5)
            socioCultural=((A[8]+A[10]+A[20]+A[22]+A[23])/5)

            dados[str(analise.inicio.strftime("%d/%m/%y %H:%M:%S"))] = [afetivoRelacional]
            dados[str(analise.inicio.strftime("%d/%m/%y %H:%M:%S"))].append(produtividade)
            dados[str(analise.inicio.strftime("%d/%m/%y %H:%M:%S"))].append(organico)
            dados[str(analise.inicio.strftime("%d/%m/%y %H:%M:%S"))].append(espiritual)
            dados[str(analise.inicio.strftime("%d/%m/%y %H:%M:%S"))].append(socioCultural)

        grafico = simplejson.dumps(dados)
        return grafico

    def graficoRadar(self):
        if 'paciente_id' in self.kwargs:
            paciente_id = self.kwargs['paciente_id']
        paciente = Paciente.objects.get(usuario_id=paciente_id)
        dados = {
        }
        anamnesia = Anamnesia.objects.filter(paciente_id=paciente.id)
        criativo=0
        reativo=0
        adaptativo=0
        for analise in anamnesia:
            if GrauIndiferenciacaoPaciente.objects.filter(anamnesia_id=analise.id).exists():
                indiferenciacao = GrauIndiferenciacaoPaciente.objects.filter(anamnesia_id=analise.id)
                for opcao in indiferenciacao:
                    resposta = GrauIndiferenciacao.objects.get(id=opcao.resposta_id)
                    if resposta.padrao == "adaptativo":
                        adaptativo=adaptativo+1
                    if resposta.padrao == "reativo":
                        reativo=reativo+1
                    if resposta.padrao == "criativo":
                        criativo=criativo+1

                dados[str(analise.inicio.strftime("%d/%m/%y %H:%M:%S"))] = [adaptativo]
                dados[str(analise.inicio.strftime("%d/%m/%y %H:%M:%S"))].append(reativo)
                dados[str(analise.inicio.strftime("%d/%m/%y %H:%M:%S"))].append(criativo)

        nascimento=str(paciente.nascimento)
        ano = int(nascimento.split("-")[0])
        mes=int(nascimento.split("-")[1])
        dia=int(nascimento.split("-")[2])
        atual=datetime.now()
        anoAtual=atual.year
        mesAtual=atual.month
        diaAtual=atual.day

        if mes > mesAtual:
            idade = anoAtual-ano-1
        if mes < mesAtual:
            idade = anoAtual-ano
        if mes == mesAtual:
            if dia >= diaAtual:
                idade = anoAtual-ano-1
            if dia < diaAtual:
                idade = anoAtual-ano

        adaptativoMin=0
        adaptativoMax=0
        criativoMin=0
        criativoMax=0
        reativoMin=0
        reativoMax=0

        if idade >=0 and idade <=3:
            adaptativoMin=14
            adaptativoMax=17
            criativoMin=0
            criativoMax=2
            reativoMin=0
            reativoMax=2
        if idade >=4 and idade <=7:
            adaptativoMin=12
            adaptativoMax=17
            criativoMin=0
            criativoMax=3
            reativoMin=2
            reativoMax=6
        if idade >=8 and idade <=12:
            adaptativoMin=8
            adaptativoMax=13
            criativoMin=2
            criativoMax=5
            reativoMin=6
            reativoMax=10
        if idade >=13 and idade <=19:
            adaptativoMin=4
            adaptativoMax=8
            criativoMin=6
            criativoMax=8
            reativoMin=10
            reativoMax=15
        if idade >=20 and idade <=24:
            adaptativoMin=1
            adaptativoMax=3
            criativoMin=9
            criativoMax=11
            reativoMin=8
            reativoMax=12
        if idade >=25 and idade <=32:
            adaptativoMin=0
            adaptativoMax=2
            criativoMin=11
            criativoMax=15
            reativoMin=3
            reativoMax=7
        if idade >=33:
            adaptativoMin=0
            adaptativoMax=2
            criativoMin=16
            criativoMax=19
            reativoMin=0
            reativoMax=2

        dados['Limite Inferior Adaptativo'] = adaptativoMin
        dados['Limite Inferior Reativo']=reativoMin
        dados['Limite Inferior Criativo']=criativoMin
        dados['Limite Superior Adaptativo'] = adaptativoMax
        dados['Limite Superior Reativo']=reativoMax
        dados['Limite Superior Criativo']=criativoMax

        grafico = simplejson.dumps(dados)
        return grafico

    def pacienteNome(self):
        if 'paciente_id' in self.kwargs:
            paciente_id = self.kwargs['paciente_id']
        paciente = Paciente.objects.get(usuario_id=paciente_id)
        dados = { 'paciente': paciente.nome
        }

        paciente = simplejson.dumps(dados)
        return paciente

class ConsultandoAnalise(SessionWizardView):
    template_name = "projetofinal/analise/consultando.html"
    form_list = [ConsultarAreaAfetiva]

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ConsultandoAnalise, self).dispatch(*args, **kwargs)

    def paciente(self):
        if 'paciente_id' in self.kwargs:
            paciente_id = self.kwargs['paciente_id']
        paciente = Paciente.objects.get(usuario_id=paciente_id)
        return paciente

    def get_form(self, step=None, data=None, files=None):
        form = super(ConsultandoAnalise, self).get_form(step, data, files)
        if 'paciente_id' in self.kwargs:
            paciente_id = self.kwargs['paciente_id']
            try:
                paciente = Paciente.objects.get(usuario_id=paciente_id)
            except Paciente.DoesNotExist:
                raise Http404("Paciente não existe")
            if 'analise_id' in self.kwargs:
                analise_id = self.kwargs['analise_id']
            try:
                analise = Anamnesia.objects.get(id=analise_id)
            except Anamnesia.DoesNotExist:
                raise Http404("Atendimento não existe")
        lista_form=[]
        for key,value in self.form_list.items():
            if value != ConsultarAreaAfetiva:
                lista_form.append(key)
        for item in lista_form:
            self.form_list.pop(item)

        relacionamentos = Relacionamento.objects.filter(anamnesia_id = analise_id)
        for relacionamento in relacionamentos:
            if relacionamento.parente == "AvoMaterno":
                self.form_list.update({'1':RelacionamentoAvosMaternos})
                if relacionamento.filhosAntes is not None:
                    self.form_list.update({'2':RelacionamentoAvoMaternoAntes})
            if relacionamento.parente == "AvoMaterna":
                if relacionamento.filhosAntes is not None:
                    self.form_list.update({'3':RelacionamentoAvoMaternaAntes})
                if relacionamento.filhosDepois is not None:
                    self.form_list.update({'4':RelacionamentoAvosMaternosDepois})
            if relacionamento.parente == "AvoPaterno":
                self.form_list.update({'5':RelacionamentoAvosPaternos})
                if relacionamento.filhosAntes is not None:
                    self.form_list.update({'6':RelacionamentoAvoPaternoAntes})
            if relacionamento.parente == "AvoPaterna":
                if relacionamento.filhosAntes is not None:
                    self.form_list.update({'7':RelacionamentoAvoPaternaAntes})
                if relacionamento.filhosDepois is not None:
                    self.form_list.update({'8':RelacionamentoAvosPaternosDepois})
            if relacionamento.parente == "Pai":
                self.form_list.update({'9':RelacionamentoPais})
                if relacionamento.filhosAntes is not None:
                    self.form_list.update({'10':RelacionamentoPaiAntes})
            if relacionamento.parente == "Mae":
                if relacionamento.filhosAntes is not None:
                    self.form_list.update({'11':RelacionamentoMaeAntes})
                if relacionamento.filhosDepois is not None:
                    self.form_list.update({'12':RelacionamentoPaisDepois})
            if relacionamento.parente == "Paciente":
                self.form_list.update({'13':RelacionamentoPaciente})
                if relacionamento.filhosAntes is not None:
                    self.form_list.update({'14':RelacionamentoPacienteAntes})
            if relacionamento.parente == "Conjuge":
                if relacionamento.filhosAntes is not None:
                    self.form_list.update({'15':RelacionamentoConjugeAntes})
                if relacionamento.filhosDepois is not None:
                    self.form_list.update({'16':RelacionamentoPacienteDepois})
        if GrauIndiferenciacaoPaciente.objects.filter(anamnesia_id = analise_id).exists():
            self.form_list.update({'17':GrauDeIndeferenciacao})

        if Seletiva.objects.filter(anamnesia_id = analise_id).exists():
            self.form_list.update({'18':ConsultarPerguntasSeletivas})

        if Interventiva.objects.filter(anamnesia_id = analise_id).exists():
            self.form_list.update({'19':ConsultarPerguntasInterventivas})
        # determine the step if not given
        if step is None:
            step = self.steps.current

        if step == "0":
            form = ConsultarAreaAfetiva(analise_id=analise_id, data=data)
            for field in form.fields:
                form.fields[field].widget.attrs['disabled'] = True
                form.fields[field].required = False
            return form

        if step == "1":
            relacionamento = Relacionamento.objects.get(paciente_id=paciente.id,anamnesia_id=analise_id,parente="AvoMaterno")
            relacionamentoavo = Relacionamento.objects.get(paciente_id=paciente.id,anamnesia_id=analise_id,parente="AvoMaterna")
            form = RelacionamentoAvosMaternos(data=data,initial = { "relacao":relacionamento.relacao,"filhos":relacionamento.filhos,
                                                                    "filhas": relacionamento.filhas,
                                                                    "relacaoAvoMaternoAntes":relacionamento.relacaoAntes,
                                                                    "relacaoAvoMaternaAntes":relacionamentoavo.relacaoAntes})
            for field in form.fields:
                form.fields[field].widget.attrs['disabled'] = True
                form.fields[field].required = False
            if not relacionamento.filhosAntes:
                for key, value in self.form_list.items():
                    if value == RelacionamentoAvoMaternoAntes:
                        self.form_list.pop(key)
            if not relacionamentoavo.filhosAntes:
                for key, value in self.form_list.items():
                    if value == RelacionamentoAvoMaternaAntes:
                        self.form_list.pop(key)
            if not relacionamento.filhosDepois:
                for key, value in self.form_list.items():
                    if value == RelacionamentoAvosMaternosDepois:
                        self.form_list.pop(key)
            return form

        if step == "2":
            relacionamento = Relacionamento.objects.get(paciente_id=paciente.id,anamnesia_id=analise_id,parente="AvoMaterno")
            form = RelacionamentoAvoMaternoAntes(data=data,initial = { "filhosAvoMaternoAntes":relacionamento.filhosAntes,
                                                                    "filhasAvoMaternoAntes":relacionamento.filhasAntes})
            for field in form.fields:
                form.fields[field].widget.attrs['disabled'] = True
                form.fields[field].required = False
            return form


        if step == "3":
            relacionamento = Relacionamento.objects.get(paciente_id=paciente.id,anamnesia_id=analise_id,parente="AvoMaterna")
            form = RelacionamentoAvoMaternaAntes(data=data,initial = { "filhosAvoMaternaAntes":relacionamento.filhosAntes,
                                                                    "filhasAvoMaternaAntes":relacionamento.filhasAntes})
            for field in form.fields:
                form.fields[field].widget.attrs['disabled'] = True
                form.fields[field].required = False
            return form

        if step == "4":
            relacionamento = Relacionamento.objects.get(paciente_id=paciente.id,anamnesia_id=analise_id,parente="AvoMaterno")
            relacionamentoavo = Relacionamento.objects.get(paciente_id=paciente.id,anamnesia_id=analise_id,parente="AvoMaterna")
            form = RelacionamentoAvosMaternosDepois(data=data,initial = { "filhosAvoMaterno":relacionamento.filhosDepois,
                                                                          "filhasAvoMaterno":relacionamento.filhasDepois,
                                                                          "filhosAvoMaterna": relacionamentoavo.filhosDepois,
                                                                          "filhasAvoMaterna":relacionamentoavo.filhosDepois})
            for field in form.fields:
                form.fields[field].widget.attrs['disabled'] = True
                form.fields[field].required = False
            return form


        if step == "5":
            relacionamento = Relacionamento.objects.get(paciente_id=paciente.id,anamnesia_id=analise_id,parente="AvoPaterno")
            relacionamentoavo = Relacionamento.objects.get(paciente_id=paciente.id,anamnesia_id=analise_id,parente="AvoPaterna")
            form = RelacionamentoAvosPaternos(data=data,initial = { "relacao":relacionamento.relacao,"filhos":relacionamento.filhos,
                                                                    "filhas": relacionamento.filhas,
                                                                    "relacaoAvoPaternoAntes":relacionamento.relacaoAntes,
                                                                    "relacaoAvoPaternaAntes":relacionamentoavo.relacaoAntes})
            for field in form.fields:
                form.fields[field].widget.attrs['disabled'] = True
                form.fields[field].required = False
            if not relacionamento.filhosAntes:
                for key, value in self.form_list.items():
                    if value == RelacionamentoAvoPaternoAntes:
                        self.form_list.pop(key)
            if not relacionamentoavo.filhosAntes:
                for key, value in self.form_list.items():
                    if value == RelacionamentoAvoPaternaAntes:
                        self.form_list.pop(key)
            if not relacionamento.filhosDepois:
                for key, value in self.form_list.items():
                    if value == RelacionamentoAvosPaternosDepois:
                        self.form_list.pop(key)
            return form

        if step == "6":
            relacionamento = Relacionamento.objects.get(paciente_id=paciente.id,anamnesia_id=analise_id,parente="AvoPaterno")
            form = RelacionamentoAvoPaternoAntes(data=data,initial = { "filhosAvoPaternoAntes":relacionamento.filhosAntes,
                                                                    "filhasAvoPaternoAntes":relacionamento.filhasAntes})
            for field in form.fields:
                form.fields[field].widget.attrs['disabled'] = True
                form.fields[field].required = False
            return form


        if step == "7":
            relacionamento = Relacionamento.objects.get(paciente_id=paciente.id,anamnesia_id=analise_id,parente="AvoPaterna")
            form = RelacionamentoAvoPaternaAntes(data=data,initial = { "filhosAvoPaternaAntes":relacionamento.filhosAntes,
                                                                    "filhasAvoPaternaAntes":relacionamento.filhasAntes})
            for field in form.fields:
                form.fields[field].widget.attrs['disabled'] = True
                form.fields[field].required = False
            return form

        if step == "8":
            relacionamento = Relacionamento.objects.get(paciente_id=paciente.id,anamnesia_id=analise_id,parente="AvoPaterno")
            relacionamentoavo = Relacionamento.objects.get(paciente_id=paciente.id,anamnesia_id=analise_id,parente="AvoPaterna")
            form = RelacionamentoAvosPaternosDepois(data=data,initial = { "filhosAvoPaterno":relacionamento.filhosDepois,
                                                                          "filhasAvoPaterno":relacionamento.filhasDepois,
                                                                          "filhosAvoPaterna": relacionamentoavo.filhosDepois,
                                                                          "filhasAvoPaterna":relacionamentoavo.filhosDepois})
            for field in form.fields:
                form.fields[field].widget.attrs['disabled'] = True
                form.fields[field].required = False
            return form

        if step == "9":
            relacionamento = Relacionamento.objects.get(paciente_id=paciente.id,anamnesia_id=analise_id,parente="Pai")
            relacionamentomae = Relacionamento.objects.get(paciente_id=paciente.id,anamnesia_id=analise_id,parente="Mae")
            form = RelacionamentoPais(data=data,initial = { "relacao":relacionamento.relacao,"filhos":relacionamento.filhos,
                                                                    "filhas": relacionamento.filhas,
                                                                    "relacaoPaiAntes":relacionamento.relacaoAntes,
                                                                    "relacaoMaeAntes":relacionamentomae.relacaoAntes})
            for field in form.fields:
                form.fields[field].widget.attrs['disabled'] = True
                form.fields[field].required = False
            if not relacionamento.filhosAntes:
                for key, value in self.form_list.items():
                    if value == RelacionamentoPaiAntes:
                        self.form_list.pop(key)
            if not relacionamentomae.filhosAntes:
                for key, value in self.form_list.items():
                    if value == RelacionamentoMaeAntes:
                        self.form_list.pop(key)
            if not relacionamento.filhosDepois:
                for key, value in self.form_list.items():
                    if value == RelacionamentoPaisDepois:
                        self.form_list.pop(key)
            return form

        if step == "10":
            relacionamento = Relacionamento.objects.get(paciente_id=paciente.id,anamnesia_id=analise_id,parente="Pai")
            form = RelacionamentoPaiAntes(data=data,initial = { "filhosPaiAntes":relacionamento.filhosAntes,
                                                                    "filhasPaiAntes":relacionamento.filhasAntes})
            for field in form.fields:
                form.fields[field].widget.attrs['disabled'] = True
                form.fields[field].required = False
            return form


        if step == "11":
            relacionamento = Relacionamento.objects.get(paciente_id=paciente.id,anamnesia_id=analise_id,parente="Mae")
            form = RelacionamentoMaeAntes(data=data,initial = { "filhosMaeAntes":relacionamento.filhosAntes,
                                                                    "filhasMaeAntes":relacionamento.filhasAntes})
            for field in form.fields:
                form.fields[field].widget.attrs['disabled'] = True
                form.fields[field].required = False
            return form

        if step == "12":
            relacionamento = Relacionamento.objects.get(paciente_id=paciente.id,anamnesia_id=analise_id,parente="Pai")
            relacionamentomae = Relacionamento.objects.get(paciente_id=paciente.id,anamnesia_id=analise_id,parente="Mae")
            form = RelacionamentoPaisDepois(data=data,initial = { "filhosPai":relacionamento.filhosDepois,
                                                                          "filhasPai":relacionamento.filhasDepois,
                                                                          "filhosMae": relacionamentomae.filhosDepois,
                                                                          "filhasMae":relacionamentomae.filhosDepois})
            for field in form.fields:
                form.fields[field].widget.attrs['disabled'] = True
                form.fields[field].required = False
            return form

        if step == "13":
            relacionamento = Relacionamento.objects.get(paciente_id=paciente.id,anamnesia_id=analise_id,parente="Paciente")
            relacionamentoconjuge = Relacionamento.objects.get(paciente_id=paciente.id,anamnesia_id=analise_id,parente="Conjuge")
            form = RelacionamentoPaciente(data=data,initial = { "relacao":relacionamento.relacao,"filhos":relacionamento.filhos,
                                                                    "filhas": relacionamento.filhas,
                                                                    "relacaoPacienteAntes":relacionamento.relacaoAntes,
                                                                    "relacaoConjugeAntes":relacionamentoconjuge.relacaoAntes})
            for field in form.fields:
                form.fields[field].widget.attrs['disabled'] = True
                form.fields[field].required = False
            if not relacionamento.filhosAntes:
                for key, value in self.form_list.items():
                    if value == RelacionamentoPacienteAntes:
                        self.form_list.pop(key)
            if not relacionamentoconjuge.filhosAntes:
                for key, value in self.form_list.items():
                    if value == RelacionamentoConjugeAntes:
                        self.form_list.pop(key)
            if not relacionamento.filhosDepois:
                for key, value in self.form_list.items():
                    if value == RelacionamentoPacienteDepois:
                        self.form_list.pop(key)
            return form

        if step == "14":
            relacionamento = Relacionamento.objects.get(paciente_id=paciente.id,anamnesia_id=analise_id,parente="Paciente")
            form = RelacionamentoPacienteAntes(data=data,initial = { "filhosPacienteAntes":relacionamento.filhosAntes,
                                                                    "filhasPacienteAntes":relacionamento.filhasAntes})
            for field in form.fields:
                form.fields[field].widget.attrs['disabled'] = True
                form.fields[field].required = False
            return form


        if step == "15":
            relacionamento = Relacionamento.objects.get(paciente_id=paciente.id,anamnesia_id=analise_id,parente="Conjuge")
            form = RelacionamentoConjugeAntes(data=data,initial = { "filhosConjugeAntes":relacionamento.filhosAntes,
                                                                    "filhasConjugeAntes":relacionamento.filhasAntes})
            for field in form.fields:
                form.fields[field].widget.attrs['disabled'] = True
                form.fields[field].required = False
            return form

        if step == "16":
            relacionamento = Relacionamento.objects.get(paciente_id=paciente.id,anamnesia_id=analise_id,parente="Paciente")
            relacionamentoconjuge = Relacionamento.objects.get(paciente_id=paciente.id,anamnesia_id=analise_id,parente="Conjuge")
            form = RelacionamentoPacienteDepois(data=data,initial = { "filhosPaciente":relacionamento.filhosDepois,
                                                                          "filhasPaciente":relacionamento.filhasDepois,
                                                                          "filhosConjuge": relacionamentoconjuge.filhosDepois,
                                                                          "filhasConjuge":relacionamentoconjuge.filhosDepois})
            for field in form.fields:
                form.fields[field].widget.attrs['disabled'] = True
                form.fields[field].required = False
            return form


        if step == "17":
            indiferenciacao = GrauIndiferenciacaoPaciente.objects.filter(paciente_id=paciente.id,anamnesia_id=analise_id)
            selecionadas = []
            for item in indiferenciacao:
                selecionadas.append(str(item.resposta.id))
            form = GrauDeIndeferenciacao(data=data,initial= {"grauIndiferenciacao":selecionadas})
            for field in form.fields:
                form.fields[field].widget.attrs['disabled'] = True
                form.fields[field].required = False
            return form

        if step == "18":
            form = ConsultarPerguntasSeletivas(analise_id=analise_id, data=data)
            for field in form.fields:
                form.fields[field].widget.attrs['disabled'] = True
                form.fields[field].required = False
            return form

        if step == "19":
            form = ConsultarPerguntasInterventivas(analise_id=analise_id, data=data)
            for field in form.fields:
                form.fields[field].widget.attrs['disabled'] = True
                form.fields[field].required = False
            return form


class ProsseguirAnalise(TemplateView):
    template_name="projetofinal/analise/prosseguir.html"


    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ProsseguirAnalise, self).dispatch(*args, **kwargs)

    def anamnesia(self):
        if 'paciente_id' in self.kwargs:
            paciente_id = self.kwargs['paciente_id']
        paciente = Paciente.objects.get(usuario_id=paciente_id)
        if Anamnesia.objects.filter(paciente_id=paciente.id).exists():
            anamnesia = Anamnesia.objects.filter(paciente_id=paciente.id).last()
            agora=datetime.now()
            inicio =anamnesia.inicio
            tempo=agora-inicio
            paciente.tempo= 30 - tempo.days
            paciente.save()
        anamnesia = Anamnesia.objects.filter(paciente_id=paciente.id)
        for analise in anamnesia:
            if Interventiva.objects.filter(anamnesia_id = analise.id).exists():
                anamnesia = anamnesia.exclude(id = analise.id)
        return anamnesia

    def indiferenciacao(self):
        indiferenciacao=0
        if 'paciente_id' in self.kwargs:
            paciente_id = self.kwargs['paciente_id']
        paciente = Paciente.objects.get(usuario_id=paciente_id)
        anamnesia = Anamnesia.objects.filter(paciente_id=paciente.id)
        for analise in anamnesia:
            if GrauIndiferenciacaoPaciente.objects.filter(anamnesia_id=analise.id).exists():
                indiferenciacao=1
        return indiferenciacao


    def grafico(self):
        if 'paciente_id' in self.kwargs:
            paciente_id = self.kwargs['paciente_id']
        paciente = Paciente.objects.get(usuario_id=paciente_id)
        dados = {
        }
        anamnesia = Anamnesia.objects.filter(paciente_id=paciente.id)
        for analise in anamnesia:
            if Interventiva.objects.filter(anamnesia_id = analise.id).exists():
                anamnesia = anamnesia.exclude(id = analise.id)
        for analise in anamnesia:
            area= AreaAfetiva.objects.filter(anamnesia_id=analise.id).order_by('resposta_id')
            A=[0]
            for respostas in area:
                resposta = RespostaAreaAfetiva.objects.get(id=respostas.resposta_id)
                A.append(resposta.valor)
            afetivoRelacional=((A[1]+A[2]+A[4]+A[6]+A[9]+A[13]+A[15]+A[17]+A[19]+A[20]+A[21]+A[22]+A[23]+A[25]+A[28])/15)
            produtividade=((A[5]+A[16]+A[20]+A[22]+A[23])/5)
            organico=((A[7]+A[12]+A[14]+A[27]+A[29])/5)
            espiritual=((A[3]+A[11]+A[18]+A[24]+A[26])/5)
            socioCultural=((A[8]+A[10]+A[20]+A[22]+A[23])/5)
            dados[str(analise.inicio.strftime("%d/%m/%y %H:%M:%S"))] = [afetivoRelacional]
            dados[str(analise.inicio.strftime("%d/%m/%y %H:%M:%S"))].append(produtividade)
            dados[str(analise.inicio.strftime("%d/%m/%y %H:%M:%S"))].append(organico)
            dados[str(analise.inicio.strftime("%d/%m/%y %H:%M:%S"))].append(espiritual)
            dados[str(analise.inicio.strftime("%d/%m/%y %H:%M:%S"))].append(socioCultural)

        grafico = simplejson.dumps(dados)
        return grafico

    def graficoRadar(self):
        if 'paciente_id' in self.kwargs:
            paciente_id = self.kwargs['paciente_id']
        paciente = Paciente.objects.get(usuario_id=paciente_id)
        dados = {
        }
        anamnesia = Anamnesia.objects.filter(paciente_id=paciente.id)
        criativo=0
        reativo=0
        adaptativo=0
        for analise in anamnesia:
            if GrauIndiferenciacaoPaciente.objects.filter(anamnesia_id=analise.id).exists():
                indiferenciacao = GrauIndiferenciacaoPaciente.objects.filter(anamnesia_id=analise.id)
                for opcao in indiferenciacao:
                    resposta = GrauIndiferenciacao.objects.get(id=opcao.resposta_id)
                    if resposta.padrao == "adaptativo":
                        adaptativo=adaptativo+1
                    if resposta.padrao == "reativo":
                        reativo=reativo+1
                    if resposta.padrao == "criativo":
                        criativo=criativo+1

                dados[str(analise.inicio.strftime("%d/%m/%y %H:%M:%S"))] = [adaptativo]
                dados[str(analise.inicio.strftime("%d/%m/%y %H:%M:%S"))].append(reativo)
                dados[str(analise.inicio.strftime("%d/%m/%y %H:%M:%S"))].append(criativo)


        nascimento=str(paciente.nascimento)
        ano = int(nascimento.split("-")[0])
        mes=int(nascimento.split("-")[1])
        dia=int(nascimento.split("-")[2])
        atual=datetime.now()
        anoAtual=atual.year
        mesAtual=atual.month
        diaAtual=atual.day

        if mes > mesAtual:
            idade = anoAtual-ano-1
        if mes < mesAtual:
            idade = anoAtual-ano
        if mes == mesAtual:
            if dia >= diaAtual:
                idade = anoAtual-ano-1
            if dia < diaAtual:
                idade = anoAtual-ano

        adaptativoMin=0
        adaptativoMax=0
        criativoMin=0
        criativoMax=0
        reativoMin=0
        reativoMax=0

        if idade >=0 and idade <=3:
            adaptativoMin=14
            adaptativoMax=17
            criativoMin=0
            criativoMax=2
            reativoMin=0
            reativoMax=2
        if idade >=4 and idade <=7:
            adaptativoMin=12
            adaptativoMax=17
            criativoMin=0
            criativoMax=3
            reativoMin=2
            reativoMax=6
        if idade >=8 and idade <=12:
            adaptativoMin=8
            adaptativoMax=13
            criativoMin=2
            criativoMax=5
            reativoMin=6
            reativoMax=10
        if idade >=13 and idade <=19:
            adaptativoMin=4
            adaptativoMax=8
            criativoMin=6
            criativoMax=8
            reativoMin=10
            reativoMax=15
        if idade >=20 and idade <=24:
            adaptativoMin=1
            adaptativoMax=3
            criativoMin=9
            criativoMax=11
            reativoMin=8
            reativoMax=12
        if idade >=25 and idade <=32:
            adaptativoMin=0
            adaptativoMax=2
            criativoMin=11
            criativoMax=15
            reativoMin=3
            reativoMax=7
        if idade >=33:
            adaptativoMin=0
            adaptativoMax=2
            criativoMin=16
            criativoMax=19
            reativoMin=0
            reativoMax=2

        dados['Limite Inferior Adaptativo'] = adaptativoMin
        dados['Limite Inferior Reativo']=reativoMin
        dados['Limite Inferior Criativo']=criativoMin
        dados['Limite Superior Adaptativo'] = adaptativoMax
        dados['Limite Superior Reativo']=reativoMax
        dados['Limite Superior Criativo']=criativoMax

        grafico = simplejson.dumps(dados)
        return grafico

    def pacienteNome(self):
        if 'paciente_id' in self.kwargs:
            paciente_id = self.kwargs['paciente_id']
        paciente = Paciente.objects.get(usuario_id=paciente_id)
        dados = { 'paciente': paciente.nome
        }
        paciente = simplejson.dumps(dados)
        return paciente

    def paciente(self):
        if 'paciente_id' in self.kwargs:
            paciente_id = self.kwargs['paciente_id']
        paciente = Paciente.objects.get(usuario_id=paciente_id)
        return paciente

@login_required()
def ProsseguindoAnalise(request,paciente_id,analise_id):

    parentes = ["AvoMaterno","AvoMaterna","AvoPaterno","AvoPaterna","Pai","Mae","Paciente","Conjuge"]
    for parente in parentes:
        if not Relacionamento.objects.filter(anamnesia_id = analise_id, parente=parente).exists():
            return HttpResponseRedirect('/analise/resumo/'+paciente_id+'/'+analise_id+'/relacionamentos')
    relacionamentos = Relacionamento.objects.filter(anamnesia_id = analise_id)
    for relacionamento in relacionamentos:
        if relacionamento.parente == "Paciente":
            relacao = relacionamento.relacao
            if relacionamento.relacaoAntes == "Sim" and relacionamento.filhosAntes is None:
                return HttpResponseRedirect('/analise/resumo/'+paciente_id+'/'+analise_id+'/relacionamentos')
            if (relacionamento.relacao == "Separado(a)" or relacionamento.relacao == "Divorciado(a)") and\
                    (relacionamento.filhosDepois is None):
                return HttpResponseRedirect('/analise/resumo/'+paciente_id+'/'+analise_id+'/relacionamentos')
        if relacionamento.parente == "Conjuge":
            if relacionamento.relacaoAntes == "Sim" and relacionamento.filhosAntes is None:
                return HttpResponseRedirect('/analise/resumo/'+paciente_id+'/'+analise_id+'/relacionamentos')

    if not GrauIndiferenciacaoPaciente.objects.filter(anamnesia_id = analise_id).exists():
        return HttpResponseRedirect('/analise/inserir/'+paciente_id+'/'+analise_id+'/indiferenciacao')

    if not Seletiva.objects.filter(anamnesia_id = analise_id).exists():
        return HttpResponseRedirect('/analise/resumo/'+paciente_id+'/'+analise_id+'/seletiva')

    verificador = False
    selecionadas = []
    perguntas = PerguntaSeletiva.objects.filter(tipo = "condicionada")
    for item in perguntas:
        respostas = RespostaSeletiva.objects.filter(pergunta_id=item.id)
        for resposta in respostas:
            selecionadas.append(resposta.id)
    for selecionada in selecionadas:
        if Seletiva.objects.filter(anamnesia_id = analise_id,resposta_id=selecionada).exists():
            verificador = True
    if verificador == False and (relacao == "Casado(a)" or relacao == "Mora junto"):
        return HttpResponseRedirect('/analise/resumo/'+paciente_id+'/'+analise_id+'/seletiva')

    if not Interventiva.objects.filter(anamnesia_id = analise_id).exists():
        return HttpResponseRedirect('/analise/resumo/'+paciente_id+'/'+analise_id+'/tarefas')

@login_required()
def RemoverAnalise(request, paciente_id):

    if request.POST:
        analises = request.POST.getlist("analise")
    for analise in analises:
        Anamnesia.objects.filter(id=analise).delete()
        AreaAfetiva.objects.filter(anamnesia_id=analise).delete()
        Relacionamento.objects.filter(anamnesia_id=analise).delete()
        GrauIndiferenciacaoPaciente.objects.filter(anamnesia_id=analise).delete()
        Seletiva.objects.filter(anamnesia_id=analise).delete()
        Interventiva.objects.filter(anamnesia_id=analise).delete()
    paciente = Paciente.objects.get(usuario_id=paciente_id)
    return render(request,"projetofinal/analise/removida.html", {'paciente': paciente},context_instance=RequestContext(request))

class AnaliseRemovida(TemplateView):
    template_name = "projetofinal/analise/removida.html"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(AnaliseRemovida, self).dispatch(*args, **kwargs)

    def paciente(self):
        if 'paciente_id' in self.kwargs:
            paciente_id = self.kwargs['paciente_id']
        paciente = Paciente.objects.get(usuario_id=paciente_id)

        return paciente

class Recomendacoes(TemplateView):
    template_name = "projetofinal/analise/recomendacao/home.html"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(Recomendacoes, self).dispatch(*args, **kwargs)

    def anamnesia(self):
        if 'paciente_id' in self.kwargs:
            paciente_id = self.kwargs['paciente_id']
        paciente = Paciente.objects.get(usuario_id=paciente_id)
        anamnesia = Anamnesia.objects.filter(paciente_id=paciente.id)

        return anamnesia

    def indiferenciacao(self):
        indiferenciacao=0
        if 'paciente_id' in self.kwargs:
            paciente_id = self.kwargs['paciente_id']
        paciente = Paciente.objects.get(usuario_id=paciente_id)
        anamnesia = Anamnesia.objects.filter(paciente_id=paciente.id)
        for analise in anamnesia:
            if GrauIndiferenciacaoPaciente.objects.filter(anamnesia_id=analise.id).exists():
                indiferenciacao=1
        return indiferenciacao

    def grafico(self):
        if 'paciente_id' in self.kwargs:
            paciente_id = self.kwargs['paciente_id']
        paciente = Paciente.objects.get(usuario_id=paciente_id)
        dados = {
        }
        anamnesia = Anamnesia.objects.filter(paciente_id=paciente.id)
        for analise in anamnesia:
            area= AreaAfetiva.objects.filter(anamnesia_id=analise.id).order_by('resposta_id')
            A=[0]
            for respostas in area:
                resposta = RespostaAreaAfetiva.objects.get(id=respostas.resposta_id)
                A.append(resposta.valor)
            afetivoRelacional=((A[1]+A[2]+A[4]+A[6]+A[9]+A[13]+A[15]+A[17]+A[19]+A[20]+A[21]+A[22]+A[23]+A[25]+A[28])/15)
            produtividade=((A[5]+A[16]+A[20]+A[22]+A[23])/5)
            organico=((A[7]+A[12]+A[14]+A[27]+A[29])/5)
            espiritual=((A[3]+A[11]+A[18]+A[24]+A[26])/5)
            socioCultural=((A[8]+A[10]+A[20]+A[22]+A[23])/5)
            dados[str(analise.inicio.strftime("%d/%m/%y %H:%M:%S"))] = [afetivoRelacional]
            dados[str(analise.inicio.strftime("%d/%m/%y %H:%M:%S"))].append(produtividade)
            dados[str(analise.inicio.strftime("%d/%m/%y %H:%M:%S"))].append(organico)
            dados[str(analise.inicio.strftime("%d/%m/%y %H:%M:%S"))].append(espiritual)
            dados[str(analise.inicio.strftime("%d/%m/%y %H:%M:%S"))].append(socioCultural)


        grafico = simplejson.dumps(dados)
        return grafico

    def graficoRadar(self):
        if 'paciente_id' in self.kwargs:
            paciente_id = self.kwargs['paciente_id']
        paciente = Paciente.objects.get(usuario_id=paciente_id)
        dados = {
        }
        anamnesia = Anamnesia.objects.filter(paciente_id=paciente.id)
        criativo=0
        reativo=0
        adaptativo=0
        for analise in anamnesia:
            if GrauIndiferenciacaoPaciente.objects.filter(anamnesia_id=analise.id).exists():
                indiferenciacao = GrauIndiferenciacaoPaciente.objects.filter(anamnesia_id=analise.id)
                for opcao in indiferenciacao:
                    resposta = GrauIndiferenciacao.objects.get(id=opcao.resposta_id)
                    if resposta.padrao == "adaptativo":
                        adaptativo=adaptativo+1
                    if resposta.padrao == "reativo":
                        reativo=reativo+1
                    if resposta.padrao == "criativo":
                        criativo=criativo+1

                dados[str(analise.inicio.strftime("%d/%m/%y %H:%M:%S"))] = [adaptativo]
                dados[str(analise.inicio.strftime("%d/%m/%y %H:%M:%S"))].append(reativo)
                dados[str(analise.inicio.strftime("%d/%m/%y %H:%M:%S"))].append(criativo)

        nascimento=str(paciente.nascimento)
        ano = int(nascimento.split("-")[0])
        mes=int(nascimento.split("-")[1])
        dia=int(nascimento.split("-")[2])
        atual=datetime.now()
        anoAtual=atual.year
        mesAtual=atual.month
        diaAtual=atual.day

        if mes > mesAtual:
            idade = anoAtual-ano-1
        if mes < mesAtual:
            idade = anoAtual-ano
        if mes == mesAtual:
            if dia >= diaAtual:
                idade = anoAtual-ano-1
            if dia < diaAtual:
                idade = anoAtual-ano

        adaptativoMin=0
        adaptativoMax=0
        criativoMin=0
        criativoMax=0
        reativoMin=0
        reativoMax=0

        if idade >=0 and idade <=3:
            adaptativoMin=14
            adaptativoMax=17
            criativoMin=0
            criativoMax=2
            reativoMin=0
            reativoMax=2
        if idade >=4 and idade <=7:
            adaptativoMin=12
            adaptativoMax=17
            criativoMin=0
            criativoMax=3
            reativoMin=2
            reativoMax=6
        if idade >=8 and idade <=12:
            adaptativoMin=8
            adaptativoMax=13
            criativoMin=2
            criativoMax=5
            reativoMin=6
            reativoMax=10
        if idade >=13 and idade <=19:
            adaptativoMin=4
            adaptativoMax=8
            criativoMin=6
            criativoMax=8
            reativoMin=10
            reativoMax=15
        if idade >=20 and idade <=24:
            adaptativoMin=1
            adaptativoMax=3
            criativoMin=9
            criativoMax=11
            reativoMin=8
            reativoMax=12
        if idade >=25 and idade <=32:
            adaptativoMin=0
            adaptativoMax=2
            criativoMin=11
            criativoMax=15
            reativoMin=3
            reativoMax=7
        if idade >=33:
            adaptativoMin=0
            adaptativoMax=2
            criativoMin=16
            criativoMax=19
            reativoMin=0
            reativoMax=2

        dados['Limite Inferior Adaptativo'] = adaptativoMin
        dados['Limite Inferior Reativo']=reativoMin
        dados['Limite Inferior Criativo']=criativoMin
        dados['Limite Superior Adaptativo'] = adaptativoMax
        dados['Limite Superior Reativo']=reativoMax
        dados['Limite Superior Criativo']=criativoMax

        grafico = simplejson.dumps(dados)
        return grafico

    def pacienteNome(self):
        if 'paciente_id' in self.kwargs:
            paciente_id = self.kwargs['paciente_id']
        paciente = Paciente.objects.get(usuario_id=paciente_id)
        dados = { 'paciente': paciente.nome
        }

        paciente = simplejson.dumps(dados)
        return paciente

    def paciente(self):
        if 'paciente_id' in self.kwargs:
            paciente_id = self.kwargs['paciente_id']
        paciente = Paciente.objects.get(usuario_id=paciente_id)
        return paciente

class ConsultandoRecomendacoes(TemplateView):
    template_name= "projetofinal/analise/recomendacao/consultando.html"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ConsultandoRecomendacoes, self).dispatch(*args, **kwargs)

    def anamnesia(self):
        if 'paciente_id' in self.kwargs:
            paciente_id = self.kwargs['paciente_id']
        if 'analise_id' in self.kwargs:
            analise_id = self.kwargs['analise_id']
        anamnesia = Anamnesia.objects.get(id=analise_id)
        main(paciente_id,analise_id)
        return anamnesia

    def usuario(self):
        if 'paciente_id' in self.kwargs:
            paciente_id = self.kwargs['paciente_id']
        paciente = Paciente.objects.get(usuario_id=paciente_id)

        return paciente

    def pacienteNome(self):
        if 'paciente_id' in self.kwargs:
            paciente_id = self.kwargs['paciente_id']
        paciente = Paciente.objects.get(usuario_id=paciente_id)
        dados = { 'paciente': paciente.nome
        }

        paciente = simplejson.dumps(dados)
        return paciente

    def paciente(self):
        if 'paciente_id' in self.kwargs:
            paciente_id = self.kwargs['paciente_id']
        paciente = Paciente.objects.get(usuario_id=paciente_id)
        return paciente

    def graficoAreaAfetiva(self):
        if 'paciente_id' in self.kwargs:
            paciente_id = self.kwargs['paciente_id']
        if 'analise_id' in self.kwargs:
            analise_id = self.kwargs['analise_id']
        paciente = Paciente.objects.get(usuario_id=paciente_id)
        dados = {
        }
        anamnesia = Anamnesia.objects.filter(id=analise_id)
        for analise in anamnesia:
            area= AreaAfetiva.objects.filter(anamnesia_id=analise.id).order_by('resposta_id')
            A=[0]
            for respostas in area:
                resposta = RespostaAreaAfetiva.objects.get(id=respostas.resposta_id)
                A.append(resposta.valor)
            afetivoRelacional=((A[1]+A[2]+A[4]+A[6]+A[9]+A[13]+A[15]+A[17]+A[19]+A[20]+A[21]+A[22]+A[23]+A[25]+A[28])/15)
            produtividade=((A[5]+A[16]+A[20]+A[22]+A[23])/5)
            organico=((A[7]+A[12]+A[14]+A[27]+A[29])/5)
            espiritual=((A[3]+A[11]+A[18]+A[24]+A[26])/5)
            socioCultural=((A[8]+A[10]+A[20]+A[22]+A[23])/5)
            dados[str(analise.inicio.strftime("%d/%m/%y %H:%M:%S"))] = [afetivoRelacional]
            dados[str(analise.inicio.strftime("%d/%m/%y %H:%M:%S"))].append(produtividade)
            dados[str(analise.inicio.strftime("%d/%m/%y %H:%M:%S"))].append(organico)
            dados[str(analise.inicio.strftime("%d/%m/%y %H:%M:%S"))].append(espiritual)
            dados[str(analise.inicio.strftime("%d/%m/%y %H:%M:%S"))].append(socioCultural)


        grafico = simplejson.dumps(dados)
        return grafico

    def textoAreaAfetiva(self):
        if 'paciente_id' in self.kwargs:
            paciente_id = self.kwargs['paciente_id']
        if 'analise_id' in self.kwargs:
            analise_id = self.kwargs['analise_id']
        paciente = Paciente.objects.get(usuario_id=paciente_id)
        dados = {
        }
        anamnesia = Anamnesia.objects.filter(id=analise_id)
        for analise in anamnesia:
            area= AreaAfetiva.objects.filter(anamnesia_id=analise.id).order_by('resposta_id')
            A=[0]
            for respostas in area:
                resposta = RespostaAreaAfetiva.objects.get(id=respostas.resposta_id)
                A.append(resposta.valor)
            afetivoRelacional=((A[1]+A[2]+A[4]+A[6]+A[9]+A[13]+A[15]+A[17]+A[19]+A[20]+A[21]+A[22]+A[23]+A[25]+A[28])/15)
            produtividade=((A[5]+A[16]+A[20]+A[22]+A[23])/5)
            organico=((A[7]+A[12]+A[14]+A[27]+A[29])/5)
            espiritual=((A[3]+A[11]+A[18]+A[24]+A[26])/5)
            socioCultural=((A[8]+A[10]+A[20]+A[22]+A[23])/5)

        texto=""
        if afetivoRelacional >= 3 and afetivoRelacional <= 4:
            complementox = Recomendacao.objects.get(nome="complementox",intervalo="Máximo")
            complementoy = Recomendacao.objects.get(nome="complementoy",intervalo="Máximo")
        if afetivoRelacional >= 1.5 and afetivoRelacional < 3:
            complementox = Recomendacao.objects.get(nome="complementox",intervalo="Médio")
            complementoy = Recomendacao.objects.get(nome="complementoy",intervalo="Médio")
        if afetivoRelacional >= 0 and afetivoRelacional < 1.5:
            complementox = Recomendacao.objects.get(nome="complementox",intervalo="Mínimo")
            complementoy = Recomendacao.objects.get(nome="complementoy",intervalo="Mínimo")
        if produtividade >= 3 and produtividade <= 4:
            PRODUTIVIDADE = Recomendacao.objects.get(nome="produtividade",intervalo="Máximo")
        if produtividade >= 1.5 and produtividade < 3:
            PRODUTIVIDADE = Recomendacao.objects.get(nome="produtividade",intervalo="Médio")
        if produtividade >= 0 and produtividade < 1.5:
            PRODUTIVIDADE = Recomendacao.objects.get(nome="produtividade",intervalo="Mínimo")
        if organico >= 3 and organico <= 4:
            ORGANICO = Recomendacao.objects.get(nome="organico",intervalo="Máximo")
        if organico >= 1.5 and organico < 3:
            ORGANICO = Recomendacao.objects.get(nome="organico",intervalo="Médio")
        if organico >= 0 and organico < 1.5:
            ORGANICO = Recomendacao.objects.get(nome="organico",intervalo="Mínimo")
        if espiritual >= 3 and espiritual <= 4:
            ESPIRITUAL = Recomendacao.objects.get(nome="espiritual",intervalo="Máximo")
        if espiritual >= 1.5 and espiritual < 3:
            ESPIRITUAL = Recomendacao.objects.get(nome="espiritual",intervalo="Médio")
        if espiritual >= 0 and espiritual < 1.5:
            ESPIRITUAL = Recomendacao.objects.get(nome="espiritual",intervalo="Mínimo")
        if socioCultural >= 3 and socioCultural <= 4:
            SOCIOCULTURAL = Recomendacao.objects.get(nome="sociocultural",intervalo="Máximo")
        if socioCultural >= 1.5 and socioCultural < 3:
            SOCIOCULTURAL = Recomendacao.objects.get(nome="sociocultural",intervalo="Médio")
        if socioCultural >= 0 and socioCultural < 1.5:
            SOCIOCULTURAL = Recomendacao.objects.get(nome="sociocultural",intervalo="Mínimo")

        lista = [(organico,"a"),(produtividade,"b"),(socioCultural, "c"),(espiritual,"d")]
        minimo = min(lista, key=lambda x: x[0])
        if minimo[0] == produtividade:
            area = PRODUTIVIDADE.texto
        if minimo[0] == organico:
            area = ORGANICO.texto
        if minimo[0] ==  espiritual:
            area = ESPIRITUAL.texto
        if minimo[0] == socioCultural:
            area = SOCIOCULTURAL.texto

        parte1 = Recomendacao.objects.get(nome="afetivorelacional",intervalo="parte1")
        parte2 = Recomendacao.objects.get(nome="afetivorelacional",intervalo="parte2")
        parte3 = Recomendacao.objects.get(nome="afetivorelacional",intervalo="parte3")
        AFETIVORELACIONAL= parte1.texto+ complementox.texto+parte2.texto+complementoy.texto+parte3.texto
        texto = AFETIVORELACIONAL + area

        return texto

    def indiferenciacao(self):
        if 'analise_id' in self.kwargs:
            analise_id = self.kwargs['analise_id']
        indiferenciacao = GrauIndiferenciacaoPaciente.objects.filter(anamnesia_id=analise_id)

        return indiferenciacao

    def media(self):
        if 'paciente_id' in self.kwargs:
            paciente_id = self.kwargs['paciente_id']
        if 'analise_id' in self.kwargs:
            analise_id = self.kwargs['analise_id']
        paciente = Paciente.objects.get(usuario_id=paciente_id)

        nascimento=str(paciente.nascimento)
        ano = int(nascimento.split("-")[0])
        mes=int(nascimento.split("-")[1])
        dia=int(nascimento.split("-")[2])
        atual=datetime.now()
        anoAtual=atual.year
        mesAtual=atual.month
        diaAtual=atual.day

        if mes > mesAtual:
            idade = anoAtual-ano-1
        if mes < mesAtual:
            idade = anoAtual-ano
        if mes == mesAtual:
            if dia >= diaAtual:
                idade = anoAtual-ano-1
            if dia < diaAtual:
                idade = anoAtual-ano

        soma=0.0
        contador=0.0
        desvio=0.0
        variancia=0.0
        areaafetiva = AreaAfetiva.objects.filter(paciente_id=paciente.id,anamnesia_id=analise_id)

        for item in areaafetiva:
            resposta = RespostaAreaAfetiva.objects.get(id=item.resposta_id)

            if idade >=0 and idade <=7:
                soma = soma + resposta.nivel1
                if resposta.nivel1 != 0:
                    contador = contador+1
            if idade >=8 and idade <=12:
                soma = soma + resposta.nivel2
                if resposta.nivel2 != 0:
                    contador = contador+1
            if idade >=13 and idade <=19:
                soma = soma + resposta.nivel3
                if resposta.nivel3 != 0:
                    contador = contador+1
            if idade >=20 and idade <=24:
                soma = soma + resposta.nivel4
                if resposta.nivel4 != 0:
                    contador = contador+1
            if idade >=25:
                soma = soma + resposta.nivel5
                if resposta.nivel5 != 0:
                    contador = contador+1

        media = soma/contador
        contador=0
        for item in areaafetiva:
            resposta = RespostaAreaAfetiva.objects.get(id=item.resposta_id)

            if idade >=0 and idade <=7:
                if resposta.nivel1 != 0:
                    contador = contador+1
                    variancia= variancia + ((resposta.nivel1 - media)*(resposta.nivel1 - media))
            if idade >=8 and idade <=12:
                if resposta.nivel2 != 0:
                    contador = contador+1
                    variancia= variancia + ((resposta.nivel2 - media)*(resposta.nivel2 - media))
            if idade >=13 and idade <=19:
                if resposta.nivel3 != 0:
                    contador = contador+1
                    variancia= variancia + ((resposta.nivel3 - media)*(resposta.nivel3 - media))
            if idade >=20 and idade <=24:
                if resposta.nivel4 != 0:
                    contador = contador+1
                    variancia= variancia + ((resposta.nivel4 - media)*(resposta.nivel4 - media))
            if idade >=25:
                if resposta.nivel5 != 0:
                    contador = contador+1
                    variancia= variancia + ((resposta.nivel5 - media)*(resposta.nivel5 - media))

        desvio = math.sqrt(variancia/(contador-1))
        dict={
            "media":media,
            "desvio":desvio
        }
        return dict

    def graficoIndiferenciacao(self):
        if 'paciente_id' in self.kwargs:
            paciente_id = self.kwargs['paciente_id']
        if 'analise_id' in self.kwargs:
            analise_id = self.kwargs['analise_id']
        paciente = Paciente.objects.get(usuario_id=paciente_id)
        dados = {
        }
        anamnesia = Anamnesia.objects.filter(id=analise_id)
        criativo=0
        reativo=0
        adaptativo=0
        for analise in anamnesia:
            indiferenciacao = GrauIndiferenciacaoPaciente.objects.filter(anamnesia_id=analise.id)
            for opcao in indiferenciacao:
                resposta = GrauIndiferenciacao.objects.get(id=opcao.resposta_id)
                if resposta.padrao == "adaptativo":
                    adaptativo=adaptativo+1
                if resposta.padrao == "reativo":
                    reativo=reativo+1
                if resposta.padrao == "criativo":
                    criativo=criativo+1

            dados[str(analise.inicio.strftime("%d/%m/%y %H:%M:%S"))] = [adaptativo]
            dados[str(analise.inicio.strftime("%d/%m/%y %H:%M:%S"))].append(reativo)
            dados[str(analise.inicio.strftime("%d/%m/%y %H:%M:%S"))].append(criativo)

        nascimento=str(paciente.nascimento)
        ano = int(nascimento.split("-")[0])
        mes=int(nascimento.split("-")[1])
        dia=int(nascimento.split("-")[2])
        atual=datetime.now()
        anoAtual=atual.year
        mesAtual=atual.month
        diaAtual=atual.day

        if mes > mesAtual:
            idade = anoAtual-ano-1
        if mes < mesAtual:
            idade = anoAtual-ano
        if mes == mesAtual:
            if dia >= diaAtual:
                idade = anoAtual-ano-1
            if dia < diaAtual:
                idade = anoAtual-ano

        adaptativoMin=0
        adaptativoMax=0
        criativoMin=0
        criativoMax=0
        reativoMin=0
        reativoMax=0

        if idade >=0 and idade <=3:
            adaptativoMin=14
            adaptativoMax=17
            criativoMin=0
            criativoMax=2
            reativoMin=0
            reativoMax=2
        if idade >=4 and idade <=7:
            adaptativoMin=12
            adaptativoMax=17
            criativoMin=0
            criativoMax=3
            reativoMin=2
            reativoMax=6
        if idade >=8 and idade <=12:
            adaptativoMin=8
            adaptativoMax=13
            criativoMin=2
            criativoMax=5
            reativoMin=6
            reativoMax=10
        if idade >=13 and idade <=19:
            adaptativoMin=4
            adaptativoMax=8
            criativoMin=6
            criativoMax=8
            reativoMin=10
            reativoMax=15
        if idade >=20 and idade <=24:
            adaptativoMin=1
            adaptativoMax=3
            criativoMin=9
            criativoMax=11
            reativoMin=8
            reativoMax=12
        if idade >=25 and idade <=32:
            adaptativoMin=0
            adaptativoMax=2
            criativoMin=11
            criativoMax=15
            reativoMin=3
            reativoMax=7
        if idade >=33:
            adaptativoMin=0
            adaptativoMax=2
            criativoMin=16
            criativoMax=19
            reativoMin=0
            reativoMax=2

        dados['Limite Inferior Adaptativo'] = adaptativoMin
        dados['Limite Inferior Reativo']=reativoMin
        dados['Limite Inferior Criativo']=criativoMin
        dados['Limite Superior Adaptativo'] = adaptativoMax
        dados['Limite Superior Reativo']=reativoMax
        dados['Limite Superior Criativo']=criativoMax

        grafico = simplejson.dumps(dados)
        return grafico

    def textoIndiferenciacao(self):
        if 'paciente_id' in self.kwargs:
            paciente_id = self.kwargs['paciente_id']
        if 'analise_id' in self.kwargs:
            analise_id = self.kwargs['analise_id']
        paciente = Paciente.objects.get(usuario_id=paciente_id)
        anamnesia = Anamnesia.objects.filter(id=analise_id)

        criativo=0
        reativo=0
        adaptativo=0
        for analise in anamnesia:
            indiferenciacao = GrauIndiferenciacaoPaciente.objects.filter(anamnesia_id=analise.id)
            for opcao in indiferenciacao:
                resposta = GrauIndiferenciacao.objects.get(id=opcao.resposta_id)
                if resposta.padrao == "adaptativo":
                    adaptativo=adaptativo+1
                if resposta.padrao == "reativo":
                    reativo=reativo+1
                if resposta.padrao == "criativo":
                    criativo=criativo+1

        nascimento=str(paciente.nascimento)
        ano = int(nascimento.split("-")[0])
        mes=int(nascimento.split("-")[1])
        dia=int(nascimento.split("-")[2])
        atual=datetime.now()
        anoAtual=atual.year
        mesAtual=atual.month
        diaAtual=atual.day

        if mes > mesAtual:
            idade = anoAtual-ano-1
        if mes < mesAtual:
            idade = anoAtual-ano
        if mes == mesAtual:
            if dia >= diaAtual:
                idade = anoAtual-ano-1
            if dia < diaAtual:
                idade = anoAtual-ano

        adaptativoMin=0
        adaptativoMax=0
        criativoMin=0
        criativoMax=0
        reativoMin=0
        reativoMax=0

        if idade >=0 and idade <=3:
            adaptativoMin=14
            adaptativoMax=17
            criativoMin=0
            criativoMax=2
            reativoMin=0
            reativoMax=2
        if idade >=4 and idade <=7:
            adaptativoMin=12
            adaptativoMax=17
            criativoMin=0
            criativoMax=3
            reativoMin=2
            reativoMax=6
        if idade >=8 and idade <=12:
            adaptativoMin=8
            adaptativoMax=13
            criativoMin=2
            criativoMax=5
            reativoMin=6
            reativoMax=10
        if idade >=13 and idade <=19:
            adaptativoMin=4
            adaptativoMax=8
            criativoMin=6
            criativoMax=8
            reativoMin=10
            reativoMax=15
        if idade >=20 and idade <=24:
            adaptativoMin=1
            adaptativoMax=3
            criativoMin=9
            criativoMax=11
            reativoMin=8
            reativoMax=12
        if idade >=25 and idade <=32:
            adaptativoMin=0
            adaptativoMax=2
            criativoMin=11
            criativoMax=15
            reativoMin=3
            reativoMax=7
        if idade >=33:
            adaptativoMin=0
            adaptativoMax=2
            criativoMin=16
            criativoMax=19
            reativoMin=0
            reativoMax=2

        tudo_dentro=""
        abaixo_adaptativo=""
        acima_adaptativo=""
        abaixo_criativo=""
        acima_criativo=""
        abaixo_reativo=""
        acima_reativo=""
        texto=""
        if adaptativo>adaptativoMin and adaptativo<adaptativoMax and\
                        reativo>reativoMin and reativo<reativoMax and\
                        criativo>criativoMin and criativo<criativoMax:
            tudo_dentro = Recomendacao.objects.get(nome='tudo_dentro')
            texto= tudo_dentro.texto
        if adaptativo<adaptativoMin:
            abaixo_adaptativo = Recomendacao.objects.get(nome='intervalo_adaptativo',intervalo="abaixo")
            texto=texto+abaixo_adaptativo.texto
        if adaptativo>adaptativoMax:
            acima_adaptativo = Recomendacao.objects.get(nome='intervalo_adaptativo',intervalo="acima")
            texto=texto+acima_adaptativo.texto
        if reativo<reativoMin:
            abaixo_reativo = Recomendacao.objects.get(nome='intervalo_reativo',intervalo="abaixo")
            texto=texto+abaixo_reativo.texto
        if reativo>reativoMax:
            acima_reativo = Recomendacao.objects.get(nome='intervalo_reativo',intervalo="acima")
            texto=texto+acima_reativo.texto
        if criativo<criativoMin:
            abaixo_criativo = Recomendacao.objects.get(nome='intervalo_criativo',intervalo="abaixo")
            texto=texto+abaixo_criativo.texto
        if criativo>criativoMax:
            acima_criativo = Recomendacao.objects.get(nome='intervalo_criativo',intervalo="acima")
            texto=texto+acima_criativo.texto

        return texto

    def textoSeletiva(self):
        if 'paciente_id' in self.kwargs:
            paciente_id = self.kwargs['paciente_id']
        if 'analise_id' in self.kwargs:
            analise_id = self.kwargs['analise_id']
        paciente = Paciente.objects.get(usuario_id=paciente_id)
        anamnesia = Anamnesia.objects.get(id=analise_id)

        nascimento=str(paciente.nascimento)
        ano = int(nascimento.split("-")[0])
        mes=int(nascimento.split("-")[1])
        dia=int(nascimento.split("-")[2])
        atual=datetime.now()
        anoAtual=atual.year
        mesAtual=atual.month
        diaAtual=atual.day

        if mes > mesAtual:
            idade = anoAtual-ano-1
        if mes < mesAtual:
            idade = anoAtual-ano
        if mes == mesAtual:
            if dia >= diaAtual:
                idade = anoAtual-ano-1
            if dia < diaAtual:
                idade = anoAtual-ano

        texto={}
        relacionamento="Não há recomendações"
        diferenciacao="Não há recomendações"
        autonomia="Não há recomendações"
        assertividade="Não há recomendações"
        autoEstima="Não há recomendações"
        somarelacionamento=0
        somadiferenciacao=0
        somaautonomia=0
        somaassertividade=0
        somaautoestima=0

        perguntasrelacionamento=["S34","S35","S36"]
        perguntasdiferenciacao=["S05","S06","S15","S16","S24","S25"]
        perguntasautonomia=["S01","S07","S08","S09","S10","S11","S12","S13","S28"]
        perguntasassertiva=["S14","S18","S20","S21","S30","S31","S32","S33",]
        perguntasautoEstima=["S02","S17","S19","S22","S23","S26","S27","S29"]

        seletiva = Seletiva.objects.filter(paciente_id=paciente.id,anamnesia_id=anamnesia.id)
        for item in seletiva:
            resposta = RespostaSeletiva.objects.get(id=item.resposta_id)
            pergunta = PerguntaSeletiva.objects.get(id=resposta.pergunta_id)

            if pergunta.numero in perguntasrelacionamento:
                nome="relacionamento"
                if idade >=0 and idade <=3:
                    if resposta.nivel0 != 0:
                        somarelacionamento=somarelacionamento+resposta.nivel0
                        if resposta.nivel0 <=1:
                            relacionamento=Recomendacao.objects.get(nome=nome,intervalo="nivel0")
                if idade >=4 and idade <=7:
                    if resposta.nivel1 != 0:
                        somarelacionamento=somarelacionamento+resposta.nivel1
                        if resposta.nivel1 <=1:
                            relacionamento=Recomendacao.objects.get(nome=nome,intervalo="nivel1")
                            relacionamento=relacionamento.texto
                if idade >=8 and idade <=12:
                    if resposta.nivel2 != 0:
                        somarelacionamento=somarelacionamento+resposta.nivel2
                        if resposta.nivel2 <=1:
                            relacionamento=Recomendacao.objects.get(nome=nome,intervalo="nivel2")
                            relacionamento=relacionamento.texto
                if idade >=13 and idade <=19:
                    if resposta.nivel3 != 0:
                        somarelacionamento=somarelacionamento+resposta.nivel3
                        if resposta.nivel3 <=1:
                            relacionamento=Recomendacao.objects.get(nome=nome,intervalo="nivel3")
                            relacionamento=relacionamento.texto
                if idade >=20 and idade <=24:
                    if resposta.nivel4 != 0:
                        somarelacionamento=somarelacionamento+resposta.nivel4
                        if resposta.nivel4 <=1:
                            relacionamento=Recomendacao.objects.get(nome=nome,intervalo="nivel4")
                            relacionamento=relacionamento.texto
                if idade >=25 and idade <=32:
                    if resposta.nivel5 != 0:
                        somarelacionamento=somarelacionamento+resposta.nivel5
                        if resposta.nivel5 <=1:
                            relacionamento=Recomendacao.objects.get(nome=nome,intervalo="nivel5")
                            relacionamento=relacionamento.texto
                if idade >=33:
                    if resposta.nivel6 != 0:
                        somarelacionamento=somarelacionamento+resposta.nivel6
                        if resposta.nivel6 <=1:
                            relacionamento=Recomendacao.objects.get(nome=nome,intervalo="nivel6")
                            relacionamento=relacionamento.texto

            if pergunta.numero in perguntasdiferenciacao:
                nome="diferenciacao"
                if idade >=0 and idade <=3:
                    if resposta.nivel0 != 0:
                        somadiferenciacao=somadiferenciacao+resposta.nivel0
                        if resposta.nivel0 <=1:
                            diferenciacao=Recomendacao.objects.get(nome=nome,intervalo="nivel0")
                if idade >=4 and idade <=7:
                    if resposta.nivel1 != 0:
                        somadiferenciacao=somadiferenciacao+resposta.nivel1
                        if resposta.nivel1 <=1:
                            diferenciacao=Recomendacao.objects.get(nome=nome,intervalo="nivel1")
                            diferenciacao=diferenciacao.texto
                if idade >=8 and idade <=12:
                    if resposta.nivel2 != 0:
                        somadiferenciacao=somadiferenciacao+resposta.nivel2
                        if resposta.nivel2 <=1:
                            diferenciacao=Recomendacao.objects.get(nome=nome,intervalo="nivel2")
                            diferenciacao=diferenciacao.texto
                if idade >=13 and idade <=19:
                    if resposta.nivel3 != 0:
                        somadiferenciacao=somadiferenciacao+resposta.nivel3
                        if resposta.nivel3 <=1:
                            diferenciacao=Recomendacao.objects.get(nome=nome,intervalo="nivel3")
                            diferenciacao=diferenciacao.texto
                if idade >=20 and idade <=24:
                    if resposta.nivel4 != 0:
                        somadiferenciacao=somadiferenciacao+resposta.nivel4
                        if resposta.nivel4 <=1:
                            diferenciacao=Recomendacao.objects.get(nome=nome,intervalo="nivel4")
                            diferenciacao=diferenciacao.texto
                if idade >=25 and idade <=32:
                    if resposta.nivel5 != 0:
                        somadiferenciacao=somadiferenciacao+resposta.nivel5
                        if resposta.nivel5 <=1:
                            diferenciacao=Recomendacao.objects.get(nome=nome,intervalo="nivel5")
                            diferenciacao=diferenciacao.texto
                if idade >=33:
                    if resposta.nivel6 != 0:
                        somadiferenciacao=somadiferenciacao+resposta.nivel6
                        if resposta.nivel6 <=1:
                            diferenciacao=Recomendacao.objects.get(nome=nome,intervalo="nivel6")
                            diferenciacao=diferenciacao.texto

            if pergunta.numero in perguntasautonomia:
                nome="autonomia"
                if idade >=0 and idade <=3:
                    if resposta.nivel0 != 0:
                        somaautonomia=somaautonomia+resposta.nivel0
                        if resposta.nivel0 <=1:
                            autonomia=Recomendacao.objects.get(nome=nome,intervalo="nivel0")
                if idade >=4 and idade <=7:
                    if resposta.nivel1 != 0:
                        somaautonomia=somaautonomia+resposta.nivel1
                        if resposta.nivel1 <=1:
                            autonomia=Recomendacao.objects.get(nome=nome,intervalo="nivel1")
                            autonomia=autonomia.texto
                if idade >=8 and idade <=12:
                    if resposta.nivel2 != 0:
                        somaautonomia=somaautonomia+resposta.nivel2
                        if resposta.nivel2 <=1:
                            autonomia=Recomendacao.objects.get(nome=nome,intervalo="nivel2")
                            autonomia=autonomia.texto
                if idade >=13 and idade <=19:
                    if resposta.nivel3 != 0:
                        somaautonomia=somaautonomia+resposta.nivel3
                        if resposta.nivel3 <=1:
                            autonomia=Recomendacao.objects.get(nome=nome,intervalo="nivel3")
                            autonomia=autonomia.texto
                if idade >=20 and idade <=24:
                    if resposta.nivel4 != 0:
                        somaautonomia=somaautonomia+resposta.nivel4
                        if resposta.nivel4 <=1:
                            autonomia=Recomendacao.objects.get(nome=nome,intervalo="nivel4")
                            autonomia=autonomia.texto
                if idade >=25 and idade <=32:
                    if resposta.nivel5 != 0:
                        somaautonomia=somaautonomia+resposta.nivel5
                        if resposta.nivel5 <=1:
                            autonomia=Recomendacao.objects.get(nome=nome,intervalo="nivel5")
                            autonomia=autonomia.texto
                if idade >=33:
                    if resposta.nivel6 != 0:
                        somaautonomia=somaautonomia+resposta.nivel6
                        if resposta.nivel6 <=1:
                            autonomia=Recomendacao.objects.get(nome=nome,intervalo="nivel6")
                            autonomia=autonomia.texto

            if pergunta.numero in perguntasassertiva:
                nome="assertividade"
                if idade >=0 and idade <=3:
                    if resposta.nivel0 != 0:
                        somaassertividade=somaassertividade+resposta.nivel0
                        if resposta.nivel0 <=1:
                            assertividade=Recomendacao.objects.get(nome=nome,intervalo="nivel0")
                if idade >=4 and idade <=7:
                    if resposta.nivel1 != 0:
                        somaassertividade=somaassertividade+resposta.nivel1
                        if resposta.nivel1 <=1:
                            assertividade=Recomendacao.objects.get(nome=nome,intervalo="nivel1")
                            assertividade=assertividade.texto
                if idade >=8 and idade <=12:
                    if resposta.nivel2 != 0:
                        somaassertividade=somaassertividade+resposta.nivel2
                        if resposta.nivel2 <=1:
                            assertividade=Recomendacao.objects.get(nome=nome,intervalo="nivel2")
                            assertividade=assertividade.texto
                if idade >=13 and idade <=19:
                    if resposta.nivel3 != 0:
                        somaassertividade=somaassertividade+resposta.nivel3
                        if resposta.nivel3 <=1:
                            assertividade=Recomendacao.objects.get(nome=nome,intervalo="nivel3")
                            assertividade=assertividade.texto
                if idade >=20 and idade <=24:
                    if resposta.nivel4 != 0:
                        somaassertividade=somaassertividade+resposta.nivel4
                        if resposta.nivel4 <=1:
                            assertividade=Recomendacao.objects.get(nome=nome,intervalo="nivel4")
                            assertividade=assertividade.texto
                if idade >=25 and idade <=32:
                    if resposta.nivel5 != 0:
                        somaassertividade=somaassertividade+resposta.nivel5
                        if resposta.nivel5 <=1:
                            assertividade=Recomendacao.objects.get(nome=nome,intervalo="nivel5")
                            assertividade=assertividade.texto
                if idade >=33:
                    if resposta.nivel6 != 0:
                        somaassertividade=somaassertividade+resposta.nivel6
                        if resposta.nivel6 <=1:
                            assertividade=Recomendacao.objects.get(nome=nome,intervalo="nivel6")
                            assertividade=assertividade.texto

            if pergunta.numero in perguntasautoEstima:
                nome="autoestima"
                if idade >=0 and idade <=3:
                    if resposta.nivel0 != 0:
                        somaautoestima=somaautoestima+resposta.nivel0
                        if resposta.nivel0 <=1:
                            autoEstima=Recomendacao.objects.get(nome=nome,intervalo="nivel0")
                if idade >=4 and idade <=7:
                    if resposta.nivel1 != 0:
                        somaautoestima=somaautoestima+resposta.nivel1
                        if resposta.nivel1 <=1:
                            autoEstima=Recomendacao.objects.get(nome=nome,intervalo="nivel1")
                            autoEstima=autoEstima.texto
                if idade >=8 and idade <=12:
                    if resposta.nivel2 != 0:
                        somaautoestima=somaautoestima+resposta.nivel2
                        if resposta.nivel2 <=1:
                            autoEstima=Recomendacao.objects.get(nome=nome,intervalo="nivel2")
                            autoEstima=autoEstima.texto
                if idade >=13 and idade <=19:
                    if resposta.nivel3 != 0:
                        somaautoestima=somaautoestima+resposta.nivel3
                        if resposta.nivel3 <=1:
                            autoEstima=Recomendacao.objects.get(nome=nome,intervalo="nivel3")
                            autoEstima=autoEstima.texto
                if idade >=20 and idade <=24:
                    if resposta.nivel4 != 0:
                        somaautoestima=somaautoestima+resposta.nivel4
                        if resposta.nivel4 <=1:
                            autoEstima=Recomendacao.objects.get(nome=nome,intervalo="nivel4")
                            autoEstima=autoEstima.texto
                if idade >=25 and idade <=32:
                    if resposta.nivel5 != 0:
                        somaautoestima=somaautoestima+resposta.nivel5
                        if resposta.nivel5 <=1:
                            autoEstima=Recomendacao.objects.get(nome=nome,intervalo="nivel5")
                            autoEstima=autoEstima.texto
                if idade >=33:
                    if resposta.nivel6 != 0:
                        somaautoestima=somaautoestima+resposta.nivel6
                        if resposta.nivel6 <=1:
                            autoEstima=Recomendacao.objects.get(nome=nome,intervalo="nivel6")
                            autoEstima=autoEstima.texto

        if somarelacionamento/len(perguntasrelacionamento) < 3:
            nome="relacionamento"
            if idade >=0 and idade <=3:
                relacionamento= Recomendacao.objects.get(nome=nome, intervalo="nivel0")
            if idade >=4 and idade <=7:
                relacionamento= Recomendacao.objects.get(nome=nome, intervalo="nivel1")
            if idade >=8 and idade <=12:
                relacionamento= Recomendacao.objects.get(nome=nome, intervalo="nivel2")
            if idade >=13 and idade <=19:
                relacionamento= Recomendacao.objects.get(nome=nome, intervalo="nivel3")
            if idade >=20 and idade <=24:
                relacionamento= Recomendacao.objects.get(nome=nome, intervalo="nivel4")
            if idade >=25 and idade <=32:
                relacionamento= Recomendacao.objects.get(nome=nome, intervalo="nivel5")
            if idade >=33:
                relacionamento= Recomendacao.objects.get(nome=nome, intervalo="nivel6")
            relacionamento=relacionamento.texto

        if somadiferenciacao/len(perguntasdiferenciacao) < 3:
            nome="diferenciacao"
            if idade >=0 and idade <=3:
                diferenciacao= Recomendacao.objects.get(nome=nome, intervalo="nivel0")
            if idade >=4 and idade <=7:
                diferenciacao= Recomendacao.objects.get(nome=nome, intervalo="nivel1")
            if idade >=8 and idade <=12:
                diferenciacao= Recomendacao.objects.get(nome=nome, intervalo="nivel2")
            if idade >=13 and idade <=19:
                diferenciacao= Recomendacao.objects.get(nome=nome, intervalo="nivel3")
            if idade >=20 and idade <=24:
                diferenciacao= Recomendacao.objects.get(nome=nome, intervalo="nivel4")
            if idade >=25 and idade <=32:
                diferenciacao= Recomendacao.objects.get(nome=nome, intervalo="nivel5")
            if idade >=33:
                diferenciacao= Recomendacao.objects.get(nome=nome, intervalo="nivel6")
            diferenciacao=diferenciacao.texto

        if somaautonomia/len(perguntasautonomia) < 3:
            nome="autonomia"
            if idade >=0 and idade <=3:
                autonomia= Recomendacao.objects.get(nome=nome, intervalo="nivel0")
            if idade >=4 and idade <=7:
                autonomia= Recomendacao.objects.get(nome=nome, intervalo="nivel1")
            if idade >=8 and idade <=12:
                autonomia= Recomendacao.objects.get(nome=nome, intervalo="nivel2")
            if idade >=13 and idade <=19:
                autonomia= Recomendacao.objects.get(nome=nome, intervalo="nivel3")
            if idade >=20 and idade <=24:
                autonomia= Recomendacao.objects.get(nome=nome, intervalo="nivel4")
            if idade >=25 and idade <=32:
                autonomia= Recomendacao.objects.get(nome=nome, intervalo="nivel5")
            if idade >=33:
                autonomia= Recomendacao.objects.get(nome=nome, intervalo="nivel6")
            autonomia=autonomia.texto

        if somaassertividade/len(perguntasassertiva) < 3:
            nome="assertividade"
            if idade >=0 and idade <=3:
                assertividade= Recomendacao.objects.get(nome=nome, intervalo="nivel0")
            if idade >=4 and idade <=7:
                assertividade= Recomendacao.objects.get(nome=nome, intervalo="nivel1")
            if idade >=8 and idade <=12:
                assertividade= Recomendacao.objects.get(nome=nome, intervalo="nivel2")
            if idade >=13 and idade <=19:
                assertividade= Recomendacao.objects.get(nome=nome, intervalo="nivel3")
            if idade >=20 and idade <=24:
                assertividade= Recomendacao.objects.get(nome=nome, intervalo="nivel4")
            if idade >=25 and idade <=32:
                assertividade= Recomendacao.objects.get(nome=nome, intervalo="nivel5")
            if idade >=33:
                assertividade= Recomendacao.objects.get(nome=nome, intervalo="nivel6")
            assertividade=assertividade.texto

        if somaautoestima/len(perguntasautoEstima) < 3:
            nome="autoestima"
            if idade >=0 and idade <=3:
                autoEstima= Recomendacao.objects.get(nome=nome, intervalo="nivel0")
            if idade >=4 and idade <=7:
                autoEstima= Recomendacao.objects.get(nome=nome, intervalo="nivel1")
            if idade >=8 and idade <=12:
                autoEstima= Recomendacao.objects.get(nome=nome, intervalo="nivel2")
            if idade >=13 and idade <=19:
                autoEstima= Recomendacao.objects.get(nome=nome, intervalo="nivel3")
            if idade >=20 and idade <=24:
                autoEstima= Recomendacao.objects.get(nome=nome, intervalo="nivel4")
            if idade >=25 and idade <=32:
                autoEstima= Recomendacao.objects.get(nome=nome, intervalo="nivel5")
            if idade >=33:
                autoEstima= Recomendacao.objects.get(nome=nome, intervalo="nivel6")
            autoEstima=autoEstima.texto

        texto["Relacionamento"]=relacionamento
        texto["Diferenciação"]=diferenciacao
        texto["Autonomia"]=autonomia
        texto["Assertividade"]=assertividade
        texto["Autoestima"]=autoEstima
        return texto

    def seletiva(self):
        if 'analise_id' in self.kwargs:
            analise_id = self.kwargs['analise_id']
        seletiva = Seletiva.objects.filter(anamnesia_id=analise_id)

        return seletiva


    def tarefaAreaAfetiva(self):
        texto={}
        if 'paciente_id' in self.kwargs:
            paciente_id = self.kwargs['paciente_id']
        if 'analise_id' in self.kwargs:
            analise_id = self.kwargs['analise_id']
        paciente= Paciente.objects.get(usuario_id=paciente_id)
        anamnesia = Anamnesia.objects.filter(paciente_id=paciente.id)
        for analise in anamnesia:
            area= AreaAfetiva.objects.filter(anamnesia_id=analise.id).order_by('resposta_id')
            A=[0]
            for respostas in area:
                resposta = RespostaAreaAfetiva.objects.get(id=respostas.resposta_id)
                A.append(resposta.valor)
            afetivoRelacional=((A[1]+A[2]+A[4]+A[6]+A[9]+A[13]+A[15]+A[17]+A[19]+A[20]+A[21]+A[22]+A[23]+A[25]+A[28])/15)
            produtividade=((A[5]+A[16]+A[20]+A[22]+A[23])/5)
            organico=((A[7]+A[12]+A[14]+A[27]+A[29])/5)
            espiritual=((A[3]+A[11]+A[18]+A[24]+A[26])/5)
            socioCultural=((A[8]+A[10]+A[20]+A[22]+A[23])/5)

        if afetivoRelacional >=1.5 and afetivoRelacional < 3:
            texto["afetivo"]="AreaAfetiva_Afetivo Relacional_1.5-3"
        if afetivoRelacional >= 0 and afetivoRelacional < 1.5:
            texto["afetivo"]="AreaAfetiva_Afetivo Relacional_0-1.5"
        if produtividade >=0 and produtividade < 1.5:
            texto["produtividade"]="AreaAfetiva_Produtividade"
        if organico >=0 and organico < 1.5:
            texto["organico"]="AreaAfetiva_Organico"
        if espiritual >=0 and espiritual < 1.5:
            texto["espiritual"]="AreaAfetiva_Espiritual"
        if socioCultural >=0 and socioCultural < 1.5:
            texto["sociocultural"]="AreaAfetiva_SocioCultural"
        return texto

    def tarefaIndiferenciacao(self):
        texto={}
        if 'paciente_id' in self.kwargs:
            paciente_id = self.kwargs['paciente_id']
        if 'analise_id' in self.kwargs:
            analise_id = self.kwargs['analise_id']
        paciente= Paciente.objects.get(usuario_id=paciente_id)
        anamnesia = Anamnesia.objects.filter(id=analise_id)

        criativo=0
        reativo=0
        adaptativo=0
        for analise in anamnesia:
            indiferenciacao = GrauIndiferenciacaoPaciente.objects.filter(anamnesia_id=analise.id)
            for opcao in indiferenciacao:
                resposta = GrauIndiferenciacao.objects.get(id=opcao.resposta_id)
                if resposta.padrao == "adaptativo":
                    adaptativo=adaptativo+1
                if resposta.padrao == "reativo":
                    reativo=reativo+1
                if resposta.padrao == "criativo":
                    criativo=criativo+1

        nascimento=str(paciente.nascimento)
        ano = int(nascimento.split("-")[0])
        mes=int(nascimento.split("-")[1])
        dia=int(nascimento.split("-")[2])
        atual=datetime.now()
        anoAtual=atual.year
        mesAtual=atual.month
        diaAtual=atual.day

        if mes > mesAtual:
            idade = anoAtual-ano-1
        if mes < mesAtual:
            idade = anoAtual-ano
        if mes == mesAtual:
            if dia >= diaAtual:
                idade = anoAtual-ano-1
            if dia < diaAtual:
                idade = anoAtual-ano

        adaptativoMin=0
        adaptativoMax=0
        criativoMin=0
        criativoMax=0
        reativoMin=0
        reativoMax=0

        if idade >=0 and idade <=3:
            adaptativoMin=14
            adaptativoMax=17
            criativoMin=0
            criativoMax=2
            reativoMin=0
            reativoMax=2
        if idade >=4 and idade <=7:
            adaptativoMin=12
            adaptativoMax=17
            criativoMin=0
            criativoMax=3
            reativoMin=2
            reativoMax=6
        if idade >=8 and idade <=12:
            adaptativoMin=8
            adaptativoMax=13
            criativoMin=2
            criativoMax=5
            reativoMin=6
            reativoMax=10
        if idade >=13 and idade <=19:
            adaptativoMin=4
            adaptativoMax=8
            criativoMin=6
            criativoMax=8
            reativoMin=10
            reativoMax=15
        if idade >=20 and idade <=24:
            adaptativoMin=1
            adaptativoMax=3
            criativoMin=9
            criativoMax=11
            reativoMin=8
            reativoMax=12
        if idade >=25 and idade <=32:
            adaptativoMin=0
            adaptativoMax=2
            criativoMin=11
            criativoMax=15
            reativoMin=3
            reativoMax=7
        if idade >=33:
            adaptativoMin=0
            adaptativoMax=2
            criativoMin=16
            criativoMax=19
            reativoMin=0
            reativoMax=2

        if adaptativo<adaptativoMin or adaptativo>adaptativoMax and\
                        reativo<reativoMin or reativo>reativoMax and\
                        criativo<criativoMin or criativo>criativoMax:
            texto["geral"]= "Padrao de Funcionamento Mental Geral"
        if adaptativo<adaptativoMin or adaptativo>adaptativoMax:
            texto["adaptativo"] = "Padrao de Funcionamento Mental Adaptativo"
        if reativo<reativoMin or reativo>reativoMax:
            texto["reativo"] = "Padrao de Funcionamento Mental Reativo"
        if criativo<criativoMin or criativo>criativoMax:
            texto["criativo"] = "Padrao de Funcionamento Mental Criativo"

        return texto

    def tarefaRelacionamento(self):
        if 'paciente_id' in self.kwargs:
            paciente_id = self.kwargs['paciente_id']
        if 'analise_id' in self.kwargs:
            analise_id = self.kwargs['analise_id']
        paciente= Paciente.objects.get(usuario_id=paciente_id)
        anamnesia = Anamnesia.objects.get(id=analise_id)

        nascimento=str(paciente.nascimento)
        ano = int(nascimento.split("-")[0])
        mes=int(nascimento.split("-")[1])
        dia=int(nascimento.split("-")[2])
        atual=datetime.now()
        anoAtual=atual.year
        mesAtual=atual.month
        diaAtual=atual.day

        if mes > mesAtual:
            idade = anoAtual-ano-1
        if mes < mesAtual:
            idade = anoAtual-ano
        if mes == mesAtual:
            if dia >= diaAtual:
                idade = anoAtual-ano-1
            if dia < diaAtual:
                idade = anoAtual-ano

        somarelacionamento=0

        perguntasrelacionamento=["S34","S35","S36"]

        texto=""
        seletiva = Seletiva.objects.filter(paciente_id=paciente.id,anamnesia_id=anamnesia.id)
        for item in seletiva:
            resposta = RespostaSeletiva.objects.get(id=item.resposta_id)
            pergunta = PerguntaSeletiva.objects.get(id=resposta.pergunta_id)

            if pergunta.numero in perguntasrelacionamento:
                if idade >=0 and idade <=3:
                    if resposta.nivel0 != 0:
                        somarelacionamento=somarelacionamento+resposta.nivel0
                        if resposta.nivel0 <=1:
                            texto="pdfrelacionamento"
                if idade >=4 and idade <=7:
                    if resposta.nivel1 != 0:
                        somarelacionamento=somarelacionamento+resposta.nivel1
                        if resposta.nivel1 <=1:
                            texto="pdfrelacionamento"
                if idade >=8 and idade <=12:
                    if resposta.nivel2 != 0:
                        somarelacionamento=somarelacionamento+resposta.nivel2
                        if resposta.nivel2 <=1:
                            texto="pdfrelacionamento"
                if idade >=13 and idade <=19:
                    if resposta.nivel3 != 0:
                        somarelacionamento=somarelacionamento+resposta.nivel3
                        if resposta.nivel3 <=1:
                            texto="pdfrelacionamento"
                if idade >=20 and idade <=24:
                    if resposta.nivel4 != 0:
                        somarelacionamento=somarelacionamento+resposta.nivel4
                        if resposta.nivel4 <=1:
                            texto="pdfrelacionamento"
                if idade >=25 and idade <=32:
                    if resposta.nivel5 != 0:
                        somarelacionamento=somarelacionamento+resposta.nivel5
                        if resposta.nivel5 <=1:
                            texto="pdfrelacionamento"
                if idade >=33:
                    if resposta.nivel6 != 0:
                        somarelacionamento=somarelacionamento+resposta.nivel6
                        if resposta.nivel6 <=1:
                            texto="pdfrelacionamento"

        if somarelacionamento/len(perguntasrelacionamento) < 3:
            texto="pdfrelacionamento"

        return texto

    def tarefaDiferenciacao(self):
        texto=""
        if 'paciente_id' in self.kwargs:
            paciente_id = self.kwargs['paciente_id']
        if 'analise_id' in self.kwargs:
            analise_id = self.kwargs['analise_id']
        paciente= Paciente.objects.get(usuario_id=paciente_id)
        anamnesia = Anamnesia.objects.get(id=analise_id)

        nascimento=str(paciente.nascimento)
        ano = int(nascimento.split("-")[0])
        mes=int(nascimento.split("-")[1])
        dia=int(nascimento.split("-")[2])
        atual=datetime.now()
        anoAtual=atual.year
        mesAtual=atual.month
        diaAtual=atual.day

        if mes > mesAtual:
            idade = anoAtual-ano-1
        if mes < mesAtual:
            idade = anoAtual-ano
        if mes == mesAtual:
            if dia >= diaAtual:
                idade = anoAtual-ano-1
            if dia < diaAtual:
                idade = anoAtual-ano

        somadiferenciacao=0
        perguntasdiferenciacao=["S05","S06","S15","S16","S24","S25"]
        seletiva = Seletiva.objects.filter(paciente_id=paciente.id,anamnesia_id=anamnesia.id)
        for item in seletiva:
            resposta = RespostaSeletiva.objects.get(id=item.resposta_id)
            pergunta = PerguntaSeletiva.objects.get(id=resposta.pergunta_id)

            if pergunta.numero in perguntasdiferenciacao:
                if idade >=0 and idade <=3:
                    if resposta.nivel0 != 0:
                        somadiferenciacao=somadiferenciacao+resposta.nivel0
                        if resposta.nivel0 <=1:
                            texto="pdfdiferenciacao"
                if idade >=4 and idade <=7:
                    if resposta.nivel1 != 0:
                        somadiferenciacao=somadiferenciacao+resposta.nivel1
                        if resposta.nivel1 <=1:
                            texto="pdfdiferenciacao"
                if idade >=8 and idade <=12:
                    if resposta.nivel2 != 0:
                        somadiferenciacao=somadiferenciacao+resposta.nivel2
                        if resposta.nivel2 <=1:
                            texto="pdfdiferenciacao"
                if idade >=13 and idade <=19:
                    if resposta.nivel3 != 0:
                        somadiferenciacao=somadiferenciacao+resposta.nivel3
                        if resposta.nivel3 <=1:
                            texto="pdfdiferenciacao"
                if idade >=20 and idade <=24:
                    if resposta.nivel4 != 0:
                        somadiferenciacao=somadiferenciacao+resposta.nivel4
                        if resposta.nivel4 <=1:
                            texto="pdfdiferenciacao"
                if idade >=25 and idade <=32:
                    if resposta.nivel5 != 0:
                        somadiferenciacao=somadiferenciacao+resposta.nivel5
                        if resposta.nivel5 <=1:
                            texto="pdfdiferenciacao"
                if idade >=33:
                    if resposta.nivel6 != 0:
                        somadiferenciacao=somadiferenciacao+resposta.nivel6
                        if resposta.nivel6 <=1:
                            texto="pdfdiferenciacao"
        if somadiferenciacao/len(perguntasdiferenciacao) < 3:
            texto="pdfdiferenciacao"

        return texto

    def tarefaAutonomia(self):
        texto=""
        if 'paciente_id' in self.kwargs:
            paciente_id = self.kwargs['paciente_id']
        if 'analise_id' in self.kwargs:
            analise_id = self.kwargs['analise_id']
        paciente= Paciente.objects.get(usuario_id=paciente_id)
        anamnesia = Anamnesia.objects.get(id=analise_id)

        nascimento=str(paciente.nascimento)
        ano = int(nascimento.split("-")[0])
        mes=int(nascimento.split("-")[1])
        dia=int(nascimento.split("-")[2])
        atual=datetime.now()
        anoAtual=atual.year
        mesAtual=atual.month
        diaAtual=atual.day

        if mes > mesAtual:
            idade = anoAtual-ano-1
        if mes < mesAtual:
            idade = anoAtual-ano
        if mes == mesAtual:
            if dia >= diaAtual:
                idade = anoAtual-ano-1
            if dia < diaAtual:
                idade = anoAtual-ano

        somaautonomia=0
        perguntasautonomia=["S01","S07","S08","S09","S10","S11","S12","S13","S28"]

        seletiva = Seletiva.objects.filter(paciente_id=paciente.id,anamnesia_id=anamnesia.id)
        for item in seletiva:
            resposta = RespostaSeletiva.objects.get(id=item.resposta_id)
            pergunta = PerguntaSeletiva.objects.get(id=resposta.pergunta_id)

            if pergunta.numero in perguntasautonomia:
                if idade >=0 and idade <=3:
                    if resposta.nivel0 != 0:
                        somaautonomia=somaautonomia+resposta.nivel0
                        if resposta.nivel0 <=1:
                            texto="pdfautonomia"
                if idade >=4 and idade <=7:
                    if resposta.nivel1 != 0:
                        somaautonomia=somaautonomia+resposta.nivel1
                        if resposta.nivel1 <=1:
                            texto="pdfautonomia"
                if idade >=8 and idade <=12:
                    if resposta.nivel2 != 0:
                        somaautonomia=somaautonomia+resposta.nivel2
                        if resposta.nivel2 <=1:
                            texto="pdfautonomia"
                if idade >=13 and idade <=19:
                    if resposta.nivel3 != 0:
                        somaautonomia=somaautonomia+resposta.nivel3
                        if resposta.nivel3 <=1:
                            texto="pdfautonomia"
                if idade >=20 and idade <=24:
                    if resposta.nivel4 != 0:
                        somaautonomia=somaautonomia+resposta.nivel4
                        if resposta.nivel4 <=1:
                            texto="pdfautonomia"
                if idade >=25 and idade <=32:
                    if resposta.nivel5 != 0:
                        somaautonomia=somaautonomia+resposta.nivel5
                        if resposta.nivel5 <=1:
                            texto="pdfautonomia"
                if idade >=33:
                    if resposta.nivel6 != 0:
                        somaautonomia=somaautonomia+resposta.nivel6
                        if resposta.nivel6 <=1:
                            texto="pdfautonomia"

        if somaautonomia/len(perguntasautonomia) < 3:
            texto="pdfautonomia"

        return texto

    def tarefaAssertividade(self):
        texto=""
        if 'paciente_id' in self.kwargs:
            paciente_id = self.kwargs['paciente_id']
        if 'analise_id' in self.kwargs:
            analise_id = self.kwargs['analise_id']
        paciente= Paciente.objects.get(usuario_id=paciente_id)
        anamnesia = Anamnesia.objects.get(id=analise_id)

        nascimento=str(paciente.nascimento)
        ano = int(nascimento.split("-")[0])
        mes=int(nascimento.split("-")[1])
        dia=int(nascimento.split("-")[2])
        atual=datetime.now()
        anoAtual=atual.year
        mesAtual=atual.month
        diaAtual=atual.day

        if mes > mesAtual:
            idade = anoAtual-ano-1
        if mes < mesAtual:
            idade = anoAtual-ano
        if mes == mesAtual:
            if dia >= diaAtual:
                idade = anoAtual-ano-1
            if dia < diaAtual:
                idade = anoAtual-ano

        somaassertividade=0
        perguntasassertiva=["S14","S18","S20","S21","S30","S31","S32","S33",]


        seletiva = Seletiva.objects.filter(paciente_id=paciente.id,anamnesia_id=anamnesia.id)
        for item in seletiva:
            resposta = RespostaSeletiva.objects.get(id=item.resposta_id)
            pergunta = PerguntaSeletiva.objects.get(id=resposta.pergunta_id)

            if pergunta.numero in perguntasassertiva:
                if idade >=0 and idade <=3:
                    if resposta.nivel0 != 0:
                        somaassertividade=somaassertividade+resposta.nivel0
                        if resposta.nivel0 <=1:
                            texto="pdfassertividade"
                if idade >=4 and idade <=7:
                    if resposta.nivel1 != 0:
                        somaassertividade=somaassertividade+resposta.nivel1
                        if resposta.nivel1 <=1:
                            texto="pdfassertividade"
                if idade >=8 and idade <=12:
                    if resposta.nivel2 != 0:
                        somaassertividade=somaassertividade+resposta.nivel2
                        if resposta.nivel2 <=1:
                            texto="pdfassertividade"
                if idade >=13 and idade <=19:
                    if resposta.nivel3 != 0:
                        somaassertividade=somaassertividade+resposta.nivel3
                        if resposta.nivel3 <=1:
                            texto="pdfassertividade"
                if idade >=20 and idade <=24:
                    if resposta.nivel4 != 0:
                        somaassertividade=somaassertividade+resposta.nivel4
                        if resposta.nivel4 <=1:
                            texto="pdfassertividade"
                if idade >=25 and idade <=32:
                    if resposta.nivel5 != 0:
                        somaassertividade=somaassertividade+resposta.nivel5
                        if resposta.nivel5 <=1:
                            texto="pdfassertividade"
                if idade >=33:
                    if resposta.nivel6 != 0:
                        somaassertividade=somaassertividade+resposta.nivel6
                        if resposta.nivel6 <=1:
                            texto="pdfassertividade"
        if somaassertividade/len(perguntasassertiva) < 3:
            texto="pdfassertividade"

        return texto

    def tarefaAutoestima(self):
        texto=""
        if 'paciente_id' in self.kwargs:
            paciente_id = self.kwargs['paciente_id']
        if 'analise_id' in self.kwargs:
            analise_id = self.kwargs['analise_id']
        paciente= Paciente.objects.get(usuario_id=paciente_id)
        anamnesia = Anamnesia.objects.get(id=analise_id)

        nascimento=str(paciente.nascimento)
        ano = int(nascimento.split("-")[0])
        mes=int(nascimento.split("-")[1])
        dia=int(nascimento.split("-")[2])
        atual=datetime.now()
        anoAtual=atual.year
        mesAtual=atual.month
        diaAtual=atual.day

        if mes > mesAtual:
            idade = anoAtual-ano-1
        if mes < mesAtual:
            idade = anoAtual-ano
        if mes == mesAtual:
            if dia >= diaAtual:
                idade = anoAtual-ano-1
            if dia < diaAtual:
                idade = anoAtual-ano

        somaautoestima=0
        perguntasautoEstima=["S02","S17","S19","S22","S23","S26","S27","S29"]

        seletiva = Seletiva.objects.filter(paciente_id=paciente.id,anamnesia_id=anamnesia.id)
        for item in seletiva:
            resposta = RespostaSeletiva.objects.get(id=item.resposta_id)
            pergunta = PerguntaSeletiva.objects.get(id=resposta.pergunta_id)
            if pergunta.numero in perguntasautoEstima:
                if idade >=0 and idade <=3:
                    if resposta.nivel0 != 0:
                        somaautoestima=somaautoestima+resposta.nivel0
                        if resposta.nivel0 <=1:
                            texto="pdfautoestima"
                if idade >=4 and idade <=7:
                    if resposta.nivel1 != 0:
                        somaautoestima=somaautoestima+resposta.nivel1
                        if resposta.nivel1 <=1:
                            texto="pdfautoestima"
                if idade >=8 and idade <=12:
                    if resposta.nivel2 != 0:
                        somaautoestima=somaautoestima+resposta.nivel2
                        if resposta.nivel2 <=1:
                            texto="pdfautoestima"
                if idade >=13 and idade <=19:
                    if resposta.nivel3 != 0:
                        somaautoestima=somaautoestima+resposta.nivel3
                        if resposta.nivel3 <=1:
                            texto="pdfautoestima"
                if idade >=20 and idade <=24:
                    if resposta.nivel4 != 0:
                        somaautoestima=somaautoestima+resposta.nivel4
                        if resposta.nivel4 <=1:
                            texto="pdfautoestima"
                if idade >=25 and idade <=32:
                    if resposta.nivel5 != 0:
                        somaautoestima=somaautoestima+resposta.nivel5
                        if resposta.nivel5 <=1:
                            autoEstima=Recomendacao.objects.get(nome=nome,intervalo="nivel5")
                            texto="pdfautoestima"
                if idade >=33:
                    if resposta.nivel6 != 0:
                        somaautoestima=somaautoestima+resposta.nivel6
                        if resposta.nivel6 <=1:
                            texto="pdfautoestima"

        if somaautoestima/len(perguntasautoEstima) < 3:
            texto="pdfautoestima"

        return texto

class RecomendacaoAreaAfetiva(TemplateView):

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(RecomendacaoAreaAfetiva, self).dispatch(*args, **kwargs)

    def anamnesia(self):
        if 'paciente_id' in self.kwargs:
            paciente_id = self.kwargs['paciente_id']
        paciente = Paciente.objects.get(usuario_id=paciente_id)
        if 'analise_id' in self.kwargs:
            analise_id = self.kwargs['analise_id']
        anamnesia = Anamnesia.objects.get(id=analise_id)
        return anamnesia

    def grafico(self):
        if 'paciente_id' in self.kwargs:
            paciente_id = self.kwargs['paciente_id']
        if 'analise_id' in self.kwargs:
            analise_id = self.kwargs['analise_id']
        paciente = Paciente.objects.get(usuario_id=paciente_id)
        dados = {
        }
        anamnesia = Anamnesia.objects.filter(id=analise_id)
        for analise in anamnesia:
            area= AreaAfetiva.objects.filter(anamnesia_id=analise.id).order_by('resposta_id')
            A=[0]
            for respostas in area:
                resposta = RespostaAreaAfetiva.objects.get(id=respostas.resposta_id)
                A.append(resposta.valor)
            afetivoRelacional=((A[1]+A[2]+A[4]+A[6]+A[9]+A[13]+A[15]+A[17]+A[19]+A[20]+A[21]+A[22]+A[23]+A[25]+A[28])/15)
            produtividade=((A[5]+A[16]+A[20]+A[22]+A[23])/5)
            organico=((A[7]+A[12]+A[14]+A[27]+A[29])/5)
            espiritual=((A[3]+A[11]+A[18]+A[24]+A[26])/5)
            socioCultural=((A[8]+A[10]+A[20]+A[22]+A[23])/5)
            dados[str(analise.inicio.strftime("%d/%m/%y %H:%M:%S"))] = [afetivoRelacional]
            dados[str(analise.inicio.strftime("%d/%m/%y %H:%M:%S"))].append(produtividade)
            dados[str(analise.inicio.strftime("%d/%m/%y %H:%M:%S"))].append(organico)
            dados[str(analise.inicio.strftime("%d/%m/%y %H:%M:%S"))].append(espiritual)
            dados[str(analise.inicio.strftime("%d/%m/%y %H:%M:%S"))].append(socioCultural)


        grafico = simplejson.dumps(dados)
        return grafico

    def pacienteNome(self):
        if 'paciente_id' in self.kwargs:
            paciente_id = self.kwargs['paciente_id']
        paciente = Paciente.objects.get(usuario_id=paciente_id)
        dados = { 'paciente': paciente.nome
        }

        paciente = simplejson.dumps(dados)
        return paciente

    def texto(self):
        if 'paciente_id' in self.kwargs:
            paciente_id = self.kwargs['paciente_id']
        if 'analise_id' in self.kwargs:
            analise_id = self.kwargs['analise_id']
        paciente = Paciente.objects.get(usuario_id=paciente_id)
        dados = {
        }
        anamnesia = Anamnesia.objects.filter(id=analise_id)
        for analise in anamnesia:
            area= AreaAfetiva.objects.filter(anamnesia_id=analise.id).order_by('resposta_id')
            A=[0]
            for respostas in area:
                resposta = RespostaAreaAfetiva.objects.get(id=respostas.resposta_id)
                A.append(resposta.valor)
            afetivoRelacional=((A[1]+A[2]+A[4]+A[6]+A[9]+A[13]+A[15]+A[17]+A[19]+A[20]+A[21]+A[22]+A[23]+A[25]+A[28])/15)
            produtividade=((A[5]+A[16]+A[20]+A[22]+A[23])/5)
            organico=((A[7]+A[12]+A[14]+A[27]+A[29])/5)
            espiritual=((A[3]+A[11]+A[18]+A[24]+A[26])/5)
            socioCultural=((A[8]+A[10]+A[20]+A[22]+A[23])/5)

        texto=""
        if afetivoRelacional >= 3 and afetivoRelacional <= 4:
            complementox = Recomendacao.objects.get(nome="complementox",intervalo="Máximo")
            complementoy = Recomendacao.objects.get(nome="complementoy",intervalo="Máximo")
        if afetivoRelacional >= 1.5 and afetivoRelacional < 3:
            complementox = Recomendacao.objects.get(nome="complementox",intervalo="Médio")
            complementoy = Recomendacao.objects.get(nome="complementoy",intervalo="Médio")
        if afetivoRelacional >= 0 and afetivoRelacional < 1.5:
            complementox = Recomendacao.objects.get(nome="complementox",intervalo="Mínimo")
            complementoy = Recomendacao.objects.get(nome="complementoy",intervalo="Mínimo")
        if produtividade >= 3 and produtividade <= 4:
            PRODUTIVIDADE = Recomendacao.objects.get(nome="produtividade",intervalo="Máximo")
        if produtividade >= 1.5 and produtividade < 3:
            PRODUTIVIDADE = Recomendacao.objects.get(nome="produtividade",intervalo="Médio")
        if produtividade >= 0 and produtividade < 1.5:
            PRODUTIVIDADE = Recomendacao.objects.get(nome="produtividade",intervalo="Mínimo")
        if organico >= 3 and organico <= 4:
            ORGANICO = Recomendacao.objects.get(nome="organico",intervalo="Máximo")
        if organico >= 1.5 and organico < 3:
            ORGANICO = Recomendacao.objects.get(nome="organico",intervalo="Médio")
        if organico >= 0 and organico < 1.5:
            ORGANICO = Recomendacao.objects.get(nome="organico",intervalo="Mínimo")
        if espiritual >= 3 and espiritual <= 4:
            ESPIRITUAL = Recomendacao.objects.get(nome="espiritual",intervalo="Máximo")
        if espiritual >= 1.5 and espiritual < 3:
            ESPIRITUAL = Recomendacao.objects.get(nome="espiritual",intervalo="Médio")
        if espiritual >= 0 and espiritual < 1.5:
            ESPIRITUAL = Recomendacao.objects.get(nome="espiritual",intervalo="Mínimo")
        if socioCultural >= 3 and socioCultural <= 4:
            SOCIOCULTURAL = Recomendacao.objects.get(nome="sociocultural",intervalo="Máximo")
        if socioCultural >= 1.5 and socioCultural < 3:
            SOCIOCULTURAL = Recomendacao.objects.get(nome="sociocultural",intervalo="Médio")
        if socioCultural >= 0 and socioCultural < 1.5:
            SOCIOCULTURAL = Recomendacao.objects.get(nome="sociocultural",intervalo="Mínimo")

        lista = [(organico,"a"),(produtividade,"b"),(socioCultural, "c"),(espiritual,"d")]
        minimo = min(lista, key=lambda x: x[0])
        if minimo[0] == produtividade:
            area = PRODUTIVIDADE.texto
        if minimo[0] == organico:
            area = ORGANICO.texto
        if minimo[0] ==  espiritual:
            area = ESPIRITUAL.texto
        if minimo[0] == socioCultural:
            area = SOCIOCULTURAL.texto

        parte1 = Recomendacao.objects.get(nome="afetivorelacional",intervalo="parte1")
        parte2 = Recomendacao.objects.get(nome="afetivorelacional",intervalo="parte2")
        parte3 = Recomendacao.objects.get(nome="afetivorelacional",intervalo="parte3")
        AFETIVORELACIONAL= parte1.texto+ complementox.texto+parte2.texto+complementoy.texto+parte3.texto
        texto = AFETIVORELACIONAL + area

        return texto

    def indiferenciacao(self):
        if 'analise_id' in self.kwargs:
            analise_id = self.kwargs['analise_id']
        indiferenciacao = GrauIndiferenciacaoPaciente.objects.filter(anamnesia_id=analise_id)

        return indiferenciacao

    def media(self):
        if 'paciente_id' in self.kwargs:
            paciente_id = self.kwargs['paciente_id']
        if 'analise_id' in self.kwargs:
            analise_id = self.kwargs['analise_id']
        paciente = Paciente.objects.get(usuario_id=paciente_id)

        nascimento=str(paciente.nascimento)
        ano = int(nascimento.split("-")[0])
        mes=int(nascimento.split("-")[1])
        dia=int(nascimento.split("-")[2])
        atual=datetime.now()
        anoAtual=atual.year
        mesAtual=atual.month
        diaAtual=atual.day

        if mes > mesAtual:
            idade = anoAtual-ano-1
        if mes < mesAtual:
            idade = anoAtual-ano
        if mes == mesAtual:
            if dia >= diaAtual:
                idade = anoAtual-ano-1
            if dia < diaAtual:
                idade = anoAtual-ano

        soma=0.0
        contador=0.0
        desvio=0.0
        variancia=0.0
        areaafetiva = AreaAfetiva.objects.filter(paciente_id=paciente.id,anamnesia_id=analise_id)

        for item in areaafetiva:
            resposta = RespostaAreaAfetiva.objects.get(id=item.resposta_id)

            if idade >=0 and idade <=7:
                soma = soma + resposta.nivel1
                if resposta.nivel1 != 0:
                    contador = contador+1
            if idade >=8 and idade <=12:
                soma = soma + resposta.nivel2
                if resposta.nivel2 != 0:
                    contador = contador+1
            if idade >=13 and idade <=19:
                soma = soma + resposta.nivel3
                if resposta.nivel3 != 0:
                    contador = contador+1
            if idade >=20 and idade <=24:
                soma = soma + resposta.nivel4
                if resposta.nivel4 != 0:
                    contador = contador+1
            if idade >=25:
                soma = soma + resposta.nivel5
                if resposta.nivel5 != 0:
                    contador = contador+1

        media = soma/contador
        contador=0
        for item in areaafetiva:
            resposta = RespostaAreaAfetiva.objects.get(id=item.resposta_id)

            if idade >=0 and idade <=7:
                if resposta.nivel1 != 0:
                    contador = contador+1
                    variancia= variancia + ((resposta.nivel1 - media)*(resposta.nivel1 - media))
            if idade >=8 and idade <=12:
                if resposta.nivel2 != 0:
                    contador = contador+1
                    variancia= variancia + ((resposta.nivel2 - media)*(resposta.nivel2 - media))
            if idade >=13 and idade <=19:
                if resposta.nivel3 != 0:
                    contador = contador+1
                    variancia= variancia + ((resposta.nivel3 - media)*(resposta.nivel3 - media))
            if idade >=20 and idade <=24:
                if resposta.nivel4 != 0:
                    contador = contador+1
                    variancia= variancia + ((resposta.nivel4 - media)*(resposta.nivel4 - media))
            if idade >=25:
                if resposta.nivel5 != 0:
                    contador = contador+1
                    variancia= variancia + ((resposta.nivel5 - media)*(resposta.nivel5 - media))

        desvio = math.sqrt(variancia/(contador-1))
        dict={
            "media":media,
            "desvio":desvio
        }
        return dict

    def paciente(self):
        if 'paciente_id' in self.kwargs:
            paciente_id = self.kwargs['paciente_id']
        paciente = Paciente.objects.get(usuario_id=paciente_id)
        return paciente


class RecomendacaoIndiferenciacao(TemplateView):

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(RecomendacaoIndiferenciacao, self).dispatch(*args, **kwargs)

    def anamnesia(self):
        if 'paciente_id' in self.kwargs:
            paciente_id = self.kwargs['paciente_id']
        paciente = Paciente.objects.get(usuario_id=paciente_id)
        if 'analise_id' in self.kwargs:
            analise_id = self.kwargs['analise_id']
        anamnesia = Anamnesia.objects.get(id=analise_id)
        main(paciente_id,analise_id)
        return anamnesia


    def grafico(self):
        if 'paciente_id' in self.kwargs:
            paciente_id = self.kwargs['paciente_id']
        if 'analise_id' in self.kwargs:
            analise_id = self.kwargs['analise_id']
        paciente = Paciente.objects.get(usuario_id=paciente_id)
        dados = {
        }
        anamnesia = Anamnesia.objects.filter(id=analise_id)
        criativo=0
        reativo=0
        adaptativo=0
        for analise in anamnesia:
            indiferenciacao = GrauIndiferenciacaoPaciente.objects.filter(anamnesia_id=analise.id)
            for opcao in indiferenciacao:
                resposta = GrauIndiferenciacao.objects.get(id=opcao.resposta_id)
                if resposta.padrao == "adaptativo":
                    adaptativo=adaptativo+1
                if resposta.padrao == "reativo":
                    reativo=reativo+1
                if resposta.padrao == "criativo":
                    criativo=criativo+1

            dados[str(analise.inicio.strftime("%d/%m/%y %H:%M:%S"))] = [adaptativo]
            dados[str(analise.inicio.strftime("%d/%m/%y %H:%M:%S"))].append(reativo)
            dados[str(analise.inicio.strftime("%d/%m/%y %H:%M:%S"))].append(criativo)

        nascimento=str(paciente.nascimento)
        ano = int(nascimento.split("-")[0])
        mes=int(nascimento.split("-")[1])
        dia=int(nascimento.split("-")[2])
        atual=datetime.now()
        anoAtual=atual.year
        mesAtual=atual.month
        diaAtual=atual.day

        if mes > mesAtual:
            idade = anoAtual-ano-1
        if mes < mesAtual:
            idade = anoAtual-ano
        if mes == mesAtual:
            if dia >= diaAtual:
                idade = anoAtual-ano-1
            if dia < diaAtual:
                idade = anoAtual-ano

        adaptativoMin=0
        adaptativoMax=0
        criativoMin=0
        criativoMax=0
        reativoMin=0
        reativoMax=0

        if idade >=0 and idade <=3:
            adaptativoMin=14
            adaptativoMax=17
            criativoMin=0
            criativoMax=2
            reativoMin=0
            reativoMax=2
        if idade >=4 and idade <=7:
            adaptativoMin=12
            adaptativoMax=17
            criativoMin=0
            criativoMax=3
            reativoMin=2
            reativoMax=6
        if idade >=8 and idade <=12:
            adaptativoMin=8
            adaptativoMax=13
            criativoMin=2
            criativoMax=5
            reativoMin=6
            reativoMax=10
        if idade >=13 and idade <=19:
            adaptativoMin=4
            adaptativoMax=8
            criativoMin=6
            criativoMax=8
            reativoMin=10
            reativoMax=15
        if idade >=20 and idade <=24:
            adaptativoMin=1
            adaptativoMax=3
            criativoMin=9
            criativoMax=11
            reativoMin=8
            reativoMax=12
        if idade >=25 and idade <=32:
            adaptativoMin=0
            adaptativoMax=2
            criativoMin=11
            criativoMax=15
            reativoMin=3
            reativoMax=7
        if idade >=33:
            adaptativoMin=0
            adaptativoMax=2
            criativoMin=16
            criativoMax=19
            reativoMin=0
            reativoMax=2

        dados['Limite Inferior Adaptativo'] = adaptativoMin
        dados['Limite Inferior Reativo']=reativoMin
        dados['Limite Inferior Criativo']=criativoMin
        dados['Limite Superior Adaptativo'] = adaptativoMax
        dados['Limite Superior Reativo']=reativoMax
        dados['Limite Superior Criativo']=criativoMax

        grafico = simplejson.dumps(dados)
        return grafico

    def pacienteNome(self):
        if 'paciente_id' in self.kwargs:
            paciente_id = self.kwargs['paciente_id']
        paciente = Paciente.objects.get(usuario_id=paciente_id)
        dados = { 'paciente': paciente.nome
        }

        paciente = simplejson.dumps(dados)
        return paciente

    def paciente(self):
        if 'paciente_id' in self.kwargs:
            paciente_id = self.kwargs['paciente_id']
        paciente = Paciente.objects.get(usuario_id=paciente_id)
        return paciente

    def texto(self):
        if 'paciente_id' in self.kwargs:
            paciente_id = self.kwargs['paciente_id']
        if 'analise_id' in self.kwargs:
            analise_id = self.kwargs['analise_id']
        paciente = Paciente.objects.get(usuario_id=paciente_id)
        anamnesia = Anamnesia.objects.filter(id=analise_id)

        criativo=0
        reativo=0
        adaptativo=0
        for analise in anamnesia:
            indiferenciacao = GrauIndiferenciacaoPaciente.objects.filter(anamnesia_id=analise.id)
            for opcao in indiferenciacao:
                resposta = GrauIndiferenciacao.objects.get(id=opcao.resposta_id)
                if resposta.padrao == "adaptativo":
                    adaptativo=adaptativo+1
                if resposta.padrao == "reativo":
                    reativo=reativo+1
                if resposta.padrao == "criativo":
                    criativo=criativo+1

        nascimento=str(paciente.nascimento)
        ano = int(nascimento.split("-")[0])
        mes=int(nascimento.split("-")[1])
        dia=int(nascimento.split("-")[2])
        atual=datetime.now()
        anoAtual=atual.year
        mesAtual=atual.month
        diaAtual=atual.day

        if mes > mesAtual:
            idade = anoAtual-ano-1
        if mes < mesAtual:
            idade = anoAtual-ano
        if mes == mesAtual:
            if dia >= diaAtual:
                idade = anoAtual-ano-1
            if dia < diaAtual:
                idade = anoAtual-ano

        adaptativoMin=0
        adaptativoMax=0
        criativoMin=0
        criativoMax=0
        reativoMin=0
        reativoMax=0

        if idade >=0 and idade <=3:
            adaptativoMin=14
            adaptativoMax=17
            criativoMin=0
            criativoMax=2
            reativoMin=0
            reativoMax=2
        if idade >=4 and idade <=7:
            adaptativoMin=12
            adaptativoMax=17
            criativoMin=0
            criativoMax=3
            reativoMin=2
            reativoMax=6
        if idade >=8 and idade <=12:
            adaptativoMin=8
            adaptativoMax=13
            criativoMin=2
            criativoMax=5
            reativoMin=6
            reativoMax=10
        if idade >=13 and idade <=19:
            adaptativoMin=4
            adaptativoMax=8
            criativoMin=6
            criativoMax=8
            reativoMin=10
            reativoMax=15
        if idade >=20 and idade <=24:
            adaptativoMin=1
            adaptativoMax=3
            criativoMin=9
            criativoMax=11
            reativoMin=8
            reativoMax=12
        if idade >=25 and idade <=32:
            adaptativoMin=0
            adaptativoMax=2
            criativoMin=11
            criativoMax=15
            reativoMin=3
            reativoMax=7
        if idade >=33:
            adaptativoMin=0
            adaptativoMax=2
            criativoMin=16
            criativoMax=19
            reativoMin=0
            reativoMax=2

        tudo_dentro=""
        abaixo_adaptativo=""
        acima_adaptativo=""
        abaixo_criativo=""
        acima_criativo=""
        abaixo_reativo=""
        acima_reativo=""
        texto=""
        if adaptativo>adaptativoMin and adaptativo<adaptativoMax and\
                        reativo>reativoMin and reativo<reativoMax and\
                        criativo>criativoMin and criativo<criativoMax:
            tudo_dentro = Recomendacao.objects.get(nome='tudo_dentro')
            texto= tudo_dentro.texto
        if adaptativo<adaptativoMin:
            abaixo_adaptativo = Recomendacao.objects.get(nome='intervalo_adaptativo',intervalo="abaixo")
            texto=texto+abaixo_adaptativo.texto
        if adaptativo>adaptativoMax:
            acima_adaptativo = Recomendacao.objects.get(nome='intervalo_adaptativo',intervalo="acima")
            texto=texto+acima_adaptativo.texto
        if reativo<reativoMin:
            abaixo_reativo = Recomendacao.objects.get(nome='intervalo_reativo',intervalo="abaixo")
            texto=texto+abaixo_reativo.texto
        if reativo>reativoMax:
            acima_reativo = Recomendacao.objects.get(nome='intervalo_reativo',intervalo="acima")
            texto=texto+acima_reativo.texto
        if criativo<criativoMin:
            abaixo_criativo = Recomendacao.objects.get(nome='intervalo_criativo',intervalo="abaixo")
            texto=texto+abaixo_criativo.texto
        if criativo>criativoMax:
            acima_criativo = Recomendacao.objects.get(nome='intervalo_criativo',intervalo="acima")
            texto=texto+acima_criativo.texto

        return texto

    def interventiva(self):
        if 'analise_id' in self.kwargs:
            analise_id = self.kwargs['analise_id']
        interventiva = Interventiva.objects.filter(anamnesia_id=analise_id)

        return interventiva

def pdf_view(request, paciente_id,analise_id):
    paciente_id=paciente_id
    analise_id=analise_id
    return FileResponse(open("/home/thaispirate/genograma-"+paciente_id+"-"+analise_id+".pdf", 'rb'), content_type='application/pdf')


class RecomendacaoSeletiva(TemplateView):

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(RecomendacaoSeletiva, self).dispatch(*args, **kwargs)

    def anamnesia(self):
        if 'paciente_id' in self.kwargs:
            paciente_id = self.kwargs['paciente_id']
        paciente = Paciente.objects.get(usuario_id=paciente_id)
        if 'analise_id' in self.kwargs:
            analise_id = self.kwargs['analise_id']
        anamnesia = Anamnesia.objects.get(id=analise_id)
        return anamnesia

    def pacienteNome(self):
        if 'paciente_id' in self.kwargs:
            paciente_id = self.kwargs['paciente_id']
        paciente = Paciente.objects.get(usuario_id=paciente_id)
        dados = { 'paciente': paciente.nome
        }

        paciente = simplejson.dumps(dados)
        return paciente

    def paciente(self):
        if 'paciente_id' in self.kwargs:
            paciente_id = self.kwargs['paciente_id']
        paciente = Paciente.objects.get(usuario_id=paciente_id)
        return paciente

    def texto(self):
        if 'paciente_id' in self.kwargs:
            paciente_id = self.kwargs['paciente_id']
        if 'analise_id' in self.kwargs:
            analise_id = self.kwargs['analise_id']
        paciente = Paciente.objects.get(usuario_id=paciente_id)
        anamnesia = Anamnesia.objects.get(id=analise_id)

        nascimento=str(paciente.nascimento)
        ano = int(nascimento.split("-")[0])
        mes=int(nascimento.split("-")[1])
        dia=int(nascimento.split("-")[2])
        atual=datetime.now()
        anoAtual=atual.year
        mesAtual=atual.month
        diaAtual=atual.day

        if mes > mesAtual:
            idade = anoAtual-ano-1
        if mes < mesAtual:
            idade = anoAtual-ano
        if mes == mesAtual:
            if dia >= diaAtual:
                idade = anoAtual-ano-1
            if dia < diaAtual:
                idade = anoAtual-ano

        texto={}
        relacionamento="Não há recomendações"
        diferenciacao="Não há recomendações"
        autonomia="Não há recomendações"
        assertividade="Não há recomendações"
        autoEstima="Não há recomendações"
        somarelacionamento=0
        somadiferenciacao=0
        somaautonomia=0
        somaassertividade=0
        somaautoestima=0

        perguntasrelacionamento=["S34","S35","S36"]
        perguntasdiferenciacao=["S05","S06","S15","S16","S24","S25"]
        perguntasautonomia=["S01","S07","S08","S09","S10","S11","S12","S13","S28"]
        perguntasassertiva=["S14","S18","S20","S21","S30","S31","S32","S33",]
        perguntasautoEstima=["S02","S17","S19","S22","S23","S26","S27","S29"]

        seletiva = Seletiva.objects.filter(paciente_id=paciente.id,anamnesia_id=anamnesia.id)
        for item in seletiva:
            resposta = RespostaSeletiva.objects.get(id=item.resposta_id)
            pergunta = PerguntaSeletiva.objects.get(id=resposta.pergunta_id)

            if pergunta.numero in perguntasrelacionamento:
                nome="relacionamento"
                if idade >=0 and idade <=3:
                    if resposta.nivel0 != 0:
                        somarelacionamento=somarelacionamento+resposta.nivel0
                        if resposta.nivel0 <=1:
                            relacionamento=Recomendacao.objects.get(nome=nome,intervalo="nivel0")
                if idade >=4 and idade <=7:
                    if resposta.nivel1 != 0:
                        somarelacionamento=somarelacionamento+resposta.nivel1
                        if resposta.nivel1 <=1:
                            relacionamento=Recomendacao.objects.get(nome=nome,intervalo="nivel1")
                            relacionamento=relacionamento.texto
                if idade >=8 and idade <=12:
                    if resposta.nivel2 != 0:
                        somarelacionamento=somarelacionamento+resposta.nivel2
                        if resposta.nivel2 <=1:
                            relacionamento=Recomendacao.objects.get(nome=nome,intervalo="nivel2")
                            relacionamento=relacionamento.texto
                if idade >=13 and idade <=19:
                    if resposta.nivel3 != 0:
                        somarelacionamento=somarelacionamento+resposta.nivel3
                        if resposta.nivel3 <=1:
                            relacionamento=Recomendacao.objects.get(nome=nome,intervalo="nivel3")
                            relacionamento=relacionamento.texto
                if idade >=20 and idade <=24:
                    if resposta.nivel4 != 0:
                        somarelacionamento=somarelacionamento+resposta.nivel4
                        if resposta.nivel4 <=1:
                            relacionamento=Recomendacao.objects.get(nome=nome,intervalo="nivel4")
                            relacionamento=relacionamento.texto
                if idade >=25 and idade <=32:
                    if resposta.nivel5 != 0:
                        somarelacionamento=somarelacionamento+resposta.nivel5
                        if resposta.nivel5 <=1:
                            relacionamento=Recomendacao.objects.get(nome=nome,intervalo="nivel5")
                            relacionamento=relacionamento.texto
                if idade >=33:
                    if resposta.nivel6 != 0:
                        somarelacionamento=somarelacionamento+resposta.nivel6
                        if resposta.nivel6 <=1:
                            relacionamento=Recomendacao.objects.get(nome=nome,intervalo="nivel6")
                            relacionamento=relacionamento.texto

            if pergunta.numero in perguntasdiferenciacao:
                nome="diferenciacao"
                if idade >=0 and idade <=3:
                    if resposta.nivel0 != 0:
                        somadiferenciacao=somadiferenciacao+resposta.nivel0
                        if resposta.nivel0 <=1:
                            diferenciacao=Recomendacao.objects.get(nome=nome,intervalo="nivel0")
                if idade >=4 and idade <=7:
                    if resposta.nivel1 != 0:
                        somadiferenciacao=somadiferenciacao+resposta.nivel1
                        if resposta.nivel1 <=1:
                            diferenciacao=Recomendacao.objects.get(nome=nome,intervalo="nivel1")
                            diferenciacao=diferenciacao.texto
                if idade >=8 and idade <=12:
                    if resposta.nivel2 != 0:
                        somadiferenciacao=somadiferenciacao+resposta.nivel2
                        if resposta.nivel2 <=1:
                            diferenciacao=Recomendacao.objects.get(nome=nome,intervalo="nivel2")
                            diferenciacao=diferenciacao.texto
                if idade >=13 and idade <=19:
                    if resposta.nivel3 != 0:
                        somadiferenciacao=somadiferenciacao+resposta.nivel3
                        if resposta.nivel3 <=1:
                            diferenciacao=Recomendacao.objects.get(nome=nome,intervalo="nivel3")
                            diferenciacao=diferenciacao.texto
                if idade >=20 and idade <=24:
                    if resposta.nivel4 != 0:
                        somadiferenciacao=somadiferenciacao+resposta.nivel4
                        if resposta.nivel4 <=1:
                            diferenciacao=Recomendacao.objects.get(nome=nome,intervalo="nivel4")
                            diferenciacao=diferenciacao.texto
                if idade >=25 and idade <=32:
                    if resposta.nivel5 != 0:
                        somadiferenciacao=somadiferenciacao+resposta.nivel5
                        if resposta.nivel5 <=1:
                            diferenciacao=Recomendacao.objects.get(nome=nome,intervalo="nivel5")
                            diferenciacao=diferenciacao.texto
                if idade >=33:
                    if resposta.nivel6 != 0:
                        somadiferenciacao=somadiferenciacao+resposta.nivel6
                        if resposta.nivel6 <=1:
                            diferenciacao=Recomendacao.objects.get(nome=nome,intervalo="nivel6")
                            diferenciacao=diferenciacao.texto

            if pergunta.numero in perguntasautonomia:
                nome="autonomia"
                if idade >=0 and idade <=3:
                    if resposta.nivel0 != 0:
                        somaautonomia=somaautonomia+resposta.nivel0
                        if resposta.nivel0 <=1:
                            autonomia=Recomendacao.objects.get(nome=nome,intervalo="nivel0")
                if idade >=4 and idade <=7:
                    if resposta.nivel1 != 0:
                        somaautonomia=somaautonomia+resposta.nivel1
                        if resposta.nivel1 <=1:
                            autonomia=Recomendacao.objects.get(nome=nome,intervalo="nivel1")
                            autonomia=autonomia.texto
                if idade >=8 and idade <=12:
                    if resposta.nivel2 != 0:
                        somaautonomia=somaautonomia+resposta.nivel2
                        if resposta.nivel2 <=1:
                            autonomia=Recomendacao.objects.get(nome=nome,intervalo="nivel2")
                            autonomia=autonomia.texto
                if idade >=13 and idade <=19:
                    if resposta.nivel3 != 0:
                        somaautonomia=somaautonomia+resposta.nivel3
                        if resposta.nivel3 <=1:
                            autonomia=Recomendacao.objects.get(nome=nome,intervalo="nivel3")
                            autonomia=autonomia.texto
                if idade >=20 and idade <=24:
                    if resposta.nivel4 != 0:
                        somaautonomia=somaautonomia+resposta.nivel4
                        if resposta.nivel4 <=1:
                            autonomia=Recomendacao.objects.get(nome=nome,intervalo="nivel4")
                            autonomia=autonomia.texto
                if idade >=25 and idade <=32:
                    if resposta.nivel5 != 0:
                        somaautonomia=somaautonomia+resposta.nivel5
                        if resposta.nivel5 <=1:
                            autonomia=Recomendacao.objects.get(nome=nome,intervalo="nivel5")
                            autonomia=autonomia.texto
                if idade >=33:
                    if resposta.nivel6 != 0:
                        somaautonomia=somaautonomia+resposta.nivel6
                        if resposta.nivel6 <=1:
                            autonomia=Recomendacao.objects.get(nome=nome,intervalo="nivel6")
                            autonomia=autonomia.texto

            if pergunta.numero in perguntasassertiva:
                nome="assertividade"
                if idade >=0 and idade <=3:
                    if resposta.nivel0 != 0:
                        somaassertividade=somaassertividade+resposta.nivel0
                        if resposta.nivel0 <=1:
                            assertividade=Recomendacao.objects.get(nome=nome,intervalo="nivel0")
                if idade >=4 and idade <=7:
                    if resposta.nivel1 != 0:
                        somaassertividade=somaassertividade+resposta.nivel1
                        if resposta.nivel1 <=1:
                            assertividade=Recomendacao.objects.get(nome=nome,intervalo="nivel1")
                            assertividade=assertividade.texto
                if idade >=8 and idade <=12:
                    if resposta.nivel2 != 0:
                        somaassertividade=somaassertividade+resposta.nivel2
                        if resposta.nivel2 <=1:
                            assertividade=Recomendacao.objects.get(nome=nome,intervalo="nivel2")
                            assertividade=assertividade.texto
                if idade >=13 and idade <=19:
                    if resposta.nivel3 != 0:
                        somaassertividade=somaassertividade+resposta.nivel3
                        if resposta.nivel3 <=1:
                            assertividade=Recomendacao.objects.get(nome=nome,intervalo="nivel3")
                            assertividade=assertividade.texto
                if idade >=20 and idade <=24:
                    if resposta.nivel4 != 0:
                        somaassertividade=somaassertividade+resposta.nivel4
                        if resposta.nivel4 <=1:
                            assertividade=Recomendacao.objects.get(nome=nome,intervalo="nivel4")
                            assertividade=assertividade.texto
                if idade >=25 and idade <=32:
                    if resposta.nivel5 != 0:
                        somaassertividade=somaassertividade+resposta.nivel5
                        if resposta.nivel5 <=1:
                            assertividade=Recomendacao.objects.get(nome=nome,intervalo="nivel5")
                            assertividade=assertividade.texto
                if idade >=33:
                    if resposta.nivel6 != 0:
                        somaassertividade=somaassertividade+resposta.nivel6
                        if resposta.nivel6 <=1:
                            assertividade=Recomendacao.objects.get(nome=nome,intervalo="nivel6")
                            assertividade=assertividade.texto

            if pergunta.numero in perguntasautoEstima:
                nome="autoestima"
                if idade >=0 and idade <=3:
                    if resposta.nivel0 != 0:
                        somaautoestima=somaautoestima+resposta.nivel0
                        if resposta.nivel0 <=1:
                            autoEstima=Recomendacao.objects.get(nome=nome,intervalo="nivel0")
                if idade >=4 and idade <=7:
                    if resposta.nivel1 != 0:
                        somaautoestima=somaautoestima+resposta.nivel1
                        if resposta.nivel1 <=1:
                            autoEstima=Recomendacao.objects.get(nome=nome,intervalo="nivel1")
                            autoEstima=autoEstima.texto
                if idade >=8 and idade <=12:
                    if resposta.nivel2 != 0:
                        somaautoestima=somaautoestima+resposta.nivel2
                        if resposta.nivel2 <=1:
                            autoEstima=Recomendacao.objects.get(nome=nome,intervalo="nivel2")
                            autoEstima=autoEstima.texto
                if idade >=13 and idade <=19:
                    if resposta.nivel3 != 0:
                        somaautoestima=somaautoestima+resposta.nivel3
                        if resposta.nivel3 <=1:
                            autoEstima=Recomendacao.objects.get(nome=nome,intervalo="nivel3")
                            autoEstima=autoEstima.texto
                if idade >=20 and idade <=24:
                    if resposta.nivel4 != 0:
                        somaautoestima=somaautoestima+resposta.nivel4
                        if resposta.nivel4 <=1:
                            autoEstima=Recomendacao.objects.get(nome=nome,intervalo="nivel4")
                            autoEstima=autoEstima.texto
                if idade >=25 and idade <=32:
                    if resposta.nivel5 != 0:
                        somaautoestima=somaautoestima+resposta.nivel5
                        if resposta.nivel5 <=1:
                            autoEstima=Recomendacao.objects.get(nome=nome,intervalo="nivel5")
                            autoEstima=autoEstima.texto
                if idade >=33:
                    if resposta.nivel6 != 0:
                        somaautoestima=somaautoestima+resposta.nivel6
                        if resposta.nivel6 <=1:
                            autoEstima=Recomendacao.objects.get(nome=nome,intervalo="nivel6")
                            autoEstima=autoEstima.texto

        if somarelacionamento/len(perguntasrelacionamento) < 3:
            nome="relacionamento"
            if idade >=0 and idade <=3:
                relacionamento= Recomendacao.objects.get(nome=nome, intervalo="nivel0")
            if idade >=4 and idade <=7:
                relacionamento= Recomendacao.objects.get(nome=nome, intervalo="nivel1")
            if idade >=8 and idade <=12:
                relacionamento= Recomendacao.objects.get(nome=nome, intervalo="nivel2")
            if idade >=13 and idade <=19:
                relacionamento= Recomendacao.objects.get(nome=nome, intervalo="nivel3")
            if idade >=20 and idade <=24:
                relacionamento= Recomendacao.objects.get(nome=nome, intervalo="nivel4")
            if idade >=25 and idade <=32:
                relacionamento= Recomendacao.objects.get(nome=nome, intervalo="nivel5")
            if idade >=33:
                relacionamento= Recomendacao.objects.get(nome=nome, intervalo="nivel6")
            relacionamento=relacionamento.texto

        if somadiferenciacao/len(perguntasdiferenciacao) < 3:
            nome="diferenciacao"
            if idade >=0 and idade <=3:
                diferenciacao= Recomendacao.objects.get(nome=nome, intervalo="nivel0")
            if idade >=4 and idade <=7:
                diferenciacao= Recomendacao.objects.get(nome=nome, intervalo="nivel1")
            if idade >=8 and idade <=12:
                diferenciacao= Recomendacao.objects.get(nome=nome, intervalo="nivel2")
            if idade >=13 and idade <=19:
                diferenciacao= Recomendacao.objects.get(nome=nome, intervalo="nivel3")
            if idade >=20 and idade <=24:
                diferenciacao= Recomendacao.objects.get(nome=nome, intervalo="nivel4")
            if idade >=25 and idade <=32:
                diferenciacao= Recomendacao.objects.get(nome=nome, intervalo="nivel5")
            if idade >=33:
                diferenciacao= Recomendacao.objects.get(nome=nome, intervalo="nivel6")
            diferenciacao=diferenciacao.texto

        if somaautonomia/len(perguntasautonomia) < 3:
            nome="autonomia"
            if idade >=0 and idade <=3:
                autonomia= Recomendacao.objects.get(nome=nome, intervalo="nivel0")
            if idade >=4 and idade <=7:
                autonomia= Recomendacao.objects.get(nome=nome, intervalo="nivel1")
            if idade >=8 and idade <=12:
                autonomia= Recomendacao.objects.get(nome=nome, intervalo="nivel2")
            if idade >=13 and idade <=19:
                autonomia= Recomendacao.objects.get(nome=nome, intervalo="nivel3")
            if idade >=20 and idade <=24:
                autonomia= Recomendacao.objects.get(nome=nome, intervalo="nivel4")
            if idade >=25 and idade <=32:
                autonomia= Recomendacao.objects.get(nome=nome, intervalo="nivel5")
            if idade >=33:
                autonomia= Recomendacao.objects.get(nome=nome, intervalo="nivel6")
            autonomia=autonomia.texto

        if somaassertividade/len(perguntasassertiva) < 3:
            nome="assertividade"
            if idade >=0 and idade <=3:
                assertividade= Recomendacao.objects.get(nome=nome, intervalo="nivel0")
            if idade >=4 and idade <=7:
                assertividade= Recomendacao.objects.get(nome=nome, intervalo="nivel1")
            if idade >=8 and idade <=12:
                assertividade= Recomendacao.objects.get(nome=nome, intervalo="nivel2")
            if idade >=13 and idade <=19:
                assertividade= Recomendacao.objects.get(nome=nome, intervalo="nivel3")
            if idade >=20 and idade <=24:
                assertividade= Recomendacao.objects.get(nome=nome, intervalo="nivel4")
            if idade >=25 and idade <=32:
                assertividade= Recomendacao.objects.get(nome=nome, intervalo="nivel5")
            if idade >=33:
                assertividade= Recomendacao.objects.get(nome=nome, intervalo="nivel6")
            assertividade=assertividade.texto

        if somaautoestima/len(perguntasautoEstima) < 3:
            nome="autoestima"
            if idade >=0 and idade <=3:
                autoEstima= Recomendacao.objects.get(nome=nome, intervalo="nivel0")
            if idade >=4 and idade <=7:
                autoEstima= Recomendacao.objects.get(nome=nome, intervalo="nivel1")
            if idade >=8 and idade <=12:
                autoEstima= Recomendacao.objects.get(nome=nome, intervalo="nivel2")
            if idade >=13 and idade <=19:
                autoEstima= Recomendacao.objects.get(nome=nome, intervalo="nivel3")
            if idade >=20 and idade <=24:
                autoEstima= Recomendacao.objects.get(nome=nome, intervalo="nivel4")
            if idade >=25 and idade <=32:
                autoEstima= Recomendacao.objects.get(nome=nome, intervalo="nivel5")
            if idade >=33:
                autoEstima= Recomendacao.objects.get(nome=nome, intervalo="nivel6")
            autoEstima=autoEstima.texto

        texto["Relacionamento"]=relacionamento
        texto["Diferenciação"]=diferenciacao
        texto["Autonomia"]=autonomia
        texto["Assertividade"]=assertividade
        texto["Autoestima"]=autoEstima
        return texto

class RecomendacaoTarefas(TemplateView):

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(RecomendacaoTarefas, self).dispatch(*args, **kwargs)

    def anamnesia(self):
        if 'paciente_id' in self.kwargs:
            paciente_id = self.kwargs['paciente_id']
        paciente = Paciente.objects.get(usuario_id=paciente_id)
        if 'analise_id' in self.kwargs:
            analise_id = self.kwargs['analise_id']
        anamnesia = Anamnesia.objects.get(id=analise_id)
        return anamnesia

    def paciente(self):
        if 'paciente_id' in self.kwargs:
            paciente_id = self.kwargs['paciente_id']
        paciente = Paciente.objects.get(usuario_id=paciente_id)
        return paciente

    def tarefaAreaAfetiva(self):
        texto={}
        if 'paciente_id' in self.kwargs:
            paciente_id = self.kwargs['paciente_id']
        if 'analise_id' in self.kwargs:
            analise_id = self.kwargs['analise_id']
        paciente= Paciente.objects.get(usuario_id=paciente_id)
        anamnesia = Anamnesia.objects.filter(paciente_id=paciente.id)
        for analise in anamnesia:
            area= AreaAfetiva.objects.filter(anamnesia_id=analise.id).order_by('resposta_id')
            A=[0]
            for respostas in area:
                resposta = RespostaAreaAfetiva.objects.get(id=respostas.resposta_id)
                A.append(resposta.valor)
            afetivoRelacional=((A[1]+A[2]+A[4]+A[6]+A[9]+A[13]+A[15]+A[17]+A[19]+A[20]+A[21]+A[22]+A[23]+A[25]+A[28])/15)
            produtividade=((A[5]+A[16]+A[20]+A[22]+A[23])/5)
            organico=((A[7]+A[12]+A[14]+A[27]+A[29])/5)
            espiritual=((A[3]+A[11]+A[18]+A[24]+A[26])/5)
            socioCultural=((A[8]+A[10]+A[20]+A[22]+A[23])/5)

        if afetivoRelacional >=1.5 and afetivoRelacional < 3:
            texto["afetivo"]="AreaAfetiva_Afetivo Relacional_1.5-3"
        if afetivoRelacional >= 0 and afetivoRelacional < 1.5:
            texto["afetivo"]="AreaAfetiva_Afetivo Relacional_0-1.5"
        if produtividade >=0 and produtividade < 1.5:
            texto["produtividade"]="AreaAfetiva_Produtividade"
        if organico >=0 and organico < 1.5:
            texto["organico"]="AreaAfetiva_Organico"
        if espiritual >=0 and espiritual < 1.5:
            texto["espiritual"]="AreaAfetiva_Espiritual"
        if socioCultural >=0 and socioCultural < 1.5:
            texto["sociocultural"]="AreaAfetiva_SocioCultural"
        return texto

    def tarefaIndiferenciacao(self):
        texto={}
        if 'paciente_id' in self.kwargs:
            paciente_id = self.kwargs['paciente_id']
        if 'analise_id' in self.kwargs:
            analise_id = self.kwargs['analise_id']
        paciente= Paciente.objects.get(usuario_id=paciente_id)
        anamnesia = Anamnesia.objects.filter(id=analise_id)

        criativo=0
        reativo=0
        adaptativo=0
        for analise in anamnesia:
            indiferenciacao = GrauIndiferenciacaoPaciente.objects.filter(anamnesia_id=analise.id)
            for opcao in indiferenciacao:
                resposta = GrauIndiferenciacao.objects.get(id=opcao.resposta_id)
                if resposta.padrao == "adaptativo":
                    adaptativo=adaptativo+1
                if resposta.padrao == "reativo":
                    reativo=reativo+1
                if resposta.padrao == "criativo":
                    criativo=criativo+1

        nascimento=str(paciente.nascimento)
        ano = int(nascimento.split("-")[0])
        mes=int(nascimento.split("-")[1])
        dia=int(nascimento.split("-")[2])
        atual=datetime.now()
        anoAtual=atual.year
        mesAtual=atual.month
        diaAtual=atual.day

        if mes > mesAtual:
            idade = anoAtual-ano-1
        if mes < mesAtual:
            idade = anoAtual-ano
        if mes == mesAtual:
            if dia >= diaAtual:
                idade = anoAtual-ano-1
            if dia < diaAtual:
                idade = anoAtual-ano

        adaptativoMin=0
        adaptativoMax=0
        criativoMin=0
        criativoMax=0
        reativoMin=0
        reativoMax=0

        if idade >=0 and idade <=3:
            adaptativoMin=14
            adaptativoMax=17
            criativoMin=0
            criativoMax=2
            reativoMin=0
            reativoMax=2
        if idade >=4 and idade <=7:
            adaptativoMin=12
            adaptativoMax=17
            criativoMin=0
            criativoMax=3
            reativoMin=2
            reativoMax=6
        if idade >=8 and idade <=12:
            adaptativoMin=8
            adaptativoMax=13
            criativoMin=2
            criativoMax=5
            reativoMin=6
            reativoMax=10
        if idade >=13 and idade <=19:
            adaptativoMin=4
            adaptativoMax=8
            criativoMin=6
            criativoMax=8
            reativoMin=10
            reativoMax=15
        if idade >=20 and idade <=24:
            adaptativoMin=1
            adaptativoMax=3
            criativoMin=9
            criativoMax=11
            reativoMin=8
            reativoMax=12
        if idade >=25 and idade <=32:
            adaptativoMin=0
            adaptativoMax=2
            criativoMin=11
            criativoMax=15
            reativoMin=3
            reativoMax=7
        if idade >=33:
            adaptativoMin=0
            adaptativoMax=2
            criativoMin=16
            criativoMax=19
            reativoMin=0
            reativoMax=2

        if adaptativo<adaptativoMin or adaptativo>adaptativoMax and\
                        reativo<reativoMin or reativo>reativoMax and\
                        criativo<criativoMin or criativo>criativoMax:
            texto["geral"]= "Padrao de Funcionamento Mental Geral"
        if adaptativo<adaptativoMin or adaptativo>adaptativoMax:
            texto["adaptativo"] = "Padrao de Funcionamento Mental Adaptativo"
        if reativo<reativoMin or reativo>reativoMax:
            texto["reativo"] = "Padrao de Funcionamento Mental Reativo"
        if criativo<criativoMin or criativo>criativoMax:
            texto["criativo"] = "Padrao de Funcionamento Mental Criativo"

        return texto

    def tarefaRelacionamento(self):
        if 'paciente_id' in self.kwargs:
            paciente_id = self.kwargs['paciente_id']
        if 'analise_id' in self.kwargs:
            analise_id = self.kwargs['analise_id']
        paciente= Paciente.objects.get(usuario_id=paciente_id)
        anamnesia = Anamnesia.objects.get(id=analise_id)

        nascimento=str(paciente.nascimento)
        ano = int(nascimento.split("-")[0])
        mes=int(nascimento.split("-")[1])
        dia=int(nascimento.split("-")[2])
        atual=datetime.now()
        anoAtual=atual.year
        mesAtual=atual.month
        diaAtual=atual.day

        if mes > mesAtual:
            idade = anoAtual-ano-1
        if mes < mesAtual:
            idade = anoAtual-ano
        if mes == mesAtual:
            if dia >= diaAtual:
                idade = anoAtual-ano-1
            if dia < diaAtual:
                idade = anoAtual-ano

        somarelacionamento=0

        perguntasrelacionamento=["S34","S35","S36"]

        texto=""
        seletiva = Seletiva.objects.filter(paciente_id=paciente.id,anamnesia_id=anamnesia.id)
        for item in seletiva:
            resposta = RespostaSeletiva.objects.get(id=item.resposta_id)
            pergunta = PerguntaSeletiva.objects.get(id=resposta.pergunta_id)

            if pergunta.numero in perguntasrelacionamento:
                if idade >=0 and idade <=3:
                    if resposta.nivel0 != 0:
                        somarelacionamento=somarelacionamento+resposta.nivel0
                        if resposta.nivel0 <=1:
                            texto="pdfrelacionamento"
                if idade >=4 and idade <=7:
                    if resposta.nivel1 != 0:
                        somarelacionamento=somarelacionamento+resposta.nivel1
                        if resposta.nivel1 <=1:
                            texto="pdfrelacionamento"
                if idade >=8 and idade <=12:
                    if resposta.nivel2 != 0:
                        somarelacionamento=somarelacionamento+resposta.nivel2
                        if resposta.nivel2 <=1:
                            texto="pdfrelacionamento"
                if idade >=13 and idade <=19:
                    if resposta.nivel3 != 0:
                        somarelacionamento=somarelacionamento+resposta.nivel3
                        if resposta.nivel3 <=1:
                            texto="pdfrelacionamento"
                if idade >=20 and idade <=24:
                    if resposta.nivel4 != 0:
                        somarelacionamento=somarelacionamento+resposta.nivel4
                        if resposta.nivel4 <=1:
                            texto="pdfrelacionamento"
                if idade >=25 and idade <=32:
                    if resposta.nivel5 != 0:
                        somarelacionamento=somarelacionamento+resposta.nivel5
                        if resposta.nivel5 <=1:
                            texto="pdfrelacionamento"
                if idade >=33:
                    if resposta.nivel6 != 0:
                        somarelacionamento=somarelacionamento+resposta.nivel6
                        if resposta.nivel6 <=1:
                            texto="pdfrelacionamento"

        if somarelacionamento/len(perguntasrelacionamento) < 3:
            texto="pdfrelacionamento"

        return texto

    def tarefaDiferenciacao(self):
        texto=""
        if 'paciente_id' in self.kwargs:
            paciente_id = self.kwargs['paciente_id']
        if 'analise_id' in self.kwargs:
            analise_id = self.kwargs['analise_id']
        paciente= Paciente.objects.get(usuario_id=paciente_id)
        anamnesia = Anamnesia.objects.get(id=analise_id)

        nascimento=str(paciente.nascimento)
        ano = int(nascimento.split("-")[0])
        mes=int(nascimento.split("-")[1])
        dia=int(nascimento.split("-")[2])
        atual=datetime.now()
        anoAtual=atual.year
        mesAtual=atual.month
        diaAtual=atual.day

        if mes > mesAtual:
            idade = anoAtual-ano-1
        if mes < mesAtual:
            idade = anoAtual-ano
        if mes == mesAtual:
            if dia >= diaAtual:
                idade = anoAtual-ano-1
            if dia < diaAtual:
                idade = anoAtual-ano

        somadiferenciacao=0
        perguntasdiferenciacao=["S05","S06","S15","S16","S24","S25"]
        seletiva = Seletiva.objects.filter(paciente_id=paciente.id,anamnesia_id=anamnesia.id)
        for item in seletiva:
            resposta = RespostaSeletiva.objects.get(id=item.resposta_id)
            pergunta = PerguntaSeletiva.objects.get(id=resposta.pergunta_id)

            if pergunta.numero in perguntasdiferenciacao:
                if idade >=0 and idade <=3:
                    if resposta.nivel0 != 0:
                        somadiferenciacao=somadiferenciacao+resposta.nivel0
                        if resposta.nivel0 <=1:
                            texto="pdfdiferenciacao"
                if idade >=4 and idade <=7:
                    if resposta.nivel1 != 0:
                        somadiferenciacao=somadiferenciacao+resposta.nivel1
                        if resposta.nivel1 <=1:
                            texto="pdfdiferenciacao"
                if idade >=8 and idade <=12:
                    if resposta.nivel2 != 0:
                        somadiferenciacao=somadiferenciacao+resposta.nivel2
                        if resposta.nivel2 <=1:
                            texto="pdfdiferenciacao"
                if idade >=13 and idade <=19:
                    if resposta.nivel3 != 0:
                        somadiferenciacao=somadiferenciacao+resposta.nivel3
                        if resposta.nivel3 <=1:
                            texto="pdfdiferenciacao"
                if idade >=20 and idade <=24:
                    if resposta.nivel4 != 0:
                        somadiferenciacao=somadiferenciacao+resposta.nivel4
                        if resposta.nivel4 <=1:
                            texto="pdfdiferenciacao"
                if idade >=25 and idade <=32:
                    if resposta.nivel5 != 0:
                        somadiferenciacao=somadiferenciacao+resposta.nivel5
                        if resposta.nivel5 <=1:
                            texto="pdfdiferenciacao"
                if idade >=33:
                    if resposta.nivel6 != 0:
                        somadiferenciacao=somadiferenciacao+resposta.nivel6
                        if resposta.nivel6 <=1:
                            texto="pdfdiferenciacao"
        if somadiferenciacao/len(perguntasdiferenciacao) < 3:
            texto="pdfdiferenciacao"

        return texto

    def tarefaAutonomia(self):
        texto=""
        if 'paciente_id' in self.kwargs:
            paciente_id = self.kwargs['paciente_id']
        if 'analise_id' in self.kwargs:
            analise_id = self.kwargs['analise_id']
        paciente= Paciente.objects.get(usuario_id=paciente_id)
        anamnesia = Anamnesia.objects.get(id=analise_id)

        nascimento=str(paciente.nascimento)
        ano = int(nascimento.split("-")[0])
        mes=int(nascimento.split("-")[1])
        dia=int(nascimento.split("-")[2])
        atual=datetime.now()
        anoAtual=atual.year
        mesAtual=atual.month
        diaAtual=atual.day

        if mes > mesAtual:
            idade = anoAtual-ano-1
        if mes < mesAtual:
            idade = anoAtual-ano
        if mes == mesAtual:
            if dia >= diaAtual:
                idade = anoAtual-ano-1
            if dia < diaAtual:
                idade = anoAtual-ano

        somaautonomia=0
        perguntasautonomia=["S01","S07","S08","S09","S10","S11","S12","S13","S28"]

        seletiva = Seletiva.objects.filter(paciente_id=paciente.id,anamnesia_id=anamnesia.id)
        for item in seletiva:
            resposta = RespostaSeletiva.objects.get(id=item.resposta_id)
            pergunta = PerguntaSeletiva.objects.get(id=resposta.pergunta_id)

            if pergunta.numero in perguntasautonomia:
                if idade >=0 and idade <=3:
                    if resposta.nivel0 != 0:
                        somaautonomia=somaautonomia+resposta.nivel0
                        if resposta.nivel0 <=1:
                            texto="pdfautonomia"
                if idade >=4 and idade <=7:
                    if resposta.nivel1 != 0:
                        somaautonomia=somaautonomia+resposta.nivel1
                        if resposta.nivel1 <=1:
                            texto="pdfautonomia"
                if idade >=8 and idade <=12:
                    if resposta.nivel2 != 0:
                        somaautonomia=somaautonomia+resposta.nivel2
                        if resposta.nivel2 <=1:
                            texto="pdfautonomia"
                if idade >=13 and idade <=19:
                    if resposta.nivel3 != 0:
                        somaautonomia=somaautonomia+resposta.nivel3
                        if resposta.nivel3 <=1:
                            texto="pdfautonomia"
                if idade >=20 and idade <=24:
                    if resposta.nivel4 != 0:
                        somaautonomia=somaautonomia+resposta.nivel4
                        if resposta.nivel4 <=1:
                            texto="pdfautonomia"
                if idade >=25 and idade <=32:
                    if resposta.nivel5 != 0:
                        somaautonomia=somaautonomia+resposta.nivel5
                        if resposta.nivel5 <=1:
                            texto="pdfautonomia"
                if idade >=33:
                    if resposta.nivel6 != 0:
                        somaautonomia=somaautonomia+resposta.nivel6
                        if resposta.nivel6 <=1:
                            texto="pdfautonomia"

        if somaautonomia/len(perguntasautonomia) < 3:
            texto="pdfautonomia"

        return texto

    def tarefaAssertividade(self):
        texto=""
        if 'paciente_id' in self.kwargs:
            paciente_id = self.kwargs['paciente_id']
        if 'analise_id' in self.kwargs:
            analise_id = self.kwargs['analise_id']
        paciente= Paciente.objects.get(usuario_id=paciente_id)
        anamnesia = Anamnesia.objects.get(id=analise_id)

        nascimento=str(paciente.nascimento)
        ano = int(nascimento.split("-")[0])
        mes=int(nascimento.split("-")[1])
        dia=int(nascimento.split("-")[2])
        atual=datetime.now()
        anoAtual=atual.year
        mesAtual=atual.month
        diaAtual=atual.day

        if mes > mesAtual:
            idade = anoAtual-ano-1
        if mes < mesAtual:
            idade = anoAtual-ano
        if mes == mesAtual:
            if dia >= diaAtual:
                idade = anoAtual-ano-1
            if dia < diaAtual:
                idade = anoAtual-ano

        somaassertividade=0
        perguntasassertiva=["S14","S18","S20","S21","S30","S31","S32","S33",]


        seletiva = Seletiva.objects.filter(paciente_id=paciente.id,anamnesia_id=anamnesia.id)
        for item in seletiva:
            resposta = RespostaSeletiva.objects.get(id=item.resposta_id)
            pergunta = PerguntaSeletiva.objects.get(id=resposta.pergunta_id)

            if pergunta.numero in perguntasassertiva:
                if idade >=0 and idade <=3:
                    if resposta.nivel0 != 0:
                        somaassertividade=somaassertividade+resposta.nivel0
                        if resposta.nivel0 <=1:
                            texto="pdfassertividade"
                if idade >=4 and idade <=7:
                    if resposta.nivel1 != 0:
                        somaassertividade=somaassertividade+resposta.nivel1
                        if resposta.nivel1 <=1:
                            texto="pdfassertividade"
                if idade >=8 and idade <=12:
                    if resposta.nivel2 != 0:
                        somaassertividade=somaassertividade+resposta.nivel2
                        if resposta.nivel2 <=1:
                            texto="pdfassertividade"
                if idade >=13 and idade <=19:
                    if resposta.nivel3 != 0:
                        somaassertividade=somaassertividade+resposta.nivel3
                        if resposta.nivel3 <=1:
                            texto="pdfassertividade"
                if idade >=20 and idade <=24:
                    if resposta.nivel4 != 0:
                        somaassertividade=somaassertividade+resposta.nivel4
                        if resposta.nivel4 <=1:
                            texto="pdfassertividade"
                if idade >=25 and idade <=32:
                    if resposta.nivel5 != 0:
                        somaassertividade=somaassertividade+resposta.nivel5
                        if resposta.nivel5 <=1:
                            texto="pdfassertividade"
                if idade >=33:
                    if resposta.nivel6 != 0:
                        somaassertividade=somaassertividade+resposta.nivel6
                        if resposta.nivel6 <=1:
                            texto="pdfassertividade"
        if somaassertividade/len(perguntasassertiva) < 3:
            texto="pdfassertividade"

        return texto

    def tarefaAutoestima(self):
        texto=""
        if 'paciente_id' in self.kwargs:
            paciente_id = self.kwargs['paciente_id']
        if 'analise_id' in self.kwargs:
            analise_id = self.kwargs['analise_id']
        paciente= Paciente.objects.get(usuario_id=paciente_id)
        anamnesia = Anamnesia.objects.get(id=analise_id)

        nascimento=str(paciente.nascimento)
        ano = int(nascimento.split("-")[0])
        mes=int(nascimento.split("-")[1])
        dia=int(nascimento.split("-")[2])
        atual=datetime.now()
        anoAtual=atual.year
        mesAtual=atual.month
        diaAtual=atual.day

        if mes > mesAtual:
            idade = anoAtual-ano-1
        if mes < mesAtual:
            idade = anoAtual-ano
        if mes == mesAtual:
            if dia >= diaAtual:
                idade = anoAtual-ano-1
            if dia < diaAtual:
                idade = anoAtual-ano

        somaautoestima=0
        perguntasautoEstima=["S02","S17","S19","S22","S23","S26","S27","S29"]

        seletiva = Seletiva.objects.filter(paciente_id=paciente.id,anamnesia_id=anamnesia.id)
        for item in seletiva:
            resposta = RespostaSeletiva.objects.get(id=item.resposta_id)
            pergunta = PerguntaSeletiva.objects.get(id=resposta.pergunta_id)
            if pergunta.numero in perguntasautoEstima:
                if idade >=0 and idade <=3:
                    if resposta.nivel0 != 0:
                        somaautoestima=somaautoestima+resposta.nivel0
                        if resposta.nivel0 <=1:
                            texto="pdfautoestima"
                if idade >=4 and idade <=7:
                    if resposta.nivel1 != 0:
                        somaautoestima=somaautoestima+resposta.nivel1
                        if resposta.nivel1 <=1:
                            texto="pdfautoestima"
                if idade >=8 and idade <=12:
                    if resposta.nivel2 != 0:
                        somaautoestima=somaautoestima+resposta.nivel2
                        if resposta.nivel2 <=1:
                            texto="pdfautoestima"
                if idade >=13 and idade <=19:
                    if resposta.nivel3 != 0:
                        somaautoestima=somaautoestima+resposta.nivel3
                        if resposta.nivel3 <=1:
                            texto="pdfautoestima"
                if idade >=20 and idade <=24:
                    if resposta.nivel4 != 0:
                        somaautoestima=somaautoestima+resposta.nivel4
                        if resposta.nivel4 <=1:
                            texto="pdfautoestima"
                if idade >=25 and idade <=32:
                    if resposta.nivel5 != 0:
                        somaautoestima=somaautoestima+resposta.nivel5
                        if resposta.nivel5 <=1:
                            texto="pdfautoestima"
                if idade >=33:
                    if resposta.nivel6 != 0:
                        somaautoestima=somaautoestima+resposta.nivel6
                        if resposta.nivel6 <=1:
                            texto="pdfautoestima"

        if somaautoestima/len(perguntasautoEstima) < 3:
            texto="pdfautoestima"

        return texto

class RecomendacaoInterventiva(TemplateView):

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(RecomendacaoInterventiva, self).dispatch(*args, **kwargs)

    def anamnesia(self):
        if 'paciente_id' in self.kwargs:
            paciente_id = self.kwargs['paciente_id']
        paciente = Paciente.objects.get(usuario_id=paciente_id)
        if 'analise_id' in self.kwargs:
            analise_id = self.kwargs['analise_id']
        anamnesia = Anamnesia.objects.get(id=analise_id)
        main(paciente_id,analise_id)
        return anamnesia

    def paciente(self):
        if 'paciente_id' in self.kwargs:
            paciente_id = self.kwargs['paciente_id']
        paciente = Paciente.objects.get(usuario_id=paciente_id)
        return paciente



