from django import forms
from .models import User,Paciente, Familia, PerguntaAreaAfetiva, RespostaAreaAfetiva, AreaAfetiva, Anamnesia
from django.contrib.auth.forms import UserCreationForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit, HTML, Button, Row, Field
from crispy_forms.bootstrap import AppendedText, PrependedText, FormActions
from django import forms
from django.utils.translation import ugettext, ugettext_lazy as _
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.forms import ValidationError


from django import forms
from django.core.validators import validate_email
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from .utils import get_user_model


class UserCreationForm(forms.ModelForm):
    """
    A form that creates a user, with no privileges, from the given username and
    password.
    """
    error_messages = {
        'duplicate_username': _("Já existe um usuário com este nome."),
        'password_mismatch': _("As senhas precisam ser iguais"),
    }
    username = forms.EmailField(label=_("Email"),
        error_messages={
            'invalid': _("Este campo só deve conter letras,números e os seguintes caracteres "
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

class CadastroPaciente(UserCreationForm):

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

class CadastroConjuge(forms.Form):
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

class CadastroPai(forms.Form):
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

class CadastroMae(forms.Form):
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

class CadastroAvoPaterno(forms.Form):
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

class CadastroAvoPaterna(forms.Form):
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

class CadastroAvoMaterno(forms.Form):
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

class CadastroAvoMaterna(forms.Form):
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

class EdicaoPaciente(forms.Form):

    def __init__(self,*args,**kwargs):
        paciente_id = kwargs.pop('paciente_id', None)
        super(EdicaoPaciente, self).__init__(*args,**kwargs)
        paciente = Paciente.objects.get(usuario_id=paciente_id)
        self.fields['nome'] = forms.CharField(label="Nome",error_messages={'required':'Este campo é obrigatório'},initial=paciente.nome)
        self.fields['nascimento'] = forms.DateField(
            label="Data de Nascimento",
            input_formats=["%d/%m/%Y",],
            widget=forms.DateInput(format='%d/%m/%Y'),
            help_text= "DD/MM/AAAA",
            error_messages={'required':'Este campo é obrigatório'},
            initial=paciente.nascimento
        )

        self.fields['sexo'] = forms.ChoiceField(
            label="Sexo",
            choices = (
                ('Feminino', "Feminino"),
                ('Masculino', "Masculino")
            ),
            widget = forms.RadioSelect,
            initial = paciente.sexo,
        )

        self.fields['escolaridade'] = forms.ChoiceField(
            label="Escolaridade",
            choices = (
                ('Fundamental', "Fundamental"),
                ('Básico', "Básico"),
                ('Técnico', 'Técnico'),
                ('Superior', 'Superior'),
                ('Pós-graduado','Pós-graduado')
            ),
            widget = forms.RadioSelect,
            initial = paciente.escolaridade,
        )


class PasswordRecoveryForm(forms.Form):
    username_or_email = forms.CharField()

    error_messages = {
        'not_found': _("Desculpe, esse usuário não existe."),
    }

    def __init__(self, *args, **kwargs):
        self.case_sensitive = kwargs.pop('case_sensitive', True)
        search_fields = kwargs.pop('search_fields', ('username', 'email'))
        super(PasswordRecoveryForm, self).__init__(*args, **kwargs)

        message = ("Apenas usuário ou email são suportados "
                   "by default")
        if len(search_fields) not in (1, 2):
            raise ValueError(message)
        for field in search_fields:
            if field not in ['username', 'email']:
                raise ValueError(message)

        labels = {
            'username': _('Usuário'),
            'email': _('Email'),
            'both': _('Usuário ou Email'),
        }
        User = get_user_model()  # noqa
        if getattr(User, 'USERNAME_FIELD', 'username') == 'email':
            self.label_key = 'email'
        elif len(search_fields) == 1:
            self.label_key = search_fields[0]
        else:
            self.label_key = 'both'
        self.fields['username_or_email'].label = labels[self.label_key]

    def clean_username_or_email(self):
        username = self.cleaned_data['username_or_email']
        cleaner = getattr(self, 'get_user_by_%s' % self.label_key)
        self.cleaned_data['user'] = user = cleaner(username)

        user_is_active = getattr(user, 'is_active', True)
        recovery_only_active_users = getattr(settings,
                                             'RECOVER_ONLY_ACTIVE_USERS',
                                             False)

        if recovery_only_active_users and not user_is_active:
            raise forms.ValidationError(_("Sorry, inactive users can't "
                                        "recover their password."))

        return username

    def get_user_by_username(self, username):
        key = 'username__%sexact' % ('' if self.case_sensitive else 'i')
        User = get_user_model()
        try:
            user = User._default_manager.get(**{key: username})
        except User.DoesNotExist:
            raise forms.ValidationError(self.error_messages['not_found'],
                                        code='not_found')
        return user

    def get_user_by_email(self, email):
        validate_email(email)
        key = 'email__%sexact' % ('' if self.case_sensitive else 'i')
        User = get_user_model()
        try:
            user = User._default_manager.get(**{key: email})
        except User.DoesNotExist:
            raise forms.ValidationError(self.error_messages['not_found'],
                                        code='not_found')
        return user

    def get_user_by_both(self, username):
        key = '__%sexact'
        key = key % '' if self.case_sensitive else key % 'i'
        f = lambda field: Q(**{field + key: username})
        filters = f('username') | f('email')
        User = get_user_model()
        try:
            user = User._default_manager.get(filters)
        except User.DoesNotExist:
            raise forms.ValidationError(self.error_messages['not_found'],
                                        code='not_found')
        except User.MultipleObjectsReturned:
            raise forms.ValidationError(_("Impossível encontrar este usuário."))

        return user


class PasswordResetForm(forms.Form):
    password1 = forms.CharField(
        label=_('Nova senha'),
        widget=forms.PasswordInput,
    )
    password2 = forms.CharField(
        label=_('Nova senha (confirmação)'),
        widget=forms.PasswordInput,
    )

    error_messages = {
        'password_mismatch': _("As duas senhas não são iguais."),
    }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(PasswordResetForm, self).__init__(*args, **kwargs)

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1', '')
        password2 = self.cleaned_data['password2']
        if not password1 == password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch')
        return password2

    def save(self, commit=True):
        self.user.set_password(self.cleaned_data['password1'])
        if commit:
            get_user_model()._default_manager.filter(pk=self.user.pk).update(
                password=self.user.password,
            )
        return self.user


class CadastroPsicologoForm(UserCreationForm):

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


    nome = forms.CharField(label="Nome",error_messages={'required':'Este campo é obrigatório'})

class IniciarAreaAfetiva(forms.Form):

    def __init__(self,*args,**kwargs):
        super(IniciarAreaAfetiva, self).__init__(*args,**kwargs)
        pergunta = PerguntaAreaAfetiva.objects.all()
        for item in pergunta:
            resposta = RespostaAreaAfetiva.objects.filter(pergunta_id=item.id)
            RESPOSTAS = []
            for resp in resposta:
                RESPOSTAS.append((resp.letra, resp.resposta))
            self.fields[item.id] = forms.ChoiceField(
                label= item.numero + ". " + item.pergunta,
                choices = RESPOSTAS,
                error_messages={'required':'Você esqueceu de marcar'},
                widget = forms.RadioSelect,
            )

class ConsultarAreaAfetiva(forms.Form):

    def __init__(self,*args,**kwargs):
        analise_id = kwargs.pop('analise_id', None)
        super(ConsultarAreaAfetiva, self).__init__(*args,**kwargs)
        pergunta = PerguntaAreaAfetiva.objects.all()
        pacienteResposta = AreaAfetiva.objects.filter(anamnesia_id=analise_id)
        for item,resposta in zip(pergunta,pacienteResposta):
            respostas = RespostaAreaAfetiva.objects.filter(pergunta_id=item.id)
            RESPOSTAS = []
            for resp in respostas:
                RESPOSTAS.append((resp.letra, resp.resposta))
            escolhida = RespostaAreaAfetiva.objects.get(id=resposta.resposta_id)
            self.fields[item.id] = forms.ChoiceField(
                label= item.numero + ". " + item.pergunta,
                choices = RESPOSTAS,
                error_messages={'required':'Você esqueceu de marcar'},
                widget = forms.RadioSelect(attrs={'disabled': 'disabled'}),
                initial= escolhida.letra,
            )

class RelacionamentoAvosMaternos(forms.Form):

    relacao = forms.ChoiceField(
        label="Seus avós maternos são:",
        choices = (
            ('Casados', "Casados"),
            ('Moram junto', "Moram junto"),
            ('Separados', 'Separados'),
            ('Divorciados', 'Divorciados')
        ),
        widget = forms.RadioSelect,
        error_messages={'required':'Este campo é obrigatório'}
    )
    filhos = forms.IntegerField(label="Seus avós maternos tiveram quantos filhos homens?",error_messages={'required':'Este campo é obrigatório'})
    filhas = forms.IntegerField(label="Seus avós maternos tiveram quantas filhas mulheres?",error_messages={'required':'Este campo é obrigatório'})
    relacaoAvoMaternoAntes = forms.ChoiceField(
        label="Seu avô materno era separado/divorciado quando se relacionava com sua avó?",
        choices = (
            ('Sim', "Sim"),
            ('Não', "Não")
        ),
        widget = forms.RadioSelect,
        error_messages={'required':'Este campo é obrigatório'}
    )
    relacaoAvoMaternaAntes = forms.ChoiceField(
        label="Sua avó materna era separada/divorciada quando se relacionava com seu avô?",
        choices = (
            ('Sim', "Sim"),
            ('Não', "Não")
        ),
        widget = forms.RadioSelect,
        error_messages={'required':'Este campo é obrigatório'}
    )

class RelacionamentoAvoMaternoAntes(forms.Form):

    filhos = forms.IntegerField(label="Seu avô materno teve quantos filhos homens no relacionamento anterior à relação com sua avó?",
                                error_messages={'required':'Este campo é obrigatório'})
    filhas = forms.IntegerField(label="Seu avô materno teve quantas filhas mulheres no relacionamento anterior à relação com sua avó?",
                                error_messages={'required':'Este campo é obrigatório'})


class RelacionamentoAvoMaternaAntes(forms.Form):

    filhos = forms.IntegerField(label="Sua avó materna teve quantos filhos homens no relacionamento anterior à relação com seu avô?",
                                error_messages={'required':'Este campo é obrigatório'})
    filhas = forms.IntegerField(label="Sua avó materna teve quantas filhas mulheres no relacionamento anterior à relação com seu avô?",
                                error_messages={'required':'Este campo é obrigatório'})

class RelacionamentoAvosMaternosDepois(forms.Form):

    filhosAvoMaterno = forms.IntegerField(label="Seu avô materno teve quantos filhos homens no relacionamento posterior à relação com sua avó?",
                                error_messages={'required':'Este campo é obrigatório'})
    filhasAvoMaterno = forms.IntegerField(label="Seu avô materno teve quantas filhas mulheres no relacionamento posterior à relação com sua avó?",
                                error_messages={'required':'Este campo é obrigatório'})

    filhosAvoMaterna = forms.IntegerField(label="Sua avó materna teve quantos filhos homens no relacionamento posterior à relação com seu avô?",
                                error_messages={'required':'Este campo é obrigatório'})
    filhasAvoMaterna = forms.IntegerField(label="Sua avó materna teve quantas filhas mulheres no relacionamento posterior à relação com seu avô?",
                                error_messages={'required':'Este campo é obrigatório'})

class RelacionamentoAvosPaternos(forms.Form):

    relacao = forms.ChoiceField(
        label="Seus avós paternos são:",
        choices = (
            ('Casados', "Casados"),
            ('Moram junto', "Moram junto"),
            ('Separados', 'Separados'),
            ('Divorciados', 'Divorciados')
        ),
        widget = forms.RadioSelect,
        error_messages={'required':'Este campo é obrigatório'}
    )
    filhos = forms.IntegerField(label="Seus avós paternos tiveram quantos filhos homens?",error_messages={'required':'Este campo é obrigatório'})
    filhas = forms.IntegerField(label="Seus avós paternos tiveram quantas filhas mulheres?",error_messages={'required':'Este campo é obrigatório'})
    relacaoAvoPaternoAntes = forms.ChoiceField(
        label="Seu avô paterno era separado/divorciado quando se relacionava com sua avó?",
        choices = (
            ('Sim', "Sim"),
            ('Não', "Não")
        ),
        widget = forms.RadioSelect,
        error_messages={'required':'Este campo é obrigatório'}
    )
    relacaoAvoPaternaAntes = forms.ChoiceField(
        label="Sua avó paterna era separada/divorciada quando se relacionava com seu avô?",
        choices = (
            ('Sim', "Sim"),
            ('Não', "Não")
        ),
        widget = forms.RadioSelect,
        error_messages={'required':'Este campo é obrigatório'}
    )

class RelacionamentoAvoPaternoAntes(forms.Form):

    filhos = forms.IntegerField(label="Seu avô paterno teve quantos filhos homens no relacionamento anterior à relação com sua avó?",
                                error_messages={'required':'Este campo é obrigatório'})
    filhas = forms.IntegerField(label="Seu avô paterno teve quantas filhas mulheres no relacionamento anterior à relação com sua avó?",
                                error_messages={'required':'Este campo é obrigatório'})


class RelacionamentoAvoPaternaAntes(forms.Form):

    filhos = forms.IntegerField(label="Sua avó paterna teve quantos filhos homens no relacionamento anterior à relação com seu avô?",
                                error_messages={'required':'Este campo é obrigatório'})
    filhas = forms.IntegerField(label="Sua avó paterna teve quantas filhas mulheres no relacionamento anterior à relação com seu avô?",
                                error_messages={'required':'Este campo é obrigatório'})

class RelacionamentoAvosPaternosDepois(forms.Form):

    filhosAvoPaterno = forms.IntegerField(label="Seu avô paterno teve quantos filhos homens no relacionamento posterior à relação com sua avó?",
                                error_messages={'required':'Este campo é obrigatório'})
    filhasAvoPaterno = forms.IntegerField(label="Seu avô paterno teve quantas filhas mulheres no relacionamento posterior à relação com sua avó?",
                                error_messages={'required':'Este campo é obrigatório'})

    filhosAvoPaterna = forms.IntegerField(label="Sua avó paterna teve quantos filhos homens no relacionamento posterior à relação com seu avô?",
                                error_messages={'required':'Este campo é obrigatório'})
    filhasAvoPaterna = forms.IntegerField(label="Sua avó paterna teve quantas filhas mulheres no relacionamento posterior à relação com seu avô?",
                                error_messages={'required':'Este campo é obrigatório'})

class RelacionamentoPais(forms.Form):

    relacao = forms.ChoiceField(
        label="Seus pais são:",
        choices = (
            ('Casados', "Casados"),
            ('Moram junto', "Moram junto"),
            ('Separados', 'Separados'),
            ('Divorciados', 'Divorciados')
        ),
        widget = forms.RadioSelect,
        error_messages={'required':'Este campo é obrigatório'}
    )
    filhos = forms.IntegerField(label="Seus pais tiveram quantos filhos homens?",error_messages={'required':'Este campo é obrigatório'})
    filhas = forms.IntegerField(label="Seus pais tiveram quantas filhas mulheres?",error_messages={'required':'Este campo é obrigatório'})
    relacaoPaiAntes = forms.ChoiceField(
        label="Seu pai era separado/divorciado quando se relacionava com sua mãe?",
        choices = (
            ('Sim', "Sim"),
            ('Não', "Não")
        ),
        widget = forms.RadioSelect,
        error_messages={'required':'Este campo é obrigatório'}
    )
    relacaoMaeAntes = forms.ChoiceField(
        label="Sua mãe era separada/divorciada quando se relacionava com seu pai?",
        choices = (
            ('Sim', "Sim"),
            ('Não', "Não")
        ),
        widget = forms.RadioSelect,
        error_messages={'required':'Este campo é obrigatório'}
    )

class RelacionamentoPaiAntes(forms.Form):

    filhos = forms.IntegerField(label="Seu pai teve quantos filhos homens no relacionamento anterior à relação com sua mãe?",
                                error_messages={'required':'Este campo é obrigatório'})
    filhas = forms.IntegerField(label="Seu pai teve quantas filhas mulheres no relacionamento anterior à relação com sua mãe?",
                                error_messages={'required':'Este campo é obrigatório'})


class RelacionamentoMaeAntes(forms.Form):

    filhos = forms.IntegerField(label="Sua mãe teve quantos filhos homens no relacionamento anterior à relação com seu pai?",
                                error_messages={'required':'Este campo é obrigatório'})
    filhas = forms.IntegerField(label="Sua mãe teve quantas filhas mulheres no relacionamento anterior à relação com seu pai?",
                                error_messages={'required':'Este campo é obrigatório'})

class RelacionamentoPaisDepois(forms.Form):

    filhosPai = forms.IntegerField(label="Seu pai teve quantos filhos homens no relacionamento posterior à relação com sua mãe?",
                                error_messages={'required':'Este campo é obrigatório'})
    filhasPai = forms.IntegerField(label="Seu pai teve quantas filhas mulheres no relacionamento posterior à relação com sua mãe?",
                                error_messages={'required':'Este campo é obrigatório'})

    filhosMae = forms.IntegerField(label="Sua mãe teve quantos filhos homens no relacionamento posterior à relação com seu pai?",
                                error_messages={'required':'Este campo é obrigatório'})
    filhasMae = forms.IntegerField(label="Sua mãe teve quantas filhas mulheres no relacionamento posterior à relação com seu pai?",
                                error_messages={'required':'Este campo é obrigatório'})

class RelacionamentoPaciente(forms.Form):

    relacao = forms.ChoiceField(
        label="Vocẽ é:",
        choices = (
            ('Casado(a)', "Casado(a)"),
            ('Mora junto', "Mora junto"),
            ('Separado(a)', 'Separado(a)'),
            ('Divorciado(a)', 'Divorciado(a)'),
            ('Não se aplica', 'Não se aplica')
        ),
        widget = forms.RadioSelect,
        error_messages={'required':'Este campo é obrigatório'}
    )
    filhos = forms.IntegerField(label="Vocẽ tem quantos filhos homens?",error_messages={'required':'Este campo é obrigatório'})
    filhas = forms.IntegerField(label="Você tem quantas filhas mulheres?",error_messages={'required':'Este campo é obrigatório'})
    relacaoPacienteAntes = forms.ChoiceField(
        label="Você era separado/divorciado antes de conhecer seu cônjuge?",
        choices = (
            ('Sim', "Sim"),
            ('Não', "Não")
        ),
        widget = forms.RadioSelect,
        error_messages={'required':'Este campo é obrigatório'}
    )
    relacaoConjugeAntes = forms.ChoiceField(
        label="Sua cônjuge era separado/divorciado antes de conhecer você?",
        choices = (
            ('Sim', "Sim"),
            ('Não', "Não")
        ),
        widget = forms.RadioSelect,
        error_messages={'required':'Este campo é obrigatório'}
    )

class RelacionamentoPacienteAntes(forms.Form):

    filhos = forms.IntegerField(label="Você teve quantos filhos homens no relacionamento anterior à relação com seu cônjuge?",
                                error_messages={'required':'Este campo é obrigatório'})
    filhas = forms.IntegerField(label="Você teve quantas filhas mulheres no relacionamento anterior à relação com seu cônjuge?",
                                error_messages={'required':'Este campo é obrigatório'})


class RelacionamentoConjugeAntes(forms.Form):

    filhos = forms.IntegerField(label="Seu cônjuge teve quantos filhos homens no relacionamento anterior à relação com você?",
                                error_messages={'required':'Este campo é obrigatório'})
    filhas = forms.IntegerField(label="Seu cônjuge teve quantos filhas mulheres no relacionamento anterior à relação com você?",
                                error_messages={'required':'Este campo é obrigatório'})

class RelacionamentoPacienteDepois(forms.Form):

    filhosPaciente = forms.IntegerField(label="Você teve quantos filhos homens no relacionamento posterior à relação com seu cônjuge?",
                                error_messages={'required':'Este campo é obrigatório'})
    filhasPaciente = forms.IntegerField(label="Você teve quantas filhas mulheres no relacionamento posterior à relação com seu cônjuge?",
                                error_messages={'required':'Este campo é obrigatório'})

    filhosConjuge = forms.IntegerField(label="Seu cônjuge teve quantos filhos homens no relacionamento posterior à relação com você?",
                                error_messages={'required':'Este campo é obrigatório'})
    filhasConjuge = forms.IntegerField(label="Seu cônjuge teve quantos filhas mulheres no relacionamento posterior à relação com você?",
                                error_messages={'required':'Este campo é obrigatório'})