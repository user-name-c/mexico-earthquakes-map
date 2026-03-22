import folium
import geopandas as gpd
import pandas as pd
from folium.plugins import Fullscreen, HeatMap, MarkerCluster
from branca.element import Template, MacroElement

# ─────────────────────────────────────────────
# SYMBOLOGY HELPERS
# ─────────────────────────────────────────────

def get_depth_color(depth):
    """Bivariate color scale for depth (km)."""
    if depth < 33:
        return '#e41a1c'   # Shallow  – Red
    elif depth < 70:
        return '#ff7f00'   # Intermediate – Orange
    elif depth < 150:
        return '#984ea3'   # Upper-mid – Purple
    elif depth < 300:
        return '#377eb8'   # Mid – Blue
    else:
        return '#4daf4a'   # Deep – Green

def get_depth_label(depth):
    if depth < 33:   return "Shallow (<33 km)"
    elif depth < 70: return "Intermediate (33–70 km)"
    elif depth < 150:return "Upper-mid (70–150 km)"
    elif depth < 300:return "Mid (150–300 km)"
    else:            return "Deep (>300 km)"

def get_radius(magnitude):
    """Bivariate size: circle size encodes magnitude."""
    return max(3, magnitude * 3.2)   # floor at 3 px

def get_fill_opacity(depth):
    """Deeper quakes → more transparent (opacity gradient)."""
    if depth < 33:   return 0.85
    elif depth < 70: return 0.75
    elif depth < 150:return 0.65
    elif depth < 300:return 0.50
    else:            return 0.35

# ─────────────────────────────────────────────
# LEGEND HTML (injected as a custom Macro)
# ─────────────────────────────────────────────

LEGEND_HTML = """
{% macro html(this, kwargs) %}
<div id="eq-legend" style="
    position: fixed;
    bottom: 30px; right: 15px;
    z-index: 1000;
    background: rgba(255,255,255,0.93);
    border: 1px solid #ccc;
    border-radius: 8px;
    padding: 14px 18px;
    font-family: 'Segoe UI', sans-serif;
    font-size: 12px;
    box-shadow: 2px 2px 8px rgba(0,0,0,0.2);
    min-width: 200px;
">
  <b style="font-size:13px;">🌎 Earthquake Legend</b>
  <hr style="margin:6px 0;">

  <b>Depth (color)</b><br>
  <span style="color:#e41a1c;">●</span> Shallow &lt;33 km<br>
  <span style="color:#ff7f00;">●</span> Intermediate 33–70 km<br>
  <span style="color:#984ea3;">●</span> Upper-mid 70–150 km<br>
  <span style="color:#377eb8;">●</span> Mid 150–300 km<br>
  <span style="color:#4daf4a;">●</span> Deep &gt;300 km<br>

  <hr style="margin:6px 0;">
  <b>Magnitude (size)</b><br>
  <svg width="120" height="22" style="display:block;margin:4px 0;">
    <circle cx="10"  cy="11" r="4"  fill="#999"/>
    <circle cx="35"  cy="11" r="7"  fill="#999"/>
    <circle cx="65"  cy="11" r="10" fill="#999"/>
    <circle cx="100" cy="11" r="14" fill="#999"/>
    <text x="6"   y="22" font-size="9" fill="#555">M4</text>
    <text x="30"  y="22" font-size="9" fill="#555">M5</text>
    <text x="60"  y="22" font-size="9" fill="#555">M6</text>
    <text x="92"  y="22" font-size="9" fill="#555">M7+</text>
  </svg>

  <hr style="margin:6px 0;">
  <b>Opacity</b> ∝ shallower → more opaque<br>
  <b>Halo outline</b> = depth color<br>
</div>
{% endmacro %}
"""

# ─────────────────────────────────────────────
# FILTER CONTROLS (magnitude + depth sliders)
# ─────────────────────────────────────────────

FILTER_HTML = """
{% macro html(this, kwargs) %}
<div id="eq-filters" style="
    position: fixed;
    top: 60px; left: 15px;
    z-index: 1000;
    background: rgba(255,255,255,0.93);
    border: 1px solid #ccc;
    border-radius: 8px;
    padding: 12px 16px;
    font-family: 'Segoe UI', sans-serif;
    font-size: 12px;
    box-shadow: 2px 2px 8px rgba(0,0,0,0.2);
    min-width: 220px;
">
  <b style="font-size:13px;">🔍 Filter Earthquakes</b>
  <hr style="margin:6px 0;">

  <label>Min Magnitude: <b id="mag-val">0</b></label><br>
  <input id="mag-slider" type="range" min="0" max="9" step="0.1" value="0"
         style="width:100%;"
         oninput="document.getElementById('mag-val').innerText=parseFloat(this.value).toFixed(1); applyFilters();">

  <br><br>
  <label>Max Depth (km): <b id="dep-val">700</b></label><br>
  <input id="dep-slider" type="range" min="0" max="700" step="10" value="700"
         style="width:100%;"
         oninput="document.getElementById('dep-val').innerText=this.value; applyFilters();">

  <br><br>
  <button onclick="resetFilters()"
          style="width:100%;padding:4px;border-radius:4px;border:1px solid #aaa;cursor:pointer;">
    Reset Filters
  </button>
</div>

<script>
function applyFilters() {
    var minMag  = parseFloat(document.getElementById('mag-slider').value);
    var maxDep  = parseFloat(document.getElementById('dep-slider').value);

    // Each CircleMarker is a <path> inside a layerGroup we tagged with data-* attrs
    document.querySelectorAll('.eq-marker').forEach(function(el) {
        var mag = parseFloat(el.dataset.mag);
        var dep = parseFloat(el.dataset.dep);
        el.style.display = (mag >= minMag && dep <= maxDep) ? '' : 'none';
    });
}
function resetFilters() {
    document.getElementById('mag-slider').value = 0;
    document.getElementById('dep-slider').value = 700;
    document.getElementById('mag-val').innerText = '0';
    document.getElementById('dep-val').innerText = '700';
    applyFilters();
}
</script>
{% endmacro %}
"""

# ─────────────────────────────────────────────
# MAIN BUILD FUNCTION
# ─────────────────────────────────────────────

def build_interactive_map(data_path, geojson_path, output_path):

    # 1. Load & clean data
    gdf_sismos = gpd.read_file(data_path)
    gdf_sismos['magnitude'] = pd.to_numeric(gdf_sismos['magnitude'], errors='coerce')
    gdf_sismos['depth']     = pd.to_numeric(gdf_sismos['depth'],     errors='coerce')
    gdf_sismos = gdf_sismos.dropna(subset=['magnitude', 'depth'])

    mexico_states = gpd.read_file(geojson_path)

    # 2. Base map
    m = folium.Map(
        location=[23.6345, -102.5528],
        zoom_start=5,
        tiles='CartoDB positron'
    )

    # ── Extra tile options ──────────────────────────────────────────────────
    folium.TileLayer('CartoDB dark_matter', name='Dark Basemap').add_to(m)
    folium.TileLayer('OpenStreetMap',       name='Street Map').add_to(m)

    # 3. Mexico states boundary
    folium.GeoJson(
        mexico_states,
        name="State Boundaries",
        style_function=lambda x: {
            'fillColor': 'transparent',
            'color': '#636363',
            'weight': 1,
            'opacity': 0.5
        }
    ).add_to(m)

    # 4. Heatmap layer (toggleable) ─────────────────────────────────────────
    heat_data = [
        [row['latitude'], row['longitude'], row['magnitude']]
        for _, row in gdf_sismos.iterrows()
    ]
    HeatMap(
        heat_data,
        name="Density Heatmap (toggle)",
        min_opacity=0.3,
        radius=18,
        blur=20,
        max_zoom=8,
        show=False          # hidden by default; user can enable via LayerControl
    ).add_to(m)

    # 5. Earthquake bubble layer ────────────────────────────────────────────
    eq_group = folium.FeatureGroup(name="Earthquakes", show=True)

    for _, row in gdf_sismos.iterrows():
        color   = get_depth_color(row['depth'])
        radius  = get_radius(row['magnitude'])
        opacity = get_fill_opacity(row['depth'])

        # Rich popup
        mag   = float(row['magnitude'])
        depth = float(row['depth'])
        lat   = float(row['latitude'])
        lon   = float(row['longitude'])
        date  = row.get('date', 'N/A')

        popup_html = f"""
        <div style="font-family:'Segoe UI',sans-serif;font-size:13px;min-width:180px;">
          <b style="font-size:14px;color:{color};">M {mag}</b>
          &nbsp;–&nbsp; {get_depth_label(depth)}<br>
          <hr style="margin:4px 0;">
          📍 <b>Depth:</b> {depth:.1f} km<br>
          🗓 <b>Date:</b> {date}<br>
          🌐 <b>Lat/Lon:</b> {lat:.3f}, {lon:.3f}
        </div>
        """

        # Halo effect: outer ring uses depth color, inner fill slightly lighter
        cm = folium.CircleMarker(
            location=[row['latitude'], row['longitude']],
            radius=radius,
            color=color,            # halo/outline = depth color
            weight=2,               # halo thickness
            fill=True,
            fill_color=color,
            fill_opacity=opacity,   # opacity gradient by depth
            popup=folium.Popup(popup_html, max_width=280),
            tooltip=folium.Tooltip(
                f"<b>M{row['magnitude']}</b> | {row['depth']:.0f} km depth",
                sticky=False
            ),
            # Custom class + data attributes so the JS filter can find markers
            class_name='eq-marker',
        )

        # Inject data-* attributes via element options hack
        cm.options.update({
            'className': 'eq-marker',
        })
        # We embed data attrs via a tiny JS snippet appended per marker
        # (folium doesn't expose data-* natively, so we use a DivIcon trick)
        cm.add_to(eq_group)

    eq_group.add_to(m)

    # 6. Inject custom data-attributes so the JS filters work ───────────────
    #    Build a JS array and mark each SVG path after map renders
    marker_js_rows = []
    for i, (_, row) in enumerate(gdf_sismos.iterrows()):
        marker_js_rows.append(
            f'{{mag:{row["magnitude"]},dep:{row["depth"]:.1f}}}'
        )
    js_array = "[" + ",".join(marker_js_rows) + "]"

    inject_js = f"""
    <script>
    window.addEventListener('load', function() {{
        var data = {js_array};
        var paths = document.querySelectorAll('path.leaflet-interactive');
        // assign sequentially (order matches iteration order)
        var idx = 0;
        paths.forEach(function(p) {{
            if (idx < data.length) {{
                p.classList.add('eq-marker');
                p.dataset.mag = data[idx].mag;
                p.dataset.dep = data[idx].dep;
                idx++;
            }}
        }});
    }});
    </script>
    """

    # 7. Add Legend, Filters, standard controls ─────────────────────────────
    legend  = MacroElement()
    legend._template = Template(LEGEND_HTML)
    m.get_root().add_child(legend)

    filters = MacroElement()
    filters._template = Template(FILTER_HTML)
    m.get_root().add_child(filters)

    folium.LayerControl(collapsed=False).add_to(m)
    Fullscreen().add_to(m)

    # 8. Inject marker-tagging JS into the HTML body ─────────────────────────
    m.get_root().html.add_child(folium.Element(inject_js))

    # 9. Save
    m.save(output_path)
    print(f"✨ Map saved → {output_path}")


if __name__ == "__main__":
    build_interactive_map(
        '../data/earthquakes.csv',
        '../data/mexico_states.geojson',
        '../output/earthquake_map_mexico.html'
    )