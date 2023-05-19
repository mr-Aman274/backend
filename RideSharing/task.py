import requests

from rest_framework.decorators import api_view
from rest_framework.response import Response
from math import radians, cos, sin, asin, sqrt

from .serializer import rideInfoSerializer
from .models import rideInfo


def haversine_distance(lat1, lon1, lat2, lon2):
    R = 6372.8 # Earth radius in kilometers
    
    # Convert latitudes and longitudes from degrees to radians
    d_lat = radians(lat2 - lat1)
    d_lon = radians(lon2 - lon1)
    lat1 = radians(lat1)
    lat2 = radians(lat2)
    
    # Apply haversine formula
    a = sin(d_lat/2)**2 + cos(lat1)*cos(lat2)*sin(d_lon/2)**2
    c = 2*asin(sqrt(a))
    return R*c

# {"destination": {"lat": 27.6999738, "lng": 85.2890594}, "destinationName": "Kalanki, Kathmandu 44600, Nepal",
#  "origin": {"lat": 27.6931052, "lng": 85.28065389999999}, "originName": "Kalimati, Kathmandu 44600, Nepal",
# }

@api_view(['POST'])
def matchUsers(request):
    data = request.data
    # Get current user's location from request
    destinationName = data['destinationName']
    print("Destination name ", destinationName)

    # Get district name from destination name
    district = destinationName.split(',')[-2]
    print(district)
    print("-----------------district----------------")
    try:
        district = district.split(" ")[-2]
        print("district", district)
    except:
        pass

    user_destination, user_origin = data['destination'], data['origin']

    # Get all users except current user
    all_users = rideInfo.objects.filter(rideType="offer")
    riders = all_users.filter(destinationName__contains=district)
    print("riders", riders)
    
    # Calculate distances between current user and all other users
    rider_origin_destination = [] # (rider, origin, destination)
    try:
        for rider in riders:
            serializer = rideInfoSerializer(rider, many=False)
            data = serializer.data
            print(data)
            distance_origin = haversine_distance(user_origin['lat'], user_origin['lng'], data['origin']['lat'], data['origin']['lng'])
            
            distance_destination = haversine_distance(user_destination['lat'], user_destination['lng'], data['destination']['lat'], data['destination']['lng'])
            rider_origin_destination.append((rider, distance_origin, distance_destination))
    except Exception as e:
        print(e)
        return Response({
            "message": "No rider found",
            "response" : True

        }, status=200)
    # Sort users by distance
    rider_origin_destination.sort(key=lambda x: x[1] + x[2])
    
    #{(ram, 1km, 3km), (hari, 2km, 200m), (gita, 3km, 1km)...} --> (rider,origin, destinaion)
    
    # Return the nearest five users
    nearest_users = [rideInfoSerializer(user[0]).data for user in rider_origin_destination[:5]]
    return Response({
        "payload": nearest_users,
        "message": "Five nearest rider in ascending order of distance in KM "
    }, status=200)


