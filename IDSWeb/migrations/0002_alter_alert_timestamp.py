# Generated by Django 4.2.13 on 2024-09-20 02:21

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('IDSWeb', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alert',
            name='timestamp',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]