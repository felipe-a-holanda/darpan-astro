from datetime import datetime,timedelta
from collections import OrderedDict
from math import ceil

import networkx as nx
import swisseph
swisseph.set_ephe_path('/usr/share/libswe/ephe/')

DELTA = 0.0004


from IPython import embed


def diff(a1, a2):
    angle_diff = ((a1 - a2 + 180 + 360) % 360) - 180
    return angle_diff

def binary_search(function, target, lo = 0, hi = None, delta = DELTA):
    val = None
    i = 0
    
    while lo < hi:
        
        mid = lo + (hi - lo)/2
        dif = diff(function(mid), target)
        i += 1
        #print(i,lo,hi,dif,delta)
        if dif < 0:
            lo = mid
        else:
            hi = mid
        if abs(dif) < delta:
            return mid
        if i > 30:
            return None
        
        


def get_sun(date):
    julday = swisseph.julday(date.year, date.month, date.day, date.hour + date.minute/60.0)
    return swisseph.calc_ut(julday, 0)[0]


class AttrDict(OrderedDict):
    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
    
    def __setitem__(self, key, value):
        super(AttrDict, self).__setitem__(key, value)
        setattr(self, str(key), value)

class AstroChart(object):
    SUN = 0
    TRUE_NODE = 11
    EARTH = 14
    
    def __init__(self, birthday):
        self.birth_date = birthday
        self.birth_julian = self.to_julian(birthday)
        self.planets = self.calc_planets()
        
    def get_opposite_angle(self, angle):
        return (360 + angle - 180) % 360
    
    def calc_planets(self):
        planets = AttrDict()
        for i in range(10):            
            angle = swisseph.calc_ut(self.birth_julian, i)[0]
            planets[swisseph.get_planet_name(i).lower()] = angle
            
            if i==0: # Add earth
                angle = swisseph.calc_ut(self.birth_julian, AstroChart.SUN)[0]
                angle = self.get_opposite_angle(angle)
                planets[swisseph.get_planet_name(AstroChart.EARTH).lower()] = angle
            elif i==1: # Add nodes
                angle = swisseph.calc_ut(self.birth_julian, AstroChart.TRUE_NODE)[0]
                planets['north node'] = angle
                planets['south node'] = self.get_opposite_angle(angle)
        
        for name, angle in planets.items():
            setattr(self, name, angle)
        return planets
            
        
        
    def to_julian(self, date):
        return swisseph.julday(date.year, date.month, date.day, date.hour + date.minute/60.0)




