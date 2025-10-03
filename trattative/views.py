# trattative/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Trattativa
from .forms import TrattativaForm
from django.db.models import Sum, Count
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


# Il decoratore @login_required protegge la pagina:
# solo gli utenti loggati possono vederla.
@login_required
def kanban_board(request):
    trattative = Trattativa.objects.all()

    # Raggruppiamo le trattative per il loro stato
    kanban_data = {
        stato[0]: trattative.filter(stato=stato[0]) 
        for stato in Trattativa.STATO_CHOICES
    }

    context = {
        'kanban_data': kanban_data
    }
    return render(request, 'trattative/kanban_board.html', context)

@login_required
def kpi_dashboard(request):
    trattative_vinte = Trattativa.objects.filter(stato='Vinta')
    trattative_perse = Trattativa.objects.filter(stato='Persa')

    totali_concluse = trattative_vinte.count() + trattative_perse.count()

    # Calcolo dei KPI
    tasso_conversione = (trattative_vinte.count() / totali_concluse * 100) if totali_concluse > 0 else 0
    valore_totale_vinto = trattative_vinte.aggregate(Sum('valore'))['valore__sum'] or 0
    valore_medio_vinto = valore_totale_vinto / trattative_vinte.count() if trattative_vinte.count() > 0 else 0

    context = {
        'trattative_totali': Trattativa.objects.count(),
        'trattative_in_corso': Trattativa.objects.filter(stato='In Corso').count(),
        'valore_in_corso': Trattativa.objects.filter(stato='In Corso').aggregate(Sum('valore'))['valore__sum'] or 0,
        'tasso_conversione': tasso_conversione,
        'valore_totale_vinto': valore_totale_vinto,
        'valore_medio_vinto': valore_medio_vinto,
    }
    return render(request, 'trattative/kpi_dashboard.html', context)

@login_required
def trattativa_create(request):
    if request.method == 'POST':
        # Se il form viene inviato, lo processiamo
        form = TrattativaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('kanban_board') # Reindirizziamo al Kanban dopo il salvataggio
    else:
        # Se la pagina viene solo visitata, mostriamo un form vuoto
        form = TrattativaForm()
        
    return render(request, 'trattative/trattativa_form.html', {'form': form, 'tipo_azione': 'Nuova'})

@login_required
def trattativa_update(request, pk):
    # Recuperiamo l'oggetto specifico da modificare o mostriamo un errore 404
    trattativa = get_object_or_404(Trattativa, pk=pk)
    
    if request.method == 'POST':
        # Processiamo il form con i dati inviati e l'istanza esistente
        form = TrattativaForm(request.POST, instance=trattativa)
        if form.is_valid():
            form.save()
            return redirect('kanban_board')
    else:
        # Mostriamo il form pre-compilato con i dati dell'istanza
        form = TrattativaForm(instance=trattativa)
        
    return render(request, 'trattative/trattativa_form.html', {'form': form, 'tipo_azione': 'Modifica'})


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
def trattativa_delete(request, pk):
    # Recuperiamo l'oggetto da eliminare
    trattativa = get_object_or_404(Trattativa, pk=pk)
    
    if request.method == 'POST':
        # Se l'utente conferma (inviando il form), eliminiamo l'oggetto
        trattativa.delete()
        # E reindirizziamo alla bacheca Kanban
        return redirect('kanban_board')
        
    # Se la richiesta è GET, mostriamo la pagina di conferma
    return render(request, 'trattative/trattativa_confirm_delete.html', {'trattativa': trattativa})

@login_required
def chart_data_api(request):
    # Contiamo le trattative vinte e perse
    vinte_count = Trattativa.objects.filter(stato='Vinta').count()
    perse_count = Trattativa.objects.filter(stato='Persa').count()

    # Prepariamo i dati per il grafico
    data = {
        'labels': ['Vinte', 'Perse'],
        'data': [vinte_count, perse_count],
    }
    
    # Restituiamo i dati come risposta JSON
    return JsonResponse(data)