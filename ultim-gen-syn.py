import pandas as pd
import numpy as np
import cartopy.feature as cfeature
from shapely.geometry import Point, Polygon, MultiPolygon
from shapely.prepared import prep
from shapely.ops import unary_union

# -------------------------
# Configuration
# -------------------------
OUTPUT_FILE = "synthetic_ocean_data_ocean_only.csv"
NUM_POINTS = 1000  # number of synthetic rows

# -------------------------
# Load land geometries from Natural Earth
# -------------------------
land_feature = cfeature.NaturalEarthFeature('physical', 'land', '110m')
land_polygons = [geom for geom in land_feature.geometries() if isinstance(geom, (Polygon, MultiPolygon))]
merged_land = prep(unary_union(land_polygons))

# -------------------------
# Function to check if a point is on land
# -------------------------
def is_land(lat, lon):
    return merged_land.contains(Point(lon, lat))

# -------------------------
# Generate ocean-only coordinates
# -------------------------
lats, lons = [], []
while len(lats) < NUM_POINTS:
    lat = np.random.uniform(-90, 90)
    lon = np.random.uniform(-180, 180)
    if not is_land(lat, lon):
        lats.append(lat)
        lons.append(lon)

lats = np.array(lats)
lons = np.array(lons)

# -------------------------
# Generate synthetic ocean parameters
# -------------------------
sst = np.random.uniform(-2, 35, NUM_POINTS)           # Sea Surface Temperature (°C)
chlor_a = np.random.uniform(0.01, 30, NUM_POINTS)     # Chlorophyll-a (mg/m³)
depth = np.random.uniform(-11000, -1, NUM_POINTS)     # Ocean Depth (m)
current_speed = np.random.uniform(0, 3, NUM_POINTS)   # Surface Current (m/s)
salinity = np.random.uniform(30, 40, NUM_POINTS)      # Salinity (PSU)

# -------------------------
# Combine into DataFrame
# -------------------------
df = pd.DataFrame({
    "lat": lats,
    "lon": lons,
    "SST_C": sst,
    "chlor_a_mg_m3": chlor_a,
    "ocean_depth_m": depth,
    "current_speed_m_s": current_speed,
    "salinity_psu": salinity
})

# -------------------------
# Save to CSV
# -------------------------
df.to_csv(OUTPUT_FILE, index=False)
print(f"Synthetic ocean data saved to {OUTPUT_FILE}")
