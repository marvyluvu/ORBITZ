from dataclasses import dataclass
from math import radians, degrees, atan2, sin, cos

@dataclass
class Target:
    kind: str
    name: str
    lat: float
    lon: float
    alt: float
    heading: float
    speed: float
    visible: bool
    az: float = 0
    el: float = 0

SHARJAH_LAT = 25.3463
SHARJAH_LON = 55.4209

def add_az_el_for_plane(target: Target) -> Target:

    lat1 = radians(SHARJAH_LAT)
    lon1 = radians(SHARJAH_LON)
    lat2 = radians(target.lat)
    lon2 = radians(target.lon)

    dlon = lon2 - lon1 

    x = sin(dlon) * cos(lat2)
    y = cos(lat1) * sin(lat2) - sin(lat1) * cos(lat2) * cos(dlon)
    az = (degrees(atan2(x,y)) + 360 )% 360

    target.az = az
    target.el = 10.0 #PLACEHOLDER

    return target
    