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

    states = {}
    with open('covid-19-dataset-1.csv') as f:
        reader = csv.reader(f)
        next(reader)  # skip the first line with the column heads

        for row in reader:
            state_name = row[2]
            confirmed = int(row[7])

            if state_name in us_state_abbrev.keys():
                if state_name in states:
                    states[us_state_abbrev[state_name]] += confirmed
                else:
                    states[us_state_abbrev[state_name]] = confirmed

    data = {
        'StateCode': states.keys(),
        'Confirmed': states.values()
    }

    data_frame = pd.DataFrame(data, columns=['StateCode', 'Confirmed'])
    pd.set_option("display.max_rows", None, "display.max_columns", None)
    print(data_frame)

    folium.Choropleth(
        geo_data="us-states.json",
        name='choropleth',
        data=data_frame,
        columns=['StateCode', 'Confirmed'],
        key_on='feature.properties.name',
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name='Infected people'
    ).add_to(folium_map)

    return folium_map._repr_html_()


if __name__ == '__main__':
    app.run(debug=True)

"""
@app.route('/')
def index():
    start_coords = (45.5236, -122.6750)
    folium_map = folium.Map(location=start_coords, zoom_start=10)

    data = list()
    first_line = True
    with open('covid-19-dataset-1.csv') as f:
        reader = csv.reader(f)
        for row in reader:
            if first_line:
                first_line = False
            else:
                lat = row[5]
                long = row[6]
                count = row[7]

                if len(lat) > 0 and len(long) > 0:
                    i = 0
                    while int(count) > i:
                        lat = float(lat)
                        long = float(long)
                        data.append([lat, long])
                        i += 1

    hm = plugins.HeatMap(data)
    folium_map.add_child(hm)

    return folium_map._repr_html_()


if __name__ == '__main__':
    app.run(debug=True)
"""
