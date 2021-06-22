import json
import requests


request = requests.get("https://nominatim.openstreetmap.org/search.php?q=Montpellier%20France&polygon_geojson=1&format=jsonv2")
stt = request.status_code
header = request.headers['content-type']
encode = request.encoding
json = request.json()
if stt==200:
    head = '{"type": "FeatureCollection", "features": [{"type": "Feature","properties":'+ '{'+'}'+',"geometry": {"type": "Polygon","coordinates": ['
    fin  = ']'+'}'+'}'+']'+'}'
    geo_js_txt = head + str(json[0]['geojson']['coordinates'][0]) +fin
    geo_js_sql = str(json[0]['geojson'])
    print(geo_js_sql)
    geo_js = open("montpellier.geojson", "w")
    geo_js.write(geo_js_txt)
    geo_js.close()