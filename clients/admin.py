from django.contrib import admin
from .models.client import (
    Client,
    ClientDeath,
    ClientTransfer,
    FamilyMember,
)
from .models.drug import (
    DrugName,
    Drug
)
from .models.management import (
    Complication,
    Vaccination,
    ComplicationType,
    # VaccinationType,
    InvestigationType,
    Investigation,
    ClinicVisit,
    GrowthRecord,
    Admission,
    Transfusion,
)
from .models.lookup import (
    Province,
    District,
    DS_Division,
    ThalassemiaUnit,
    DiagnosisType,
    Choice
)

# ───────────────────────────────────────────────
# INLINE MODELS
# ───────────────────────────────────────────────


class FamilyMemberInline(admin.TabularInline):
    model = FamilyMember
    extra = 1


class DrugInline(admin.TabularInline):
    model = Drug
    extra = 1


class ComplicationInline(admin.TabularInline):
    model = Complication
    extra = 1


class VaccinationInline(admin.TabularInline):
    model = Vaccination
    extra = 1


# class TransfusionInline(admin.TabularInline):
#   model = Transfusion
#   extra = 1


class ClinicVisitInline(admin.TabularInline):
    model = ClinicVisit
    extra = 1


class InvestigationInline(admin.TabularInline):
    model = Investigation
    extra = 1


class GrowthRecordInline(admin.TabularInline):
    model = GrowthRecord
    extra = 1


class AdmissionInline(admin.TabularInline):
    model = Admission
    extra = 1


# ───────────────────────────────────────────────
# CLIENT ADMIN
# ───────────────────────────────────────────────


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = (
        "full_name",
        "common_name",
        "gender",
        "date_of_birth",
        "blood_group",
        "diagnosis",
        "date_of_registration",
    )
    search_fields = ("full_name", "common_name", "diagnosis", "contact_number")
    list_filter = ("gender", "blood_group", "diagnosis", "ethnicity")
    ordering = ("full_name",)
    date_hierarchy = "date_of_registration"

    # Attach all related inlines for editing on the same page
    inlines = [
        FamilyMemberInline,
        DrugInline,
        ComplicationInline,
        VaccinationInline,
        ClinicVisitInline,
        InvestigationInline,
        GrowthRecordInline,
    ]


# ───────────────────────────────────────────────
# REGISTER OTHER MODELS (for independent access)
# ───────────────────────────────────────────────


@admin.register(ClientDeath)
class ClientDeathAdmin(admin.ModelAdmin):
    list_display = ("client", "date_of_death", "cause_of_death")
    search_fields = ("client__full_name", "cause_of_death")


@admin.register(ClientTransfer)
class ClientTransferAdmin(admin.ModelAdmin):
    list_display = ("client", "date_of_transfer", "transferred_unit")
    search_fields = ("client__full_name", "transferred_unit__name")


@admin.register(Province)
class ProvinceAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    list_display = ("name", "province")
    list_filter = ("province",)
    search_fields = ("name",)


@admin.register(DS_Division)
class DS_DivisionAdmin(admin.ModelAdmin):
    list_display = ("name", "district")
    list_filter = ("district",)
    search_fields = ("name",)


@admin.register(FamilyMember)
class FamilyMemberAdmin(admin.ModelAdmin):
    list_display = ("client", "name", "relationship", "diagnosis")
    search_fields = ("name", "relationship")


@admin.register(Drug)
class DrugAdmin(admin.ModelAdmin):
    list_display = ("client", "date_prescribed", "drug_name", "dose", "duration")
    list_filter = ("drug_name",)
    search_fields = ("drug_name",)


@admin.register(Complication)
class ComplicationAdmin(admin.ModelAdmin):
    list_display = ("client", "complication", "detected_date")
    list_filter = ("complication",)
    search_fields = ("complication",)


@admin.register(Vaccination)
class VaccinationAdmin(admin.ModelAdmin):
    list_display = ("client", "vaccine_name", "date_given", "next_dose_date")
    list_filter = ("vaccine_name",)
    search_fields = ("vaccine_name",)


@admin.register(Transfusion)
class TransfusionAdmin(admin.ModelAdmin):
    list_display = ("get_client", "get_date_of_admission", "HB_level", "amount_of_blood", "next_date_given")
    list_filter = ("special_type",)
    date_hierarchy = "date_of_transfusion"

    def get_client(self, obj):
        return obj.admission.client

    def get_date_of_admission(self, obj):
        return obj.admission.date_of_admission

    get_client.short_description = "Client"
    get_date_of_admission.short_description = "Admission Date"


@admin.register(ClinicVisit)
class ClinicVisitAdmin(admin.ModelAdmin):
    list_display = (
        "client",
        "date_visit",
        "clinic_type",
        "referral",
        "next_visit_date",
    )
    list_filter = ("clinic_type",)
    date_hierarchy = "date_visit"


@admin.register(Investigation)
class InvestigationAdmin(admin.ModelAdmin):
    list_display = ("client", "date_done", "investigation_type", "value")
    list_filter = ("investigation_type",)
    search_fields = ("investigation_type",)


@admin.register(GrowthRecord)
class GrowthRecordAdmin(admin.ModelAdmin):
    list_display = ("client", "date_measured", "type", "value")
    list_filter = ("type",)
    date_hierarchy = "date_measured"


@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ("category", "name")
    list_filter = ("category",)
    search_fields = ("name",)


@admin.register(DiagnosisType)
class DiagnosisTypeAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(InvestigationType)
class InvestigationTypeAdmin(admin.ModelAdmin):
    list_display = ("name", "unit")
    search_fields = ("name",)


@admin.register(DrugName)
class DrugNameAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(ComplicationType)
class ComplicationTypeAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(ThalassemiaUnit)
class ThalassemiaUnitAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Admission)
class AdmissionAdmin(admin.ModelAdmin):
    list_display = ("client", "date_of_admission", "reason_for_admission", "date_of_discharge", "outcome")
    list_filter = ("outcome",)
    date_hierarchy = "date_of_admission"
    search_fields = ("client__full_name", "reason_for_admission", "outcome")
