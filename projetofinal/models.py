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

    def __str__(self):
        return self.usuario.first_name


class Familia(models.Model):
    parentes = (
        ("pai", "Pai"),
        ("mae", "Mãe"),
        ("avoPaterno", "Avô Paterno"),
        ("avoPaterna","Avó Paterna"),
        ("avoMaterno","Avô Materno"),
        ("avoMaterna","Avó Materna"),
        ("conjuge","Cônjuge"),

    )
    usuario = models.ForeignKey(Paciente, on_delete=models.CASCADE,null=True)
    parente = models.CharField(max_length=10,choices=parentes,null=True)
    nome = models.CharField(max_length=50,null=True)
    nascimento = models.DateField(null=True)
    falecimento = models.DateField(null=True,blank=True)
    sexo = models.CharField(max_length=10,null=True,blank=True)
    escolaridade = models.CharField(max_length=15, null=True,blank=True)

    def __str__(self):
        return self.usuario.nome + "-" + self.parente


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


class Anamnesia(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE,null=True)
    areaAfetiva = models.CharField(max_length=20,null=True)
    inicio = models.DateTimeField(null=True)
    fim = models.DateTimeField(null=True,blank=True)
    retornos = models.IntegerField(null=True, blank=True)
    GrauDiferenciacao = models.IntegerField(null=True, blank=True)


    def __str__(self):
        return self.paciente.nome+" "+(self.inicio.strftime("%Y-%m-%d %H:%M:%S"))

class AreaAfetiva(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE,null=True)
    resposta = models.ForeignKey(RespostaAreaAfetiva, on_delete=models.CASCADE,null=True)
    anamnesia = models.ForeignKey(Anamnesia, on_delete=models.CASCADE,null=True)

    def __str__(self):
        return self.paciente.nome+" "+self.resposta.pergunta.numero+"-"+self.resposta.letra+" "+self.anamnesia.inicio.strftime("%Y-%m-%d %H:%M:%S")


class Relacionamento(models.Model):
    parentes = (
        ("Pai", "Pai"),
        ("Mae", "Mãe"),
        ("AvoPaterno", "Avô Paterno"),
        ("AvoPaterna","Avó Paterna"),
        ("AvoMaterno","Avô Materno"),
        ("AvoMaterna","Avó Materna"),
        ("Paciente","Paciente"),
        ("Conjuge","Cônjuge"),

    )

    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE,null=True)
    anamnesia = models.ForeignKey(Anamnesia, on_delete=models.CASCADE,null=True)
    parente = models.CharField(max_length=10, choices=parentes,null=True)
    relacao = models.CharField(max_length=20,null=True)
    filhos = models.IntegerField(null=True)
    filhas = models.IntegerField(null=True)
    relacaoAntes = models.CharField(max_length=20,null=True)
    filhosAntes = models.IntegerField(null=True, blank=True)
    filhasAntes = models.IntegerField(null=True, blank=True)
    filhosDepois = models.IntegerField(null=True, blank=True)
    filhasDepois = models.IntegerField(null=True, blank=True)


    def __str__(self):
        return self.paciente.nome + "-" + self.parente + " " + self.anamnesia.inicio.strftime("%Y-%m-%d %H:%M:%S")

