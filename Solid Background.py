from PIL import Image
import os, sys, math

def update_progress(progress):
    barLength = 10 # Modify this to change the length of the progress bar
    status = ""
    if isinstance(progress, int):
        progress = float(progress)
    if not isinstance(progress, float):
        progress = 0
        status = "error: progress var must be float\r\n"
    if progress < 0:
        progress = 0
        status = "Halt...\r\n"
    if progress >= 1:
        progress = 1
        status = "Done...\r\n"
    block = int(round(barLength*progress))
    text = "\rPercent: [{0}] {1}% {2}".format( "#"*block + "-"*(barLength-block), progress*100, status)
    sys.stdout.write(text)
    sys.stdout.flush()

def leftMostPoint(image, width, height, pixalArray, bright1):

    for x in xrange(width):
        for y in xrange(height):

            pixelRGB = image.getpixel((x,y))
            R,G,B = pixelRGB

            bright2 = (R + G + B) / 3

            diff = abs(bright1 - bright2)

            if diff > 10:
                return x

def rightMostPoint(image, width, height, pixalArray, bright1):

    for x in reversed(xrange(width)):
        for y in xrange(height):

            pixelRGB = image.getpixel((x,y))
            R,G,B = pixelRGB

            bright2 = (R + G + B) / 3

            diff = abs(bright1 - bright2)

            if diff > 10:
                return x

def topMostPoint(image, width, height, pixalArray, bright1):

    for y in xrange(height):
        for x in xrange(width):

            pixelRGB = image.getpixel((x,y))
            R,G,B = pixelRGB

            bright2 = (R + G + B) / 3

            diff = abs(bright1 - bright2)

            if diff > 10:
                return y

def bottMostPoint(image, width, height, pixalArray, bright1):

    for y in reversed(xrange(height)):
        for x in xrange(width):

            pixelRGB = image.getpixel((x,y))
            R,G,B = pixelRGB

            bright2 = (R + G + B) / 3

            diff = abs(bright1 - bright2)

            if diff > 10:
                return y

def configImage(filename, doFull, cropThing = 1):

    newPath1 = curentPath + '\\' + newFileName1
    newPath2 = curentPath + '\\' + newFileName2
    newPath3 = curentPath + '\\' + oldFile

    if not os.path.exists(newPath1):
        os.makedirs(newPath1)
    if not os.path.exists(newPath2):
        os.makedirs(newPath2)
    if not os.path.exists(newPath3):
        os.makedirs(newPath3)


    i = Image.open(curentPath + "\\" + filename)
    fn, fext = os.path.splitext(filename)

    o = i.copy()

    if i.mode != 'RGB':
        i = i.convert('RGB')

    pixels = list(i.getdata())
    firstPixel = i.getpixel((0,0))
    oR,oG,oB = firstPixel

    if cropThing != 1:

        box = cropThing
        i = i.crop(box) ##For crop -- (left, upper, right, lower)

    else:

        shrink = 100
        i.thumbnail((shrink,shrink))
        if oR < 250 or oG < 250 or oB < 250:

            i = masking(i, oR,oG,oB)
            

    R,G,B = 255, 255, 255
    
    width, height = i.size

    s = i.copy()

    bright1 = (R + G + B) / 3

    fluff = 5

    #print width, height, bright1, fluff

    if not doFull:

        ##Take the left side off
        x = leftMostPoint(i, width, height, pixels, bright1) - fluff
        if x < 0:
            x = 0
        box = (x, 0, width, height)
        i = i.crop(box) ##For crop -- (left, upper, right, lower)
        width, height = i.size

        ##Take the top off
        y = topMostPoint(i, width, height, pixels, bright1) - fluff
        if y < 0:
            y = 0
        box = (0, y, width, height)
        i = i.crop(box) ##For crop -- (left, upper, right, lower)
        width, height = i.size

        ##Take the right side off
        x2 = rightMostPoint(i, width, height, pixels, bright1) + fluff
        if x2 > width:
            x2 = width
        box = (0, 0, x2, height)
        i = i.crop(box) ##For crop -- (left, upper, right, lower)
        width, height = i.size

        ##Take the bottom off
        y2 = bottMostPoint(i, width, height, pixels, bright1) + fluff
        if y2 > height:
            y2 = height
        box = (0, 0, width, y2)
        i = i.crop(box) ##For crop -- (left, upper, right, lower)
        width, height = i.size

        newX1 = int((x * o.width) / s.width)
        newY1 = int((y * o.height) / s.height)
        newX2 = int(((x2 + x) * o.width) / s.width)
        newY2 = int(((y2 + y) * o.height) / s.height)

        configImage(filename, True,
                    (newX1, newY1, newX2, newY2))
        return

    i.thumbnail((size2 - 30, size2 - 35))

    if oR < 250 or oG < 250 or oB < 250:
        i = masking(i, oR,oG,oB)
    
    width, height = i.size

    newImage = Image.new('RGBA', sizeTwo, "white")

    newX = (newImage.width - width) / 2
    newY = (newImage.height - height) / 2

    position = (newX, newY)
    newImage.paste(i, position) ##Position = upper left

    newImage.save(newPath2 + '/' + fn + '_' + str(sizeTwo[0]) + saveAs)

    i.thumbnail(sizeOne)
    width, height = i.size

    newImage = Image.new('RGBA', sizeOne, "white")

    newX = (newImage.width - width) / 2
    newY = (newImage.height - height) / 2

    position = (newX, newY)
    newImage.paste(i, position) ##Position = upper left

    newImage.save(newPath1 + '/' + fn + '_' + str(sizeOne[0]) + saveAs)

    os.rename(curentPath + '\\' + filename, newPath3 + '\\' + filename)


