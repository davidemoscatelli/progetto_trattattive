from django import forms
from .models import Trattativa, Commento, Task # Assicurati di importare anche Commento

class TrattativaForm(forms.ModelForm):
    class Meta:
        model = Trattativa
        fields = ['titolo', 'cliente', 'valore', 'stato', 'responsabile', 'note']
        widgets = {
            'titolo': forms.TextInput(attrs={'class': 'form-control'}),
            'cliente': forms.TextInput(attrs={'class': 'form-control'}),
            'valore': forms.NumberInput(attrs={'class': 'form-control'}),
            'stato': forms.Select(attrs={'class': 'form-select'}),
            'responsabile': forms.Select(attrs={'class': 'form-select'}),
            'note': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }

# --- AGGIUNGI QUESTA CLASSE CHE MANCA ---
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
        labels = {
            'testo': '' # Nasconde l'etichetta del campo
        }

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['titolo', 'trattativa', 'assegnato_a', 'priorita', 'data_scadenza']

        # Usiamo un widget HTML5 per il campo data per un'esperienza migliore
        widgets = {
            'data_scadenza': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'titolo': forms.TextInput(attrs={'class': 'form-control'}),
            'trattativa': forms.Select(attrs={'class': 'form-select'}),
            'assegnato_a': forms.Select(attrs={'class': 'form-select'}),
            'priorita': forms.Select(attrs={'class': 'form-select'}),
        }
        
        labels = {
            'titolo': 'Titolo Attività',
            'trattativa': 'Collegata alla Trattativa (Opzionale)',
            'assegnato_a': 'Assegna a',
            'priorita': 'Priorità',
            'data_scadenza': 'Data di Scadenza',
        }