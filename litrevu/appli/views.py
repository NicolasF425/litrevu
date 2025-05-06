from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from itertools import chain
from functools import wraps
import os
from . import forms, models
from authentication.models import User
from appli.models import UserFollows


# décorateur pour limiter les modifications ou suppression
# de ticket au créateur du ticket
def is_ticket_owner(view_func):
    @wraps(view_func)
    def wrapper(request, ticket_id, *args, **kwargs):
        from .models import Ticket  # Import à l'intérieur pour éviter les imports circulaires

        ticket = get_object_or_404(Ticket, id=ticket_id)

        if ticket.user == request.user:
            return view_func(request, ticket_id, *args, **kwargs)
        else:
            return redirect('flux')
    return wrapper


# décorateur pour limiter les modifications ou suppression
# de riview au créateur de la review
def is_review_owner(view_func):
    @wraps(view_func)
    def wrapper(request, review_id, *args, **kwargs):
        from .models import Review  # Import à l'intérieur pour éviter les imports circulaires

        review = get_object_or_404(Review, id=review_id)

        if review.user == request.user:
            return view_func(request, review_id, *args, **kwargs)
        else:
            return redirect('flux')
    return wrapper


def ticket_has_review(view_func):
    @wraps(view_func)
    def wrapper(request, ticket_id, *args, **kwargs):

        reviewed = models.Review.objects.filter(ticket_id=ticket_id).values_list('ticket', flat=True)

        if reviewed:
            return redirect('flux')
        else:
            return view_func(request, ticket_id, *args, **kwargs)
    return wrapper


@login_required
def flux(request):
    current_user = request.user
    tickets = models.Ticket.objects.all()
    reviews = models.Review.objects.all()

    followed = models.UserFollows.objects.filter(user=current_user).values_list('followed_user', flat=True)

    tickets = models.Ticket.objects.filter(
        Q(user=current_user) |  # Tickets créés par l'utilisateur connecté
        Q(user__in=followed)  # OU créés par les utilisateurs suivis
    )

    reviews = models.Review.objects.filter(
        Q(user=current_user) |  # Reviews créés par l'utilisateur connecté
        Q(user__in=followed) |  # OU créées par les utilisateurs suivis
        Q(ticket__user=current_user)  # OU dont le ticket a été créé par l'utilisateur connecté
    )

    # on fusionne les listes en posts et on les trie par ordre antichronologique
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
@is_ticket_owner
def edit_ticket(request, ticket_id):
    ticket_form = forms.TicketForm()
    ticket = get_object_or_404(models.Ticket, id=ticket_id)
    if ticket.user == request.user:
        ticket_form = forms.TicketForm(instance=ticket)
        if request.method == 'POST':
            # handle the POST request here
            ticket_form = forms.TicketForm(request.POST, request.FILES, instance=ticket)
            if (ticket_form.is_valid()):
                ticket = ticket_form.save(commit=False)
                ticket.user = request.user
                ticket_form.save()

                return redirect('post_list')

        context = {
            'ticket_form': ticket_form,
        }
        return render(request, 'appli/create_ticket.html', context=context)
    else:
        return redirect('flux')


@login_required
@is_ticket_owner
def delete_ticket(request, ticket_id):
    ticket = models.Ticket.objects.get(id=ticket_id)

    if request.method == 'POST':
        if ticket.image:
            if os.path.isfile(ticket.image.path):
                os.remove(ticket.image.path)
        # handle the POST request here
        ticket.delete()
        return redirect('flux')

    return render(request, 'appli/delete_ticket.html', {'ticket': ticket})


# Créer un ticket et une review associée
# puis les sauvegarder
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
@is_review_owner
def edit_review(request, review_id):
    review = models.Review.objects.get(id=review_id)
    ticket = get_object_or_404(models.Ticket, id=review.ticket_id)
    review_form = forms.ReviewForm()
    if request.method == 'POST':
        # handle the POST request here
        review_form = forms.ReviewForm(request.POST, )
        if (review_form.is_valid()):
            review = review_form.save(commit=False)
            review.user = request.user
            review.rating = int(review_form.cleaned_data['rating'])
            review.ticket = ticket
            review.save()
            return redirect('flux')

    context = {
        'ticket': ticket,
        'review_form': review_form,
        'message': "Modifier votre critique",
    }
    return render(request, 'appli/create_response.html', context=context)


@login_required
@is_review_owner
def delete_review(request, review_id):
    review = models.Review.objects.get(id=review_id)

    if request.method == 'POST':
        # handle the POST request here
        review.delete()
        return redirect('flux')

    return render(request, 'appli/delete_review.html', {'review': review})


# Créer une review en réponse à un ticket
@login_required
@ticket_has_review
def create_response(request, ticket_id):
    ticket = get_object_or_404(models.Ticket, id=ticket_id)
    review_form = forms.ReviewForm()
    if request.method == 'POST':
        # handle the POST request here
        review_form = forms.ReviewForm(request.POST, )
        if (review_form.is_valid()):
            review = review_form.save(commit=False)
            review.user = request.user
            review.rating = int(review_form.cleaned_data['rating'])
            review.ticket = ticket
            review.save()
            return redirect('flux')

    context = {
        'ticket': ticket,
        'review_form': review_form,
        'message': "Créer une critique",
    }
    return render(request, 'appli/create_response.html', context=context)


@login_required
def check_user_to_follow(request):
    message = ""
    form = forms.UserToFollowForm(request.POST)
    user_follows = models.UserFollows()
    if request.method == 'POST':
        if form.is_valid():
            user_to_follow = form.cleaned_data['user_to_follow']
            resultats = User.objects.filter(username__icontains=user_to_follow)
            #  si l'utilisateur existe
            if resultats:
                target_user = resultats[0]  # Récupérer l'objet User
                # Vérifier si l'utilisateur suit déjà cette personne
                already_following = UserFollows.objects.filter(
                    user=request.user,
                    followed_user=target_user
                ).exists()
                if not already_following:
                    user_follows.user = request.user
                    user_follows.followed_user = target_user
                    user_follows.save()
                else:
                    message = "vous suivez déjà cet utilisateur"
            else:
                message = "Utilisateur non trouvé"
    followed_users = UserFollows.objects.filter(user=request.user)
    followers = User.objects.filter(
        id__in=request.user.followed_by.all().values_list('user', flat=True)
    )

    context = {
        'form': form,
        'followed_users': followed_users,
        'followers': followers,
        'message': message,

    }
    return render(request, 'appli/subscriptions.html', context=context)


@login_required
def delete_following(request, user_follows_id):
    following = models.UserFollows.objects.get(id=user_follows_id)

    if request.method == 'POST':
        # handle the POST request here
        following.delete()
        return redirect('subscriptions')

    return render(request, 'appli/delete_following.html', {'following': following})
