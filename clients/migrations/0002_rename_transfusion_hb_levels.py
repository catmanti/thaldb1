from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("clients", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="transfusion",
            old_name="HB_level_to_be_kept",
            new_name="pre_HB_level",
        ),
        migrations.RenameField(
            model_name="transfusion",
            old_name="HB_level",
            new_name="post_HB_level",
        ),
    ]
