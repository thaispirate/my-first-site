from datetime import datetime
import json
from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.models import User, Group
from .models import Paciente,User, Psicologo, AreaAfetiva, Anamnesia, RespostaAreaAfetiva, PerguntaAreaAfetiva
from formtools.wizard.views import SessionWizardView
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
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
from .forms import ConsultarAreaAfetiva

try:
    from django.contrib.sites.shortcuts import get_current_site
except ImportError:
    from django.contrib.sites.models import get_current_site

from .forms import PasswordRecoveryForm, PasswordResetForm
from .signals import user_recovers_password
from .utils import get_user_model, get_username
from django.contrib.auth import logout

# Create your views here.

#Views Paciente
def Home(request):
    return render(request, 'projetofinal/home.html', {})

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
                return HttpResponseRedirect('home')
            else:
                state = 1
        else:
            state = 2
    return render_to_response('projetofinal/login.html', {'state':state, 'username': username},context_instance=RequestContext(request))


def LogoutView(request):
    logout(request)
    return render(request, 'projetofinal/home.html', {})

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
        group = Group.objects.get(name='paciente')
        user.groups.add(group)
        paciente = Paciente()
        paciente.usuario = user
        paciente.email = form_data[0]['username']
        paciente.nome = form_data[0]['nome']
        paciente.nascimento = form_data[0]['nascimento']
        paciente.sexo = form_data[0]['sexo']
        paciente.escolaridade = form_data[0]['escolaridade']
        paciente.nomeConjuge = form_data[1]['nomeConjuge']
        paciente.nascimentoConjuge = form_data[1]['nascimentoConjuge']
        paciente.sexoConjuge = form_data[1]['sexoConjuge']
        paciente.escolaridadeConjuge = form_data[1]['escolaridadeConjuge']
        paciente.nomePai = form_data[2]['nomePai']
        paciente.nascimentoPai = form_data[2]['nascimentoPai']
        paciente.falecimentoPai = form_data[2]['falecimentoPai']
        paciente.escolaridadePai = form_data[2]['escolaridadePai']
        paciente.nomeMae = form_data[3]['nomeMae']
        paciente.nascimentoMae = form_data[3]['nascimentoMae']
        paciente.falecimentoMae = form_data[3]['falecimentoMae']
        paciente.escolaridadeMae = form_data[3]['escolaridadeMae']
        paciente.nomeAvoPaterno = form_data[4]['nomeAvoPaterno']
        paciente.nascimentoAvoPaterno = form_data[4]['nascimentoAvoPaterno']
        paciente.falecimentoAvoPaterno = form_data[4]['falecimentoAvoPaterno']
        paciente.escolaridadeAvoPaterno = form_data[4]['escolaridadeAvoPaterno']
        paciente.nomeAvoPaterna = form_data[5]['nomeAvoPaterna']
        paciente.nascimentoAvoPaterna = form_data[5]['nascimentoAvoPaterna']
        paciente.falecimentoAvoPaterna = form_data[5]['falecimentoAvoPaterna']
        paciente.escolaridadeAvoPaterna = form_data[5]['escolaridadeAvoPaterna']
        paciente.nomeAvoMaterno = form_data[6]['nomeAvoMaterno']
        paciente.nascimentoAvoMaterno = form_data[6]['nascimentoAvoMaterno']
        paciente.falecimentoAvoMaterno = form_data[6]['falecimentoAvoMaterno']
        paciente.escolaridadeAvoMaterno = form_data[6]['escolaridadeAvoMaterno']
        paciente.nomeAvoMaterna = form_data[7]['nomeAvoMaterna']
        paciente.nascimentoAvoMaterna = form_data[7]['nascimentoAvoMaterna']
        paciente.falecimentoAvoMaterna = form_data[7]['falecimentoAvoMaterna']
        paciente.escolaridadeAvoMaterna = form_data[7]['escolaridadeAvoMaterna']
        paciente.save()
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

    def get_form_initial(self, step):
        if 'paciente_id' in self.kwargs:
            paciente_id = self.kwargs['paciente_id']
            try:
                paciente = Paciente.objects.get(usuario_id=paciente_id)
            except Paciente.DoesNotExist:
                raise Http404("Paciente não existe")

            from django.forms.models import model_to_dict
            project_dict = model_to_dict(paciente)
            return project_dict
        else:
            return self.initial_dict.get(step, {})

    def done(self, form_list, form_dict, **kwargs):
        paciente_id = self.kwargs['paciente_id']
        paciente = Paciente.objects.get(usuario_id=paciente_id)
        form_data= [form.cleaned_data for form in form_list]
        paciente.nome = form_data[0]['nome']
        paciente.nascimento = form_data[0]['nascimento']
        paciente.sexo = form_data[0]['sexo']
        paciente.escolaridade = form_data[0]['escolaridade']
        paciente.nomeConjuge = form_data[1]['nomeConjuge']
        paciente.nascimentoConjuge = form_data[1]['nascimentoConjuge']
        paciente.sexoConjuge = form_data[1]['sexoConjuge']
        paciente.escolaridadeConjuge = form_data[1]['escolaridadeConjuge']
        paciente.nomePai = form_data[2]['nomePai']
        paciente.nascimentoPai = form_data[2]['nascimentoPai']
        paciente.falecimentoPai = form_data[2]['falecimentoPai']
        paciente.escolaridadePai = form_data[2]['escolaridadePai']
        paciente.nomeMae = form_data[3]['nomeMae']
        paciente.nascimentoMae = form_data[3]['nascimentoMae']
        paciente.falecimentoMae = form_data[3]['falecimentoMae']
        paciente.escolaridadeMae = form_data[3]['escolaridadeMae']
        paciente.nomeAvoPaterno = form_data[4]['nomeAvoPaterno']
        paciente.nascimentoAvoPaterno = form_data[4]['nascimentoAvoPaterno']
        paciente.falecimentoAvoPaterno = form_data[4]['falecimentoAvoPaterno']
        paciente.escolaridadeAvoPaterno = form_data[4]['escolaridadeAvoPaterno']
        paciente.nomeAvoPaterna = form_data[5]['nomeAvoPaterna']
        paciente.nascimentoAvoPaterna = form_data[5]['nascimentoAvoPaterna']
        paciente.falecimentoAvoPaterna = form_data[5]['falecimentoAvoPaterna']
        paciente.escolaridadeAvoPaterna = form_data[5]['escolaridadeAvoPaterna']
        paciente.nomeAvoMaterno = form_data[6]['nomeAvoMaterno']
        paciente.nascimentoAvoMaterno = form_data[6]['nascimentoAvoMaterno']
        paciente.falecimentoAvoMaterno = form_data[6]['falecimentoAvoMaterno']
        paciente.escolaridadeAvoMaterno = form_data[6]['escolaridadeAvoMaterno']
        paciente.nomeAvoMaterna = form_data[7]['nomeAvoMaterna']
        paciente.nascimentoAvoMaterna = form_data[7]['nascimentoAvoMaterna']
        paciente.falecimentoAvoMaterna = form_data[7]['falecimentoAvoMaterna']
        paciente.escolaridadeAvoMaterna = form_data[7]['escolaridadeAvoMaterna']
        paciente.save()
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
        timestamp = timezone.now() - datetime.timedelta(seconds=age)
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

