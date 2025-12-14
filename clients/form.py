from django import forms
from .models.client import Client
from .models.management import Admission


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = "__all__"
        exclude = ["photo"]


class AdmissionForm(forms.ModelForm):
    class Meta:
        model = Admission
        fields = "__all__"
