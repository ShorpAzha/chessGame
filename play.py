from time import *
from math import *

from client import client_send
from server import server_start

import os
import pygame

tile=64
LONG,LARG=tile*10,tile*10

pygame.init()
fenetre = pygame.display.set_mode((LONG, LARG))
pygame.display.set_caption("jeu d'aventure")
font = pygame.font.Font('freesansbold.ttf', 20)
frequence = pygame.time.Clock()

fond=pygame.image.load('textures/echequier.png')

blanc_pion=pygame.image.load('textures/blanc-pion.png')
blanc_tour=pygame.image.load('textures/blanc-tour.png')
blanc_cavalier=pygame.image.load('textures/blanc-cavalier.png')
blanc_fou=pygame.image.load('textures/blanc-fou.png')
blanc_dame=pygame.image.load('textures/blanc-dame.png')
blanc_roi=pygame.image.load('textures/blanc-roi.png')
noir_pion=pygame.image.load('textures/noir-poin.png')
noir_tour=pygame.image.load('textures/noir-tour.png')
noir_cavalier=pygame.image.load('textures/noir-cavalier.png')
noir_fou=pygame.image.load('textures/noir-fou.png')
noir_dame=pygame.image.load('textures/noir-dame.png')
noir_roi=pygame.image.load('textures/noir-roi.png')

# Curseurs
curseur=pygame.image.load('textures/curseur.png')
blanc_pion_curseur=pygame.image.load('textures/blanc-pion-curseur.png')
blanc_tour_curseur=pygame.image.load('textures/blanc-tour-curseur.png')
blanc_cavalier_curseur=pygame.image.load('textures/blanc-cavalier-curseur.png')
blanc_fou_curseur=pygame.image.load('textures/blanc-fou-curseur.png')
blanc_dame_curseur=pygame.image.load('textures/blanc-dame-curseur.png')
blanc_roi_curseur=pygame.image.load('textures/blanc-roi-curseur.png')
noir_pion_curseur=pygame.image.load('textures/noir-poin-curseur.png')
noir_tour_curseur=pygame.image.load('textures/noir-tour-curseur.png')
noir_cavalier_curseur=pygame.image.load('textures/noir-cavalier-curseur.png')
noir_fou_curseur=pygame.image.load('textures/noir-fou-curseur.png')
noir_dame_curseur=pygame.image.load('textures/noir-dame-curseur.png')
noir_roi_curseur=pygame.image.load('textures/noir-roi-curseur.png')

pos=pygame.image.load('textures/possibility.png')
superpos=pygame.image.load('textures/superpos.png')

data_file='chess_table.csv'

lst = {1:blanc_pion,2:blanc_tour,3:blanc_cavalier,4:blanc_fou,5:blanc_dame,6:blanc_roi,
       11:noir_pion,12:noir_tour,13:noir_cavalier,14:noir_fou,15:noir_dame,16:noir_roi,
       21:pos,25:superpos,
       100:curseur,
       101:blanc_pion_curseur,102:blanc_tour_curseur,103:blanc_cavalier_curseur,
       104:blanc_fou_curseur,105:blanc_dame_curseur,106:blanc_roi_curseur,
       111:noir_pion_curseur,112:noir_tour_curseur,113:noir_cavalier_curseur,
       114:noir_fou_curseur,115:noir_dame_curseur,116:noir_roi_curseur}

table = [2,3,4,5,6,4,3,2,
         1,1,1,1,1,1,1,1,
         0,0,0,0,0,0,0,0,
         0,0,0,0,0,0,0,0,
         0,0,0,0,0,0,0,0,
         0,0,0,0,0,0,0,0,
         11,11,11,11,11,11,11,11,
         12,13,14,15,16,14,13,12,0]

def map():
    fenetre.blit(fond,(tile,tile))
    for y in range(8):
        for x in range(8):
            if table[y*8+x] != 0 and table[y*8+x] < 50:
                fenetre.blit(lst[table[y*8+x]],((x+1)*tile,(y+1)*tile))
            elif table[y*8+x] > 50:
                fenetre.blit(lst[table[y*8+x]-50],((x+1)*tile,(y+1)*tile))
                fenetre.blit(lst[25],((x+1)*tile,(y+1)*tile))

