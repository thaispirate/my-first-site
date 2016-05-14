from django.contrib import admin
from .models import Paciente, Psicologo, QuestionarioAreaAfetiva, AreaAfetiva, Anamnesia
# Register your models here.

admin.site.register(Paciente)
admin.site.register(Psicologo)
admin.site.register(QuestionarioAreaAfetiva)
admin.site.register(AreaAfetiva)
admin.site.register(Anamnesia)