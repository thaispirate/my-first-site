from datetime import datetime
from django.db import models
from django import forms
from django.utils import timezone
from datetime import date
from django.contrib.auth.models import User

# Create your models here.

class Paciente(models.Model):
    usuario = models.OneToOneField(User)
    email = models.EmailField()
    nome = models.CharField(max_length=50,null=True)
    nascimento = models.DateField(null=True)
    sexo = models.CharField(max_length=10,null=True)
    escolaridade = models.CharField(max_length=15, null=True)
    nomeConjuge = models.CharField(max_length=50,null=True,blank=True)
    nascimentoConjuge = models.DateField(null=True,blank=True)
    sexoConjuge = models.CharField(max_length=10,null=True,blank=True)
    escolaridadeConjuge = models.CharField(max_length=15, null=True,blank=True)
    nomePai = models.CharField(max_length=50,null=True)
    nascimentoPai = models.DateField(null=True)
    falecimentoPai = models.DateField(null=True,blank=True)
    escolaridadePai = models.CharField(max_length=15, null=True)
    nomeMae = models.CharField(max_length=50,null=True)
    nascimentoMae = models.DateField(null=True)
    falecimentoMae = models.DateField(null=True, blank=True)
    escolaridadeMae = models.CharField(max_length=15, null=True)
    nomeAvoPaterna = models.CharField(max_length=50,null=True)
    nascimentoAvoPaterna = models.DateField(null=True)
    falecimentoAvoPaterna = models.DateField(null=True,blank=True)
    escolaridadeAvoPaterna = models.CharField(max_length=15, null=True)
    nomeAvoPaterno = models.CharField(max_length=50,null=True)
    nascimentoAvoPaterno = models.DateField(null=True)
    falecimentoAvoPaterno = models.DateField(null=True,blank=True)
    escolaridadeAvoPaterno = models.CharField(max_length=15, null=True)
    nomeAvoMaterna = models.CharField(max_length=50,null=True)
    nascimentoAvoMaterna = models.DateField(null=True)
    falecimentoAvoMaterna = models.DateField(null=True,blank=True)
    escolaridadeAvoMaterna = models.CharField(max_length=15, null=True)
    nomeAvoMaterno = models.CharField(max_length=50,null=True)
    nascimentoAvoMaterno = models.DateField(null=True)
    falecimentoAvoMaterno = models.DateField(null=True,blank=True)
    escolaridadeAvoMaterno = models.CharField(max_length=15, null=True)

    def __str__(self):
        return self.usuario.first_name


class Psicologo(models.Model):
    usuario = models.OneToOneField(User)
    email = models.EmailField()
    nome = models.CharField(max_length=50,null=True)

    def __str__(self):
        return self.usuario.first_name

class PerguntaAreaAfetiva(models.Model):
    numero = models.CharField(max_length=10,null=True)
    pergunta = models.TextField(null=True)

    def __str__(self):
        return self.numero

class RespostaAreaAfetiva(models.Model):
    pergunta =  models.ForeignKey(PerguntaAreaAfetiva, on_delete=models.CASCADE,null=True)
    letra = models.CharField(max_length=1,null=True)
    resposta = models.TextField(null=True)
    valor = models.FloatField(null=True)

    def __str__(self):
        return self.pergunta.numero+"-"+self.letra

class AreaAfetiva(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE,null=True)
    resposta = models.ForeignKey(RespostaAreaAfetiva, on_delete=models.CASCADE,null=True)

    def __str__(self):
        return self.paciente.nome+" "+self.resposta.pergunta.numero+"-"+self.resposta.letra

class Anamnesia(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE,null=True)
    areaAfetiva = models.CharField(max_length=20,null=True)
    inicio = models.DateTimeField(null=True)
    fim = models.DateTimeField(null=True,blank=True)
    retornos = models.IntegerField(null=True, blank=True)
    GrauDiferenciacao = models.IntegerField(null=True, blank=True)


    def __str__(self):
        return self.paciente.nome+" "+(self.inicio.strftime("%Y-%m-%d %H:%M:%S"))