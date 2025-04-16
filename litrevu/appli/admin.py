from django.contrib import admin

from appli.models import Ticket, Review, UserFollows

admin.site.register(Ticket)
admin.site.register(Review)
admin.site.register(UserFollows)
