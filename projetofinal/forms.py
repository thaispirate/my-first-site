from django import forms
from django.contrib.auth.forms import UserCreationForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit, HTML, Button, Row, Field
from crispy_forms.bootstrap import AppendedText, PrependedText, FormActions

class UserForm(UserCreationForm):
    email = forms.EmailField()
    nome = forms.CharField()
    nascimento = forms.DateField()
    sexo = forms.CharField()

class MessageForm(UserCreationForm):
    email = forms.EmailField()
    nome = forms.CharField()
    nascimento = forms.DateField(
        input_formats=["%d/%m/%Y",],
        widget=forms.DateInput(format='%d/%m/%Y'),
        help_text= "DD/MM/AAAA"
    )

    sexo = forms.ChoiceField(
        choices = (
            ('Feminino', "Feminino"),
            ('Masculino', "Masculino")
        ),
        widget = forms.RadioSelect,
        initial = 'Feminino',
    )

    escolaridade = forms.ChoiceField(
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