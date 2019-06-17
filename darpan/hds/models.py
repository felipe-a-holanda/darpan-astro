from django.db import models
from django.db.models.signals import post_save
from django.urls import reverse
from django.dispatch import receiver
from django.template.defaultfilters import slugify
from charts.models import Chart

from .hds import RaveChart as Rave_Chart

class Gate(models.Model):
    GATES = [
        (1, "Self-Expression"),
        (2, "Higher Knowledge"),
        (3, "Ordering"),
        (4, "Formulization"),
        (5, "Fixed Rhythms"),
        (6, "Friction"),
        (7, "The Role of the Self"),
        (8, "Contribution"),
        (9, "Focus"),
        (10, "Behavior of the Self"),
        (11, "Ideas"),
        (12, "Caution"),
        (13, "Listener"),
        (14, "Power Skills"),
        (15, "Extremes"),
        (16, "Skills"),
        (17, "Opinions"),
        (18, "Correction"),
        (19, "Wanting"),
        (20, "The Now"),
        (21, "The Hunter/Huntress"),
        (22, "Openness"),
        (23, "Assimilation"),
        (24, "Rationalizing"),
        (25, "The Spirit of the Self"),
        (26, "The Egoist"),
        (27, "Caring"),
        (28, "The Game Player"),
        (29, "Saying Yes"),
        (30, "Recognition of Feelings"),
        (31, "Leading"),
        (32, "Continuity"),
        (33, "Privacy"),
        (34, "Power"),
        (35, "Change"),
        (36, "Crisis"),
        (37, "Friendship"),
        (38, "The Fighter"),
        (39, "The Provocateur"),
        (40, "Aloneness"),
        (41, "Contraction"),
        (42, "Growth"),
        (43, "Insight"),
        (44, "Alertness"),
        (45, "Gatherer"),
        (46, "The Determination of the Self"),
        (47, "Realizing"),
        (48, "Depth"),
        (49, "Principles"),
        (50, "Values"),
        (51, "Shock"),
        (52, "Inaction"),
        (53, "Beginnings"),
        (54, "Ambition"),
        (55, "Spirit"),
        (56, "Stimulation"),
        (57, "Intuitive Insight"),
        (58, "Aliveness"),
        (59, "Sexuality"),
        (60, "Acceptance"),
        (61, "Mystery"),
        (62, "Detail"),
        (63, "Doubt"),
        (64, "Confusion"),


    ]
    number = models.PositiveSmallIntegerField(unique=True)
    name = models.CharField(max_length=20)
    slug = models.SlugField(max_length=20)
    
    def __str__(self):
        return "%d - Gate of %s" % (self.number, self.name)
        
    def get_absolute_url(self):
        return reverse('hds:gate-detail', kwargs={'slug':self.slug})
    
    def save(self, *args, **kwargs):
        self.slug = slugify(str(self))
        super(Gate, self).save(*args, **kwargs)
    
    
    

class Channel(models.Model):
    CHANNELS = [
        ((1, 8), 'Inspiration', 'A creative Role Model', 'Individual', 'Knowing'),
        ((2, 14), 'The Beat', 'A Keeper of the Keys', 'Individual', 'Knowing'),
        ((3, 60), 'Mutation', 'Energy which initiates and fluctuates, Pulse', 'Individual', 'Knowing'),
        ((4, 63), 'Logic', 'Mental Ease mixed with Doubt', 'Collective', 'Logical'),
        ((5, 15), 'Rhythm', 'Being in the flow', 'Collective', 'Logical'),
        ((6, 59), 'Intimacy', 'Focused on Reproduction', 'Tribal', 'Defense'),
        ((7, 31), 'The Alpha', 'Leadership for good or bad', 'Collective', 'Logical'),
        ((9, 52), 'Concentration', 'Determination', 'Collective', 'Logical'),
        ((10, 20), 'Awakening', 'Commitment to Higher Principles', 'Individual', 'Integration'),
        ((10, 34), 'Exploration', 'Following own convictions', 'Individual', 'Centering'),
        ((10, 57), 'Perfected Form', 'Survival', 'Individual', 'Integration'),
        ((11, 56), 'Curiosity', 'A Seeker', 'Collective', 'Abstract/Sensing'),
        ((12, 22), 'Openness', 'A Social Being', 'Individual', 'Knowing'),
        ((13, 33), 'The Prodigal', 'A Witness', 'Collective', 'Abstract/Sensing'),
        ((16, 48), 'The Wavelength', 'Talent', 'Collective', 'Logical'),
        ((17, 62), 'Acceptance', 'An Organisational Being', 'Collective', 'Logical'),
        ((18, 58), 'Judgement', 'Insatiability', 'Collective', 'Logical'),
        ((19, 49), 'Synthesis', 'Sensitivity', 'Tribal', 'Ego'),
        ((20, 34), 'Charisma', 'Where Thoughts must become Deeds', 'Individual', 'Integration'),
        ((20, 57), 'The Brainwave', 'Awareness in the now', 'Individual', 'Knowing'),
        ((21, 45), 'The Money Line', 'A Materialist', 'Tribal', 'Ego'),
        ((23, 43), 'Structuring', 'Individuality ((Genius to Freak)', 'Individual', 'Knowing'),
        ((24, 61), 'Awareness', 'A Thinker', 'Individual', 'Knowing'),
        ((25, 51), 'Initiation', 'Needing to be First', 'Individual', 'Centering'),
        ((26, 44), 'Surrender', 'A Transmitter', 'Tribal', 'Ego'),
        ((27, 50), 'Preservation', 'Custodianship', 'Tribal', 'Defense'),
        ((28, 38), 'Struggle', 'Stubbornness', 'Individual', 'Knowing'),
        ((29, 46), 'Discovery', 'Succeeding where others Fail', 'Collective', 'Abstract/Sensing'),
        ((30, 41), 'Recognition', 'Focused Energy ((feelings)', 'Collective', 'Abstract/Sensing'),
        ((32, 54), 'Transformation', 'Being Driven', 'Tribal', 'Ego'),
        ((34, 57), 'Power', 'An Archetype', 'Individual', 'Integration'),
        ((35, 36), 'Transitoriness', 'A Jack of all Trades', 'Collective', 'Abstract/Sensing'),
        ((37, 40), 'Community', 'A Part seeking a Whole', 'Tribal', 'Ego'),
        ((39, 55), 'Emoting', 'Moodiness', 'Individual', 'Knowing'),
        ((42, 53), 'Maturation', 'Balanced Development ((cyclic)', 'Collective', 'Abstract/Sensing'),
        ((47, 64), 'Abstraction', 'Mental Activity mixed with Clarity', 'Collective', 'Abstract/Sensing'),
    ]
    
    gate1 = models.ForeignKey('Gate', on_delete=models.CASCADE, related_name='gate1')
    gate2 = models.ForeignKey('Gate', on_delete=models.CASCADE, related_name='gate2')
    name = models.CharField(max_length=20)
    slug = models.SlugField(max_length=20)
    title = models.CharField(max_length=30)
    circuit_group = models.CharField(max_length=30)
    circuit = models.CharField(max_length=30)
    
    class Meta:
        unique_together = (("gate1", "gate2"),)
    
    def __str__(self):
        return "(%d-%d) Channel of %s " % (self.gate1.number, self.gate2.number, self.name)
        
    def get_absolute_url(self):
        return reverse('hds:channel-detail', kwargs={'slug':self.slug})
        
    def save(self, *args, **kwargs):
        self.slug = slugify(str(self))
        super(Channel, self).save(*args, **kwargs)
    
