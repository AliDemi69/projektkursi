# Generated by Django 5.0.4 on 2024-05-01 15:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0002_order_status_order_total'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='discount',
            field=models.IntegerField(null=True),
        ),
    ]
