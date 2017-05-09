import datetime
import math
from datetime import datetime, timedelta
import json
from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.models import User, Group
from .forms import CadastroPaciente,CadastroConjuge,CadastroPai,CadastroMae,CadastroAvoPaterno,\
    CadastroAvoPaterna,CadastroAvoMaterno,CadastroAvoMaterna,EdicaoPaciente,AtualizarChave, HabilitarPsicologo, BuscarPsicologo
from .models import Paciente, Chave, User,Familia, Psicologo, Anamnesia

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
#from dal import autocomplete

# Create your views here.

#Views Paciente

def is_member(user):
    return user.groups.filter(name='paciente').exists()

class Home(TemplateView):
    template_name = "projetofinal/home.html"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(Home, self).dispatch(*args, **kwargs)

    def paciente(self):
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

        return paciente

def LoginPaciente(request):
    username = password = ''
    state="please log in"
    if request.POST:
        username = request.POST['username'].lower()
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active and user.groups.filter(name='paciente').exists():
                login(request, user)
                state = "You're successfully logged in!"
                paciente_id=str(user.id)
                return HttpResponseRedirect('home/'+ paciente_id +'/')
            else:
                state = 1
        else:
            state = 2
    return render_to_response('projetofinal/login.html', {'state':state, 'username': username},context_instance=RequestContext(request))


def LogoutView(request):
    logout(request)
    return render(request, 'projetofinal/sair.html', {})

def Erro404(request):
    return render(request,'404.html')

class CadastroWizard(SessionWizardView):
    template_name = "projetofinal/cadastro.html"

    def done(self, form_list, form_dict, **kwargs):
        form_data= [form.cleaned_data for form in form_list]
        user = User()
        user.username = form_data[0]['username']
        user.set_password(form_data[0]['password1'])
        user.email = form_data[0]['username']
        user.first_name = form_data[0]['nome']
        user.save()
        code= form_data[0]['code']
        chave= Chave.objects.get(chave = code)
        chave.padrao = "usada"
        chave.save()
        group = Group.objects.get_or_create(name='paciente')
        group = Group.objects.get(name='paciente')
        user.groups.add(group)
        paciente = Paciente()
        paciente.usuario = user
        paciente.email = form_data[0]['username']
        paciente.nome = form_data[0]['nome']
        paciente.nascimento = form_data[0]['nascimento']
        paciente.sexo = form_data[0]['sexo']
        paciente.escolaridade = form_data[0]['escolaridade']
        paciente.retornos=0
        paciente.save()
        familia = Familia()
        familia.paciente = paciente
        familia.parente = "conjuge"
        familia.nome = form_data[1]['nomeConjuge']
        familia.nascimento = form_data[1]['nascimentoConjuge']
        familia.sexo = form_data[1]['sexoConjuge']
        familia.escolaridade = form_data[1]['escolaridadeConjuge']
        familia.save()
        familia = Familia()
        familia.paciente = paciente
        familia.parente = "pai"
        familia.nome = form_data[2]['nomePai']
        familia.nascimento = form_data[2]['nascimentoPai']
        familia.falecimento = form_data[2]['falecimentoPai']
        familia.escolaridade = form_data[2]['escolaridadePai']
        familia.save()
        familia = Familia()
        familia.paciente = paciente
        familia.parente = "mae"
        familia.nome = form_data[3]['nomeMae']
        familia.nascimento = form_data[3]['nascimentoMae']
        familia.falecimento = form_data[3]['falecimentoMae']
        familia.escolaridade = form_data[3]['escolaridadeMae']
        familia.save()
        familia = Familia()
        familia.paciente = paciente
        familia.parente = "avoPaterno"
        familia.nome = form_data[4]['nomeAvoPaterno']
        familia.nascimento = form_data[4]['nascimentoAvoPaterno']
        familia.falecimento = form_data[4]['falecimentoAvoPaterno']
        familia.escolaridade = form_data[4]['escolaridadeAvoPaterno']
        familia.save()
        familia = Familia()
        familia.paciente = paciente
        familia.parente = "avoPaterna"
        familia.nome = form_data[5]['nomeAvoPaterna']
        familia.nascimento = form_data[5]['nascimentoAvoPaterna']
        familia.falecimento = form_data[5]['falecimentoAvoPaterna']
        familia.escolaridade = form_data[5]['escolaridadeAvoPaterna']
        familia.save()
        familia = Familia()
        familia.paciente = paciente
        familia.parente = "avoMaterno"
        familia.nome = form_data[6]['nomeAvoMaterno']
        familia.nascimento = form_data[6]['nascimentoAvoMaterno']
        familia.falecimento = form_data[6]['falecimentoAvoMaterno']
        familia.escolaridade = form_data[6]['escolaridadeAvoMaterno']
        familia.save()
        familia = Familia()
        familia.paciente = paciente
        familia.parente = "avoMaterna"
        familia.nome = form_data[7]['nomeAvoMaterna']
        familia.nascimento = form_data[7]['nascimentoAvoMaterna']
        familia.falecimento = form_data[7]['falecimentoAvoMaterna']
        familia.escolaridade = form_data[7]['escolaridadeAvoMaterna']
        familia.save()

        return redirect(CadastroRealizado)


