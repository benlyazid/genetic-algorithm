#  ------------THIS  EXEMPLE OF GENITIC ALG  WHERE I WILL CRIET A AI THAT WILL LEARN HOW TO PLAY THE GOLL OF THE GAME IS TO GET INTO THE GREEN POINT 
import pygame
import sys
import random
from pygame.locals import *
from pygame.rect import *
import math

RED = (255,   0,   0)
GREEN = (25,   100,   0)
BLACK = (0, 0, 0)
SCORE = 0
#TARGET POINT COORDINATE TX, TY 
TX = 0
TY = 0
# FETNESS_GOAL IS HOW MUTCH YOU WANT TO LEARN YOUR AI
FETNESS_GOAL = 4000
# MOVE_FOR_TOUR THE MAXIMUN NUMBER OF MOVE ECRY TIME 
MOVE_FOR_TOUR = 200

def by_fet(elem): # FOR SORT OUR TABLE BY SECEND ELEMENT 
    return abs(elem[1])


def segmoid_function(gamma): # THIS FUNCTION MAKE RESULTE BETWEEN 0 AND 1
    if gamma < 0:
       res = 1 - 1 / (1 + math.exp(gamma))
    else:
        res = 1 / (1 + math.exp(-gamma))
    if res < 0.5:
        return 1
    return 0


def generate_point_for_fetness(score): # CRIET NEW POINT FOR OUR PLAYER AND FOR GOALS FOR LEARNING
    mx = 0
    my = 0
    tx = 0
    ty = 0
    global TX, TY
    while abs(mx - tx) + abs (my - ty) < 30:
        mx = random.randint(0, 59) * 10
        my = random.randint(0, 59) * 10
        tx = random.randint(0, 59) * 10
        ty = random.randint(0, 59) * 10
    TX = tx
    TY = ty
    return mx, my, tx, ty

def calcule_fetness(obj): # HERE  WE CALCULLATE THE FETNESS OF PLAYER 
    move = 0
    score = 0
    mx, my, tx, ty = generate_point_for_fetness(score)
    dest = abs(tx - mx) + abs(ty - my)
    i = 0
    global FETNESS_GOAL, MOVE_FOR_TOUR
    while i < MOVE_FOR_TOUR:
        ipts = [mx, my, tx, ty]
        res = make_dessision(ipts, obj)
        if res == 1 and mx < 590:
            mx += 10
        if res == 2 and mx >= 10:
            mx -= 10
        if res == 3 and my < 590:
            my += 10
        if res == 4 and my >= 10:
            my -= 10
        if tx == mx and ty == my:
            if score == FETNESS_GOAL:
                return score, mx, my
            if dest != 0:
                calcule = ((move / dest) * 10)
                if calcule == 10:
                    score += calcule
                    i = 0
            mx, my, tx, ty = generate_point_for_fetness(score)
            move = 0
            dest = abs(tx - mx) + abs(ty - my)
        move += 10
        i += 1
    return score, mx, my


def make_dessision(ipt, obj): # THIS IS A NUUERAL NETWORK THAT MAKE DECISIOnNS
    # XPLUS AND XMUNUS DESSESION 
    xp = (ipt[0] * obj[0]) + (ipt[2] * obj[4])
    xp = segmoid_function(xp)
    
    xm = (ipt[0] * obj[1]) + (ipt[2] * obj[5])
    xm = segmoid_function(xm)

    # YPLUS AND YMUNUS DESSESION 
    yp = (ipt[1] * obj[2]) + (ipt[3] * obj[6])
    yp = segmoid_function(yp)
    
    ym = (ipt[1] * obj[3]) + (ipt[3] * obj[7])
    ym = segmoid_function(ym)
    if xp == 1:
        return 1
    if xm == 1:
        return 2
    if yp == 1:
        return 3
    if ym == 1:
        return 4
    return 0

