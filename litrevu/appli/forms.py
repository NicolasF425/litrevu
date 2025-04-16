from django import forms
from . import models


class TicketForm(forms.ModelForm):
    class Meta:
        model = models.Ticket
        fields = ['title', 'description', 'image']


class ReviewForm(forms.ModelForm):
    class Meta:
        model = models.Review
        fields = ['headline', 'rating', 'body']
        widgets = {
            'body': forms.Textarea(attrs={'rows': 4, 'cols': 60}),
        }


class UserToFollowForm(forms.Form):
    user_to_follow = forms.CharField()


class UserFollowedForm(forms.Form):
    user_followed = forms.Textarea(attrs={'rows': 1, 'cols': 60})


class FollowersForm(forms.Form):
    followers = forms.Textarea(attrs={'rows': 1, 'cols': 80})
