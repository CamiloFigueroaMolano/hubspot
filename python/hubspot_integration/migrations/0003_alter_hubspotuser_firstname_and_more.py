# Generated by Django 5.0 on 2023-12-05 16:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hubspot_integration', '0002_remove_hubspotuser_first_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hubspotuser',
            name='firstname',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='hubspotuser',
            name='lastname',
            field=models.CharField(max_length=255),
        ),
    ]