def generat_point(DISPLAY): #GENERATE PONTS FOR THE GAME
    global TX, TY
    x = random.randint(0, 59)
    y = random.randint(0, 59)
    x *= 10
    y *= 10
    TX = x
    TY = y
    pygame.draw.rect(DISPLAYSURF, RED, (x, y, 10, 10))

 
def random_objet(): # CREAT RANDOM PLAYER BY RANDOM NUMBER , THE OBJET HAS NUMBERS 
    obj = []
    for i in range(8):
        r = random.uniform(-1, 1.0)
        obj.append(r)
    return obj


def new_child(parent1, parent2): # CRIAT OBJET BY USING TOP ENGINS OF THE LAST TOP PLAYERS
    child = []
    for i in range(len(parent1)):
        r = random.random()
        if r <= 0.45:
            child.append(parent1[i])
        elif r <= 0.90:
            child.append(parent2[i])
        else:
            number_randomly = random.uniform(-1, 1)
            child.append(number_randomly)
    return child


def ferst_population(): # CRIAT FERTS 100 PLAYER RANDOMLY
    regestr = []
    for i in range(100):
        obj = random_objet()
        fet, x, y = calcule_fetness(obj)
        regestr.append([obj, fet, x, y])
    regestr.sort(key=by_fet, reverse=True)
    for i in range(2):
        print(regestr[i])
    return regestr


def ai_move(x, y, DISPLAYSURF, player): # MOVING OF THE PLAYER IN THE GAME
    global TX, TY, SCORE, BLACK, RED
    ipt = [x, y, TX, TY]

    res = make_dessision(ipt, player)
    if x == TX and y == TY:
        SCORE += 10
        generat_point(DISPLAYSURF)
        pygame.draw.rect(DISPLAYSURF, BLACK, (x, y, 10, 10))

    elif res == 2 and x >= 10:
        if DISPLAYSURF.get_at((x - 10, y)) == RED:
            SCORE += 10
            generat_point(DISPLAYSURF)
        pygame.draw.rect(DISPLAYSURF, BLACK, (x, y, 10, 10))
        x -= 10
    elif ( res == 1) and x < 590:
        if DISPLAYSURF.get_at((x + 10, y)) == RED:
            SCORE += 10
            generat_point(DISPLAYSURF)
        pygame.draw.rect(DISPLAYSURF, BLACK, (x, y, 10, 10))
        x += 10
    elif ( res == 4) and y >= 10:
        if DISPLAYSURF.get_at((x, y - 10)) == RED:
            SCORE += 10
            generat_point(DISPLAYSURF)
        pygame.draw.rect(DISPLAYSURF, BLACK, (x, y, 10, 10))
        y -= 10
    elif ( res == 3) and y < 590:
        if DISPLAYSURF.get_at((x, y + 10)) == RED:
            SCORE += 10
            generat_point(DISPLAYSURF)
        pygame.draw.rect(DISPLAYSURF, BLACK, (x, y, 10, 10))
        y += 10
    return x, y



# START THE PROGRAME
regestr = ferst_population()

while regestr[0][1] < FETNESS_GOAL:
    new_regestre = regestr[:10]
    for i in range(90):
        parent1 = random.choice(regestr[:50])
        parent2 = random.choice(regestr[:50])
        child = new_child(parent1[0], parent2[0])
        fet, x, y= calcule_fetness(child)
        new_regestre.append([child, fet, x, y])
    regestr = new_regestre
    regestr.sort(key=by_fet, reverse=True)
    for i in range(2):
        print(regestr[i])

player = regestr[0][0] 
pygame.init()
DISPLAYSURF = pygame.display.set_mode((600, 600))
pygame.display.set_caption('Game')
generat_point(DISPLAYSURF)
x = 0
y = 0
while True:
    rect = Rect(x, y, 10, 10)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    x, y = ai_move(x, y, DISPLAYSURF, player)
    pygame.draw.rect(DISPLAYSURF, GREEN, (x, y, 10, 10))
    pygame.display.update()

