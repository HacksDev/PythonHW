import geocoder
import os
import sys
API_KEY = "ca3ebd75916f4b5fa633fac3b0563fab"

argInp = []

if __name__ == "__main__":
    for param in sys.argv:
        argInp.append(param)

lines = []
if (len(argInp) > 2):
    lines.append("#	{}	{}".format(argInp[1], argInp[2]))
else:
    with open(os.path.dirname(os.path.abspath(__file__))+'\coords.txt', 'r') as f:
        lines = f.readlines()

for line in lines:
    x, y = line.split('	')[1], line.split('	')[2] 
    print("Input coords: {:>10}, {:>10}".format(x, y))
    location = geocoder.opencage([x, y], method='reverse', key=API_KEY).json['address']
    print("Location:", location)
    print("GoogleMaps URL:", "https://www.google.com/maps/search/?api=1&query={},{}".format(x,y))
    print()
