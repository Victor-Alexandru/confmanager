from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='conferences-index'),
    path('profile', views.user_profile, name='user-profile'),

]
