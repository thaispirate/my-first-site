import autocomplete_light

from .models import Psicologo

class PsicologoAutocomplete(autocomplete_light.AutocompleteModelBase):
    search_fields = ['nome']

autocomplete_light.register(Psicologo, PsicologoAutocomplete)