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


def ticket_list(request):
    tickets = models.Ticket.objects.all()
    return render(request, 'appli/ticket_list.html', {'tickets': tickets})


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
def delete_ticket(request, ticket_id):
    ticket = models.Ticket.objects.get(id=ticket_id)

    if request.method == 'POST':
        # handle the POST request here
        ticket.delete()
        return redirect('flux')

    return render(request, 'appli/delete_ticket.html', {'ticket': ticket})


@login_required
def create_review(request):
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
def edit_review(request, critic_id):
    critic = get_object_or_404(models.Review, id=critic_id)
    ticket = get_object_or_404(models.Ticket, id=critic.ticket.id)
    critic_form = forms.CriticForm(instance=critic, prefix='second')
    ticket_form = forms.TicketForm(instance=ticket, prefix='first')
    if request.method == 'POST':
        # handle the POST request here
        ticket_form = forms.TicketForm(request.POST, request.FILES, prefix='first', instance=ticket)
        critic_form = forms.CriticForm(request.POST, prefix='second', instance=critic)
        if all([ticket_form.is_valid(), critic_form.is_valid()]):
            ticket = ticket_form.save(commit=False)
            ticket.save()
            critic = critic_form.save(commit=False)
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


@login_required
def edit_response(request, response_id):
    response = get_object_or_404(models.Review, id=response_id)
    ticket = get_object_or_404(models.Ticket, id=response.ticket.id)
    ticket_form = forms.TicketForm(instance=ticket)
    critic_form = forms.CriticForm(instance=response)
    if request.method == 'POST':
        # handle the POST request here
        critic_form = forms.CriticForm(request.POST, instance=response)
        if (critic_form.is_valid()):
            critic = critic_form.save(commit=False)
            critic.save()

            return redirect('flux')

    context = {
        'ticket_form': ticket_form,
        'critic_form': critic_form,
    }
    return render(request, 'appli/create_response.html', context=context)
