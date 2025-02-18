#This program allows the game to generate 2 lists, which it will use to make a random level.
import random

tile_list = [
    [4,4,64,64],
    [72,4,64,64],
    [140,4,64,64],
    [84,72,64,64],
    [152,72,64,64],
    [220,72,64,64],
    ]

def nextPlatform(x,y,n,m): #x location, y location
    #n is the amount you're moving horizontally, and m is the amount you move vertically.
    i = 1 #Starting option
    j = 33 #Ending option
    if y < 200: #So that if the platforms get too high, they can't get any higher.
        i = 16
    if y > 400: #So if the platforms are too low, they don't get any lower.
        j = 21
    options = random.randint(i,j)
    if options <= 5: #1
        ending_tile = [x+n, y-(2*m)]
    elif options <= 10: #2, changed to 1.5 times so that the platforms aren't too close.
        ending_tile = [x+(1.5*n), y-m]
    elif options <= 15: #3
        ending_tile = [x+(2*n), y-m]
    elif options <= 18: #4
        ending_tile = [x+(2*n), y]
    elif options <= 21: #5
        ending_tile = [x+(3*n), y]
    elif options <= 23: #6, changed to 1.5 times so that the platforms aren't too close.
        ending_tile = [x+(1.5*n), y+m]
    elif options <= 25: #7
        ending_tile = [x+(2*n), y+m]
    elif options <= 27: #8
        ending_tile = [x+(3*n), y+m]
    elif options <= 29: #9
        ending_tile = [x+n, y+(2*m)]
    elif options <= 31: #10
        ending_tile = [x+(2*n), y+(2*m)]
    elif options <= 33: #11
        ending_tile = [x+(3*n), y+(2*m)]
    ending_tile[0] = int(ending_tile[0])
    ending_tile[1] = int(ending_tile[1])
    return ending_tile[0], ending_tile[1]

def makePlatforms(numberOfPlatforms):
    platform_list = []
    enemy_list = []

    #Makes the first platform in the level.
    x = 400 #Location of the starting tile.
    y = 536
    tile = random.choice(tile_list)
    for n in range(0,random.randint(1,3)):
        offset = n*64
        platform_list.append([tile,x+offset,y])
        
    for i in range(numberOfPlatforms):
        #Use the last thing in the list as the previous platform
        prevPlatform = platform_list[-1]
        x,y = nextPlatform(prevPlatform[1], prevPlatform[2],70,60)
        platform_length = random.randint(1,5) #A platform can be from 1 to 5 in length.
        #Choose a random tile design for the platform.
        tile = random.choice(tile_list)
        #This controls "notches", notches are to make the platforms more intresting.
        if platform_length >= 2:
            random_notch_chance = random.random()
            if random_notch_chance < 0.5:
                x_offset = random.randint(1,platform_length-1)
                x1 = x + (x_offset*64)
                y1 = y - 64
                #Creates the notches.
                for n in range(0,random.randint(1,platform_length-x_offset)):
                    offset = n*64
                    platform_list.append([tile,x1+offset, y1])
        #Choosing whether or not to put a enemy near the platform.
        random_enemy_chance = random.random()
        if random_enemy_chance < 0.25:
            x_offset = random.randint(0,platform_length-1)
            x1 = x + (x_offset*64)
            #If the platform is above the half way point then the enemy goes below the platform
            #otherwise the enemy goes below.
            if y < 300:
                y1 = y + 128
            else:
                y1 = y - 192
            enemy_list.append([x1,y1])
        for n in range(0,platform_length):
            offset = n*64
            platform_list.append([tile,x+offset,y])
    return platform_list, enemy_list

