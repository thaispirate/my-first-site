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
    return render_to_response('projetofinal/psicologo/login.html', {'state':state, 'username': username},context_instance=RequestContext(request))

class CadastroPsicologoWizard(SessionWizardView):
    template_name = "projetofinal/psicologo/cadastro.html"

    def done(self, form_list, form_dict, **kwargs):
        form_data= [form.cleaned_data for form in form_list]
        user = User()
        user.username = form_data[0]['username']
        user.set_password(form_data[0]['password1'])
        user.email = form_data[0]['username']
        user.first_name = form_data[1]['nome']
        user.save()
        code= form_data[0]['code']
        chave= Chave.objects.get(chave = code)
        chave.padrao = "usada"
        chave.save()
        group = Group.objects.get_or_create(name="psicologo")
        group = Group.objects.get(name="psicologo")
        user.groups.add(group)
        psicologo = Psicologo()
        psicologo.usuario = user
        psicologo.email = form_data[0]['username']
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
        return paciente_id

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

        for key,value in self.form_list.items():
            if value != ConsultarAreaAfetiva:
                self.form_list.pop(key)

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
        return self.render_to_response(self.get_context_data(invalid=True))

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