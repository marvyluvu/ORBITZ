from typing import List
from datetime import datetime, timezone
import requests
from skyfield.api import Loader, EarthSatellite, wgs84
from tracker.coords import Target
from skyfield.api import load


#these coords are based on where I am, Please update if you plan on testing in your location!!

SHARJAH_LAT = 25.3463
SHARJAH_LON = 55.4209
SHARJAH_ELEV = 0 # in meters

load = Loader("./skyfield_data")
ts = load.timescale()
earth = load("de421.bsp")

def _get_iss_satellite() -> EarthSatellite:
    url = "https://celestrak.org/NORAD/elements/gp.php"
    params = {"CATNR": "25544", "FORMAT": "TLE"}
    txt = requests.get(url, params=params, timeout=5).text
    lines = [line.strip() for line in txt.splitlines() if line.strip()]
    name, l1, l2 = lines[0], lines[1], lines[2]
    return EarthSatellite(l1, l2, name, ts)

def get_iss() -> Target:
    sat = _get_iss_satellite()
    t = ts.from_datetime(datetime.now(timezone.utc))
    observer = wgs84.latlon(SHARJAH_LAT, SHARJAH_LON, SHARJAH_ELEV)
    topocentric = (sat - observer).at(t)

    alt, az, distance = topocentric.altaz()
    subpoint = sat.at(t).subpoint()

    lat = subpoint.latitude.degrees
    lon = subpoint.longitude.degrees
    height = subpoint.elevation.m

    visible = alt.degrees > 0
    return Target(
        kind="iss",
        name="ISS",
        lat=lat,
        lon=lon,
        alt=height,
        heading=0.0,
        speed=0.0,
        visible=visible,
        az=az.degrees,
        el=alt.degrees,
    )
def get_next_iss_rise_minutes() -> float | None:

    sat = _get_iss_satellite()
    ts_local = ts

    t0 = ts_local.now()
    t1 = ts_local.tt_jd(t0.tt + 1.0)

    observer = wgs84.latlon(SHARJAH_LAT, SHARJAH_LON, SHARJAH_ELEV)

    times, events = sat.find_events(observer, t0, t1, altitude_degrees=0.0)

    for ti, ev in zip(times,events):
        if ev == 0:
            minutes = (ti.utc_datetime() - t0.utc_datetime()).total_seconds() / 60.0

            return minutes
    return None