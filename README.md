# Mexico Earthquake Interactive Map 🌍🌋

[![Live Demo](https://img.shields.io/badge/Live%20Demo-GitHub%20Pages-blue)](https://user-name-c.github.io/mexico-earthquakes-map/)
[![Python](https://img.shields.io/badge/Python-3.x-green)](https://www.python.org/)
[![GeoPandas](https://img.shields.io/badge/GeoPandas-Geospatial-orange)](https://geopandas.org/)

An end-to-end geospatial data project that transforms raw seismic data from the **USGS Earthquake Hazards Program API** into a fully interactive, deployable web application. This project demonstrates the complete data pipeline—from API ingestion to production-ready deployment—showcasing both geospatial analysis expertise and modern web deployment practices.

## 🌐 Live Demo

**Explore the interactive map:** [https://user-name-c.github.io/mexico-earthquakes-map/](https://user-name-c.github.io/mexico-earthquakes-map/)

The live application features:
- Real-time earthquake filtering by magnitude and depth
- Interactive zoom, pan, and popup information
- Dynamic statistics updates as filters change
- Multiple basemap layers for different contexts

## 📊 Preliminary Map Visualization

![Preliminary Exploration Map](https://raw.githubusercontent.com/user-name-c/mexico-earthquakes-map/main/docs/preliminary_exploration.png)

*Figure 1: Preliminary visualization of seismic activity in Mexico showing earthquake distribution, magnitude (bubble size), and depth (color scale).*

## 🚀 Project Objectives

- **Data Acquisition:** Fetch live earthquake data (Magnitude, Depth, Coordinates, Date) via REST API
- **Geospatial Processing:** Convert tabular data into **GeoDataFrames** with proper **Point geometries**
- **Coordinate Reference Systems (CRS):** Ensure data consistency by projecting to **WGS84 (EPSG:4326)** for web compatibility
- **Thematic Cartography:** Visualize earthquakes using proportional symbols (Magnitude) and color scales (Depth)
- **Interactive Web Interface:** Build a responsive dashboard with dynamic filtering and real-time statistics
- **Production Deployment:** Deploy to **GitHub Pages** with automated static site serving

## 🛠️ Tech Stack

### Data Processing & Analysis
- **Language:** Python 3.x
- **Data Analysis:** `Pandas`, `NumPy`
- **Geospatial:** `GeoPandas`, `Shapely`
- **API Integration:** `Requests`

### Visualization & Frontend
- **Mapping Library:** `Folium` (Leaflet.js wrapper)
- **Frontend:** HTML5, CSS3, Vanilla JavaScript
- **Styling:** Custom CSS with responsive design
- **Deployment:** GitHub Pages (served from `/docs`)

## 📁 Project Structure

```text
mexico-earthquakes-map/
├── data/                   # Raw and processed datasets (CSV, SHP)
├── notebooks/              # Jupyter Notebooks for EDA (exploration.ipynb)
├── src/                    # Modular Python scripts
│   ├── load_data.py        # API requests and data fetching
│   ├── process_data.py     # GeoDataFrame creation and CRS handling
│   └── build_map.py        # Map generation and styling
├── docs/                   # 📦 DEPLOYMENT FOLDER - GitHub Pages root
│   ├── earthquake_map_mexico.html  # Generated interactive map
│   ├── index.html                 # Dashboard wrapper with filters
│   ├── preliminary_exploration.png # Static map preview
│   └── (other static assets)
├── README.md
└── requirements.txt        # Project dependencies
```

## 🗺️ Interactive Features

The deployed web application includes:

1. **Live Data Integration:** Connects directly to the USGS API for recent seismic events
2. **Interactive Popups:** Detailed earthquake information (Date, Magnitude, Depth) on click
3. **Dynamic Filtering:**
   - **Magnitude slider:** Filter events by minimum magnitude (0-9)
   - **Depth slider:** Filter events by maximum depth (0-700km)
   - **Real-time statistics:** Instant updates showing total/visible events, max/avg magnitude
4. **Visual Encoding:**
   - **Circle size** = Earthquake magnitude
   - **Circle color** = Depth (Red: <33km, Orange: 33-70km, Blue: >70km)
5. **Base Map Layers:** Toggle between OpenStreetMap, CartoDB Positron, and Satellite views
6. **Responsive Layout:** Fixed sidebar with controls, full-width map display

## 🔧 Installation & Local Development

1. **Clone the repository:**
```bash
git clone https://github.com/user-name-c/mexico-earthquakes-map.git
cd mexico-earthquakes-map
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Run the data pipeline:**
```bash
python src/load_data.py      # Fetch earthquake data from USGS API
python src/process_data.py   # Process into GeoDataFrame
python src/build_map.py      # Generate interactive map
```

4. **View locally:**
```bash
# Navigate to the docs folder
cd docs

# Start a local server
python -m http.server 8000

# Open your browser to http://localhost:8000
```

## 🚢 Deployment to GitHub Pages

This project is configured for automatic deployment via GitHub Pages:

1. **Output Configuration:** All generated files are saved to the `/docs` folder
2. **GitHub Pages Setup:** Repository settings → Pages → Source: "Deploy from main branch" → Folder: "/docs"
3. **Automatic Updates:** Any new map generation (via `build_map.py`) updates the live site on next push

### Why This Deployment Strategy Matters

This deployment approach demonstrates **production-ready technical skills**:

- **Repository Structure:** Clean separation of source code (`/src`), data (`/data`), and deployment artifacts (`/docs`)
- **Automation:** Python scripts generate deployable static assets, eliminating manual HTML editing
- **CI/CD Ready:** The `/docs` convention aligns with GitHub Pages, enabling future automation with GitHub Actions
- **Professional Presentation:** Interactive web application showcases data insights through a custom interface, not just static notebooks

## 📈 Project Impact & Skills Demonstrated

By completing this project, I demonstrate:

- **End-to-End Data Pipeline:** From API ingestion → geospatial processing → interactive visualization → production deployment
- **Geospatial Analysis:** Working with GeoPandas, CRS projections, and spatial data structures
- **Web Development:** Building responsive interfaces with HTML/CSS/JavaScript that communicate with embedded maps
- **Git & Deployment:** Version control best practices and static site deployment via GitHub Pages
- **Technical Communication:** Translating complex geospatial data into accessible, interactive visualizations

## 📚 Future Enhancements

- [ ] Add time-series animation to show earthquake progression over time
- [ ] Integrate tectonic plate boundaries layer
- [ ] Add population density overlay for risk assessment
- [ ] Implement historical earthquake data comparison
- [ ] Add export functionality for filtered datasets

## 📄 License

This project is open-source and available under the MIT License.

## 🙏 Acknowledgments

- Data provided by the [USGS Earthquake Hazards Program](https://earthquake.usgs.gov/earthquakes/feed/v1.0/geojson.php)
- Built with [Folium](https://python-visualization.github.io/folium/) and [Leaflet.js](https://leafletjs.com/)
```
