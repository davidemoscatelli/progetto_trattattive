# gestione_trattative/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # Include le URL di Django per login, logout, cambio password, ecc.
    path('accounts/', include('django.contrib.auth.urls')), 
    # Include le URL della nostra app (che creeremo tra poco)
    path('', include('trattative.urls')),
]