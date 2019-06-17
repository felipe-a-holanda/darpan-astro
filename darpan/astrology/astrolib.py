import json
import swisseph as swe
from collections import OrderedDict, namedtuple
from random import randrange
from datetime import timedelta
from datetime import datetime

#from matplotlib import pylab as plt
#from IPython import embed
from .sinastry_points import AspectPointer

swe.set_ephe_path('/usr/share/libswe/ephe/')

NPLANETS = swe.NPLANETS
NPLANETS = 12



Ascmc = namedtuple('Ascmc', ['ascendant',
'mc',
'armc',
'vertex',
'equatorial_ascendant',
'co_ascendant_Koch',
'co_ascendant_Munkasey',
'polar_ascendant'])


import swisseph as swe

PLANET_NAMES = [
    'Sun',
    'Moon',
    'Mercury',
    'Venus',
    'Mars',
    'Jupiter',
    'Saturn',
    'Uranus',
    'Neptune',
    'Pluto',
    'mean Node',
    'true Node',
    'mean Apogee',
    'osc. Apogee',
    'Earth',
    'Chiron',
    'Pholus',
    'Ceres',
    'Pallas',
    'Juno',
    'Vesta',
    'intp. Apogee',
    'intp. Perigee',
]

SIGN_NAMES = ["Aries",
    "Taurus",
    "Gemini",
    "Cancer",
    "Leo",
    "Virgo",
    "Libra",
    "Scorpio",
    "Sagittarius",
    "Capricorn",
    "Aquarius",
    "Pisces"]

SIGN_INDEX_DIC = {name:i for i, name in enumerate(SIGN_NAMES)}

class Planet(object):
    def __init__(self, index, chart):
        self.index = index
        self.name = swe.get_planet_name(index)
        self.chart = chart
        self.field = self.get_field_name(self.name)
        if hasattr(chart, self.field):
            self.angle = getattr(chart, self.field)
            self.sign = SIGN_NAMES[int(self.angle / 30) % 12]

    def get_field_name(self, name):
        return name.lower().replace(' ', '_')


def dumper(obj):
    try:
        return obj.toJSON()
    except:
        return obj.__dict__

def midpoint(a1, a2):
    return ((a1 + a2) % 360)/2


def random_date(start, end):
    """
    This function will return a random datetime between two datetime 
    objects.
    """
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = randrange(int_delta)
    return start + timedelta(seconds=random_second)

def random_birthday(birthday):
    year = 365.25
    start = birthday - timedelta(days=14*year)
    end = birthday + timedelta(days=42*year)
    
    return random_date(start, end)

def percentile(numbers, max__=200):
    numbers = sorted(numbers)
    l = len(numbers)
    d = {}
    for i, n in enumerate(numbers):
        if n not in d:
            d[n] = (i+1)/float(l)
    
    p = []
    min_ = min(d.keys())
    max_ = max(d.keys())
    last = 0
    for i in range(max__):
        if i< min_:
            last = 0
            p.append(last)
        elif i in d:
            last = d[i]
            p.append(last)
        else:
            p.append(last)
    return p




class AttrDict(OrderedDict):
    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self


class Aspect(object):
    ASPECTS = ['conjunction', 'semisextile', 'sextile', 'square', 'trine', 'quincunx', 'opposition']
    POINTER = AspectPointer()

    def __init__(self, planet1, planet2, aspect_type, diff_from_exact):
        self.planet1 = planet1
        self.planet2 = planet2
        self.aspect_type = int(aspect_type * 30)
        self.diff = diff_from_exact
        self.aspect_type_code = Aspect.ASPECTS[int(aspect_type)]
        self.aspect_code = '%s-%s-%s' % (planet1.code, self.aspect_type_code, planet2.code)
        self.points = Aspect.POINTER.point(planet1.code, self.aspect_type, planet2.code)

    @classmethod
    def calc_aspect(cls, planet1, planet2):
        a1 = planet1.x
        a2 = planet2.x
        angle_diff = abs(((a1 - a2 + 180 + 360) % 360) - 180)
        a, b = divmod(angle_diff, 30)
        c, d = map(abs, divmod(angle_diff, -30))
        diff_from_exact, exact = min((b, a), (d, c))
        if diff_from_exact < 10 and exact != 1:
            aspect_type_code = Aspect.ASPECTS[int(exact)]
            aspect_code = '%s-%s-%s' % (planet1.code, aspect_type_code, planet2.code)
            return cls(planet1, planet2, exact, diff_from_exact)
            #return int(exact*30), diff_from_exact, aspect_code


