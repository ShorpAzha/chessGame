import pygame

tile=16
LONG,LARG=tile*8,tile*8

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

lst = {1:blanc_pion,2:blanc_tour,3:blanc_cavalier,4:blanc_fou,5:blanc_dame,6:blanc_roi,
       11:noir_pion,12:noir_tour,13:noir_cavalier,14:noir_fou,15:noir_dame,16:noir_roi}
table = [2,3,4,5,6,4,3,2,
         1,1,1,1,1,1,1,1,
         0,0,0,0,0,0,0,0,
         0,0,0,0,0,0,0,0,
         0,0,0,0,0,0,0,0,
         0,0,0,0,0,0,0,0,
         11,11,11,11,11,11,11,11,
         12,13,14,15,16,14,13,12]

def map():
    fenetre.blit(fond,(0,0))
    for y in range(8):
        for x in range(8):
            if table[y*8+x] != 0:
                fenetre.blit(lst[table[y*8+x]],(x*16,y*16))

loop=True
while loop==True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            loop = False            #fermeture de la fenetre (croix rouge)
        pos_x,pos_y=pygame.mouse.get_pos()
        fenetre.blit(lst[1],(int(pos_x/tile)*tile,int(pos_y/tile)*tile))
        map()

    # Actualisation de l'affichage
    frequence.tick(60)
    pygame.display.update()
pygame.quit()