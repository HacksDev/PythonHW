import geocoder
import os
API_KEY = "ca3ebd75916f4b5fa633fac3b0563fab"

lines = []
with open(os.path.dirname(os.path.abspath(__file__))+'\coords.txt', 'r') as f:
    lines = f.readlines()

for line in lines:
    x, y = line.split('	')[1], line.split('	')[2] 
    print("Input coords: {:>10}, {:>10}".format(x, y))
    location = geocoder.opencage([x, y], method='reverse', key=API_KEY).json['address']
    print("Location:", location)
    print("GoogleMaps URL:", "https://www.google.com/maps/search/?api=1&query={},{}".format(x,y))
    print()
