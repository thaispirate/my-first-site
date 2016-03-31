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
