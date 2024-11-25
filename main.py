import pandas as pd
import plotly.express as px
import json

# Load your CSV file
file_path = "df2013.csv"  # Replace with your CSV file path
data = pd.read_csv(file_path)

# Aggregate data to calculate total pct_production for each state
state_data = data.groupby("State_Name", as_index=False)["pct_production_all_Over_India"].sum()

# Load Indian GeoJSON file
geojson_path = "india.json"  # Replace with your GeoJSON file path
with open(geojson_path, "r") as file:
    india_geojson = json.load(file)

# Extract all state names from the GeoJSON file   # here
geojson_states = [feature["properties"]["st_nm"] for feature in india_geojson["features"]]


# Ensure all states are included in the data
state_data_complete = pd.DataFrame({"State_Name": geojson_states}).merge(
    state_data, on="State_Name", how="left"
)

# Fill missing pct_production values with 0
state_data_complete["pct_production_all_Over_India"] = state_data_complete["pct_production_all_Over_India"].fillna(0)

# Plot the Choropleth map
# Updated Choropleth Map Code with Custom Colors
fig = px.choropleth(
    state_data_complete,
    geojson=india_geojson,
    locations="State_Name",
    featureidkey="properties.st_nm",
    color="pct_production_all_Over_India",
    color_continuous_scale=[
        (0.0, "white"),     # For 0 percent production
        (0.01, "lightblue"),
        (0.5, "blue"),
        (1.0, "darkblue")   # Highest production
    ],
    title="Percentage Production by State in India"
)

# Update map appearance
fig.update_geos(
    fitbounds="locations",
    visible=False,
    projection=dict(scale=1, type="mercator")
)
fig.update_layout(
    title_font_size=18,
    geo=dict(bgcolor="rgba(0,0,0,0)")
)

# Show the map
fig.show()
