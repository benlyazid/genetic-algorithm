import pygame
import sys
import random
from pygame.locals import *
from pygame.rect import *
import math

RED = (255,   0,   0)
GREEN = (25,   100,   0)
BLACK = (0, 0, 0)
width = 600
height = 600
SCORE = 0
MOVE = 0
TX = 0
TY = 0

def by_fet(elem):
    return abs(elem[1])

    

def segmoid_function(gamma):
    if gamma < 0:
       res = 1 - 1 / (1 + math.exp(gamma))
    else:
        res = 1 / (1 + math.exp(-gamma))
    if res < 0.5:
        return 1
    return 0

def generate_point_for_fetness(score):
    mx = 0
    my = 0
    tx = 0
    ty = 0
    global TX, TY
    '''if score == 0:
        mx = random.randint(0, 29) * 10
        my = random.randint(0, 59) * 10
        tx = random.randint(30, 59) * 10
        ty = random.randint(0, 59) * 10
    elif score == 10:
        mx = random.randint(30, 59) * 10
        my = random.randint(0, 59) * 10
        tx = random.randint(0, 29) * 10
        ty = random.randint(0, 59) * 10

    elif score == 20:
        my = random.randint(0, 29) * 10
        mx = random.randint(0, 59) * 10
        ty = random.randint(30, 59) * 10
        tx = random.randint(0, 59) * 10
    elif score == 30:
        my = random.randint(30, 59) * 10
        mx = random.randint(0, 59) * 10
        ty = random.randint(0, 29) * 10
        tx = random.randint(0, 59) * 10
    else:'''
    while abs(mx - tx) + abs (my - ty) < 30:
        mx = random.randint(0, 59) * 10
        my = random.randint(0, 59) * 10
        tx = random.randint(0, 59) * 10
        ty = random.randint(0, 59) * 10
    TX = tx
    TY = ty


    return mx, my, tx, ty

def calcule_fetness(obj):
    move = 0
    dest = 0
    mx = 0
    my = 0
    tx = 0
    ty = 0 
    score = 0
    mx, my, tx, ty = generate_point_for_fetness(score)
    dest = abs(tx - mx) + abs(ty - my)
    i = 0
    while i < 200:
    #for i in range(200):
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
            if score == 1000:
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


def make_dessision(ipt, obj):
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


def generat_maze(DISPLAY):
    for y in range(height):
        if y % 20 == 0 and y != 0:
            for i in range(40):
                z = random.randint(0, 60)
                z *= 10
                pygame.draw.rect(DISPLAYSURF, RED, (z, y, 10, 10))


def generat_point(DISPLAY):
    global TX, TY

    x = random.randint(0, 59)
    y = random.randint(0, 59)
    x *= 10
    y *= 10
    TX = x
    TY = y
    pygame.draw.rect(DISPLAYSURF, RED, (x, y, 10, 10))


def moving(x, y, DISPLAYSURF, auto_player, player):
    global SCORE
    global MOVE
    global TX, TY
    ipt = [x, y, TX, TY]
    res = 0
    if auto_player == True:
        res = make_dessision(ipt, player)

    if event.type == pygame.KEYDOWN:
        if (event.key == pygame.K_LEFT or res == 1) and x >= 10:
            if DISPLAYSURF.get_at((x - 10, y)) == RED:
                SCORE += 10
                print(str(SCORE))
                generat_point(DISPLAYSURF)
            MOVE += 1
            pygame.draw.rect(DISPLAYSURF, BLACK, (x, y, 10, 10))
            x -= 10
        if (event.key == pygame.K_RIGHT or res == 2) and x < 590:
            if DISPLAYSURF.get_at((x + 10, y)) == RED:
                SCORE += 10
                print(str(SCORE))
                generat_point(DISPLAYSURF)
            MOVE += 1
            pygame.draw.rect(DISPLAYSURF, BLACK, (x, y, 10, 10))
            x += 10

        if (event.key == pygame.K_UP or res == 3) and y >= 10:
            if DISPLAYSURF.get_at((x, y - 10)) == RED:
                SCORE += 10
                print(str(SCORE))
                generat_point(DISPLAYSURF)
            pygame.draw.rect(DISPLAYSURF, BLACK, (x, y, 10, 10))
            y -= 10
            MOVE += 1
        if (event.key == pygame.K_DOWN or res == 4) and y < 590:
            if DISPLAYSURF.get_at((x, y + 10)) == RED:
                SCORE += 10
                print(str(SCORE))
                generat_point(DISPLAYSURF)
            pygame.draw.rect(DISPLAYSURF, BLACK, (x, y, 10, 10))
            y += 10
            MOVE += 1

    # AUTO PLAYER7
    if res == 2 and x >= 10:
        if DISPLAYSURF.get_at((x - 10, y)) == RED:
            SCORE += 10
            print(str(SCORE))
            generat_point(DISPLAYSURF)
        MOVE += 1
        pygame.draw.rect(DISPLAYSURF, BLACK, (x, y, 10, 10))
        x -= 10
    if ( res == 1) and x < 590:
        if DISPLAYSURF.get_at((x + 10, y)) == RED:
            SCORE += 10
            print(str(SCORE))
            generat_point(DISPLAYSURF)
        MOVE += 1
        pygame.draw.rect(DISPLAYSURF, BLACK, (x, y, 10, 10))
        x += 10

    if ( res == 4) and y >= 10:
        if DISPLAYSURF.get_at((x, y - 10)) == RED:
            SCORE += 10
            print(str(SCORE))
            generat_point(DISPLAYSURF)
        pygame.draw.rect(DISPLAYSURF, BLACK, (x, y, 10, 10))
        y -= 10
        MOVE += 1
    if ( res == 3) and y < 590:
        if DISPLAYSURF.get_at((x, y + 10)) == RED:
            SCORE += 10
            print(str(SCORE))
            generat_point(DISPLAYSURF)
        pygame.draw.rect(DISPLAYSURF, BLACK, (x, y, 10, 10))
        y += 10
        MOVE += 1
    return x, y


