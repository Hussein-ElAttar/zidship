import os
import random
import uuid

from django.contrib.auth.models import User
from django.core.management import call_command
from django.core.management.base import BaseCommand
from django_seed import Seed
from shipments.enums import CourierEnvironmentEnum, ShipmentStatusEnum
from shipments.models import (Courier, CourierApiSettings, Shipment,
                              ShipmentMethod, ShipmentStatus)


class Command(BaseCommand):

    def handle(self, *args, **options):
        seeder = Seed.seeder()
        has_data = False

        if not User.objects.exists():
            has_data = True
            self.stdout.write('Seeding initial data')
            user = User.objects.create_superuser(
                os.environ.get('DJANGO_SUPER_USER_NAME'),
                os.environ.get('DJANGO_SUPER_USER_EMAIL'),
                os.environ.get('DJANGO_SUPER_USER_PASSWORD')
            )

        if not Courier.objects.exists():
            has_data = True
            seeder.add_entity(Courier, 1, {'name': 'Fedex'})

        if not CourierApiSettings.objects.exists():
            has_data = True
            seeder.add_entity(CourierApiSettings, 1, {
                'client_id': os.environ.get('FEDEX_CLIENT_ID'),
                'client_secret': os.environ.get('FEDEX_CLIENT_SECRET'),
                'access_token': None,
                'refresh_token': None,
                'token_expiration_date': None,
                'base_url': None,
                'api_url': 'https://apis-sandbox.fedex.com',
                'token_path': 'oauth/token',
                'auth_flow': 'client_credentials',
                'env': CourierEnvironmentEnum.SANDBOX,
            })

        if not ShipmentMethod.objects.exists():
            has_data = True
            seeder.add_entity(ShipmentMethod, 1, {'name': 'Same day delivery'})
            seeder.add_entity(ShipmentMethod, 1, {'name': 'Within 7 Days'})

        if not ShipmentStatus.objects.exists():
            has_data = True
            seeder.add_entity(ShipmentStatus, 1, {'code':ShipmentStatusEnum.PROCCESSING, 'external_code': ShipmentStatusEnum.PROCCESSING })
            seeder.add_entity(ShipmentStatus, 1, {'code':ShipmentStatusEnum.PENDING, 'external_code': ShipmentStatusEnum.PENDING })
            seeder.add_entity(ShipmentStatus, 1, {'code':ShipmentStatusEnum.CONFIRMED, 'external_code': ShipmentStatusEnum.CONFIRMED })
            seeder.add_entity(ShipmentStatus, 1, {'code':ShipmentStatusEnum.IN_PROGRESS, 'external_code': ShipmentStatusEnum.IN_PROGRESS })
            seeder.add_entity(ShipmentStatus, 1, {'code':ShipmentStatusEnum.DELIVERED, 'external_code': ShipmentStatusEnum.DELIVERED })
            seeder.add_entity(ShipmentStatus, 1, {'code':ShipmentStatusEnum.PENDING_CANCELATION, 'external_code': ShipmentStatusEnum.PENDING_CANCELATION })
            seeder.add_entity(ShipmentStatus, 1, {'code':ShipmentStatusEnum.CANCELED, 'external_code': ShipmentStatusEnum.CANCELED })

        if not Shipment.objects.exists():
            has_data = True
            seeder.add_entity(Shipment, 10, {
                'tracking_id': lambda x: str(uuid.uuid4()),
                'sender_phone_number': lambda x: seeder.faker.phone_number(),
                'sender_address': lambda x: seeder.faker.street_address(),
                'sender_country': lambda x: seeder.faker.country(),
                'sender_city': lambda x: seeder.faker.city(),
                'sender_postal_code': lambda x: seeder.faker.postcode(),
                'receiver_address': lambda x: seeder.faker.street_address(),
                'receiver_country': lambda x: seeder.faker.country(),
                'receiver_city': lambda x: seeder.faker.city(),
                'receiver_postal_code': lambda x: seeder.faker.postcode(),
                'receiver_phone_number': lambda x: seeder.faker.phone_number(),
                'user': user
            })

        if(has_data):
            inserted_pks = seeder.execute()
