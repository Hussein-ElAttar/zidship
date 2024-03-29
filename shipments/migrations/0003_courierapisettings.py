# Generated by Django 4.0.1 on 2022-01-26 20:47

from django.db import migrations, models
import django.db.models.deletion
import shipments.enums


class Migration(migrations.Migration):

    dependencies = [
        ('shipments', '0002_rename_at_courier_description_shipmentstatus_description_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='CourierApiSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client_id', models.CharField(max_length=255, null=True)),
                ('client_secret', models.CharField(max_length=255, null=True)),
                ('access_token', models.CharField(max_length=255, null=True)),
                ('refresh_token', models.CharField(max_length=255, null=True)),
                ('token_expiration_date', models.DateTimeField(null=True)),
                ('base_url', models.CharField(max_length=255, null=True)),
                ('api_url', models.CharField(max_length=255)),
                ('token_path', models.CharField(default='oauth/token', max_length=255, null=True)),
                ('auth_flow', models.CharField(blank=True, max_length=255, null=True)),
                ('scope', models.CharField(blank=True, max_length=255, null=True)),
                ('env', models.CharField(choices=[('SANDBOX', 'sandbox'), ('LIVE', 'live')], default=shipments.enums.CourierEnvironmentEnum['SANDBOX'], max_length=30)),
                ('courier', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_courier', to='shipments.courier')),
            ],
        ),
    ]
