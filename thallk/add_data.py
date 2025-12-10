from clients.models.lookup import (
    Choice, Province, District, DS_Division,
    ThalassemiaUnit, DiagnosisType
)

# ------------------------------
# Choices
# ------------------------------
choice_data = [
    ("clinic_type", "Endocrine Clinic"),
    ("clinic_type", "STD Clinic"),
    ("clinic_type", "Obstetrics Clinic"),
    ("marital_status", "Single"),
    ("marital_status", "Married"),
    ("current_status", "Alive"),
    ("current_status", "Transferred"),
    ("current_status", "Deceased"),
    ("complication_status", "Diabetes Mellitus"),
    ("complication_status", "Hypothyroidism"),
    ("complication_status", "CKD"),
    ("vaccine_name", "Hepatitis B"),
    ("vaccine_name", "HIB"),
    ("special_blood_type", "Washed Blood"),
    ("special_blood_type", "Irradiated Blood"),
    ("growth", "Normal Growth"),
    ("growth", "Poor Growth"),
]

for category, name in choice_data:
    Choice.objects.get_or_create(category=category, name=name)

print("Choices added.")

# ------------------------------
# Provinces, Districts, Divisions
# ------------------------------
province = Province.objects.get_or_create(name="North Western Province")[0]

district_names = ["Kurunegala", "Puttalam"]
district_objects = []

for d in district_names:
    district, created = District.objects.get_or_create(name=d, province=province)
    district_objects.append(district)

print("Districts added.")

ds_data = {
    "Kurunegala": ["Kurunegala", "Mawathagama", "Polpithigama", "Wariyapola", "Nikaweratiya"],
    "Puttalam": ["Puttalam", "Chilaw", "Wennappuwa", "Mundalama", "Anamaduwa"],
}

for dist in district_objects:
    for ds_name in ds_data.get(dist.name, []):
        DS_Division.objects.get_or_create(name=ds_name, district=dist)

print("DS Divisions added.")

# ------------------------------
# Thalassaemia Units
# ------------------------------
units = [
    ("National Thalassaemia Centre", "Kurunegala district unit", "Kurunegala"),
    ("Ragama Thalassaemia Centre", "Ragama hospital unit", "Gampaha"),
    ("Anunradhapura Treatment Unit", "Anuradhapura district unit", "Anuradhapura"),
]

for name, desc, ds_name in units:
    ds = DS_Division.objects.get(name=ds_name)
    ThalassemiaUnit.objects.get_or_create(
        name=name,
        defaults={"description": desc, "ds_division": ds},
    )

print("Thalassaemia units added.")

# ------------------------------
# Diagnosis Types
# ------------------------------
diagnosis_list = [
    ("Beta Thalassemia Major", "Severe form of thalassaemia", "D56.1"),
    ("Beta Thalassemia Trait", "Carrier state", "D56.3"),
    ("HbE Beta Thalassemia", "Compound heterozygous condition", "D56.4"),
]

for name, desc, icd in diagnosis_list:
    DiagnosisType.objects.get_or_create(
        name=name,
        defaults={"description": desc, "icd_code": icd},
    )

print("Diagnosis types added.")

print("All mock data inserted successfully.")