class RaveGraph(object):
    
    CENTERS = [
        ('root', [53, 60, 52, 19, 39, 41, 58, 38, 54, ]),
        ('sacral', [5,14, 29,59, 9, 3, 42, 27, 34]),
        ('splenic', [48, 57, 44, 50, 32, 28, 18]),
        ('solar_plexus', [36, 22, 37,6, 49, 55, 30]),
        ('g', [1, 13, 25, 46, 2, 15, 10, 7]),
        ('heart', [21, 40, 26, 51]),
        ('throat', [62, 23, 56, 35, 12, 45, 33, 8, 31, 20, 16]),
        ('ajna', [47, 24, 4, 11, 43, 17]),
        ('head', [64, 61, 63]),
    ]


    # https://www.geneticmatrix.com/human-design-channels/
    CHANNELS = [
        ((1, 8), 'Inspiration', 'A creative Role Model', 'Individual'),
        ((2, 14), 'The Beat', 'A Keeper of the Keys', 'Individual'),
        ((3, 60), 'Mutation', 'Energy which initiates and fluctuates, Pulse', 'Individual'),
        ((4, 63), 'Logic', 'Mental Ease mixed with Doubt', 'Logical'),
        ((5, 15), 'Rhythm', 'Being in the flow', 'Logical'),
        ((6, 59), 'Intimacy', 'Focused on Reproduction', 'Tribal'),
        ((7, 31), 'The Alpha', 'Leadership for good or bad', 'Logical'),
        ((9, 52), 'Concentration', 'Determination', 'Logical'),
        ((10, 20), 'Awakening', 'Commitment to Higher Principles', 'Integration'),
        ((10, 34), 'Exploration', 'Following own convictions', 'Centering'),
        ((10, 57), 'Perfected Form', 'Survival', 'Integration'),
        ((11, 56), 'Curiosity', 'A Seeker', 'Abstract'),
        ((12, 22), 'Openness', 'A Social Being', 'Individual'),
        ((13, 33), 'The Prodigal', 'A Witness', 'Abstract'),
        ((16, 48), 'The Wavelength', 'Talent', 'Logical'),
        ((17, 62), 'Acceptance', 'An Organisational Being', 'Logical'),
        ((18, 58), 'Judgement', 'Insatiability', 'Logical'),
        ((19, 49), 'Synthesis', 'Sensitivity', 'Tribal'),
        ((20, 34), 'Charisma', 'Where Thoughts must become Deeds', 'Integration'),
        ((20, 57), 'The Brainwave', 'Awareness in the now', 'Individual'),
        ((21, 45), 'The Money Line', 'A Materialist', 'Tribal'),
        ((23, 43), 'Structuring', 'Individuality ((Genius to Freak)', 'Individual'),
        ((24, 61), 'Awareness', 'A Thinker', 'Individual'),
        ((25, 51), 'Initiation', 'Needing to be First', 'Centering'),
        ((26, 44), 'Surrender', 'A Transmitter', 'Tribal'),
        ((27, 50), 'Preservation', 'Custodianship', 'Tribal'),
        ((28, 38), 'Struggle', 'Stubbornness', 'Individual'),
        ((29, 46), 'Discovery', 'Succeeding where others Fail', 'Abstract'),
        ((30, 41), 'Recognition', 'Focused Energy ((feelings)', 'Abstract'),
        ((32, 54), 'Transformation', 'Being Driven', 'Tribal'),
        ((34, 57), 'Power', 'An Archetype', 'Integration'),
        ((35, 36), 'Transitoriness', 'A Jack of all Trades', 'Abstract'),
        ((37, 40), 'Community', 'A Part seeking a Whole', 'Tribal'),
        ((39, 55), 'Emoting', 'Moodiness', 'Individual'),
        ((42, 53), 'Maturation', 'Balanced Development ((cyclic)', 'Abstract'),
        ((47, 64), 'Abstraction', 'Mental Activity mixed with Clarity', 'Abstract'),
    ]
    
    
    def __init__(self, activated_gates):
        self.graph = self.create_graph()
        for g in activated_gates:
            self.set_activated_gate(g)
        
        self.activated_channels = self.get_activated_channels()
        for g1,g2 in self.activated_channels:
            self.graph[g1][g2]['activated'] = True
            c1 = self.graph.node[g1]['center']
            c2 = self.graph.node[g2]['center']
            self.graph.node[c1]['activated'] =  True
            self.graph.node[c2]['activated'] =  True
            
        self.type = self.get_type()
            
    def get_type(self):
        if self.graph.node['sacral']['activated']:
            return 'generator'
        return 'other'
            
        
    
        

    def create_graph(self):
        rave = nx.Graph()    
        rave.add_nodes_from(range(1,65), type='gate', activated=False)    
        for center, gates in RaveGraph.CENTERS:
            rave.add_node(center, type='center', activated=False)
            rave.add_edges_from([(center, gate) for gate in gates], type='center-gate')
            for g in gates:
                rave.node[g]['center'] = center
        for ports, name, desc, circuit in RaveGraph.CHANNELS:
            rave.add_edge(*ports, name=name, description=desc, circuit=circuit, type='channel', activated=False)
        return rave
    
    @property
    def centers(self):
        return [n for n in self.graph.nodes if self.graph.nodes(data=True)[n]['type']=='center']
        
    
    @property
    def gates(self):
        return [n for n in self.graph.nodes if self.graph.nodes(data=True)[n]['type']=='gate']
    
    @property
    def channels(self):
        return [a for a,b in nx.get_edge_attributes(self.graph, 'type').items() if b=='channel']
    
    @property
    def center_gates(self):
        return [a for a,b in nx.get_edge_attributes(self.graph, 'type').items() if b=='center-gate']
        
    def set_activated_gate(self, gate):
        self.graph.nodes[gate]['activated']=True
    
    def get_activated_channels(self):
        return [channel for channel in self.channels if (self.graph.node[channel[0]]['activated']==True and self.graph.node[channel[1]]['activated']==True)]
    
    def get_activated_centers(self):
        return [n for n in self.centers if self.graph.nodes(data=True)[n]['activated']==True]
    

