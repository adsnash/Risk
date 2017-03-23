#! python3

import random
import logging

#set logging - change to DEBUG to see all output
logging.basicConfig(level=logging.WARNING)

#dict for each territory to track owner and number of units
terr = {1:{'n':0, 'p':0}, 2:{'n':0, 'p':0}, 3:{'n':0, 'p':0},
        4:{'n':0, 'p':0}, 5:{'n':0, 'p':0}, 6:{'n':0, 'p':0},
        7:{'n':0, 'p':0}, 8:{'n':0, 'p':0}, 9:{'n':0, 'p':0},
        10:{'n':0, 'p':0}, 11:{'n':0, 'p':0}, 12:{'n':0, 'p':0},
        13:{'n':0, 'p':0}, 14:{'n':0, 'p':0}, 15:{'n':0, 'p':0},
        16:{'n':0, 'p':0}, 17:{'n':0, 'p':0}, 18:{'n':0, 'p':0},
        19:{'n':0, 'p':0}, 20:{'n':0, 'p':0}, 21:{'n':0, 'p':0},
        22:{'n':0, 'p':0}, 23:{'n':0, 'p':0}, 24:{'n':0, 'p':0},
        25:{'n':0, 'p':0}, 26:{'n':0, 'p':0}, 27:{'n':0, 'p':0},
        28:{'n':0, 'p':0}, 29:{'n':0, 'p':0}, 30:{'n':0, 'p':0},
        31:{'n':0, 'p':0}, 32:{'n':0, 'p':0}, 33:{'n':0, 'p':0},
        34:{'n':0, 'p':0}, 35:{'n':0, 'p':0}, 36:{'n':0, 'p':0},
        37:{'n':0, 'p':0}, 38:{'n':0, 'p':0}, 39:{'n':0, 'p':0},
        40:{'n':0, 'p':0}, 41:{'n':0, 'p':0}, 42:{'n':0, 'p':0}}

#dict to track which territories each territory touches
touch = {1:{2,6,32}, 2:{1,6,7,9}, 3:{4,9,13},
         4:{3,7,8,9}, 5:{6,7,8,15}, 6:{1,2,5,7},
         7:{2,4,5,6,8,9}, 8:{4,5,6,7}, 9:{2,3,4,7},
         10:{11,12}, 11:{10,12,13,25}, 12:{10,11,13},
         13:{3,11,12}, 14:{15,16,17,20}, 15:{5,14,17},
         16:{14,17,18,19,20}, 17:{14,15,16,19}, 18:{16,19,20,23,25,33},
         19:{16,17,18,27,33,37}, 20:{14,16,18,25}, 21:{22,25,26},
         22:{21,23,24,25,26,33}, 23:{18,22,25,33}, 24:{22,26},
         25:{11,18,20,21,22,23}, 26:{21,22,24}, 27:{19,28,29,33,37},
         28:{27,29,34,35,36,37}, 29:{27,28,33,35}, 30:{32,34,36,38},
         31:{32,34}, 32:{1,30,31,34,38}, 33:{18,19,22,23,27,29},
         34:{28,30,31,32,36}, 35:{28,29,40}, 36:{28,30,34,37,38},
         37:{19,27,28,36}, 38:{30,32,36}, 39:{41,42},
         40:{35,41,42}, 41:{39,40,42}, 42:{39,40,41}}

#dict to check if a continent is owned and how many units it is worth
extra = { 1:{'x':5,'t':[1,2,3,4,5,6,7,8,9]},
         10:{'x':2,'t':[10,11,12,13]},
         14:{'x':5,'t':[14,15,16,17,18,19,20]},
         21:{'x':3,'t':[21,22,23,24,25,26]},
         27:{'x':7,'t':[27,28,29,30,31,32,33,34,35,36,37,38]},
         39:{'x':2,'t':[39,40,41,42]}}

#dict to track how many units, territories, and cards each player has
#info = {1:{'units':0, 'terr':0, 'cards':0}}
info = {}

#card cash amounts
cardCash = [4,6,8,10,12,15]