#Views da Análise
class InserirAnalise(SessionWizardView):
    template_name = "projetofinal/analise/inserir.html"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(InserirAnalise, self).dispatch(*args, **kwargs)


    def done(self, form_list, form_dict, **kwargs):
        paciente_id = self.kwargs['paciente_id']
        paciente = Paciente.objects.get(usuario_id=paciente_id)
        form_data= [form.cleaned_data for form in form_list]
        anamnesia = Anamnesia()
        anamnesia.paciente = paciente
        A=[0]
        for item in form_data[0]:
            resposta = RespostaAreaAfetiva.objects.get(pergunta_id=int(item),letra=form_data[0][item])
            A.append(resposta.valor)

        afetivoRelacional=(A[1]+A[2]+A[4]+A[6]+A[9]+A[13]+A[15]+A[17]+A[19]+A[20]+A[21]+A[22]+A[23]+A[25]+A[28])/(15*0.8)
        produtividade=(A[5]+A[16]+A[20]+A[22]+A[23])/5
        organico=(A[7]+A[12]+A[14]+A[27]+A[29])/5
        espiritual=(A[3]+A[11]+A[18]+A[24]+A[26])/5
        socioCultural=(A[8]+A[10]+A[20]+A[22]+A[23])/5

        anamnesia.areaAfetiva= "Espiritual"
        if socioCultural >= espiritual:
            anamnesia.areaAfetiva= "Socio-Cultural"
        if afetivoRelacional >= socioCultural and anamnesia.areaAfetiva=="Socio-Cultural":
                anamnesia.areaAfetiva= "Afetivo-Relacional"
        if produtividade >= afetivoRelacional and anamnesia.areaAfetiva=="Afetivo-Relacional":
            anamnesia.areaAfetiva= "Produtividade"
        if organico >= produtividade and anamnesia.areaAfetiva=="Produtividade":
            anamnesia.areaAfetiva="Orgânico"

        anamnesia.inicio=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        anamnesia.save()

        for item in form_data[0]:
            resposta = RespostaAreaAfetiva.objects.get(pergunta_id=int(item),letra=form_data[0][item])
            areaAfetiva = AreaAfetiva()
            areaAfetiva.paciente = paciente
            areaAfetiva.resposta = resposta
            areaAfetiva.anamnesia = anamnesia
            areaAfetiva.save()

        return redirect(AnaliseIniciada)

