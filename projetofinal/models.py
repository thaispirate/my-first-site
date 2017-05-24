from datetime import datetime
from django.db import models
from django import forms
from django.utils import timezone
from datetime import date
from django.contrib.auth.models import User
from smart_selects.db_fields import ChainedForeignKey

# Create your models here.
class Estado(models.Model):
    estado = models.CharField(max_length=100,null=True, blank=True)
    sigla = models.CharField(max_length=3,null=True, blank=True)

    def __str__(self):
        return self.estado

class Municipio(models.Model):
    municipio = models.CharField(max_length=100,null=True, blank=True)
    estado = models.ForeignKey(Estado, on_delete=models.CASCADE,null=True)

    def __str__(self):
        return self.municipio

class Chave(models.Model):
    PADRAO =(
        ("usada","Usada"),
        ("livre","Livre")
    )
    chave = models.CharField(max_length=100)
    padrao = models.CharField(max_length=20,choices=PADRAO,null=True, blank=True)

    def __str__(self):
        return self.chave

class Psicologo(models.Model):
    usuario = models.OneToOneField(User)
    email = models.EmailField()
    nome = models.CharField(max_length=50,null=True)
    telefone = models.PositiveIntegerField(null=True, blank=True)
    celular = models.PositiveIntegerField(null=True, blank=True)
    estado = models.ForeignKey(Estado, on_delete=models.CASCADE,null=True)
    municipio = ChainedForeignKey(
        Municipio,
        chained_field="estado",
        chained_model_field="estado",
        show_all=False,
        auto_choose=True,
        sort=True,
        null=True)
    endereco = models.CharField(max_length=200,null=True)
    numero=models.PositiveIntegerField(null=True, blank=True)
    complemento = models.CharField(max_length=200,null=True)
    bairro = models.CharField(max_length=50,null=True)
    crp = models.CharField(max_length=50,null=True)

    def __str__(self):
        return self.nome


class Paciente(models.Model):
    usuario = models.OneToOneField(User)
    email = models.EmailField()
    nome = models.CharField(max_length=50,null=True)
    nascimento = models.DateField(null=True)
    sexo = models.CharField(max_length=10,null=True)
    escolaridade = models.CharField(max_length=15, null=True,blank=True)
    psicologo = models.ForeignKey(Psicologo, on_delete=models.CASCADE,null=True)
    habilitado = models.DateTimeField(null=True,blank=True)
    retornos = models.PositiveIntegerField(null=True, blank=True)
    tempo= models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return self.nome


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
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE,null=True)
    parente = models.CharField(max_length=10,choices=parentes,null=True)
    nome = models.CharField(max_length=50,null=True,blank=True)
    nascimento = models.DateField(null=True,blank=True)
    falecimento = models.DateField(null=True,blank=True)
    sexo = models.CharField(max_length=10,null=True,blank=True)
    escolaridade = models.CharField(max_length=15, null=True,blank=True)

    def __str__(self):
        return self.paciente.nome + "-" + self.parente


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
    nivel1 = models.FloatField(null=True,blank=True)
    nivel2 = models.FloatField(null=True,blank=True)
    nivel3 = models.FloatField(null=True,blank=True)
    nivel4 = models.FloatField(null=True,blank=True)
    nivel5 = models.FloatField(null=True,blank=True)


    def __str__(self):
        return self.pergunta.numero+"-"+self.letra


