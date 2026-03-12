from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.exceptions import PermissionDenied


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
        return queryset.filter(
            care_links__unit_id=user_unit_id, care_links__is_active=True
        ).distinct()

    def scope_unit_queryset(self, queryset):
        if self._is_superuser():
            return queryset
        user_unit_id = self._user_unit_id()
        if not user_unit_id:
            return queryset.none()
        return queryset.filter(id=user_unit_id)


class AuthenticatedPermissionRequiredMixin(PermissionRequiredMixin):
    """Redirect anonymous users to login.

    but return 403 for authenticated users lacking required permissions.
    """

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            raise PermissionDenied
        return super().handle_no_permission()