class BodyPos(object):

    OTHER_BODIES = {
        'asc': 'Ascendant',
        'mc': 'Medium Coeli',
        'vertex': 'Vertex',
        'sun-moon-midpoint': 'Sun Moon Midpoint',
    }

    SIGN_CODES = ["aries",
                  "taurus",
                  "gemini",
                  "cancer",
                  "leo",
                  "virgo",
                  "libra",
                  "scorpio",
                  "sagittarius",
                  "capricorn",
                  "aquarius",
                  "pisces"]

    HOUSES = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI', 'XII']




    def __init__(self, index, armc, latitude, ecl_nut, x, y=None, z=None, dx=None, dy=None, dz=None):
        self.index = index
        self.code = self.get_planet_code(index)
        self.name = self.get_planet_name(index)
        self.x = x
        self.dx = dx
        self.y = y
        self.sign = BodyPos.SIGN_CODES[int(x / 30) % 12]
        self.body_in_sign = '%s-in-%s' % (self.code, self.sign)

        self.house = None
        self.body_in_house = None
        if latitude and ecl_nut and armc:
            self.house = int(self.calc_house(armc, latitude, ecl_nut))
            house_name = BodyPos.HOUSES[self.house-1].lower()
            self.body_in_house = '%s-in-%s' % (self.code, house_name)

    def get_planet_name(self, index):
        if isinstance(index, int):
            return swe.get_planet_name(index)
        return BodyPos.OTHER_BODIES[self.code]

    def get_planet_code(self, index):
        if isinstance(index, int):
            name = self.get_planet_name(index)
            code = name.lower().replace(' ', '-')
            return code
        return index

    def calc_house(self, armc, latitude, ecl_nut):
        return swe.house_pos(armc, latitude, ecl_nut, self.x, self.y)

    def calc_aspect(self, other):
        return Aspect.calc_aspect(self, other)

    def calc_aspect_old(self, other):
        a1 = self.x
        a2 = other.x
        angle_diff = abs(((a1 - a2 + 180 + 360) % 360) - 180)
        a, b = divmod(angle_diff, 30)
        c, d = map(abs, divmod(angle_diff, -30))
        diff_from_exact, exact = min((b, a), (d, c))
        if diff_from_exact < 10:
            aspect_type_code = BodyPos.ASPECTS[int(exact)]
            aspect_code = '%s-%s-%s' % (self.code, aspect_type_code, other.code)
            return int(exact*30), diff_from_exact, aspect_code

    def round(self, f):
        return float("%.3f"% f)

    def toDict(self):
        return self.__dict__

    def toJSON(self):
        return {'index':self.index, 'code':self.code, 'name':self.name,'x':self.round(self.x), 'dx':self.round(self.dx), 'sign':self.sign, 'body_in_sign':self.body_in_sign}




