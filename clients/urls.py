from django.urls import path
from . import views

app_name = "clients"
urlpatterns = [
    path("add/", views.ClientFormView.as_view(), name="client-add"),
    path("update/<int:pk>", views.ClientUpdateView.as_view(), name="client-update"),
    path("detail/<int:pk>", views.ClientDetailView.as_view(), name="client-detail"),
    path("admissions/<int:pk>", views.AdmissionListView.as_view(), name="client-admission-list"),
    path("transfusions/<int:pk>", views.TransfusionListView.as_view(), name="client-transfusion-list"),
    path("", views.ClientListView.as_view(), name="client-list"),
    path("test/", views.test_view, name="client-test"),
]
