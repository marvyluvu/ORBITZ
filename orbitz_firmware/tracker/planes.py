
import math
import requests

from config import (
    PLANES_API_URL,
    PLANES_API_TIMEOUT,
    PLANES_BBOX_DEGREES,
    PLANES_MAX_RANGE_KM,
    PLANES_LOCAL_URL,
    PLANES_LOCAL_TIMEOUT,
)

from tracker.coords import Target

from tracker.location import get_observer

def haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    R = 6371.0
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)

    a = math.sin(dphi / 2.0) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2.0) ** 2
    c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))
    return R * c


def bearing_deg(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    dlambda = math.radians(lon2 - lon1)

    y = math.sin(dlambda) * math.cos(phi2)
    x = math.cos(phi1) * math.sin(phi2) - math.sin(phi1) * math.cos(phi2) * math.cos(dlambda)
    brng = math.degrees(math.atan2(y, x))
    return (brng + 360.0) % 360.0


def _fetch_opensky_states():


    obs = get_observer()

    obs_lat = obs.lat
    obs_lon = obs.lon

    half = PLANES_BBOX_DEGREES
    lamin = obs_lat - half
    lamax = obs_lat + half
    lomin = obs_lon - half
    lomax = obs_lon + half

    params = {
        "lamin": lamin,
        "lamax": lamax,
        "lomin": lomin,
        "lomax": lomax,
    }

    try:
        resp = requests.get(
            PLANES_API_URL,
            params=params,
            timeout=PLANES_API_TIMEOUT,
        )
        resp.raise_for_status()
        data = resp.json()
    except Exception:
        return []

    states = data.get("states") or []
    return states

def _fetch_local_planes():
    try:
        resp = requests.get(
            PLANES_LOCAL_URL,
            timeout=PLANES_LOCAL_TIMEOUT
        )
        resp.raise_for_status()
        data = resp.json()
    except Exception:
        return []
    
    ac_list = data.get("aircraft") or []
    planes = []
    for ac in ac_list:
        lat = ac.get("lat")
        lon = ac.get("lon")
        if lat is None or lon is None:
            continue
        planes.append(
           { "icao24": ac.get("hex"),
            "callsign":(ac.get("flight") or "").strip(),
            "lat":float(lat),
            "lon":float(lon),
            "alt":float(ac.get("alt_geom") or 0.0) * 0.3048, #feet to meters
            "velocity": float(ac.get("gs") or 0.0) * 0.514444, #knots to m/s
            "heading": float(ac.get("track") or 0.0),
            "on_ground": bool(ac.get("on ground",False)),
           }
        )
    return planes


def _states_to_targets(states):

    obs = get_observer()
    obs_lat = obs.lat
    obs_lon = obs.lon

    targets: list[Target] = []

    for s in states:
        if not isinstance(s, list) or len(s) < 11:
            continue

        icao24 = s[0]
        callsign = s[1] or ""
        lon = s[5]
        lat = s[6]
        baro_alt = s[7]
        on_ground = s[8]
        velocity = s[9]
        heading = s[10]

        if lat is None or lon is None:
            continue

        dist_km = haversine_km(obs_lat, obs_lon, lat, lon)
        if dist_km > PLANES_MAX_RANGE_KM:
            continue

        az = bearing_deg(obs_lat, obs_lon, lat, lon)

        if PLANES_MAX_RANGE_KM > 0:
            frac = max(0.0, min(1.0, 1.0 - dist_km / PLANES_MAX_RANGE_KM))
        else:
            frac = 0.5
        el = 5.0 + frac * 55.0

        alt = float(baro_alt) if baro_alt is not None else 0.0
        speed = float(velocity) if velocity is not None else 0.0
        hdg = float(heading) if heading is not None else 0.0

        name = callsign.strip() or icao24 or "plane"

        t = Target(
            kind="plane",
            name=name,
            lat=float(lat),
            lon=float(lon),
            alt=alt,
            heading=hdg,
            speed=speed,
            visible=not bool(on_ground),
            az=az,
            el=el,
        )
        targets.append(t)

    return targets

def get_planes_bbox():
    local_planes = _fetch_local_planes()
    if local_planes:
        obs = get_observer()
        obs_lat = obs.lat
        obs_lon = obs.lon

        targets: list[Target] = []
        for p in local_planes:
            dist_km = haversine_km(obs_lat, obs_lon, p["lat"], p["lon"])
            if dist_km > PLANES_MAX_RANGE_KM:
                continue
            az = bearing_deg(obs_lat, obs_lon, p["lat"], p["lon"])
            if PLANES_MAX_RANGE_KM > 0:
                frac = max(0.0, min(1.0, 1.0 - dist_km / PLANES_MAX_RANGE_KM))
            else:
                frac = 0.5
            el = 5.0 + frac * 55.0

            name = p["callsign"] or p["icao24"] or "plane"

            t = Target(
                kind="plane",
                name=name.strip(),
                lat=float(p["lat"]),
                lon=float(p["lon"]),
                alt=float(p["alt"]),
                heading=float(p["heading"]),
                speed=float(p["velocity"]),
                visible=not bool(p["on_ground"]),
                az=az,
                el=el,
            )
            targets.append(t)
        if targets:
            return targets
    states = _fetch_opensky_states()
    if not states:
        return []
    return _states_to_targets(states)