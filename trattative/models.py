# trattative/models.py
from django.db import models
from django.contrib.auth.models import User

class Trattativa(models.Model):
    # Definiamo gli stati possibili per una trattativa
    STATO_CHOICES = [
        ('Da Contattare', 'Da Contattare'),
        ('Contattato', 'Contattato'),
        ('Demo', 'Demo'),
        ('Preventivo Tecnico', 'Preventivo Tecnico'),
        ('Preventivo Commerciale', 'Preventivo Commerciale'),
        ('Vinta', 'Vinta'),
        ('Persa', 'Persa'),
    ]

    titolo = models.CharField(max_length=200)
    cliente = models.CharField(max_length=100)
    valore = models.DecimalField(max_digits=10, decimal_places=2, help_text="Valore stimato della trattativa")
    stato = models.CharField(max_length=30, choices=STATO_CHOICES, default='Da Contattare')
    responsabile = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    data_creazione = models.DateTimeField(auto_now_add=True)
    ultima_modifica = models.DateTimeField(auto_now=True)
    note = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.titolo

    class Meta:
        ordering = ['-ultima_modifica']