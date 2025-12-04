from django import forms
from .models.client import Client


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = "__all__"
        exclude = ["photo"]
