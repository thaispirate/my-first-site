from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit, HTML, Button, Row, Field
from crispy_forms.bootstrap import AppendedText, PrependedText, FormActions
from django import forms
from django.utils.translation import ugettext, ugettext_lazy as _

class UserCreationForm(forms.ModelForm):
    """
    A form that creates a user, with no privileges, from the given username and
    password.
    """
    error_messages = {
        'duplicate_username': _("Já existe um usuário com este nome."),
        'password_mismatch': _("As senhas precisam ser iguais"),
    }
    username = forms.RegexField(label=_("Usuario"), max_length=30,
        regex=r'^[\w.@+-]+$',
        help_text=_("Ate 30 caracteres que podem ser letras, numeros ou "
                    "@/./+/-/_"),
        error_messages={
            'invalid': _("Este campo só deve conter letras,numeros e os seguintes caracteres "
                         "@/./+/-/_"),
            'required': _("Este campo é obrigatório")
        })
    password1 = forms.CharField(label=_("Senha"),
        widget=forms.PasswordInput,
        error_messages={
            'required': _("Este campo é obrigatório")
        })
    password2 = forms.CharField(label=_("Confirmação da senha"),
        widget=forms.PasswordInput,
        help_text=_("Escreva a mesma senha para confirmação"),
        error_messages={
            'required': _("Este campo é obrigatório")
        })

    class Meta:
        model = User
        fields = ("username",)

    def clean_username(self):
        # Since User.username is unique, this check is redundant,
        # but it sets a nicer error message than the ORM. See #13147.
        username = self.cleaned_data["username"]
        try:
            User._default_manager.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(
            self.error_messages['duplicate_username'],
            code='duplicate_username',
        )

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class Cadastro1Form(UserCreationForm):

    class Meta():
        model = User
        fields=['username','password1','password2']
        error_messages = {
            'password1': {
                'required': "Please enter your first password",
            },
             'password2': {
                 'required': "Please enter your second password.",
            },
         }


    email = forms.EmailField(label="Email",error_messages={'required':'Este campo é obrigatório'})
    nome = forms.CharField(label="Nome",error_messages={'required':'Este campo é obrigatório'})
    nascimento = forms.DateField(
        label="Data de Nascimento",
        input_formats=["%d/%m/%Y",],
        widget=forms.DateInput(format='%d/%m/%Y'),
        help_text= "DD/MM/AAAA",
        error_messages={'required':'Este campo é obrigatório'}
    )

    sexo = forms.ChoiceField(
        label="Sexo",
        choices = (
            ('Feminino', "Feminino"),
            ('Masculino', "Masculino")
        ),
        widget = forms.RadioSelect,
        initial = 'Feminino',
    )

    escolaridade = forms.ChoiceField(
        label="Escolaridade",
        choices = (
            ('Fundamental', "Fundamental"),
            ('Básico', "Básico"),
            ('Técnico', 'Técnico'),
            ('Superior', 'Superior'),
            ('Pós-graduado','Pós-graduado')
        ),
        widget = forms.RadioSelect,
        initial = 'Fundamental',
    )

class Cadastro2Form(forms.Form):
    nomeConjuge = forms.CharField(required=False,label="Primeiro nome do Cônjuge")
    nascimentoConjuge = forms.DateField(
        label="Data de Nascimento do Cônjuge",
        required=False,
        input_formats=["%d/%m/%Y",],
        widget=forms.DateInput(format='%d/%m/%Y'),
        help_text= "DD/MM/AAAA",
    )

    sexoConjuge = forms.ChoiceField(
        label="Sexo do Cônjuge",
        choices = (
            ('Feminino', "Feminino"),
            ('Masculino', "Masculino")
        ),
        widget = forms.RadioSelect,
        initial = 'Feminino',
    )
    escolaridadeConjuge = forms.ChoiceField(
        label="Escolaridade do Cônjuge",
        choices = (
            ('Fundamental', "Fundamental"),
            ('Básico', "Básico"),
            ('Técnico', 'Técnico'),
            ('Superior', 'Superior'),
            ('Pós-graduado','Pós-graduado')
        ),
        widget = forms.RadioSelect,
        initial = 'Fundamental',
    )

class Cadastro3Form(forms.Form):
    nomePai = forms.CharField(label="Primeiro nome do Pai",error_messages={'required':'Este campo é obrigatório'})
    nascimentoPai = forms.DateField(
        label="Data de Nascimento do Pai",
        input_formats=["%d/%m/%Y",],
        widget=forms.DateInput(format='%d/%m/%Y'),
        help_text= "DD/MM/AAAA",
        error_messages={'required':'Este campo é obrigatório'}
    )
    falecimentoPai = forms.DateField(
        label="Data de falecimento do Pai",
        required=False,
        input_formats=["%d/%m/%Y",],
        widget=forms.DateInput(format='%d/%m/%Y'),
        help_text= "DD/MM/AAAA",
    )
    escolaridadePai = forms.ChoiceField(
        label="Escolaridade do Pai",
        choices = (
            ('Fundamental', "Fundamental"),
            ('Básico', "Básico"),
            ('Técnico', 'Técnico'),
            ('Superior', 'Superior'),
            ('Pós-graduado','Pós-graduado')
        ),
        widget = forms.RadioSelect,
        initial = 'Fundamental',
    )

