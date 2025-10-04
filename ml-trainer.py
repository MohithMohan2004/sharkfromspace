import os
import argparse
import numpy as np
import pandas as pd
import folium
from tqdm import tqdm
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
from scipy.spatial import cKDTree
import cartopy.feature as cfeature
import matplotlib.path as mpath
from folium.plugins import HeatMap

# -----------------------------
# Heuristic shark probability
# -----------------------------
def compute_shark_probability(row):
    sst_opt = np.exp(-((row["SST_C"] - 24.0) ** 2) / (2 * 3.0 ** 2))
    chlor_opt = np.tanh(row["chlor_a_mg_m3"] / 2.0)
    depth_opt = np.exp(-((row["ocean_depth_m"] - 200) ** 2) / (2 * 500 ** 2))
    curr_opt = np.exp(-((row["current_speed_m_s"] - 0.5) ** 2) / (2 * 0.5 ** 2))
    sal_opt = np.exp(-((row["salinity_psu"] - 35.0) ** 2) / (2 * 2.0 ** 2))
    prob = (sst_opt + chlor_opt + depth_opt + curr_opt + sal_opt) / 5.0
    return prob

# -----------------------------
# Land masking functions
# -----------------------------
def build_land_mask(resolution="110m"):
    land = cfeature.NaturalEarthFeature("physical", "land", resolution)
    polys = list(land.geometries())
    land_paths = []
    for poly in polys:
        if poly.geom_type == "Polygon":
            land_paths.append(mpath.Path(np.asarray(poly.exterior.coords)))
        elif poly.geom_type == "MultiPolygon":
            for subpoly in poly.geoms:
                land_paths.append(mpath.Path(np.asarray(subpoly.exterior.coords)))
    return land_paths

def is_ocean_vectorized(lats, lons, land_paths):
    mask = np.ones(len(lats), dtype=bool)
    for path in tqdm(land_paths, desc="Masking land polygons", unit="poly"):
        points = np.c_[lons, lats]
        inside = path.contains_points(points)
        mask &= ~inside
    return mask

# -----------------------------
# Main function
# -----------------------------
def main():
    parser = argparse.ArgumentParser(description="Shark Probability HeatMap Generator")
    parser.add_argument("--input", "-i", type=str, default="synthetic_ocean_data.csv", help="Input CSV")
    parser.add_argument("--out", "-o", type=str, default="shark_heatmap.html", help="Output map HTML")
    parser.add_argument("--grid_res", type=float, default=0.25, help="Grid resolution in degrees")
    parser.add_argument("--prob_threshold", type=float, default=0.4, help="Shark probability threshold")
    parser.add_argument("--test_size", type=float, default=0.2, help="Test fraction")
    parser.add_argument("--n_est", type=int, default=200, help="RandomForest trees")
    args = parser.parse_args()

    # -----------------------------
    # Load CSV and compute heuristic probability
    # -----------------------------
    print(f"Loading CSV: {args.input}")
    df = pd.read_csv(args.input)

    print("Computing heuristic shark probabilities...")
    tqdm.pandas(desc="Shark heuristic")
    df["shark_prob"] = df.progress_apply(compute_shark_probability, axis=1)

    features = ["SST_C", "chlor_a_mg_m3", "ocean_depth_m", "current_speed_m_s", "salinity_psu"]
    X = df[features]
    y = df["shark_prob"]

    # -----------------------------
    # Train RandomForest
    # -----------------------------
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=args.test_size, random_state=42)
    model = RandomForestRegressor(n_estimators=args.n_est, random_state=42)
    print("Training RandomForestRegressor...")
    model.fit(X_train, y_train)
    preds = model.predict(X_test)
    mse = mean_squared_error(y_test, preds)
    r2 = r2_score(y_test, preds)
    print(f"Test MSE: {mse:.5f} | R^2: {r2:.3f}")

    # -----------------------------
    # Build prediction grid
    # -----------------------------
    print("Building prediction grid...")
    lat_min, lat_max = df["lat"].min(), df["lat"].max()
    lon_min, lon_max = df["lon"].min(), df["lon"].max()
    lats = np.arange(lat_min, lat_max, args.grid_res)
    lons = np.arange(lon_min, lon_max, args.grid_res)
    grid_lat, grid_lon = np.meshgrid(lats, lons)
    grid_df = pd.DataFrame({"lat": grid_lat.ravel(), "lon": grid_lon.ravel()})
    print(f"Grid points before masking: {len(grid_df)}")

    # -----------------------------
    # Mask land points
    # -----------------------------
    print("Masking land points...")
    land_paths = build_land_mask()
    ocean_mask = is_ocean_vectorized(grid_df["lat"].values, grid_df["lon"].values, land_paths)
    grid_df = grid_df[ocean_mask]
    print(f"Grid points after masking (ocean only): {len(grid_df)}")

    # -----------------------------
    # Assign environmental features using KDTree
    # -----------------------------
    print("Assigning environmental features via KDTree...")
    tree = cKDTree(df[["lat", "lon"]].values)
    dists, idxs = tree.query(grid_df[["lat", "lon"]].values, workers=-1)
    X_grid = df[features].iloc[idxs].values

    # Convert to DataFrame to remove feature warning
    X_grid_df = pd.DataFrame(X_grid, columns=features)

    # -----------------------------
    # Predict shark probability
    # -----------------------------
    print("Predicting shark probabilities...")
    grid_df["prob"] = model.predict(X_grid_df)

    # -----------------------------
    # Build interactive HeatMap
    # -----------------------------
    print("Building interactive HeatMap...")
    mask = grid_df["prob"] >= args.prob_threshold
    heat_data = [[lat, lon, prob] for lat, lon, prob in zip(
        grid_df.loc[mask, "lat"], grid_df.loc[mask, "lon"], grid_df.loc[mask, "prob"]
    )]

    # Create 'maps' folder if it doesn't exist
    os.makedirs("maps", exist_ok=True)

    center_lat, center_lon = df["lat"].mean(), df["lon"].mean()
    m = folium.Map(location=[center_lat, center_lon], zoom_start=3, tiles="cartodbpositron")
    HeatMap(heat_data, radius=8, blur=15, max_zoom=6).add_to(m)

    # Save map inside 'maps' folder
    output_path = os.path.join("maps", args.out)
    m.save(output_path)
    print(f"✅ HeatMap saved to {output_path}. File size will be much minimal and interactive!")


if __name__ == "__main__":
    main()
