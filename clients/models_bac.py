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


class DrugName(models.Model):
    """
    Drug names.
    """

    name = models.CharField(max_length=100, unique=True)
    dose = models.CharField(max_length=50, blank=True, null=True)
    regimen = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]


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


class ComplicationType(models.Model):
    """COMPLICATIONS TYPES like DM, HYPOTHYROIDISM etc."""

    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class InvestigationType(models.Model):
    """Represents a type of investigation, e.g., FBC, LFT."""

    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    unit = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.name


# -------------------------------------------------------------------
#                      MAIN CLIENT MODEL
# -------------------------------------------------------------------
class Client(models.Model):
    """Basic demographic and registration details."""

    GENDER_CHOICES = [
        ("M", "Male"),
        ("F", "Female"),
    ]

    BLOOD_GROUP_CHOICES = [
        ("A+", "A+"),
        ("A-", "A-"),
        ("B+", "B+"),
        ("B-", "B-"),
        ("AB+", "AB+"),
        ("AB-", "AB-"),
        ("O+", "O+"),
        ("O-", "O-"),
    ]

    ETHNICITY_CHOICES = [
        ("Sinhalese", "Sinhalese"),
        ("Tamil", "Tamil"),
        ("SriLankanMoor", "Sri Lankan Moor"),
        ("Burger", "Burger"),
        ("Other", "Other"),
    ]
    # --- Demographics ---
    full_name = models.CharField(max_length=150)
    common_name = models.CharField(max_length=100, blank=True, null=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    ethnicity = models.CharField(max_length=100, choices=ETHNICITY_CHOICES, default="Sinhalese", blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUP_CHOICES, blank=True, null=True)
    nic_number = models.CharField(max_length=15, blank=True, null=True, unique=True)

    # --- Registration & clinical ---
    registration_number = models.CharField(max_length=50, unique=True)
    date_of_registration = models.DateField(blank=True, null=True)
    unit = models.ForeignKey(ThalassemiaUnit, on_delete=models.SET_NULL, blank=True, null=True, related_name="clients")
    diagnosis = models.ForeignKey(
        DiagnosisType, on_delete=models.SET_NULL, blank=True, null=True, related_name="clients"
    )

    # --- Social details ---
    marital_status = models.ForeignKey(
        "Choice",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={"category": "marital_status"},
        related_name="clients_marital_status",
    )
    occupation = models.CharField(max_length=100, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    ds_division = models.ForeignKey(DS_Division, on_delete=models.SET_NULL, blank=True, null=True)
    contact_number = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    photo = models.ImageField(upload_to="client_photos/", blank=True, null=True)
    guardian_name_1 = models.CharField(max_length=100, blank=True, null=True)
    guardian_name_2 = models.CharField(max_length=100, blank=True, null=True)
    guardian_contact_number_1 = models.CharField(max_length=20, blank=True, null=True)
    guardian_contact_number_2 = models.CharField(max_length=20, blank=True, null=True)
    # --- TODO DELETE LATER? ---
    # diagnosis = models.ForeignKey(
    #     DiagnosisType, on_delete=models.SET_NULL, null=True, blank=True, related_name="clients_diagnosis"
    # )
    diagnosis_date = models.DateField(blank=True, null=True)
    HB_level_at_diagnosis = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True)
    date_first_transfused = models.DateField(blank=True, null=True)
    date_iron_chelation_started = models.DateField(blank=True, null=True)
    transfusion_regimen = models.CharField(max_length=200, blank=True, null=True)
    allergic_history = models.TextField(blank=True, null=True)
    special_note = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.registration_number} : {self.full_name}"

    class Meta:
        ordering = ["full_name"]


# -------------------------------------------------------------------
#                      DEATH RECORD
# -------------------------------------------------------------------
class ClientDeath(models.Model):
    """Stores client death details."""

    client = models.OneToOneField(Client, on_delete=models.CASCADE, related_name="death_record")
    date_of_death = models.DateField()
    cause_of_death = models.TextField(blank=True, null=True)
    postmortem_findings = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Death record: {self.client.full_name}"


# -------------------------------------------------------------------
#                      TRANSFER RECORD
# -------------------------------------------------------------------
class ClientTransfer(models.Model):
    """Records client transfer details."""

    client = models.OneToOneField(Client, on_delete=models.CASCADE, related_name="transfer_record")
    transferred_unit = models.ForeignKey(
        ThalassemiaUnit,
        on_delete=models.SET_NULL,
        null=True,
        related_name="transferred_clients",
    )
    date_of_transfer = models.DateField(blank=True, null=True)
    reason = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.client.full_name} transferred to {self.transferred_unit}"