def AnaliseIniciada(request):
    return render(request, 'projetofinal/analise/inserida.html', {})

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

    def grafico(self):
        if 'paciente_id' in self.kwargs:
            paciente_id = self.kwargs['paciente_id']
        paciente = Paciente.objects.get(usuario_id=paciente_id)
        dados = {
        }
        anamnesia = Anamnesia.objects.filter(paciente_id=paciente.id)
        for analise in anamnesia:
            area= AreaAfetiva.objects.filter(anamnesia_id=analise.id)
            A=[0]
            for respostas in area:
                resposta = RespostaAreaAfetiva.objects.get(id=respostas.resposta_id)
                A.append(resposta.valor)
            afetivoRelacional=((A[1]+A[2]+A[4]+A[6]+A[9]+A[13]+A[15]+A[17]+A[19]+A[20]+A[21]+A[22]+A[23]+A[25]+A[28])/(15*0.8))*10
            produtividade=((A[5]+A[16]+A[20]+A[22]+A[23])/5)*10
            organico=((A[7]+A[12]+A[14]+A[27]+A[29])/5)*10
            espiritual=((A[3]+A[11]+A[18]+A[24]+A[26])/5)*10
            socioCultural=((A[8]+A[10]+A[20]+A[22]+A[23])/5)*10
            dados[str(analise.inicio)] = [afetivoRelacional]
            dados[str(analise.inicio)].append(produtividade)
            dados[str(analise.inicio)].append(organico)
            dados[str(analise.inicio)].append(espiritual)
            dados[str(analise.inicio)].append(socioCultural)


        grafico = simplejson.dumps(dados)
        return grafico

