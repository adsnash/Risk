#! python3

import pygame
import time
import logging
import Risk2
import sys

#initialize pygame 
pygame.init()

#set logging: default is WARNING
#change to DEBUG to see all output
#change to INFO to see output for failed moves/more important updates
#change to WARNING to only see program issues
logging.basicConfig(level=logging.WARNING)

#set GUI dimensions
displayWidth = 1000 
displayHeight = 612 

#set color constants
white = (255,255,255)
black = (0,0,0)
grey = (150,150,150)
lightGrey = (200,200,200)
red = (200,0,0)
brightRed = (255,0,0)
orange = (200,130,0)
brightOrange = (255,180,0)
yellow = (200,200,0)
brightYellow = (255,255,0)
green = (0,200,0)
brightGreen = (0,255,0)
blue = (0,0,200)
brightBlue = (0,70,255)
purple = (160,0,160)
brightPurple = (255,0,255)

#initial board setup
gameDisplay = pygame.display.set_mode((displayWidth,displayHeight))
pygame.display.set_caption('Risk Simulation by Alex Nash')

#map has RGB values that correspond to each territory
#R = 1-42 (depending on territory number), G = 150, B = 100
masterMap = pygame.image.load('masterMap.png').convert()
gameMap = pygame.Surface((1000,512))
gameDisplay.blit(gameMap, (0,0))

#set icon image
icon = pygame.image.load('RedR.png')
pygame.display.set_icon(icon)

#declare constants
players = 6
cardCount = 0
colors = {1:red, 2:blue, 3:yellow, 4:green, 5:orange, 6:purple, 0:lightGrey}
#constants for controlling next button
nextB = 'Attack'
nextC = False
nextH = False
#constants for message display
box1 = 'Player 1\'s Turn'
box2 = 'Welcome to Risk!'
box3 = 'Have fun!'

#functions for making boxes and text
def makeText(msg, s=30):
    font = pygame.font.Font('freesansbold.ttf', s)
    text = font.render(msg, True, black)
    return text

#if passed empty string, can be used to make a colored rectangle
def makeButton(color,x,y,w,h,msg,s):
    pygame.draw.rect(gameDisplay, color, (x,y,w,h))
    text = makeText(msg, s)
    spot = text.get_rect()
    spot.center = ((x+w/2),(y+h/2))
    gameDisplay.blit(text, spot)
    pygame.display.update 

#introduction pages
#initial instructions
def instructions():
    global nextH
    intro = True
    while intro:
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        makeButton(black,0,0,displayWidth,displayHeight,'',0)
        makeButton(grey,2,2,displayWidth-4,displayHeight-4,'',0)
        msgA = "This is a Risk simulation I built in python to practice programming. I hope you enjoy it!"
        msgB = "Please take note - there are a few changes from the original rules:"
        msgC = "Country and troop placement is randomized."
        msgD = "Cards have been simplified. You may cash your cards when you have 3 or 4."
        msgE = "Cards are automatically cashed when you have 5 or more."
        msgF = "Attacking and defending is set to use the maximum number of dice."
        msgG = "If an invasion is successful, any number of troops can be placed in either territory."
        msgH = "Pro Tip: when placing units, you can left click to add 1 or right click to add 5."
        msgI = "If there are less than 5 to add, all of the remaining units will be added."
        msgJ = "You can check out the source code on my github: https://github.com/adsnash"
        msgK = "If you are unfamiliar with the rules of Risk, please visit: http://www.hasbro.com/common/instruct/risk.pdf"
        msgL = "Legal disclaimer: Risk is a registered trademark of Parker Brothers. This simulation is for educational purposes only."
        msgM = "I do not claim to own any of Parker Brothers’ intellectual property. Please don’t sue me!"
        msgAr = [msgB,msgC,msgD,msgE,msgF,msgG,msgH,msgI]
        makeButton(grey,250,20,500,50,'Welcome to my Risk Simulation!',45)
        makeButton(grey,150,80,700,25,msgA,16)
        down = 25
        for i in range(len(msgAr)):
            makeButton(grey,150,(120+(down+5)*i),700,30,msgAr[i],20)
        makeButton(grey,50,460,900,20,msgJ,16)
        makeButton(grey,50,490,900,20,msgK,16)
        makeButton(grey,50,530,900,20,msgL,13)
        makeButton(grey,50,555,900,20,msgM,13)
        makeButton(black,385,380,180,60,'',0)
        makeButton(red,390,385,170,50,'Got it!',30)
        if 390 < mouse[0] < 390+170 and 385 < mouse[1] < 435:
            makeButton(brightRed,390,385,170,50,'Got it!',30)
            if click[0] == 1:
                intro = False
        else:
            makeButton(red,390,385,170,50,'Got it!',30)
        pygame.display.update()

