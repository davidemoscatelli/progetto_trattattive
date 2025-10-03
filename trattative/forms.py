# trattative/forms.py
from django import forms
from .models import Trattativa

class TrattativaForm(forms.ModelForm):
    class Meta:
        model = Trattativa
        # Specifichiamo i campi del modello da includere nel form
        fields = ['titolo', 'cliente', 'valore', 'stato', 'responsabile', 'note']
        
        # Opzionale: aggiungiamo delle classi CSS di Bootstrap per rendere i campi più gradevoli
        widgets = {
            'titolo': forms.TextInput(attrs={'class': 'form-control'}),
            'cliente': forms.TextInput(attrs={'class': 'form-control'}),
            'valore': forms.NumberInput(attrs={'class': 'form-control'}),
            'stato': forms.Select(attrs={'class': 'form-select'}),
            'responsabile': forms.Select(attrs={'class': 'form-select'}),
            'note': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }