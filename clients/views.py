from django.views.generic.edit import FormView
from django.views.generic import ListView, DetailView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .form import ClientForm
from .models.client import Client
from .models.management import Transfusion


class ClientFormView(LoginRequiredMixin, FormView):
    template_name = "clients/client_form.html"
    form_class = ClientForm
    success_url = reverse_lazy("clients:client-list")

    def form_valid(self, form):
        # Save the Client record
        form.save()
        return super().form_valid(form)


class ClientListView(LoginRequiredMixin, ListView):
    model = Client
    template_name = "clients/client_list.html"
    context_object_name = "clients"

    def get_queryset(self):
        return Client.objects.all().order_by("full_name")


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    model = Client
    form_class = ClientForm
    template_name = "clients/client_form.html"
    success_url = reverse_lazy("clients:client-list")


class ClientDetailView(LoginRequiredMixin, DetailView):
    model = Client

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        client = get_object_or_404(Client, pk=self.kwargs['pk'])
        context['admissions'] = (
            client.client_admissions.all()
            .order_by('-date_of_admission')
        )
        return context


# Get a single client's admission records ordered by date_of_admission descending
class AdmissionListView(LoginRequiredMixin, ListView):
    model = Client
    template_name = "clients/client_admission_list.html"
    context_object_name = "admissions"

    def get_queryset(self):
        client = get_object_or_404(Client, pk=self.kwargs['pk'])
        return client.client_admissions.all().order_by('-date_of_admission')


# Get a single client's trnsfusion records ordered by date_of_transfusion descending
class TransfusionListView(LoginRequiredMixin, ListView):
    model = Client
    template_name = "clients/client_transfusion_list.html"
    context_object_name = "transfusions"

    def get_queryset(self):
        client = get_object_or_404(Client, pk=self.kwargs['pk'])
        return Transfusion.objects.filter(admission__client__id=client.id).order_by('-date_of_transfusion')


def test_view(request):
    from django.http import HttpResponse
    transfusion = Transfusion.objects.filter(admission__client__id=1).order_by('-date_of_transfusion')
    records = []
    for t in transfusion:
        records.append(f"Transfusion on {t.date_of_transfusion} - {t.admission.client.full_name}")
    return HttpResponse("Transfusion records: ".join(records))
