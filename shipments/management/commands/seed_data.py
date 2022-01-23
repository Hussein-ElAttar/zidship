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
            seeder.add_entity(ShipmentStatus, 10, {
                'status': lambda x: random.choice(ShipmentStatusEnum.choices())[1]
            })

        if not Shipment.objects.exists():
            seeder.add_entity(Shipment, 10, {
                'tracking_id': lambda x: str(uuid.uuid4())
            })

        inserted_pks = seeder.execute()
