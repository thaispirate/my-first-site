import random
from django import forms
from .models import User, Chave, Paciente, Psicologo, Familia, PerguntaAreaAfetiva, RespostaAreaAfetiva, AreaAfetiva,\
    Anamnesia, GrauIndiferenciacao, PerguntaSeletiva, RespostaSeletiva,Seletiva,\
    PerguntaInterventiva, Interventiva
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
        'duplicate_username': _("Já existe um usuário com este email."),
        'password_mismatch': _("As senhas precisam ser iguais"),
        'chave_acesso': _("Chave de acesso inválida"),
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
    code = forms.CharField(label=_("Chave de acesso"),
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

    def clean_code(self):
        code = self.cleaned_data.get("code")
        if not Chave.objects.filter(chave = code).exists():
            raise forms.ValidationError(
                self.error_messages['chave_acesso'],
                code='chave_acesso',
            )
        else:
            chave=Chave.objects.get(chave=code)
            if chave.padrao == "usada":
                raise forms.ValidationError(
                self.error_messages['chave_acesso'],
                code='chave_acesso',
            )
        return code

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
        label="Data de Nascimento(ou data aproximada)",
        input_formats=["%d/%m/%Y",],
        widget=forms.DateInput(format='%d/%m/%Y'),
        help_text= "DD/MM/AAAA",
    )

    sexo = forms.ChoiceField(
        label="Sexo",
        choices = (
            ('Feminino', "Feminino"),
            ('Masculino', "Masculino")
        ),
        widget = forms.RadioSelect,

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
        required=False

    )

    psicologo = forms.ModelChoiceField(
        label="Psicólogo",
        queryset = Psicologo.objects.all(),
        required=False

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
        required=False
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
        required=False
    )

class CadastroPai(forms.Form):
    nomePai = forms.CharField(label="Primeiro nome do Pai",required=False)
    nascimentoPai = forms.DateField(
        label="Data de Nascimento do Pai",
        input_formats=["%d/%m/%Y",],
        widget=forms.DateInput(format='%d/%m/%Y'),
        help_text= "DD/MM/AAAA",
        required=False
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
        required=False
    )

class CadastroMae(forms.Form):
    nomeMae = forms.CharField(label="Primeiro nome da Mãe",required=False)
    nascimentoMae = forms.DateField(
        label="Data de Nascimento da Mãe",
        input_formats=["%d/%m/%Y",],
        widget=forms.DateInput(format='%d/%m/%Y'),
        help_text= "DD/MM/AAAA",
        required=False
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
        required=False
    )

class CadastroAvoPaterno(forms.Form):
    nomeAvoPaterno = forms.CharField(label="Primeiro nome do Avô Paterno",required=False)
    nascimentoAvoPaterno = forms.DateField(
        label="Data de Nascimento do Avô Paterno",
        input_formats=["%d/%m/%Y",],
        widget=forms.DateInput(format='%d/%m/%Y'),
        help_text= "DD/MM/AAAA",
        required=False
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
        required=False
    )

class CadastroAvoPaterna(forms.Form):
    nomeAvoPaterna = forms.CharField(label="Primeiro nome da Avó Paterna",required=False)
    nascimentoAvoPaterna = forms.DateField(
        label="Data de Nascimento da Avó Paterna",
        input_formats=["%d/%m/%Y",],
        widget=forms.DateInput(format='%d/%m/%Y'),
        help_text= "DD/MM/AAAA",
        required=False
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
        required=False
    )

class CadastroAvoMaterno(forms.Form):
    nomeAvoMaterno = forms.CharField(label="Primeiro nome do Avô Materno",required=False)
    nascimentoAvoMaterno = forms.DateField(
        label="Data de Nascimento do Avô Materno",
        input_formats=["%d/%m/%Y",],
        widget=forms.DateInput(format='%d/%m/%Y'),
        help_text= "DD/MM/AAAA",
        required=False
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
        required=False
    )

