from django import forms
from .models.client import Client
from .models.management import Admission
from .models.lookup import ThalassemiaUnit


class ClientForm(forms.ModelForm):
    primary_unit = forms.ModelChoiceField(
        queryset=ThalassemiaUnit.objects.all(),
        required=False,
        help_text="Required when creating a new client.",
    )

    class Meta:
        model = Client
        fields = "__all__"
        exclude = ["photo", "care_units"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk and self.instance.primary_care_unit:
            self.fields["primary_unit"].initial = self.instance.primary_care_unit

    def clean(self):
        cleaned_data = super().clean()
        if not self.instance.pk and not cleaned_data.get("primary_unit"):
            self.add_error("primary_unit", "Primary unit is required.")
        return cleaned_data


# class AdmissionForm(forms.ModelForm):
#     class Meta:
#         model = Admission
#         fields = "__all__"


class AdmissionForm(forms.ModelForm):
    date_of_admission = forms.DateField(
        input_formats=["%Y-%m-%d"],
        widget=forms.DateInput(
            format="%Y-%m-%d",
            attrs={
                "type": "date",
                "class": "input input-bordered w-full",
            },
        ),
    )

    date_of_discharge = forms.DateField(
        required=False,
        input_formats=["%Y-%m-%d"],
        widget=forms.DateInput(
            format="%Y-%m-%d",
            attrs={
                "type": "date",
                "class": "input input-bordered w-full",
            },
        ),
    )

    class Meta:
        model = Admission
        fields = ["client", "date_of_admission", "date_of_discharge", "reason_for_admission"]

    # disable client field editing showing only the client name
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # disable editing
        self.fields["client"].disabled = True

        # apply CSS
        self.fields["client"].widget.attrs.update({"class": "input input-bordered w-full"})

        # widgets = {
        #     "reason_for_admission": forms.Textarea(attrs={"class": "textarea textarea-bordered w-full", "rows": 3}),
        # }
