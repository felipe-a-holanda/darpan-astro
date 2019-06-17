from .astrolib import PLANET_NAMES


def consts(request):
    return {
            'planets':PLANET_NAMES,
        }