class CadastroAvoMaterna(forms.Form):
    nomeAvoMaterna = forms.CharField(label="Primeiro nome da Avó Materna",required=False)
    nascimentoAvoMaterna = forms.DateField(
        label="Data de Nascimento da Avó Materna",
        input_formats=["%d/%m/%Y",],
        widget=forms.DateInput(format='%d/%m/%Y'),
        help_text= "DD/MM/AAAA",
        required=False
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
        required=False
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
            initial=paciente.nascimento,
            required=False
        )

        self.fields['sexo'] = forms.ChoiceField(
            label="Sexo",
            choices = (
                ('Feminino', "Feminino"),
                ('Masculino', "Masculino")
            ),
            widget = forms.RadioSelect,
            initial = paciente.sexo,
            required=False
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
            required=False
        )
        self.fields['psicologo'] = forms.ModelChoiceField(
            label= "Psicólogo",
            queryset= Psicologo.objects.all(),
            initial = paciente.psicologo,
            required=False
        )


class PasswordRecoveryForm(forms.Form):
    username_or_email = forms.CharField(error_messages={'required':'Este campo é obrigatório'})

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

class AtualizarChave(forms.Form):

    error_messages = {
        'chave_acesso': _("Chave de acesso inválida"),
    }

    chave = forms.CharField(label="Digite sua nova chave:",
                            error_messages={'required':'Este campo é obrigatório'})

    def clean_chave(self):
        code = self.cleaned_data.get("chave")
        if not Chave.objects.filter(chave = code).exists():
            raise forms.ValidationError(
                self.error_messages['chave_acesso'],
                code='chave_acesso',
            )
        else:
            chave=Chave.objects.get(chave=code)
            if chave.padrao == "usada":
                raise forms.ValidationError(
                self.error_messages['chave_acesso'],
                code='chave_acesso',
            )
        return chave

