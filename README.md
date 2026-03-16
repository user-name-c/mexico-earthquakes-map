# Mexico Earthquake Interactive Map 🌍🌋

An end-to-end geospatial data project to visualize seismic activity in Mexico using real-time data from the **USGS Earthquake Hazards Program API**.

This tool transforms raw seismic data into an interactive web-based map, allowing users to analyze spatial distributions, magnitudes, and depths of recent earthquakes.

## 🚀 Project Objectives

* **Data Acquisition:** Fetch live earthquake data (Magnitude, Depth, Coordinates, Date) via REST API.
* **Geospatial Processing:** Convert tabular data into **GeoDataFrames** with proper **Point geometries**.
* **Coordinate Reference Systems (CRS):** Ensure data consistency by projecting to **WGS84 (EPSG:4326)** for web compatibility.
* **Thematic Cartography:** Visualize earthquakes using proportional symbols (Magnitude) and color scales (Depth).
* **Interactivity:** Provide a dynamic user experience with zoom, pan, and informative popups.

## 🛠️ Tech Stack

* **Language:** Python 3.x
* **Data Analysis:** `Pandas`, `NumPy`
* **Geospatial:** `GeoPandas`, `Shapely`
* **Visualization:** `Folium` (Leaflet.js wrapper) or `Plotly`
* **API Integration:** `Requests`

## 📁 Project Structure

```text
mexico-earthquakes-map/
├── data/                   # Raw and processed datasets (CSV, SHP)
├── notebooks/              # Jupyter Notebooks for EDA (exploration.ipynb)
├── src/                    # Modular Python scripts
│   ├── load_data.py        # API requests and data fetching
│   ├── process_data.py     # GeoDataFrame creation and CRS handling
│   └── build_map.py        # Map generation and styling
├── output/                 # Final interactive HTML maps
├── README.md
└── requirements.txt        # Project dependencies

```

## 🗺️ Key Features

1. **Live Data:** Connects directly to the USGS API to ensure the map reflects recent events.
2. **Interactive Popups:** Detailed information (Date, Magnitude, Depth) available on click.
3. **Base Map Layers:** Toggle between OpenStreetMap, CartoDB Positron, and Satellite views.
4. **Spatial Filtering:** Focused specifically on the Mexican tectonic region using bounding box coordinates.

## 🔧 Installation & Usage

1. **Clone the repository:**
```bash
git clone https://github.com/your-username/mexico-earthquakes-map.git

```


2. **Install dependencies:**
```bash
pip install -r requirements.txt

```


3. **Run the pipeline:**
```bash
python src/load_data.py
python src/build_map.py

```


4. **View the result:**
Open `output/earthquake_map_mexico.html` in any web browser.
