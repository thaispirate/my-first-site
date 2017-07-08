from django.utils import timezone
from haystack import indexes

from .models import Psicologo


class NoteIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    title = indexes.CharField(model_attr='cidade',null=True)
    body = indexes.CharField(model_attr='estado',null=True)

    def get_model(self):
        return Psicologo

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()