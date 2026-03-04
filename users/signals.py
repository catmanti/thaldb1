from django.contrib.auth.models import Group, Permission
from django.db.models.signals import post_migrate
from django.dispatch import receiver

from .roles import ROLE_PERMISSIONS


@receiver(post_migrate)
def sync_role_groups(sender, **kwargs):
    for role_name, permission_names in ROLE_PERMISSIONS.items():
        group, _ = Group.objects.get_or_create(name=role_name)
        permissions = []
        for permission_name in permission_names:
            app_label, codename = permission_name.split(".", maxsplit=1)
            permission = Permission.objects.filter(content_type__app_label=app_label, codename=codename).first()
            if permission:
                permissions.append(permission)
        group.permissions.set(permissions)
