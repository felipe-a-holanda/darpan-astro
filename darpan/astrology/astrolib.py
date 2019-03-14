
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
