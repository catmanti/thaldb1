from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views.generic import ListView

from ..models.client import Client
from ..models.management import Transfusion
from .mixins import AuthenticatedPermissionRequiredMixin, UnitScopedMixin


class TransfusionListView(
    LoginRequiredMixin, AuthenticatedPermissionRequiredMixin, UnitScopedMixin, ListView
):
    permission_required = "clients.view_transfusion"
    model = Client
    template_name = "clients/client_transfusion_list.html"
    context_object_name = "transfusions"

    def get_queryset(self):
        client = get_object_or_404(
            self.scope_client_queryset(Client.objects.all()), pk=self.kwargs["pk"]
        )
        return Transfusion.objects.filter(admission__client__id=client.id).order_by(
            "-date_of_transfusion"
        )
