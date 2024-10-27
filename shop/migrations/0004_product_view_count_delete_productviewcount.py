# Generated by Django 4.2 on 2024-10-26 07:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("shop", "0003_productviewcount"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="view_count",
            field=models.PositiveBigIntegerField(default=0),
        ),
        migrations.DeleteModel(
            name="ProductViewCount",
        ),
    ]