class AstroChart(object):

    def __init__(self, datetime_utc, latitude=None, longitude=None):
        self.datetime_utc = datetime_utc
        self.datetime_julday = self.calc_julday(self.datetime_utc)
        self.latitude = latitude
        self.longitude = longitude

        self.houses = None
        self.ascmc = None
        self.armc = None
        self.asc = None
        if self.latitude and self.longitude:
            self.houses, self.ascmc = self.calc_houses()
            self.asc = self.houses[1]
            self.mc = self.houses[10]

        if self.ascmc:
            self.armc = self.ascmc.armc
            self.asc = self.ascmc.ascendant
            self.mc = self.ascmc.mc
            self.vertex = self.ascmc.vertex


        self.ecl_nut = swe.calc_ut(self.datetime_julday, swe.ECL_NUT)[0]
        
        if self.latitude:
            self.planets = self.calc_planets_houses()
        else:
            self.planets = self.calc_planets()
        

        self.aspects = self.calc_aspects(self.planets)
        self.categories = self.generate_categories()

    def generate_categories(self):
        categories = []
        for planet_code, attrs in self.planets.items():
            categories.append(attrs.body_in_sign)
            categories.append(attrs.body_in_house)
            categories += [aspect.aspect_code for aspect_dic in self.aspects.values() for aspect in aspect_dic.values() if aspect]
        categories = filter(None, categories)
        return categories


    def calc_julday(self, datetime_utc):
        j = swe.julday(datetime_utc.year, datetime_utc.month, datetime_utc.day, datetime_utc.hour + datetime_utc.minute / 60.0)
        return j
        
        
    def calc_planets(self):
        planets = AttrDict()

        for i in range(NPLANETS):
            body_pos = BodyPos(i, self.armc, self.latitude, self.ecl_nut, *swe.calc_ut(self.datetime_julday, i))
            planets[body_pos.code] = body_pos

        sun_moon_midpoint = midpoint(planets['sun'].x,  planets['moon'].x)
        planets['sun-moon-midpoint'] = BodyPos('sun-moon-midpoint', None, None, None, sun_moon_midpoint)


        self.planets_dict = OrderedDict()
        for k in planets:
            self.planets_dict[k] = planets[k].toDict()
        return planets



    def calc_planets_houses(self):
        planets = AttrDict()

        planets['asc'] = BodyPos('asc', None, None, None, self.asc)
        for i in range(NPLANETS):
            body_pos = BodyPos(i, self.armc, self.latitude, self.ecl_nut, *swe.calc_ut(self.datetime_julday, i))
            planets[body_pos.code] = body_pos

        planets['mc'] = BodyPos('mc', None, None, None, self.mc)
        planets['vertex'] = BodyPos('vertex', None, None, None, self.vertex)

        sun_moon_midpoint = midpoint(planets['sun'].x,  planets['moon'].x)
        planets['sun-moon-midpoint'] = BodyPos('sun-moon-midpoint', None, None, None, sun_moon_midpoint)


        self.planets_dict = OrderedDict()
        for k in planets:
            self.planets_dict[k] = planets[k].toDict()
        return planets


    def calc_houses(self):
        houses, ascmc = swe.houses(self.datetime_julday, self.latitude, self.longitude)
        houses = OrderedDict([(i+1, angle) for i, angle in enumerate(houses)])
        ascmc = Ascmc(*ascmc)
        return houses, ascmc

    def calc_aspects(self, planets):
        aspects = OrderedDict()
        for p1_code, p1 in planets.items():
            aspects[p1_code] = OrderedDict()
            for p2_code, p2 in planets.items():
                aspects[p1_code][p2_code] = p1.calc_aspect(p2)
        return aspects


    def calc_sinastry(self, other):
        sinastry = OrderedDict()
        planets1 = self.planets
        planets2 = other.planets
        points = 0
        abs_points = 0
        for p1_code, p1 in planets1.items():
            sinastry[p1_code] = OrderedDict()
            for p2_code, p2 in planets2.items():
                aspect = p1.calc_aspect(p2)
                if aspect:
                    points += aspect.points
                    abs_points += abs(aspect.points)
                sinastry[p1_code][p2_code] = aspect
        return sinastry, points, abs_points
        
    
    def generate_sinastry_model(self, num_interactions=1000):
        dates = [random_birthday(self.datetime_utc) for i in range(num_interactions)]
        charts = [AstroChart(date, self.latitude, self.longitude) for date in dates]
        
        sinastries = []
        for chart in charts:
            sinastry, points, abs_points = self.calc_sinastry(chart)
            sinastries.append(points)
        #print(sorted(sinastries))
        return percentile(sinastries)
        
            


    def get_chart(self):
        return {'planets':self.planets_dict, 'houses':self.houses, 'asc':self.asc, 'aspects':self.aspects}

    def get_chart_json(self):
        return json.dumps(self.get_chart(), default=dumper, indent=2)



def find_percent(number, array):
    array = sorted(array)
    l = len(array)
    for i,n in enumerate(array):
        if number < n:
            return i/float(l)
    return 1
    



def test_points(chart_data):
    name, date, lat, lon = chart_data
    print("\n\n%s\n\n"%name)
    dates = [random_birthday(date) for i in range(10000)]
    
    chart = AstroChart(date, lat, lon)
    
    points_dates = []
    for d in dates:
        chart2 = AstroChart(d, lat, lon)
        p = chart.calc_sinastry(chart2)[2]
        points_dates.append([p, str(d)])
    
    points_dates = sorted(points_dates)
    points = [i[0] for i in points_dates]
    for i in range(len(points)):
        p = find_percent(points[i], points)
        points_dates[i].append(p)
    
    si = []
    for l in charts:
        name, d, lat, lon = l
        chart2 = AstroChart(d, lat, lon)
        p = chart.calc_sinastry(chart2)[2]
        si.append((p, name))
        
    si = sorted(si)
    
    for p, n in si:
        c = find_percent(p, points)
        print(c, p, n)
    
    y = si[-4][0]
    x = find_percent(y, points)*len(points)
    
    plt.plot(points)
    plt.plot([x],[y],'x')
    
    for i in points_dates[-10:]:
        print(i)
    
    plt.show()
    embed()
    return points
    


def test():
    from datetime import datetime
    date = datetime(1986,  12, 22, 8, 34)
    lat = -5.14
    lon = -38.09
    chart = AstroChart(date, lat, lon)
    chart2 = AstroChart(date, lat, lon)
    print(chart.calc_sinastry(chart2)[2])
    
    sun = chart.planets['sun'].x
    print(sun)
    assert sun >270 and sun <271


if __name__ == '__main__':
    points = test_points(charts[0])
    #print(points)
