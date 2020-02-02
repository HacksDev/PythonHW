import os
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS

def getCoords(filename):
    exif = Image.open(filename)._getexif()
    GPSInfo = 34853
    if (exif is not None and GPSInfo in exif):
        info = exif[GPSInfo]
        x, y = 2, 4 # GPSLatitude, GPSLongitude # x-1 | y - 1 <- Direction 
        for id in [x,y]:
            v = info[id];
            info[id] = ( v[0][0]/v[0][1] + v[1][0]/v[1][1] / 60 + v[2][0]/v[2][1] / 3600) * \
                (-1 if info[id - 1] in ['S','W'] else 1)
        return [info[x], info[y]]
    else:
        print("Изображение не содержит GPS информации!")
        return [0, 0]


coords = getCoords(os.path.dirname(os.path.abspath(__file__))+'\\1.jpg')
print(coords[0], coords[1])
os.system("python3 Task5.1.py {} {}".format(coords[0], coords[1]))