#intro map to show continent borders and bonuses
def introMap():
    global nextH
    intro = True
    def colorPicker(num):
        if num <= 9:
            return red
        elif 10 <= num <= 13:
            return orange
        elif 14 <= num <= 20:
            return yellow
        elif 21 <= num <= 26:
            return green
        elif 27 <= num <= 38:
            return blue
        elif 39 <= num <=42:
            return purple    
    for i in range(1000):
        for j in range(512):
            p = masterMap.get_at((i, j))
            if p[1] == 150 and p[2] == 100:
                if 1 <= p[0] <= 43:
                    c = colorPicker(p[0])
                    gameMap.set_at((i,j), c)
            else:
                gameMap.set_at((i,j), p)
    gameDisplay.blit(gameMap, (0,0))
    pygame.display.update()
    NA, NA1 = "North America", "5 Extra Units"
    SA, SA1 = "South America", "2 Extra Units"
    EU, EU1 = "Europe", "5 Extra Units"
    AF, AF1 = "Africa", "3 Extra Units"
    AS, AS1 = "Asia", "7 Extra Units"
    AU, AU1 = "Oceania", "2 Extra Units"
    Coords = {NA:(113,107), SA:(203,315), EU:(492,98), AF:(445,215), AS:(690,110), AU:(826,395)}
    contAr = [NA,NA1,SA,SA1,EU,EU1,AF,AF1,AS,AS1,AU,AU1]
    font = pygame.font.Font('freesansbold.ttf', 20)
    for i in range(0,len(contAr),2):
        msg1 = contAr[i]
        msg2 = contAr[i+1]
        coordinates1 = Coords[contAr[i]]
        coordinates2 = (coordinates1[0],coordinates1[1]+20)
        text1 = font.render(msg1, True, white)
        text2 = font.render(msg2, True, white)
        gameDisplay.blit(text1, coordinates1)
        gameDisplay.blit(text2, coordinates2)
        pygame.display.update
    msgA = "This map shows the different continents, their borders, and their extra unit value."
    msgB = "Please note: the button to move to the next phase of your turn will be red when active or grey if action must be taken."
    makeButton(black,0,512,displayWidth,100,'',0)
    makeButton(grey,2,513,displayWidth-4,97,'',0)
    makeButton(grey,50,530,900,25,msgA,17)
    makeButton(grey,50,565,900,25,msgB,17)
    makeButton(black,385,445,180,60,'',0)
    makeButton(red,390,450,170,50,'Let\'s Play!',30)
    while intro:
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        if 390 < mouse[0] < 390+170 and 450 < mouse[1] < 500:
            makeButton(brightRed,390,450,170,50,'Let\'s Play!',30)
            if click[0] == 1:
                intro = False
        else:
            makeButton(red,390,450,170,50,'Let\'s Play!',30)
        pygame.display.update()