class FamilyMember(models.Model):
    """FAMILY MEMBERS"""

    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="family_members")
    relationship = models.CharField(
        max_length=50,
        choices=[
            ("Father", "Father"),
            ("Mother", "Mother"),
            ("Sibling", "Sibling"),
            ("Other", "Other"),
        ],
        default="Other",
    )
    name = models.CharField(max_length=100)
    birth_day = models.DateField(blank=True, null=True)
    diagnosis = models.ForeignKey(DiagnosisType, on_delete=models.SET_NULL, blank=True, null=True)
    pt_id = models.CharField(max_length=20, blank=True, null=True)  # if the family member is also a client
    is_carrier = models.BooleanField(default=False)
    contact_number = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.relationship})"


class Drug(models.Model):
    """DRUGS"""

    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="drugs")
    date_prescribed = models.DateField()
    drug_name = models.ForeignKey(DrugName, on_delete=models.SET_NULL, null=True)
    dose = models.CharField(max_length=50)
    regimen = models.CharField(max_length=100)
    duration = models.CharField(max_length=50)
    indication = models.CharField(max_length=200, blank=True, null=True)
    prescribed_by = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.drug_name} - {self.client.full_name}"


class Complication(models.Model):
    """CLIENT'S COMPLICATIONS"""

    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="client_complications")
    complication = models.ForeignKey(ComplicationType, on_delete=models.SET_NULL, null=True)

    detected_date = models.DateField()
    status = models.ForeignKey(
        "Choice",
        on_delete=models.SET_NULL,
        null=True,
        limit_choices_to={"category": "complication_status"},
    )

    remarks = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.complication} - {self.client.full_name}"


class Vaccination(models.Model):
    """VACCINATIONS"""

    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="vaccinations")
    vaccine_name = models.ForeignKey(
        "Choice",
        on_delete=models.SET_NULL,
        null=True,
        limit_choices_to={"category": "vaccine_name"},
    )

    date_given = models.DateField()
    next_dose_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.vaccine_name} ({self.client.full_name})"


class Admission(models.Model):
    """HOSPITAL ADMISSIONS"""

    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="client_admissions")
    date_of_admission = models.DateField()
    reason_for_admission = models.TextField(default="Blood Transfusion")
    date_of_discharge = models.DateField(blank=True, null=True)
    outcome = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return f"Admission on {self.date_of_admission} - {self.client.full_name}"


class Transfusion(models.Model):
    """BLOOD TRANSFUSIONS"""

    # Client of the transfusion is the client of the admission
    admission = models.ForeignKey(Admission, on_delete=models.CASCADE, related_name="blood_transfusions")
    date_of_transfusion = models.DateField()
    HB_level_to_be_kept = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True, default=9.0)
    HB_level = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True)
    WBC_count = models.DecimalField(max_digits=8, decimal_places=1, blank=True, null=True)
    platelet_count = models.DecimalField(max_digits=8, decimal_places=1, blank=True, null=True)
    amount_of_blood = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    special_type = models.ForeignKey(
        "Choice",
        on_delete=models.SET_NULL,
        null=True,
        limit_choices_to={"category": "special_blood_type"},
    )
    next_date_given = models.DateField(blank=True, null=True)
    reaction = models.CharField(max_length=200, blank=True, null=True, default="None")
    checked_by = models.CharField(max_length=100, blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Transfusion on {self.date_of_transfusion} - {self.admission.client.full_name}"


class ClinicVisit(models.Model):
    """CLINIC VISITS"""

    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="clinic_visits")
    date_visit = models.DateField()
    problem = models.TextField(blank=True, null=True)
    clinic_type = models.ForeignKey(
        "Choice",
        on_delete=models.SET_NULL,
        null=True,
        limit_choices_to={"category": "clinic_type"},
    )
    action = models.TextField(blank=True, null=True)
    referral = models.CharField(max_length=200, blank=True, null=True)
    next_visit_date = models.DateField(blank=True, null=True)
    doctor_name = models.CharField(max_length=100, blank=True, null=True)
    follow_up_needed = models.BooleanField(default=False)

    def __str__(self):
        return f"Clinic visit - {self.client.full_name} ({self.date_visit})"


class Investigation(models.Model):
    """INVESTIGATIONS"""

    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="client_investigations")
    date_done = models.DateField()
    investigation_type = models.ForeignKey(InvestigationType, on_delete=models.SET_NULL, blank=True, null=True)
    value = models.CharField(max_length=100, blank=True, null=True)
    unit = models.CharField(max_length=20, blank=True, null=True)
    laboratory_name = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.investigation_type} - {self.client.full_name}"


class GrowthRecord(models.Model):
    """GROWTH RECORDS"""

    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="growth_records")
    date_measured = models.DateField()
    type = models.ForeignKey("Choice", on_delete=models.SET_NULL, null=True, limit_choices_to={"category": "growth"})
    value = models.DecimalField(max_digits=6, decimal_places=2)
    percentile = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return f"{self.type} - {self.value} ({self.client.full_name})"
