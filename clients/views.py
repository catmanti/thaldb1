from django.views.generic.edit import FormView
from django.views.generic import ListView, DetailView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.views.generic.edit import UpdateView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .form import ClientForm, AdmissionForm
from .models.client import Client
from .models.management import Transfusion, Admission


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
            .order_by('-date_of_admission')[:4]
        )
        return context


# # Get a single client's admission records ordered by date_of_admission descending
# class AdmissionListView(LoginRequiredMixin, ListView):
#     model = Client
#     template_name = "clients/client_admission_list.html"
#     context_object_name = "admissions"

#     def get_queryset(self):
#         client = get_object_or_404(Client, pk=self.kwargs['pk'])
#         return client.client_admissions.all().order_by('-date_of_admission')

class AdmissionListView(LoginRequiredMixin, ListView):
    model = Admission
    template_name = "clients/client_admission_list.html"
    context_object_name = "admissions"

    def get_queryset(self):
        return Admission.objects.filter(
            client_id=self.kwargs["pk"]
        ).order_by("-date_of_admission")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["client_id"] = self.kwargs["pk"]
        return context


class AdmissionCreateView(LoginRequiredMixin, CreateView):
    model = Admission
    form_class = AdmissionForm
    template_name = "clients/client_admission_form.html"

    def get_initial(self):
        initial = super().get_initial()
        initial["client"] = self.kwargs["pk"]   # pre-fill but hidden
        return initial

    def form_valid(self, form):
        form.instance.client_id = self.kwargs["pk"]  # attach client
        return super().form_valid(form)


class AdmissionUpdateView(LoginRequiredMixin, UpdateView):
    model = Admission
    form_class = AdmissionForm
    template_name = "clients/client_admission_form.html"

    def get_success_url(self):
        client_id = self.object.client.id
        return reverse_lazy("clients:client-detail", kwargs={"pk": client_id})


# Get a single client's trnsfusion records ordered by date_of_transfusion descending
class TransfusionListView(LoginRequiredMixin, ListView):
    model = Client
    template_name = "clients/client_transfusion_list.html"
    context_object_name = "transfusions"

    def get_queryset(self):
        client = get_object_or_404(Client, pk=self.kwargs['pk'])
        return Transfusion.objects.filter(admission__client__id=client.id).order_by('-date_of_transfusion')


# Get a single client's investigation records ordered by date_done descending
class InvestigationListView(LoginRequiredMixin, ListView):
    model = Client
    template_name = "clients/client_investigation_list.html"
    context_object_name = "investigations"

    def get_queryset(self):
        client = get_object_or_404(Client, pk=self.kwargs['pk'])
        return client.client_investigations.all().order_by('investigation_type__name', '-date_done')


def test_view(request):
    from django.http import HttpResponse
    transfusion = Transfusion.objects.filter(admission__client__id=1).order_by('-date_of_transfusion')
    records = []
    for t in transfusion:
        records.append(f"Transfusion on {t.date_of_transfusion} - {t.admission.client.full_name}")
    return HttpResponse("Transfusion records: ".join(records))
