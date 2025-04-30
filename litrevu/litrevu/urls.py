"""
URL configuration for litrevu project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
import authentication.views
import appli.views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', authentication.views.login_view, name='login'),
    path('logout/', authentication.views.logout_user, name='logout'),
    path('signup/', authentication.views.signup_page, name='signup'),
    path('flux/', appli.views.flux, name='flux'),
    path('ticket/', appli.views.create_ticket, name='ticket'),
    path('ticket/<int:ticket_id>/edit/', appli.views.edit_ticket, name='edit_ticket'),
    path('ticket/<int:ticket_id>/delete/', appli.views.delete_ticket, name='delete_ticket'),
    path('review/', appli.views.create_review, name='review'),
    path('review/<int:review_id>/edit/', appli.views.edit_review, name='edit_review'),
    path('review/<int:review_id>/delete/', appli.views.delete_review, name='delete_review'),
    path('response/<int:ticket_id>/', appli.views.create_response, name='response'),
    path('response/<int:response_id>/edit/', appli.views.edit_response, name='edit_response'),
    path('post_list/', appli.views.post_list, name='post_list'),
    path('subscriptions/', appli.views.check_user_to_follow, name='subscriptions'),
    path('subscriptions/<int:user_follows_id>/delete/', appli.views.delete_following,
         name='delete_following'),
    ]
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
