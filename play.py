from time import *

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

pos=pygame.image.load('textures/possibility.png')

data_file='chess_table.csv'

lst = {1:blanc_pion,2:blanc_tour,3:blanc_cavalier,4:blanc_fou,5:blanc_dame,6:blanc_roi,
       11:noir_pion,12:noir_tour,13:noir_cavalier,14:noir_fou,15:noir_dame,16:noir_roi,
       21:pos}

table = [2,3,4,5,6,4,3,2,
         1,1,1,1,1,1,1,1,
         0,0,0,0,0,0,0,0,
         0,0,0,0,0,0,0,0,
         0,0,0,0,0,0,0,0,
         0,0,0,0,0,0,0,0,
         11,11,11,11,11,11,11,11,
         12,13,14,15,16,14,13,12]

def map():
    fenetre.blit(fond,(tile,tile))
    for y in range(8):
        for x in range(8):
            if table[y*8+x] != 0:
                fenetre.blit(lst[table[y*8+x]],((x+1)*tile,(y+1)*tile))

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

def txt():
    data=''
    for y in range(8):
        for x in range(8):
            data+=str(table[y*8+x])+','
        data+='\n'
    return data

set_data(data_file,txt())

def whereCanMove(nb,pos_x,pos_y):
    possibility=[]
    if nb == 1:
        if pos_y == 1:
            possibility.append((pos_x,3))
        possibility.append((pos_x,pos_y+1))
    elif nb == 11:
        if pos_y == 6:
            possibility.append((pos_x,4))
        possibility.append((pos_x,pos_y-1))
    return possibility

loop=True
pion=0
qt_pion=1
memx,memy=0,0

while loop==True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            loop = False            #fermeture de la fenetre (croix rouge)
        pos_x,pos_y=pygame.mouse.get_pos()
        pos_x,pos_y=pos_x-tile,pos_y-tile
        if pygame.mouse.get_pressed()[0] and 0 < pos_x < 8*tile and 0 < pos_y < 8*tile:
            if pion == 0:
                pion=table[pos_x//tile+pos_y//tile*8]
                table[pos_x//tile+pos_y//tile*8]=0
                if ( pion == 1 or pion == 11 ) and pos_x < 8*tile and pos_y < 8*tile:
                    lzt=whereCanMove(pion, pos_x//tile, pos_y//tile)
                    memx,memy=pos_x//tile,pos_y//tile
                    for i in range(len(lzt)):
                        (x,y)=lzt[i]
                        if table[x+y*8] == 0:
                            table[x+y*8]=21
            set_data(data_file,txt())
        elif pygame.mouse.get_pressed()[2] and 0 < pos_x < 8*tile and 0 < pos_y < 8*tile:
            if pion == 0:
                pass
            elif pion < 10:
                if table[pos_x//tile+pos_y//tile*8] == 0 or table[pos_x//tile+pos_y//tile*8] > 10:
                    if pion == 1 or pion == 11:
                        lzt=whereCanMove(pion, memx, memy)
                        for i in range(len(lzt)):
                            (x,y)=lzt[i]
                            table[x+y*8]=0
                    table[pos_x//tile+pos_y//tile*8]=pion
                    set_data(data_file,txt())
                    pion=0; qt_pion+=1
            elif pion > 10:
                if table[pos_x//tile+pos_y//tile*8] == 0 or table[pos_x//tile+pos_y//tile*8] < 10 or table[pos_x//tile+pos_y//tile*8] == 21:
                    if pion == 1 or pion == 11:
                        lzt=whereCanMove(pion, memx, memy)
                        for i in range(len(lzt)):
                            (x,y)=lzt[i]
                            table[x+y*8]=0
                    table[pos_x//tile+pos_y//tile*8]=pion
                    set_data(data_file,txt())
                    pion=0; qt_pion+=1
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