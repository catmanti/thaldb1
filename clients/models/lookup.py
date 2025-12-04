from django.db import models


class Choice(models.Model):
    """
    Generic choice model for various categorical fields.

        category:
            The category of the choice (e.g., 'clinic_type', 'marital_status', etc.)
        name:
            The name/value of the choice.
    """

    CATEGORY_CHOICES = [
        ("clinic_type", "Clinic Type"),
        ("marital_status", "Marital Status"),
        ("current_status", "Current Status"),
        ("complication_status", "Complication Status"),
        ("vaccine_name", "Vaccine Name"),
        ("special_blood_type", "Special Blood Type"),
        ("growth", "Growth"),
    ]
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name}"


class Province(models.Model):
    """
    Store Provinces.
    """

    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]


class District(models.Model):
    """
    Store Districts.
    """

    name = models.CharField(max_length=100, unique=True)
    province = models.ForeignKey(Province, on_delete=models.CASCADE, related_name="districts")

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]


class DS_Division(models.Model):
    """
    Store DS Divisions.
    """

    name = models.CharField(max_length=100, unique=True)
    district = models.ForeignKey(District, on_delete=models.CASCADE, related_name="ds_divisions")

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class ThalassemiaUnit(models.Model):
    """
    Store Thalassaemia units.
    """

    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    ds_division = models.ForeignKey(DS_Division, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.name


class DiagnosisType(models.Model):
    """
    DIAGNOSIS TYPES.
    """

    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    icd_code = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]
