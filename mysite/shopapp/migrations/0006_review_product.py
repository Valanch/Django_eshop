# Generated by Django 4.2 on 2023-06-01 06:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("shopapp", "0005_review"),
    ]

    operations = [
        migrations.AddField(
            model_name="review",
            name="product",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                to="shopapp.product",
            ),
            preserve_default=False,
        ),
    ]