import datetime
import math
from datetime import datetime, timedelta
import json
from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.models import User, Group
from .forms import ConsultarAreaAfetiva,EdicaoPsicologo,\
    PerguntasAreaAfetiva,\
    RelacionamentoAvosMaternos, RelacionamentoAvoMaternoAntes, RelacionamentoAvoMaternaAntes, RelacionamentoAvosMaternosDepois,\
    RelacionamentoAvosPaternos, RelacionamentoAvoPaternoAntes, RelacionamentoAvoPaternaAntes, RelacionamentoAvosPaternosDepois,\
    RelacionamentoPais, RelacionamentoPaiAntes,RelacionamentoMaeAntes,RelacionamentoPaisDepois, RelacionamentoPaciente,\
    RelacionamentoPacienteAntes, RelacionamentoConjugeAntes, RelacionamentoPacienteDepois,GrauDeIndeferenciacao,\
    PerguntasSeletivas, ConsultarPerguntasSeletivas,\
    PerguntasInterventivas, ConsultarPerguntasInterventivas

from .models import Paciente, Chave,Estado,Municipio, User,Familia, Psicologo, AreaAfetiva, Anamnesia, PerguntaAreaAfetiva,RespostaAreaAfetiva,\
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
from django.urls import reverse, reverse_lazy
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.template import loader
from django.utils import timezone
from django.views import generic
from django.views.decorators.debug import sensitive_post_parameters
import json as simplejson
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
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from reportlab.lib.units import cm, mm, inch, pica
from reportlab.lib.pagesizes import letter

# Create your views here.

#Views do Psicólogo
def PsicologoAdministracao(request):
    return render(request, 'projetofinal/psicologo/administracao.html', {})

def LoginPsicologo(request):
    username = password = ''
    state="please log in"
    if request.POST:
        username = request.POST['username'].lower().strip()
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active and user.groups.filter(name='psicologo').exists():
                login(request, user)
                state = "You're successfully logged in!"
                return HttpResponseRedirect('home')
            else:
                state = 1
        else:
            state = 2
    return render(request, 'projetofinal/psicologo/login.html', {'state':state, 'username': username})

class CadastroPsicologoWizard(SessionWizardView):
    template_name = "projetofinal/psicologo/cadastro.html"

    def done(self, form_list, form_dict, **kwargs):
        form_data= [form.cleaned_data for form in form_list]
        user = User()
        user.username = form_data[0]['username']
        user.set_password(form_data[0]['password1'])
        user.username = form_data[0]['username']
        user.email = form_data[1]['email']
        user.first_name = form_data[1]['nome']
        user.save()
        #code= form_data[0]['code']
        #chave= Chave.objects.get(chave = code)
        #chave.padrao = "usada"
        #chave.save()
        group = Group.objects.get_or_create(name="psicologo")
        group = Group.objects.get(name="psicologo")
        user.groups.add(group)
        psicologo = Psicologo()
        psicologo.usuario = user
        psicologo.email = form_data[1]['email']
        psicologo.nome = form_data[1]['nome']
        estado= form_data[1]['estado']
        estado = Estado.objects.get(estado=estado)
        psicologo.estado=estado
        municipio= form_data[1]['municipio']
        municipio = Municipio.objects.get(municipio=municipio)
        psicologo.municipio=municipio
        psicologo.endereco = form_data[1]['endereco']
        psicologo.numero = form_data[1]['numero']
        psicologo.complemento = form_data[1]['complemento']
        psicologo.bairro = form_data[1]['bairro']
        psicologo.telefone = form_data[1]['telefone']
        psicologo.celular = form_data[1]['celular']
        psicologo.crp = form_data[1]['crp']
        psicologo.save()
        return redirect(CadastroPsicologoRealizado)

def CadastroPsicologoRealizado(request):
    return render(request, 'projetofinal/psicologo/cadastrado.html', {})

@login_required()
def PsicologoHome(request):

    paciente = Paciente.objects.all()
    return render(request, 'projetofinal/psicologo/home.html', {'pacientes':paciente})

class EditarCadastroPsicologo(SessionWizardView):
    template_name = "projetofinal/psicologo/editar.html"
    form_list = [EdicaoPsicologo]

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(EditarCadastroPsicologo, self).dispatch(*args, **kwargs)

    def get_form(self, step=None, data=None, files=None):

        if 'psicologo_id' in self.kwargs:
                psicologo_id = self.kwargs['psicologo_id']
                try:
                    psicologo = Psicologo.objects.get(usuario_id=psicologo_id)
                except Paciente.DoesNotExist:
                    raise Http404("Psicologo não existe")
        # determine the step if not given
        if step is None:
            step = self.steps.current

        if step == "0":
            form = EdicaoPsicologo(psicologo_id=psicologo_id, data=data)
            return form



    def done(self, form_list, form_dict, **kwargs):
        psicologo_id = self.kwargs['psicologo_id']
        psicologo = Psicologo.objects.get(usuario_id=psicologo_id)
        form_data= [form.cleaned_data for form in form_list]
        psicologo.nome = form_data[0]['nome']
        psicologo.email = form_data[0]['email']
        estado= form_data[0]['estado']
        estado = Estado.objects.get(estado=estado)
        psicologo.estado=estado
        municipio= form_data[0]['municipio']
        municipio = Municipio.objects.get(municipio=municipio)
        psicologo.municipio=municipio
        psicologo.endereco = form_data[0]['endereco']
        psicologo.numero = form_data[0]['numero']
        psicologo.complemento = form_data[0]['complemento']
        psicologo.bairro = form_data[0]['bairro']
        psicologo.telefone = form_data[0]['telefone']
        psicologo.celular = form_data[0]['celular']
        psicologo.crp = form_data[0]['crp']
        psicologo.save()
        return HttpResponseRedirect('/psicologo/editado/'+psicologo_id)

class EdicaoRealizadaPsicologo(TemplateView):
    template_name = "projetofinal/psicologo/editado.html"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(EdicaoRealizadaPsicologo, self).dispatch(*args, **kwargs)

class PsicologoPaciente(TemplateView):
    template_name="projetofinal/psicologo/paciente/home.html"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(PsicologoPaciente, self).dispatch(*args, **kwargs)

    def paciente(self):
        if 'paciente_id' in self.kwargs:
            paciente_id = self.kwargs['paciente_id']
            try:
                paciente = Paciente.objects.get(usuario_id=paciente_id)
            except Paciente.DoesNotExist:
                raise Http404("Paciente não existe")
        return paciente_id

def LogoutPsicologo(request):
    logout(request)
    return render(request, 'projetofinal/psicologo/administracao.html', {})

class AnalisePaciente(TemplateView):
    template_name="projetofinal/psicologo/paciente/analise.html"


    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(AnalisePaciente, self).dispatch(*args, **kwargs)

    def paciente(self):
        if 'paciente_id' in self.kwargs:
            paciente_id = self.kwargs['paciente_id']
            try:
                paciente = Paciente.objects.get(usuario_id=paciente_id)
            except Paciente.DoesNotExist:
                raise Http404("Paciente não existe")
        return paciente_id

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

    def anamnesia(self):
        if 'paciente_id' in self.kwargs:
            paciente_id = self.kwargs['paciente_id']
        paciente = Paciente.objects.get(usuario_id=paciente_id)
        anamnesia = Anamnesia.objects.filter(paciente_id=paciente.id)
        return anamnesia

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

    def pacienteGrafico(self):
        if 'paciente_id' in self.kwargs:
            paciente_id = self.kwargs['paciente_id']
        paciente = Paciente.objects.get(usuario_id=paciente_id)
        dados = { 'paciente': paciente.nome
        }

        paciente = simplejson.dumps(dados)
        return paciente

class ConsultandoAnalisePaciente(SessionWizardView):
    template_name = "projetofinal/psicologo/paciente/consultando.html"
    form_list = [ConsultarAreaAfetiva]

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ConsultandoAnalisePaciente, self).dispatch(*args, **kwargs)

    def paciente(self):
        if 'paciente_id' in self.kwargs:
            paciente_id = self.kwargs['paciente_id']
            try:
                paciente = Paciente.objects.get(usuario_id=paciente_id)
            except Paciente.DoesNotExist:
                raise Http404("Paciente não existe")
        return paciente

    def get_form(self, step=None, data=None, files=None):
        form = super(ConsultandoAnalisePaciente, self).get_form(step, data, files)
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

class GenogramaPaciente(TemplateView):
    template_name="projetofinal/psicologo/paciente/genograma.html"


    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(GenogramaPaciente, self).dispatch(*args, **kwargs)

    def paciente(self):
        if 'paciente_id' in self.kwargs:
            paciente_id = self.kwargs['paciente_id']
            try:
                paciente = Paciente.objects.get(usuario_id=paciente_id)
            except Paciente.DoesNotExist:
                raise Http404("Paciente não existe")
        return paciente_id

    def anamnesia(self):
        if 'paciente_id' in self.kwargs:
            paciente_id = self.kwargs['paciente_id']
        paciente = Paciente.objects.get(usuario_id=paciente_id)
        anamnesia = Anamnesia.objects.filter(paciente_id=paciente.id,padrao__isnull= False)
        for analise in anamnesia:
            analise_id = str(analise.id)
            main(paciente_id,analise_id)
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
        anamnesia = Anamnesia.objects.filter(paciente_id=paciente.id,padrao__isnull= False)
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
        anamnesia = Anamnesia.objects.filter(paciente_id=paciente.id,padrao__isnull= False)
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

    def pacienteGrafico(self):
        if 'paciente_id' in self.kwargs:
            paciente_id = self.kwargs['paciente_id']
        paciente = Paciente.objects.get(usuario_id=paciente_id)
        dados = { 'paciente': paciente.nome
        }

        paciente = simplejson.dumps(dados)
        return paciente

class RelatorioPaciente(TemplateView):
    template_name="projetofinal/psicologo/paciente/relatorio.html"


    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(RelatorioPaciente, self).dispatch(*args, **kwargs)

    def paciente(self):
        if 'paciente_id' in self.kwargs:
            paciente_id = self.kwargs['paciente_id']
            try:
                paciente = Paciente.objects.get(usuario_id=paciente_id)
            except Paciente.DoesNotExist:
                raise Http404("Paciente não existe")
        return paciente_id

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
        anamnesia = Anamnesia.objects.filter(paciente_id=paciente.id,padrao__isnull= False)
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
        anamnesia = Anamnesia.objects.filter(paciente_id=paciente.id,padrao__isnull= False)
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

    def pacienteGrafico(self):
        if 'paciente_id' in self.kwargs:
            paciente_id = self.kwargs['paciente_id']
        paciente = Paciente.objects.get(usuario_id=paciente_id)
        dados = { 'paciente': paciente.nome
        }

        paciente = simplejson.dumps(dados)
        return paciente