#page to get number of players, reused for rematch to get new number
def intro():
    global players, nextH
    intro = True
    while intro:
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        makeButton(black,0,0,displayWidth,displayHeight,'',0)
        makeButton(grey,2,2,displayWidth-4,displayHeight-4,'',0)
        makeButton(grey,250,100,500,100,'Get ready to start!',50)
        makeButton(grey,250,200,500,100,'How many players?',40)
        margin = 130
        color = {1:red, 2:blue, 3:green, 4:yellow, 5:purple}
        other = {1:brightRed, 2:brightBlue, 3:brightGreen, 4:brightYellow, 5:brightPurple}
        for i in range(1,6):
            c = color[i]
            makeButton(black,(65+margin*i),345,90,90,'',0)
            makeButton(c,(70+margin*i),350,80,80,str(i+1),38)
        for j in range(1,6):
            if (70+margin*j) < mouse[0] < (70+margin*j+80) and 350 < mouse[1] < 430:
                c = other[j]
                makeButton(c,(70+margin*j),350,80,80,str(j+1),38)
                if click[0] == 1:
                    #get number of players
                    players = j+1
                    intro = False
            else:
                c = color[j]
                makeButton(c,(70+margin*j),350,80,80,str(j+1),38)
        pygame.display.update()

#user interface for messages and player info
#used with getMouseClick to make grey or red, will highlight if hovered over
def nextButton():
    msg = nextB
    if nextC == True and nextH == False:
        color = red
    elif nextC == True and nextH == True:
        color = brightRed
    else:
        color = grey
    makeButton(black,617,519,100,28,'',0)
    makeButton(color,621,523,92,20,msg,20)

def box(msg,y,w=440):
    x,h,s = 280, 30, 24
    makeButton(white,x,y,w,h,msg,s)

def msgBox1():
    y = 516
    w = 390
    msg = box1
    box(msg,y,w)
    makeButton(white,670,y,50,30,'',0)

def msgBox2():
    y = 516+30
    msg = box2
    box(msg,y)

def msgBox3():
    y = 516+60
    msg = box3
    box(msg,y)

def playerToken(player):
    color = colors[player]
    makeButton(black,305,519,28,28,'',0)
    makeButton(color,309,523,20,20,'',0)

def staticInfo(players):
    xInc = 720
    yInc = 27
    s = (' '*3)
    makeButton(grey,110,515,160,15,('Units'+s+'Territories'+s+'Cards'),14)
    makeButton(grey,110+xInc,515,160,15,('Units'+s+'Territories'+s+'Cards'),14)
    for i in range(1,players+1):
        side = i%2
        down = (i+side)//2
        color = colors[i]
        makeButton(grey,(750-xInc*side),(505+yInc*down),80,20,('Player '+str(i)),17)
        makeButton(black,(730-xInc*side),(506+yInc*down),18,18,'',0)
        makeButton(color,(732-xInc*side),(508+yInc*down),14,14,'',0)
    if players == 2:
        color = colors[0]
        makeButton(grey,(30),(559),80,20,('Neutral'),17)
        makeButton(black,(10),(560),18,18,'',0)
        makeButton(color,(12),(562),14,14,'',0)

#updated when units or territories changes
def dynamicInfo(players):
    xInc = 720
    yInc = 27
    for i in range(1,players+1):
        side = i%2
        down = (i+side)//2
        u = str(Risk2.info[i]['units'])
        t = str(Risk2.info[i]['terr'])
        c = str(Risk2.info[i]['cards'])
        s = (' '*9)
        makeButton(grey,(830-xInc*side),(505+yInc*down),160,18,(u+s+t+s+c),17)
    if players == 2:
        u = str(Risk2.info[0]['units'])
        t = str(Risk2.info[0]['terr'])
        c = str(Risk2.info[0]['cards'])
        s = (' '*9)
        makeButton(grey,(830-xInc),(505+yInc*2),160,20,(u+s+t+s+c),17)

def legendDynamic():
    if cardCount <= 5:
        c = Risk2.cardCash[cardCount]
    else:
        c = (cardCount - 5)*5+15  
    makeButton(grey,135,475,20,15,str(c),15)
        
