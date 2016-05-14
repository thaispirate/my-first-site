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

class QuestionarioAreaAfetiva(models.Model):
    numero = models.CharField(max_length=10,null=True)
    pergunta = models.TextField(null=True)
    respostaA = models.TextField(null=True,blank=True)
    respostaB = models.TextField(null=True,blank=True)
    respostaC = models.TextField(null=True,blank=True)
    respostaD = models.TextField(null=True,blank=True)
    respostaE = models.TextField(null=True,blank=True)
    respostaF = models.TextField(null=True,blank=True)
    respostaG = models.TextField(null=True,blank=True)
    valorA = models.FloatField(null=True,blank=True)
    valorB = models.FloatField(null=True,blank=True)
    valorC = models.FloatField(null=True,blank=True)
    valorD = models.FloatField(null=True,blank=True)
    valorE = models.FloatField(null=True,blank=True)
    valorF = models.FloatField(null=True,blank=True)
    valorG = models.FloatField(null=True,blank=True)

    def __str__(self):
        return self.numero

class AreaAfetiva(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE,null=True)
    afetivoRelacional = models.FloatField(null=True)
    produtividade = models.FloatField(null=True)
    socioCultural = models.FloatField(null=True)
    organico = models.FloatField(null=True)
    espiritual = models.FloatField(null=True)

    def __str__(self):
        return self.paciente.nome

class Anamnesia(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE,null=True)
    area = models.CharField(max_length=50,null=True,blank=True)
    inicio = models.DateField(null=True)
    fim = models.DateField(null=True,blank=True)
    retornos = models.IntegerField(null=True, blank=True)
    GrauDiferenciacao = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.paciente.nome