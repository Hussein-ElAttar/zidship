import os
import random
import uuid

from django.contrib.auth.models import User
from django.core.management import call_command
from django.core.management.base import BaseCommand
from django_seed import Seed
from shipments.enums import ShipmentStatusEnum
from shipments.models import Courier, Shipment, ShipmentMethod, ShipmentStatus


class Command(BaseCommand):

    def handle(self, *args, **options):
        seeder = Seed.seeder()

        if not User.objects.exists():
            self.stdout.write('Seeding initial data')
            user = User.objects.create_superuser(
                os.environ.get('DJANGO_SUPER_USER_NAME'),
                os.environ.get('DJANGO_SUPER_USER_EMAIL'),
                os.environ.get('DJANGO_SUPER_USER_PASSWORD')
            )

        if not Courier.objects.exists():
            seeder.add_entity(Courier, 1, {'name': 'Fedex'})

        if not ShipmentMethod.objects.exists():
            seeder.add_entity(ShipmentMethod, 1, {'name': 'Same day delivery'})
            seeder.add_entity(ShipmentMethod, 1, {'name': 'Within 7 Days'})

        if not ShipmentStatus.objects.exists():
            seeder.add_entity(ShipmentStatus, 1, {'status':ShipmentStatusEnum.PROCCESSING })
            seeder.add_entity(ShipmentStatus, 1, {'status':ShipmentStatusEnum.PENDING })
            seeder.add_entity(ShipmentStatus, 1, {'status':ShipmentStatusEnum.CONFIRMED })
            seeder.add_entity(ShipmentStatus, 1, {'status':ShipmentStatusEnum.IN_PROGRESS })
            seeder.add_entity(ShipmentStatus, 1, {'status':ShipmentStatusEnum.DELIVERED })
            seeder.add_entity(ShipmentStatus, 1, {'status':ShipmentStatusEnum.PENDING_CANCELATION })
            seeder.add_entity(ShipmentStatus, 1, {'status':ShipmentStatusEnum.CANCELED })

        if not Shipment.objects.exists():
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
            })
        inserted_pks = seeder.execute()