def random_objet():
    obj = []
    for i in range(8):
        r = random.uniform(-1, 1.0)
        obj.append(r)
    return obj


def new_child(parent1, parent2):
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


def ferst_population():
    regestr = []
    for i in range(100):
        obj = random_objet()
        fet, x, y = calcule_fetness(obj)
        regestr.append([obj, fet, x, y])
    regestr.sort(key=by_fet, reverse=True)
    for i in range(2):
        print(regestr[i])
    print('-------------------Next Generation1')
    return regestr


def ai_move(x, y, DISPLAYSURF, player):
    global TX, TY, SCORE, MOVE, BLACK, RED
    ipt = [x, y, TX, TY]

    res = make_dessision(ipt, player)
    if x == TX and y == TY:
        SCORE += 10
        #print(str(SCORE))
        generat_point(DISPLAYSURF)
        MOVE += 1
        pygame.draw.rect(DISPLAYSURF, BLACK, (x, y, 10, 10))

    elif res == 2 and x >= 10:
        if DISPLAYSURF.get_at((x - 10, y)) == RED:
            SCORE += 10
        #print(str(SCORE))
            generat_point(DISPLAYSURF)
        MOVE += 1
        pygame.draw.rect(DISPLAYSURF, BLACK, (x, y, 10, 10))
        x -= 10
    elif ( res == 1) and x < 590:
        if DISPLAYSURF.get_at((x + 10, y)) == RED:
            SCORE += 10
        #print(str(SCORE))
            generat_point(DISPLAYSURF)
        MOVE += 1
        pygame.draw.rect(DISPLAYSURF, BLACK, (x, y, 10, 10))
        x += 10

    elif ( res == 4) and y >= 10:
        if DISPLAYSURF.get_at((x, y - 10)) == RED:
            SCORE += 10
        #print(str(SCORE))
            generat_point(DISPLAYSURF)
        pygame.draw.rect(DISPLAYSURF, BLACK, (x, y, 10, 10))
        y -= 10
        MOVE += 1
    elif ( res == 3) and y < 590:
        if DISPLAYSURF.get_at((x, y + 10)) == RED:
            SCORE += 10
        #print(str(SCORE))
            generat_point(DISPLAYSURF)
        pygame.draw.rect(DISPLAYSURF, BLACK, (x, y, 10, 10))
        y += 10
        MOVE += 1
    return x, y






regestr = ferst_population()

while regestr[1][1] < 1000:
    new_regestre = regestr[:10]
    for i in range(90):
        parent1 = random.choice(regestr[:50])
        parent2 = random.choice(regestr[:50])
        child = new_child(parent1[0], parent2[0])
        #print(child)
        fet, x, y= calcule_fetness(child)
        new_regestre.append([child, fet, x, y])
    regestr = new_regestre
    regestr.sort(key=by_fet, reverse=True)
    for i in range(2):
        print(regestr[i])
    print('-------------------Next Generation')


player = regestr[0][0] 

print('-------------------L it s Fucking Play')


'''
file = open('playerAi.txt', 'w+')
for i in range(len(player)):
    txt = str(player[i])
    file.write(txt)
    file.write('\n')  
'''
pygame.init()
DISPLAYSURF = pygame.display.set_mode((600, 600))
pygame.display.set_caption('Snack Game')
#generat_maze(DISPLAYSURF)
#pygame.draw.rect(DISPLAYSURF, GREEN, (0, 0, 10, 10))
generat_point(DISPLAYSURF)


x = 0
y = 0
i = 0
while True:
    rect = Rect(x, y, 10, 10)
    for event in pygame.event.get():
    #while SCORE != 100:
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        #x, y =  moving(x, y, DISPLAYSURF, True, player)
    #print('I AM IN {} {} | TARGET IS {} {} | WITH SCORE {}'.format(x, y, TX, TY, SCORE))
    x, y = ai_move(x, y, DISPLAYSURF, player)
    
    pygame.draw.rect(DISPLAYSURF, GREEN, (x, y, 10, 10))
    pygame.display.update()