def Relatorio(request,paciente_id,analise_id):
    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="Relatorio.pdf"'

    # Create the PDF object, using the response object as its "file."
    p = canvas.Canvas(response)

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    paciente=Paciente.objects.get(usuario_id=paciente_id)

    #Área Afetiva
    if AreaAfetiva.objects.filter(paciente_id=paciente.id,anamnesia_id=analise_id).exists():
        areaafetivap=PerguntaAreaAfetiva.objects.all()
        lista_resposta={}
        respostas=AreaAfetiva.objects.filter(paciente_id=paciente.id,anamnesia_id=analise_id)
        for item in respostas:
            pergunta=RespostaAreaAfetiva.objects.get(id=item.resposta_id)
            pergunta_id=pergunta.pergunta_id
            resposta=RespostaAreaAfetiva.objects.get(id=item.resposta_id)
            resposta=resposta.resposta
            lista_resposta[pergunta_id]=resposta

        p.setFont('Helvetica', 16)
        p.setFillColorRGB(0,0,1)
        p.drawString(250,800,paciente.nome)
        p.drawString(250,770,"Área Afetiva")

        alturap=740

        for item,value in zip(areaafetivap,lista_resposta):
            if len(item.pergunta) >100:
                p.setFillColorRGB(0,0,0)
                p.setFont("Helvetica", 12)
                string=item.pergunta
                depois=string[80:len(string)].split(" ",1)[1]
                antes=string[80:len(string)].split(" ",1)[0]
                p.drawString(10,alturap,item.pergunta[0:80]+antes)
                p.drawString(10,alturap-15,depois)
                p.setFillColorRGB(1,0,0)
                p.drawString(10,alturap-40,lista_resposta[value])

            else:
                p.setFillColorRGB(0,0,0)
                p.setFont("Helvetica", 12)
                p.drawString(10,alturap,item.pergunta)
                p.setFillColorRGB(1,0,0)
                p.drawString(10,alturap-25,lista_resposta[value])

            alturap = alturap -70

            if alturap <=60:
                p.showPage()
                alturap=740
                p.setFillColorRGB(0,0,1)
                p.setFont("Helvetica", 16)
                p.drawString(250,800,paciente.nome)
                p.drawString(250,770,"Área Afetiva")

    #Recomendacao Area Afetiva
    anamnesia = Anamnesia.objects.filter(id=analise_id)
    for analise in anamnesia:
        area = AreaAfetiva.objects.filter(anamnesia_id=analise.id).order_by('resposta_id')
        A = [0]
        for respostas in area:
            resposta = RespostaAreaAfetiva.objects.get(id=respostas.resposta_id)
            A.append(resposta.valor)
        afetivoRelacional = ((A[1] + A[2] + A[4] + A[6] + A[9] + A[13] + A[15] + A[17] + A[19] + A[20] + A[21] + A[22] +
                              A[23] + A[25] + A[28]) / 15)
        produtividade = ((A[5] + A[16] + A[20] + A[22] + A[23]) / 5)
        organico = ((A[7] + A[12] + A[14] + A[27] + A[29]) / 5)
        espiritual = ((A[3] + A[11] + A[18] + A[24] + A[26]) / 5)
        socioCultural = ((A[8] + A[10] + A[20] + A[22] + A[23]) / 5)

    texto = ""
    if afetivoRelacional >= 3 and afetivoRelacional <= 4:
        complementox = Recomendacao.objects.get(nome="complementox", intervalo="Máximo")
        complementoy = Recomendacao.objects.get(nome="complementoy", intervalo="Máximo")
    if afetivoRelacional >= 1.5 and afetivoRelacional < 3:
        complementox = Recomendacao.objects.get(nome="complementox", intervalo="Médio")
        complementoy = Recomendacao.objects.get(nome="complementoy", intervalo="Médio")
    if afetivoRelacional >= 0 and afetivoRelacional < 1.5:
        complementox = Recomendacao.objects.get(nome="complementox", intervalo="Mínimo")
        complementoy = Recomendacao.objects.get(nome="complementoy", intervalo="Mínimo")
    if produtividade >= 3 and produtividade <= 4:
        PRODUTIVIDADE = Recomendacao.objects.get(nome="produtividade", intervalo="Máximo")
    if produtividade >= 1.5 and produtividade < 3:
        PRODUTIVIDADE = Recomendacao.objects.get(nome="produtividade", intervalo="Médio")
    if produtividade >= 0 and produtividade < 1.5:
        PRODUTIVIDADE = Recomendacao.objects.get(nome="produtividade", intervalo="Mínimo")
    if organico >= 3 and organico <= 4:
        ORGANICO = Recomendacao.objects.get(nome="organico", intervalo="Máximo")
    if organico >= 1.5 and organico < 3:
        ORGANICO = Recomendacao.objects.get(nome="organico", intervalo="Médio")
    if organico >= 0 and organico < 1.5:
        ORGANICO = Recomendacao.objects.get(nome="organico", intervalo="Mínimo")
    if espiritual >= 3 and espiritual <= 4:
        ESPIRITUAL = Recomendacao.objects.get(nome="espiritual", intervalo="Máximo")
    if espiritual >= 1.5 and espiritual < 3:
        ESPIRITUAL = Recomendacao.objects.get(nome="espiritual", intervalo="Médio")
    if espiritual >= 0 and espiritual < 1.5:
        ESPIRITUAL = Recomendacao.objects.get(nome="espiritual", intervalo="Mínimo")
    if socioCultural >= 3 and socioCultural <= 4:
        SOCIOCULTURAL = Recomendacao.objects.get(nome="sociocultural", intervalo="Máximo")
    if socioCultural >= 1.5 and socioCultural < 3:
        SOCIOCULTURAL = Recomendacao.objects.get(nome="sociocultural", intervalo="Médio")
    if socioCultural >= 0 and socioCultural < 1.5:
        SOCIOCULTURAL = Recomendacao.objects.get(nome="sociocultural", intervalo="Mínimo")

    lista = [(organico, "a"), (produtividade, "b"), (socioCultural, "c"), (espiritual, "d")]
    minimo = min(lista, key=lambda x: x[0])
    if minimo[0] == produtividade:
        area = PRODUTIVIDADE.texto
    if minimo[0] == organico:
        area = ORGANICO.texto
    if minimo[0] == espiritual:
        area = ESPIRITUAL.texto
    if minimo[0] == socioCultural:
        area = SOCIOCULTURAL.texto

    parte1 = Recomendacao.objects.get(nome="afetivorelacional", intervalo="parte1")
    parte2 = Recomendacao.objects.get(nome="afetivorelacional", intervalo="parte2")
    parte3 = Recomendacao.objects.get(nome="afetivorelacional", intervalo="parte3")
    AFETIVORELACIONAL = parte1.texto + complementox.texto + parte2.texto + complementoy.texto + parte3.texto
    texto = AFETIVORELACIONAL + area

    p.showPage()
    p.setFont('Helvetica', 16)
    p.setFillColorRGB(0, 0, 1)
    p.drawString(250, 800, paciente.nome)
    p.drawString(190, 770, "Recomendaçao Área Afetiva")
    p.drawString(220, 740, "(Valores entre 0 e 4)")

    alturap = 700
    p.setFillColorRGB(0, 0, 0)
    p.setFont("Helvetica", 12)
    p.drawString(10, alturap,"Afetivo-Relacional: "+ str("%.2f" % afetivoRelacional))
    alturap=alturap-20
    p.drawString(10, alturap,"Produtividade: "+ str("%.2f" % produtividade))
    alturap=alturap-20
    p.drawString(10, alturap,"Orgânico: "+ str("%.2f" % organico))
    alturap=alturap-20
    p.drawString(10, alturap,"Socio-Cultural: "+ str("%.2f" % socioCultural))
    alturap=alturap-20
    p.drawString(10, alturap,"Espiritual: "+ str("%.2f" % espiritual))
    alturap=alturap-20
    if len(texto) > 100:
        string = texto
        depois = string[80:len(string)].split(" ", 1)[1]
        antes = string[80:len(string)].split(" ", 1)[0]
        alturap = alturap - 40
        p.setFillColorRGB(0, 0, 0)
        p.setFont("Helvetica", 12)
        p.drawString(10, alturap, string[0:80] + antes)
        while len(depois) > 100:
            string = depois
            depois = string[80:len(string)].split(" ", 1)[1]
            antes = string[80:len(string)].split(" ", 1)[0]
            p.setFillColorRGB(0, 0, 0)
            p.setFont("Helvetica", 12)
            p.drawString(10, alturap - 15, string[0:80] + antes)
            alturap = alturap - 15
            if alturap <= 60:
                p.showPage()
                alturap = 740
                p.setFillColorRGB(0, 0, 1)
                p.setFont("Helvetica", 16)
                p.drawString(250, 800, paciente.nome)
                p.drawString(250, 770, "Recomendaçao Área Afetiva")
        p.setFillColorRGB(0, 0, 0)
        p.setFont("Helvetica", 12)
        p.drawString(10, alturap - 15, depois)

    else:
        p.setFillColorRGB(0, 0, 0)
        p.drawString(10, alturap - 40, texto)

    #Relacionamento

    #Relacionamento Avós Maternos
    if Relacionamento.objects.filter(anamnesia_id=analise_id,paciente_id=paciente.id,parente="AvoMaterno").exists():

        p.showPage()
        p.setFont("Helvetica", 16)
        p.setFillColorRGB(0,0,1)
        p.drawString(250,800,paciente.nome)
        p.drawString(230,770,"Relacionamentos")

        alturap=740
        p.setFillColorRGB(0,0,0)
        p.setFont("Helvetica", 12)
        p.drawString(10,alturap,"Qual é/era o relacionamento dos seus avós maternos:")
        p.drawString(10,alturap-70,"Seus avós maternos tiveram quantos filhos homens?")
        p.drawString(10,alturap-140,"Seus avós maternos tiveram quantas filhas mulheres?")
        p.drawString(10,alturap-210,"Seu avô materno era separado/divorciado quando se relacionava com sua avó?")
        p.drawString(10,alturap-280,"Sua avó materna era separada/divorciada quando se relacionava com seu avô?")

        avomaterno=Relacionamento.objects.get(paciente_id=paciente.id,anamnesia_id=analise_id,parente="AvoMaterno")
        avomaterna=Relacionamento.objects.get(paciente_id=paciente.id,anamnesia_id=analise_id,parente="AvoMaterna")
        p.setFillColorRGB(1,0,0)
        p.setFont("Helvetica", 12)
        p.drawString(10,alturap-40,avomaterno.relacao)
        p.drawString(10,alturap-110,str(avomaterno.filhos))
        p.drawString(10,alturap-180,str(avomaterno.filhas))
        p.drawString(10,alturap-250,avomaterno.relacaoAntes)
        p.drawString(10,alturap-320,avomaterna.relacaoAntes)
        if avomaterno.relacaoAntes == "Sim" and avomaterno.filhosAntes != None:
            p.setFillColorRGB(0,0,0)
            p.drawString(10,alturap-350,"Seu avô materno teve quantos filhos homens no relacionamento anterior à relação com sua avó?")
            p.drawString(10,alturap-420,"Seu avô materno teve quantas filhas mulheres no relacionamento anterior à relação com sua avó?")
            p.setFillColorRGB(1,0,0)
            p.drawString(10,alturap-390,str(avomaterno.filhosAntes))
            p.drawString(10,alturap-460,str(avomaterno.filhasAntes))

            if avomaterna.relacaoAntes == "Sim" and avomaterna.filhosAntes != None:
                p.setFillColorRGB(0,0,0)
                p.drawString(10,alturap-490,"Sua avó materna teve quantos filhos homens no relacionamento anterior à relação com seu avô?")
                p.drawString(10,alturap-560,"Sua avó materna teve quantas filhas mulheres no relacionamento anterior à relação com seu avô?")
                p.setFillColorRGB(1,0,0)
                p.drawString(10,alturap-530,str(avomaterna.filhosAntes))
                p.drawString(10,alturap-600,str(avomaterna.filhasAntes))

        else:
            if avomaterna.relacaoAntes == "Sim" and avomaterna.filhosAntes != None:
                p.setFillColorRGB(0,0,0)
                p.drawString(10,alturap-350,"Sua avó materna teve quantos filhos homens no relacionamento anterior à relação com seu avô?")
                p.drawString(10,alturap-420,"Sua avó materna teve quantas filhas mulheres no relacionamento anterior à relação com seu avô?")
                p.setFillColorRGB(1,0,0)
                p.drawString(10,alturap-390,str(avomaterna.filhosAntes))
                p.drawString(10,alturap-460,str(avomaterna.filhasAntes))

        if (avomaterno.relacaoAntes=="Sim" or avomaterna.relacaoAntes=="Sim")and\
                (avomaterno.relacao == "Separados" or avomaterno.relacao == "Divorciados")and\
                (avomaterno.filhosDepois !=None):
            p.showPage()
            p.setFont("Helvetica", 16)
            p.setFillColorRGB(0,0,1)
            p.drawString(250,800,paciente.nome)
            p.drawString(230,770,"Relacionamentos")
            p.setFillColorRGB(0,0,0)
            p.setFont("Helvetica", 12)
            p.drawString(10,alturap,"Seu avô materno teve quantos filhos homens no relacionamento posterior à relação com sua avó?")
            p.drawString(10,alturap-70,"Seu avô materno teve quantas filhas mulheres no relacionamento posterior à relação com sua avó?")
            p.setFillColorRGB(1,0,0)
            p.drawString(10,alturap-40,str(avomaterno.filhosDepois))
            p.drawString(10,alturap-110,str(avomaterno.filhasDepois))
            p.setFillColorRGB(0,0,0)
            p.drawString(10,alturap-140,"Sua avó materna teve quantos filhos homens no relacionamento posterior à relação com seu avô?")
            p.drawString(10,alturap-210,"Sua avó materna teve quantas filhas mulheres no relacionamento posterior à relação com seu avô?")
            p.setFillColorRGB(1,0,0)
            p.drawString(10,alturap-180,str(avomaterna.filhosDepois))
            p.drawString(10,alturap-250,str(avomaterna.filhasDepois))

        if (avomaterno.relacaoAntes=="Não" and avomaterna.relacaoAntes=="Não")and\
                (avomaterno.relacao == "Separados" or avomaterno.relacao == "Divorciados")and\
                 (avomaterno.filhosDepois !=None):
            p.showPage()
            p.setFont("Helvetica", 16)
            p.setFillColorRGB(0,0,1)
            p.drawString(250,800,paciente.nome)
            p.drawString(230,770,"Relacionamentos")
            p.setFillColorRGB(0,0,0)
            p.setFont("Helvetica", 12)
            p.drawString(10,alturap-350,"Seu avô materno teve quantos filhos homens no relacionamento posterior à relação com sua avó?")
            p.drawString(10,alturap-420,"Seu avô materno teve quantas filhas mulheres no relacionamento posterior à relação com sua avó?")
            p.setFillColorRGB(1,0,0)
            p.drawString(10,alturap-390,str(avomaterno.filhosDepois))
            p.drawString(10,alturap-460,str(avomaterno.filhasDepois))
            p.setFillColorRGB(0,0,0)
            p.drawString(10,alturap-490,"Sua avó materna teve quantos filhos homens no relacionamento posterior à relação com seu avô?")
            p.drawString(10,alturap-560,"Sua avó materna teve quantas filhas mulheres no relacionamento posterior à relação com seu avô?")
            p.setFillColorRGB(1,0,0)
            p.drawString(10,alturap-530,str(avomaterna.filhosDepois))
            p.drawString(10,alturap-600,str(avomaterna.filhasDepois))

    #Relacionamento Avós Paternos
    if Relacionamento.objects.filter(anamnesia_id=analise_id,paciente_id=paciente.id,parente="AvoPaterno").exists():

        p.showPage()
        p.setFont("Helvetica", 16)
        p.setFillColorRGB(0,0,1)
        p.drawString(250,800,paciente.nome)
        p.drawString(230,770,"Relacionamentos")

        alturap=740
        p.setFillColorRGB(0,0,0)
        p.setFont("Helvetica", 12)
        p.drawString(10,alturap,"Qual é/era o relacionamento dos seus avós paternos:")
        p.drawString(10,alturap-70,"Seus avós paternos tiveram quantos filhos homens?")
        p.drawString(10,alturap-140,"Seus avós paternos tiveram quantas filhas mulheres?")
        p.drawString(10,alturap-210,"Seu avô paterno era separado/divorciado quando se relacionava com sua avó?")
        p.drawString(10,alturap-280,"Sua avó paterna era separada/divorciada quando se relacionava com seu avô?")

        avopaterno=Relacionamento.objects.get(paciente_id=paciente.id,anamnesia_id=analise_id,parente="AvoPaterno")
        avopaterna=Relacionamento.objects.get(paciente_id=paciente.id,anamnesia_id=analise_id,parente="AvoPaterna")
        p.setFillColorRGB(1,0,0)
        p.setFont("Helvetica", 12)
        p.drawString(10,alturap-40,avopaterno.relacao)
        p.drawString(10,alturap-110,str(avopaterno.filhos))
        p.drawString(10,alturap-180,str(avopaterno.filhas))
        p.drawString(10,alturap-250,avopaterno.relacaoAntes)
        p.drawString(10,alturap-320,avopaterna.relacaoAntes)
        if avopaterno.relacaoAntes == "Sim" and avopaterno.filhosAntes !=None:
            p.setFillColorRGB(0,0,0)
            p.drawString(10,alturap-350,"Seu avô paterno teve quantos filhos homens no relacionamento anterior à relação com sua avó?")
            p.drawString(10,alturap-420,"Seu avô paterno teve quantas filhas mulheres no relacionamento anterior à relação com sua avó?")
            p.setFillColorRGB(1,0,0)
            p.drawString(10,alturap-390,str(avopaterno.filhosAntes))
            p.drawString(10,alturap-460,str(avopaterno.filhasAntes))

            if avopaterna.relacaoAntes == "Sim" and avopaterna.filhosAntes !=None:
                p.setFillColorRGB(0,0,0)
                p.drawString(10,alturap-490,"Sua avó paterna teve quantos filhos homens no relacionamento anterior à relação com seu avô?")
                p.drawString(10,alturap-560,"Sua avó paterna teve quantas filhas mulheres no relacionamento anterior à relação com seu avô?")
                p.setFillColorRGB(1,0,0)
                p.drawString(10,alturap-530,str(avopaterna.filhosAntes))
                p.drawString(10,alturap-600,str(avopaterna.filhasAntes))

        else:
            if avopaterna.relacaoAntes == "Sim" and avopaterna.filhosAntes !=None:
                p.setFillColorRGB(0,0,0)
                p.drawString(10,alturap-350,"Sua avó paterna teve quantos filhos homens no relacionamento anterior à relação com seu avô?")
                p.drawString(10,alturap-420,"Sua avó paterna teve quantas filhas mulheres no relacionamento anterior à relação com seu avô?")
                p.setFillColorRGB(1,0,0)
                p.drawString(10,alturap-390,str(avopaterna.filhosAntes))
                p.drawString(10,alturap-460,str(avopaterna.filhasAntes))

        if (avopaterno.relacaoAntes=="Sim" or avopaterna.relacaoAntes=="Sim") and\
            (avopaterno.relacao == "Separados" or avopaterno.relacao == "Divorciados")and\
            (avopaterno.filhosAntes !=None):
            p.showPage()
            p.setFont("Helvetica", 16)
            p.setFillColorRGB(0,0,1)
            p.drawString(250,800,paciente.nome)
            p.drawString(230,770,"Relacionamentos")
            p.setFillColorRGB(0,0,0)
            p.setFont("Helvetica", 12)
            p.drawString(10,alturap,"Seu avô paterno teve quantos filhos homens no relacionamento posterior à relação com sua avó?")
            p.drawString(10,alturap-70,"Seu avô paterno teve quantas filhas mulheres no relacionamento posterior à relação com sua avó?")
            p.setFillColorRGB(1,0,0)
            p.drawString(10,alturap-40,str(avopaterno.filhosDepois))
            p.drawString(10,alturap-110,str(avopaterno.filhasDepois))
            p.setFillColorRGB(0,0,0)
            p.drawString(10,alturap-140,"Sua avó paterna teve quantos filhos homens no relacionamento posterior à relação com seu avô?")
            p.drawString(10,alturap-210,"Sua avó paterna teve quantas filhas mulheres no relacionamento posterior à relação com seu avô?")
            p.setFillColorRGB(1,0,0)
            p.drawString(10,alturap-180,str(avopaterna.filhosDepois))
            p.drawString(10,alturap-250,str(avopaterna.filhasDepois))

        if (avopaterno.relacaoAntes=="Não" and avopaterna.relacaoAntes=="Não") and\
            (avopaterno.relacao == "Separados" or avopaterno.relacao == "Divorciados")and\
            (avopaterno.filhosAntes !=None):
            p.showPage()
            p.setFont("Helvetica", 16)
            p.setFillColorRGB(0,0,1)
            p.drawString(250,800,paciente.nome)
            p.drawString(230,770,"Relacionamentos")
            p.setFillColorRGB(0,0,0)
            p.setFont("Helvetica", 12)
            p.drawString(10,alturap-350,"Seu avô paterno teve quantos filhos homens no relacionamento posterior à relação com sua avó?")
            p.drawString(10,alturap-420,"Seu avô paterno teve quantas filhas mulheres no relacionamento posterior à relação com sua avó?")
            p.setFillColorRGB(1,0,0)
            p.drawString(10,alturap-390,str(avopaterno.filhosDepois))
            p.drawString(10,alturap-460,str(avopaterno.filhasDepois))
            p.setFillColorRGB(0,0,0)
            p.drawString(10,alturap-490,"Sua avó paterna teve quantos filhos homens no relacionamento posterior à relação com seu avô?")
            p.drawString(10,alturap-560,"Sua avó paterna teve quantas filhas mulheres no relacionamento posterior à relação com seu avô?")
            p.setFillColorRGB(1,0,0)
            p.drawString(10,alturap-530,str(avopaterna.filhosDepois))
            p.drawString(10,alturap-600,str(avopaterna.filhasDepois))

    #Relacionamento Pais
    if Relacionamento.objects.filter(anamnesia_id=analise_id,paciente_id=paciente.id,parente="Pai").exists():

        p.showPage()
        p.setFont("Helvetica", 16)
        p.setFillColorRGB(0,0,1)
        p.drawString(250,800,paciente.nome)
        p.drawString(230,770,"Relacionamentos")

        alturap=740
        p.setFillColorRGB(0,0,0)
        p.setFont("Helvetica", 12)
        p.drawString(10,alturap,"Qual é/era o relacionamento dos seus pais:")
        p.drawString(10,alturap-70,"Seus pais tiveram quantos filhos homens?")
        p.drawString(10,alturap-140,"Seus pais tiveram quantas filhas mulheres?")
        p.drawString(10,alturap-210,"Seu pai era separado/divorciado quando se relacionava com sua mãe?")
        p.drawString(10,alturap-280,"Sua mãe era separada/divorciada quando se relacionava com seu pai?")

        pai=Relacionamento.objects.get(paciente_id=paciente.id,anamnesia_id=analise_id,parente="Pai")
        mae=Relacionamento.objects.get(paciente_id=paciente.id,anamnesia_id=analise_id,parente="Mae")
        p.setFillColorRGB(1,0,0)
        p.setFont("Helvetica", 12)
        p.drawString(10,alturap-40,pai.relacao)
        p.drawString(10,alturap-110,str(pai.filhos))
        p.drawString(10,alturap-180,str(pai.filhas))
        p.drawString(10,alturap-250,pai.relacaoAntes)
        p.drawString(10,alturap-320,mae.relacaoAntes)
        if pai.relacaoAntes == "Sim" and pai.filhosAntes != None:
            p.setFillColorRGB(0,0,0)
            p.drawString(10,alturap-350,"Seu pai teve quantos filhos homens no relacionamento anterior à relação com sua mãe?")
            p.drawString(10,alturap-420,"Seu pai teve quantas filhas mulheres no relacionamento anterior à relação com sua mãe?")
            p.setFillColorRGB(1,0,0)
            p.drawString(10,alturap-390,str(pai.filhosAntes))
            p.drawString(10,alturap-460,str(pai.filhasAntes))

            if mae.relacaoAntes == "Sim" and mae.filhosAntes != None:
                p.setFillColorRGB(0,0,0)
                p.drawString(10,alturap-490,"Sua mãe teve quantos filhos homens no relacionamento anterior à relação com seu pai?")
                p.drawString(10,alturap-560,"Sua mãe teve quantas filhas mulheres no relacionamento anterior à relação com seu pai?")
                p.setFillColorRGB(1,0,0)
                p.drawString(10,alturap-530,str(mae.filhosAntes))
                p.drawString(10,alturap-600,str(mae.filhasAntes))

        else:
            if mae.relacaoAntes == "Sim" and mae.filhosAntes != None:
                p.setFillColorRGB(0,0,0)
                p.drawString(10,alturap-350,"Sua mãe teve quantos filhos homens no relacionamento anterior à relação com seu pai?")
                p.drawString(10,alturap-420,"Sua mãe teve quantas filhas mulheres no relacionamento anterior à relação com seu pai?")
                p.setFillColorRGB(1,0,0)
                p.drawString(10,alturap-390,str(mae.filhosAntes))
                p.drawString(10,alturap-460,str(mae.filhasAntes))

        if (pai.relacaoAntes == "Sim" or mae.relacaoAntes == "Sim" ) and\
                (pai.relacao == "Separados" or pai.relacao == "Divorciados")and\
            (pai.filhosAntes !=None):
            p.showPage()
            p.setFont("Helvetica", 16)
            p.setFillColorRGB(0,0,1)
            p.drawString(250,800,paciente.nome)
            p.drawString(230,770,"Relacionamentos")
            p.setFillColorRGB(0,0,0)
            p.setFont("Helvetica", 12)
            p.drawString(10,alturap,"Seu pai teve quantos filhos homens no relacionamento posterior à relação com sua mãe?")
            p.drawString(10,alturap-70,"Seu pai teve quantas filhas mulheres no relacionamento posterior à relação com sua mãe?")
            p.setFillColorRGB(1,0,0)
            p.drawString(10,alturap-40,str(pai.filhosDepois))
            p.drawString(10,alturap-110,str(pai.filhasDepois))
            p.setFillColorRGB(0,0,0)
            p.drawString(10,alturap-140,"Sua mãe teve quantos filhos homens no relacionamento posterior à relação com seu pai?")
            p.drawString(10,alturap-210,"Sua mãe teve quantas filhas mulheres no relacionamento posterior à relação com seu pai?")
            p.setFillColorRGB(1,0,0)
            p.drawString(10,alturap-180,str(mae.filhosDepois))
            p.drawString(10,alturap-250,str(mae.filhasDepois))

        if (pai.relacaoAntes == "Não" and mae.relacaoAntes == "Não" ) and\
                (pai.relacao == "Separados" or pai.relacao == "Divorciados")and\
            (pai.filhosAntes !=None):
            p.showPage()
            p.setFont("Helvetica", 16)
            p.setFillColorRGB(0,0,1)
            p.drawString(250,800,paciente.nome)
            p.drawString(230,770,"Relacionamentos")
            p.setFillColorRGB(0,0,0)
            p.setFont("Helvetica", 12)
            p.drawString(10,alturap-350,"Seu pai teve quantos filhos homens no relacionamento posterior à relação com sua mãe?")
            p.drawString(10,alturap-420,"Seu pai teve quantas filhas mulheres no relacionamento posterior à relação com sua mãe?")
            p.setFillColorRGB(1,0,0)
            p.drawString(10,alturap-390,str(pai.filhosDepois))
            p.drawString(10,alturap-460,str(pai.filhasDepois))
            p.setFillColorRGB(0,0,0)
            p.drawString(10,alturap-490,"Sua mãe teve quantos filhos homens no relacionamento posterior à relação com seu pai?")
            p.drawString(10,alturap-560,"Sua mãe teve quantas filhas mulheres no relacionamento posterior à relação com seu pai?")
            p.setFillColorRGB(1,0,0)
            p.drawString(10,alturap-530,str(mae.filhosDepois))
            p.drawString(10,alturap-600,str(mae.filhasDepois))

    #Relacionamento Paciente
    if Relacionamento.objects.filter(anamnesia_id=analise_id,paciente_id=paciente.id,parente="Paciente").exists():

        p.showPage()
        p.setFont("Helvetica", 16)
        p.setFillColorRGB(0,0,1)
        p.drawString(250,800,paciente.nome)
        p.drawString(230,770,"Relacionamentos")

        alturap=740
        p.setFillColorRGB(0,0,0)
        p.setFont("Helvetica", 12)
        p.drawString(10,alturap,"Você é:")
        p.drawString(10,alturap-70,"Você tem quantos filhos homens?")
        p.drawString(10,alturap-140,"Você tem quantas filhas mulheres?")
        p.drawString(10,alturap-210,"Você já foi separado/divorciado?")
        p.drawString(10,alturap-280,"Seu cônjuge era separado/divorciado antes de conhecer você?")

        pac=Relacionamento.objects.get(paciente_id=paciente.id,anamnesia_id=analise_id,parente="Paciente")
        conjuge=Relacionamento.objects.get(paciente_id=paciente.id,anamnesia_id=analise_id,parente="Conjuge")
        p.setFillColorRGB(1,0,0)
        p.setFont("Helvetica", 12)
        p.drawString(10,alturap-40,pac.relacao)
        p.drawString(10,alturap-110,str(pac.filhos))
        p.drawString(10,alturap-180,str(pac.filhas))
        p.drawString(10,alturap-250,pac.relacaoAntes)
        p.drawString(10,alturap-320,conjuge.relacaoAntes)
        if pac.relacaoAntes == "Sim" and pac.filhosAntes != None:
            p.setFillColorRGB(0,0,0)
            p.drawString(10,alturap-350,"Você teve quantos filhos homens no relacionamento anterior à relação com seu cônjuge?")
            p.drawString(10,alturap-420,"Você teve quantas filhas mulheres no relacionamento anterior à relação com seu cônjuge?")
            p.setFillColorRGB(1,0,0)
            p.drawString(10,alturap-390,str(pac.filhosAntes))
            p.drawString(10,alturap-460,str(pac.filhasAntes))

            if conjuge.relacaoAntes == "Sim" and conjuge.filhosAntes != None:
                p.setFillColorRGB(0,0,0)
                p.drawString(10,alturap-490,"Seu cônjuge teve quantos filhos homens no relacionamento anterior à relação com você?")
                p.drawString(10,alturap-560,"Seu cônjuge teve quantos filhas mulheres no relacionamento anterior à relação com você?")
                p.setFillColorRGB(1,0,0)
                p.drawString(10,alturap-530,str(conjuge.filhosAntes))
                p.drawString(10,alturap-600,str(conjuge.filhasAntes))

        else:
            if conjuge.relacaoAntes == "Sim" and conjuge.filhosAntes != None:
                p.setFillColorRGB(0,0,0)
                p.drawString(10,alturap-350,"Seu cônjuge teve quantos filhos homens no relacionamento anterior à relação com você?")
                p.drawString(10,alturap-420,"Seu cônjuge teve quantos filhas mulheres no relacionamento anterior à relação com você?")
                p.setFillColorRGB(1,0,0)
                p.drawString(10,alturap-390,str(conjuge.filhosAntes))
                p.drawString(10,alturap-460,str(conjuge.filhasAntes))

        if (conjuge.relacaoAntes == "Sim" or pac.relacaoAntes == "Sim") and\
                (pac.relacao == "Separado(a)" or avopaterno.relacao == "Divorciado(a)")and\
            (pac.filhosAntes !=None):
            p.showPage()
            p.setFont("Helvetica", 16)
            p.setFillColorRGB(0,0,1)
            p.drawString(250,800,paciente.nome)
            p.drawString(230,770,"Relacionamentos")
            p.setFillColorRGB(0,0,0)
            p.setFont("Helvetica", 12)
            p.drawString(10,alturap,"Você teve quantos filhos homens no relacionamento posterior à relação com seu cônjuge?")
            p.drawString(10,alturap-70,"Você teve quantas filhas mulheres no relacionamento posterior à relação com seu cônjuge?")
            p.setFillColorRGB(1,0,0)
            p.drawString(10,alturap-40,str(pac.filhosDepois))
            p.drawString(10,alturap-110,str(pac.filhasDepois))
            p.setFillColorRGB(0,0,0)
            p.drawString(10,alturap-140,"Seu cônjuge teve quantos filhos homens no relacionamento posterior à relação com você?")
            p.drawString(10,alturap-210,"Seu cônjuge teve quantos filhas mulheres no relacionamento posterior à relação com você?")
            p.setFillColorRGB(1,0,0)
            p.drawString(10,alturap-180,str(conjuge.filhosDepois))
            p.drawString(10,alturap-250,str(conjuge.filhasDepois))

        if (conjuge.relacaoAntes == "Não" and pac.relacaoAntes == "Não") and\
                (pac.relacao == "Separado(a)" or avopaterno.relacao == "Divorciado(a)")and\
            (pac.filhosAntes !=None):
            p.setFillColorRGB(0,0,0)
            p.setFont("Helvetica", 12)
            p.drawString(10,alturap-350,"Você teve quantos filhos homens no relacionamento posterior à relação com seu cônjuge?")
            p.drawString(10,alturap-420,"Você teve quantas filhas mulheres no relacionamento posterior à relação com seu cônjuge?")
            p.setFillColorRGB(1,0,0)
            p.drawString(10,alturap-390,str(pac.filhosDepois))
            p.drawString(10,alturap-460,str(pac.filhasDepois))
            p.setFillColorRGB(0,0,0)
            p.drawString(10,alturap-490,"Seu cônjuge teve quantos filhos homens no relacionamento posterior à relação com você?")
            p.drawString(10,alturap-560,"Seu cônjuge teve quantos filhas mulheres no relacionamento posterior à relação com você?")
            p.setFillColorRGB(1,0,0)
            p.drawString(10,alturap-530,str(conjuge.filhosDepois))
            p.drawString(10,alturap-600,str(conjuge.filhasDepois))

    #Grau de Indiferenciação
    if GrauIndiferenciacaoPaciente.objects.filter(paciente_id=paciente.id,anamnesia_id=analise_id).exists():
        lista_resposta=[]
        respostas=GrauIndiferenciacaoPaciente.objects.filter(paciente_id=paciente.id,anamnesia_id=analise_id)
        for item in respostas:
            resposta=GrauIndiferenciacao.objects.get(id=item.resposta_id)
            resposta=resposta.resposta
            lista_resposta.append(resposta)

        p.showPage()
        p.setFont("Helvetica", 16)
        p.setFillColorRGB(0,0,1)
        p.drawString(250,800,paciente.nome)
        p.drawString(210,770,"Grau de Indiferenciação")
        p.setFont("Helvetica", 12)
        p.setFillColorRGB(0,0,0)
        p.drawString(10,740,"Assinale as características que coincidem com o seu comportamento.")


        alturap=700

        for item in lista_resposta:
            if len(item) >100:
                string=item
                depois=string[80:len(string)].split(" ",1)[1]
                antes=string[80:len(string)].split(" ",1)[0]
                p.setFillColorRGB(1,0,0)
                p.setFont("Helvetica", 12)
                p.drawString(10,alturap,item[0:80]+antes)
                if len(depois) >100:
                    string=depois
                    depoisdepois=string[80:len(string)].split(" ",1)[1]
                    antes=string[80:len(string)].split(" ",1)[0]
                    p.setFillColorRGB(1,0,0)
                    p.setFont("Helvetica", 12)
                    p.drawString(10,alturap-15,depois[0:80]+antes)
                    p.drawString(10,alturap-30,depoisdepois)
                    alturap=alturap-30

                else:
                    p.drawString(10,alturap-15,depois)
                    alturap=alturap-10

            else:
                p.setFillColorRGB(1,0,0)
                p.setFont("Helvetica", 12)
                p.drawString(10,alturap,item)

            alturap = alturap -50

            if alturap <= 30:
                p.showPage()
                alturap=720
                p.setFillColorRGB(0,0,1)
                p.setFont("Helvetica", 16)
                p.drawString(250,800,paciente.nome)
                p.drawString(210,770,"Grau de Indiferenciação")

    #Recomendaçao Grau de Indiferenciacao
    anamnesia = Anamnesia.objects.filter(id=analise_id)
    criativo = 0
    reativo = 0
    adaptativo = 0
    for analise in anamnesia:
        indiferenciacao = GrauIndiferenciacaoPaciente.objects.filter(anamnesia_id=analise.id)
        for opcao in indiferenciacao:
            resposta = GrauIndiferenciacao.objects.get(id=opcao.resposta_id)
            if resposta.padrao == "adaptativo":
                adaptativo = adaptativo + 1
            if resposta.padrao == "reativo":
                reativo = reativo + 1
            if resposta.padrao == "criativo":
                criativo = criativo + 1

    nascimento = str(paciente.nascimento)
    ano = int(nascimento.split("-")[0])
    mes = int(nascimento.split("-")[1])
    dia = int(nascimento.split("-")[2])
    atual = datetime.now()
    anoAtual = atual.year
    mesAtual = atual.month
    diaAtual = atual.day

    if mes > mesAtual:
        idade = anoAtual - ano - 1
    if mes < mesAtual:
        idade = anoAtual - ano
    if mes == mesAtual:
        if dia >= diaAtual:
            idade = anoAtual - ano - 1
        if dia < diaAtual:
            idade = anoAtual - ano

    adaptativoMin = 0
    adaptativoMax = 0
    criativoMin = 0
    criativoMax = 0
    reativoMin = 0
    reativoMax = 0

    if idade >= 0 and idade <= 3:
        adaptativoMin = 14
        adaptativoMax = 17
        criativoMin = 0
        criativoMax = 2
        reativoMin = 0
        reativoMax = 2
    if idade >= 4 and idade <= 7:
        adaptativoMin = 12
        adaptativoMax = 17
        criativoMin = 0
        criativoMax = 3
        reativoMin = 2
        reativoMax = 6
    if idade >= 8 and idade <= 12:
        adaptativoMin = 8
        adaptativoMax = 13
        criativoMin = 2
        criativoMax = 5
        reativoMin = 6
        reativoMax = 10
    if idade >= 13 and idade <= 19:
        adaptativoMin = 4
        adaptativoMax = 8
        criativoMin = 6
        criativoMax = 8
        reativoMin = 10
        reativoMax = 15
    if idade >= 20 and idade <= 24:
        adaptativoMin = 1
        adaptativoMax = 3
        criativoMin = 9
        criativoMax = 11
        reativoMin = 8
        reativoMax = 12
    if idade >= 25 and idade <= 32:
        adaptativoMin = 0
        adaptativoMax = 2
        criativoMin = 11
        criativoMax = 15
        reativoMin = 3
        reativoMax = 7
    if idade >= 33:
        adaptativoMin = 0
        adaptativoMax = 2
        criativoMin = 16
        criativoMax = 19
        reativoMin = 0
        reativoMax = 2

    p.showPage()
    p.setFont('Helvetica', 16)
    p.setFillColorRGB(0, 0, 1)
    p.drawString(250, 800, paciente.nome)
    p.drawString(160, 770, "Recomendaçao Grau de Indiferenciação")

    alturap = 740
    p.setFillColorRGB(0, 0, 0)
    p.setFont("Helvetica", 12)

    p.drawString(10, alturap, "Quantidade de respostas selecionadas de cada padrão")
    alturap = alturap - 40
    p.drawString(10, alturap, "Criativo: " + str(criativo))
    alturap = alturap - 20
    p.setFillColorRGB(1, 0, 0)
    p.drawString(10, alturap, "Limite Maximo Criativo: " + str(criativoMax))
    alturap = alturap - 20
    p.drawString(10, alturap, "Limite Mínimo Criativo: " + str(criativoMin))
    alturap = alturap - 20
    p.setFillColorRGB(0, 0, 0)
    p.drawString(10, alturap, "Adaptativo: " + str(adaptativo))
    alturap = alturap - 20
    p.setFillColorRGB(1, 0, 0)
    p.drawString(10, alturap, "Limite Maximo Adaptativo: " + str(adaptativoMax))
    alturap = alturap - 20
    p.drawString(10, alturap, "Limite Mínimo Adaptativo: " + str(adaptativoMin))
    alturap = alturap - 20
    p.setFillColorRGB(0, 0, 0)
    p.drawString(10, alturap, "Reativo: " + str(reativo))
    alturap = alturap - 20
    p.setFillColorRGB(1, 0, 0)
    p.drawString(10, alturap, "Limite Maximo Reativo: " + str(reativoMax))
    alturap = alturap - 20
    p.drawString(10, alturap, "Limite Mínimo Reativo: " + str(reativoMin))
    alturap = alturap - 20

    tudo_dentro = ""
    abaixo_adaptativo = ""
    acima_adaptativo = ""
    abaixo_criativo = ""
    acima_criativo = ""
    abaixo_reativo = ""
    acima_reativo = ""
    texto = ""
    if adaptativo > adaptativoMin and adaptativo < adaptativoMax and \
                    reativo > reativoMin and reativo < reativoMax and \
                    criativo > criativoMin and criativo < criativoMax:
        tudo_dentro = Recomendacao.objects.get(nome='tudo_dentro')
        texto = tudo_dentro.texto
    if adaptativo < adaptativoMin:
        abaixo_adaptativo = Recomendacao.objects.get(nome='intervalo_adaptativo', intervalo="abaixo")
        texto = texto + abaixo_adaptativo.texto
    if adaptativo > adaptativoMax:
        acima_adaptativo = Recomendacao.objects.get(nome='intervalo_adaptativo', intervalo="acima")
        texto = texto + acima_adaptativo.texto
    if reativo < reativoMin:
        abaixo_reativo = Recomendacao.objects.get(nome='intervalo_reativo', intervalo="abaixo")
        texto = texto + abaixo_reativo.texto
    if reativo > reativoMax:
        acima_reativo = Recomendacao.objects.get(nome='intervalo_reativo', intervalo="acima")
        texto = texto + acima_reativo.texto
    if criativo < criativoMin:
        abaixo_criativo = Recomendacao.objects.get(nome='intervalo_criativo', intervalo="abaixo")
        texto = texto + abaixo_criativo.texto
    if criativo > criativoMax:
        acima_criativo = Recomendacao.objects.get(nome='intervalo_criativo', intervalo="acima")
        texto = texto + acima_criativo.texto
    texto = texto.replace("\n", " ")
    if len(texto) > 100:
        string = texto
        depois = string[80:len(string)].split(" ", 1)[1]
        antes = string[80:len(string)].split(" ", 1)[0]
        alturap = alturap - 40
        p.setFillColorRGB(0, 0, 0)
        p.setFont("Helvetica", 12)
        p.drawString(10, alturap, string[0:80] + antes)
        while len(depois) > 100:
            string = depois
            depois = string[80:len(string)].split(" ", 1)[1]
            antes = string[80:len(string)].split(" ", 1)[0]
            p.setFillColorRGB(0, 0, 0)
            p.setFont("Helvetica", 12)
            p.drawString(10, alturap - 15, string[0:80] + antes)
            alturap = alturap - 15
            if alturap <= 60:
                p.showPage()
                alturap = 740
                p.setFillColorRGB(0, 0, 1)
                p.setFont("Helvetica", 16)
                p.drawString(250, 800, paciente.nome)
                p.drawString(160, 770, "Recomendaçao Grau de Indiferenciação")
        p.setFillColorRGB(0, 0, 0)
        p.setFont("Helvetica", 12)
        p.drawString(10, alturap - 15, depois)

    else:
        p.setFillColorRGB(0, 0, 0)
        p.drawString(10, alturap - 40, texto)

    #Seletivas
    if Seletiva.objects.filter(paciente_id=paciente.id,anamnesia_id=analise_id).exists():
        seletivap=PerguntaSeletiva.objects.all()
        lista_resposta={}
        lista_resposta[3]=[]
        lista_resposta[4]=[]
        respostas=Seletiva.objects.filter(paciente_id=paciente.id,anamnesia_id=analise_id)
        for item in respostas:
            pergunta=RespostaSeletiva.objects.get(id=item.resposta_id)
            pergunta_id=pergunta.pergunta_id
            resposta=RespostaSeletiva.objects.get(id=item.resposta_id)
            resposta_seletiva=resposta.resposta
            if resposta.pergunta_id == 3 or resposta.pergunta_id == 4:
                lista_resposta[pergunta_id].append(resposta_seletiva)
            else:
                lista_resposta[pergunta_id]=resposta_seletiva
        p.showPage()
        p.setFont("Helvetica", 16)
        p.setFillColorRGB(0,0,1)
        p.drawString(250,800,paciente.nome)
        p.drawString(265,770,"Seletiva")

        alturap=740

        for item,value in zip(seletivap,lista_resposta):
            if item.numero =="S03" or item.numero == "S04":
                if len(item.pergunta) >100:
                        p.setFillColorRGB(0,0,0)
                        p.setFont("Helvetica", 12)
                        string=item.pergunta
                        depois=string[80:len(string)].split(" ",1)[1]
                        antes=string[80:len(string)].split(" ",1)[0]
                        p.drawString(10,alturap,item.pergunta[0:80]+antes)
                        p.drawString(10,alturap-15,depois)
                else:
                        p.setFillColorRGB(0,0,0)
                        p.setFont("Helvetica", 12)
                        p.drawString(10,alturap,item.pergunta)

                for resp in lista_resposta[value]:
                        p.setFillColorRGB(1,0,0)
                        p.drawString(10,alturap-40,resp)
                        alturap=alturap-15

            else:
                if len(item.pergunta) >100:
                    p.setFillColorRGB(0,0,0)
                    p.setFont("Helvetica", 12)
                    string=item.pergunta
                    depois=string[80:len(string)].split(" ",1)[1]
                    antes=string[80:len(string)].split(" ",1)[0]
                    p.drawString(10,alturap,item.pergunta[0:80]+antes)
                    p.drawString(10,alturap-15,depois)
                    p.setFillColorRGB(1,0,0)
                    p.drawString(10,alturap-40,lista_resposta[value])

                else:
                    p.setFillColorRGB(0,0,0)
                    p.setFont("Helvetica", 12)
                    p.drawString(10,alturap,item.pergunta)
                    p.setFillColorRGB(1,0,0)
                    p.drawString(10,alturap-25,lista_resposta[value])

            alturap = alturap -70

            if alturap <=60:
                p.showPage()
                alturap=740
                p.setFillColorRGB(0,0,1)
                p.setFont("Helvetica", 16)
                p.drawString(250,800,paciente.nome)
                p.drawString(265,770,"Seletiva")

    #Recomendacao Seletiva
    anamnesia = Anamnesia.objects.get(id=analise_id)

    nascimento = str(paciente.nascimento)
    ano = int(nascimento.split("-")[0])
    mes = int(nascimento.split("-")[1])
    dia = int(nascimento.split("-")[2])
    atual = datetime.now()
    anoAtual = atual.year
    mesAtual = atual.month
    diaAtual = atual.day

    if mes > mesAtual:
        idade = anoAtual - ano - 1
    if mes < mesAtual:
        idade = anoAtual - ano
    if mes == mesAtual:
        if dia >= diaAtual:
            idade = anoAtual - ano - 1
        if dia < diaAtual:
            idade = anoAtual - ano

    texto = {}
    relacionamento = "Não há recomendações"
    diferenciacao = "Não há recomendações"
    autonomia = "Não há recomendações"
    assertividade = "Não há recomendações"
    autoEstima = "Não há recomendações"
    somarelacionamento = 0
    somadiferenciacao = 0
    somaautonomia = 0
    somaassertividade = 0
    somaautoestima = 0

    perguntasrelacionamento = ["S34", "S35", "S36"]
    perguntasdiferenciacao = ["S05", "S06", "S15", "S16", "S24", "S25"]
    perguntasautonomia = ["S01", "S07", "S08", "S09", "S10", "S11", "S12", "S13", "S28"]
    perguntasassertiva = ["S14", "S18", "S20", "S21", "S30", "S31", "S32", "S33", ]
    perguntasautoEstima = ["S02", "S17", "S19", "S22", "S23", "S26", "S27", "S29"]

    seletiva = Seletiva.objects.filter(paciente_id=paciente.id, anamnesia_id=anamnesia.id)
    for item in seletiva:
        resposta = RespostaSeletiva.objects.get(id=item.resposta_id)
        pergunta = PerguntaSeletiva.objects.get(id=resposta.pergunta_id)

        if pergunta.numero in perguntasrelacionamento:
            nome = "relacionamento"
            if idade >= 0 and idade <= 3:
                if resposta.nivel0 != 0:
                    somarelacionamento = somarelacionamento + resposta.nivel0
                    if resposta.nivel0 <= 1:
                        relacionamento = Recomendacao.objects.get(nome=nome, intervalo="nivel0")
            if idade >= 4 and idade <= 7:
                if resposta.nivel1 != 0:
                    somarelacionamento = somarelacionamento + resposta.nivel1
                    if resposta.nivel1 <= 1:
                        relacionamento = Recomendacao.objects.get(nome=nome, intervalo="nivel1")
                        relacionamento = relacionamento.texto
            if idade >= 8 and idade <= 12:
                if resposta.nivel2 != 0:
                    somarelacionamento = somarelacionamento + resposta.nivel2
                    if resposta.nivel2 <= 1:
                        relacionamento = Recomendacao.objects.get(nome=nome, intervalo="nivel2")
                        relacionamento = relacionamento.texto
            if idade >= 13 and idade <= 19:
                if resposta.nivel3 != 0:
                    somarelacionamento = somarelacionamento + resposta.nivel3
                    if resposta.nivel3 <= 1:
                        relacionamento = Recomendacao.objects.get(nome=nome, intervalo="nivel3")
                        relacionamento = relacionamento.texto
            if idade >= 20 and idade <= 24:
                if resposta.nivel4 != 0:
                    somarelacionamento = somarelacionamento + resposta.nivel4
                    if resposta.nivel4 <= 1:
                        relacionamento = Recomendacao.objects.get(nome=nome, intervalo="nivel4")
                        relacionamento = relacionamento.texto
            if idade >= 25 and idade <= 32:
                if resposta.nivel5 != 0:
                    somarelacionamento = somarelacionamento + resposta.nivel5
                    if resposta.nivel5 <= 1:
                        relacionamento = Recomendacao.objects.get(nome=nome, intervalo="nivel5")
                        relacionamento = relacionamento.texto
            if idade >= 33:
                if resposta.nivel6 != 0:
                    somarelacionamento = somarelacionamento + resposta.nivel6
                    if resposta.nivel6 <= 1:
                        relacionamento = Recomendacao.objects.get(nome=nome, intervalo="nivel6")
                        relacionamento = relacionamento.texto

        if pergunta.numero in perguntasdiferenciacao:
            nome = "diferenciacao"
            if idade >= 0 and idade <= 3:
                if resposta.nivel0 != 0:
                    somadiferenciacao = somadiferenciacao + resposta.nivel0
                    if resposta.nivel0 <= 1:
                        diferenciacao = Recomendacao.objects.get(nome=nome, intervalo="nivel0")
            if idade >= 4 and idade <= 7:
                if resposta.nivel1 != 0:
                    somadiferenciacao = somadiferenciacao + resposta.nivel1
                    if resposta.nivel1 <= 1:
                        diferenciacao = Recomendacao.objects.get(nome=nome, intervalo="nivel1")
                        diferenciacao = diferenciacao.texto
            if idade >= 8 and idade <= 12:
                if resposta.nivel2 != 0:
                    somadiferenciacao = somadiferenciacao + resposta.nivel2
                    if resposta.nivel2 <= 1:
                        diferenciacao = Recomendacao.objects.get(nome=nome, intervalo="nivel2")
                        diferenciacao = diferenciacao.texto
            if idade >= 13 and idade <= 19:
                if resposta.nivel3 != 0:
                    somadiferenciacao = somadiferenciacao + resposta.nivel3
                    if resposta.nivel3 <= 1:
                        diferenciacao = Recomendacao.objects.get(nome=nome, intervalo="nivel3")
                        diferenciacao = diferenciacao.texto
            if idade >= 20 and idade <= 24:
                if resposta.nivel4 != 0:
                    somadiferenciacao = somadiferenciacao + resposta.nivel4
                    if resposta.nivel4 <= 1:
                        diferenciacao = Recomendacao.objects.get(nome=nome, intervalo="nivel4")
                        diferenciacao = diferenciacao.texto
            if idade >= 25 and idade <= 32:
                if resposta.nivel5 != 0:
                    somadiferenciacao = somadiferenciacao + resposta.nivel5
                    if resposta.nivel5 <= 1:
                        diferenciacao = Recomendacao.objects.get(nome=nome, intervalo="nivel5")
                        diferenciacao = diferenciacao.texto
            if idade >= 33:
                if resposta.nivel6 != 0:
                    somadiferenciacao = somadiferenciacao + resposta.nivel6
                    if resposta.nivel6 <= 1:
                        diferenciacao = Recomendacao.objects.get(nome=nome, intervalo="nivel6")
                        diferenciacao = diferenciacao.texto

        if pergunta.numero in perguntasautonomia:
            nome = "autonomia"
            if idade >= 0 and idade <= 3:
                if resposta.nivel0 != 0:
                    somaautonomia = somaautonomia + resposta.nivel0
                    if resposta.nivel0 <= 1:
                        autonomia = Recomendacao.objects.get(nome=nome, intervalo="nivel0")
            if idade >= 4 and idade <= 7:
                if resposta.nivel1 != 0:
                    somaautonomia = somaautonomia + resposta.nivel1
                    if resposta.nivel1 <= 1:
                        autonomia = Recomendacao.objects.get(nome=nome, intervalo="nivel1")
                        autonomia = autonomia.texto
            if idade >= 8 and idade <= 12:
                if resposta.nivel2 != 0:
                    somaautonomia = somaautonomia + resposta.nivel2
                    if resposta.nivel2 <= 1:
                        autonomia = Recomendacao.objects.get(nome=nome, intervalo="nivel2")
                        autonomia = autonomia.texto
            if idade >= 13 and idade <= 19:
                if resposta.nivel3 != 0:
                    somaautonomia = somaautonomia + resposta.nivel3
                    if resposta.nivel3 <= 1:
                        autonomia = Recomendacao.objects.get(nome=nome, intervalo="nivel3")
                        autonomia = autonomia.texto
            if idade >= 20 and idade <= 24:
                if resposta.nivel4 != 0:
                    somaautonomia = somaautonomia + resposta.nivel4
                    if resposta.nivel4 <= 1:
                        autonomia = Recomendacao.objects.get(nome=nome, intervalo="nivel4")
                        autonomia = autonomia.texto
            if idade >= 25 and idade <= 32:
                if resposta.nivel5 != 0:
                    somaautonomia = somaautonomia + resposta.nivel5
                    if resposta.nivel5 <= 1:
                        autonomia = Recomendacao.objects.get(nome=nome, intervalo="nivel5")
                        autonomia = autonomia.texto
            if idade >= 33:
                if resposta.nivel6 != 0:
                    somaautonomia = somaautonomia + resposta.nivel6
                    if resposta.nivel6 <= 1:
                        autonomia = Recomendacao.objects.get(nome=nome, intervalo="nivel6")
                        autonomia = autonomia.texto

        if pergunta.numero in perguntasassertiva:
            nome = "assertividade"
            if idade >= 0 and idade <= 3:
                if resposta.nivel0 != 0:
                    somaassertividade = somaassertividade + resposta.nivel0
                    if resposta.nivel0 <= 1:
                        assertividade = Recomendacao.objects.get(nome=nome, intervalo="nivel0")
            if idade >= 4 and idade <= 7:
                if resposta.nivel1 != 0:
                    somaassertividade = somaassertividade + resposta.nivel1
                    if resposta.nivel1 <= 1:
                        assertividade = Recomendacao.objects.get(nome=nome, intervalo="nivel1")
                        assertividade = assertividade.texto
            if idade >= 8 and idade <= 12:
                if resposta.nivel2 != 0:
                    somaassertividade = somaassertividade + resposta.nivel2
                    if resposta.nivel2 <= 1:
                        assertividade = Recomendacao.objects.get(nome=nome, intervalo="nivel2")
                        assertividade = assertividade.texto
            if idade >= 13 and idade <= 19:
                if resposta.nivel3 != 0:
                    somaassertividade = somaassertividade + resposta.nivel3
                    if resposta.nivel3 <= 1:
                        assertividade = Recomendacao.objects.get(nome=nome, intervalo="nivel3")
                        assertividade = assertividade.texto
            if idade >= 20 and idade <= 24:
                if resposta.nivel4 != 0:
                    somaassertividade = somaassertividade + resposta.nivel4
                    if resposta.nivel4 <= 1:
                        assertividade = Recomendacao.objects.get(nome=nome, intervalo="nivel4")
                        assertividade = assertividade.texto
            if idade >= 25 and idade <= 32:
                if resposta.nivel5 != 0:
                    somaassertividade = somaassertividade + resposta.nivel5
                    if resposta.nivel5 <= 1:
                        assertividade = Recomendacao.objects.get(nome=nome, intervalo="nivel5")
                        assertividade = assertividade.texto
            if idade >= 33:
                if resposta.nivel6 != 0:
                    somaassertividade = somaassertividade + resposta.nivel6
                    if resposta.nivel6 <= 1:
                        assertividade = Recomendacao.objects.get(nome=nome, intervalo="nivel6")
                        assertividade = assertividade.texto

        if pergunta.numero in perguntasautoEstima:
            nome = "autoestima"
            if idade >= 0 and idade <= 3:
                if resposta.nivel0 != 0:
                    somaautoestima = somaautoestima + resposta.nivel0
                    if resposta.nivel0 <= 1:
                        autoEstima = Recomendacao.objects.get(nome=nome, intervalo="nivel0")
            if idade >= 4 and idade <= 7:
                if resposta.nivel1 != 0:
                    somaautoestima = somaautoestima + resposta.nivel1
                    if resposta.nivel1 <= 1:
                        autoEstima = Recomendacao.objects.get(nome=nome, intervalo="nivel1")
                        autoEstima = autoEstima.texto
            if idade >= 8 and idade <= 12:
                if resposta.nivel2 != 0:
                    somaautoestima = somaautoestima + resposta.nivel2
                    if resposta.nivel2 <= 1:
                        autoEstima = Recomendacao.objects.get(nome=nome, intervalo="nivel2")
                        autoEstima = autoEstima.texto
            if idade >= 13 and idade <= 19:
                if resposta.nivel3 != 0:
                    somaautoestima = somaautoestima + resposta.nivel3
                    if resposta.nivel3 <= 1:
                        autoEstima = Recomendacao.objects.get(nome=nome, intervalo="nivel3")
                        autoEstima = autoEstima.texto
            if idade >= 20 and idade <= 24:
                if resposta.nivel4 != 0:
                    somaautoestima = somaautoestima + resposta.nivel4
                    if resposta.nivel4 <= 1:
                        autoEstima = Recomendacao.objects.get(nome=nome, intervalo="nivel4")
                        autoEstima = autoEstima.texto
            if idade >= 25 and idade <= 32:
                if resposta.nivel5 != 0:
                    somaautoestima = somaautoestima + resposta.nivel5
                    if resposta.nivel5 <= 1:
                        autoEstima = Recomendacao.objects.get(nome=nome, intervalo="nivel5")
                        autoEstima = autoEstima.texto
            if idade >= 33:
                if resposta.nivel6 != 0:
                    somaautoestima = somaautoestima + resposta.nivel6
                    if resposta.nivel6 <= 1:
                        autoEstima = Recomendacao.objects.get(nome=nome, intervalo="nivel6")
                        autoEstima = autoEstima.texto

    if somarelacionamento / len(perguntasrelacionamento) < 3:
        nome = "relacionamento"
        if idade >= 0 and idade <= 3:
            relacionamento = Recomendacao.objects.get(nome=nome, intervalo="nivel0")
        if idade >= 4 and idade <= 7:
            relacionamento = Recomendacao.objects.get(nome=nome, intervalo="nivel1")
        if idade >= 8 and idade <= 12:
            relacionamento = Recomendacao.objects.get(nome=nome, intervalo="nivel2")
        if idade >= 13 and idade <= 19:
            relacionamento = Recomendacao.objects.get(nome=nome, intervalo="nivel3")
        if idade >= 20 and idade <= 24:
            relacionamento = Recomendacao.objects.get(nome=nome, intervalo="nivel4")
        if idade >= 25 and idade <= 32:
            relacionamento = Recomendacao.objects.get(nome=nome, intervalo="nivel5")
        if idade >= 33:
            relacionamento = Recomendacao.objects.get(nome=nome, intervalo="nivel6")
        relacionamento = relacionamento.texto

    if somadiferenciacao / len(perguntasdiferenciacao) < 3:
        nome = "diferenciacao"
        if idade >= 0 and idade <= 3:
            diferenciacao = Recomendacao.objects.get(nome=nome, intervalo="nivel0")
        if idade >= 4 and idade <= 7:
            diferenciacao = Recomendacao.objects.get(nome=nome, intervalo="nivel1")
        if idade >= 8 and idade <= 12:
            diferenciacao = Recomendacao.objects.get(nome=nome, intervalo="nivel2")
        if idade >= 13 and idade <= 19:
            diferenciacao = Recomendacao.objects.get(nome=nome, intervalo="nivel3")
        if idade >= 20 and idade <= 24:
            diferenciacao = Recomendacao.objects.get(nome=nome, intervalo="nivel4")
        if idade >= 25 and idade <= 32:
            diferenciacao = Recomendacao.objects.get(nome=nome, intervalo="nivel5")
        if idade >= 33:
            diferenciacao = Recomendacao.objects.get(nome=nome, intervalo="nivel6")
        diferenciacao = diferenciacao.texto

    if somaautonomia / len(perguntasautonomia) < 3:
        nome = "autonomia"
        if idade >= 0 and idade <= 3:
            autonomia = Recomendacao.objects.get(nome=nome, intervalo="nivel0")
        if idade >= 4 and idade <= 7:
            autonomia = Recomendacao.objects.get(nome=nome, intervalo="nivel1")
        if idade >= 8 and idade <= 12:
            autonomia = Recomendacao.objects.get(nome=nome, intervalo="nivel2")
        if idade >= 13 and idade <= 19:
            autonomia = Recomendacao.objects.get(nome=nome, intervalo="nivel3")
        if idade >= 20 and idade <= 24:
            autonomia = Recomendacao.objects.get(nome=nome, intervalo="nivel4")
        if idade >= 25 and idade <= 32:
            autonomia = Recomendacao.objects.get(nome=nome, intervalo="nivel5")
        if idade >= 33:
            autonomia = Recomendacao.objects.get(nome=nome, intervalo="nivel6")
        autonomia = autonomia.texto

    if somaassertividade / len(perguntasassertiva) < 3:
        nome = "assertividade"
        if idade >= 0 and idade <= 3:
            assertividade = Recomendacao.objects.get(nome=nome, intervalo="nivel0")
        if idade >= 4 and idade <= 7:
            assertividade = Recomendacao.objects.get(nome=nome, intervalo="nivel1")
        if idade >= 8 and idade <= 12:
            assertividade = Recomendacao.objects.get(nome=nome, intervalo="nivel2")
        if idade >= 13 and idade <= 19:
            assertividade = Recomendacao.objects.get(nome=nome, intervalo="nivel3")
        if idade >= 20 and idade <= 24:
            assertividade = Recomendacao.objects.get(nome=nome, intervalo="nivel4")
        if idade >= 25 and idade <= 32:
            assertividade = Recomendacao.objects.get(nome=nome, intervalo="nivel5")
        if idade >= 33:
            assertividade = Recomendacao.objects.get(nome=nome, intervalo="nivel6")
        assertividade = assertividade.texto

    if somaautoestima / len(perguntasautoEstima) < 3:
        nome = "autoestima"
        if idade >= 0 and idade <= 3:
            autoEstima = Recomendacao.objects.get(nome=nome, intervalo="nivel0")
        if idade >= 4 and idade <= 7:
            autoEstima = Recomendacao.objects.get(nome=nome, intervalo="nivel1")
        if idade >= 8 and idade <= 12:
            autoEstima = Recomendacao.objects.get(nome=nome, intervalo="nivel2")
        if idade >= 13 and idade <= 19:
            autoEstima = Recomendacao.objects.get(nome=nome, intervalo="nivel3")
        if idade >= 20 and idade <= 24:
            autoEstima = Recomendacao.objects.get(nome=nome, intervalo="nivel4")
        if idade >= 25 and idade <= 32:
            autoEstima = Recomendacao.objects.get(nome=nome, intervalo="nivel5")
        if idade >= 33:
            autoEstima = Recomendacao.objects.get(nome=nome, intervalo="nivel6")
        autoEstima = autoEstima.texto

    p.showPage()
    p.setFont('Helvetica', 16)
    p.setFillColorRGB(0, 0, 1)
    p.drawString(250, 800, paciente.nome)
    p.drawString(200, 770, "Recomendaçao Seletiva")

    alturap = 740
    p.setFillColorRGB(0, 0, 0)
    p.setFont("Helvetica", 12)

    if not (relacionamento == ""):
        texto=relacionamento
        texto=texto.replace("\n"," ")
        p.drawString(10, alturap, "Relacionamento:")
        if len(texto) > 100:
            string = texto
            depois = string[80:len(string)].split(" ", 1)[1]
            antes = string[80:len(string)].split(" ", 1)[0]
            alturap = alturap - 40
            p.setFillColorRGB(0, 0, 0)
            p.setFont("Helvetica", 12)
            p.drawString(10, alturap, string[0:80] + antes)
            while len(depois) > 100:
                string = depois
                depois = string[80:len(string)].split(" ", 1)[1]
                antes = string[80:len(string)].split(" ", 1)[0]
                p.setFillColorRGB(0, 0, 0)
                p.setFont("Helvetica", 12)
                p.drawString(10, alturap - 15, string[0:80] + antes)
                alturap = alturap - 15
                if alturap <= 60:
                    p.showPage()
                    alturap = 740
                    p.setFillColorRGB(0, 0, 1)
                    p.setFont("Helvetica", 16)
                    p.drawString(250, 800, paciente.nome)
                    p.drawString(200, 770, "Recomendaçao Seletiva")
            p.setFillColorRGB(0, 0, 0)
            p.setFont("Helvetica", 12)
            p.drawString(10, alturap - 15, depois)

        else:
            p.setFillColorRGB(0, 0, 0)
            p.drawString(10, alturap - 40, texto)

        alturap=alturap-70

        if not (diferenciacao == ""):
            texto = diferenciacao
            texto = texto.replace("\n", " ")
            p.drawString(10, alturap, "Diferenciação:")
            if len(texto) > 100:
                string = texto
                depois = string[80:len(string)].split(" ", 1)[1]
                antes = string[80:len(string)].split(" ", 1)[0]
                alturap = alturap - 40
                p.setFillColorRGB(0, 0, 0)
                p.setFont("Helvetica", 12)
                p.drawString(10, alturap, string[0:80] + antes)
                while len(depois) > 100:
                    string = depois
                    depois = string[80:len(string)].split(" ", 1)[1]
                    antes = string[80:len(string)].split(" ", 1)[0]
                    p.setFillColorRGB(0, 0, 0)
                    p.setFont("Helvetica", 12)
                    p.drawString(10, alturap - 15, string[0:80] + antes)
                    alturap = alturap - 15
                    if alturap <= 60:
                        p.showPage()
                        alturap = 740
                        p.setFillColorRGB(0, 0, 1)
                        p.setFont("Helvetica", 16)
                        p.drawString(250, 800, paciente.nome)
                        p.drawString(200, 770, "Recomendaçao Seletiva")
                p.setFillColorRGB(0, 0, 0)
                p.setFont("Helvetica", 12)
                p.drawString(10, alturap - 15, depois)

            else:
                p.setFillColorRGB(0, 0, 0)
                p.drawString(10, alturap - 40, texto)

            alturap = alturap - 70

            if not (autonomia == ""):
                texto = autonomia
                texto = texto.replace("\n", " ")
                p.drawString(10, alturap, "Autonomia:")
                if len(texto) > 100:
                    string = texto
                    depois = string[80:len(string)].split(" ", 1)[1]
                    antes = string[80:len(string)].split(" ", 1)[0]
                    alturap = alturap - 40
                    p.setFillColorRGB(0, 0, 0)
                    p.setFont("Helvetica", 12)
                    p.drawString(10, alturap, string[0:80] + antes)
                    while len(depois) > 100:
                        string = depois
                        depois = string[80:len(string)].split(" ", 1)[1]
                        antes = string[80:len(string)].split(" ", 1)[0]
                        p.setFillColorRGB(0, 0, 0)
                        p.setFont("Helvetica", 12)
                        p.drawString(10, alturap - 15, string[0:80] + antes)
                        alturap = alturap - 15
                        if alturap <= 60:
                            p.showPage()
                            alturap = 740
                            p.setFillColorRGB(0, 0, 1)
                            p.setFont("Helvetica", 16)
                            p.drawString(250, 800, paciente.nome)
                            p.drawString(200, 770, "Recomendaçao Seletiva")
                    p.setFillColorRGB(0, 0, 0)
                    p.setFont("Helvetica", 12)
                    p.drawString(10, alturap - 15, depois)

                else:
                    p.setFillColorRGB(0, 0, 0)
                    p.drawString(10, alturap - 40, texto)

                alturap = alturap - 70

                if not (assertividade == ""):
                    texto = assertividade
                    texto = texto.replace("\n", " ")
                    p.drawString(10, alturap, "Assertividade:")
                    if len(texto) > 100:
                        string = texto
                        depois = string[80:len(string)].split(" ", 1)[1]
                        antes = string[80:len(string)].split(" ", 1)[0]
                        alturap = alturap - 40
                        p.setFillColorRGB(0, 0, 0)
                        p.setFont("Helvetica", 12)
                        p.drawString(10, alturap, string[0:80] + antes)
                        while len(depois) > 100:
                            string = depois
                            depois = string[80:len(string)].split(" ", 1)[1]
                            antes = string[80:len(string)].split(" ", 1)[0]
                            p.setFillColorRGB(0, 0, 0)
                            p.setFont("Helvetica", 12)
                            p.drawString(10, alturap - 15, string[0:80] + antes)
                            alturap = alturap - 15
                            if alturap <= 60:
                                p.showPage()
                                alturap = 740
                                p.setFillColorRGB(0, 0, 1)
                                p.setFont("Helvetica", 16)
                                p.drawString(250, 800, paciente.nome)
                                p.drawString(200, 770, "Recomendaçao Seletiva")
                        p.setFillColorRGB(0, 0, 0)
                        p.setFont("Helvetica", 12)
                        p.drawString(10, alturap - 15, depois)

                    else:
                        p.setFillColorRGB(0, 0, 0)
                        p.drawString(10, alturap - 40, texto)

                    alturap = alturap - 70

                    if not (autoEstima == ""):
                        texto = autoEstima
                        texto = texto.replace("\n", " ")
                        p.drawString(10, alturap, "Autoestima:")
                        if len(texto) > 100:
                            string = texto
                            depois = string[80:len(string)].split(" ", 1)[1]
                            antes = string[80:len(string)].split(" ", 1)[0]
                            alturap = alturap - 40
                            p.setFillColorRGB(0, 0, 0)
                            p.setFont("Helvetica", 12)
                            p.drawString(10, alturap, string[0:80] + antes)
                            while len(depois) > 100:
                                string = depois
                                depois = string[80:len(string)].split(" ", 1)[1]
                                antes = string[80:len(string)].split(" ", 1)[0]
                                p.setFillColorRGB(0, 0, 0)
                                p.setFont("Helvetica", 12)
                                p.drawString(10, alturap - 15, string[0:80] + antes)
                                alturap = alturap - 15
                                if alturap <= 60:
                                    p.showPage()
                                    alturap = 740
                                    p.setFillColorRGB(0, 0, 1)
                                    p.setFont("Helvetica", 16)
                                    p.drawString(250, 800, paciente.nome)
                                    p.drawString(200, 770, "Recomendaçao Seletiva")
                            p.setFillColorRGB(0, 0, 0)
                            p.setFont("Helvetica", 12)
                            p.drawString(10, alturap - 15, depois)

                        else:
                            p.setFillColorRGB(0, 0, 0)
                            p.drawString(10, alturap - 40, texto)
    #Interventivas
    if Interventiva.objects.filter(paciente_id=paciente.id,anamnesia_id=analise_id).exists():
        perguntas=PerguntaInterventiva.objects.all().order_by("numero")
        lista_resposta=[]
        respostas=Interventiva.objects.filter(paciente_id=paciente.id,anamnesia_id=analise_id).order_by("pergunta_id")
        for item in respostas:
            lista_resposta.append(item.resposta)

        p.showPage()
        p.setFont("Helvetica", 16)
        p.setFillColorRGB(0,0,1)
        p.drawString(250,800,paciente.nome)
        p.drawString(250,770,"Interventiva")

        alturap=740

        for item,value in zip(perguntas,lista_resposta):
            if len(item.pergunta) >100:
                p.setFillColorRGB(0,0,0)
                p.setFont("Helvetica", 12)
                string=item.pergunta
                depois=string[80:len(string)].split(" ",1)[1]
                antes=string[80:len(string)].split(" ",1)[0]
                p.drawString(10,alturap,item.pergunta[0:80]+antes)
                if len(depois) >100:
                    string=depois
                    depois=string[80:len(string)].split(" ",1)[1]
                    antes=string[80:len(string)].split(" ",1)[0]
                    p.drawString(10,alturap-15,string[0:80]+antes)
                    p.drawString(10,alturap-30,depois)
                    alturap=alturap-30
                else:
                    p.drawString(10,alturap-15,depois)
                    alturap=alturap-10


            else:
                p.setFillColorRGB(0,0,0)
                p.setFont("Helvetica", 12)
                p.drawString(10,alturap,item.pergunta)

            if len(value)>100:
                string=value
                depois=string[80:len(string)].split(" ",1)[1]
                antes=string[80:len(string)].split(" ",1)[0]
                alturap=alturap-40
                p.setFillColorRGB(1,0,0)
                p.setFont("Helvetica", 12)
                p.drawString(10,alturap,string[0:80]+antes)
                while len(depois) >100:
                    string=depois
                    depois=string[80:len(string)].split(" ",1)[1]
                    antes=string[80:len(string)].split(" ",1)[0]
                    p.setFillColorRGB(1,0,0)
                    p.setFont("Helvetica", 12)
                    p.drawString(10,alturap-15,string[0:80]+antes)
                    alturap=alturap-15
                    if alturap <=60:
                        p.showPage()
                        alturap=740
                        p.setFillColorRGB(0,0,1)
                        p.setFont("Helvetica", 16)
                        p.drawString(250,800,paciente.nome)
                        p.drawString(250,770,"Interventiva")
                p.setFillColorRGB(1,0,0)
                p.setFont("Helvetica", 12)
                p.drawString(10,alturap-15,depois)

            else:
                p.setFillColorRGB(1,0,0)
                p.drawString(10,alturap-40,value)


            alturap = alturap -70

            if alturap <=60:
                p.showPage()
                alturap=740
                p.setFillColorRGB(0,0,1)
                p.setFont("Helvetica", 16)
                p.drawString(250,800,paciente.nome)
                p.drawString(250,770,"Interventiva")

    # Close the PDF object cleanly, and we're done
    p.showPage()
    p.save()
    return response