class PerguntasAreaAfetiva(forms.Form):

    def __init__(self,*args,**kwargs):
        super(PerguntasAreaAfetiva, self).__init__(*args,**kwargs)
        pergunta = PerguntaAreaAfetiva.objects.all()
        for item in pergunta:
            resposta = RespostaAreaAfetiva.objects.filter(pergunta_id=item.id)
            RESPOSTAS = []
            for resp in resposta:
                RESPOSTAS.append((resp.letra, resp.resposta))
            self.fields[item.numero] = forms.ChoiceField(
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
        pacienteResposta = AreaAfetiva.objects.filter(anamnesia_id=analise_id).order_by('resposta')
        for item,resposta in zip(pergunta,pacienteResposta):
            respostas = RespostaAreaAfetiva.objects.filter(pergunta_id=item.id)
            RESPOSTAS = []
            for resp in respostas:
                RESPOSTAS.append((resp.letra, resp.resposta))
            escolhida = RespostaAreaAfetiva.objects.get(id=resposta.resposta_id)
            self.fields[item.numero] = forms.ChoiceField(
                label= item.numero + ". " + item.pergunta,
                choices = RESPOSTAS,
                error_messages={'required':'Você esqueceu de marcar'},
                widget = forms.RadioSelect,
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
    filhos = forms.IntegerField(min_value=0,label="Seus avós maternos tiveram quantos filhos homens?",error_messages={'required':'Este campo é obrigatório'})
    filhas = forms.IntegerField(min_value=1,label="Seus avós maternos tiveram quantas filhas mulheres?",error_messages={'required':'Este campo é obrigatório'})
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

    filhosAvoMaternoAntes = forms.IntegerField(min_value=0,label="Seu avô materno teve quantos filhos homens no relacionamento anterior à relação com sua avó?",
                                error_messages={'required':'Este campo é obrigatório'})
    filhasAvoMaternoAntes = forms.IntegerField(min_value=0,label="Seu avô materno teve quantas filhas mulheres no relacionamento anterior à relação com sua avó?",
                                error_messages={'required':'Este campo é obrigatório'})


class RelacionamentoAvoMaternaAntes(forms.Form):

    filhosAvoMaternaAntes = forms.IntegerField(min_value=0,label="Sua avó materna teve quantos filhos homens no relacionamento anterior à relação com seu avô?",
                                error_messages={'required':'Este campo é obrigatório'})
    filhasAvoMaternaAntes = forms.IntegerField(min_value=0,label="Sua avó materna teve quantas filhas mulheres no relacionamento anterior à relação com seu avô?",
                                error_messages={'required':'Este campo é obrigatório'})

class RelacionamentoAvosMaternosDepois(forms.Form):

    filhosAvoMaterno = forms.IntegerField(min_value=0,label="Seu avô materno teve quantos filhos homens no relacionamento posterior à relação com sua avó?",
                                error_messages={'required':'Este campo é obrigatório'})
    filhasAvoMaterno = forms.IntegerField(min_value=0,label="Seu avô materno teve quantas filhas mulheres no relacionamento posterior à relação com sua avó?",
                                error_messages={'required':'Este campo é obrigatório'})

    filhosAvoMaterna = forms.IntegerField(min_value=0,label="Sua avó materna teve quantos filhos homens no relacionamento posterior à relação com seu avô?",
                                error_messages={'required':'Este campo é obrigatório'})
    filhasAvoMaterna = forms.IntegerField(min_value=0,label="Sua avó materna teve quantas filhas mulheres no relacionamento posterior à relação com seu avô?",
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
    filhos = forms.IntegerField(min_value=1,label="Seus avós paternos tiveram quantos filhos homens?",error_messages={'required':'Este campo é obrigatório'})
    filhas = forms.IntegerField(min_value=0,label="Seus avós paternos tiveram quantas filhas mulheres?",error_messages={'required':'Este campo é obrigatório'})
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

    filhosAvoPaternoAntes = forms.IntegerField(min_value=0,label="Seu avô paterno teve quantos filhos homens no relacionamento anterior à relação com sua avó?",
                                error_messages={'required':'Este campo é obrigatório'})
    filhasAvoPaternoAntes = forms.IntegerField(min_value=0,label="Seu avô paterno teve quantas filhas mulheres no relacionamento anterior à relação com sua avó?",
                                error_messages={'required':'Este campo é obrigatório'})


class RelacionamentoAvoPaternaAntes(forms.Form):

    filhosAvoPaternaAntes = forms.IntegerField(min_value=0,label="Sua avó paterna teve quantos filhos homens no relacionamento anterior à relação com seu avô?",
                                error_messages={'required':'Este campo é obrigatório'})
    filhasAvoPaternaAntes = forms.IntegerField(min_value=0,label="Sua avó paterna teve quantas filhas mulheres no relacionamento anterior à relação com seu avô?",
                                error_messages={'required':'Este campo é obrigatório'})

class RelacionamentoAvosPaternosDepois(forms.Form):

    filhosAvoPaterno = forms.IntegerField(min_value=0,label="Seu avô paterno teve quantos filhos homens no relacionamento posterior à relação com sua avó?",
                                error_messages={'required':'Este campo é obrigatório'})
    filhasAvoPaterno = forms.IntegerField(min_value=0,label="Seu avô paterno teve quantas filhas mulheres no relacionamento posterior à relação com sua avó?",
                                error_messages={'required':'Este campo é obrigatório'})

    filhosAvoPaterna = forms.IntegerField(min_value=0,label="Sua avó paterna teve quantos filhos homens no relacionamento posterior à relação com seu avô?",
                                error_messages={'required':'Este campo é obrigatório'})
    filhasAvoPaterna = forms.IntegerField(min_value=0,label="Sua avó paterna teve quantas filhas mulheres no relacionamento posterior à relação com seu avô?",
                                error_messages={'required':'Este campo é obrigatório'})

class RelacionamentoPais(forms.Form):

    def __init__(self,*args,**kwargs):
        paciente_sexo = kwargs.pop('paciente_sexo',None)
        step = kwargs.pop('step',None)
        super(RelacionamentoPais, self).__init__(*args,**kwargs)
        filhas=0
        filhos=0
        step=str(step)
        step=step+"-"
        if step == "None-":
            step=""
        if paciente_sexo == "Feminino":
            filhas=1
        if paciente_sexo == "Masculino":
            filhos=1
        print(step)
        self.fields[step+"relacao"] = forms.ChoiceField(
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
        self.fields[step+"filhos"] = forms.IntegerField(min_value=filhos,label="Seus pais tiveram quantos filhos homens?",error_messages={'required':'Este campo é obrigatório'})
        self.fields[step+"filhas"] = forms.IntegerField(min_value=filhas,label="Seus pais tiveram quantas filhas mulheres?",error_messages={'required':'Este campo é obrigatório'})
        self.fields[step+"relacaoPaiAntes"] = forms.ChoiceField(
            label="Seu pai era separado/divorciado quando se relacionava com sua mãe?",
            choices = (
                ('Sim', "Sim"),
                ('Não', "Não")
            ),
            widget = forms.RadioSelect,
            error_messages={'required':'Este campo é obrigatório'}
        )
        self.fields[step+"relacaoMaeAntes"] = forms.ChoiceField(
            label="Sua mãe era separada/divorciada quando se relacionava com seu pai?",
            choices = (
                ('Sim', "Sim"),
                ('Não', "Não")
            ),
            widget = forms.RadioSelect,
            error_messages={'required':'Este campo é obrigatório'}
        )

class RelacionamentoPaiAntes(forms.Form):

    filhosPaiAntes = forms.IntegerField(min_value=0,label="Seu pai teve quantos filhos homens no relacionamento anterior à relação com sua mãe?",
                                error_messages={'required':'Este campo é obrigatório'})
    filhasPaiAntes = forms.IntegerField(min_value=0,label="Seu pai teve quantas filhas mulheres no relacionamento anterior à relação com sua mãe?",
                                error_messages={'required':'Este campo é obrigatório'})


class RelacionamentoMaeAntes(forms.Form):

    filhosMaeAntes = forms.IntegerField(min_value=0,label="Sua mãe teve quantos filhos homens no relacionamento anterior à relação com seu pai?",
                                error_messages={'required':'Este campo é obrigatório'})
    filhasMaeAntes = forms.IntegerField(min_value=0,label="Sua mãe teve quantas filhas mulheres no relacionamento anterior à relação com seu pai?",
                                error_messages={'required':'Este campo é obrigatório'})

class RelacionamentoPaisDepois(forms.Form):

    filhosPai = forms.IntegerField(min_value=0,label="Seu pai teve quantos filhos homens no relacionamento posterior à relação com sua mãe?",
                                error_messages={'required':'Este campo é obrigatório'})
    filhasPai = forms.IntegerField(min_value=0,label="Seu pai teve quantas filhas mulheres no relacionamento posterior à relação com sua mãe?",
                                error_messages={'required':'Este campo é obrigatório'})

    filhosMae = forms.IntegerField(min_value=0,label="Sua mãe teve quantos filhos homens no relacionamento posterior à relação com seu pai?",
                                error_messages={'required':'Este campo é obrigatório'})
    filhasMae = forms.IntegerField(min_value=0,label="Sua mãe teve quantas filhas mulheres no relacionamento posterior à relação com seu pai?",
                                error_messages={'required':'Este campo é obrigatório'})

class RelacionamentoPaciente(forms.Form):

    relacao = forms.ChoiceField(
        label="Vocẽ é:",
        choices = (
            ('Casado(a)', "Casado(a)"),
            ('Mora junto', "Mora junto"),
            ('Separado(a)', 'Separado(a)'),
            ('Divorciado(a)', 'Divorciado(a)'),
            ('Solteiro(a)', 'Solteiro(a)')
        ),
        widget = forms.RadioSelect,
        error_messages={'required':'Este campo é obrigatório'}
    )
    filhos = forms.IntegerField(min_value=0,label="Vocẽ tem quantos filhos homens?",error_messages={'required':'Este campo é obrigatório'})
    filhas = forms.IntegerField(min_value=0,label="Você tem quantas filhas mulheres?",error_messages={'required':'Este campo é obrigatório'})
    relacaoPacienteAntes = forms.ChoiceField(
        label="Você já foi separado/divorciado?",
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
            ('Não', "Não"),
            ("Não se aplica", "Não se aplica")
        ),
        widget = forms.RadioSelect,
        error_messages={'required':'Este campo é obrigatório'}
    )

class RelacionamentoPacienteAntes(forms.Form):

    filhosPacienteAntes = forms.IntegerField(min_value=0,label="Você teve quantos filhos homens no relacionamento anterior à relação com seu cônjuge?",
                                error_messages={'required':'Este campo é obrigatório'})
    filhasPacienteAntes = forms.IntegerField(min_value=0,label="Você teve quantas filhas mulheres no relacionamento anterior à relação com seu cônjuge?",
                                error_messages={'required':'Este campo é obrigatório'})


class RelacionamentoConjugeAntes(forms.Form):

    filhosConjugeAntes = forms.IntegerField(min_value=0,label="Seu cônjuge teve quantos filhos homens no relacionamento anterior à relação com você?",
                                error_messages={'required':'Este campo é obrigatório'})
    filhasConjugeAntes = forms.IntegerField(min_value=0,label="Seu cônjuge teve quantos filhas mulheres no relacionamento anterior à relação com você?",
                                error_messages={'required':'Este campo é obrigatório'})

class RelacionamentoPacienteDepois(forms.Form):

    filhosPaciente = forms.IntegerField(min_value=0,label="Você teve quantos filhos homens no relacionamento posterior à relação com seu cônjuge?",
                                error_messages={'required':'Este campo é obrigatório'})
    filhasPaciente = forms.IntegerField(min_value=0,label="Você teve quantas filhas mulheres no relacionamento posterior à relação com seu cônjuge?",
                                error_messages={'required':'Este campo é obrigatório'})

    filhosConjuge = forms.IntegerField(min_value=0,label="Seu cônjuge teve quantos filhos homens no relacionamento posterior à relação com você?",
                                error_messages={'required':'Este campo é obrigatório'})
    filhasConjuge = forms.IntegerField(min_value=0,label="Seu cônjuge teve quantos filhas mulheres no relacionamento posterior à relação com você?",
                                error_messages={'required':'Este campo é obrigatório'})

class GrauDeIndeferenciacao(forms.Form):

    def __init__(self,*args,**kwargs):
        super(GrauDeIndeferenciacao, self).__init__(*args,**kwargs)
        resposta = GrauIndiferenciacao.objects.all()
        RESPOSTAS = []
        for item in resposta:
            RESPOSTAS.append((item.id,item.resposta))
        random.shuffle(RESPOSTAS)
        self.fields['grauIndiferenciacao'] = forms.MultipleChoiceField(
            label= "Assinale as características que coincidem com o seu comportamento.",
            choices = RESPOSTAS,
            error_messages={'required':'Você esqueceu de marcar'},
            widget = forms.CheckboxSelectMultiple
        )

class PerguntasSeletivas(forms.Form):

    def __init__(self,*args,**kwargs):
        relacao = kwargs.pop('relacao',None)
        super(PerguntasSeletivas, self).__init__(*args,**kwargs)
        if relacao == "Solteiro(a)" or relacao == "Separado(a)" or relacao == "Divorciado(a)":
            pergunta = PerguntaSeletiva.objects.filter(tipo=None)
        else:
            pergunta = PerguntaSeletiva.objects.filter()
        for item in pergunta:
            if item.numero != "S03" and item.numero != "S04":
                resposta = RespostaSeletiva.objects.filter(pergunta_id=item.id)
                RESPOSTAS = []
                for resp in resposta:
                    RESPOSTAS.append((resp.letra, resp.resposta))
                self.fields[item.numero] = forms.ChoiceField(
                    label= item.numero + ". " + item.pergunta,
                    choices = RESPOSTAS,
                    error_messages={'required':'Você esqueceu de marcar'},
                    widget = forms.RadioSelect,
                )
            else:
                resposta = RespostaSeletiva.objects.filter(pergunta_id=item.id)
                RESPOSTAS = []
                for resp in resposta:
                    RESPOSTAS.append((resp.letra, resp.resposta))
                self.fields[item.numero] = forms.MultipleChoiceField(
                    label= item.numero + ". " + item.pergunta,
                    choices = RESPOSTAS,
                    error_messages={'required':'Você esqueceu de marcar'},
                    widget = forms.CheckboxSelectMultiple,
                )

class ConsultarPerguntasSeletivas(forms.Form):

    def __init__(self,*args,**kwargs):
        analise_id = kwargs.pop('analise_id',None)
        super(ConsultarPerguntasSeletivas, self).__init__(*args,**kwargs)
        pergunta = PerguntaSeletiva.objects.all()
        respostaPaciente = Seletiva.objects.filter(anamnesia_id=analise_id).order_by('resposta')
        for item in pergunta:
            escolhidas =[]
            for selecionadas in respostaPaciente:
                if item.numero == selecionadas.resposta.pergunta.numero and (item.numero == "S03" or item.numero == "S04"):
                    resposta = RespostaSeletiva.objects.filter(pergunta_id=item.id)
                    RESPOSTAS = []
                    for resp in resposta:
                        RESPOSTAS.append((resp.letra, resp.resposta))
                    selecionada = RespostaSeletiva.objects.get(id=selecionadas.resposta_id)
                    escolhidas.append(selecionada.letra)
                    self.fields[item.numero] = forms.MultipleChoiceField(
                        label= item.numero + ". " + item.pergunta,
                        choices = RESPOSTAS,
                        widget = forms.CheckboxSelectMultiple,
                        initial= escolhidas
                    )
                if item.numero == selecionadas.resposta.pergunta.numero and (item.numero != "S03" and item.numero != "S04"):
                    resposta = RespostaSeletiva.objects.filter(pergunta_id=item.id)
                    RESPOSTAS = []
                    for resp in resposta:
                        RESPOSTAS.append((resp.letra, resp.resposta))
                    selecionada = RespostaSeletiva.objects.get(id=selecionadas.resposta_id)
                    self.fields[item.numero] = forms.ChoiceField(
                        label= item.numero + ". " + item.pergunta,
                        choices = RESPOSTAS,
                        widget = forms.RadioSelect,
                        initial = selecionada.letra
                    )

class PerguntasInterventivas(forms.Form):

    def __init__(self,*args,**kwargs):
        super(PerguntasInterventivas, self).__init__(*args,**kwargs)
        pergunta = PerguntaInterventiva.objects.all()
        for item in pergunta:
            self.fields[item.numero] = forms.CharField(
                label= item.numero + ". " + item.pergunta,
                error_messages={'required':'Você esqueceu de responder'},
                widget=forms.Textarea(attrs={'rows': 2, 'cols': 40})
            )

class ConsultarPerguntasInterventivas(forms.Form):

    def __init__(self,*args,**kwargs):
        analise_id = kwargs.pop('analise_id', None)
        super(ConsultarPerguntasInterventivas, self).__init__(*args,**kwargs)
        pergunta = PerguntaInterventiva.objects.all()
        pacienteResposta = Interventiva.objects.filter(anamnesia_id=analise_id).order_by('pergunta')
        for item,resposta in zip(pergunta,pacienteResposta):
            self.fields[item.id] = forms.ChoiceField(
                label= item.numero + ". " + item.pergunta,
                widget=forms.Textarea(attrs={'rows': 2, 'cols': 40}),
                initial= resposta.resposta
            )









