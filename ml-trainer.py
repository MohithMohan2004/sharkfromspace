import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import MinMaxScaler
import folium
from folium import plugins
from shapely.geometry import Point, Polygon, MultiPolygon
from shapely.prepared import prep
import cartopy.feature as cfeature
from shapely.ops import unary_union

# -------------------------
# 1. Load synthetic ocean data
# -------------------------
df = pd.read_csv("synthetic_ocean_data.csv")
features = ['SST_C', 'chlor_a_mg_m3', 'ocean_depth_m', 'current_speed_m_s', 'salinity_psu']

# -------------------------
# 2. Shark probability framework
# -------------------------
scaler = MinMaxScaler()
X_norm = scaler.fit_transform(df[features])
weights = np.array([0.3, 0.2, 0.2, 0.1, 0.2])

# Shallower depth and lower currents = higher probability
depth_norm = 1 - X_norm[:, 2]
current_norm = 1 - X_norm[:, 3]

shark_prob = (
    weights[0]*X_norm[:,0] + 
    weights[1]*X_norm[:,1] + 
    weights[2]*depth_norm + 
    weights[3]*current_norm + 
    weights[4]*X_norm[:,4]
)
shark_prob = shark_prob / shark_prob.max()  # normalize 0-1
df['shark_prob'] = shark_prob

# -------------------------
# 3. Train ML model
# -------------------------
X = df[features]
y = df['shark_prob']
ml_model = RandomForestRegressor(n_estimators=100, random_state=42)
ml_model.fit(X, y)
df['shark_prob_ml'] = ml_model.predict(X)

# -------------------------
# 4. Keep only ocean points (depth > 0)
# -------------------------
ocean_df = df[df['ocean_depth_m'] < 0]  # negative depth underwater

if ocean_df.empty:
    raise ValueError("No ocean points found in the dataset.")

# -------------------------
# 5. Prepare heatmap data
# -------------------------
heat_data = [[row['lat'], row['lon'], row['shark_prob_ml']**1.5] for _, row in ocean_df.iterrows()]

# -------------------------
# 6. Create interactive map
# -------------------------
map_center = [ocean_df['lat'].mean(), ocean_df['lon'].mean()]
m = folium.Map(location=map_center, zoom_start=3, tiles='CartoDB positron')

plugins.HeatMap(
    heat_data,
    min_opacity=0.3,
    radius=25,
    blur=35,
    gradient={0.0: 'green', 0.5: 'yellow', 1.0: 'red'}
).add_to(m)

# -------------------------
# 7. Optional: Hover tooltips for probability
# -------------------------
for point in heat_data:
    lat, lon, prob = point
    folium.CircleMarker(
        location=[lat, lon],
        radius=1,
        color=None,
        fill=False,
        popup=f"Shark Probability: {prob:.2f}"
    ).add_to(m)

# -------------------------
# 8. Save map
# -------------------------
output_file = "interactive_shark_heatmap.html"
m.save(output_file)
print(f"Interactive shark heatmap saved to {output_file}")
