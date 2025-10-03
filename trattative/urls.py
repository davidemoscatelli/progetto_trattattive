from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # La rotta radice (homepage) ora punta alla nuova vista dashboard
    path('', views.homepage, name='homepage'),
    
    # La bacheca Kanban è stata spostata a /kanban/
    path('kanban/', views.kanban_board, name='kanban_board'),
    
    # Le altre pagine
    path('dashboard/', views.kpi_dashboard, name='kpi_dashboard'),
    path('tasks/', views.task_list, name='task_list'),
    path('profilo/', views.profilo, name='profilo'),

    # URL per la gestione delle Trattative
    path('trattativa/nuova/', views.trattativa_create, name='trattativa_create'),
    path('trattativa/<int:pk>/', views.trattativa_detail, name='trattativa_detail'),
    path('trattativa/modifica/<int:pk>/', views.trattativa_update, name='trattativa_update'),
    path('trattativa/elimina/<int:pk>/', views.trattativa_delete, name='trattativa_delete'),

    # URL per la gestione dei Task
    path('tasks/nuovo/', views.task_create, name='task_create'),
    path('tasks/<int:pk>/modifica/', views.task_update, name='task_update'),
    path('tasks/<int:pk>/completa/', views.task_complete, name='task_complete'),

    # URL per il cambio password
    path('profilo/password-change/', 
        auth_views.PasswordChangeView.as_view(
            template_name='trattative/password_change.html',
            success_url='/profilo/password-change/done/'
        ), 
        name='password_change'),
    path('profilo/password-change/done/', 
        auth_views.PasswordChangeDoneView.as_view(
            template_name='trattative/password_change_done.html'
        ), 
        name='password_change_done'),
    
    # URL per le API interne
    path('api/update-status/', views.update_trattativa_status, name='update_trattativa_status'),
    path('api/chart-data/', views.chart_data_api, name='chart_data_api'),
]