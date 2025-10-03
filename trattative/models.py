from django.db import models
from django.contrib.auth.models import User

class Trattativa(models.Model):
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
    responsabile = models.ForeignKey(User, on_delete=models.PROTECT, related_name='trattative')
    data_creazione = models.DateTimeField(auto_now_add=True)
    ultima_modifica = models.DateTimeField(auto_now=True)
    note = models.TextField(blank=True, null=True)
    collaboratori = models.ManyToManyField(User, related_name='trattative_collabora', blank=True)
    def __str__(self):
        return self.titolo

    class Meta:
        ordering = ['-ultima_modifica']

# --- NUOVI MODELLI ---

class GruppoLavoro(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    membri = models.ManyToManyField(User, related_name='gruppi_lavoro')

    def __str__(self):
        return self.nome

class Task(models.Model):
    PRIORITA_CHOICES = [
        (3, 'Urgente'),
        (2, 'Media'),
        (1, 'Bassa'),
    ]
    titolo = models.CharField(max_length=200)
    trattativa = models.ForeignKey(Trattativa, on_delete=models.CASCADE, null=True, blank=True, related_name='tasks')
    assegnato_a = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='tasks')
    priorita = models.IntegerField(choices=PRIORITA_CHOICES, default=2)
    data_scadenza = models.DateField(null=True, blank=True)
    completato = models.BooleanField(default=False)
    creato_da = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks_create')
    collaboratori = models.ManyToManyField(User, related_name='task_collabora', blank=True)

    class Meta:
        ordering = ['-priorita', 'data_scadenza']

    def __str__(self):
        return self.titolo

class Commento(models.Model):
    trattativa = models.ForeignKey(Trattativa, on_delete=models.CASCADE, related_name='commenti')
    autore = models.ForeignKey(User, on_delete=models.CASCADE)
    testo = models.TextField()
    data_creazione = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['data_creazione']

    def __str__(self):
        return f'Commento di {self.autore} su {self.trattativa}'