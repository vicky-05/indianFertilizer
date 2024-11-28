# Generated by Django 4.2 on 2024-11-28 11:00

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authendicate', '0003_alter_user_profile_img'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='mobile_no',
            field=models.BigIntegerField(blank=True, default=1111111111, null=True, validators=[django.core.validators.MinValueValidator(1111111111), django.core.validators.MaxValueValidator(9999999999)]),
        ),
    ]
