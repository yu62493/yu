import geocoder
import folium

x = geocoder.google('燁聯鋼鐵')
print(x.latlng)
fmap = folium.Map(location=x.latlng ,zoom_start=16)
fmap.add_child(folium.Marker(location=x.latlng,popup='燁聯鋼鐵'))
fmap.save('map.html')