class Anamnesia(models.Model):
    PADRAO = (
        ("adaptativo","Adaptativo"),
        ("reativo","Reativo"),
        ("criativo","Criativo")

    )
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE,null=True)
    areaAfetiva = models.CharField(max_length=20,null=True)
    inicio = models.DateTimeField(null=True)
    fim = models.DateTimeField(null=True,blank=True)
    retornos = models.PositiveIntegerField(null=True, blank=True)
    padrao = models.CharField(max_length=20,choices=PADRAO,null=True, blank=True)


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
    filhos = models.PositiveIntegerField(null=True)
    filhas = models.PositiveIntegerField(null=True)
    relacaoAntes = models.CharField(max_length=20,null=True)
    filhosAntes = models.PositiveIntegerField(null=True, blank=True)
    filhasAntes = models.PositiveIntegerField(null=True, blank=True)
    filhosDepois = models.PositiveIntegerField(null=True, blank=True)
    filhasDepois = models.PositiveIntegerField(null=True, blank=True)


    def __str__(self):
        return self.paciente.nome + "-" + self.parente + " " + self.anamnesia.inicio.strftime("%Y-%m-%d %H:%M:%S")


class GrauIndiferenciacao(models.Model):
    PADRAO = (
        ("adaptativo","Adaptativo"),
        ("reativo","Reativo"),
        ("criativo","Criativo")

    )
    padrao = models.CharField(max_length=10,choices=PADRAO,null=True)
    resposta = models.TextField(null=True)

    def __str__(self):
        return self.padrao+"-"+self.resposta

class GrauIndiferenciacaoPaciente(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE,null=True)
    anamnesia = models.ForeignKey(Anamnesia, on_delete=models.CASCADE,null=True)
    resposta = models.ForeignKey(GrauIndiferenciacao, on_delete=models.CASCADE,null=True)


    def __str__(self):
        return self.paciente.nome+" "+self.anamnesia.inicio.strftime("%Y-%m-%d %H:%M:%S")+" "+self.resposta.padrao

class PerguntaSeletiva(models.Model):
    numero = models.CharField(max_length=10,null=True)
    pergunta = models.TextField(null=True)
    tipo = models.CharField(max_length=10,null=True,blank=True)

    def __str__(self):
        return self.numero

class RespostaSeletiva(models.Model):
    pergunta =  models.ForeignKey(PerguntaSeletiva, on_delete=models.CASCADE,null=True)
    letra = models.CharField(max_length=1,null=True)
    resposta = models.TextField(null=True)
    tipo = models.CharField(max_length=10,null=True,blank=True)
    nivel0 = models.FloatField(null=True,blank=True)
    nivel1 = models.FloatField(null=True,blank=True)
    nivel2 = models.FloatField(null=True,blank=True)
    nivel3 = models.FloatField(null=True,blank=True)
    nivel4 = models.FloatField(null=True,blank=True)
    nivel5 = models.FloatField(null=True,blank=True)
    nivel6 = models.FloatField(null=True,blank=True)

    def __str__(self):
        return self.pergunta.numero+"-"+self.letra

class Seletiva(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE,null=True)
    anamnesia = models.ForeignKey(Anamnesia, on_delete=models.CASCADE,null=True)
    resposta = models.ForeignKey(RespostaSeletiva, on_delete=models.CASCADE,null=True)


    def __str__(self):
        return self.paciente.nome+" "+self.resposta.pergunta.numero+"-"+self.resposta.letra+" "+self.anamnesia.inicio.strftime("%Y-%m-%d %H:%M:%S")

class PerguntaInterventiva(models.Model):
    numero = models.CharField(max_length=10,null=True)
    pergunta = models.TextField(null=True)

    def __str__(self):
        return self.numero


class Interventiva(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE,null=True)
    anamnesia = models.ForeignKey(Anamnesia, on_delete=models.CASCADE,null=True)
    resposta = models.TextField(null=True)
    pergunta = models.ForeignKey(PerguntaInterventiva,on_delete=models.CASCADE,null=True)


    def __str__(self):
        return self.paciente.nome+" "+self.anamnesia.inicio.strftime("%Y-%m-%d %H:%M:%S")+" "+self.pergunta.numero

class Recomendacao(models.Model):

    nome= models.CharField(max_length=20,null=True)
    intervalo = models.CharField(max_length=10,null=True)
    texto = models.TextField(null=True)

    def __str__(self):
        return self.nome + self.intervalo
