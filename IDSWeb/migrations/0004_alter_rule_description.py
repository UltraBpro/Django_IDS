# Generated by Django 5.1.1 on 2024-10-27 02:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('IDSWeb', '0003_rule'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rule',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]
