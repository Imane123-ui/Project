import math
import sys


# computes the distance in Km between 2 latitudes / longitudes
def distance2points(lat1, long1, lat2, long2):
    R = 6371
    lat1Float = float(lat1)
    lat2Float = float(lat2)
    long1Float = float(long1)
    long2Float = float(long2)

    lat1Float = math.radians(lat1Float)
    lon1Float = math.radians(long1Float)
    lat2Float = math.radians(lat2Float)
    lon2Float = math.radians(long2Float)

    dlon = lon2Float - lon1Float
    dlat = lat2Float - lat1Float

    a = math.sin(dlat / 2) ** 2 + math.cos(lat1Float) * math.cos(lat2Float) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    d = R * c

    return [d, lat1, long1]


# get the distance minimum distance in  array of type [distances, corresponding places]
def getMinDist(distances):
    minDistance = [sys.float_info.max]
    for distance in distances:
        if distance[0] < minDistance[0]:
            minDistance = distance

    return minDistance
