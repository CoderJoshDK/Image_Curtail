from PIL import Image
import os, cv2, sys
import numpy as np

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

            i = masking(i)
            

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
        i = masking(i)
    
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


def masking(i):
        #== Parameters =======================================================================
    BLUR = 1
    CANNY_THRESH_1 = 10
    CANNY_THRESH_2 = 200
    MASK_DILATE_ITER = 10
    MASK_ERODE_ITER = 10
    MASK_COLOR = (1.0,1.0,1.0) # In BGR format


    #== Processing =======================================================================

    #-- Read image -----------------------------------------------------------------------
    img = cv2.cvtColor(np.array(i), cv2.COLOR_RGB2BGR)
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    #-- Edge detection -------------------------------------------------------------------
    edges = cv2.Canny(gray, CANNY_THRESH_1, CANNY_THRESH_2)
    edges = cv2.dilate(edges, None)
    edges = cv2.erode(edges, None)

    #-- Find contours in edges, sort by area ---------------------------------------------
    contour_info = []
    _, contours, _= cv2.findContours(edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
    for c in contours:
        contour_info.append((
            c,
            cv2.isContourConvex(c),
            cv2.contourArea(c),
        ))
    contour_info = sorted(contour_info, key=lambda c: c[2], reverse=True)
    max_contour = contour_info[0]

    #-- Create empty mask, draw filled polygon on it corresponding to largest contour ----
    # Mask is black, polygon is white
    mask = np.zeros(edges.shape)
    cv2.fillConvexPoly(mask, max_contour[0], (255))

    #-- Smooth mask, then blur it --------------------------------------------------------
    mask = cv2.dilate(mask, None, iterations=MASK_DILATE_ITER)
    mask = cv2.erode(mask, None, iterations=MASK_ERODE_ITER)
    mask = cv2.GaussianBlur(mask, (BLUR, BLUR), 0)
    mask_stack = np.dstack([mask]*3)    # Create 3-channel alpha mask

    #-- Blend masked img into MASK_COLOR background --------------------------------------
    mask_stack  = mask_stack.astype('float32') / 255.0          # Use float matrices, 
    img         = img.astype('float32') / 255.0                 #  for easy blending

    masked = (mask_stack * img) + ((1-mask_stack) * MASK_COLOR) # Blend
    masked = (masked * 255).astype('uint8')                     # Convert back to 8-bit 

    masked = cv2.cvtColor(masked, cv2.COLOR_BGR2RGB)  # Save

    image = Image.fromarray(masked)

    return image

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