#Classes do password-reset(esqueci a senha)

class SaltMixin(object):
    salt = 'psicologo/password_recovery'
    url_salt = 'psicologo/password_recovery_url'


def loads_with_timestamp(value, salt):
    """Returns the unsigned value along with its timestamp, the time when it
    got dumped."""
    try:
        signing.loads(value, salt=salt, max_age=-1)
    except signing.SignatureExpired as e:
        age = float(str(e).split('Signature age ')[1].split(' >')[0])
        timestamp = timezone.now() - timedelta(seconds=age)
        return timestamp, signing.loads(value, salt=salt)


class RecoverDone(SaltMixin, generic.TemplateView):
    template_name = 'psicologo/password_reset/reset_sent2.html'

    def get_context_data(self, **kwargs):
        ctx = super(RecoverDone, self).get_context_data(**kwargs)
        try:
            ctx['timestamp'], ctx['email'] = loads_with_timestamp(
                self.kwargs['signature'], salt=self.url_salt,
            )
        except signing.BadSignature:
            raise Http404
        return ctx
recover_done = RecoverDone.as_view()


class Recover(SaltMixin, generic.FormView):
    case_sensitive = True
    form_class = PasswordRecoveryForm
    template_name = 'psicologo/password_reset/recovery_form2.html'
    success_url_name = 'psicologo/password_reset_sent'
    email_template_name = 'psicologo/password_reset/recovery_email2.txt'
    email_subject_template_name = 'psicologo/password_reset/recovery_email_subject2.txt'
    search_fields = ['username', 'email']

    def get_success_url(self):
        return reverse(self.success_url_name, args=[self.mail_signature])

    def get_context_data(self, **kwargs):
        kwargs['url'] = self.request.get_full_path()
        return super(Recover, self).get_context_data(**kwargs)

    def get_form_kwargs(self):
        kwargs = super(Recover, self).get_form_kwargs()
        kwargs.update({
            'case_sensitive': self.case_sensitive,
            'search_fields': self.search_fields,
        })
        return kwargs

    def get_site(self):
        return get_current_site(self.request)

    def send_notification(self):
        context = {
            'site': self.get_site(),
            'user': self.user,
            'username': get_username(self.user),
            'token': signing.dumps(self.user.pk, salt=self.salt),
            'secure': self.request.is_secure(),
        }
        body = loader.render_to_string(self.email_template_name,
                                       context).strip()
        subject = loader.render_to_string(self.email_subject_template_name,
                                          context).strip()
        send_mail(subject, body, settings.DEFAULT_FROM_EMAIL,
                  [self.user.email])

    def form_valid(self, form):
        self.user = form.cleaned_data['user']
        self.send_notification()
        if (
            len(self.search_fields) == 1 and
            self.search_fields[0] == 'username'
        ):
            # if we only search by username, don't disclose the user email
            # since it may now be public information.
            email = self.user.username
        else:
            email = self.user.email
        self.mail_signature = signing.dumps(email, salt=self.url_salt)
        return super(Recover, self).form_valid(form)
