# coding: utf-8

# ### Convert csv data to geojson.
#
# Thanks to https://gist.github.com/Spaxe/94e130c73a1b835d3c30ea672ec7e5fe

import pandas
import json

data_in = pandas.read_csv("../data/italy_v01.csv",index_col=0,header=0,sep='\s+')
data_in.T.plot()

latlon = pandas.read_csv("../data/italy_latlon.csv",index_col=0,header=0,sep='\s+')
latlon

data_joined = pandas.concat([latlon, data_in], axis=1, join='inner')

json_result_string = data_joined.to_json(
    orient='index',
    double_precision=12,
    date_format='iso'
)
json_result = json.loads(json_result_string)

data_joined = pandas.concat([latlon, data_in], axis=1, join='inner')

json_result_string = data_joined.to_json(
    orient='index',
    double_precision=12,
    date_format='iso'
)
json_result = json.loads(json_result_string)

geojson = {
    'type': 'FeatureCollection',
    'features': []
}

for name,data in json_result.copy().iteritems():

    lon, lat = data.pop('lon'), data.pop('lat')

    properties = data
    properties["lon"] = lon
    properties["lat"] = lat
    properties["name"] = name

    geojson['features'].append({
        'type': 'Feature',
        'geometry': {
            'type': 'Point',
            'coordinates': [lon, lat],
        },
        'properties': properties
    })

with open('../data/italy_v01.json', 'w') as f:
    f.write(json.dumps(geojson, indent=2, sort_keys=True))

