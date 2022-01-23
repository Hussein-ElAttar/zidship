# Generated by Django 4.0.1 on 2022-01-23 02:10

from django.db import migrations, models
import django.db.models.deletion
import shipments.enums


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Courier',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='ShipmentMethods',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ShipmentStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('PENDING', 'pending'), ('CONFIRMED', 'confirmed'), ('IN_PROGRESS', 'in_progress'), ('DELIVERED', 'delivered'), ('CANCELED', 'canceled')], db_index=True, default=shipments.enums.ShipmentStatus['PENDING'], max_length=100)),
                ('source_id', models.CharField(max_length=200, null=True)),
                ('source_description', models.TextField(blank=True, null=True)),
                ('courier', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_courier', to='shipments.courier')),
            ],
        ),
        migrations.CreateModel(
            name='Shipment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tracking_id', models.CharField(max_length=200, null=True)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('weight', models.DecimalField(decimal_places=2, max_digits=6)),
                ('weight_unit', models.CharField(choices=[('CM', 'cm'), ('Inch', 'in')], default=shipments.enums.WeightUnits['KG'], max_length=15)),
                ('dimensions_unit', models.CharField(choices=[('CM', 'cm'), ('Inch', 'in')], default=shipments.enums.DimensionUnits['CM'], max_length=15)),
                ('sender_address', models.CharField(max_length=200)),
                ('sender_country', models.CharField(max_length=200)),
                ('sender_city', models.CharField(max_length=200)),
                ('sender_postal_code', models.CharField(max_length=200)),
                ('sender_phone_number', models.CharField(max_length=15)),
                ('receiver_address', models.CharField(max_length=200)),
                ('receiver_country', models.CharField(max_length=200)),
                ('receiver_city', models.CharField(max_length=200)),
                ('receiver_postal_code', models.CharField(max_length=15)),
                ('receiver_phone_number', models.CharField(max_length=15)),
                ('courier', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_courier', to='shipments.courier')),
                ('status', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_courier', to='shipments.shipmentstatus')),
            ],
        ),
    ]