def CadastroRealizado(request):
    return render(request, 'projetofinal/cadastrado.html', {})

def EdicaoRealizada(request):
    return render(request, 'projetofinal/editado.html', {})

class EditarCadastro(SessionWizardView):
    template_name = "projetofinal/editar.html"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(EditarCadastro, self).dispatch(*args, **kwargs)

    def paciente(self):
        if 'paciente_id' in self.kwargs:
            paciente_id = self.kwargs['paciente_id']
        paciente = Paciente.objects.get(usuario_id=paciente_id)
        return paciente

    def get_form(self, step=None, data=None, files=None):

        if 'paciente_id' in self.kwargs:
                paciente_id = self.kwargs['paciente_id']
                try:
                    paciente = Paciente.objects.get(usuario_id=paciente_id)
                except Paciente.DoesNotExist:
                    raise Http404("Paciente não existe")
        # determine the step if not given
        if step is None:
            step = self.steps.current

        if step == "0":
            form = EdicaoPaciente(paciente_id=paciente_id, data=data)
            return form
        if step == "1":
            familia = Familia.objects.get(paciente_id=paciente.id,parente="conjuge")
            form = CadastroConjuge(data= data,initial = { "nomeConjuge":familia.nome,"nascimentoConjuge":familia.nascimento,
                                             "sexoConjuge":familia.sexo,"escolaridadeConjuge":familia.escolaridade})
            return form
        if step == "2":
            familia = Familia.objects.get(paciente_id=paciente.id,parente="pai")
            form = CadastroPai(data=data,initial = { "nomePai":familia.nome,"nascimentoPai":familia.nascimento,
                                             "falecimentoPai":familia.falecimento,"escolaridadePai":familia.escolaridade})
            return form
        if step == "3":
            familia = Familia.objects.get(paciente_id=paciente.id,parente="mae")
            form = CadastroMae(data=data,initial = { "nomeMae":familia.nome,"nascimentoMae":familia.nascimento,
                                             "falecimentoMae":familia.falecimento,"escolaridadeMae":familia.escolaridade})
            return form
        if step == "4":
            familia = Familia.objects.get(paciente_id=paciente.id,parente="avoPaterno")
            form = CadastroAvoPaterno(data=data,initial = { "nomeAvoPaterno":familia.nome,"nascimentoAvoPaterno":familia.nascimento,
                                             "falecimentoAvoPaterno":familia.falecimento,"escolaridadeAvoPaterno":familia.escolaridade})
            return form
        if step == "5":
            familia = Familia.objects.get(paciente_id=paciente.id,parente="avoPaterna")
            form = CadastroAvoPaterna(data=data,initial = { "nomeAvoPaterna":familia.nome,"nascimentoAvoPaterna":familia.nascimento,
                                             "falecimentoAvoPaterna":familia.falecimento,"escolaridadeAvoPaterna":familia.escolaridade})
            return form
        if step == "6":
            familia = Familia.objects.get(paciente_id=paciente.id,parente="avoMaterno")
            form = CadastroAvoMaterno(data=data,initial = { "nomeAvoMaterno":familia.nome,"nascimentoAvoMaterno":familia.nascimento,
                                             "falecimentoAvoMaterno":familia.falecimento,"escolaridadeAvoMaterno":familia.escolaridade})
            return form
        if step == "7":
            familia = Familia.objects.get(paciente_id=paciente.id,parente="avoMaterna")
            form = CadastroAvoMaterna(data=data,initial = { "nomeAvoMaterna":familia.nome,"nascimentoAvoMaterna":familia.nascimento,
                                             "falecimentoAvoMaterna":familia.falecimento,"escolaridadeAvoMaterna":familia.escolaridade})
            return form


    def done(self, form_list, form_dict, **kwargs):
        paciente_id = self.kwargs['paciente_id']
        paciente = Paciente.objects.get(usuario_id=paciente_id)
        form_data= [form.cleaned_data for form in form_list]
        paciente.nome = form_data[0]['nome']
        paciente.nascimento = form_data[0]['nascimento']
        paciente.sexo = form_data[0]['sexo']
        paciente.escolaridade = form_data[0]['escolaridade']
        paciente.save()
        familia = Familia.objects.get(paciente_id=paciente.id,parente="conjuge")
        familia.nome = form_data[1]['nomeConjuge']
        familia.nascimento = form_data[1]['nascimentoConjuge']
        familia.sexo = form_data[1]['sexoConjuge']
        familia.escolaridade = form_data[1]['escolaridadeConjuge']
        familia.save()
        familia = Familia.objects.get(paciente_id=paciente.id,parente="pai")
        familia.nome = form_data[2]['nomePai']
        familia.nascimento = form_data[2]['nascimentoPai']
        familia.falecimento = form_data[2]['falecimentoPai']
        familia.escolaridade = form_data[2]['escolaridadePai']
        familia.save()
        familia = Familia.objects.get(paciente_id=paciente.id,parente="mae")
        familia.nome = form_data[3]['nomeMae']
        familia.nascimento = form_data[3]['nascimentoMae']
        familia.falecimento = form_data[3]['falecimentoMae']
        familia.escolaridade = form_data[3]['escolaridadeMae']
        familia.save()
        familia = Familia.objects.get(paciente_id=paciente.id,parente="avoPaterno")
        familia.nome = form_data[4]['nomeAvoPaterno']
        familia.nascimento = form_data[4]['nascimentoAvoPaterno']
        familia.falecimento = form_data[4]['falecimentoAvoPaterno']
        familia.escolaridade = form_data[4]['escolaridadeAvoPaterno']
        familia.save()
        familia = Familia.objects.get(paciente_id=paciente.id,parente="avoPaterna")
        familia.nome = form_data[5]['nomeAvoPaterna']
        familia.nascimento = form_data[5]['nascimentoAvoPaterna']
        familia.falecimento = form_data[5]['falecimentoAvoPaterna']
        familia.escolaridade = form_data[5]['escolaridadeAvoPaterna']
        familia.save()
        familia = Familia.objects.get(paciente_id=paciente.id,parente="avoMaterno")
        familia.nome = form_data[6]['nomeAvoMaterno']
        familia.nascimento = form_data[6]['nascimentoAvoMaterno']
        familia.falecimento = form_data[6]['falecimentoAvoMaterno']
        familia.escolaridade = form_data[6]['escolaridadeAvoMaterno']
        familia.save()
        familia = Familia.objects.get(paciente_id=paciente.id,parente="avoMaterna")
        familia.nome = form_data[7]['nomeAvoMaterna']
        familia.nascimento = form_data[7]['nascimentoAvoMaterna']
        familia.falecimento = form_data[7]['falecimentoAvoMaterna']
        familia.escolaridade = form_data[7]['escolaridadeAvoMaterna']
        familia.save()
        return redirect(EdicaoRealizada)

