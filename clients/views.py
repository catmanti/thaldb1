from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, FormView, UpdateView

from .form import AdmissionForm, ClientForm
from .models.client import Client
from .models.management import Admission, Transfusion


class UnitScopedMixin:
    """Scope querysets to the authenticated user's assigned thalassemia unit."""

    def _is_superuser(self):
        return self.request.user.is_superuser

    def _user_unit_id(self):
        return getattr(self.request.user, "thalassemia_unit_id", None)

    def scope_client_queryset(self, queryset):
        if self._is_superuser():
            return queryset

        user_unit_id = self._user_unit_id()
        if not user_unit_id:
            return queryset.none()
        return queryset.filter(unit_id=user_unit_id)

    def scope_unit_queryset(self, queryset):
        if self._is_superuser():
            return queryset
        user_unit_id = self._user_unit_id()
        if not user_unit_id:
            return queryset.none()
        return queryset.filter(id=user_unit_id)


class AuthenticatedPermissionRequiredMixin(PermissionRequiredMixin):
    """
    Redirect anonymous users to login, but return 403 for authenticated users
    lacking required permissions.
    """

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            raise PermissionDenied
        return super().handle_no_permission()


class ClientFormView(LoginRequiredMixin, AuthenticatedPermissionRequiredMixin, UnitScopedMixin, FormView):
    permission_required = "clients.add_client"
    template_name = "clients/client_form.html"
    form_class = ClientForm
    success_url = reverse_lazy("clients:client-list")

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["unit"].queryset = self.scope_unit_queryset(form.fields["unit"].queryset)
        if not self._is_superuser() and self._user_unit_id():
            form.fields["unit"].initial = self._user_unit_id()
        return form

    def form_valid(self, form):
        if not self._is_superuser():
            user_unit_id = self._user_unit_id()
            if not user_unit_id:
                raise Http404("No unit assigned to current user.")
            form.instance.unit_id = user_unit_id
        form.save()
        return super().form_valid(form)


class ClientListView(LoginRequiredMixin, AuthenticatedPermissionRequiredMixin, UnitScopedMixin, ListView):
    permission_required = "clients.view_client"
    model = Client
    template_name = "clients/client_list.html"
    context_object_name = "clients"

    def get_queryset(self):
        queryset = Client.objects.all().order_by("full_name")
        return self.scope_client_queryset(queryset)


class ClientUpdateView(LoginRequiredMixin, AuthenticatedPermissionRequiredMixin, UnitScopedMixin, UpdateView):
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
        form.fields["unit"].queryset = self.scope_unit_queryset(form.fields["unit"].queryset)
        return form


class ClientDetailView(LoginRequiredMixin, AuthenticatedPermissionRequiredMixin, UnitScopedMixin, DetailView):
    permission_required = "clients.view_client"
    model = Client

    def get_queryset(self):
        queryset = super().get_queryset()
        return self.scope_client_queryset(queryset)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        client = self.object
        context["admissions"] = client.client_admissions.all().order_by("-date_of_admission")[:4]
        context["transfusions"] = Transfusion.objects.filter(admission__client__id=client.id).order_by("-date_of_transfusion")[:4]
        context["investigations"] = client.client_investigations.all().order_by("investigation_type__name", "-date_done")[:4]
        return context


class AdmissionListView(LoginRequiredMixin, AuthenticatedPermissionRequiredMixin, UnitScopedMixin, ListView):
    permission_required = "clients.view_admission"
    model = Admission
    template_name = "clients/client_admission_list.html"
    context_object_name = "admissions"

    def get_queryset(self):
        allowed_clients = self.scope_client_queryset(Client.objects.all()).values_list("id", flat=True)
        queryset = Admission.objects.filter(client_id=self.kwargs["pk"], client_id__in=allowed_clients).order_by(
            "-date_of_admission"
        )
        show_all = self.request.GET.get("all") == "1"
        if show_all:
            return queryset
        return queryset[:4]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["client_id"] = self.kwargs["pk"]
        context["show_all"] = self.request.GET.get("all") == "1"
        return context


class AdmissionCreateView(LoginRequiredMixin, AuthenticatedPermissionRequiredMixin, UnitScopedMixin, CreateView):
    permission_required = "clients.add_admission"
    model = Admission
    form_class = AdmissionForm
    template_name = "clients/client_admission_form.html"

    def dispatch(self, request, *args, **kwargs):
        self.client_obj = get_object_or_404(self.scope_client_queryset(Client.objects.all()), pk=self.kwargs["pk"])
        return super().dispatch(request, *args, **kwargs)

    def get_initial(self):
        initial = super().get_initial()
        initial["client"] = self.client_obj
        return initial

    def form_valid(self, form):
        form.instance.client = self.client_obj
        return super().form_valid(form)


class AdmissionUpdateView(LoginRequiredMixin, AuthenticatedPermissionRequiredMixin, UnitScopedMixin, UpdateView):
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
        return queryset.filter(client__unit_id=user_unit_id)

    def get_success_url(self):
        client_id = self.object.client.id
        return reverse_lazy("clients:client-detail", kwargs={"pk": client_id})


class TransfusionListView(LoginRequiredMixin, AuthenticatedPermissionRequiredMixin, UnitScopedMixin, ListView):
    permission_required = "clients.view_transfusion"
    model = Client
    template_name = "clients/client_transfusion_list.html"
    context_object_name = "transfusions"

    def get_queryset(self):
        client = get_object_or_404(self.scope_client_queryset(Client.objects.all()), pk=self.kwargs["pk"])
        return Transfusion.objects.filter(admission__client__id=client.id).order_by("-date_of_transfusion")


class InvestigationListView(LoginRequiredMixin, AuthenticatedPermissionRequiredMixin, UnitScopedMixin, ListView):
    permission_required = "clients.view_investigation"
    model = Client
    template_name = "clients/client_investigation_list.html"
    context_object_name = "investigations"

    def get_queryset(self):
        client = get_object_or_404(self.scope_client_queryset(Client.objects.all()), pk=self.kwargs["pk"])
        return client.client_investigations.all().order_by("investigation_type__name", "-date_done")


def test_view(request):
    from django.http import HttpResponse

    transfusion = Transfusion.objects.filter(admission__client__id=1).order_by("-date_of_transfusion")
    records = []
    for transfusion_record in transfusion:
        records.append(
            f"Transfusion on {transfusion_record.date_of_transfusion} - {transfusion_record.admission.client.full_name}"
        )
    return HttpResponse("Transfusion records: ".join(records))
