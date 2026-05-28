from django.urls import path
from .views import groups_view, add_member

urlpatterns = [
    path("", groups_view),
    path("<int:group_id>/members/", add_member),
]
