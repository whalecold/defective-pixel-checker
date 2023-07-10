import PIL.ExifTags
import sys
import getopt

from prettytable import PrettyTable
from PIL import Image


def getCoordinate(index, hor):
    return index / hor, index % hor


def calcPixel(im, display, nosieThreshold):
    horizontal = im.size[0]
    defectiveNum = 0
    nosieNum = 0
    dic = {}
    data = list(im.getdata())
    for idx in range(0, len(data)):
        r, g, b = data[idx]
        light = r*0.299+g*0.587+b*0.114
        if light > 250:
            dic[idx] = ("defective", light)
            defectiveNum += 1
        elif light > nosieThreshold:
            dic[idx] = ("nosie", light)
            nosieNum += 1
    table = PrettyTable(['position', 'kind', 'value'])
    for k, v in dic.items():
        x, y = getCoordinate(k, horizontal)
        table.add_row([(x, y), v[0], v[1]])

    if display:
        print(table)
    print("defective pixel %d nosie poxel %d" % (defectiveNum, nosieNum))


def printExif(im):
    print("format %s, mode %s " % (im.format, im.mode))
    print("pixel size", im.size)
    exif = im._getexif()
    dic = {'ISOSpeedRatings': 1, 'ExposureTime': 1, 'FNumber': 1, 'Model': 1,
           'LensModel': 1, "FocalLengthIn35mmFilm": 1}
    for k, v in exif.items():
        if k in PIL.ExifTags.TAGS:
            tagVal = PIL.ExifTags.TAGS[k]
            if tagVal in dic:
                if tagVal == "LensModel":
                    v = v.replace('\x00', '')
                dic[tagVal] = v

    table = PrettyTable(['parameter', 'value'])
    for k, v in dic.items():
        table.add_row([k, v])
    print(table)


def main(argv):
    file = ""
    displayDetail = False
    nosieThreshold = 60
    try:
        opts, args = getopt.getopt(argv, "f:dn:", ["file=", "detail", "nosie"])
    except getopt.GetoptError:
        print('test.py -f <inputfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-f", "--file"):
            file = arg
        if opt in ("-d", "--detail"):
            displayDetail = True
        if opt in ("-n", "--nosie"):
            nosieThreshold = int(arg)
    if len(file) == 0:
        print("should spcify the file name")
        sys.exit(2)
    print("{read image %s}" % file)
    im = Image.open(file)
    printExif(im)
    calcPixel(im, displayDetail, nosieThreshold)


if __name__ == "__main__":
    main(sys.argv[1:])