#functions to update board and user interface 
def show():
    msgBox1()
    msgBox2()
    msgBox3()
    nextButton()
    playerToken(player)
    dynamicInfo(players)
    legendDynamic()
    pygame.display.update()

def displayUnits():
    gameDisplay.blit(gameMap, (0,0))
    for i in range(1,43):
        u = Risk2.terr[i]['n']
        text = makeText(str(u), 20)
        coordinates = Risk2.coord[i]
        gameDisplay.blit(text, coordinates)
        pygame.display.update

def drawBoard():
    for i in range(1000):
        for j in range(512):
            p = masterMap.get_at((i, j))
            if p[1] == 150 and p[2] == 100:
                if 1 <= p[0] <= 43:
                    t = Risk2.terr[p[0]]['p']
                    gameMap.set_at((i,j), colors[t])
            else:
                gameMap.set_at((i,j), p)
    gameDisplay.blit(gameMap, (0,0))
    displayUnits()
    legendDynamic()

#handle mouse click and position
def getMouseClick(hover=False):
    global nextH
    pygame.event.pump()
    pygame.event.clear()
    while True:
        if hover:
            (x,y) = pygame.mouse.get_pos()
            if 600 < x < 700 and 518 < y < 546:
                if nextH == False:
                    nextH = True
                    show()
            else:
                if nextH == True:
                    nextH = False
                    show()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: # use 1 for left btn, 3 for right btn
                    return (event.pos, event.button)
                elif event.button == 3:
                    return (event.pos, event.button)

#check win state
def checkWin(player):
    global box1, box2, box3
    flag = True
    for i in range(1,43):
        if Risk2.terr[i]['p'] != player:
            if Risk2.terr[i]['p'] == 0:
                continue
            else:
                flag = False
                break
    if flag == True:
        logging.info('Player '+str(player)+' wins')
        box1 = ('Player '+str(player)+' Wins!')
        box2 = ('World Domination Complete')
        box3 = ('Interested in a rematch?')
        show()
    return flag

#rematch 
def rematch():
    global nextB, nextC, nextH, cardCount
    nextB = 'Rematch'
    nextC = True
    nextH = True
    show()
    while True:
        (x,y), t = getMouseClick(True)
        if 600 < x < 700 and 518 < y < 546:
            if t == 1:
                logging.info('Rematch')
                cardCount = 0
                for i in Risk2.terr:
                    Risk2.terr[i]['n'] = 0
                    Risk2.terr[i]['p'] = 0
                Risk2.info.clear()
                break
        else:
            continue