recover = Recover.as_view()


class Reset(SaltMixin, generic.FormView):
    form_class = PasswordResetForm
    token_expires = 3600 * 48  # Two days
    template_name = 'psicologo/password_reset/reset2.html'
    success_url = reverse_lazy('psicologo/password_reset_done')

    @method_decorator(sensitive_post_parameters('password1', 'password2'))
    def dispatch(self, request, *args, **kwargs):
        self.request = request
        self.args = args
        self.kwargs = kwargs
        self.user = None

        try:
            pk = signing.loads(kwargs['token'], max_age=self.token_expires,
                               salt=self.salt)
        except signing.BadSignature:
            return self.invalid()

        self.user = get_object_or_404(get_user_model(), pk=pk)
        return super(Reset, self).dispatch(request, *args, **kwargs)

    def invalid(self):
        return self.render(self.get_context_data(invalid=True))

    def get_form_kwargs(self):
        kwargs = super(Reset, self).get_form_kwargs()
        kwargs['user'] = self.user
        return kwargs

    def get_context_data(self, **kwargs):
        ctx = super(Reset, self).get_context_data(**kwargs)
        if 'invalid' not in ctx:
            ctx.update({
                'username': get_username(self.user),
                'token': self.kwargs['token'],
            })
        return ctx

    def form_valid(self, form):
        form.save()
        user_recovers_password.send(
            sender=get_user_model(),
            user=form.user,
            request=self.request
        )
        return redirect(self.get_success_url())
reset = Reset.as_view()


class ResetDone(generic.TemplateView):
    template_name = 'psicologo/password_reset/recovery_done2.html'


reset_done = ResetDone.as_view()