import folium
import pandas

#Split txt data into variables
data = pandas.read_csv("Volcanoes.txt")
lat = list(data["LAT"])
lon = list(data["LON"])
elev = list(data["ELEV"])
name = list(data["NAME"])

#Function to color volcano leaflets based on 
#elevation
def color_blimps(elevation):
    if elevation < 1000:
        return 'green'
    elif 1000 <= elevation < 3000:
        return 'orange'
    else:
        return 'red'

#Start position of map
map = folium.Map(location = [37.79648, -99.164589], zoom_start = 5, tiles = "Mapbox Bright")

#HTML to allow users to lookup university & HS
htmlUniv = """
Name:<br>
<a href="https://www.google.com/search?q=%%22%s%%22" target="_blank">%s</a><br><br>
Year Founded: %s 
"""

#My schools feature group
fg = folium.FeatureGroup(name = "University")
fg.add_child(folium.Marker(location = [40.862243, -73.88566], popup= folium.Popup(folium.IFrame(html=htmlUniv % ("Fordham University", "Fordham University", "1841"), width=200, height=100)), icon = folium.Icon(color = 'blue')))
fg.add_child(folium.Marker(location = [40.729938, -73.997374], popup= folium.Popup(folium.IFrame(html=htmlUniv % ("New York University", "New York University", "1831"), width=200, height=100)), icon = folium.Icon(color = 'pink')))

fgHS = folium.FeatureGroup(name = "High School")
fgHS.add_child(folium.Marker(location = [40.734978, -73.821337], popup= folium.Popup(folium.IFrame(html=htmlUniv % ("Townsend Harris High School", "Townsend Harris High School", "1904"), width=200, height=100)), icon = folium.Icon(color = 'black')))

#HTML to allow user to quickly lookup volcano in 
#Google Search
html = """
Volcano name:<br>
<a href="https://www.google.com/search?q=%%22%s%%22%%20volcano" target="_blank">%s</a><br><br>
Height: %s m
"""

#Volcano feature group
fgvol = folium.FeatureGroup(name = "Volcanoes")
for lt, ln, el, nm in zip(lat, lon, elev, name):
    iframe = folium.IFrame(html=html % (nm, nm, el), width=200, height=100)
    fgvol.add_child(folium.Marker(location = [lt, ln], popup= folium.Popup(iframe), icon = folium.Icon(color = color_blimps(el))))

#Population is used to color countries
fgpop = folium.FeatureGroup(name = "Population")
fgpop.add_child(folium.GeoJson(data = open('world.json', 'r', encoding='utf-8-sig').read(),
style_function=lambda x: {'fillColor':'green' if x['properties']['POP2005'] < 15000000
else 'orange' if 15000000 <= x['properties']['POP2005'] < 35000000 else 'red'}))

#Add all feature groups to map, and save
map.add_child(fg)
map.add_child(fgHS)
map.add_child(fgvol)
map.add_child(fgpop)
map.add_child(folium.LayerControl())
map.save("MapView.html")