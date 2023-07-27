import datetime
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Card
from .form import CreateCardForm, UpdateCardForm
from users.models import User
from django.http import JsonResponse

def card_details(request, pk):
    card = Card.objects.get(pk=pk)
    t = User.objects.get(username=card.created_by)
    cards_per_user = t.created_by.all()
    context = {'card': card, 'cards_per_user': cards_per_user}
    return render(request, 'card/card_details.html', context)

def view_all_cards(request):
    cards = Card.objects.all().values()
    return JsonResponse(list(cards), safe=False)

def create_card(request):
    if request.method == 'POST':
        form = CreateCardForm(request.POST)
        if form.is_valid():
            var = form.save(commit=False)
            var.created_by = request.user
            var.card_status = 'Pending'
            var.save()
            messages.info(request, 'Your card was successfully submitted.')
            return redirect('dashboard')
        else:
            messages.warning(request, 'Something went wrong. Please check form input')
            return redirect('create-card')
    else:
        form = CreateCardForm()
        context = {'form':form}
        return render(request, 'card/create-card.html', context)

def update_card(request, pk):
    card = Card.objects.get(pk=pk)
    if request.method == 'POST':
        form = UpdateCardForm(request.POST, instance=card)
        if form.is_valid():
            form.save()
            messages.info(request, 'Your card info has been updated and all changes are saved in the Database.')
            return redirect('dashboard')
        else:
            messages.warning(request, 'Something went wrong. Please check form input')
            #return redirect('create_card')
    else:
        form = UpdateCardForm(instance=card)
        context = {'form':form}
        return render(request, 'card/update_card.html', context)

def all_cards(request):
    cards = Card.objects.filter(created_by=request.user).order_by('-date_created')
    context = {'cards':cards}
    return render(request, 'card/all_cards.html', context)

def card_queue(request):
    cards = Card.objects.filter(card_status='Pending')
    context = {'cards':cards}
    return render(request, 'card/card_queue.html', context)

def activate_card(request, pk):
    card = Card.objects.get(pk=pk)
    card.assigned_to = request.user
    card.card_status = 'Active'
    card.is_resolved = False
    card.accepted_date = datetime.datetime.now()
    card.save()
    messages.info(request, 'Card has been activated.')
    return redirect('workspace')

def disable_card(request, pk):
    card = Card.objects.get(pk=pk)
    card.card_status = 'Disable'
    card.is_resolved = True
    card.closed_date = datetime.datetime.now()
    card.save()
    messages.info(request, 'Card has been disabled.')
    return redirect('card-queue')

def workspace(request):
    cards = Card.objects.filter(assigned_to=request.user, is_resolved=False)
    context = {'cards':cards}
    return render(request, 'card/workspace.html', context)

def all_disabled_cards(request):
    cards = Card.objects.filter(assigned_to=request.user, is_resolved=True)
    context = {'cards': cards}
    return render(request, 'card/all_disabled_cards.html', context)







