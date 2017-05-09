import autocomplete_light

from .models import Psicologo

class PsicologoAutocomplete(autocomplete_light.AutocompleteModelBase):
    search_fields = ['estado', 'nome']
    model = Psicologo
autocomplete_light.register(PsicologoAutocomplete)