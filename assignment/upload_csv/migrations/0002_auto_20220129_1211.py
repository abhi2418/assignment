# Generated by Django 2.2.12 on 2022-01-29 12:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('upload_csv', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='csv',
            old_name='timestamp',
            new_name='date',
        ),
        migrations.AlterField(
            model_name='csv',
            name='objects_detected',
            field=models.CharField(max_length=250),
        ),
    ]
