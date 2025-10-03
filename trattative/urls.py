# trattative/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # La homepage (es. 'http://127.0.0.1:8000/') mostrerà la bacheca Kanban
    path('', views.kanban_board, name='kanban_board'),
    # Una pagina per la dashboard con i KPI
    path('dashboard/', views.kpi_dashboard, name='kpi_dashboard'),

    path('trattativa/nuova/', views.trattativa_create, name='trattativa_create'),
    path('trattativa/modifica/<int:pk>/', views.trattativa_update, name='trattativa_update'),
    path('trattativa/elimina/<int:pk>/', views.trattativa_delete, name='trattativa_delete'),
    path('api/update-status/', views.update_trattativa_status, name='update_trattativa_status'),
    path('api/chart-data/', views.chart_data_api, name='chart_data_api'),
]