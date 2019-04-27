from django.contrib import admin
from django.urls import path,include
from .views import *

urlpatterns = [
    path("abstracts/<int:conf_id>/<int:rev_id>/", abstracts_view),
    path("accept/<int:rev_id>/<int:a_id>/", add_bid),
    path("reject/<int:rev_id>/<int:a_id>/", reject_bid),
    path("review/<int:rev_id>/", paper_table_view),
    path("paper/<int:a_id>/", paper_view),
    path("assign/<int:conf_id>/", assign_reviews),
    path("change_status/<int:rev_id>/<int:a_id>/", change_review),
    path("see_review/<int:rev_id>/<int:a_id>/", see_review),
    path("accept/<int:conf_id>/", accept_conference),
    path('',abstracts_view)
]