import pandas as pd
import plotly.express as px
import json

# Load the state-wise crop production data
data = pd.read_csv("state_crop_production.csv")  # Path to your CSV file

# Load the GeoJSON file
geojson_path = "india.json"  # Path to your GeoJSON file
with open(geojson_path, "r") as file:
    geojson_data = json.load(file)  # Correctly load the GeoJSON file

# Create a choropleth map with customized color scale
fig = px.choropleth(
    data,
    geojson=geojson_data,
    featureidkey="properties.st_nm",  # Key in GeoJSON that matches state names
    locations="State_Name",           # Column in data for state names
    color="Pct_Production",           # Data column for coloring
    color_continuous_scale="YlGn",    # Color scale where YlGn is yellow-green, light green -> dark green
    title="State-wise Crop Production in India",
    labels={"Pct_Production": "Production (%)"}
)

# Customize map properties
fig.update_geos(
    fitbounds="locations",  # Ensures the map zooms to your data
    visible=False
)

# Show the map
fig.show()