class RaveChart(object):
    
    ICHING = (1, 43, 14, 34, 9, 5, 26, 11, 10, 58, 38, 54, 61, 60, 41,19, 
    13, 49, 30, 55, 37, 63, 22, 36, 25, 17, 21,51,42, 3, 27, 24, 
    2, 23,8, 20, 16, 35, 45, 12, 15, 52, 39, 53, 62, 56, 31, 33, 
    7, 4, 29, 59, 40, 64, 47, 6, 46, 18, 48, 57,32, 50, 28, 44)
    
    FIRST_HEXAGRAM = 223.25 # 8*30 - 3*360.0/64 + 1.0/8
    DIVISIONS = [64, 6, 6, 6, 5]
    
    HEXAGRAM = 5.625 # 360.0 /  64
    LINE = 0.9375    # 360.0 / (64*6)
    COLOR = 0.15625  # 360.0 / (64*6*6)
    TONE = 0.026041666666666666 # 360.0 / (64*6*6*6)
    BASE = 0.005208333333333333 # 360.0 / (64*6*6*6*5)
    SEQUENCE = [HEXAGRAM, LINE, COLOR, TONE, BASE]
    
    # Determination:
    #   Design Sun/Earth
    #   Dietary
    DETERMINATION_COLOR = [
        # Color Number, Sensing, Left Tone, Right Tone
        (1, 'Appetite', 'Consecutive', 'Alternating'),
        (2, 'Taste', 'Open', 'Closed'),
        (3, 'Thirst', 'Hot', 'Cold'),
        (4, 'Touch', 'Calm', 'Nervous'),
        (5, 'Sound', 'High', 'Low'),
        (6, 'Light', 'Direct', 'Indirect'),
    ]
    
    
    DETERMINATION_TONE = [
        # (Tone Number, Direction, Sensing, Center, Mode)
        (1, 'Left', 'Smell', 'Splenic', 'Concentrated'),
        (2, 'Left', 'Taste', 'Splenic', 'Concentrated'),
        (3, 'Left', 'Outer Vision', 'Ajna', 'Periodic'),
        (4, 'Right', 'Inner Vision', 'Ajna', 'Periodic'),
        (5, 'Right', 'Feeling', 'Solar Plexus', 'Clyclic'),
        (6, 'Right', 'Touch', 'Solar Plexus', 'Cyclic'),
    ]
    
    # Transformation:
    #   Personality Sun/Earth
    #   Motivation
    TRANSFORMATION_COLOR = [
        # (Color number, Motivation, Transference, Left Tone, Right Tone)
        (1, 'Fear', 'Need', 'Communalist', 'Separatist'),
        (2, 'Hope', 'Guilt', 'Theist', 'Antitheist'),
        (3, 'Desire', 'Innocence', 'Leader', 'Follower'),
        (4, 'Need', 'Fear', 'Master', 'Novice'),
        (5, 'Guilt', 'Hope', 'Conditioner', 'Conditioned'),
        (6, 'Innocence', 'Desire', 'Observer', 'Observed'),
        
    ]
    
    # Environment
    #  Design Node
    
    ENVIRONMENT_COLOR = [
        # (Color Number, Environment, Left Tone, Right Tone)
        (1, 'Caves', 'Exclusive', 'Flexible'),
        (2, 'Markets', 'Internal', 'External'),
        (3, 'Kitchens', 'Wet', 'Dry'),
        (4, 'Mountains', 'Active', 'Passive'),
        (5, 'Valleys', 'Narrow', 'Wide'),
        (6, 'Shores', 'Natural', 'Artificial'),
    ]
    

    
    def __init__(self, birthday):
        self.birth_date = birthday
                        
        self.birth_chart = AstroChart(self.birth_date)
        self.design_date = self.find_design_date()
        
        self.design_chart = AstroChart(self.design_date)
        
        self.personality = self.generate_activated_ports(self.birth_chart)
        self.design = self.generate_activated_ports(self.design_chart)
        
        self.activated_gates = self.generate_activated_gates(self.personality, self.design)
        
        self.rave_graph = self.create_rave_graph(self.personality, self.design)
        self.type = self.rave_graph.type
        
        self.determination = self.calculate_determination()
        self.transformation = self.calculate_transformation()
        self.environment = self.calculate_environment()
    
    
    
    
    def __str__(self):
        return "Rave: %s "%(str(self.birth_date))
        
    def calculate_environment(self):
        """
        Design Node
        """
        gate, line, color, tone, base = self.design['north node']
        
        env_color = self.ENVIRONMENT_COLOR[color-1]
        
        t = divmod(tone-1,3)[0]
        env = env_color[1], env_color[2+t]
        
        
        return env
        
    def calculate_transformation(self):
        """
        Personality Sun/Earth
        """
        
        gate, line, color, tone, base = self.personality['sun']
        
        t_color = self.TRANSFORMATION_COLOR[color-1]
        
        t = list(t_color[1:3])
        if tone <= 3:
            t.append(t_color[3])
        else:
            t.append(t_color[4])
        return t
        
    def calculate_determination(self):
        """
        Design Sun/Earth
        """
        gate, line, color, tone, base = self.design['sun']
        
        det_color = self.DETERMINATION_COLOR[color-1]
        det_tone = self.DETERMINATION_TONE[tone-1]
        
        det = [det_tone[1], det_color[1]]
        
        if det_tone[1] == 'Left':
            det.append(det_color[2])
        else:
            det.append(det_color[3])
        
        det += det_tone[2:]
        
        
        
        return det
        
    def variables(self):
        report = ''
        report += 'Determination (dietary):\n'
        report += str(self.design['sun'][2:4]) + '\n'
        report += str(self.determination) + '\n\n'
        report += 'Transformation (motivation)\n'
        report += str(self.personality['sun'][2:4]) + '\n'
        report += str(self.transformation) +'\n\n'
        report += 'Environment\n'
        report += str(self.design['north node'][2:4]) + '\n'
        report += str(self.environment) +'\n\n'
        
        return report
    
    def generate_activated_ports(self, astrochart):
        ports = AttrDict()
        for name, angle in astrochart.planets.items():
            numbers = self.degress_to_hexagram(angle)
            ports[name] = numbers
        return ports
        
    def create_rave_graph(self, personality_gates, design_gates):
        
        activated_gates = [n[0] for n in personality_gates.values()]
        activated_gates += [n[0] for n in design_gates.values()]
        rave_graph = RaveGraph(activated_gates)
        #for planet, numbers in personality_gates.items():
        #    rave_graph.set_activated_gate(numbers[0])
        #for planet, numbers in design_gates.items():
        #    rave_graph.set_activated_gate(numbers[0])
        return rave_graph
        
    def generate_activated_gates(self, personality, design):        
        activations = AttrDict()
        for planet, numbers in personality.items():
            gate = numbers[0]
            if gate not in activations:
                activations[gate] = []
            activations[gate].append((planet, 'personality', numbers))
        for planet, numbers in design.items():
            gate = numbers[0]
            if gate not in activations:
                activations[gate] = []
            activations[gate].append((planet, 'design', numbers))
        return activations
            
    def get_activated_channels(self):
        return self.rave_graph.get_activated_channels()
        
    def get_activated_centers(self):
        return self.rave_graph.get_activated_centers()
        
        
        
    def find_design_date(self):
        self.target_design_sun = (360+ self.birth_chart.sun - 88) % 360
        lo = self.birth_date - timedelta(days=94)
        hi = self.birth_date - timedelta(days=86)
        design_date = binary_search(get_sun, self.target_design_sun, lo, hi)
        
        if not design_date:
            raise Exception('SOCORRO')
        return design_date
    
    def degress_to_hexagram(self, degrees):        
        angle = (360 + degrees - RaveChart.FIRST_HEXAGRAM) % 360        
        circle = 360.0
        a = 1.0
        numbers = []
        for divisor in RaveChart.DIVISIONS:
            a *= divisor
            size = circle/a
            i = angle/size
            angle = angle - int(angle/size) * size
            numbers.append(i)            
        
        numbers[0] = int(numbers[0])
        numbers[0] = RaveChart.ICHING[numbers[0]]
        
        for i,n in enumerate(numbers):
            numbers[i] = int(ceil(n))
        
        return numbers
    
    def connection(self, other):
        self_gates = self.activated_gates.keys()
        other_gates = other.activated_gates.keys()
        eletromagnetic = []
        friendship = []
        dominance_self = []
        dominance_other = []
        compromise_self = []
        compromise_other = []
        
        channels = dict()
        channels['eletromagnetic'] = []
        channels['friendship'] = []
        channels['dominance_self'] = []
        channels['dominance_other'] = []
        channels['compromise_self'] = []
        channels['compromise_other'] = []
        
        for channel in RaveGraph.CHANNELS:
            gates,a,y,z = channel
            g1, g2 = gates
            if g1 in self_gates and g1 in other_gates:
                friendship.append(g1)
            if g2 in self_gates and g2 in other_gates:
                friendship.append(g2)
            if (g1 in self_gates and g1 not in other_gates and g2 in other_gates and g2 not in self_gates) or (g2 in self_gates and g2 not in other_gates and g1 in other_gates and g1 not in self_gates):
                eletromagnetic.append(channel)
            elif g1 in self_gates and g2 in self_gates and g1 in other_gates and g2 in other_gates:
                friendship.append(channel)
            elif g1 in self_gates and g2 in self_gates and g1 not in other_gates and g2 not in other_gates:
                dominance_self.append(channel)
            elif not g1 in self_gates and not g2 in self_gates and g1 in other_gates and g2  in other_gates:
                dominance_other.append(channel)
            elif g1 in self_gates and g2 in self_gates and (g1  in other_gates or g2  in other_gates):
                compromise_self.append(channel)
            elif g1 in other_gates and g2 in other_gates and (g1  in self_gates or g2  in self_gates):
                compromise_other.append(channel)
        
        channels['eletromagnetic'] = eletromagnetic
        channels['friendship'] = sorted(set(friendship))
        channels['dominance_self'] = dominance_self
        channels['dominance_other'] = dominance_other
        channels['compromise_self'] = compromise_self
        channels['compromise_other'] = compromise_other
        
        
        return channels
            
        
        
        


