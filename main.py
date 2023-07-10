import PIL.ExifTags
import sys
import getopt

from PIL import Image


def getCoordinate(index, hor):
    return index / hor, index % hor


def calcPixel(im, display):
    horizontal = im.size[0]
    defectiveNum = 0
    nosieNum = 0
    data = list(im.getdata())
    for idx in range(0, len(data)):
        r, g, b = data[idx]
        light = r*0.30+g*0.59+b*0.11
        if light > 250:
            x, y = getCoordinate(idx, horizontal)
            if display:
                print("position (%d,%d) defective pixel, value %d" %
                      (x, y, light))
            defectiveNum += 1
        elif light > 180:
            x, y = getCoordinate(idx, horizontal)
            if display:
                print("position (%d,%d) nosie pixel, value %d" %
                      (x, y, light))
            nosieNum += 1
    print("defective pixel %d nosie poxel %d" % (defectiveNum, nosieNum))


def printExif(im):
    print("format %s, mode %s " % (im.format, im.mode))
    print("pixel size", im.size)
    exif = im._getexif()
    dic = {}
    for k, v in exif.items():
        if k in PIL.ExifTags.TAGS:
            tagVal = PIL.ExifTags.TAGS[k]
            if tagVal == "ISOSpeedRatings":
                dic["ISOSpeedRatings"] = v
            if tagVal == "ExposureTime":
                dic["ExposureTime"] = v
            if tagVal == "Model":
                dic["Model"] = v
            if tagVal == "DateTime":
                dic["DateTime"] = v
    print(dic)


def main(argv):
    file = ""
    displayDetail = False
    try:
        opts, args = getopt.getopt(argv, "f:d", ["file=", "detail"])
    except getopt.GetoptError:
        print('test.py -f <inputfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-f", "--file"):
            file = arg
        if opt in ("-d", "--detail"):
            displayDetail = True
    print("read image %s" % file)
    im = Image.open(file)
    printExif(im)
    calcPixel(im, displayDetail)


if __name__ == "__main__":
    main(sys.argv[1:])
