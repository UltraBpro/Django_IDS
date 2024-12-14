# Generated by Django 4.2.13 on 2024-12-03 05:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('IDSWeb', '0003_alert_ip_address'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('pattern', models.TextField(help_text='Regular expression pattern to match')),
                ('attack_type', models.CharField(max_length=100)),
                ('severity', models.CharField(choices=[('High', 'High'), ('Medium', 'Medium'), ('Low', 'Low')], max_length=20)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]