class Cadastro4Form(forms.Form):
    nomeMae = forms.CharField(label="Primeiro nome da Mãe",error_messages={'required':'Este campo é obrigatório'})
    nascimentoMae = forms.DateField(
        label="Data de Nascimento da Mãe",
        input_formats=["%d/%m/%Y",],
        widget=forms.DateInput(format='%d/%m/%Y'),
        help_text= "DD/MM/AAAA",
        error_messages={'required':'Este campo é obrigatório'}
    )
    falecimentoMae = forms.DateField(
        label="Data de falecimento da Mãe",
        required=False,
        input_formats=["%d/%m/%Y",],
        widget=forms.DateInput(format='%d/%m/%Y'),
        help_text= "DD/MM/AAAA",
    )
    escolaridadeMae = forms.ChoiceField(
        label="Escolaridade da Mãe",
        choices = (
            ('Fundamental', "Fundamental"),
            ('Básico', "Básico"),
            ('Técnico', 'Técnico'),
            ('Superior', 'Superior'),
            ('Pós-graduado','Pós-graduado')
        ),
        widget = forms.RadioSelect,
        initial = 'Fundamental',
    )

class Cadastro5Form(forms.Form):
    nomeAvoPaterno = forms.CharField(label="Primeiro nome do Avô Paterno",error_messages={'required':'Este campo é obrigatório'})
    nascimentoAvoPaterno = forms.DateField(
        label="Data de Nascimento do Avô Paterno",
        input_formats=["%d/%m/%Y",],
        widget=forms.DateInput(format='%d/%m/%Y'),
        help_text= "DD/MM/AAAA",
        error_messages={'required':'Este campo é obrigatório'}
    )
    falecimentoAvoPaterno = forms.DateField(
        label="Data de falecimento do Avô Paterno",
        required=False,
        input_formats=["%d/%m/%Y",],
        widget=forms.DateInput(format='%d/%m/%Y'),
        help_text= "DD/MM/AAAA",
    )
    escolaridadeAvoPaterno = forms.ChoiceField(
        label="Escolaridade do Avô Paterno",
        choices = (
            ('Fundamental', "Fundamental"),
            ('Básico', "Básico"),
            ('Técnico', 'Técnico'),
            ('Superior', 'Superior'),
            ('Pós-graduado','Pós-graduado')
        ),
        widget = forms.RadioSelect,
        initial = 'Fundamental',
    )

class Cadastro6Form(forms.Form):
    nomeAvoPaterna = forms.CharField(label="Primeiro nome da Avó Paterna",error_messages={'required':'Este campo é obrigatório'})
    nascimentoAvoPaterna = forms.DateField(
        label="Data de Nascimento da Avó Paterna",
        input_formats=["%d/%m/%Y",],
        widget=forms.DateInput(format='%d/%m/%Y'),
        help_text= "DD/MM/AAAA",
        error_messages={'required':'Este campo é obrigatório'}
    )
    falecimentoAvoPaterna = forms.DateField(
        label="Data de falecimento da Avó Paterna",
        required=False,
        input_formats=["%d/%m/%Y",],
        widget=forms.DateInput(format='%d/%m/%Y'),
        help_text= "DD/MM/AAAA",
    )
    escolaridadeAvoPaterna = forms.ChoiceField(
        label="Escolaridade da Avó Paterna",
        choices = (
            ('Fundamental', "Fundamental"),
            ('Básico', "Básico"),
            ('Técnico', 'Técnico'),
            ('Superior', 'Superior'),
            ('Pós-graduado','Pós-graduado')
        ),
        widget = forms.RadioSelect,
        initial = 'Fundamental',
    )

class Cadastro7Form(forms.Form):
    nomeAvoMaterno = forms.CharField(label="Primeiro nome do Avô Materno",error_messages={'required':'Este campo é obrigatório'})
    nascimentoAvoMaterno = forms.DateField(
        label="Data de Nascimento do Avô Materno",
        input_formats=["%d/%m/%Y",],
        widget=forms.DateInput(format='%d/%m/%Y'),
        help_text= "DD/MM/AAAA",
        error_messages={'required':'Este campo é obrigatório'}
    )
    falecimentoAvoMaterno = forms.DateField(
        label="Data de falecimento do Avô Materno",
        required=False,
        input_formats=["%d/%m/%Y",],
        widget=forms.DateInput(format='%d/%m/%Y'),
        help_text= "DD/MM/AAAA",
    )
    escolaridadeAvoMaterno = forms.ChoiceField(
        label="Escolaridade do Avô Materno",
        choices = (
            ('Fundamental', "Fundamental"),
            ('Básico', "Básico"),
            ('Técnico', 'Técnico'),
            ('Superior', 'Superior'),
            ('Pós-graduado','Pós-graduado')
        ),
        widget = forms.RadioSelect,
        initial = 'Fundamental',
    )

class Cadastro8Form(forms.Form):
    nomeAvoMaterna = forms.CharField(label="Primeiro nome da Avó Materna",error_messages={'required':'Este campo é obrigatório'})
    nascimentoAvoMaterna = forms.DateField(
        label="Data de Nascimento da Avó Materna",
        input_formats=["%d/%m/%Y",],
        widget=forms.DateInput(format='%d/%m/%Y'),
        help_text= "DD/MM/AAAA",
        error_messages={'required':'Este campo é obrigatório'}
    )
    falecimentoAvoMaterna = forms.DateField(
        label="Data de falecimento da Avó Materna",
        required=False,
        input_formats=["%d/%m/%Y",],
        widget=forms.DateInput(format='%d/%m/%Y'),
        help_text= "DD/MM/AAAA",
    )
    escolaridadeAvoMaterna = forms.ChoiceField(
        label="Escolaridade da Avó Materna",
        choices = (
            ('Fundamental', "Fundamental"),
            ('Básico', "Básico"),
            ('Técnico', 'Técnico'),
            ('Superior', 'Superior'),
            ('Pós-graduado','Pós-graduado')
        ),
        widget = forms.RadioSelect,
        initial = 'Fundamental',
    )