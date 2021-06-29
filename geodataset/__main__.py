import os
import shutil
from datetime import datetime

import dotenv
import geojson
import numpy as np
import pandas as pd
import requests
import shapely.geometry
from furl import furl
from tqdm import tqdm

print("Configuring")

dotenv.load_dotenv()
API_KEY = os.environ["API_KEY"]

x_n = 50
y_n = 100

geojson_source_filepath = "assets/france.json"

print("Building grid")

with open(geojson_source_filepath) as f:
    geojson_data = geojson.load(f)

shape = shapely.geometry.shape(geojson_data["features"][0]["geometry"])

x_min, y_min, x_max, y_max = shape.bounds

points = np.array(
    [
        [x, y]
        for x in np.linspace(x_min, x_max, x_n)
        for y in np.linspace(y_min, y_max, y_n)
        if shape.contains(shapely.geometry.Point(x, y))
    ]
)

print("Starting extraction")

API_URL = "https://maps.googleapis.com/maps/api/streetview"

extract_datetime = datetime.utcnow()
extract_folder_path = os.path.join(
    "extract",
    extract_datetime.strftime("%Y%M%d%H%m"),
)
os.makedirs(extract_folder_path, exist_ok=True)

records = []
for i, (x, y) in tqdm(list(enumerate(points.tolist()))):
    url = furl(API_URL)
    url.set(
        {
            "size": "400x400",
            "location": f"{y},{x}",
            # to the NORTH
            "heading": 0,
            # radius to look for a picture, in m
            "radius": 100,
            "key": API_KEY,
            "return_error_code": "true",
        }
    )

    r = requests.get(str(url), stream=True)
    if r.status_code == 200:
        filename = f"{i}.png"
        filepath = os.path.join(extract_folder_path, filename)
        with open(filepath, "wb") as f:  # type: ignore
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)

        records.append({"x": x, "y": y, "filename": filename})

df = pd.DataFrame(records)
df.to_csv(os.path.join(extract_folder_path, "df.csv"))