def masking(i, oR,oG,oB):

    output_img = Image.new("RGB", i.size)
    
    firstPixel = i.getpixel((0,0))
    oR,oG,oB = firstPixel

    for y in xrange(i.size[1]):
        for x in xrange(i.size[0]):

            p = i.getpixel((x, y))
            d = math.sqrt(math.pow(p[0] - oR, 2) + math.pow((p[1] - oG), 2) + math.pow(p[2] - oB, 2))

            if d > 100:
                output_img.putpixel((x, y), (p[0], p[1], p[2]))
            else:
                
                output_img.putpixel((x, y), (255, 255, 255))

            

    return output_img


fileDir = os.getcwd()

curentPath = os.path.join(fileDir, 'Images')

startPath = fileDir

doneFiles = []

custom = open(fileDir + '\Customization.txt', 'r')
customLines =  custom.readlines()

size1 = int(customLines[3])
size2 = int(customLines[6])

sizeOne = (size1, size1)
sizeTwo = (size2, size2)

newFileName1 = 'New_Images_' + str(sizeOne[0])
newFileName2 = 'New_Images_' + str(sizeTwo[0])
oldFile = 'Old_Images'

saveAs = customLines[9]

update_progress(0)

running = True
totalImages = 0

while running == True:

    running = False

    for filename in os.listdir(curentPath):

        if filename != newFileName1 and filename != newFileName2 and filename != oldFile:

            if filename not in doneFiles:

                if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                    totalImages += 1
                    doneFiles.append(filename)
                    running = True

                else:

                    running = True
                    curentPath = curentPath = os.path.join(curentPath, filename)
                    doneFiles.append(filename)
                    break
                    
            
    if running == False:

        curentPath = os.path.split(curentPath)[0]
        running = True

    if curentPath == startPath:
        running = False

running = True

curentPath = os.path.join(fileDir, 'Images')
doneFiles = []

currentImage = 0

while running == True:

    running = False

    for filename in os.listdir(curentPath):

        if filename != newFileName1 and filename != newFileName2 and filename != oldFile:

            if filename not in doneFiles:

                if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                    configImage(filename, False)
                    currentImage += 1
                    update_progress(currentImage / float(totalImages))
                    running = True

                else:

                    running = True
                    curentPath = curentPath = os.path.join(curentPath, filename)
                    doneFiles.append(filename)
                    break
                    
            
    if running == False:

        curentPath = os.path.split(curentPath)[0]
        running = True

    if curentPath == startPath:
        running = False

