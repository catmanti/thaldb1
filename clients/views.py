from django.views.generic.edit import FormView
from django.views.generic import ListView
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .form import ClientForm
from .models import Client


class ClientFormView(FormView):
    template_name = "clients/client_form.html"
    form_class = ClientForm
    success_url = reverse_lazy("clients:client-list")

    def form_valid(self, form):
        # Save the Client record
        form.save()
        return super().form_valid(form)


# Need login required mixin for production
class ClientListView(LoginRequiredMixin, ListView):
    model = Client
    template_name = "clients/client_list.html"
    context_object_name = "clients"

    def get_queryset(self):
        return Client.objects.all().order_by("full_name")


class ClientUpdateView(UpdateView):
    model = Client
    form_class = ClientForm
    template_name = "clients/client_form.html"
    success_url = reverse_lazy("clients:client-list")
