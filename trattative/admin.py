# trattative/admin.py

from django.contrib import admin
from .models import Trattativa, GruppoLavoro, Task, Commento

# Usiamo il decoratore per i modelli con configurazioni personalizzate
@admin.register(Trattativa)
class TrattativaAdmin(admin.ModelAdmin):
    list_display = ('titolo', 'cliente', 'stato', 'responsabile', 'valore')
    filter_horizontal = ('collaboratori',)

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('titolo', 'assegnato_a', 'priorita', 'completato')
    filter_horizontal = ('collaboratori',)

# Registriamo gli altri modelli in modo semplice, perché non hanno personalizzazioni
admin.site.register(GruppoLavoro)
admin.site.register(Commento)