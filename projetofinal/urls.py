from django.conf.urls import include, url, patterns
from . import views
from .forms import Cadastro1Form, Cadastro2Form, Cadastro3Form, Cadastro4Form, Cadastro5Form, Cadastro6Form, Cadastro7Form, Cadastro8Form
from .views import CadastroRealizado,CadastroWizard, EditarCadastro

urlpatterns = [
    url(r'^$', views.home),
    url(r'^home$', views.home),
    url(r'^cadastro$', CadastroWizard.as_view([Cadastro1Form,Cadastro2Form,Cadastro3Form,Cadastro4Form,Cadastro5Form,Cadastro6Form,Cadastro7Form,Cadastro8Form]), name="cadastro"),
    url(r'^cadastrado$', CadastroRealizado.as_view(), name="cadastro_realizado"),
    url(r'^login$', 'django.contrib.auth.views.login', {'template_name':'projetofinal/login.html'}, name='login'),
    url(r'^editar$', EditarCadastro.as_view([Cadastro1Form,Cadastro2Form,Cadastro3Form,Cadastro4Form,Cadastro5Form,Cadastro6Form,Cadastro7Form,Cadastro8Form]), name="editar"),
    url(r'^sair/$', 'django.contrib.auth.views.logout_then_login', name='logout')
]
