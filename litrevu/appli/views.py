from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from . import forms


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
    context = {
        'ticket_form': ticket_form,
    }
    return render(request, 'appli/create_ticket.html', context=context)
