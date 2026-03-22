import folium
import geopandas as gpd
import pandas as pd
from folium.plugins import Fullscreen

def get_color(depth):
    """Returns color based on earthquake depth (km)."""
    if depth < 33:
        return '#e41a1c'  # Shallow (Red) - High Risk
    elif depth < 70:
        return '#ff7f00'  # Intermediate (Orange)
    else:
        return '#377eb8'  # Deep (Blue)

def build_interactive_map(data_path, geojson_path, output_path):
    # 1. Load Data
    gdf_sismos = gpd.read_file(data_path) # Assuming your points are ready
    # Convert magnitude to numeric, coercing errors to NaN
    gdf_sismos['magnitude'] = pd.to_numeric(gdf_sismos['magnitude'], errors='coerce')
    # Drop rows with NaN magnitudes if necessary
    gdf_sismos = gdf_sismos.dropna(subset=['magnitude'])
    # Convert depth to numeric, coercing errors to NaN
    gdf_sismos['depth'] = pd.to_numeric(gdf_sismos['depth'], errors='coerce')
    # Drop rows with NaN depths if necessary
    gdf_sismos = gdf_sismos.dropna(subset=['depth'])


    mexico_states = gpd.read_file(geojson_path)
    
    # 2. Initialize Folium Map centered on Mexico
    # We use 'CartoDB positron' for a clean, professional look
    m = folium.Map(
        location=[23.6345, -102.5528], 
        zoom_start=5, 
        tiles='CartoDB positron',
        width='100%',
        height='100%'
    )

    # 3. Add Mexico States Layer (Context)
    folium.GeoJson(
        mexico_states,
        name="Mexico State Boundaries",
        style_function=lambda x: {
            'fillColor': 'transparent',
            'color': '#636363',
            'weight': 1,
            'opacity': 0.5
        }
    ).add_to(m)

    # 4. Add Earthquake Points (Bubble Map)
    for _, row in gdf_sismos.iterrows():
        # Tooltip for hover, Popup for click
        info = f"<b>Magnitude:</b> {row['magnitude']}<br><b>Depth:</b> {row['depth']} km<br><b>Date:</b> {row['date']}"
        
        folium.CircleMarker(
            location=[row['latitude'], row['longitude']],
            radius=row['magnitude'] * 2.5,  # Proportional scaling
            color=get_color(row['depth']),
            fill=True,
            fill_color=get_color(row['depth']),
            fill_opacity=0.7,
            popup=folium.Popup(info, max_width=300),
            tooltip=f"Mag {row['magnitude']}"
        ).add_to(m)

    # 5. Add Map Features
    folium.LayerControl().add_to(m)
    Fullscreen().add_to(m)

    # 6. Save Final HTML
    m.save(output_path)
    print(f"✨ Interactive map successfully generated at: {output_path}")

if __name__ == "__main__":
    # Update these paths to match your project structure
    build_interactive_map(
        '../data/earthquakes.csv', 
        '../data/mexico_states.geojson', 
        '../docs/earthquake_map_mexico.html'
    )