# Generated by Django 4.2 on 2024-01-29 10:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_productcollection_group_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='productcollection',
            name='brand_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