#draw connecting lines for attack and fortify
def drawlines(place, other):
    #for Alaska/Eastern Russia so lines go to both ends of display
    def edgeCase():
        NA = Risk2.coord[1]
        ptNA = (NA[0]+5, NA[1]+6)
        altNA = (0, ptNA[1])
        AS = Risk2.coord[32]
        ptAS = (AS[0]+5, AS[1]+6)
        altAS = (1000, ptAS[1])
        pygame.draw.line(gameDisplay, white, ptNA, altNA, 1)
        pygame.draw.line(gameDisplay, white, ptAS, altAS, 1)
    if place in Risk2.altCoord:
        A = Risk2.altCoord[place]
        ptA = (A[0], A[1])
    else:
        A = Risk2.coord[place]
        ptA = (A[0]+5, A[1]+7)
    #post-attack fortify: only lines between attacking/conquered territory
    if 0 < other < 43:
        if (place == 1 and other == 32) or (place == 32 and other == 1):
            edgeCase()
        else:
            if other in Risk2.altCoord:
                B = Risk2.altCoord[other]
                ptB = (B[0], B[1])
                pygame.draw.line(gameDisplay, white, ptA, ptB, 1)
            else:
                B = Risk2.coord[other]
                ptB = (B[0]+5, B[1]+7)
                pygame.draw.line(gameDisplay, white, ptA, ptB, 1)
    #attack: lines to all non-player owned connected territories
    elif other == 100:
        for i in Risk2.touch[place]:
            if Risk2.terr[i]['p'] != player:
                if (place == 1 and i == 32) or (place == 32 and i == 1):
                    edgeCase()
                elif i in Risk2.altCoord:
                    B = Risk2.altCoord[i]
                    ptB = (B[0], B[1])
                    pygame.draw.line(gameDisplay, white, ptA, ptB, 1)
                else:
                    B = Risk2.coord[i]
                    ptB = (B[0]+5, B[1]+7)
                    pygame.draw.line(gameDisplay, white, ptA, ptB, 1)
    #fortify: lines to all player owned connected territories
    elif other == 0:
        for i in Risk2.touch[place]:
            if Risk2.terr[i]['p'] == player:
                if (place == 1 and i == 32) or (place == 32 and i == 1):
                    edgeCase()
                elif i in Risk2.altCoord:
                    B = Risk2.altCoord[i]
                    ptB = (B[0], B[1])
                    pygame.draw.line(gameDisplay, white, ptA, ptB, 1)
                else:
                    B = Risk2.coord[i]
                    ptB = (B[0]+5, B[1]+7)
                    pygame.draw.line(gameDisplay, white, ptA, ptB, 1)
    pygame.display.update()
    displayUnits()

#redistribute troops between attacking and conquered territory
def redistribute(attacker, defender):
    global box1, box2, box3
    troops = Risk2.terr[attacker]['n'] -1
    Risk2.terr[attacker]['n'] -= troops
    displayUnits()
    while troops > 0:
        logging.debug('Player has '+str(troops)+' to add')
        box2 = (str(troops)+' unit(s) to place')
        show()
        drawlines(attacker, defender)
        (x3,y3), t3 = getMouseClick()
        if ( y3 > 512 ):
            continue
        else:
            p3 = masterMap.get_at((x3,y3))
            if p3[0] == attacker or p3[0] == defender:
                if t3 == 1:
                    Risk2.terr[p3[0]]['n'] += 1 
                    logging.debug('1 troop added')
                    box3 = ('1 troop added')
                    show()
                    displayUnits()
                    pygame.display.update()
                    troops -= 1
                elif t3 == 3:
                    if troops > 5:
                        Risk2.terr[p3[0]]['n'] += 5 
                        logging.debug('5 troops added')
                        box3 = ('5 troops added')
                        show()
                        displayUnits()
                        pygame.display.update() 
                        troops -= 5
                    else:
                        Risk2.terr[p3[0]]['n'] += troops 
                        logging.debug(str(troops)+' troops added')
                        box3 = (str(troops)+' troops added')
                        show()
                        displayUnits()
                        pygame.display.update() 
                        troops = 0
            else:
                logging.info('Must be attacking or new territory')
                box3 = ('Must be attacking or new territory')
                show()

#place troops at beginning of turn or when cards cashed mid attack
def placeTroops(troops):
    global box2, box3
    while troops > 0:
        logging.debug('Player has '+str(troops)+' to add')
        box2 = (str(troops)+' unit(s) to place')
        show()
        (x2,y2), t2 = getMouseClick()
        if ( y2 > 512 ):
            continue
        else:
            p = masterMap.get_at((x2,y2))
            if 43 > p[0] > 0:
                if Risk2.terr[p[0]]['p'] == player:
                    if t2 == 1:
                        Risk2.terr[p[0]]['n'] += 1
                        Risk2.info[player]['units'] += 1
                        logging.debug('1 troop added')
                        box3 = ('1 troop added')
                        show()
                        displayUnits()
                        pygame.display.update()
                        troops -= 1
                    elif t2 == 3:
                        if troops > 5:
                            Risk2.terr[p[0]]['n'] += 5
                            Risk2.info[player]['units'] += 5
                            logging.debug('5 troops added')
                            box3 = ('5 troops added')
                            show()
                            displayUnits()
                            pygame.display.update()
                            troops -= 5
                        else:
                            Risk2.terr[p[0]]['n'] += troops
                            Risk2.info[player]['units'] += troops
                            logging.debug(str(troops)+' troops added')
                            box3 = (str(troops)+' troops added')
                            show()
                            displayUnits()
                            pygame.display.update()
                            troops = 0
                else:
                    logging.info('Not player\'s territory')
                    box3 = ('Must choose your own territory')
                    show()