import random
from random import randrange
from datetime import timedelta

def random_date(start, end):
    """
    This function will return a random datetime between two datetime 
    objects.
    """
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = randrange(int_delta)
    return start + timedelta(seconds=random_second)

def test():
    s = datetime(1900,1,1,12,0)
    e = datetime(2020,1,1,12,0)
    random.seed(3)
    dates = sorted([random_date(s, e) for i in range(1000)])
    charts = []
    for i,d in enumerate(dates):
        r = RaveChart(d)
        charts.append(r)
        print(i,r, r.type)
    print(len([r for r in charts if r.type=='generator']))
        
        



if __name__=='__main__':
    #gabs = RaveChart(datetime(1996,12,15,14,11))
    #test()
    darpan = RaveChart(datetime(1986,12,22,8,34))
    print(darpan.get_activated_centers())
    embed()
    
def c():
    darpan = RaveChart(datetime(1986,12,22,8,34))
    puja = RaveChart(datetime(1985,9,21,12,15))
    tiago = RaveChart(datetime(1993,7,5,17))
    vitor = RaveChart(datetime(1988,8,18,21,30))

    print("Darpan")
    print(darpan.personality['north node'], 'perspective')
    print(darpan.design['north node'], 'environment')

    print (darpan.variables())

    print("Puja")
    print(puja.variables())


    def print_connection():
        for k,v in darpan.connection(vitor).items():
            print(k)
            for c in v:
                print(c)
            print()
    #print darpan.get_activated_channels()
