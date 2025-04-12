from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from . import forms, models


@login_required
def flux(request):
    return render(request, 'appli/flux.html')


@login_required
def create_ticket(request):
    ticket_form = forms.TicketForm()
    if request.method == 'POST':
        # handle the POST request here
        ticket_form = forms.TicketForm(request.POST, request.FILES)
        if (ticket_form.is_valid()):
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            ticket_form.save()

            return redirect('flux')

    context = {
        'ticket_form': ticket_form,
    }
    return render(request, 'appli/create_ticket.html', context=context)


@login_required
def edit_ticket(request, ticket_id):
    ticket_form = forms.TicketForm()
    ticket = get_object_or_404(models.Ticket, id=ticket_id)
    ticket_form = forms.TicketForm(instance=ticket)
    if request.method == 'POST':
        # handle the POST request here
        ticket_form = forms.TicketForm(request.POST, instance=ticket)
        if (ticket_form.is_valid()):
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            ticket_form.save()

            return redirect('flux')

    context = {
        'ticket_form': ticket_form,
    }
    return render(request, 'appli/create_ticket.html', context=context)


@login_required
def create_critic(request):
    ticket_form = forms.TicketForm()
    critic_form = forms.CriticForm()
    if request.method == 'POST':
        # handle the POST request here
        ticket_form = forms.TicketForm(request.POST, request.FILES, prefix='first')
        critic_form = forms.CriticForm(request.POST, prefix='second')
        if all([ticket_form.is_valid(), critic_form.is_valid()]):
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            critic = critic_form.save(commit=False)
            critic.user = request.user
            critic.ticket = ticket
            critic.save()

            return redirect('flux')

    context = {
        'ticket_form': ticket_form,
        'critic_form': critic_form,
    }
    return render(request, 'appli/create_critic.html', context=context)


@login_required
def create_response(request, ticket_id):
    ticket = get_object_or_404(models.Ticket, id=ticket_id)
    ticket_form = forms.TicketForm(instance=ticket)
    critic_form = forms.CriticForm()
    if request.method == 'POST':
        # handle the POST request here
        critic_form = forms.CriticForm(request.POST, )
        if (critic_form.is_valid()):
            critic = critic_form.save(commit=False)
            critic.user = request.user
            critic.ticket = ticket
            critic.save()

            return redirect('flux')

    context = {
        'ticket_form': ticket_form,
        'critic_form': critic_form,
    }
    return render(request, 'appli/create_response.html', context=context)