#check for eliminated player
def eliminated(attacker, defender):
    global box2, box3, cardCount
    if Risk2.info[defender]['units'] == 0 and Risk2.info[defender]['terr'] == 0:
        c = Risk2.info[defender]['cards']
        Risk2.info[defender]['cards'] = 0
        Risk2.info[attacker]['cards'] += c
        #draw line through eliminated player with color of attacker
        xInc = 720
        yInc = 27
        side = defender%2
        down = (defender+side)//2
        color = colors[attacker]
        makeButton(black,(725-xInc*side),(513+yInc*down),105,4,'',0)
        makeButton(color,(726-xInc*side),(514+yInc*down),103,2,'',0)
        show()
        if checkWin(attacker) == True:
            pass
        else:
            troops = 0
            if Risk2.info[attacker]['cards'] >= 6:
                while Risk2.info[attacker]['cards'] > 4:
                    troops += Risk2.cashCards(player, cardCount)
                    cardCount += 1
                if troops > 0:
                    logging.info('Cards cashed - '+str(troops)+' extra units')
                    box3 = ('Cards cashed - '+str(troops)+' extra units')
                    show()
                    placeTroops(troops)

#attack
def attack(player):
    global box1, box2, box3, nextB, nextC, nextH
    logging.debug('Select territory to attack from')
    nextB = 'Fortify'
    nextH = False
    show()
    attacking = True
    card = False
    while attacking:
        try:
            box1 = ('Player '+str(player)+' - Attack')
            box2 = ('Select one of your territories')
            box3 = ('to launch attack from')
            nextC = True
            show()
            flag = False
            if not flag:
                (x,y), t = getMouseClick(True)
                if 600 < x < 700 and 518 < y < 546:
                    if t == 1:
                        attacking = False
                    else:
                        continue
                else:
                    p = masterMap.get_at((x,y))
                    if 43 > p[0] > 0:
                        if t == 3:
                            continue
                        elif t == 1:
                            if Risk2.terr[p[0]]['p'] == player:
                                if Risk2.terr[p[0]]['n'] > 1:
                                    target = False
                                    for i in Risk2.touch[p[0]]:
                                        if Risk2.terr[i]['p'] != player:
                                            target = True
                                            break
                                    if target:
                                        logging.debug('Territory available to attack from')
                                        box2 = ('Select enemy territory to attack')
                                        box3 = ('Click the water to reset')
                                        show()
                                        flag = True
                                    else:
                                        logging.info('No enemy territory to attack')
                                        box2 = ('No enemy territory to attack')
                                        box3 = ('You own all connected territories')
                                        show()
                                        time.sleep(1)
                                else:
                                    logging.info('Must have more than 1 unit to attack')
                                    box2 = ('Must have more than 1 unit to attack')
                                    box3 = ('Select enemy territory to attack')
                                    show()
                                    time.sleep(1)
                            elif Risk2.terr[p[0]]['p'] != player:
                                logging.info('Player does not own territory')
                                box2 = ('Select one of your territories')
                                show()
            while flag:
                nextC = False
                show()
                drawlines(p[0], 100)
                (x2,y2), t2 = getMouseClick()
                if ( y2 > 512 ):
                    continue
                else:
                    p2 = masterMap.get_at((x2,y2))
                    if 43 > p2[0] > 0 and p2[0] != p[0]:
                        if Risk2.terr[p2[0]]['p'] != player:
                            if p2[0] in Risk2.touch[p[0]]:
                                if t2 == 3:
                                    continue
                                elif t2 == 1:
                                    attacker = p[0]
                                    defender = p2[0]
                                    defPlayer = Risk2.terr[defender]['p']
                                    attLoss, defLoss, change = Risk2.dice(attacker,defender)
                                    logging.debug('Player lost '+str(attLoss)+', defender lost '+str(defLoss))
                                    box2 = ('You lost '+str(attLoss)+', defender lost '+str(defLoss))
                                    box3 = ('Click to attack again or water to reset')
                                    show()
                                    displayUnits()
                                    if change == True:
                                        if Risk2.terr[defender]['p'] == player:
                                            if checkWin(player) == True:
                                                eliminated(player, defPlayer)
                                                drawBoard()
                                                attacking = False
                                                flag = False
                                                break
                                            else:
                                                card = True
                                                flag = False
                                                logging.info('Territory conquered')
                                                box3 = ('Territory conquered')
                                                show()
                                                drawBoard()
                                                if Risk2.terr[attacker]['n'] > 1:
                                                    redistribute(attacker, defender)
                                                eliminated(player, defPlayer)
                                        elif Risk2.terr[attacker]['n'] < 2:
                                            flag = False
                                else:
                                    flag = False
                            else:
                                logging.info('Territories are not touching')
                                box2 = ('Territories are not touching')
                                show()
                        elif Risk2.terr[p2[0]]['p'] == player:
                            logging.info('Cannot attack owned territory')
                            box2 = ('Can\'t attack your own territory')
                            show()
                    #touch water to pick a different place
                    elif p2[0] == 162:
                        logging.info('Resetting selected territory')
                        box2 = ('Resetting selected territory')
                        box3 = ('Select territory to attack from')
                        show()
                        time.sleep(1)
                        flag = False
                        break
        except KeyError:
            pass
        except IndexError:
            pass
    if card:
        Risk2.info[player]['cards'] += 1
        show()

