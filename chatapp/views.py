# chatapp/views.py
import requests
from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings

def index(request):
    return render(request, 'chatapp/index.html')

def search(request):
    query = request.GET.get('query')
    lat = request.GET.get('lat')
    lon = request.GET.get('lon')
    location = f"{lat},{lon}"
    response = search_places(query, location)
    return JsonResponse(response)

def search_places(query, location):
    api_key = settings.GOOGLE_PLACES_API_KEY
    url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={location}&radius=1500&keyword={query}&key={api_key}"
    response = requests.get(url).json()
    
    # Calculate the distance for each place
    for place in response.get('results', []):
        place_location = place['geometry']['location']
        place_lat = place_location['lat']
        place_lon = place_location['lng']
        place['distance'] = haversine(float(location.split(',')[0]), float(location.split(',')[1]), place_lat, place_lon)
    
    return response

def haversine(lat1, lon1, lat2, lon2):
    from math import radians, cos, sin, sqrt, atan2

    R = 6371  # Earth radius in kilometers

    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat / 2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c
    return round(distance, 2)
