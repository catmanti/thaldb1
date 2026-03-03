from django import forms
from .models.client import Client
from .models.management import Admission


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = "__all__"
        exclude = ["photo"]


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