#add troops at beginning of turn
def addTroops(player):
    global box1, box2, box3, nextB, nextC, nextH, cardCount            
    extra = 0        
    box1 = ('Player '+str(player)+' - Add Units')
    additional = False
    choice = True
    #choice to cash if 3-5 cards, must cash if above
    while choice:
        cards = Risk2.info[player]['cards']
        if cards < 3:
            box3 = ('Select territories to place units')
            choice = False
            break
        elif cards >= 5:
            extra += Risk2.cashCards(player, cardCount)
            logging.info('Cards cashed - '+str(extra)+' extra units')
            box3 = ('Cards cashed - '+str(extra)+' extra units')
            cardCount += 1
            additional = True
        elif 3 <= cards < 5:
            if additional:
                box2 = ('Would you like to cash extra cards?')
            else:
                box2 = ('Would you like to cash your cards?')
                box3 = ('Click \'Cash\' if so or click the map')
            nextB = ('Cash')
            nextC = True
            nextH = False
            show()
            while True:
                (x,y), t = getMouseClick(True)
                if y < 512:
                    logging.debug('Player not cashing')
                    choice = False
                    break
                elif 600 < x < 700 and 518 < y < 546:
                    if t == 1:
                        extra += Risk2.cashCards(player, cardCount)
                        logging.info('Cards cashed - '+str(extra)+' extra units')
                        box3 = ('Cards cashed - '+str(extra)+' extra units')
                        cardCount += 1
                        choice = False
                        break
                else:
                    continue
    nextB = 'Attack'
    nextC = False
    nextH = False
    troops = Risk2.add(player) + extra
    show()
    placeTroops(troops)

