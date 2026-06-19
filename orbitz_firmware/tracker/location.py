from dataclasses import dataclass
from typing import Optional
from config import OBSERVER_LAT, OBSERVER_LON, OBSERVER_ELEV

try:
    import gpsd
    GPSD_AVAILABLE =True 

except ImportError:
    GPSD_AVAILABLE = False

@dataclass

class Observer:
    lat: float
    lon: float
    elev: float

def _get_observer_from_config() -> Observer:
    return Observer(OBSERVER_LAT, OBSERVER_LON, OBSERVER_ELEV)

def _get_observer_from_gpsd() -> Optional[Observer]:
    if not GPSD_AVAILABLE:
        return None
    
    try: 
        gpsd.connect()
        packet = gpsd.get_current()
        lat = getattr(packet, "lat", None)
        lon = getattr(packet, "lon", None)
        alt = getattr(packet, "alt", None)

        if lat is None or lon is None:
            return None
        
        if alt is None:
            elev = OBSERVER_ELEV
        else:
            elev = float(alt)
        
        return Observer(float(lat), float(lon), elev)
    except Exception:
        return None

def get_observer() -> Observer:
    #PRIMARY : GPS VIA GPSD
    #FALLBACK: STATIC CONFIG COORDS
    obs = _get_observer_from_gpsd()
    if obs is not None:
        return obs
    return _get_observer_from_config()