class ConsultandoAnalise(SessionWizardView):
    template_name = "projetofinal/analise/consultando.html"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ConsultandoAnalise, self).dispatch(*args, **kwargs)

    def get_form(self, step=None, data=None, files=None):
        form = super(ConsultandoAnalise, self).get_form(step, data, files)

        # determine the step if not given
        if step is None:
            step = self.steps.current

        if step == "0":
            if 'paciente_id' in self.kwargs:
                paciente_id = self.kwargs['paciente_id']
                try:
                    paciente = Paciente.objects.get(usuario_id=paciente_id)
                except Paciente.DoesNotExist:
                    raise Http404("Paciente não existe")
                if 'analise_id' in self.kwargs:
                    analise_id = self.kwargs['analise_id']
                try:
                    analise = AreaAfetiva.objects.filter(anamnesia_id=analise_id)
                except Anamnesia.DoesNotExist:
                    raise Http404("Análise não existe")
            form = ConsultarAreaAfetiva(analise_id=analise_id, data=data)

        return form


@login_required()
def RemoverAnalise(request, paciente_id):

    if request.POST:
        analise = request.POST['analise']
    Anamnesia.objects.filter(id=analise).delete()
    AreaAfetiva.objects.filter(anamnesia_id=analise).delete()
    return render(request,"projetofinal/analise/removida.html")




#Views do Psicólogo
def PsicologoAdministracao(request):
    return render(request, 'projetofinal/psicologo/administracao.html', {})

def LoginPsicologo(request):
    username = password = ''
    state="please log in"
    if request.POST:
        username = request.POST['username']
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
        user.first_name = form_data[0]['nome']
        user.save()
        group = Group.objects.get(name='psicologo')
        user.groups.add(group)
        psicologo = Psicologo()
        psicologo.usuario = user
        psicologo.email = form_data[0]['username']
        psicologo.nome = form_data[0]['nome']
        psicologo.save()
        return redirect(CadastroPsicologoRealizado)

def CadastroPsicologoRealizado(request):
    return render(request, 'projetofinal/psicologo/cadastrado.html', {})

@login_required()
def PsicologoHome(request):
    paciente = Paciente.objects.all()
    return render(request, 'projetofinal/psicologo/home.html', {'pacientes':paciente})


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
            area= AreaAfetiva.objects.filter(anamnesia_id=analise.id)
            A=[0]
            for respostas in area:
                resposta = RespostaAreaAfetiva.objects.get(id=respostas.resposta_id)
                A.append(resposta.valor)
            afetivoRelacional=((A[1]+A[2]+A[4]+A[6]+A[9]+A[13]+A[15]+A[17]+A[19]+A[20]+A[21]+A[22]+A[23]+A[25]+A[28])/(15*0.8))*10
            produtividade=((A[5]+A[16]+A[20]+A[22]+A[23])/5)*10
            organico=((A[7]+A[12]+A[14]+A[27]+A[29])/5)*10
            espiritual=((A[3]+A[11]+A[18]+A[24]+A[26])/5)*10
            socioCultural=((A[8]+A[10]+A[20]+A[22]+A[23])/5)*10
            dados[str(analise.inicio)] = [afetivoRelacional]
            dados[str(analise.inicio)].append(produtividade)
            dados[str(analise.inicio)].append(organico)
            dados[str(analise.inicio)].append(espiritual)
            dados[str(analise.inicio)].append(socioCultural)


        grafico = simplejson.dumps(dados)
        return grafico

class ConsultandoAnalisePaciente(SessionWizardView):
    template_name = "projetofinal/psicologo/paciente/consultando.html"

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

        # determine the step if not given
        if step is None:
            step = self.steps.current

        if step == "0":
            if 'paciente_id' in self.kwargs:
                paciente_id = self.kwargs['paciente_id']
                try:
                    paciente = Paciente.objects.get(usuario_id=paciente_id)
                except Paciente.DoesNotExist:
                    raise Http404("Paciente não existe")
                if 'analise_id' in self.kwargs:
                    analise_id = self.kwargs['analise_id']
                try:
                    analise = AreaAfetiva.objects.filter(anamnesia_id=analise_id)
                except Anamnesia.DoesNotExist:
                    raise Http404("Análise não existe")
            form = ConsultarAreaAfetiva(analise_id=analise_id, data=data)

        return form