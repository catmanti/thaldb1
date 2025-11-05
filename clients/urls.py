from django.urls import path
from . import views

app_name = "clients"
urlpatterns = [
    path("add/", views.ClientFormView.as_view(), name="client-add"),
    path("update/<int:pk>", views.ClientUpdateView.as_view(), name="client-update"),
    path("", views.ClientListView.as_view(), name="client-list"),
]
