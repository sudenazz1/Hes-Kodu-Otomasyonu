from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.RunSQL(open('home/sql/database.sql').read()),
    ]
