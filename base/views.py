from tokenize import cookie_re
from django.shortcuts import render

from ipaddress import IPv4Address

import geocoder
import folium
import requests
import json

# Create your views here.
def index(request):

    def get_data_from_api(lat,long):
        try:
            API_KEY = '3f1f05b69ed84d6aa3d083bdd7af1827'
            URL = f"https://api.opencagedata.com/geocode/v1/json?q={lat}+{long}&key={API_KEY}"
            response = requests.get(URL, timeout=(5,10)).text
            data =json.loads(response)
            address_coordinates = data['results'][0]['bounds']
            address_components = data['results'][0]['components']
            continent = address_components['continent']
            country =address_components['country']
            country_code = address_components['country_code']
            #region = address_components['region']
            road = address_components['road']
            state = address_components['state']

            map = folium.Map(coordinates, zoom_start = 10)
            folium.Marker(coordinates).add_to(map)
            folium.raster_layers.TileLayer('Stamen Terrain').add_to(map)
            folium.raster_layers.TileLayer('Stamen Toner').add_to(map)
            folium.raster_layers.TileLayer('Stamen Watercolor').add_to(map)
            folium.LayerControl().add_to(map)
            map = map._repr_html_()

            data = {
                'continent':continent,
                    'country':country,
                    'road':road,
                    'state' : state,
                    'ip_address':ip_addr,
                    'lat' :address_coordinates['northeast']['lat'],
                    'lng':address_coordinates['northeast']['lng'],
                    'map':map,
                }
            return data
        except Exception:
            map = folium.Map([0,0])
            map = map._repr_html_()
            data = {
                'error':'Connection/Timeout error',
                'map':map
                }
            return data

    ip_addr = request.GET.get('ip_address')
    data = {}

    if ip_addr:
        g= geocoder.ip(ip_addr, timeout=5)
        coordinates = g.latlng
        lat = coordinates[0]
        long = coordinates[1]

        data = get_data_from_api(lat,long)


       
    
    else:
        try:
            client_ip =requests.get('https://api.ipify.org').text
            g= geocoder.ip("me", timeout=5)
            coordinates = g.latlng
            lat = coordinates[0]
            long = coordinates[1]
            
            API_KEY = '3f1f05b69ed84d6aa3d083bdd7af1827'
            URL = f"https://api.opencagedata.com/geocode/v1/json?q={lat}+{long}&key={API_KEY}"
            response = requests.get(URL, timeout=(5,10)).text
            data =json.loads(response)
            address_coordinates = data['results'][0]['bounds']
            address_components = data['results'][0]['components']
            continent = address_components['continent']
            country =address_components['country']
            country_code = address_components['country_code']
            #region = address_components['region']
            road = address_components['road']
            state = address_components['state']

            map = folium.Map(coordinates, zoom_start = 10)
            folium.Marker(coordinates, popup=state).add_to(map)
            folium.raster_layers.TileLayer('Stamen Terrain').add_to(map)
            folium.raster_layers.TileLayer('Stamen Toner').add_to(map)
            folium.raster_layers.TileLayer('Stamen Watercolor').add_to(map)
            folium.LayerControl().add_to(map)
            map = map._repr_html_()
            print('success')

            data = {
                'continent':continent,
                    'country':country,
                    'road':road,
                    'state' : state,
                    'lat' :address_coordinates['northeast']['lat'],
                    'lng':address_coordinates['northeast']['lng'],
                    'client_ip':client_ip,
                    'map':map,
                    
                    
                    
                }
        except Exception:
            map = folium.Map([0,0])
            map = map._repr_html_()
            data = {
                'error':'Connection/Timeout error',
                'map':map
                }
           

        
              

               
   
   

    return render(request, 'base/index.html', data)
    

  
    
                

    
    
    

    
    
