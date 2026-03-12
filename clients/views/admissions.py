from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView

from ..form import AdmissionForm
from ..models.client import Client
from ..models.management import Admission
from .mixins import AuthenticatedPermissionRequiredMixin, UnitScopedMixin


class AdmissionListView(
    LoginRequiredMixin, AuthenticatedPermissionRequiredMixin, UnitScopedMixin, ListView
):
    permission_required = "clients.view_admission"
    model = Admission
    template_name = "clients/client_admission_list.html"
    context_object_name = "admissions"

    def get_queryset(self):
        allowed_clients = self.scope_client_queryset(Client.objects.all()).values_list(
            "id", flat=True
        )
        queryset = Admission.objects.filter(
            client_id=self.kwargs["pk"], client_id__in=allowed_clients
        ).order_by("-date_of_admission")
        show_all = self.request.GET.get("all") == "1"
        if show_all:
            return queryset
        return queryset[:4]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["client_id"] = self.kwargs["pk"]
        context["show_all"] = self.request.GET.get("all") == "1"
        return context


class AdmissionCreateView(
    LoginRequiredMixin,
    AuthenticatedPermissionRequiredMixin,
    UnitScopedMixin,
    CreateView,
):
    permission_required = "clients.add_admission"
    model = Admission
    form_class = AdmissionForm
    template_name = "clients/client_admission_form.html"

    def dispatch(self, request, *args, **kwargs):
        self.client_obj = get_object_or_404(
            self.scope_client_queryset(Client.objects.all()), pk=self.kwargs["pk"]
        )
        return super().dispatch(request, *args, **kwargs)

    def get_initial(self):
        initial = super().get_initial()
        initial["client"] = self.client_obj
        return initial

    def form_valid(self, form):
        form.instance.client_id = self.client_obj.id
        return super().form_valid(form)


class AdmissionUpdateView(
    LoginRequiredMixin,
    AuthenticatedPermissionRequiredMixin,
    UnitScopedMixin,
    UpdateView,
):
    permission_required = "clients.change_admission"
    model = Admission
    form_class = AdmissionForm
    template_name = "clients/client_admission_form.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        if self._is_superuser():
            return queryset
        user_unit_id = self._user_unit_id()
        if not user_unit_id:
            return queryset.none()
        return queryset.filter(
            client__care_links__unit_id=user_unit_id, client__care_links__is_active=True
        ).distinct()

    def get_success_url(self):
        client_id = self.object.client.id
        return reverse_lazy("clients:client-detail", kwargs={"pk": client_id})
