## Basic Data

Project Start Date 2025-10-20 9:00 AM


## TODO

Fill the Client's ThalassemiaUnit automatically using userID. The user should have a ThalassemiaUnit.
He should be able to edit only his ThalassemiaUnit data.

The dates like date_first_transfused, diagnosis_date, iron_chelation_started_date,  blood_transfusion_start_date
should be able to calculated from approximate age.  Add a TextBox near it in the form.

Change the ThalassemiaUnit to thalassemia_unit

## In Production:
make sure in manage.py to change 'prod':
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "thallk.settings.prod")

On your droplet:

In your Gunicorn systemd service file (/etc/systemd/system/gunicorn.service),
find the Environment= line or ExecStart and add:

Environment="DJANGO_SETTINGS_MODULE=thallk.settings.prod"


Then restart:

sudo systemctl daemon-reload
sudo systemctl restart gunicorn

## Test only a One test:

uv run manage.py test clients.tests.FamilyMemberOnDeleteTest.test_diagnosis_set_null_when_deleted

- Below will run all the tests in that test class:
uv run manage.py test clients.tests.FamilyMemberOnDeleteTest

- To display all the test names:
uv run manage.py test clients --pattern="tests.py" -v 2

## TODO
Add HB_level_to_be_kept in both client and Transfution (alrady added) models. Then programally add it to Transfution
model from client model.
Add same for:
    Amount_of_blood;
    Special Type of Bood;
