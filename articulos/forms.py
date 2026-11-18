# articulos/forms.py
from django import forms

from .models import Comentario


class FormularioComentario(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ["comentario"]
        labels = {"comentario": "Tu comentario"}
        widgets = {"comentario": forms.Textarea(attrs={"rows": 3})}