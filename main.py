import csv

import folium
import pandas as pd
from abbreviations import us_state_abbrev
from flask import Flask

app = Flask(__name__)


@app.route('/')
def index():
    start_coords = (45.5236, -122.6750)
    folium_map = folium.Map(location=start_coords, zoom_start=3)

    data = pd.read_csv("data-edited.csv")
    print(data)
    data_frame = pd.DataFrame(data, columns=['StateCode', 'Confirmed'])
    pd.set_option("display.max_rows", None, "display.max_columns", None)
    print(data_frame)

    #  bins = [0, 10, 50, 100, 250, 500, 800, 1000]
    bins = data_frame['Confirmed'].quantile([0, 0.05, 0.1, 0.4, 0.8, 1])
    folium.Choropleth(
        geo_data="us-states.json",
        name='choropleth',
        bins=bins,
        data=data_frame,
        columns=['StateCode', 'Confirmed'],
        key_on='feature.id',
        fill_opacity=0.7,
        line_opacity=0.2,
        fill_color='YlOrRd',
        legend_name='Infected people'
    ).add_to(folium_map)

    folium.LayerControl().add_to(folium_map)

    return folium_map._repr_html_()


if __name__ == '__main__':
    app.run(debug=True)
