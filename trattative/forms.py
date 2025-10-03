# trattative/forms.py

from django import forms
from django.contrib.auth.models import User
from .models import Trattativa, Commento, Task

class TrattativaForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['responsabile'].required = False

    class Meta:
        model = Trattativa
        fields = ['titolo', 'cliente', 'valore', 'stato', 'responsabile', 'note', 'collaboratori']
        widgets = {
            'titolo': forms.TextInput(attrs={'class': 'form-control'}),
            'cliente': forms.TextInput(attrs={'class': 'form-control'}),
            'valore': forms.NumberInput(attrs={'class': 'form-control'}),
            'stato': forms.Select(attrs={'class': 'form-select'}),
            'responsabile': forms.Select(attrs={'class': 'form-select'}),
            'note': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'collaboratori': forms.SelectMultiple(attrs={'class': 'form-select', 'size': '5'}),
        }

class CommentoForm(forms.ModelForm):
    class Meta:
        model = Commento
        fields = ['testo']
        widgets = {
            'testo': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 3, 
                'placeholder': 'Scrivi un commento...'
            }),
        }
        labels = { 'testo': '' }

# --- QUESTA È LA CLASSE DA CORREGGERE ---
class TaskForm(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Filtra la lista degli utenti assegnabili
        gruppi_utente = user.gruppi_lavoro.all()
        membri_dei_gruppi = User.objects.filter(gruppi_lavoro__in=gruppi_utente).distinct()
        
        if membri_dei_gruppi.exists():
            self.fields['assegnato_a'].queryset = membri_dei_gruppi
        else:
            self.fields['assegnato_a'].queryset = User.objects.filter(pk=user.pk)

    class Meta:
        model = Task
        fields = ['titolo', 'trattativa', 'assegnato_a', 'priorita', 'data_scadenza', 'collaboratori']
        widgets = {
            'data_scadenza': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'titolo': forms.TextInput(attrs={'class': 'form-control'}),
            'trattativa': forms.Select(attrs={'class': 'form-select'}),
            'assegnato_a': forms.Select(attrs={'class': 'form-select'}),
            'priorita': forms.Select(attrs={'class': 'form-select'}),
            'collaboratori': forms.SelectMultiple(attrs={'class': 'form-select', 'size': '5'}),
        }
        labels = {
            'titolo': 'Titolo Attività',
            'trattativa': 'Collegata alla Trattativa (Opzionale)',
            'assegnato_a': 'Assegna a',
            'priorita': 'Priorità',
            'data_scadenza': 'Data di Scadenza',
            'collaboratori': 'Altri Collaboratori',
        }