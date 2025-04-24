from django import forms
from . import models


class TicketForm(forms.ModelForm):
    class Meta:
        model = models.Ticket
        fields = ['title', 'description', 'image']


class ReviewForm(forms.ModelForm):
    RATING_CHOICES = [
        (0, '0'),
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5')
    ]

    rating = forms.ChoiceField(
        choices=RATING_CHOICES,
        widget=forms.RadioSelect(),
        label='Rating'
    )

    class Meta:
        model = models.Review
        fields = ['headline', 'rating', 'body']
        widgets = {
            'rating': 'Note',
            'body': forms.Textarea(attrs={'rows': 4, 'cols': 60}),
        }


class UserToFollowForm(forms.Form):
    user_to_follow = forms.CharField()


class UserFollowedForm(forms.Form):
    user_followed = forms.Textarea(attrs={'rows': 1, 'cols': 60})


class FollowersForm(forms.Form):
    followers = forms.Textarea(attrs={'rows': 1, 'cols': 80})
