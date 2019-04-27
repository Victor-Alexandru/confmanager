from django.urls import path,include
from . import views
urlpatterns = [
    path('',views.index,name="confsite-index"),
    path('bid/',include('bidreview.urls')),
    path('auth/',include('users.urls')),
    path('see_conf/',include("joinsubmit.urls")),
    path('conferences/',include("conference.urls"))
]

