from django.contrib import admin
from .models import Paciente,Familia, Psicologo, PerguntaAreaAfetiva, RespostaAreaAfetiva,\
    AreaAfetiva, Anamnesia,Relacionamento, GrauIndiferenciacao, GrauIndiferenciacaoPaciente,\
    PerguntaSeletiva, RespostaSeletiva, Seletiva
# Register your models here.

admin.site.register(Paciente)
admin.site.register(Familia)
admin.site.register(Psicologo)
admin.site.register(PerguntaAreaAfetiva)
admin.site.register(RespostaAreaAfetiva)
admin.site.register(AreaAfetiva)
admin.site.register(Anamnesia)
admin.site.register(Relacionamento)
admin.site.register(GrauIndiferenciacao)
admin.site.register(GrauIndiferenciacaoPaciente)
admin.site.register(PerguntaSeletiva)
admin.site.register(RespostaSeletiva)
admin.site.register(Seletiva)