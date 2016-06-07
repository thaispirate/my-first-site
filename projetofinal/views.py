from datetime import datetime
import json
from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.models import User, Group
from .forms import ConsultarAreaAfetiva,CadastroPaciente,CadastroConjuge,CadastroPai,CadastroMae,CadastroAvoPaterno,\
    CadastroAvoPaterna,CadastroAvoMaterno,CadastroAvoMaterna,EdicaoPaciente, IniciarAreaAfetiva,\
    RelacionamentoAvosMaternos, RelacionamentoAvoMaternoAntes, RelacionamentoAvoMaternaAntes, RelacionamentoAvosMaternosDepois,\
    RelacionamentoAvosPaternos, RelacionamentoAvoPaternoAntes, RelacionamentoAvoPaternaAntes, RelacionamentoAvosPaternosDepois,\
    RelacionamentoPais, RelacionamentoPaiAntes,RelacionamentoMaeAntes,RelacionamentoPaisDepois, RelacionamentoPaciente,\
    RelacionamentoPacienteAntes, RelacionamentoConjugeAntes, RelacionamentoPacienteDepois
from .models import Paciente,User,Familia, Psicologo, AreaAfetiva, Anamnesia, RespostaAreaAfetiva, Relacionamento
from formtools.wizard.views import SessionWizardView
from django.http import Http404, HttpResponseRedirect, HttpResponse
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

# Create your views here.

#Views Paciente

def is_member(user):
    return user.groups.filter(name='paciente').exists()

