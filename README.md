## Basic Data

Project Start Date 2025-10-20 9:00 AM


## TODO

Fill the Client's ThalassemiaUnit automatically using userID. The user should have a ThalassemiaUnit.
He should be able to edit only his ThalassemiaUnit data.

The dates like date_first_transfused, diagnosis_date, iron_chelation_started_date,  blood_transfusion_start_date
should be able to calculated from approximate age.  Add a TextBox near it in the form.

On your droplet:

In your Gunicorn systemd service file (/etc/systemd/system/gunicorn.service),
find the Environment= line or ExecStart and add:

Environment="DJANGO_SETTINGS_MODULE=thallk.settings.prod"


Then restart:

sudo systemctl daemon-reload
sudo systemctl restart gunicorn
