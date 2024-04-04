# maze solver for square as well as rectangular mazes
# maze generated from https://keesiemeijer.github.io/maze-generator/
# todo: make the code cleaner (user input, less functions, shorter code?)
"""
sample maze after encoding: starts from [1, 0] and ends at [9, 10]
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
[0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1]
[1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1]
[1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1]
[1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1]
[1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1]
[1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1]
[1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1]
[1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1]
[1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0]
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
direction codes: down = 0, right = 1, left = 2, up = 3
solution for this would be: [1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 3, 3, 3, 3, 3, 3, 3, 3, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 2, 2, 0, 0, 1, 1, 1]
"""
from PIL import Image
import sys

filepath = sys.argv[1]
wallthickness = int(sys.argv[2])
im = Image.open(filepath,'r')
pixelRGBA = list(im.getdata())
mazesizeX = im.width // wallthickness
mazesizeY = im.height // wallthickness
mazearray1d = []
mazearray2d = []
currentY, currentX = 1, 0 # currentY is row, currentX is column
direction = [] # solution can be represented as the final form of this list
possibleDirections = []
directionstack = [] # temporary [[currentY, currentX], index of direction list, [possibleDirections]] to be appended here when branching out
alreadyreached = [] # already reached positions (branch nodes)

# this function encodes (labels) a particular pixel as black or white based on its RGBA values in the tuple tup
# {0, 1, 2, 3, 252, 253, 254, 255} - rough estimate of all possible values of RGB in the tuple, more close it is to zero more black it is
def encode():
    for i in range(len(pixelRGBA)):
        if 2*pixelRGBA[i][0] < 255/2: # if closer to black then to white return 1
            mazearray1d.append(1)
        else:
            mazearray1d.append(0)
    # takes 1 row (mazesize elements) at a time and makes it a 2d list: 1d to 2d list converter
    # take a block of wallthickness * wallthickness size and represents it as 1 or 0
    for k in range(0, mazesizeY * wallthickness, wallthickness):
        templist=[]
        for i in range(k * im.width, (k+1) * im.width, wallthickness):
            templist.append(mazearray1d[i])
        mazearray2d.append(templist)

# update position based on direction code given
def move(code):
    global currentY, currentX # avoiding creation of local variables
    match code:
        case 0:
            currentY += 1
        case 1:
            currentX += 1
        case 2:
            currentX -= 1
        case 3:
            currentY -= 1
        case _:
            print("did not give proper direction code, debug!")

# seeks possible directions to move
def seek():
    global possibleDirections
    # to not reset possibleDirections, and let it be the same as it was from directionstack
    if ([currentY, currentX] in alreadyreached):
        return -1
    # see if its a valid spot (if you are at a white space)
    if mazearray2d[currentY][currentX]:
        print("the spot is not white!")
        return -1
    possibleDirections = [0, 1, 2, 3]
    # remove the direction from which it just arrived, in case you've made at least one move
    if len(direction):
        match direction[-1]:
            case 0:
                possibleDirections.remove(3)
            case 1:
                possibleDirections.remove(2)
            case 2:
                possibleDirections.remove(1)
            case 3:
                possibleDirections.remove(0)
            case _:
                print("something went wrong, debug!")
    # seek in X direction
    if not currentX:
        possibleDirections.remove(2)
    elif currentX == mazesizeX - 1:
        possibleDirections.remove(1)
    else:
        if mazearray2d[currentY][currentX + 1]:
            possibleDirections.remove(1)
        if mazearray2d[currentY][currentX - 1]:
            possibleDirections.remove(2)
    # seek in Y direction
    if not currentY:
        possibleDirections.remove(3)
    elif currentY == mazesizeY - 1:
        possibleDirections.remove(0)
    else:
        if mazearray2d[currentY + 1][currentX]:
            possibleDirections.remove(0)
        if mazearray2d[currentY - 1][currentX]:
            possibleDirections.remove(3)

# makes a decision of where to move and actually moves, if multiple choices go with the priority: down, right, left, up
def movedecision():
    global direction, possibleDirections, directionstack, currentY, currentX
    seek()
    # if reached dead end, jump back to latest branching node with the help of directionstack
    if not len(possibleDirections):
        currentY, currentX = directionstack[0][0][0], directionstack[0][0][1] # jump back to latest branching node
        direction = direction[:directionstack[0][1]] # erase direction record till branching node
        possibleDirections = directionstack[0][2]
        directionstack.pop(0) # remove the entry as its use is done
    elif len(possibleDirections) == 1:
        move(possibleDirections[0])
        direction.append(possibleDirections[0])
    else:
        # put position, index of direction (if needed to delete from that point) and possible directions which are not explored yet
        # this list will have latest branching details at first position
        directionstack.insert(0, [[currentY, currentX], len(direction), possibleDirections[1:]])
        alreadyreached.append([currentY, currentX])
        move(possibleDirections[0])
        direction.append(possibleDirections[0])

# paint an entire block of wallthickness * wallthickness size, given the top left corner location
# paintY and paintX are actual co-ordinates, not pseudo co-ordinates
def paintblock(paintX, paintY):
    for y in range(wallthickness):
        for x in range(wallthickness):
            im.putpixel((paintX+x, paintY+y), (255, 0, 0))

def paint():
    global currentY, currentX
    currentY, currentX = 1, 0
    paintblock(currentX * wallthickness, currentY * wallthickness)
    for i in range(len(direction)):
        move(direction[i])
        paintblock(currentX * wallthickness, currentY * wallthickness)

def main():
    encode()
    while [currentY, currentX] != [mazesizeY - 2, mazesizeX - 1]:
        movedecision()
    paint()
    im.show()

main()