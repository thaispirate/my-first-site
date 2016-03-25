from django.shortcuts import render
from django.views.generic import CreateView, TemplateView, FormView
from django.core.urlresolvers import reverse_lazy
from .models import Paciente,User
from django.shortcuts import render_to_response
from formtools.wizard.views import SessionWizardView


# Create your views here.

def home(request):
    return render(request, 'projetofinal/home.html', {})


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
