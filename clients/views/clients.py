from django.http import Http404
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import DetailView, ListView
from django.views.generic.edit import FormView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

from ..form import ClientForm
from ..models.client import Client, ClientCareUnit
from ..models.management import Transfusion
from .mixins import AuthenticatedPermissionRequiredMixin, UnitScopedMixin


class ClientFormView(
    LoginRequiredMixin, AuthenticatedPermissionRequiredMixin, UnitScopedMixin, FormView
):
    """Form view for creating a new client."""

    permission_required = "clients.add_client"
    template_name = "clients/client_form.html"
    form_class = ClientForm
    success_url = reverse_lazy("clients:client-list")

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        if "primary_unit" in form.fields:
            form.fields["primary_unit"].queryset = self.scope_unit_queryset(
                form.fields["primary_unit"].queryset
            )
            if not self._is_superuser() and self._user_unit_id():
                form.fields["primary_unit"].initial = self._user_unit_id()
        return form

    def form_valid(self, form):
        client = form.save()
        if not self._is_superuser():
            user_unit_id = self._user_unit_id()
            if not user_unit_id:
                raise Http404("No unit assigned to current user.")
            primary_unit_id = user_unit_id
        else:
            primary_unit = form.cleaned_data.get("primary_unit")
            if not primary_unit:
                form.add_error("primary_unit", "Primary unit is required.")
                return self.form_invalid(form)
            primary_unit_id = primary_unit.id

        ClientCareUnit.objects.create(
            client=client,
            unit_id=primary_unit_id,
            role=ClientCareUnit.Role.PRIMARY,
            start_date=timezone.localdate(),
            is_active=True,
        )
        return super().form_valid(form)


class ClientListView(
    LoginRequiredMixin, AuthenticatedPermissionRequiredMixin, UnitScopedMixin, ListView
):
    permission_required = "clients.view_client"
    model = Client
    template_name = "clients/client_list.html"
    context_object_name = "clients"

    def get_queryset(self):
        queryset = Client.objects.all().order_by("full_name")
        return self.scope_client_queryset(queryset)


class ClientUpdateView(
    LoginRequiredMixin,
    AuthenticatedPermissionRequiredMixin,
    UnitScopedMixin,
    UpdateView,
):
    permission_required = "clients.change_client"
    model = Client
    form_class = ClientForm
    template_name = "clients/client_form.html"
    success_url = reverse_lazy("clients:client-list")

    def get_queryset(self):
        queryset = super().get_queryset()
        return self.scope_client_queryset(queryset)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        if "primary_unit" in form.fields:
            form.fields.pop("primary_unit")
        return form


class ClientDetailView(
    LoginRequiredMixin,
    AuthenticatedPermissionRequiredMixin,
    UnitScopedMixin,
    DetailView,
):
    permission_required = "clients.view_client"
    model = Client

    def get_queryset(self):
        queryset = super().get_queryset()
        return self.scope_client_queryset(queryset)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        client = self.object
        context["admissions"] = client.client_admissions.all().order_by(
            "-date_of_admission"
        )[:4]
        context["transfusions"] = Transfusion.objects.filter(
            admission__client__id=client.id
        ).order_by("-date_of_transfusion")[:4]
        context["investigations"] = client.client_investigations.all().order_by(
            "investigation_type__name", "-date_done"
        )[:4]
        return context