#coordinates for placing unit numbers on each territory
coord = {
1:(73, 55), 
2:(120, 90),
3:(115, 205),
4:(175, 150),
5:(320, 33),
6:(150, 57),
7:(190, 100),
8:(260, 95),
9:(105, 145),
10:(240, 420),
11:(270, 315),
12:(230, 350),
13:(210, 265),
14:(385, 90),
15:(410, 20),
16:(495, 103),
17:(500, 30),
18:(527, 132),
19:(575, 80),
20:(443, 145),
21:(525, 295),
22:(560, 245),
23:(530, 195),
24:(660, 355),
25:(455, 225),
26:(530, 365),
27:(650, 125),
28:(760, 160),
29:(710, 195),
30:(770, 90),
31:(940, 150),
32:(885, 55),
33:(590, 170),
34:(785, 125),
35:(795, 230),
36:(700, 50),
37:(645, 65),
38:(795, 55),
39:(885, 385),
40:(822, 312), 
41:(920, 280),
42:(835, 415) }

#alternative coordinates for drawing lines
altCoord = {
14:(450, 90), 
15:(415, 50),
17:(520, 60), 
24:(640, 360),
31:(925, 170),
41:(925, 320) }

# RGB for map -- R: NUM, G: 150, B: 100

#set initial data structures for players
def randomStart(players):
    computer = 0
    if players == 2:
        computer = 1
    if players > 6 or players < 2:
        logging.error('Invalid number of players, must be 2-6')
    else:
        troopNum = {2:40, 3:35, 4:30, 5:25, 6:20}
        troops = [troopNum[players]]*(players+computer)
        for i in range(1,players+1+computer):
            info[i] = {'units':0, 'terr':0, 'cards':0}
        first = random.randint(0,players-1+computer)
        for i in range(42):
            p = (i+first)%(players + computer)+ 1
            while True:
                r = random.randint(1,42)
                if terr[r]['p'] == 0:
                    terr[r]['p'] = p
                    terr[r]['n'] = 1
                    troops[p-1] -= 1
                    info[p]['units'] += 1
                    info[p]['terr'] += 1
                    break
        for i in range(len(troops)):
            while troops[i] > 0:
                r = random.randint(1,42)
                if terr[r]['p'] == (i+1):
                    terr[r]['n'] += 1
                    troops[i] -= 1
                    info[i+1]['units'] += 1
        if computer == 1:
            info[0] = info.pop(3)
            for i in terr:
                if terr[i]['p'] == 3:
                    terr[i]['p'] = 0
        return random.randint(1,players)

#get number of troops to place
def add(player):
    troops = info[player]['terr'] // 3
    if troops < 3:
        troops = 3
    for i in extra:
        cont = extra[i]['t']
        flag = True
        for t in cont:
            if terr[t]['p'] != player:
                flag = False
                break
        if flag == True:
            troops += extra[i]['x']
    return troops

#roll dice for attack state 
def dice(attacker, defender):
    attTotal = terr[attacker]['n']
    defTotal = terr[defender]['n']
    attPlayer = terr[attacker]['p']
    defPlayer = terr[defender]['p']
    attNum = min(3, attTotal-1)
    defNum = min(2, defTotal)
    attAr = []
    defAr = []
    attLoss = 0
    defLoss = 0
    change = False
    for i in range(attNum):
        n = random.randint(1,6)
        attAr.append(n)
    for j in range(defNum):
        n = random.randint(1,6)
        defAr.append(n)
    attAr.sort(reverse=True)
    defAr.sort(reverse=True)
    for i in range(min(attNum, defNum)):
        if attAr[i] > defAr[i]:
            defLoss += 1
            info[defPlayer]['units'] -= 1
            terr[defender]['n'] -= 1
        else:
            attLoss += 1
            info[attPlayer]['units'] -= 1
            terr[attacker]['n'] -= 1
    logging.debug('Attacker lost '+str(attLoss)+', Defender lost '+str(defLoss))
    if terr[defender]['n'] < 1:
        info[attPlayer]['terr'] += 1
        info[defPlayer]['terr'] -= 1
        terr[defender]['p'] = attPlayer
        terr[defender]['n'] += 1
        terr[attacker]['n'] -= 1
        change = True
    elif terr[attacker]['n'] < 2:
        change = True
    return attLoss, defLoss, change

#get number of extra units from card cash
def cashCards(player, count):
    cards = info[player]['cards']
    if cards < 3:
        logging.warning('Not enough cards to cash')
        return 0
    elif cards >= 3:
        info[player]['cards'] -= 3
        if count <= 5:
            return cardCash[count]
        else:
            n = count - 5
            return n*5+15
