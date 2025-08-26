# app/services/horoscope.py
import os
from skyfield.api import Loader, Topos
from skyfield.framelib import ecliptic_frame 
from datetime import datetime
import pytz
import numpy as np

# Define the path to the data directory (absolute path recommended)
DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'data'))

# Ensure the data directory exists
os.makedirs(DATA_DIR, exist_ok=True)

# Use Skyfield's Loader to manage data files and downloads in DATA_DIR
loader = Loader(DATA_DIR)
ts = loader.timescale()
eph = loader('de421.bsp')

# Define the celestial bodies we want to track
# The keys are what Skyfield uses, the values are for our output.
PLANETS = {
    'sun': 'Sun',
    'moon': 'Moon',
    'mercury': 'Mercury',
    'venus': 'Venus',
    'mars': 'Mars',
    'jupiter barycenter': 'Jupiter',
    'saturn barycenter': 'Saturn',
    'uranus barycenter': 'Uranus',
    'neptune barycenter': 'Neptune',
    'pluto barycenter': 'Pluto',
}

def _normalize_degrees(degrees):
    """Normalizes an angle to the range [0, 360)."""
    return degrees % 360

def _calculate_placidus_houses(ramc_degrees, latitude_rad, obliquity_rad):
    """
    Calculates the 12 house cusps using the Placidus system.
    
    Args:
        ramc_degrees (float): Right Ascension of the Midheaven in degrees.
        latitude_rad (float): Geographic latitude in radians.
        obliquity_rad (float): Obliquity of the ecliptic in radians.
        
    Returns:
        list: A list of 12 house cusp longitudes in degrees.
    """
    cusps = [0.0] * 12
    
    # House 10 is the Midheaven (MC)
    mc_longitude = np.degrees(np.arctan2(
        np.sin(np.radians(ramc_degrees)),
        np.cos(np.radians(ramc_degrees)) * np.cos(obliquity_rad)
    ))
    cusps[9] = _normalize_degrees(mc_longitude)

    # House 1 is the Ascendant (ASC)
    asc_longitude = np.degrees(np.arctan2(
        np.cos(np.radians(ramc_degrees)),
        - (np.sin(np.radians(ramc_degrees)) * np.cos(obliquity_rad) + 
           np.tan(latitude_rad) * np.sin(obliquity_rad))
    ))
    cusps[0] = _normalize_degrees(asc_longitude)

    # Cusps for houses 11, 12, 2, 3
    for i, h in zip([10, 11, 1, 2], [11, 12, 2, 3]):
        ao = np.radians(ramc_degrees + 30 * i)
        a = np.arcsin(np.sin(latitude_rad) * np.sin(ao))
        fo = np.arctan(-np.tan(ao) * np.cos(obliquity_rad))
        f = fo + a
        r = np.arctan(np.tan(f) / np.cos(latitude_rad))
        cusp_ra = np.degrees(r)
        if np.degrees(f) < 0: cusp_ra += 180
        if np.degrees(ao) < 90 or np.degrees(ao) > 270: cusp_ra += 180
        
        cusp_lon = np.degrees(np.arctan2(
            np.sin(np.radians(cusp_ra)) * np.cos(obliquity_rad) + np.tan(latitude_rad) * np.sin(obliquity_rad),
            np.cos(np.radians(cusp_ra))
        ))
        cusps[h-1] = _normalize_degrees(cusp_lon)

    # --- CORRECTED LOGIC for Opposite Houses ---
    # The previous loop was buggy and overwrote correct values.
    # This calculates each opposite house cusp individually.
    cusps[3] = _normalize_degrees(cusps[9] + 180)   # Cusp 4 (IC) is opposite Cusp 10 (MC)
    cusps[4] = _normalize_degrees(cusps[10] + 180)  # Cusp 5 is opposite Cusp 11
    cusps[5] = _normalize_degrees(cusps[11] + 180)  # Cusp 6 is opposite Cusp 12
    cusps[6] = _normalize_degrees(cusps[0] + 180)   # Cusp 7 (DSC) is opposite Cusp 1 (ASC)
    cusps[7] = _normalize_degrees(cusps[1] + 180)   # Cusp 8 is opposite Cusp 2
    cusps[8] = _normalize_degrees(cusps[2] + 180)   # Cusp 9 is opposite Cusp 3

    return [round(c, 2) for c in cusps]


def calculate_chart(birth_date, birth_time, birth_timezone, latitude, longitude):
    """
    Calculates the full natal chart data including planetary positions, angles, and houses.
    """
    try:
        # --- 1. Set up Time and Location ---
        local_tz = pytz.timezone(birth_timezone)
        dt_local = local_tz.localize(datetime.strptime(f"{birth_date} {birth_time}", '%Y-%m-%d %H:%M:%S'))
        t = ts.from_datetime(dt_local)
        observer = eph['earth'] + Topos(latitude_degrees=latitude, longitude_degrees=longitude)

        # --- 2. Calculate Planetary Positions ---
        positions = {}
        for body_key, body_name in PLANETS.items():
            planet = eph[body_key]
            astrometric = observer.at(t).observe(planet)
            _, ecliptic_lon, _ = astrometric.ecliptic_latlon()
            positions[body_name] = {
                "longitude": round(_normalize_degrees(ecliptic_lon.degrees), 2)
            }
        
        # --- 3. Calculate Angles and Houses ---
        rotation = ecliptic_frame.rotation_at(t)
        ecliptic_obliquity_rad = np.arctan2(rotation[1, 2], rotation[2, 2])
        
        gast_hours = t.gast
        longitude_hours = longitude / 15.0
        last_hours = gast_hours + longitude_hours
        ramc_degrees = _normalize_degrees(last_hours * 15.0)

        # Calculate house cusps using the new function
        house_cusps = _calculate_placidus_houses(ramc_degrees, np.radians(latitude), ecliptic_obliquity_rad)

        angles = {
            "ascendant": {"longitude": house_cusps[0]},
            "midheaven": {"longitude": house_cusps[9]}
        }

        # --- 4. Combine and Return Results ---
        chart_data = {
            "bodies": positions,
            "angles": angles,
            "houses": house_cusps
        }

        return {"status": "success", "data": chart_data}

    except pytz.UnknownTimeZoneError:
        return {"status": "error", "message": "Invalid timezone specified."}
    except ValueError:
        return {"status": "error", "message": "Invalid date or time format. Use YYYY-MM-DD and HH:MM:SS."}
    except Exception as e:
        return {"status": "error", "message": str(e)}