from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from itertools import chain
from . import forms, models
from authentication.models import User


@login_required
def flux(request):
    current_user = request.user
    tickets = models.Ticket.objects.all()
    reviews = models.Review.objects.all()

    followed = models.UserFollows.objects.filter(followed_user=current_user).values_list('user', flat=True)

    tickets = models.Ticket.objects.filter(
        Q(user=current_user) |  # Tickets créés par l'utilisateur connecté
        Q(user__in=followed)  # OU créés par les utilisateurs suivis
    ).order_by('-time_created')

    reviews = models.Review.objects.filter(
        Q(user=current_user) |  # Reviews crééss par l'utilisateur connecté
        Q(user__in=followed)  # OU créées par les utilisateurs suivis
    ).order_by('-time_created')

    posts = list(chain(tickets, reviews))
    posts.sort(key=lambda x: x.time_created, reverse=True)

    context = {
        'posts': posts,
    }
    return render(request, 'appli/flux.html', context=context)


@login_required
def post_list(request):
    current_user = request.user
    tickets = models.Ticket.objects.all()
    reviews = models.Review.objects.all()

    tickets = models.Ticket.objects.filter(
        Q(user=current_user)   # Tickets créés par l'utilisateur connecté
    ).order_by('-time_created')

    reviews = models.Review.objects.filter(
        Q(user=current_user)   # Reviews crééss par l'utilisateur connecté

    ).order_by('-time_created')

    posts = list(chain(tickets, reviews))
    posts.sort(key=lambda x: x.time_created, reverse=True)

    context = {
        'posts': posts,
    }
    return render(request, 'appli/post_list.html', context=context)


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
    if ticket.user == request.user:
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
    else:
        return redirect('flux')


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
    review_form = forms.ReviewForm()
    if request.method == 'POST':
        # handle the POST request here
        ticket_form = forms.TicketForm(request.POST, request.FILES, prefix='first')
        review_form = forms.ReviewForm(request.POST, prefix='second')
        if all([ticket_form.is_valid(), review_form.is_valid()]):
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            review = review_form.save(commit=False)
            review.user = request.user
            review.ticket = ticket
            review.save()

            return redirect('flux')

    context = {
        'ticket_form': ticket_form,
        'review_form': review_form,
    }
    return render(request, 'appli/create_review.html', context=context)


@login_required
def edit_review(request, review_id):
    review = get_object_or_404(models.Review, id=review_id)
    ticket = get_object_or_404(models.Ticket, id=review.ticket.id)
    review_form = forms.ReviewForm(instance=review, prefix='second')
    ticket_form = forms.TicketForm(instance=ticket, prefix='first')
    if request.method == 'POST':
        # handle the POST request here
        ticket_form = forms.TicketForm(request.POST, request.FILES, prefix='first', instance=ticket)
        review_form = forms.reviewForm(request.POST, prefix='second', instance=review)
        if all([ticket_form.is_valid(), review_form.is_valid()]):
            ticket = ticket_form.save(commit=False)
            ticket.save()
            review = review_form.save(commit=False)
            review.ticket = ticket
            review.save()

            return redirect('flux')

    context = {
        'ticket_form': ticket_form,
        'review_form': review_form,
    }
    return render(request, 'appli/create_review.html', context=context)


@login_required
def delete_review(request, review_id):
    review = models.Review.objects.get(id=review_id)

    if request.method == 'POST':
        # handle the POST request here
        review.delete()
        return redirect('flux')

    return render(request, 'appli/delete_review.html', {'review': review})


@login_required
def create_response(request, ticket_id):
    ticket = get_object_or_404(models.Ticket, id=ticket_id)
    ticket_form = forms.TicketForm(instance=ticket)
    review_form = forms.ReviewForm()
    if request.method == 'POST':
        # handle the POST request here
        review_form = forms.ReviewForm(request.POST, )
        if (review_form.is_valid()):
            review = review_form.save(commit=False)
            review.user = request.user
            review.ticket = ticket
            review.save()

            return redirect('flux')

    context = {
        'ticket_form': ticket_form,
        'review_form': review_form,
    }
    return render(request, 'appli/create_response.html', context=context)


@login_required
def edit_response(request, response_id):
    response = get_object_or_404(models.Review, id=response_id)
    ticket = get_object_or_404(models.Ticket, id=response.ticket.id)
    ticket_form = forms.TicketForm(instance=ticket)
    review_form = forms.ReviewForm(instance=response)
    if request.method == 'POST':
        # handle the POST request here
        review_form = forms.ReviewForm(request.POST, instance=response)
        if (review_form.is_valid()):
            review = review_form.save(commit=False)
            review.save()

            return redirect('flux')

    context = {
        'ticket_form': ticket_form,
        'review_form': review_form,
    }
    return render(request, 'appli/create_response.html', context=context)


@login_required
def check_user_to_follow(request):
    form = forms.UserToFollowForm(request.POST)
    user_follows = models.UserFollows()
    if request.method == 'POST':
        if form.is_valid():
            user_to_follow = form.cleaned_data['user_to_follow']
            resultats = User.objects.filter(username__icontains=user_to_follow)
            user_follows.user = request.user
            user_follows.followed_user = resultats[0]
            user_follows.save()
    followed_users = User.objects.filter(
        id__in=request.user.following.all().values_list('followed_user', flat=True)
    )
    followers = User.objects.filter(
        id__in=request.user.followed_by.all().values_list('user', flat=True)
    )

    context = {
        'form': form,
        'followed_users': followed_users,
        'followers': followers,

    }
    return render(request, 'appli/subscriptions.html', context=context)
