from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = [
        "email",
        "username",
        "thalassemia_unit",
        "is_staff",
    ]
    list_filter = ["is_staff", "is_superuser", "is_active", "thalassemia_unit", "groups"]
    fieldsets = UserAdmin.fieldsets + ((None, {"fields": ("thalassemia_unit",)}),)
    add_fieldsets = UserAdmin.add_fieldsets + ((None, {"fields": ("thalassemia_unit",)}),)


admin.site.register(CustomUser, CustomUserAdmin)
