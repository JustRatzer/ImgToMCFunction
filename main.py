import math
import json
from PIL import Image

BlockDataFile = open("data.json", 'r')
BlockDataJson = json.load(BlockDataFile)

#Gets all the colors from the data.json
colorList = []
for i in BlockDataJson["blocks"]:
        colorList.append(i["rgb"])

def calculate_distance(rgb1, rgb2):
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(rgb1, rgb2)))

def find_closest_color(target_rgb, color_list):
    distances = [calculate_distance(target_rgb, color) for color in color_list]
    min_distance_index = distances.index(min(distances))
    closest_color = color_list[min_distance_index]
    return closest_color

def getBlockFromColor(rgb):
    closestFromList = find_closest_color(rgb, colorList)
    for i in BlockDataJson["blocks"]:
        if(closestFromList == i["rgb"]):
            return(i["block_name"])

#Get image and convert to list of rgb values
imageName = input("What is the name and extension of the image file (for example image.png): ")
im = Image.open(imageName, 'r')
pixVal = list(im.getdata())

#Random variables honestly i forget what there for
blockList = []
newFunction = ""
offset=0
bigOffset = 0
funcs = 0
x=1
y = im.height

#Create list of block names from colors
print("Creating BlockList")
for i in pixVal:
    blockList.append(getBlockFromColor(i))

#Create MCFunctions
print("Creating Functions")
for i in range(len(blockList) +1):

    if(i == 0):
         continue

    if (i-bigOffset) == 32000:
        with open('image' + str(funcs) + '.mcfunction', 'w') as f:
            newFunction = newFunction + "execute as @s run function ratz:image" + str(funcs + 1)
            f.write(newFunction)
            newFunction = ""
            funcs = funcs + 1
            bigOffset = bigOffset + 32000

    newFunction = newFunction + "execute at @s run setblock ~" + str(x + 1) +" ~" +str(y)+" ~ "  + blockList[i-1] + "\n"
    
    x = x + 1
    if ((i) - offset == im.width):
        y = y -1
        offset = offset + im.width
        x = 1

    #   //DEBUGING OUTPUTS//
    #print(str(x) + " "  + blockList[i-1] + " I=" + str(i) + " xyz=~"+ str(x) +" ~" +str(y)+" ~")
    #print(im.width)
    #print(len(blockList))

#Write Finale Function
with open('image' + str(funcs) + '.mcfunction', 'w') as f:
        f.write(newFunction)