@user_passes_test(is_member)
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
        paciente.save()
        familia = Familia()
        familia.usuario = paciente
        familia.parente = "conjuge"
        familia.nome = form_data[1]['nomeConjuge']
        familia.nascimento = form_data[1]['nascimentoConjuge']
        familia.sexo = form_data[1]['sexoConjuge']
        familia.escolaridade = form_data[1]['escolaridadeConjuge']
        familia.save()
        familia = Familia()
        familia.usuario = paciente
        familia.parente = "pai"
        familia.nome = form_data[2]['nomePai']
        familia.nascimento = form_data[2]['nascimentoPai']
        familia.falecimento = form_data[2]['falecimentoPai']
        familia.escolaridade = form_data[2]['escolaridadePai']
        familia.save()
        familia = Familia()
        familia.usuario = paciente
        familia.parente = "mae"
        familia.nome = form_data[3]['nomeMae']
        familia.nascimento = form_data[3]['nascimentoMae']
        familia.falecimento = form_data[3]['falecimentoMae']
        familia.escolaridade = form_data[3]['escolaridadeMae']
        familia.save()
        familia = Familia()
        familia.usuario = paciente
        familia.parente = "avoPaterno"
        familia.nome = form_data[4]['nomeAvoPaterno']
        familia.nascimento = form_data[4]['nascimentoAvoPaterno']
        familia.falecimento = form_data[4]['falecimentoAvoPaterno']
        familia.escolaridade = form_data[4]['escolaridadeAvoPaterno']
        familia.save()
        familia = Familia()
        familia.usuario = paciente
        familia.parente = "avoPaterna"
        familia.nome = form_data[5]['nomeAvoPaterna']
        familia.nascimento = form_data[5]['nascimentoAvoPaterna']
        familia.falecimento = form_data[5]['falecimentoAvoPaterna']
        familia.escolaridade = form_data[5]['escolaridadeAvoPaterna']
        familia.save()
        familia = Familia()
        familia.usuario = paciente
        familia.parente = "avoMaterno"
        familia.nome = form_data[6]['nomeAvoMaterno']
        familia.nascimento = form_data[6]['nascimentoAvoMaterno']
        familia.falecimento = form_data[6]['falecimentoAvoMaterno']
        familia.escolaridade = form_data[6]['escolaridadeAvoMaterno']
        familia.save()
        familia = Familia()
        familia.usuario = paciente
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
            familia = Familia.objects.get(usuario_id=paciente.id,parente="conjuge")
            form = CadastroConjuge(data= data,initial = { "nomeConjuge":familia.nome,"nascimentoConjuge":familia.nascimento,
                                             "sexoConjuge":familia.sexo,"escolaridadeConjuge":familia.escolaridade})
            return form
        if step == "2":
            familia = Familia.objects.get(usuario_id=paciente.id,parente="pai")
            form = CadastroPai(data=data,initial = { "nomePai":familia.nome,"nascimentoPai":familia.nascimento,
                                             "falecimentoPai":familia.falecimento,"escolaridadePai":familia.escolaridade})
            return form
        if step == "3":
            familia = Familia.objects.get(usuario_id=paciente.id,parente="mae")
            form = CadastroMae(data=data,initial = { "nomeMae":familia.nome,"nascimentoMae":familia.nascimento,
                                             "falecimentoMae":familia.falecimento,"escolaridadeMae":familia.escolaridade})
            return form
        if step == "4":
            familia = Familia.objects.get(usuario_id=paciente.id,parente="avoPaterno")
            form = CadastroAvoPaterno(data=data,initial = { "nomeAvoPaterno":familia.nome,"nascimentoAvoPaterno":familia.nascimento,
                                             "falecimentoAvoPaterno":familia.falecimento,"escolaridadeAvoPaterno":familia.escolaridade})
            return form
        if step == "5":
            familia = Familia.objects.get(usuario_id=paciente.id,parente="avoPaterna")
            form = CadastroAvoPaterna(data=data,initial = { "nomeAvoPaterna":familia.nome,"nascimentoAvoPaterna":familia.nascimento,
                                             "falecimentoAvoPaterna":familia.falecimento,"escolaridadeAvoPaterna":familia.escolaridade})
            return form
        if step == "6":
            familia = Familia.objects.get(usuario_id=paciente.id,parente="avoMaterno")
            form = CadastroAvoMaterno(data=data,initial = { "nomeAvoMaterno":familia.nome,"nascimentoAvoMaterno":familia.nascimento,
                                             "falecimentoAvoMaterno":familia.falecimento,"escolaridadeAvoMaterno":familia.escolaridade})
            return form
        if step == "7":
            familia = Familia.objects.get(usuario_id=paciente.id,parente="avoMaterna")
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
        familia = Familia.objects.get(usuario_id=paciente.id,parente="conjuge")
        familia.nome = form_data[1]['nomeConjuge']
        familia.nascimento = form_data[1]['nascimentoConjuge']
        familia.sexo = form_data[1]['sexoConjuge']
        familia.escolaridade = form_data[1]['escolaridadeConjuge']
        familia.save()
        familia = Familia.objects.get(usuario_id=paciente.id,parente="pai")
        familia.nome = form_data[2]['nomePai']
        familia.nascimento = form_data[2]['nascimentoPai']
        familia.falecimento = form_data[2]['falecimentoPai']
        familia.escolaridade = form_data[2]['escolaridadePai']
        familia.save()
        familia = Familia.objects.get(usuario_id=paciente.id,parente="mae")
        familia.nome = form_data[3]['nomeMae']
        familia.nascimento = form_data[3]['nascimentoMae']
        familia.falecimento = form_data[3]['falecimentoMae']
        familia.escolaridade = form_data[3]['escolaridadeMae']
        familia.save()
        familia = Familia.objects.get(usuario_id=paciente.id,parente="avoPaterno")
        familia.nome = form_data[4]['nomeAvoPaterno']
        familia.nascimento = form_data[4]['nascimentoAvoPaterno']
        familia.falecimento = form_data[4]['falecimentoAvoPaterno']
        familia.escolaridade = form_data[4]['escolaridadeAvoPaterno']
        familia.save()
        familia = Familia.objects.get(usuario_id=paciente.id,parente="avoPaterna")
        familia.nome = form_data[5]['nomeAvoPaterna']
        familia.nascimento = form_data[5]['nascimentoAvoPaterna']
        familia.falecimento = form_data[5]['falecimentoAvoPaterna']
        familia.escolaridade = form_data[5]['escolaridadeAvoPaterna']
        familia.save()
        familia = Familia.objects.get(usuario_id=paciente.id,parente="avoMaterno")
        familia.nome = form_data[6]['nomeAvoMaterno']
        familia.nascimento = form_data[6]['nascimentoAvoMaterno']
        familia.falecimento = form_data[6]['falecimentoAvoMaterno']
        familia.escolaridade = form_data[6]['escolaridadeAvoMaterno']
        familia.save()
        familia = Familia.objects.get(usuario_id=paciente.id,parente="avoMaterna")
        familia.nome = form_data[7]['nomeAvoMaterna']
        familia.nascimento = form_data[7]['nascimentoAvoMaterna']
        familia.falecimento = form_data[7]['falecimentoAvoMaterna']
        familia.escolaridade = form_data[7]['escolaridadeAvoMaterna']
        familia.save()
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
    form_list = [IniciarAreaAfetiva,
                 RelacionamentoAvosMaternos,RelacionamentoAvoMaternoAntes,
                 RelacionamentoAvoMaternaAntes,RelacionamentoAvosMaternosDepois,
                 RelacionamentoAvosPaternos,RelacionamentoAvoPaternoAntes,
                 RelacionamentoAvoPaternaAntes,RelacionamentoAvosPaternosDepois,
                 RelacionamentoPais,RelacionamentoPaiAntes,RelacionamentoMaeAntes,
                 RelacionamentoPaisDepois,RelacionamentoPaciente,
                 RelacionamentoPacienteAntes,RelacionamentoConjugeAntes,
                 RelacionamentoPacienteDepois]

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(InserirAnalise, self).dispatch(*args, **kwargs)

    def get_form_step_data(self, form):
        if form.data['inserir_analise-current_step'] == '1':
            if form.data['1-relacaoAvoMaternoAntes'] == "Não":
                for key, value in self.form_list.items():
                    if value == RelacionamentoAvoMaternoAntes:
                        self.form_list.pop(key)
            if form.data['1-relacaoAvoMaternaAntes'] == "Não":
                for key, value in self.form_list.items():
                    if value == RelacionamentoAvoMaternaAntes:
                        self.form_list.pop(key)
            if (form.data['1-relacao'] == "Casados") or (form.data['1-relacao'] == "Moram junto"):
                for key, value in self.form_list.items():
                    if value == RelacionamentoAvosMaternosDepois:
                        self.form_list.pop(key)
        if form.data['inserir_analise-current_step'] == '5':
            if form.data['5-relacaoAvoPaternoAntes'] == "Não":
                for key, value in self.form_list.items():
                    if value == RelacionamentoAvoPaternoAntes:
                        self.form_list.pop(key)
            if form.data['5-relacaoAvoPaternaAntes'] == "Não":
                for key, value in self.form_list.items():
                    if value == RelacionamentoAvoPaternaAntes:
                        self.form_list.pop(key)
            if (form.data['5-relacao'] == "Casados") or (form.data['5-relacao'] == "Moram junto"):
                for key, value in self.form_list.items():
                    if value == RelacionamentoAvosPaternosDepois:
                        self.form_list.pop(key)
        if form.data['inserir_analise-current_step'] == '9':
            if form.data['9-relacaoPaiAntes'] == "Não":
                for key, value in self.form_list.items():
                    if value == RelacionamentoPaiAntes:
                        self.form_list.pop(key)
            if form.data['9-relacaoMaeAntes'] == "Não":
                for key, value in self.form_list.items():
                    if value == RelacionamentoMaeAntes:
                        self.form_list.pop(key)
            if (form.data['9-relacao'] == "Casados") or (form.data['9-relacao'] == "Moram junto"):
                for key, value in self.form_list.items():
                    if value == RelacionamentoPaisDepois:
                        self.form_list.pop(key)
        if form.data['inserir_analise-current_step'] == '13':
            if form.data['13-relacaoPacienteAntes'] == "Não":
                for key, value in self.form_list.items():
                    if value == RelacionamentoPacienteAntes:
                        self.form_list.pop(key)
            if form.data['13-relacaoConjugeAntes'] == "Não":
                for key, value in self.form_list.items():
                    if value == RelacionamentoConjugeAntes:
                        self.form_list.pop(key)
            if (form.data['13-relacao'] == "Casados") or (form.data['13-relacao'] == "Mora junto") or (form.data['13-relacao'] == "Não se aplica"):
                for key, value in self.form_list.items():
                    if value == RelacionamentoPacienteDepois:
                        self.form_list.pop(key)
        return form.data

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

        inicio=anamnesia.inicio=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        anamnesia.save()
        anamnesia = Anamnesia.objects.get(inicio=inicio)
        anamnesia_id = anamnesia.id

        for item in form_data[0]:
            resposta = RespostaAreaAfetiva.objects.get(pergunta_id=int(item),letra=form_data[0][item])
            areaAfetiva = AreaAfetiva()
            areaAfetiva.paciente = paciente
            areaAfetiva.resposta = resposta
            areaAfetiva.anamnesia = anamnesia
            areaAfetiva.save()

        parentes = ["AvoMaterno","AvoMaterna","AvoPaterno","AvoPaterna","Pai","Mae","Paciente","Conjuge"]
        contador = -1
        indice = -1

        for item in form_data:
            indice = indice +1
            if "relacao" in item:
                relacionamento = Relacionamento()
                relacionamento.paciente = paciente
                relacionamento.anamnesia = Anamnesia.objects.get(id = anamnesia_id,paciente_id=paciente.id)
                contador = contador +1
                relacionamento.parente=parentes[contador]
                relacionamento.relacao = form_data[indice]["relacao"]
                relacionamento.filhos = form_data[indice]["filhos"]
                relacionamento.filhas = form_data[indice]["filhas"]
                relacionamento.relacaoAntes = form_data[indice]["relacao"+parentes[contador]+"Antes"]
                relacionamento.save()
                relacionamento = Relacionamento()
                relacionamento.paciente = paciente
                relacionamento.anamnesia = Anamnesia.objects.get(id = anamnesia_id,paciente_id=paciente.id)
                contador = contador +1
                relacionamento.parente=parentes[contador]
                relacionamento.relacao = form_data[indice]["relacao"]
                relacionamento.filhos = form_data[indice]["filhos"]
                relacionamento.filhas = form_data[indice]["filhas"]
                relacionamento.relacaoAntes = form_data[indice]["relacao"+parentes[contador]+"Antes"]
                relacionamento.save()

        contador = -2
        indice = -1

        for item in form_data:
            indice = indice +1
            if "relacao" in item:
                contador = contador + 2
            if "filhos"+parentes[contador]+"Antes" in item:
                relacionamento = Relacionamento.objects.get(paciente_id = paciente.id, anamnesia_id = anamnesia_id,parente = parentes[contador])
                relacionamento.filhosAntes = form_data[indice]["filhos"+parentes[contador]+"Antes"]
                relacionamento.filhasAntes = form_data[indice]["filhas"+parentes[contador]+"Antes"]
                relacionamento.save()
            if "filhos"+parentes[contador+1]+"Antes" in item:
                relacionamento = Relacionamento.objects.get(paciente_id = paciente.id, anamnesia_id = anamnesia_id,parente = parentes[contador+1])
                relacionamento.filhosAntes = form_data[indice]["filhos"+parentes[contador+1]+"Antes"]
                relacionamento.filhasAntes = form_data[indice]["filhas"+parentes[contador+1]+"Antes"]
                relacionamento.save()

        contador = -2
        indice = -1

        for item in form_data:
            indice = indice +1
            if "relacao" in item:
                contador = contador +2
            if "filhos"+parentes[contador] in item:
                relacionamento = Relacionamento.objects.get(paciente_id = paciente.id, anamnesia_id = anamnesia_id,parente = parentes[contador])
                relacionamento.filhosDepois = form_data[indice]["filhos"+parentes[contador]]
                relacionamento.filhasDepois = form_data[indice]["filhas"+parentes[contador]]
                relacionamento.save()
            if "filhos"+parentes[contador+1] in item:
                relacionamento = Relacionamento.objects.get(paciente_id = paciente.id, anamnesia_id = anamnesia_id,parente = parentes[contador+1])
                relacionamento.filhosDepois = form_data[indice]["filhos"+parentes[contador+1]]
                relacionamento.filhasDepois = form_data[indice]["filhas"+parentes[contador+1]]
                relacionamento.save()



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
    form_list = [ConsultarAreaAfetiva,RelacionamentoAvosMaternos,
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
        return super(ConsultandoAnalise, self).dispatch(*args, **kwargs)

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
                analise = AreaAfetiva.objects.filter(anamnesia_id=analise_id)
            except Anamnesia.DoesNotExist:
                raise Http404("Análise não existe")


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
                print("aqui")
                print(self.form_list)
                print(self.steps.all)
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


@login_required()
def RemoverAnalise(request, paciente_id):

    if request.POST:
        analises = request.POST.getlist("analise")
    for analise in analises:
        Anamnesia.objects.filter(id=analise).delete()
        AreaAfetiva.objects.filter(anamnesia_id=analise).delete()
        Relacionamento.objects.filter(anamnesia_id=analise).delete()
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
        # determine the step if not given
        if step is None:
            step = self.steps.current

        if step == "0":
            form = ConsultarAreaAfetiva(analise_id=analise_id, data=data)

        return form