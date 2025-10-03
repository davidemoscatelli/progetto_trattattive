# trattative/views.py

import json
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Sum
from .models import Trattativa, Task
from .forms import TrattativaForm, CommentoForm, TaskForm

@login_required
def kanban_board(request):
    trattative = Trattativa.objects.all()
    kanban_data = {
        stato[0]: trattative.filter(stato=stato[0]) 
        for stato in Trattativa.STATO_CHOICES
    }
    context = {'kanban_data': kanban_data}
    return render(request, 'trattative/kanban_board.html', context)

@login_required
def kpi_dashboard(request):
    trattative_vinte = Trattativa.objects.filter(stato='Vinta')
    trattative_perse = Trattativa.objects.filter(stato='Persa')
    totali_concluse = trattative_vinte.count() + trattative_perse.count()
    tasso_conversione = (trattative_vinte.count() / totali_concluse * 100) if totali_concluse > 0 else 0
    valore_totale_vinto = trattative_vinte.aggregate(Sum('valore'))['valore__sum'] or 0
    context = {
        'trattative_in_corso': Trattativa.objects.exclude(stato__in=['Vinta', 'Persa']).count(),
        'valore_in_corso': Trattativa.objects.exclude(stato__in=['Vinta', 'Persa']).aggregate(Sum('valore'))['valore__sum'] or 0,
        'tasso_conversione': tasso_conversione,
        'valore_totale_vinto': valore_totale_vinto,
    }
    return render(request, 'trattative/kpi_dashboard.html', context)

@login_required
def trattativa_create(request):
    if request.method == 'POST':
        form = TrattativaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('kanban_board')
    else:
        form = TrattativaForm()
    return render(request, 'trattative/trattativa_form.html', {'form': form, 'tipo_azione': 'Nuova'})

@login_required
def trattativa_update(request, pk):
    trattativa = get_object_or_404(Trattativa, pk=pk)
    if request.method == 'POST':
        form = TrattativaForm(request.POST, instance=trattativa)
        if form.is_valid():
            form.save()
            return redirect('kanban_board')
    else:
        form = TrattativaForm(instance=trattativa)
    return render(request, 'trattative/trattativa_form.html', {'form': form, 'tipo_azione': 'Modifica'})

@login_required
def trattativa_delete(request, pk):
    trattativa = get_object_or_404(Trattativa, pk=pk)
    if request.method == 'POST':
        trattativa.delete()
        return redirect('kanban_board')
    return render(request, 'trattative/trattativa_confirm_delete.html', {'trattativa': trattativa})

@login_required
def profilo(request):
    return render(request, 'trattative/profilo.html')

@login_required
def trattativa_detail(request, pk):
    trattativa = get_object_or_404(Trattativa, pk=pk)
    commenti = trattativa.commenti.all()
    
    if request.method == 'POST':
        form = CommentoForm(request.POST)
        if form.is_valid():
            nuovo_commento = form.save(commit=False)
            nuovo_commento.trattativa = trattativa
            nuovo_commento.autore = request.user
            nuovo_commento.save()
            return redirect('trattativa_detail', pk=trattativa.pk)
    else:
        form = CommentoForm()

    context = {
        'trattativa': trattativa,
        'commenti': commenti,
        'form': form,
    }
    return render(request, 'trattative/trattativa_detail.html', context)

@csrf_exempt
@login_required
def update_trattativa_status(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        trattativa_id = data.get('trattativa_id')
        nuovo_stato = data.get('nuovo_stato')
        try:
            trattativa = Trattativa.objects.get(pk=trattativa_id)
            trattativa.stato = nuovo_stato
            trattativa.save()
            return JsonResponse({'status': 'success', 'message': 'Stato aggiornato'})
        except Trattativa.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Trattativa non trovata'}, status=404)
    return JsonResponse({'status': 'error', 'message': 'Metodo non valido'}, status=400)

@login_required
def chart_data_api(request):
    vinte_count = Trattativa.objects.filter(stato='Vinta').count()
    perse_count = Trattativa.objects.filter(stato='Persa').count()
    data = {
        'labels': ['Vinte', 'Perse'],
        'data': [vinte_count, perse_count],
    }
    return JsonResponse(data)


@login_required
def task_list(request):
    # Mostriamo i task non completati, ordinati per priorità e data
    tasks = Task.objects.filter(completato=False)
    context = {
        'tasks': tasks
    }
    return render(request, 'trattative/task_list.html', context)

@login_required
def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.creato_da = request.user # Imposta chi ha creato il task
            task.save()
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'trattative/task_form.html', {'form': form})

@login_required
def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)
    return render(request, 'trattative/task_form.html', {'form': form})

@login_required
def task_complete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        task.completato = True
        task.save()
    return redirect('task_list')

@login_required
def homepage(request):
    # Recupera i task urgenti non completati assegnati all'utente loggato
    tasks_urgenti = Task.objects.filter(
        assegnato_a=request.user, 
        priorita=3, # 3 = Urgente
        completato=False
    )

    # Riepilogo trattative (per ora, le mostriamo tutte)
    trattative_in_corso_count = Trattativa.objects.exclude(stato__in=['Vinta', 'Persa']).count()
    trattative_vinte_count = Trattativa.objects.filter(stato='Vinta').count()
    valore_in_corso = Trattativa.objects.exclude(stato__in=['Vinta', 'Persa']).aggregate(Sum('valore'))['valore__sum'] or 0

    context = {
        'tasks_urgenti': tasks_urgenti,
        'trattative_in_corso_count': trattative_in_corso_count,
        'trattative_vinte_count': trattative_vinte_count,
        'valore_in_corso': valore_in_corso,
    }
    return render(request, 'trattative/homepage.html', context)