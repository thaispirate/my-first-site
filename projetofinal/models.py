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
    SEXO = (
        ('F','Feminino'),
        ('M','Masculino')
    )
    sexo = models.CharField(max_length=10,null=True)


    def __str__(self):
        return self.usuario.username