class AtualizarChave(SessionWizardView):
    template_name = "projetofinal/chave.html"
    form_list = [AtualizarChave]

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(AtualizarChave, self).dispatch(*args, **kwargs)

    def paciente(self):
        if 'paciente_id' in self.kwargs:
            paciente_id = self.kwargs['paciente_id']
        paciente = Paciente.objects.get(usuario_id=paciente_id)
        return paciente

    def done(self, form_list, form_dict, **kwargs):
        form_data= [form.cleaned_data for form in form_list]
        paciente_id = self.kwargs['paciente_id']
        paciente = Paciente.objects.get(usuario_id=paciente_id)
        novachave=form_data[0]['chave']
        chave = Chave.objects.get(chave = novachave)
        paciente.retornos=0
        paciente.save()
        chave.padrao="usada"
        chave.save()
        return HttpResponseRedirect('/home/'+paciente_id)

class HabilitarPsicologo(SessionWizardView):
    template_name = "projetofinal/psicologo.html"
    form_list = [HabilitarPsicologo]

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(HabilitarPsicologo, self).dispatch(*args, **kwargs)

    def paciente(self):
        if 'paciente_id' in self.kwargs:
            paciente_id = self.kwargs['paciente_id']
        paciente = Paciente.objects.get(usuario_id=paciente_id)
        return paciente

    def done(self, form_list, form_dict, **kwargs):
        form_data= [form.cleaned_data for form in form_list]
        crp=form_data[0]['CRP']
        paciente_id = self.kwargs['paciente_id']
        paciente = Paciente.objects.get(usuario_id=paciente_id)
        psicologo = Psicologo.objects.get(codigo = crp)
        paciente.psicologo=psicologo
        paciente.save()
        return redirect(PsicologoHabilitado)

def PsicologoHabilitado(request):
    return render(request, 'projetofinal/habilitado.html', {})


class BuscarPsicologo(SessionWizardView):
    template_name = "projetofinal/busca.html"
    form_list=[BuscarPsicologo]

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(BuscarPsicologo, self).dispatch(*args, **kwargs)

    def paciente(self):
        if 'paciente_id' in self.kwargs:
            paciente_id = self.kwargs['paciente_id']
        paciente = Paciente.objects.get(usuario_id=paciente_id)
        return paciente

    def get_form_step_data(self, form):
        paciente_id = self.kwargs['paciente_id']
        paciente = Paciente.objects.get(usuario_id=paciente_id)

        return form.data

    def done(self, form_list, form_dict, **kwargs):

        return redirect(EdicaoRealizada)

#Classes do password-reset(esqueci a senha)

class SaltMixin(object):
    salt = 'password_recovery'
    url_salt = 'password_recovery_url'


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
    template_name = 'password_reset/reset_sent2.html'

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
    template_name = 'password_reset/recovery_form2.html'
    success_url_name = 'password_reset_sent'
    email_template_name = 'password_reset/recovery_email2.txt'
    email_subject_template_name = 'password_reset/recovery_email_subject2.txt'
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
    template_name = 'password_reset/reset2.html'
    success_url = reverse_lazy('password_reset_done')

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
    template_name = 'password_reset/recovery_done2.html'


reset_done = ResetDone.as_view()