def get_data(filename):
    file=open(filename)
    content=file.read()
    file.close()
    return content

def set_data(filename,string=''):
    file=open(filename,'w')
    file.write(str(string))
    file.close()
    return get_data(filename)

def thisIsATable(filename=data_file):
    content=get_data(filename)
    table=[]; ctr=''
    for i in content:
        if i == ',': table.append(int(ctr)); ctr=''
        elif i == '\n': pass
        else: ctr+=i
    return table

def txt():
    data=''
    for y in range(8):
        for x in range(8):
            data+=str(table[y*8+x])+','
        data+='\n'
    return data

def Btw(n,m):
    if 0 <= n < 8 and 0 <= m < 8: return True
    else: return False

def sqt(posx,posy,x,y):
    return sqrt((posx-x)**2+(posy-y)**2)

set_data(data_file,txt())

def whereCanMove(nb,pos_x,pos_y):
    possibility=[(pos_x,pos_y)]
    coli=[(0,0),(7,0),(0,0),(0,7)]
    cavalier_dep=[(-2,-1),(-1,2),(2,1),(1,2),(2,-1),(-1,-2),(-2,1),(1,-2)]
    roi_dep=[(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]
    if nb == 1:
        if 7 >= pos_x-1 >= 0 and 7 >= pos_y+1 >= 0 and table[pos_x-1+(pos_y+1)*8] != 0: possibility.append((pos_x-1,pos_y+1))
        if 7 >= pos_x+1 >= 0 and 7 >= pos_y+1 >= 0 and table[pos_x+1+(pos_y+1)*8] != 0: possibility.append((pos_x+1,pos_y+1))
        if pos_y == 1 and table[pos_x+24] == 0: possibility.append((pos_x,3))
        if pos_y <= 6 and table[pos_x+(pos_y+1)*8] == 0: possibility.append((pos_x,pos_y+1))
        elif pos_y == 7 or table[pos_x+(pos_y+1)*8] != 0: possibility.append((pos_x,pos_y))
    elif nb == 2 or nb == 12:
        # colisions
        colip,colim=False,False
        colipp,colimm=False,False
        for i in range(1,8):
            if 0 <= pos_x+i < 8 and table[pos_y*8+pos_x+i] != 0 and colip == False:
                coli.pop(1)
                coli.insert(1,(pos_x+i,pos_y))
                colip=True
            if 0 <= pos_x-i < 8 and table[pos_y*8+pos_x-i] != 0 and colim == False:
                coli.pop(0)
                coli.insert(0,(pos_x-i,pos_y))
                colim=True
            if 0 <= pos_y+i < 8 and table[(pos_y+i)*8+pos_x] != 0 and colipp == False:
                coli.pop(3)
                coli.insert(3,(pos_x,pos_y+i))
                colipp=True
            if 0 <= pos_y-i < 8 and table[(pos_y-i)*8+pos_x] != 0 and colimm == False:
                coli.pop(2)
                coli.insert(2,(pos_x,pos_y-i))
                colimm=True
        for k in range(coli[0][0],coli[1][0]+1):
            if pos_x != k:
                possibility.append((k,pos_y))
        for l in range(coli[2][1],coli[3][1]+1):
            if pos_y != l:
                possibility.append((pos_x,l))
    elif nb == 3 or nb == 13:
        for i in cavalier_dep:
            (x,y)=i
            if 7 >= pos_x+x >= 0 and 7 >= pos_y+y >= 0:
                possibility.append((pos_x+x,pos_y+y))
    elif nb == 4 or nb == 14:
        lines=[]
        # Bordures
        for i in range(8):
            if Btw(pos_x-i,pos_y-i) == True:
                coli.pop(0)
                coli.insert(0,(pos_x-i,pos_y-i))
            if Btw(pos_x+i,pos_y+i) == True:
                coli.pop(1)
                coli.insert(1,(pos_x+i,pos_y+i))
            if Btw(pos_x-i,pos_y+i) == True:
                coli.pop(2)
                coli.insert(2,(pos_x-i,pos_y+i))
            if Btw(pos_x+i,pos_y-i) == True:
                coli.pop(3)
                coli.insert(3,(pos_x+i,pos_y-i))
        # Lines
        pa_x,pa_y=coli[0][0],coli[0][1]
        pb_x,pb_y=coli[2][0],coli[2][1]
        while pa_x != coli[1][0]+1:
            lines.append((pa_x,pa_y))
            pa_x,pa_y=pa_x+1,pa_y+1
        while pb_x != coli[3][0]+1:
            lines.append((pb_x,pb_y))
            pb_x,pb_y=pb_x+1,pb_y-1
        # Colisions
        ma=[None,None,None,None]
        for i in range(len(lines)):
            (x,y)=lines[i]
            if table[y*8+x] == 0:
                pass
            elif x < pos_x and y < pos_y and ( ma[0] == None or ma[0][2] > sqt(pos_x,pos_y,x,y) ):
                ma.pop(0); ma.insert(0,(x,y,sqt(pos_x,pos_y,x,y)))
            elif x > pos_x and y > pos_y and ( ma[1] == None or ma[1][2] > sqt(pos_x,pos_y,x,y) ):
                ma.pop(1); ma.insert(1,(x,y,sqt(pos_x,pos_y,x,y)))
            elif x < pos_x and y > pos_y and ( ma[2] == None or ma[2][2] > sqt(pos_x,pos_y,x,y) ):
                ma.pop(2); ma.insert(2,(x,y,sqt(pos_x,pos_y,x,y)))
            elif x > pos_x and y < pos_y and ( ma[3] == None or ma[3][2] > sqt(pos_x,pos_y,x,y) ):
                ma.pop(3); ma.insert(3,(x,y,sqt(pos_x,pos_y,x,y)))
        mb=ma
        if not(ma[0] != None): mb.pop(0); mb.insert(0,(coli[0][0],coli[0][1],0))
        if not(ma[1] != None): mb.pop(1); mb.insert(1,(coli[1][0],coli[1][1],0))
        if not(ma[2] != None): mb.pop(2); mb.insert(2,(coli[2][0],coli[2][1],0))
        if not(ma[3] != None): mb.pop(3); mb.insert(3,(coli[3][0],coli[3][1],0))
        for i in range(len(lines)):
            (x,y)=lines[i]
            if x != pos_x and y != pos_y:
                if mb[0][0] <= x <= mb[1][0] and mb[0][1] <= y <= mb[1][1]:
                    possibility.append((x,y))
                elif mb[2][0] <= x <= mb[3][0] and mb[2][1] >= y >= mb[3][1]:
                    possibility.append((x,y))
    elif nb == 5 or nb == 15:
        lines=[]
        # Bordures
        for i in range(8):
            if Btw(pos_x-i,pos_y-i) == True:
                coli.pop(0)
                coli.insert(0,(pos_x-i,pos_y-i))
            if Btw(pos_x+i,pos_y+i) == True:
                coli.pop(1)
                coli.insert(1,(pos_x+i,pos_y+i))
            if Btw(pos_x-i,pos_y+i) == True:
                coli.pop(2)
                coli.insert(2,(pos_x-i,pos_y+i))
            if Btw(pos_x+i,pos_y-i) == True:
                coli.pop(3)
                coli.insert(3,(pos_x+i,pos_y-i))
        # Lines
        pa_x,pa_y=coli[0][0],coli[0][1]
        pb_x,pb_y=coli[2][0],coli[2][1]
        while pa_x != coli[1][0]+1:
            lines.append((pa_x,pa_y))
            pa_x,pa_y=pa_x+1,pa_y+1
        while pb_x != coli[3][0]+1:
            lines.append((pb_x,pb_y))
            pb_x,pb_y=pb_x+1,pb_y-1
        # Colisions
        ma=[None,None,None,None]
        for i in range(len(lines)):
            (x,y)=lines[i]
            if table[y*8+x] == 0:
                pass
            elif x < pos_x and y < pos_y and ( ma[0] == None or ma[0][2] > sqt(pos_x,pos_y,x,y) ):
                ma.pop(0); ma.insert(0,(x,y,sqt(pos_x,pos_y,x,y)))
            elif x > pos_x and y > pos_y and ( ma[1] == None or ma[1][2] > sqt(pos_x,pos_y,x,y) ):
                ma.pop(1); ma.insert(1,(x,y,sqt(pos_x,pos_y,x,y)))
            elif x < pos_x and y > pos_y and ( ma[2] == None or ma[2][2] > sqt(pos_x,pos_y,x,y) ):
                ma.pop(2); ma.insert(2,(x,y,sqt(pos_x,pos_y,x,y)))
            elif x > pos_x and y < pos_y and ( ma[3] == None or ma[3][2] > sqt(pos_x,pos_y,x,y) ):
                ma.pop(3); ma.insert(3,(x,y,sqt(pos_x,pos_y,x,y)))
        mb=ma
        if not(ma[0] != None): mb.pop(0); mb.insert(0,(coli[0][0],coli[0][1],0))
        if not(ma[1] != None): mb.pop(1); mb.insert(1,(coli[1][0],coli[1][1],0))
        if not(ma[2] != None): mb.pop(2); mb.insert(2,(coli[2][0],coli[2][1],0))
        if not(ma[3] != None): mb.pop(3); mb.insert(3,(coli[3][0],coli[3][1],0))
        for i in range(len(lines)):
            (x,y)=lines[i]
            if x != pos_x and y != pos_y:
                if mb[0][0] <= x <= mb[1][0] and mb[0][1] <= y <= mb[1][1]:
                    possibility.append((x,y))
                elif mb[2][0] <= x <= mb[3][0] and mb[2][1] >= y >= mb[3][1]:
                    possibility.append((x,y))
        # la croix de l'angleterre
        coli=[(0,0),(7,0),(0,0),(0,7)]
        # colisions
        colip,colim=False,False
        colipp,colimm=False,False
        for i in range(1,8):
            if 0 <= pos_x+i < 8 and table[pos_y*8+pos_x+i] != 0 and colip == False:
                coli.pop(1)
                coli.insert(1,(pos_x+i,pos_y))
                colip=True
            if 0 <= pos_x-i < 8 and table[pos_y*8+pos_x-i] != 0 and colim == False:
                coli.pop(0)
                coli.insert(0,(pos_x-i,pos_y))
                colim=True
            if 0 <= pos_y+i < 8 and table[(pos_y+i)*8+pos_x] != 0 and colipp == False:
                coli.pop(3)
                coli.insert(3,(pos_x,pos_y+i))
                colipp=True
            if 0 <= pos_y-i < 8 and table[(pos_y-i)*8+pos_x] != 0 and colimm == False:
                coli.pop(2)
                coli.insert(2,(pos_x,pos_y-i))
                colimm=True
        for k in range(coli[0][0],coli[1][0]+1):
            if pos_x != k:
                possibility.append((k,pos_y))
        for l in range(coli[2][1],coli[3][1]+1):
            if pos_y != l:
                possibility.append((pos_x,l))
    elif nb == 6 or nb == 16:
        for i in roi_dep:
            (x,y)=i
            if 7 >= pos_x+x >= 0 and 7 >= pos_y+y >= 0:
                possibility.append((pos_x+x,pos_y+y))
    elif nb == 11:
        if 7 >= pos_x-1 >= 0 and 7 >= pos_y-1 >= 0 and table[pos_x-1+(pos_y-1)*8] != 0: possibility.append((pos_x-1,pos_y-1))
        if 7 >= pos_x+1 >= 0 and 7 >= pos_y-1 >= 0 and table[pos_x+1+(pos_y-1)*8] != 0: possibility.append((pos_x+1,pos_y-1))
        if pos_y == 6 and table[pos_x+32] == 0: possibility.append((pos_x,4))
        if pos_y >= 1 and table[pos_x+(pos_y-1)*8] == 0: possibility.append((pos_x,pos_y-1))
        elif pos_y == 0 or table[pos_x+(pos_y-1)*8]: possibility.append((pos_x,pos_y))
    return possibility

loop=True
pion=0
qt_pion=1
memx,memy=0,0
oldx,oldy=0,0

while loop==True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            loop = False            #fermeture de la fenetre (croix rouge)
        pos_x,pos_y=pygame.mouse.get_pos()
        pos_x,pos_y=pos_x-tile,pos_y-tile
        
        # Curseurs
        cursor = lst[pion+100].convert_alpha()
        cursorr = pygame.cursors.Cursor((0,0), cursor)
        pygame.mouse.set_cursor(cursorr)
        if pygame.mouse.get_pressed()[0] and 0 < pos_x < 8*tile and 0 < pos_y < 8*tile:
            if pion == 0 and table[pos_y//tile*8+pos_x//tile] != 0:
                pion=table[pos_x//tile+pos_y//tile*8]
                table[pos_x//tile+pos_y//tile*8]=0
                oldx,oldy=pos_x//tile,pos_y//tile
                set_data(data_file,txt())
                lzt=whereCanMove(pion, pos_x//tile, pos_y//tile)
                memx,memy=pos_x//tile,pos_y//tile
                for i in range(len(lzt)):
                    (x,y)=lzt[i]
                    if table[x+y*8] == 0: table[x+y*8]=21
                    elif pion < 10 and table[x+y*8] > 10: table[x+y*8]+=50
                    elif pion > 10 and table[x+y*8] < 10: table[x+y*8]+=50
        elif pygame.mouse.get_pressed()[2] and 0 < pos_x < 8*tile and 0 < pos_y < 8*tile:
            if pion == 0:
                pass
            elif 0 < pion < 10:
                if table[pos_x//tile+pos_y//tile*8] == 0 or table[pos_x//tile+pos_y//tile*8] > 10:
                    #if pion == 1 or pion == 2 or pion == 3 or pion == 4 or pion == 6:
                    isPossible=False
                    table=thisIsATable()
                    lzt=whereCanMove(pion, memx, memy)
                    for i in range(len(lzt)):
                        (x,y)=lzt[i]
                        if pos_x//tile == x and pos_y//tile == y:
                            table[pos_x//tile+pos_y//tile*8]=pion
                            isPossible=True
                    set_data(data_file,txt())
                    if isPossible:
                        pion=0
                        if oldx != pos_x//tile and oldy != pos_y//tile: qt_pion+=1
            elif pion > 10:
                if table[pos_x//tile+pos_y//tile*8] == 0 or table[pos_x//tile+pos_y//tile*8] < 10 or table[pos_x//tile+pos_y//tile*8] > 20:
                    #if pion == 11 or pion == 12 or pion == 13 or pion == 14 or pion == 16:
                    isPossible=False
                    table=thisIsATable()
                    lzt=whereCanMove(pion, memx, memy)
                    for i in range(len(lzt)):
                        (x,y)=lzt[i]
                        if pos_x//tile == x and pos_y//tile ==y:
                            table[pos_x//tile+pos_y//tile*8]=pion
                            isPossible=True
                    set_data(data_file,txt())
                    if isPossible:
                        pion=0
                        if oldx != pos_x//tile and oldy != pos_y//tile: qt_pion+=1
            if qt_pion % 2 == 0:
                texte = font.render(f'Au tour des Noirs', True, (255, 255, 255))
            else:
                texte = font.render(f'Au tour des Blancs', True, (255, 255, 255))
            pygame.draw.rect(fenetre, (0,0,0), (0,0,10*tile,tile),0)
            fenetre.blit(texte,(10,10))
        map()

    # Actualisation de l'affichage
    frequence.tick(60)
    pygame.display.update()
pygame.quit()