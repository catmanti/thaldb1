from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views.generic import ListView

from ...models.client import Client
from ..mixins import AuthenticatedPermissionRequiredMixin, UnitScopedMixin


class InvestigationListView(
    LoginRequiredMixin, AuthenticatedPermissionRequiredMixin, UnitScopedMixin, ListView
):
    permission_required = "clients.view_investigation"
    model = Client
    template_name = "clients/client_investigation_list.html"
    context_object_name = "investigations"

    def get_queryset(self):
        client = get_object_or_404(
            self.scope_client_queryset(Client.objects.all()), pk=self.kwargs["pk"]
        )
        return client.client_investigations.all().order_by(
            "investigation_type__name", "-date_done"
        )
