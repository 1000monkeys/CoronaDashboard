import csv

import branca
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
    data_frame = pd.DataFrame(data, columns=['StateCode', 'Confirmed'])
    pd.set_option("display.max_rows", None, "display.max_columns", None)
    print(data_frame)

    colormap = branca.colormap.linear.YlOrRd_09.scale(0, 105000).to_step(6)
    colormap.caption = 'Infected people'
    folium_map.add_child(colormap)

    #  bins = [0, 10, 50, 100, 250, 500, 800, 1000]
    bins = data_frame['Confirmed'].quantile([0, 0.16, 0.32, 0.48, 0.64, 0.80, 1])
    choropleth = folium.Choropleth(
        geo_data="us-states.json",
        name='choropleth',
        bins=bins,
        data=data_frame,
        columns=['StateCode', 'Confirmed'],
        key_on='feature.id',
        fill_opacity=0.7,
        line_opacity=0.2,
        fill_color='YlOrRd',
    )
    for key in choropleth._children:
        if key.startswith('color_map'):
            del(choropleth._children[key])

    choropleth.add_to(folium_map)

    return folium_map._repr_html_()


if __name__ == '__main__':
    app.run(debug=True)
