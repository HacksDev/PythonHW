# Task5.3 (hw18)

## Task description

Написать скрипт, который будет создавать миниатюры фотографий.
Объем полученого файла должен передаваться как параметр.

## Report

Preparing

```cmd
pip install pillow 
```


[File 5.3](Task5.3.py)  

How to run

```
python ./Task5.3.py -h # help
python ./Task5.3.py -f filename.jpg # open file
python ./Task5.3.py -f filename.jpg -sS 0.5 # set scale
python ./Task5.3.py -f filename.jpg -sW 100 # set width
python ./Task5.3.py -f filename.jpg -sH 100 # set height
python ./Task5.3.py -f filename.jpg -sW 100 -sH 100 # set height and width
```

```python
import sys, os
from PIL import Image

currentImage = None;

def _openimage(filename):
    pathname = filename
    if ("\\" not in filename or "/" not in filename):
       pathname = os.path.dirname(os.path.abspath(__file__))+"/"+filename
    if (os.path.exists(pathname)):
        return Image.open(pathname)
    else:
        print("File not found!")
        exit(-1)

def _saveimage(image):
    path = currentImage.filename.split('/')
    name = "/".join(path[0:-1])+"/preview_"+path[-1] 
    if ("\\" not in filename or "/" not in filename):
       pathname = os.path.dirname(os.path.abspath(__file__))+"/preview_"+filename
    image.save(pathname)
    # image.show()

def squeezeHeight(height):
    size = currentImage.size
    squeezeScale(height/size[1])

def squeezeWidth(width):
    size = currentImage.size
    squeezeScale(width/size[0])

def squeezeWidthAndHeight(width, height):
    _saveimage(currentImage.resize((width, height)))

def squeezeScale(scale):
    size = currentImage.size
    _saveimage(currentImage.resize((int(size[0]*scale),int(size[1]*scale))))

if __name__ == "__main__":
    args = sys.argv
    if ("-h" in args): print("""
Flags: \n-h for help,
-f for the file name,
-sH for setting height,
-sW for setting width, 
-sS for setting scale

Example: *** -f filename.jpg -sS 0.5
""")
    try:
        if ("-f" in args):
            filename = args[args.index("-f") + 1] 
            currentImage = _openimage(filename)
        if ("-sH" in args and "-sW" in args):
            width = int(args[args.index("-sW") + 1]) 
            height = int(args[args.index("-sH") + 1])
            squeezeWidthAndHeight(width=width,height=height)
            exit()
        if ("-sH" in args):
            height = int(args[args.index("-sH") + 1])
            squeezeHeight(height=height)
            exit()
        if ("-sW" in args):
            width = int(args[args.index("-sW") + 1]) 
            squeezeWidth(width=width)
            exit()
        if ("-sS" in args):
            scale = float(args[args.index("-sS") + 1]) 
            squeezeScale(scale=scale)
            exit()
    except Exception as e:
        print("[ERROR]: "+str(e))
        print("Entry params are incorrect! Please use -h for getting help.")
```