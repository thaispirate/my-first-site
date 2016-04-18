from django.shortcuts import render
from django.views.generic import TemplateView
from .models import Paciente,User
from .forms import Cadastro1Form
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from django.utils.translation import ugettext as _
from formtools.wizard.views import SessionWizardView
from django.http import Http404
from django.template import RequestContext
from django.contrib.auth.views import password_reset

import datetime

from django.conf import settings
from django.core import signing
from django.core.mail import send_mail
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.template import loader
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views import generic
from django.views.decorators.debug import sensitive_post_parameters

try:
    from django.contrib.sites.shortcuts import get_current_site
except ImportError:
    from django.contrib.sites.models import get_current_site

from .forms import PasswordRecoveryForm, PasswordResetForm
from .signals import user_recovers_password
from .utils import get_user_model, get_username


# Create your views here.
def home(request):
    return render(request, 'projetofinal/home.html', {})

def erro404(request):
    return render(request,'404.html')

class CadastroWizard(SessionWizardView):
    template_name = "projetofinal/cadastro.html"

    def done(self, form_list, form_dict, **kwargs):
        form_data= [form.cleaned_data for form in form_list]
        user = User()
        user.username = form_data[0]['username']
        user.set_password(form_data[0]['password1'])
        user.email = form_data[0]['email']
        user.save()
        paciente = Paciente()
        paciente.usuario = user
        paciente.email = form_data[0]['email']
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
        return render_to_response('projetofinal/cadastrado.html')

class CadastroRealizado(TemplateView):
    template_name = "projetofinal/cadastrado.html"


class PacienteNaoExiste(TemplateView):
    template_name = "projetofinal/paciente_invalido.html"

class EditarCadastro(SessionWizardView):
    template_name = "projetofinal/editar.html"

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
        paciente.email = form_data[0]['email']
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
        return render_to_response('projetofinal/cadastrado.html')

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