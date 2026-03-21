import pandas as pd
import geopandas as gpd
from shapely.geometry import Point

def transform_to_geodataframe(csv_path):
    # 1. load the cleaned CSV data into a pandas DataFrame
    df = pd.read_csv(csv_path)
    
    # 2. create 'Point' geometry
    # Note: Longitude always comes first (x-axis), Latitude second (y-axis)
    geometry = [Point(xy) for xy in zip(df['longitude'], df['latitude'])]
    
    # 3. Build the GeoDataFrame and assign the initial CRS (Step 4)
    # We use EPSG:4326 because the USGS API data comes in WGS84
    gdf = gpd.GeoDataFrame(df, geometry=geometry, crs="EPSG:4326")
    
    return gdf

# Execution
gdf_earthquakes = transform_to_geodataframe('../data/earthquakes.csv')

# Technical Validation
print(f"Coordinate System: {gdf_earthquakes.crs}")
print(gdf_earthquakes[['magnitude', 'geometry']].head())