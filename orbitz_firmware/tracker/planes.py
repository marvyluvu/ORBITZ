import requests
from typing import List
from tracker.coords import Target, add_az_el_for_plane

LAT_MIN, LAT_MAX = 24.0, 26.0
LON_MIN, LON_MAX = 54.0, 56.0

def get_planes_bbox() -> List[Target]:
    url = "https://opensky-network.org/api/states/all"
    params = {
        "lamin": LAT_MIN,
        "lamax": LAT_MAX,
        "lomin": LON_MIN,
        "lomax": LON_MAX,

    }
    resp = requests.get(url, params=params, timeout=5) 
    resp.raise_for_status()
    data = resp.json()

    states = data.get("states") or []
    targets: List[Target] = []

    for s in states:
        icao24 = s[0] or ""
        callsign = (s[1] or "").strip() or icao24
        lat = s[6]
        lon = s[5]
        alt = s[7] or 0.0
        vel = s[9] or 0.0
        heading = s[10] or 0.0

        if lat is None or lon is None:
            continue
        
        t = Target(
            kind="plane",
            name=callsign,
            lat=lat,
            lon=lon,   
            alt=float(alt),
            heading=float(heading),
            speed=float(vel),
            visible=True,
        )
        add_az_el_for_plane(t)
        targets.append(t)
    return targets