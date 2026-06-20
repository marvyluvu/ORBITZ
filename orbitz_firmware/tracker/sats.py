from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import List, Optional

import requests
from skyfield.api import Loader, EarthSatellite, wgs84

from tracker.coords import Target
from tracker.location import get_observer


DATA_DIR = Path("skyfield_data")
TLE_DIR = Path("data")
TLE_FILE = TLE_DIR / "sats.tle"

loader = Loader(str(DATA_DIR))
ts = loader.timescale()

_iss_cache: Optional[EarthSatellite] = None
_all_sats: Optional[List[EarthSatellite]] = None


def _load_all_sats() -> List[EarthSatellite]:
    global _all_sats
    if _all_sats is not None:
        return _all_sats

    sats: List[EarthSatellite] = []
    if TLE_FILE.exists():
        lines = [
            line.strip()
            for line in TLE_FILE.read_text().splitlines()
            if line.strip()
        ]
        for i in range(0, len(lines), 3):
            try:
                name = lines[i]
                line1 = lines[i + 1]
                line2 = lines[i + 2]
            except IndexError:
                break
            sats.append(EarthSatellite(line1, line2, name, ts))
    _all_sats = sats
    return sats


def _get_iss_satellite() -> EarthSatellite:
    global _iss_cache
    if _iss_cache is not None:
        return _iss_cache

    url = "https://celestrak.org/NORAD/elements/gp.php"
    params = {"CATNR": "25544", "FORMAT": "TLE"}

    try:
        txt = requests.get(url, params=params, timeout=3).text
        lines = [line.strip() for line in txt.splitlines() if line.strip()]
        name = lines[0]
        line1 = lines[1]
        line2 = lines[2]
        _iss_cache = EarthSatellite(line1, line2, name, ts)
        return _iss_cache
    except Exception:
        sats = _load_all_sats()
        for sat in sats:
            if "ISS" in sat.name: # type: ignore
                _iss_cache = sat
                return _iss_cache
        raise


def get_iss() -> Target:
    sat = _get_iss_satellite()
    t = ts.from_datetime(datetime.now(timezone.utc))

    obs = get_observer()
    observer = wgs84.latlon(obs.lat, obs.lon, obs.elev)

    topocentric = (sat - observer).at(t)
    alt, az, distance = topocentric.altaz()

    subpoint = sat.at(t).subpoint() # type: ignore
    lat = subpoint.latitude.degrees
    lon = subpoint.longitude.degrees
    height = subpoint.elevation.m

    visible = alt.degrees > 0.0 # type: ignore

    return Target(
        kind="iss",
        name="ISS",
        lat=float(lat), # type: ignore
        lon=float(lon), # type: ignore
        alt=float(height), # type: ignore
        heading=0.0,
        speed=0.0,
        visible=visible,
        az=float(az.degrees), # type: ignore
        el=float(alt.degrees), # type: ignore
    )


def get_next_iss_rise_minutes() -> float | None:
    try:
        sat = _get_iss_satellite()
    except Exception:
        return None

    t0 = ts.now()
    t1 = ts.tt_jd(t0.tt + 1.0)

    obs = get_observer()
    observer = wgs84.latlon(obs.lat, obs.lon, obs.elev)

    times, events = sat.find_events(observer, t0, t1, altitude_degrees=0.0)
    for ti, ev in zip(times, events):
        if ev == 0:
            minutes = (
                ti.utc_datetime() - t0.utc_datetime()
            ).total_seconds() / 60.0
            return float(minutes)
    return None


def get_visible_sat_targets(min_el_deg: float = 10.0) -> List[Target]:
    sats = _load_all_sats()
    if not sats:
        return []

    obs = get_observer()
    observer = wgs84.latlon(obs.lat, obs.lon, obs.elev)
    t = ts.from_datetime(datetime.now(timezone.utc))

    targets: List[Target] = []

    for sat in sats:
        topocentric = (sat - observer).at(t)
        alt, az, distance = topocentric.altaz()

        if alt.degrees < min_el_deg: # type: ignore
            continue

        subpoint = sat.at(t).subpoint() # type: ignore
        lat = subpoint.latitude.degrees
        lon = subpoint.longitude.degrees
        height = subpoint.elevation.m

        targets.append(
            Target(
                kind="sat",
                name=sat.name.strip(), # type: ignore
                lat=float(lat), # type: ignore
                lon=float(lon), # type: ignore
                alt=float(height), # type: ignore
                heading=0.0,
                speed=0.0,
                visible=True,
                az=float(az.degrees), # type: ignore
                el=float(alt.degrees), # type: ignore
            )
        )

    return targets