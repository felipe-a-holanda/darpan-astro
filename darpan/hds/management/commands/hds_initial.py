from django.core.management.base import BaseCommand, CommandError
from hds.models import Gate, Channel, Center
from django.db import transaction

class Command(BaseCommand):
    help = 'Populate with initial data'

    def add_arguments(self, parser):
        parser.add_argument(
            '--delete',
            action='store_true',
            dest='delete',
            help='Delete poll instead of closing it',
        )

    
    def handle(self, *args, **options):
        if options['delete']:
           
            print(Gate.objects.all().delete())
            print(Channel.objects.all().delete())
            print(Center.objects.all().delete())
            print("All deleted")
        else:
            self.create_gates()
            self.create_channels()
            self.create_centers()
            
            
    
    @transaction.atomic
    def create_gates(self):
        for g in Gate.GATES:
            number, name = g
            gate, created = Gate.objects.get_or_create(number=number, name=name)
            gate.save()
            print(gate)
            
            
    @transaction.atomic
    def create_channels(self):
       for channel in Channel.CHANNELS:
            (1, 8), 'Inspiration', 'A creative Role Model', 'Individual'
            gates, name, title, circuit_group, circuit = channel
            g1, g2 = gates
            gate1 = Gate.objects.get(number=g1)
            gate2 = Gate.objects.get(number=g2)
            channel, created = Channel.objects.get_or_create(gate1=gate1, gate2=gate2, name=name, title=title, circuit_group=circuit_group, circuit=circuit)
            channel.save()
            print(channel)
            
    @transaction.atomic
    def create_centers(self):
        for center in Center.CENTERS:
            center_slug, center_gates = center
            name = center_slug.replace('_',' ').replace('-',' ').title()
            center, created = Center.objects.get_or_create(slug=center_slug, name=name)
            center.save()
            center.gates.set(Gate.objects.filter(number__in=center_gates))
            print(center)
            
            
