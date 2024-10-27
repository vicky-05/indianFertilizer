# Generated by Django 4.2 on 2024-10-26 08:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("shop", "0006_category_image_alter_product_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="category",
            name="image",
            field=models.ImageField(
                default="product_images/default_product.jpg",
                upload_to="category_images/<function getFilename at 0x777f4fd1f9c0>",
            ),
        ),
        migrations.AlterField(
            model_name="product",
            name="image",
            field=models.ImageField(
                default="product_images/default_product.jpg",
                upload_to="product_images/<function getFilename at 0x777f4fd1f9c0>",
            ),
        ),
    ]
