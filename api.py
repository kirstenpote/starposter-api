from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from skyfield.api import load, wgs84

app = FastAPI()

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with your domain for tighter security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

planets = load('de421.bsp')
earth = planets['earth']
ts = load.timescale()

@app.get("/sky")
def get_sky(year:int, month:int, day:int, hour:int, minute:int, lat:float, 
lon:float):
    location = earth + wgs84.latlon(lat, lon)
    t = ts.utc(year, month, day, hour, minute)
    mars = planets['mars']

    astrometric = location.at(t).observe(mars)
    alt, az, distance = astrometric.apparent().altaz()

    return {
        "mars": {
            "altitude": alt.degrees,
            "azimuth": az.degrees,
            "distance_au": distance.au
        }
    }

