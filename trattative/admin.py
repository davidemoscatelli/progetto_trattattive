# trattative/admin.py

from django.contrib import admin
from .models import Trattativa, GruppoLavoro, Task, Commento

# Registra tutti i modelli per renderli visibili nel pannello di admin
admin.site.register(Trattativa)
admin.site.register(GruppoLavoro)
admin.site.register(Task)
admin.site.register(Commento)