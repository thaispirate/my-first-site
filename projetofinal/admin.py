from django.contrib import admin
from .models import Paciente, Psicologo, PerguntaAreaAfetiva, RespostaAreaAfetiva, AreaAfetiva, Anamnesia
# Register your models here.

admin.site.register(Paciente)
admin.site.register(Psicologo)
admin.site.register(PerguntaAreaAfetiva)
admin.site.register(RespostaAreaAfetiva)
admin.site.register(AreaAfetiva)
admin.site.register(Anamnesia)