class Center(models.Model):
    CENTERS = [
        ('root', [53, 60, 52, 19, 39, 41, 58, 38, 54]),
        ('sacral', [5,14, 29,59, 9, 3, 42, 27, 34]),
        ('splenic', [48, 57, 44, 50, 32, 28, 18]),
        ('solar_plexus', [36, 22, 37,6, 49, 55, 30]),
        ('g', [1, 13, 25, 46, 2, 15, 10, 7]),
        ('heart', [21, 40, 26, 51]),
        ('throat', [62, 23, 56, 35, 12, 45, 33, 8, 31, 20, 16]),
        ('ajna', [47, 24, 4, 11, 43, 17]),
        ('head', [64, 61, 63]),
    ]
    
    
    name = models.CharField(max_length=20, null=True)
    slug = models.SlugField(max_length=20)
    gates = models.ManyToManyField(Gate)
    
    def __str__(self):
        return self.name
        
    def get_absolute_url(self):
        return reverse('hds:center-detail', kwargs={'slug':self.slug})
    
    def save(self, *args, **kwargs):
        self.slug = slugify(str(self))
        super(Center, self).save(*args, **kwargs)


class RaveChart(models.Model):
    chart = models.OneToOneField(Chart, related_name='ravechart',  on_delete=models.CASCADE)
    gates = models.ManyToManyField(Gate)
    channels = models.ManyToManyField(Channel)
    defined_centers = models.ManyToManyField(Center, related_name='defined')
    undefined_centers = models.ManyToManyField(Center, related_name='undefined')
    
    
    root = models.BooleanField(blank=True, null=True)
    sacral = models.BooleanField(blank=True, null=True)
    sacral = models.BooleanField(blank=True, null=True)
    solar_plexus = models.BooleanField(blank=True, null=True)
    g = models.BooleanField(blank=True, null=True)
    heart = models.BooleanField(blank=True, null=True)
    throat = models.BooleanField(blank=True, null=True)
    ajna = models.BooleanField(blank=True, null=True)
    head = models.BooleanField(blank=True, null=True)

    def __str__(self):
        return str(self.chart)
        
    def make_rave(self):
        rave = Rave_Chart(self.chart.datetime_utc)
        activated_gates = rave.activated_gates.keys()
        self.gates.set(Gate.objects.filter(number__in=activated_gates))
        
        channels = []
        for channel in Channel.objects.all():
            if channel.gate1.number in activated_gates and channel.gate2.number in activated_gates:
                channels.append(channel)
        
        self.channels.set(channels)
        
        print('get_activated_centers:',rave.get_activated_centers())
        for center in Center.objects.all():
            print(center.slug)
            if center.slug in rave.get_activated_centers():
                setattr(self,center.slug,True)
                self.defined_centers.add(center)
            else:
                setattr(self,center.slug,False)
                self.undefined_centers.add(center)
        
    def save(self, *args, **kwargs):
        self.make_rave()
        super().save(*args, **kwargs)


@receiver(post_save, sender=Chart)
def create_astrochart(sender, **kwargs):
    chart = kwargs["instance"]
    if kwargs["created"]:
        ravechart = RaveChart(chart=chart)
        ravechart.save()
    else:
        chart.ravechart.save()
