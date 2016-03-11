from django.shortcuts import render
from django.views.generic import CreateView, TemplateView, FormView
from django.core.urlresolvers import reverse_lazy
from .forms import UserForm, MessageForm
from .models import Paciente

# Create your views here.

def home(request):
    return render(request, 'projetofinal/home.html', {})


class CadastrarPaciente(FormView):
    template_name = "projetofinal/cadastro.html"
    form_class = MessageForm
    success_url = reverse_lazy('cadastro_realizado')

    def form_valid(self, form):
        user = form.save()
        paciente = Paciente()
        paciente.usuario = user
        paciente.email = form.cleaned_data['email']
        paciente.nome = form.cleaned_data['nome']
        paciente.nascimento = form.cleaned_data['nascimento']
        paciente.sexo = form.cleaned_data['sexo']
        paciente.save()
        return super(CadastrarPaciente, self).form_valid(form)

class CadastroRealizado(TemplateView):
    template_name = "projetofinal/cadastrado.html"

    