#fortify at end of turn
def fortify(player):
    global box1, box2, box3, nextB, nextC, nextH
    nextH = False
    nextB = 'End Turn'
    box1 = ('Player '+str(player)+' - Fortify')
    while True:
        logging.debug('Select territory to move units')
        nextC = True
        box2 = ('Select territory to move units')
        box3 = ('Click \'End Turn\' when finished')
        show()
        (x,y), t = getMouseClick(True)
        troops = 0
        if 600 < x < 700 and 518 < y < 546:
            if t == 1:
                logging.debug('End Turn')
                break
            else:
                continue
        else:
            p = masterMap.get_at((x,y))
            if 43 > p[0] > 0:
                if Risk2.terr[p[0]]['p'] == player:
                    if Risk2.terr[p[0]]['n'] > 1:
                        if t == 1:
                            valid = False
                            for i in Risk2.touch[p[0]]:
                                if Risk2.terr[i]['p'] == player:
                                    valid = True
                                    break
                            if valid:
                                troops = Risk2.terr[p[0]]['n']-1
                                Risk2.terr[p[0]]['n'] -= troops
                                displayUnits()
                                box3 = ('Territories must be touching')
                                show()
                                pygame.display.update()
                            else:
                                box3 = ('No owned connecting territories')
                                show()
                                time.sleep(1)   
                        elif t == 3:
                            continue
                    else:
                        logging.info('Must have more than 1 unit')
                        box3 = ('Must have more than 1 unit')
                        show()
                        time.sleep(1)
                else:
                    logging.info('Must select owned territory')
                    box3 = ('Must select your own territory')
                    show()
                    time.sleep(1)
        while troops > 0:
            nextC = False
            show()
            logging.info(str(troops)+' unit(s) to place')
            box2 = (str(troops)+' unit(s) to place')
            drawlines(p[0], 0)
            (x2,y2), t2 = getMouseClick()
            if ( y2 > 512 ):
                continue
            else:
                p2 = masterMap.get_at((x2,y2))
                if 43 > p2[0] > 0:
                    if Risk2.terr[p2[0]]['p'] == player:
                        if p2[0] in Risk2.touch[p[0]] or p2[0] == p[0]:
                            if t2 == 1: 
                                Risk2.terr[p2[0]]['n'] += 1
                                logging.debug('1 troop added')
                                box3 = ('1 troop added')
                                show()
                                displayUnits()
                                pygame.display.update()
                                troops -= 1
                            elif t2 == 3:
                                if troops > 5:
                                    Risk2.terr[p2[0]]['n'] += 5
                                    logging.debug('5 troops added')
                                    box3 = ('5 troops added')
                                    show()
                                    displayUnits()
                                    pygame.display.update()
                                    troops -= 5
                                else:
                                    Risk2.terr[p2[0]]['n'] += troops
                                    logging.debug(str(troops)+'troops added')
                                    box3 = (str(troops)+' troops added')
                                    show()
                                    displayUnits()
                                    pygame.display.update()
                                    troops = 0
                        else:
                            logging.info('Not connected')
                            box3 = ('Territories not connected')
                            show()
                    else:
                        logging.info('Not owned territory')
                        box3 = ('Must choose your own territory')
                        show()


#intro and instructions
instructions()
introMap()
while True:
    #initial game state
    intro()
    count = Risk2.randomStart(players)
    player = count
    #draw initial board state and user interface
    makeButton(black,0,502,displayWidth,120,'',0)
    makeButton(grey,2,512,displayWidth-4,98,'',0)
    makeButton(black,278,514,444,94,'',0)
    staticInfo(players)
    drawBoard()
    show()    
    #uncomment these two lines to add starting card cash for testing
##    for i in range(1,players+1):
##        Risk2.info[i]['cards'] = 4
    #game loop
    while True:
        player = count%players + 1
        logging.info('Player '+str(player)+'\'s turn')
        #don't need both here
        if Risk2.info[player]['units'] == 0 and Risk2.info[player]['terr'] == 0:
            count += 1
        else:
            addTroops(player)
            attack(player)
            if checkWin(player) == True:
                rematch()
                break
            fortify(player)
            count += 1
