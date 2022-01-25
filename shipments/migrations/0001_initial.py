# Generated by Django 4.0.1 on 2022-01-25 00:24

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
            name='ShipmentStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('PROCCESSING', 'proccessing'), ('PENDING', 'pending'), ('CONFIRMED', 'confirmed'), ('IN_PROGRESS', 'in_progress'), ('DELIVERED', 'delivered'), ('PENDING_CANCELATION', 'pending-cancelation'), ('CANCELED', 'canceled')], db_index=True, default=shipments.enums.ShipmentStatusEnum['PENDING'], max_length=100)),
                ('at_courier_status', models.CharField(max_length=200, null=True)),
                ('at_courier_description', models.TextField(blank=True, null=True)),
                ('courier', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_courier', to='shipments.courier')),
            ],
            options={
                'unique_together': {('status', 'courier')},
            },
        ),
        migrations.CreateModel(
            name='ShipmentMethod',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
                ('courier', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_courier', to='shipments.courier')),
            ],
        ),
        migrations.CreateModel(
            name='Shipment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('tracking_id', models.CharField(max_length=200, null=True)),
                ('weight', models.DecimalField(decimal_places=2, max_digits=6)),
                ('weight_unit', models.CharField(choices=[('KG', 'kg'), ('Pound', 'lb')], default=shipments.enums.WeightUnitsEnum['KG'], max_length=15)),
                ('height', models.DecimalField(decimal_places=2, max_digits=6)),
                ('width', models.DecimalField(decimal_places=2, max_digits=6)),
                ('length', models.DecimalField(decimal_places=2, max_digits=6)),
                ('dimensions_unit', models.CharField(choices=[('CM', 'cm'), ('Inch', 'in')], default=shipments.enums.DimensionUnitsEnum['CM'], max_length=15)),
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
                ('pickup_date', models.DateTimeField(null=True)),
                ('estimated_delivery_date', models.DateTimeField(null=True)),
                ('courier', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_courier', to='shipments.courier')),
                ('shipment_method', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_courier', to='shipments.shipmentmethod')),
                ('status', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_courier', to='shipments.shipmentstatus')),
            ],
            options={
                'ordering': ['-created_at', '-updated_at'],
                'abstract': False,
            },
        ),
    ]
