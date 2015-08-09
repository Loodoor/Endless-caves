#-*- coding:Utf-8 -*

import sys
import os
import pygame
import time
import pickle
from random import randrange
from classes import *



VERSION=0.1



fond=pygame.image.load("images/fond.bmp")

def placer_salles(niveau):


    # GENERATION DE L'EMPLACEMENT DES SALLES


    nombre_de_salles=randrange(8+niveau,10+(2*niveau)) # Création du tableau contenant l'emplacement des salles
    if nombre_de_salles>150:
        nombre_de_salles=150

    tableau=[]
    for i in range(nombre_de_salles+1):
        tableau.append([0]*nombre_de_salles)



    x=nombre_de_salles//2 # Initialisation de certaines variables
    y=nombre_de_salles//2
    tableau[y][x]=2
    i=0
    nombre_de_salles_au_tresor_verouillees=randrange(niveau+1)
    while i<(nombre_de_salles+nombre_de_salles_au_tresor_verouillees):
        n=randrange(4)
        m=randrange(1000)
        if m>=0 and m<=25: # Choix du type de salle
            l=2
        else:
            l=0
        if i>nombre_de_salles-1: # Création salles au trésor vérouillées
            while True:
                xa=randrange(nombre_de_salles)
                ya=randrange(nombre_de_salles)
                try:
                    if tableau[ya][xa]==0 and ( (tableau[ya+1][xa]!=0 and tableau[ya+1][xa]!=5)
                                                or (tableau[ya-1][xa]!=0 and tableau[ya-1][xa]!=5)
                                                or (tableau[ya][xa+1]!=0 and tableau[ya][xa+1]!=5)
                                                or (tableau[ya][xa-1]!=0 and tableau[ya][xa-1]!=5)):
                        tableau[ya][xa]=5
                        i+=1
                        break
                except:
                    continue
            continue
        if i==nombre_de_salles-1-nombre_de_salles_au_tresor_verouillees: # Création salle du boss
            l=3

        if n==0 and x<(nombre_de_salles-1): # Remplissage de tableau
            if tableau[y][x+1]==0:
                tableau[y][x+1]=1+l
                i+=1
            x+=1
        if n==1 and x>0:
            if tableau[y][x-1]==0:
                tableau[y][x-1]=1+l
                i+=1
            x-=1
        if n==2 and y<(nombre_de_salles-1):
            if tableau[y+1][x]==0:
                tableau[y+1][x]=1+l
                i+=1
            y+=1
        if n==3 and y>0:
            if tableau[y-1][x]==0:
                tableau[y-1][x]=1+l
                i+=1
            y-=1



    map=Map(nombre_de_salles+1+nombre_de_salles_au_tresor_verouillees) # Creation de la variable *map*
    map.salles=[]
    for i in range(map.nombre_de_salles):
        map.salles.append(Salle())

    for i in range(len(tableau)): # Initialisation de la carte du niveau
        map.carte_map.append([])
        for j in range(len(tableau[i])):
            map.carte_map[i].append(tableau[i][j])

    map.niveau=niveau # Initialisation du niveau dans la variable *map*

    liste=[] # Créations de listes contenant le type et l'emplacement des salles
    liste_x=[]
    liste_y=[]

    for j in range(nombre_de_salles):
        for k in range(nombre_de_salles):
            if tableau[j][k]!=0:
                liste.append(tableau[j][k])
                liste_x.append(k)
                liste_y.append(j)
                tableau[j][k]=0

    for i in range(map.nombre_de_salles): # Initialisation du type et de l'emplacement des salles dans *map*
        map.salles[i].type_salle=liste[i]
        map.salles[i].x=liste_x[i]
        map.salles[i].y=liste_y[i]

    return map

def generer_salles(map):

    fichier=open("patterns.txt","r") # Obtention des patterns de salles

    chaine_obtenue=fichier.read()
    liste_paternes=chaine_obtenue.split("\n")

    for i in range(len(liste_paternes)):
        liste_paternes[i]=liste_paternes[i].split(" ")

    for i in range(map.nombre_de_salles): # Remplissage des salles dans la variable *map*

        if map.salles[i].type_salle==1: # Remplissage des salles de type normal
            a=randrange(int(len(liste_paternes)/10))
            chaine_a_obtenir=[str(a)]
            j=0
            chaine_obtenue=""

            while chaine_a_obtenir!=chaine_obtenue:
                chaine_obtenue=liste_paternes[j]
                j+=1

            while liste_paternes[j]!=[str(a+1)]:
                for l in range(9):
                    map.salles[i].blocs_type.append(list())
                    for k in range(15):
                        map.salles[i].blocs_type[l].append(liste_paternes[j][k])
                    j+=1

            h=0
            g=0
            for j in range(9): # Recherche d'objets potentiels et d'ennemis potentiels

                for k in range(15):

                    if map.salles[i].blocs_type[j][k]=="1001":

                        map.salles[i].blocs_type[j][k]=1
                        map.salles[i].objets_potentiels.append(Objet())
                        map.salles[i].objets_potentiels[h].x=k*64
                        map.salles[i].objets_potentiels[h].y=j*64
                        h+=1

                    elif map.salles[i].blocs_type[j][k]=="2000":

                        map.salles[i].blocs_type[j][k]=0
                        map.salles[i].ennemis_potentiels.append(Ennemis())
                        map.salles[i].ennemis_potentiels[g].x=k*64
                        map.salles[i].ennemis_potentiels[g].y=j*64
                        g+=1

        elif map.salles[i].type_salle==2\
        or map.salles[i].type_salle==3\
        or map.salles[i].type_salle==5: # Remplissage du spawn et des salles au trésor

            map.salles[i].blocs_type=\
        [
            [9,2,2,2,2,2,2,2,2,2,2,2,2,2,8],
            [3,0,0,0,0,0,0,0,0,0,0,0,0,0,3],
            [3,0,0,0,0,0,0,0,0,0,0,0,0,0,3],
            [3,0,0,0,0,0,0,0,0,0,0,0,0,0,3],
            [3,0,0,0,0,0,0,0,0,0,0,0,0,0,3],
            [3,0,0,0,0,0,0,0,0,0,0,0,0,0,3],
            [3,0,0,0,0,0,0,0,0,0,0,0,0,0,3],
            [3,0,0,0,0,0,0,0,0,0,0,0,0,0,3],
            [11,2,2,2,2,2,2,2,2,2,2,2,2,2,10],
        ]

        elif map.salles[i].type_salle==4: # Remplissage des salles du boss

            map.salles[i].blocs_type=\
        [
            [9,2,2,2,2,2,2,2,2,2,2,2,2,2,8],
            [3,0,0,1,0,0,0,0,0,0,0,1,0,0,3],
            [3,1,0,0,0,0,0,0,0,0,0,0,0,1,3],
            [3,0,0,0,0,0,0,0,0,0,0,0,0,0,3],
            [3,0,0,0,0,0,0,12,0,0,0,0,0,0,3],
            [3,0,0,0,0,0,0,0,0,0,0,0,0,0,3],
            [3,1,0,0,0,0,0,0,0,0,0,0,0,1,3],
            [3,0,0,1,0,0,0,0,0,0,0,1,0,0,3],
            [11,2,2,2,2,2,2,2,2,2,2,2,2,2,10],
        ]

        for j in range(map.nombre_de_salles): # Création des portes

                if map.salles[i].x+1==map.salles[j].x and map.salles[i].y==map.salles[j].y and map.salles[j].type_salle!=5:
                    map.salles[i].blocs_type[4][14]=6

                if map.salles[i].x-1==map.salles[j].x and map.salles[i].y==map.salles[j].y and map.salles[j].type_salle!=5:
                    map.salles[i].blocs_type[4][0]=7

                if map.salles[i].y+1==map.salles[j].y and map.salles[i].x==map.salles[j].x and map.salles[j].type_salle!=5:
                    map.salles[i].blocs_type[8][7]=5

                if map.salles[i].y-1==map.salles[j].y and map.salles[i].x==map.salles[j].x and map.salles[j].type_salle!=5:
                    map.salles[i].blocs_type[0][7]=4

                if map.salles[i].x+1==map.salles[j].x and map.salles[i].y==map.salles[j].y and map.salles[j].type_salle==5:
                    map.salles[i].blocs_type[4][14]=20

                if map.salles[i].x-1==map.salles[j].x and map.salles[i].y==map.salles[j].y and map.salles[j].type_salle==5:
                    map.salles[i].blocs_type[4][0]=21

                if map.salles[i].y+1==map.salles[j].y and map.salles[i].x==map.salles[j].x and map.salles[j].type_salle==5:
                    map.salles[i].blocs_type[8][7]=19

                if map.salles[i].y-1==map.salles[j].y and map.salles[i].x==map.salles[j].x and map.salles[j].type_salle==5:
                    map.salles[i].blocs_type[0][7]=18

        map.salles[i].visited=False

    return map

def generer_images_salles(map,i):

    tileset=pygame.image.load("images/tileset.bmp")
    map.salles[i].image=pygame.Surface((960,576))

    for j in range(9):

        for h in range(15):

            map.salles[i].blocs_type[j][h]=int(map.salles[i].blocs_type[j][h])

            map.salles[i].image.blit(tileset.subsurface((map.salles[i].blocs_type[j][h]-(int(map.salles[i].blocs_type[j][h]/10)*10))*64,(int(map.salles[i].blocs_type[j][h]/10))*64,64,64),(h*64,j*64))

    return map

def generer_hitboxs(map,i):

    for y in range(9):

        map.salles[i].blocs_hitboxs.append([])
        for x in range(15):

            map.salles[i].blocs_hitboxs[y].append(Hitbox())
            map.salles[i].blocs_hitboxs[y][x].x=x*64
            map.salles[i].blocs_hitboxs[y][x].y=y*64
            map.salles[i].blocs_hitboxs[y][x].w=64
            map.salles[i].blocs_hitboxs[y][x].h=64

    return map

def charger_image_joueur(joueur):

    personnages=pygame.image.load("images/personnages.bmp")

    joueur.images.bas=[]
    joueur.images.haut=[]
    joueur.images.droite=[]
    joueur.images.gauche=[]

    for l in range(6):
        joueur.images.bas.append(personnages.subsurface(l*64,0,64,64))
        joueur.images.haut.append(personnages.subsurface((l+6)*64,0,64,64))
        joueur.images.droite.append(personnages.subsurface((l+12)*64,0,64,64))
        joueur.images.gauche.append(personnages.subsurface((l+18)*64,0,64,64))
        joueur.images.bas[l].set_colorkey((255,255,255))
        joueur.images.haut[l].set_colorkey((255,255,255))
        joueur.images.droite[l].set_colorkey((255,255,255))
        joueur.images.gauche[l].set_colorkey((255,255,255))

    return joueur

def initialiser_joueur(map,joueur):

    if joueur.salle==-1:
        joueur.x=448
        joueur.y=256
        i=0
        while map.salles[i].type_salle!=2:
            i+=1
        joueur.salle=i
    else:
        i=0
        if joueur.x>=832:
            joueur.x=64
            joueur.y=256
            while not (map.salles[joueur.salle].x==(map.salles[i].x-1) and map.salles[joueur.salle].y==map.salles[i].y):
                i+=1
        elif joueur.x<128:
            joueur.x=832
            joueur.y=256
            while not (map.salles[joueur.salle].x==(map.salles[i].x+1) and map.salles[joueur.salle].y==map.salles[i].y):
                i+=1
        elif joueur.y>=448:
            joueur.x=448
            joueur.y=64
            while not (map.salles[joueur.salle].y==(map.salles[i].y-1) and map.salles[joueur.salle].x==map.salles[i].x):
                i+=1
        elif joueur.y<128:
            joueur.x=448
            joueur.y=448
            while not (map.salles[joueur.salle].y==(map.salles[i].y+1) and map.salles[joueur.salle].x==map.salles[i].x):
                i+=1

        joueur.salle=i

    return joueur

def initialiser_ennemis(map,joueur):

    if not map.salles[joueur.salle].visited:

        if map.salles[joueur.salle].type_salle==1: # Generation aléatoire d'ennemis pour les salles normales

            personnages=pygame.image.load("images/personnages.bmp")

            if randrange(2)==0:

                for i in range(randrange(len(map.salles[joueur.salle].ennemis_potentiels))):
                    map.salles[joueur.salle].ennemis.append(Ennemis())
                    map.salles[joueur.salle].ennemis[i].x=map.salles[joueur.salle].ennemis_potentiels[i].x
                    map.salles[joueur.salle].ennemis[i].y=map.salles[joueur.salle].ennemis_potentiels[i].y
                    map.salles[joueur.salle].ennemis[i].type=randrange((personnages.get_size()[1]//64)-1)
                    map.salles[joueur.salle].ennemis[i].attaque=10+(map.niveau*map.niveau)-((map.niveau*randrange(map.niveau))//2)
                    map.salles[joueur.salle].ennemis[i].points_de_vies=map.salles[joueur.salle].ennemis[i].attaque*10
                    map.salles[joueur.salle].ennemis[i].hitbox_degats.x=map.salles[joueur.salle].ennemis[i].x
                    map.salles[joueur.salle].ennemis[i].hitbox_degats.y=map.salles[joueur.salle].ennemis[i].y
                    map.salles[joueur.salle].ennemis[i].hitbox_degats.w=64
                    map.salles[joueur.salle].ennemis[i].hitbox_degats.h=64
                    map.salles[joueur.salle].ennemis[i].mort=False
                    map.salles[joueur.salle].ennemis[i].hitbox_deplacement.x=map.salles[joueur.salle].ennemis[i].x+16
                    map.salles[joueur.salle].ennemis[i].hitbox_deplacement.y=map.salles[joueur.salle].ennemis[i].y+16
                    map.salles[joueur.salle].ennemis[i].hitbox_deplacement.w=32
                    map.salles[joueur.salle].ennemis[i].hitbox_deplacement.h=48

                    for l in range(6):
                        map.salles[joueur.salle].ennemis[i].images.bas.append(personnages.subsurface(l*64,(map.salles[joueur.salle].ennemis[i].type+1)*64,64,64))
                        map.salles[joueur.salle].ennemis[i].images.haut.append(personnages.subsurface((l+6)*64,(map.salles[joueur.salle].ennemis[i].type+1)*64,64,64))
                        map.salles[joueur.salle].ennemis[i].images.droite.append(personnages.subsurface((l+12)*64,(map.salles[joueur.salle].ennemis[i].type+1)*64,64,64))
                        map.salles[joueur.salle].ennemis[i].images.gauche.append(personnages.subsurface((l+18)*64,(map.salles[joueur.salle].ennemis[i].type+1)*64,64,64))
                        map.salles[joueur.salle].ennemis[i].images.bas[l].set_colorkey((255,255,255))
                        map.salles[joueur.salle].ennemis[i].images.haut[l].set_colorkey((255,255,255))
                        map.salles[joueur.salle].ennemis[i].images.droite[l].set_colorkey((255,255,255))
                        map.salles[joueur.salle].ennemis[i].images.gauche[l].set_colorkey((255,255,255))

    return map

def initialiser_objets(map,joueur):

    if not map.salles[joueur.salle].visited:

        if map.salles[joueur.salle].type_salle==1:

            objets=pygame.image.load("images/objets_communs.bmp")

            compteur=0
            for i in range(len(map.salles[joueur.salle].objets_potentiels)):

                if randrange(3)==0:

                    n=randrange(len(map.salles[joueur.salle].objets_potentiels))
                    map.salles[joueur.salle].objets.append(Objet())
                    map.salles[joueur.salle].objets[compteur].x=map.salles[joueur.salle].objets_potentiels[n].x
                    map.salles[joueur.salle].objets[compteur].y=map.salles[joueur.salle].objets_potentiels[n].y
                    map.salles[joueur.salle].objets[compteur].hitbox.x=map.salles[joueur.salle].objets[compteur].x
                    map.salles[joueur.salle].objets[compteur].hitbox.y=map.salles[joueur.salle].objets[compteur].y
                    map.salles[joueur.salle].objets[compteur].hitbox.w=64
                    map.salles[joueur.salle].objets[compteur].hitbox.h=64
                    map.salles[joueur.salle].blocs_type[int(map.salles[joueur.salle].objets[compteur].y/64)][int(map.salles[joueur.salle].objets[compteur].x/64)]=0

                    type=randrange(100)
                    if type<25:
                        map.salles[joueur.salle].objets[compteur].type=0
                    elif type>=25 and type<50:
                        map.salles[joueur.salle].objets[compteur].type=2
                    elif type>=50 and type<75:
                        map.salles[joueur.salle].objets[compteur].type=4
                    elif type>=75 and type<85:
                        map.salles[joueur.salle].objets[compteur].type=1
                    elif type>=85 and type<92:
                        map.salles[joueur.salle].objets[compteur].type=3
                    elif type>=92 and type<97:
                        map.salles[joueur.salle].objets[compteur].type=5
                    elif type>=97 and type<100:
                        map.salles[joueur.salle].objets[compteur].type=6

                    map.salles[joueur.salle].objets[compteur].image=objets.subsurface(((map.salles[joueur.salle].objets[compteur].type%10)*64,(map.salles[joueur.salle].objets[compteur].type//10)*64,64,64))
                    map.salles[joueur.salle].objets[compteur].image.set_colorkey((255,255,255))

                    del map.salles[joueur.salle].objets_potentiels[n]
                    compteur+=1
                else:
                    break

        elif map.salles[joueur.salle].type_salle==3 or  map.salles[joueur.salle].type_salle==5:

            objets=pygame.image.load("images/objets_rares.bmp")

            objet=Objet()
            objet.x=448
            objet.y=256
            objet.type=1000+randrange(8)
            objet.image=objets.subsurface((((objet.type-1000)%10)*64,((objet.type-1000)//10)*64,64,64))
            objet.image.set_colorkey((255,255,255))
            objet.hitbox.x=448
            objet.hitbox.y=256
            objet.hitbox.w=64
            objet.hitbox.h=64
            map.salles[joueur.salle].objets.append(objet)
            map.salles[joueur.salle].blocs_type[int(map.salles[joueur.salle].objets[0].y/64)][int(map.salles[joueur.salle].objets[0].x/64)]=0


    return map

def rafraichir_image(liste_rafraichir,ecran):

    liste=[]
    for i in range(9):
        for j in range(len(liste_rafraichir)):
            if liste_rafraichir[j][2]==i:
                ecran.blit(liste_rafraichir[j][0],liste_rafraichir[j][1])
                liste.append(liste_rafraichir[j][1])

    pygame.display.update(liste)

    return 0

def collisions(rect_un,rect_deux):

    if rect_un.x >= rect_deux.x + rect_deux.w \
    or rect_deux.x >= rect_un.x + rect_un.w \
    or rect_un.y >= rect_deux.y + rect_deux.h \
    or rect_deux.y >= rect_un.y + rect_un.h:
        return False
    else:
        return True

def gerer_portes(map,joueur,liste_rafraichir,position_ecran_x,position_ecran_y):

    if len(map.salles[joueur.salle].ennemis)==0 and (not map.salles[joueur.salle].visited):
        map.salles[joueur.salle].visited=True

        tileset=pygame.image.load("images/tileset.bmp")

        if map.salles[joueur.salle].blocs_type[0][7]==4:
            map.salles[joueur.salle].blocs_type[0][7]=14
            map.salles[joueur.salle].image.blit(tileset.subsurface((256,64,64,64)),(448,0))
        if map.salles[joueur.salle].blocs_type[4][0]==7:
            map.salles[joueur.salle].blocs_type[4][0]=17
            map.salles[joueur.salle].image.blit(tileset.subsurface((448,64,64,64)),(0,256))
        if map.salles[joueur.salle].blocs_type[8][7]==5:
            map.salles[joueur.salle].blocs_type[8][7]=15
            map.salles[joueur.salle].image.blit(tileset.subsurface((320,64,64,64)),(448,512))
        if map.salles[joueur.salle].blocs_type[4][14]==6:
            map.salles[joueur.salle].blocs_type[4][14]=16
            map.salles[joueur.salle].image.blit(tileset.subsurface((384,64,64,64)),(896,256))

        if map.salles[joueur.salle].type_salle==4:
            map.salles[joueur.salle].blocs_type[4][7]=13
            map.salles[joueur.salle].image.blit(tileset.subsurface((192,64,64,64)),(448,256))

        if map.salles[joueur.salle].blocs_type[0][7]==14:
            liste=[map.salles[joueur.salle].image.subsurface((448,0,64,64)),(448+position_ecran_x,0+position_ecran_y,64,64),0]
            liste_rafraichir.append(liste)
        if map.salles[joueur.salle].blocs_type[4][0]==17:
            liste=[map.salles[joueur.salle].image.subsurface((0,256,64,64)),(0+position_ecran_x,256+position_ecran_y,64,64),0]
            liste_rafraichir.append(liste)
        if map.salles[joueur.salle].blocs_type[8][7]==15:
            liste=[map.salles[joueur.salle].image.subsurface((448,512,64,64)),(448+position_ecran_x,512+position_ecran_y,64,64),0]
            liste_rafraichir.append(liste)
        if map.salles[joueur.salle].blocs_type[4][14]==16:
            liste=[map.salles[joueur.salle].image.subsurface((896,256,64,64)),(896+position_ecran_x,256+position_ecran_y,64,64),0]
            liste_rafraichir.append(liste)

        if map.salles[joueur.salle].type_salle==4:
            liste=[map.salles[joueur.salle].image.subsurface((448,256,64,64)),(448+position_ecran_x,256+position_ecran_y,64,64),0]
            liste_rafraichir.append(liste)

    if len(map.salles[joueur.salle].ennemis)==0 and \
    (map.salles[joueur.salle].blocs_type[0][7]==18 or map.salles[joueur.salle].blocs_type[4][0]==21
     or map.salles[joueur.salle].blocs_type[8][7]==19 or map.salles[joueur.salle].blocs_type[4][14]==20):

        tileset=pygame.image.load("images/tileset.bmp")

        salle_ouverte=0

        if map.salles[joueur.salle].blocs_type[0][7]==18 \
        and joueur.x>432 and joueur.x<496 and joueur.y==48 and joueur.deplacement_y<0 and joueur.cles>0:
            rafraichir_cles(position_ecran_x,position_ecran_y,joueur,liste_rafraichir,joueur.cles-1)
            map.salles[joueur.salle].blocs_type[0][7]=14
            map.salles[joueur.salle].image.blit(tileset.subsurface((256,64,64,64)),(448,0))
            for i in range(len(map.salles)):
                if map.salles[joueur.salle].x==map.salles[i].x and map.salles[joueur.salle].y==map.salles[i].y+1:
                    salle_ouverte=i

        if map.salles[joueur.salle].blocs_type[4][0]==21 \
        and joueur.y>240 and joueur.y<304 and joueur.x==48 and joueur.deplacement_x<0 and joueur.cles>0:
            rafraichir_cles(position_ecran_x,position_ecran_y,joueur,liste_rafraichir,joueur.cles-1)
            map.salles[joueur.salle].blocs_type[4][0]=17
            map.salles[joueur.salle].image.blit(tileset.subsurface((448,64,64,64)),(0,256))
            for i in range(len(map.salles)):
                if map.salles[joueur.salle].x==map.salles[i].x+1 and map.salles[joueur.salle].y==map.salles[i].y:
                    salle_ouverte=i

        if map.salles[joueur.salle].blocs_type[8][7]==19 \
        and joueur.x>432 and joueur.x<496 and joueur.y==448 and joueur.deplacement_y>0 and joueur.cles>0:
            rafraichir_cles(position_ecran_x,position_ecran_y,joueur,liste_rafraichir,joueur.cles-1)
            map.salles[joueur.salle].blocs_type[8][7]=15
            map.salles[joueur.salle].image.blit(tileset.subsurface((320,64,64,64)),(448,512))
            for i in range(len(map.salles)):
                if map.salles[joueur.salle].x==map.salles[i].x and map.salles[joueur.salle].y==map.salles[i].y-1:
                    salle_ouverte=i

        if map.salles[joueur.salle].blocs_type[4][14]==20 \
        and joueur.x==848 and joueur.y<304 and joueur.y>240 and joueur.deplacement_x>0 and joueur.cles>0:
            print("Prout")
            rafraichir_cles(position_ecran_x,position_ecran_y,joueur,liste_rafraichir,joueur.cles-1)
            map.salles[joueur.salle].blocs_type[4][14]=16
            map.salles[joueur.salle].image.blit(tileset.subsurface((384,64,64,64)),(896,256))
            for i in range(len(map.salles)):
                if map.salles[joueur.salle].x==map.salles[i].x-1 and map.salles[joueur.salle].y==map.salles[i].y:
                    salle_ouverte=i

        if map.salles[salle_ouverte].blocs_type[0][7]==4:
            for i in range(len(map.salles)):
                if map.salles[i].x==map.salles[salle_ouverte].x and map.salles[i].y+1==map.salles[salle_ouverte].y:
                    map.salles[i].blocs_type[8][7]=15
                    map.salles[i].image.blit(tileset.subsurface((320,64,64,64)),(448,512))

        if map.salles[salle_ouverte].blocs_type[4][0]==7:
            for i in range(len(map.salles)):
                if map.salles[i].x+1==map.salles[salle_ouverte].x and map.salles[i].y==map.salles[salle_ouverte].y:
                    map.salles[i].blocs_type[4][14]=16
                    map.salles[i].image.blit(tileset.subsurface((384,64,64,64)),(896,256))

        if map.salles[salle_ouverte].blocs_type[8][7]==5:
            for i in range(len(map.salles)):
                if map.salles[i].x==map.salles[salle_ouverte].x and map.salles[i].y-1==map.salles[salle_ouverte].y:
                    map.salles[i].blocs_type[0][7]=14
                    map.salles[i].image.blit(tileset.subsurface((256,64,64,64)),(448,0))

        if map.salles[salle_ouverte].blocs_type[4][14]==6:
            for i in range(len(map.salles)):
                if map.salles[i].x-1==map.salles[salle_ouverte].x and map.salles[i].y==map.salles[salle_ouverte].y:
                    map.salles[i].blocs_type[4][0]=17
                    map.salles[i].image.blit(tileset.subsurface((448,64,64,64)),(0,256))


        if map.salles[joueur.salle].blocs_type[0][7]==14:
            liste=[map.salles[joueur.salle].image.subsurface((448,0,64,64)),(448+position_ecran_x,0+position_ecran_y,64,64),0]
            liste_rafraichir.append(liste)
        if map.salles[joueur.salle].blocs_type[4][0]==17:
            liste=[map.salles[joueur.salle].image.subsurface((0,256,64,64)),(0+position_ecran_x,256+position_ecran_y,64,64),0]
            liste_rafraichir.append(liste)
        if map.salles[joueur.salle].blocs_type[8][7]==15:
            liste=[map.salles[joueur.salle].image.subsurface((448,512,64,64)),(448+position_ecran_x,512+position_ecran_y,64,64),0]
            liste_rafraichir.append(liste)
        if map.salles[joueur.salle].blocs_type[4][14]==16:
            liste=[map.salles[joueur.salle].image.subsurface((896,256,64,64)),(896+position_ecran_x,256+position_ecran_y,64,64),0]
            liste_rafraichir.append(liste)

    return map,liste_rafraichir,joueur

def gerer_fps(temps_actuel):

    temps_precedent=temps_actuel
    temps_actuel=pygame.time.get_ticks()
    print(temps_actuel-temps_precedent)
    if (temps_actuel-temps_precedent)<35:
        pygame.time.wait(30-(temps_actuel-temps_precedent))
        temps_actuel=pygame.time.get_ticks()
    return temps_actuel

def afficher_objets(map,liste_rafraichir,position_ecran_x,position_ecran_y,joueur):

    for i in range(len(map.salles[joueur.salle].objets)):

        liste=[]
        liste.append(map.salles[joueur.salle].objets[i].image)
        liste.append((map.salles[joueur.salle].objets[i].x+position_ecran_x, map.salles[joueur.salle].objets[i].y+position_ecran_y,64,64))
        liste.append(1)
        liste_rafraichir.append(liste)

    return liste_rafraichir

def deplacer_personnage(map,joueur,liste_rafraichir,tempo,position_ecran_x,position_ecran_y):

    liste=[map.salles[joueur.salle].image.subsurface((joueur.x,joueur.y,64,64)),(joueur.x+position_ecran_x,joueur.y+position_ecran_y,64,64),0]
    liste_rafraichir.append(liste)

    blocs_a_proximite=[]

    if joueur.deplacement_x!=0:

        joueur.x+=joueur.deplacement_x

        blocs_a_proximite=[]
        blocs_a_proximite.append([int(joueur.x/64),int(joueur.y/64)])
        blocs_a_proximite.append([blocs_a_proximite[0][0]+1,blocs_a_proximite[0][1]])
        blocs_a_proximite.append([blocs_a_proximite[0][0],blocs_a_proximite[0][1]+1])
        blocs_a_proximite.append([blocs_a_proximite[0][0]+1,blocs_a_proximite[0][1]+1])

        joueur.hitbox.x=joueur.x+16
        joueur.hitbox.y=joueur.y+16

        for i in range(4):

            while collisions(joueur.hitbox, map.salles[joueur.salle].blocs_hitboxs[blocs_a_proximite[i][1]][blocs_a_proximite[i][0]])\
            and ((map.salles[joueur.salle].blocs_type[blocs_a_proximite[i][1]][blocs_a_proximite[i][0]]>=1
            and map.salles[joueur.salle].blocs_type[blocs_a_proximite[i][1]][blocs_a_proximite[i][0]]<=11)
            or (map.salles[joueur.salle].blocs_type[blocs_a_proximite[i][1]][blocs_a_proximite[i][0]]>=18
            and map.salles[joueur.salle].blocs_type[blocs_a_proximite[i][1]][blocs_a_proximite[i][0]]<=21)):

                if joueur.deplacement_x>0:
                    joueur.x-=1
                else:
                    joueur.x+=1

                joueur.hitbox.x=joueur.x+16

                if int(joueur.x/64)!=blocs_a_proximite[0][0]:
                    blocs_a_proximite=[]
                    blocs_a_proximite.append([int(joueur.x/64),int(joueur.y/64)])
                    blocs_a_proximite.append([blocs_a_proximite[0][0]+1,blocs_a_proximite[0][1]])
                    blocs_a_proximite.append([blocs_a_proximite[0][0],blocs_a_proximite[0][1]+1])
                    blocs_a_proximite.append([blocs_a_proximite[0][0]+1,blocs_a_proximite[0][1]+1])

    if joueur.deplacement_y!=0:

        joueur.y+=joueur.deplacement_y

        blocs_a_proximite=[]
        blocs_a_proximite.append([int(joueur.x/64),int(joueur.y/64)])
        blocs_a_proximite.append([blocs_a_proximite[0][0]+1,blocs_a_proximite[0][1]])
        blocs_a_proximite.append([blocs_a_proximite[0][0],blocs_a_proximite[0][1]+1])
        blocs_a_proximite.append([blocs_a_proximite[0][0]+1,blocs_a_proximite[0][1]+1])

        joueur.hitbox.x=joueur.x+16
        joueur.hitbox.y=joueur.y+16

        for i in range(4):

            while collisions(joueur.hitbox, map.salles[joueur.salle].blocs_hitboxs[blocs_a_proximite[i][1]][blocs_a_proximite[i][0]])\
            and ((map.salles[joueur.salle].blocs_type[blocs_a_proximite[i][1]][blocs_a_proximite[i][0]]>=1
            and map.salles[joueur.salle].blocs_type[blocs_a_proximite[i][1]][blocs_a_proximite[i][0]]<=11)
            or (map.salles[joueur.salle].blocs_type[blocs_a_proximite[i][1]][blocs_a_proximite[i][0]]>=18
            and map.salles[joueur.salle].blocs_type[blocs_a_proximite[i][1]][blocs_a_proximite[i][0]]<=21)):

                if joueur.deplacement_y>0:
                    joueur.y-=1
                else:
                    joueur.y+=1

                joueur.hitbox.y=joueur.y+16

                if int(joueur.y/64)!=blocs_a_proximite[0][1]:
                    blocs_a_proximite=[]
                    blocs_a_proximite.append([int(joueur.x/64),int(joueur.y/64)])
                    blocs_a_proximite.append([blocs_a_proximite[0][0]+1,blocs_a_proximite[0][1]])
                    blocs_a_proximite.append([blocs_a_proximite[0][0],blocs_a_proximite[0][1]+1])
                    blocs_a_proximite.append([blocs_a_proximite[0][0]+1,blocs_a_proximite[0][1]+1])

    if joueur.deplacement_x>0 and joueur.attaques.autorisation==[]:
        liste=[joueur.images.droite[int(tempo/8)],(joueur.x+position_ecran_x,joueur.y+position_ecran_y,64,64),4]
    if joueur.deplacement_x<0 and joueur.attaques.autorisation==[]:
        liste=[joueur.images.gauche[int(tempo/8)],(joueur.x+position_ecran_x,joueur.y+position_ecran_y,64,64),4]
    if joueur.deplacement_y>0 and joueur.attaques.autorisation==[]:
        liste=[joueur.images.bas[int(tempo/8)],(joueur.x+position_ecran_x,joueur.y+position_ecran_y,64,64),4]
    if joueur.deplacement_y<0 and joueur.attaques.autorisation==[]:
        liste=[joueur.images.haut[int(tempo/8)],(joueur.x+position_ecran_x,joueur.y+position_ecran_y,64,64),4]
    if joueur.deplacement_x==0 and joueur.deplacement_y==0 and joueur.attaques.autorisation==[]:
        liste=[joueur.images.bas[0],(joueur.x+position_ecran_x,joueur.y+position_ecran_y,64,64),4]

    if joueur.deplacement_x>0 and joueur.attaques.autorisation!=[]:
        liste=[joueur.images.droite[3+int(tempo/8)],(joueur.x+position_ecran_x,joueur.y+position_ecran_y,64,64),4]
    if joueur.deplacement_x<0 and joueur.attaques.autorisation!=[]:
        liste=[joueur.images.gauche[3+int(tempo/8)],(joueur.x+position_ecran_x,joueur.y+position_ecran_y,64,64),4]
    if joueur.deplacement_y>0 and joueur.attaques.autorisation!=[]:
        liste=[joueur.images.bas[3+int(tempo/8)],(joueur.x+position_ecran_x,joueur.y+position_ecran_y,64,64),4]
    if joueur.deplacement_y<0 and joueur.attaques.autorisation!=[]:
        liste=[joueur.images.haut[3+int(tempo/8)],(joueur.x+position_ecran_x,joueur.y+position_ecran_y,64,64),4]
    if joueur.deplacement_x==0 and joueur.deplacement_y==0 and joueur.attaques.autorisation!=[]:
        liste=[joueur.images.bas[3],(joueur.x+position_ecran_x,joueur.y+position_ecran_y,64,64),4]

    liste_rafraichir.append(liste)

    return liste_rafraichir,blocs_a_proximite

def gerer_tempo(tempo):

    if tempo==23:
        tempo=0
    else:
        tempo+=1

    return tempo

def ramasser_objets(map,joueur,liste_rafraichir,position_ecran_x,position_ecran_y):

    i=0

    while i < len(map.salles[joueur.salle].objets): # Gérer les collisions avec les objets

        if collisions(joueur.hitbox, map.salles[joueur.salle].objets[i].hitbox):

            if map.salles[joueur.salle].objets[i].type==0:
                liste_rafraichir,joueur=rafraichir_bombes(position_ecran_x,position_ecran_y,joueur,liste_rafraichir,joueur.bombes+1)
            if map.salles[joueur.salle].objets[i].type==1:
                liste_rafraichir,joueur=rafraichir_bombes(position_ecran_x,position_ecran_y,joueur,liste_rafraichir,joueur.bombes+3)
            if map.salles[joueur.salle].objets[i].type==2:
                liste_rafraichir,joueur=rafraichir_cles(position_ecran_x,position_ecran_y,joueur,liste_rafraichir,joueur.cles+1)
            if map.salles[joueur.salle].objets[i].type==3:
                liste_rafraichir,joueur=rafraichir_cles(position_ecran_x,position_ecran_y,joueur,liste_rafraichir,joueur.cles+3)
            if map.salles[joueur.salle].objets[i].type==4:
                liste_rafraichir,joueur=rafraichir_argent(position_ecran_x,position_ecran_y,joueur,liste_rafraichir,joueur.argent+1)
            if map.salles[joueur.salle].objets[i].type==5:
                liste_rafraichir,joueur=rafraichir_argent(position_ecran_x,position_ecran_y,joueur,liste_rafraichir,joueur.argent+5)
            if map.salles[joueur.salle].objets[i].type==6:
                liste_rafraichir,joueur=rafraichir_argent(position_ecran_x,position_ecran_y,joueur,liste_rafraichir,joueur.argent+10)
            if map.salles[joueur.salle].objets[i].type==7:
                liste_rafraichir,joueur=rafraichir_vie(position_ecran_x,position_ecran_y,joueur,liste_rafraichir,joueur.points_de_vies+10,joueur.vie_maximum)
            if map.salles[joueur.salle].objets[i].type==1000:
                liste_rafraichir,joueur=rafraichir_bombes(position_ecran_x,position_ecran_y,joueur,liste_rafraichir,99)
            if map.salles[joueur.salle].objets[i].type==1001:
                liste_rafraichir,joueur=rafraichir_cles(position_ecran_x,position_ecran_y,joueur,liste_rafraichir,99)
            if map.salles[joueur.salle].objets[i].type==1002:
                liste_rafraichir,joueur=rafraichir_argent(position_ecran_x,position_ecran_y,joueur,liste_rafraichir,joueur.argent+50)
            if map.salles[joueur.salle].objets[i].type==1003:
                joueur.vitesse+=1
                if joueur.deplacement_x>0:
                    joueur.deplacement_x=joueur.vitesse
                if joueur.deplacement_x<0:
                    joueur.deplacement_x=-joueur.vitesse
                if joueur.deplacement_y>0:
                    joueur.deplacement_y=joueur.vitesse
                if joueur.deplacement_y<0:
                    joueur.deplacement_y=-joueur.vitesse
            if map.salles[joueur.salle].objets[i].type==1004 \
            or map.salles[joueur.salle].objets[i].type==1005:
                joueur.attaque+=2
            if map.salles[joueur.salle].objets[i].type==1006 \
            or map.salles[joueur.salle].objets[i].type==1007:
                liste_rafraichir,joueur=rafraichir_vie(position_ecran_x,position_ecran_y,joueur,liste_rafraichir,joueur.points_de_vies+5,joueur.vie_maximum+5)

            if joueur.vitesse>10:
                joueur.vitesse=10
            if joueur.vitesse_attaque<75:
                joueur.vitesse_attaque=75


            liste=[map.salles[joueur.salle].image.subsurface((map.salles[joueur.salle].objets[i].x, map.salles[joueur.salle].objets[i].y,64,64)),
                    (map.salles[joueur.salle].objets[i].x+position_ecran_x, map.salles[joueur.salle].objets[i].y+position_ecran_y,64,64),1]
            liste_rafraichir.append(liste)

            del map.salles[joueur.salle].objets[i]
            i=-1
        i+=1

    return map,joueur,liste_rafraichir

def afficher_interface(position_ecran_x,position_ecran_y,ecran,joueur,session):

    interface=pygame.image.load("images/interface.bmp")
    caracteres=pygame.image.load("images/ascii.bmp")
    objets=pygame.image.load("images/objets_communs.bmp")
    interface.set_colorkey((255,255,255))
    caracteres.set_colorkey((255,255,255))
    objets.set_colorkey((255,255,255))

    for i in range(15):
        ecran.blit(interface.subsurface((0,64,64,64)),(position_ecran_x+(64*i),position_ecran_y-64))
        ecran.blit(interface.subsurface((0,64,64,64)),(position_ecran_x+(64*i),position_ecran_y+576))
        if i<9:
            ecran.blit(interface.subsurface((0,64,64,64)),(position_ecran_x+960,position_ecran_y+(i*64)))

    for i in range(3):
        ecran.blit(interface.subsurface((84,64,2,64)),(position_ecran_x+(144*(i+1)),position_ecran_y-64))
        ecran.blit(interface.subsurface((64,64,20,64)),(position_ecran_x+(144*i)+64,position_ecran_y-64))

    ecran.blit(objets.subsurface((0,0,64,64)),(position_ecran_x,position_ecran_y-64))
    ecran.blit(objets.subsurface((128,0,64,64)),(position_ecran_x+144,position_ecran_y-64))
    ecran.blit(objets.subsurface((384,0,64,64)),(position_ecran_x+288,position_ecran_y-64))

    ecran.blit(interface.subsurface(((joueur.bombes//10)*30,0,30,64)),(position_ecran_x+84,position_ecran_y-64))
    ecran.blit(interface.subsurface(((joueur.bombes%10)*30,0,30,64)),(position_ecran_x+114,position_ecran_y-64))

    ecran.blit(interface.subsurface((int(joueur.cles/10)*30,0,30,64)),(position_ecran_x+228,position_ecran_y-64))
    ecran.blit(interface.subsurface(((joueur.cles-(int(joueur.cles/10)*10))*30,0,30,64)),(position_ecran_x+258,position_ecran_y-64))

    ecran.blit(interface.subsurface(((joueur.argent//10)*30,0,30,64)),(position_ecran_x+372,position_ecran_y-64))
    ecran.blit(interface.subsurface(((joueur.argent-(int(joueur.argent/10)*10))*30,0,30,64)),(position_ecran_x+402,position_ecran_y-64))

    for i in range(int((joueur.points_de_vies/joueur.vie_maximum)*450)):
        ecran.blit(interface.subsurface((86,64,1,32)),(position_ecran_x+510+i,position_ecran_y-64))
    for i in range(450-int((joueur.points_de_vies/joueur.vie_maximum)*450)):
        ecran.blit(interface.subsurface((86,96,1,32)),(position_ecran_x+959-i,position_ecran_y-64))
    ecran.blit(interface.subsurface((84,64,2,32)),(position_ecran_x+510,position_ecran_y-64))

    mana_max=100+(20*session.competences[7])

    for i in range(450):
        if i<=int(joueur.mana*(450/mana_max)):
            ecran.blit(interface.subsurface((87,64,1,32)),(position_ecran_x+510+i,position_ecran_y-32))
        else:
            ecran.blit(interface.subsurface((86,96,1,32)),(position_ecran_x+510+i,position_ecran_y-32))
    ecran.blit(interface.subsurface((84,64,2,32)),(position_ecran_x+510,position_ecran_y-32))

    ecran.blit(interface.subsurface((0,128,64,64)),(position_ecran_x+446,position_ecran_y-64))

    mot="VIES:"
    for i in range(len(mot)):
        ecran.blit(pygame.transform.scale(caracteres.subsurface(((ord(mot[i])%10)*32,(ord(mot[i])//10)*64,32,64)),(30,60)),(position_ecran_x+(30*i)+2,position_ecran_y+578))

    ecran.blit(interface.subsurface((int(joueur.nombre_de_vies/10)*30,0,30,64)),(position_ecran_x+150,position_ecran_y+576))
    ecran.blit(interface.subsurface(((joueur.nombre_de_vies-(int(joueur.nombre_de_vies/10)*10))*30,0,30,64)),(position_ecran_x+180,position_ecran_y+576))

    mot="NIVEAU:"
    for i in range(len(mot)):
        ecran.blit(pygame.transform.scale(caracteres.subsurface(((ord(mot[i])%10)*32,(ord(mot[i])//10)*64,32,64)),(30,60)),(position_ecran_x+(30*i)+688,position_ecran_y+578))

    ecran.blit(interface.subsurface((int(session.niveau/10)*30,0,30,64)),(position_ecran_x+898,position_ecran_y+576))
    ecran.blit(interface.subsurface(((session.niveau-(int(session.niveau/10)*10))*30,0,30,64)),(position_ecran_x+928,position_ecran_y+576))

    ecran.blit(interface.subsurface((64,192,64,32)),(position_ecran_x+960,position_ecran_y+288))
    ecran.blit(interface.subsurface((0,194,64,2)),(position_ecran_x+960,position_ecran_y+574))
    ecran.blit(interface.subsurface((0,194,64,2)),(position_ecran_x+960,position_ecran_y+320))
    for i in range(252):
        if i<(session.xp*252)//int(100*(1.8**session.niveau)):
            ecran.blit(interface.subsurface((0,192,64,1)),(position_ecran_x+960,position_ecran_y+573-i))
        else:
            ecran.blit(interface.subsurface((0,193,64,1)),(position_ecran_x+960,position_ecran_y+573-i))


    pygame.display.flip()

    return 0

def rafraichir_bombes(position_ecran_x,position_ecran_y,joueur,liste_rafraichir,nouvelle_valeur):

    if nouvelle_valeur>99:
        nouvelle_valeur=99

    if nouvelle_valeur!=joueur.bombes:

        interface_images=pygame.image.load("images/interface.bmp")
        interface_images.set_colorkey((255,255,255))


        liste=[interface_images.subsurface(((nouvelle_valeur-(int(nouvelle_valeur/10)*10))*30,0,30,64)),
                (position_ecran_x+114,position_ecran_y-64,30,64),6]
        liste_rafraichir.append(liste)

        liste=[interface_images.subsurface((114,128,30,64)),
                (position_ecran_x+114,position_ecran_y-64,30,64),5]
        liste_rafraichir.append(liste)


        if int(nouvelle_valeur/10)!=int(joueur.bombes/10):

            liste=[interface_images.subsurface((int(nouvelle_valeur/10)*30,0,30,64)),
                (position_ecran_x+84,position_ecran_y-64,30,64),6]
            liste_rafraichir.append(liste)

            liste=[interface_images.subsurface((84,128,30,64)),
                (position_ecran_x+84,position_ecran_y-64,30,64),5]
            liste_rafraichir.append(liste)

        joueur.bombes=nouvelle_valeur

    return liste_rafraichir,joueur

def rafraichir_cles(position_ecran_x,position_ecran_y,joueur,liste_rafraichir,nouvelle_valeur):

    if nouvelle_valeur>99:
        nouvelle_valeur=99

    if nouvelle_valeur!=joueur.cles:

        interface_images=pygame.image.load("images/interface.bmp")
        interface_images.set_colorkey((255,255,255))

        liste=[interface_images.subsurface(((nouvelle_valeur-(int(nouvelle_valeur/10)*10))*30,0,30,64)),
               (position_ecran_x+258,position_ecran_y-64,30,64),6]
        liste_rafraichir.append(liste)

        liste=[interface_images.subsurface((66,128,30,64)),
               (position_ecran_x+258,position_ecran_y-64,30,64),5]
        liste_rafraichir.append(liste)


        if int(nouvelle_valeur/10)!=int(joueur.cles/10):

            liste=[interface_images.subsurface((int(nouvelle_valeur/10)*30,0,30,64)),
               (position_ecran_x+228,position_ecran_y-64,30,64),6]
            liste_rafraichir.append(liste)

            liste=[interface_images.subsurface((100,128,30,64)),
               (position_ecran_x+228,position_ecran_y-64,30,64),5]
            liste_rafraichir.append(liste)

        joueur.cles=nouvelle_valeur

    return liste_rafraichir,joueur

def rafraichir_argent(position_ecran_x,position_ecran_y,joueur,liste_rafraichir,nouvelle_valeur):

    if nouvelle_valeur>=99:
        nouvelle_valeur-=99
        liste_rafraichir,joueur=rafraichir_nombre_de_vies(position_ecran_x,position_ecran_y,joueur,liste_rafraichir,joueur.nombre_de_vies+1)

    if nouvelle_valeur!=joueur.argent:

        interface_images=pygame.image.load("images/interface.bmp")
        interface_images.set_colorkey((255,255,255))

        liste=[interface_images.subsurface(((nouvelle_valeur-(int(nouvelle_valeur/10)*10))*30,0,30,64)),
               (position_ecran_x+402,position_ecran_y-64,30,64),6]
        liste_rafraichir.append(liste)

        liste=[interface_images.subsurface((82,128,30,64)),
               (position_ecran_x+402,position_ecran_y-64,30,64),5]
        liste_rafraichir.append(liste)


        if int(nouvelle_valeur/10)!=int(joueur.argent/10):

            liste=[interface_images.subsurface((int(nouvelle_valeur/10)*30,0,30,64)),
               (position_ecran_x+372,position_ecran_y-64,30,64),6]
            liste_rafraichir.append(liste)

            liste=[interface_images.subsurface((116,128,30,64)),
               (position_ecran_x+372,position_ecran_y-64,30,64),5]
            liste_rafraichir.append(liste)

        joueur.argent=nouvelle_valeur

    return liste_rafraichir,joueur

def rafraichir_vie(position_ecran_x,position_ecran_y,joueur,liste_rafraichir,nouvelle_vie,nouvelle_vie_maximum):

    if (not joueur.invincible) or nouvelle_vie>joueur.points_de_vies:

        if nouvelle_vie<0:
            nouvelle_vie=0
        if nouvelle_vie>nouvelle_vie_maximum:
            nouvelle_vie=nouvelle_vie_maximum
        if nouvelle_vie<joueur.points_de_vies:
            joueur.invincible=True
            joueur.temps_depuis_invincible=pygame.time.get_ticks()

        a=(int((joueur.points_de_vies/joueur.vie_maximum)*450))-(int((nouvelle_vie/nouvelle_vie_maximum)*450))

        if a>0:

            bout_de_barre=pygame.Surface((a,28))
            bout_de_barre.fill((42,42,42))
            liste=[bout_de_barre,(position_ecran_x+510+(int((nouvelle_vie/nouvelle_vie_maximum)*450)),position_ecran_y-62,a,28),6]
            liste_rafraichir.append(liste)

        if a<0:

            bout_de_barre=pygame.Surface((-a,28))
            bout_de_barre.fill((237,28,36))
            liste=[bout_de_barre,(position_ecran_x+510+(int((joueur.points_de_vies/joueur.vie_maximum)*450)),position_ecran_y-62,-a,28),6]
            liste_rafraichir.append(liste)

        joueur.points_de_vies=nouvelle_vie
        joueur.vie_maximum=nouvelle_vie_maximum

    return liste_rafraichir,joueur

def rafraichir_nombre_de_vies(position_ecran_x,position_ecran_y,joueur,liste_rafraichir,nouvelle_valeur):

    if nouvelle_valeur>99:
        nouvelle_valeur=99

    if nouvelle_valeur!=joueur.nombre_de_vies:

        interface_images=pygame.image.load("images/interface.bmp")
        interface_images.set_colorkey((255,255,255))


        liste=[interface_images.subsurface(((nouvelle_valeur-(int(nouvelle_valeur/10)*10))*30,0,30,64)),
                (position_ecran_x+180,position_ecran_y+576,30,64),6]
        liste_rafraichir.append(liste)

        liste=[interface_images.subsurface((116,128,30,64)),
                (position_ecran_x+180,position_ecran_y+576,30,64),5]
        liste_rafraichir.append(liste)


        if int(nouvelle_valeur/10)!=int(joueur.nombre_de_vies/10):

            liste=[interface_images.subsurface((int(nouvelle_valeur/10)*30,0,30,64)),
                (position_ecran_x+150,position_ecran_y+576,30,64),6]
            liste_rafraichir.append(liste)

            liste=[interface_images.subsurface((86,128,30,64)),
                (position_ecran_x+150,position_ecran_y+576,30,64),5]
            liste_rafraichir.append(liste)

        joueur.nombre_de_vies=nouvelle_valeur

    return liste_rafraichir,joueur

def rafraichir_mana(position_ecran_x,position_ecran_y,joueur,liste_rafraichir,session,nouveau_mana):

    mana_max=100+(20*session.competences[7])

    if nouveau_mana<0:
        nouveau_mana=0
    if nouveau_mana>mana_max:
        nouveau_mana=mana_max

    a=(joueur.mana*(450//mana_max))-(nouveau_mana*(450//mana_max))

    if a>0:

        bout_de_barre=pygame.Surface((a,28))
        bout_de_barre.fill((42,42,42))
        liste=[bout_de_barre,(position_ecran_x+510+nouveau_mana*(450//mana_max),position_ecran_y-30,a,28),6]
        liste_rafraichir.append(liste)

    if a<0:

        bout_de_barre=pygame.Surface((-a,28))
        bout_de_barre.fill((63,72,204))
        liste=[bout_de_barre,(position_ecran_x+510+(int(joueur.mana*(450//mana_max))),position_ecran_y-30,-a,28),6]
        liste_rafraichir.append(liste)

    joueur.mana=nouveau_mana

    return liste_rafraichir,joueur

def rafraichir_niveau_session(position_ecran_x,position_ecran_y,session,liste_rafraichir):

    i=0

    while session.xp>=int(100*(1.8**session.niveau)):
        liste_rafraichir,session=rafraichir_xp(position_ecran_x,position_ecran_y,session,liste_rafraichir,session.xp-int(100*(1.8**session.niveau)))
        session.niveau+=1
        session.points_de_competences+=1
        session.points_de_sorts+=1
        i=1

    if session.niveau>15:
        session.niveau=15
        liste_rafraichir,session=rafraichir_xp(position_ecran_x,position_ecran_y,session,liste_rafraichir,674664)

    if i==1:

        interface=pygame.image.load("images/interface.bmp")
        interface.set_colorkey((255,255,255))

        liste_rafraichir.append([interface.subsurface(((session.niveau//10)*30,0,30,64)),
            (position_ecran_x+898,position_ecran_y+576,30,64),6])

        liste_rafraichir.append([interface.subsurface((66,128,30,64)),
            (position_ecran_x+898,position_ecran_y+576,30,64),5])

        liste_rafraichir.append([interface.subsurface(((session.niveau%10)*30,0,30,64)),
            (position_ecran_x+928,position_ecran_y+576,30,64),6])

        liste_rafraichir.append([interface.subsurface((96,128,30,64)),
            (position_ecran_x+928,position_ecran_y+576,30,64),5])

    return liste_rafraichir,session

def rafraichir_xp(position_ecran_x,position_ecran_y,session,liste_rafraichir,nouvelle_valeur):

    a=((session.xp*252)//int(100*(1.8**session.niveau)))-((nouvelle_valeur*252)//int(100*(1.8**session.niveau)))

    if a>0:

        bout_de_barre=pygame.Surface((60,a))
        bout_de_barre.fill((42,42,42))
        liste_rafraichir.append([bout_de_barre,(position_ecran_x+962,position_ecran_y+574-(((session.xp*252)//int(100*(1.8**session.niveau)))),60,a),6])

    if a<0:

        bout_de_barre=pygame.Surface((60,-a))
        bout_de_barre.fill((34,177,76))
        liste_rafraichir.append([bout_de_barre,(position_ecran_x+962,position_ecran_y+574-((session.xp*252)//int(100*(1.8**session.niveau)))+a,60,-a),6])

    session.xp=nouvelle_valeur

    return liste_rafraichir,session

def creer_attaque(joueur,position_ecran_x,position_ecran_y,session):

    for i in range(len(joueur.attaques.autorisation)):
        if joueur.attaques.autorisation[i]==1:

            if pygame.time.get_ticks()>=joueur.attaques.temps_derniere_attaque+joueur.vitesse_attaque:

                try:
                    joueur.attaques.temps_derniere_attaque=pygame.time.get_ticks()

                    attaques=pygame.image.load("images/attaques_joueur.bmp")
                    attaques.set_colorkey((255,255,255))

                    entite=Entite_Attaque()
                    entite.x=joueur.x+27
                    entite.y=joueur.y+27
                    entite.type=1
                    entite.images=[attaques.subsurface((0,0,20,20)),attaques.subsurface((20,0,40,40))]
                    entite.detruit=False
                    entite.temps=0

                    difference_x=joueur.attaques.position_souris[0]-(joueur.x+position_ecran_x+27)
                    difference_y=joueur.attaques.position_souris[1]-(joueur.y+position_ecran_y+27)

                    if difference_x<0:
                        difference_x_absolue=-difference_x
                    else:
                        difference_x_absolue=difference_x

                    if difference_y<0:
                        difference_y_absolue=-difference_y
                    else:
                        difference_y_absolue=difference_y

                    if difference_y_absolue>difference_x_absolue:
                        if difference_y<0:
                            entite.deplacement_y=-15
                            if session.competences[4]==1:
                                entite.deplacement_y=-18
                            elif session.competences[4]==2:
                                entite.deplacement_y=-20
                            elif session.competences[4]==3:
                                entite.deplacement_y=-23
                        else:
                            entite.deplacement_y=15
                            if session.competences[4]==1:
                                entite.deplacement_y=18
                            elif session.competences[4]==2:
                                entite.deplacement_y=20
                            elif session.competences[4]==3:
                                entite.deplacement_y=23
                        entite.deplacement_x=(entite.deplacement_y*difference_x)/difference_y

                    else:
                        if difference_x<0:
                            entite.deplacement_x=-15
                            if session.competences[4]==1:
                                entite.deplacement_x=-18
                            elif session.competences[4]==2:
                                entite.deplacement_x=-20
                            elif session.competences[4]==3:
                                entite.deplacement_x=-23
                        else:
                            entite.deplacement_x=15
                            if session.competences[4]==1:
                                entite.deplacement_x=18
                            elif session.competences[4]==2:
                                entite.deplacement_x=20
                            elif session.competences[4]==3:
                                entite.deplacement_x=23
                        entite.deplacement_y=(entite.deplacement_x*difference_y)/difference_x

                    joueur.attaques.entites.append(entite)

                except:
                    continue

        if joueur.attaques.autorisation[i]==2:

            attaques=pygame.image.load("images/attaques_joueur.bmp")
            attaques.set_colorkey((255,255,255))

            entite=Entite_Attaque()
            entite.x=joueur.x
            entite.y=joueur.y
            entite.type=2
            entite.images=[attaques.subsurface((0,40,64,64)),
                           attaques.subsurface((64,40,64,64)),
                           attaques.subsurface((128,40,192,192))]
            entite.detruit=False
            entite.temps=0
            entite.w=192
            entite.h=192

            joueur.attaques.entites.append(entite)

            joueur.attaques.autorisation.remove(2)

    return joueur

def gerer_attaques(joueur,position_ecran_x,position_ecran_y,map,liste_rafraichir,session):

    i=0

    while i<len(joueur.attaques.entites):

        if joueur.attaques.entites[i].type==1:

            if not joueur.attaques.entites[i].detruit:

                liste_rafraichir.append([map.salles[joueur.salle].image.subsurface((joueur.attaques.entites[i].x,joueur.attaques.entites[i].y,20,20)),
                                         (joueur.attaques.entites[i].x+position_ecran_x,joueur.attaques.entites[i].y+position_ecran_y,20,20),2])

                collision=0



                joueur.attaques.entites[i].x+=joueur.attaques.entites[i].deplacement_x
                bloc_a_proximite=[int(joueur.attaques.entites[i].y/64),int(joueur.attaques.entites[i].x/64)]

                while (map.salles[joueur.salle].blocs_type[bloc_a_proximite[0]][bloc_a_proximite[1]]>=1 \
                and map.salles[joueur.salle].blocs_type[bloc_a_proximite[0]][bloc_a_proximite[1]]<=11) \
                or (map.salles[joueur.salle].blocs_type[bloc_a_proximite[0]][bloc_a_proximite[1]]>=14 \
                and map.salles[joueur.salle].blocs_type[bloc_a_proximite[0]][bloc_a_proximite[1]]<=21):
                    if joueur.attaques.entites[i].deplacement_x<0:
                        joueur.attaques.entites[i].x+=1
                    else:
                        joueur.attaques.entites[i].x-=1
                    collision=1
                    bloc_a_proximite=[int(joueur.attaques.entites[i].y/64),int(joueur.attaques.entites[i].x/64)]



                joueur.attaques.entites[i].y+=joueur.attaques.entites[i].deplacement_y
                bloc_a_proximite=[int(joueur.attaques.entites[i].y/64),int(joueur.attaques.entites[i].x/64)]

                while (map.salles[joueur.salle].blocs_type[bloc_a_proximite[0]][bloc_a_proximite[1]]>=1 \
                and map.salles[joueur.salle].blocs_type[bloc_a_proximite[0]][bloc_a_proximite[1]]<=11) \
                or (map.salles[joueur.salle].blocs_type[bloc_a_proximite[0]][bloc_a_proximite[1]]>=14 \
                and map.salles[joueur.salle].blocs_type[bloc_a_proximite[0]][bloc_a_proximite[1]]<=21):
                    if joueur.attaques.entites[i].deplacement_y<0:
                        joueur.attaques.entites[i].y+=1
                    else:
                        joueur.attaques.entites[i].y-=1
                    collision=1
                    bloc_a_proximite=[int(joueur.attaques.entites[i].y/64),int(joueur.attaques.entites[i].x/64)]



                for j in range(len(map.salles[joueur.salle].ennemis)):

                    if collisions(joueur.attaques.entites[i],map.salles[joueur.salle].ennemis[j].hitbox_degats):

                        collision=1
                        map.salles[joueur.salle].ennemis[j].points_de_vies-=joueur.attaque
                        if session.competences[10]>0:
                            liste_rafraichir,joueur=rafraichir_vie(position_ecran_x,position_ecran_y,joueur,liste_rafraichir,joueur.points_de_vies+(2*session.competences[10]),joueur.vie_maximum)
                        map.salles[joueur.salle].ennemis[j],liste_rafraichir=\
                        gerer_knockback_contre_monstres(joueur,map.salles[joueur.salle].ennemis[j],6,joueur,map,liste_rafraichir,position_ecran_x,position_ecran_y)

                        if map.salles[joueur.salle].ennemis[j].points_de_vies<=0:
                            map.salles[joueur.salle].ennemis[j].mort=True

                        joueur.attaques.entites[i].x=map.salles[joueur.salle].ennemis[j].x+22
                        joueur.attaques.entites[i].y=map.salles[joueur.salle].ennemis[j].y+22
                        break

                if collision==0:
                    liste_rafraichir.append([joueur.attaques.entites[i].images[0],(int(joueur.attaques.entites[i].x)+position_ecran_x,int(joueur.attaques.entites[i].y)+position_ecran_y,20,20),2])

                if collision==1:
                    joueur.attaques.entites[i].detruit=True
                    joueur.attaques.entites[i].temps=0

                i+=1

            else:

                joueur.attaques.entites[i].temps+=1

                if joueur.attaques.entites[i].temps>24:

                    if joueur.attaques.entites[i].deplacement_x>=0:
                        if joueur.attaques.entites[i].deplacement_y>=0:
                            liste_rafraichir.append([map.salles[joueur.salle].image.subsurface((joueur.attaques.entites[i].x,joueur.attaques.entites[i].y,40,40)),
                                                     (int(joueur.attaques.entites[i].x)+position_ecran_x,int(joueur.attaques.entites[i].y)+position_ecran_y,40,40),2])
                        else:
                            liste_rafraichir.append([map.salles[joueur.salle].image.subsurface((joueur.attaques.entites[i].x,joueur.attaques.entites[i].y-40,40,40)),
                                                     (int(joueur.attaques.entites[i].x)+position_ecran_x,int(joueur.attaques.entites[i].y)+position_ecran_y-40,40,40),2])
                    else:
                        if joueur.attaques.entites[i].deplacement_y>=0:
                            liste_rafraichir.append([map.salles[joueur.salle].image.subsurface((joueur.attaques.entites[i].x-40,joueur.attaques.entites[i].y,40,40)),
                                                     (int(joueur.attaques.entites[i].x)+position_ecran_x-40,int(joueur.attaques.entites[i].y)+position_ecran_y,40,40),2])
                        else:
                            liste_rafraichir.append([map.salles[joueur.salle].image.subsurface((joueur.attaques.entites[i].x-40,joueur.attaques.entites[i].y-40,40,40)),
                                                     (int(joueur.attaques.entites[i].x)+position_ecran_x-40,int(joueur.attaques.entites[i].y)+position_ecran_y-40,40,40),2])

                    del joueur.attaques.entites[i]

                elif joueur.attaques.entites[i].temps<24:
                    if joueur.attaques.entites[i].deplacement_x>=0:
                        if joueur.attaques.entites[i].deplacement_y>=0:
                            liste_rafraichir.append([joueur.attaques.entites[i].images[1],(int(joueur.attaques.entites[i].x)+position_ecran_x,int(joueur.attaques.entites[i].y)+position_ecran_y,40,40),2])
                        else:
                            liste_rafraichir.append([joueur.attaques.entites[i].images[1],(int(joueur.attaques.entites[i].x)+position_ecran_x,int(joueur.attaques.entites[i].y)+position_ecran_y-40,40,40),2])
                    else:
                        if joueur.attaques.entites[i].deplacement_y>=0:
                            liste_rafraichir.append([joueur.attaques.entites[i].images[1],(int(joueur.attaques.entites[i].x)+position_ecran_x-40,int(joueur.attaques.entites[i].y)+position_ecran_y,40,40),2])
                        else:
                            liste_rafraichir.append([joueur.attaques.entites[i].images[1],(int(joueur.attaques.entites[i].x)+position_ecran_x-40,int(joueur.attaques.entites[i].y)+position_ecran_y-40,40,40),2])
                    i+=1

        elif joueur.attaques.entites[i].type==2:

            if not joueur.attaques.entites[i].detruit:

                joueur.attaques.entites[i].temps+=1
                liste_rafraichir.append([map.salles[joueur.salle].image.subsurface((joueur.attaques.entites[i].x,joueur.attaques.entites[i].y,64,64)),
                                        (position_ecran_x+joueur.attaques.entites[i].x,position_ecran_y+joueur.attaques.entites[i].y,64,64),2])

                if joueur.attaques.entites[i].temps==144:
                    joueur.attaques.entites[i].detruit=True
                    joueur.attaques.entites[i].temps=0

                if joueur.attaques.entites[i].temps%16<8:
                    liste_rafraichir.append([joueur.attaques.entites[i].images[0],
                                             (position_ecran_x+joueur.attaques.entites[i].x,position_ecran_y+joueur.attaques.entites[i].y,64,64),2])
                else:
                    liste_rafraichir.append([joueur.attaques.entites[i].images[1],
                                             (position_ecran_x+joueur.attaques.entites[i].x,position_ecran_y+joueur.attaques.entites[i].y,64,64),2])

                i+=1

            else:

                joueur.attaques.entites[i].temps+=1

                if joueur.attaques.entites[i].temps==1:

                    tileset=pygame.image.load("images/tileset.bmp")

                    joueur.attaques.entites[i].x-=64
                    joueur.attaques.entites[i].y-=64

                    if joueur.attaques.entites[i].x<0:
                        joueur.attaques.entites[i].x=0
                    elif joueur.attaques.entites[i].x>768:
                        joueur.attaques.entites[i].x=768
                    if joueur.attaques.entites[i].y<0:
                        joueur.attaques.entites[i].y=0
                    elif joueur.attaques.entites[i].y>384:
                        joueur.attaques.entites[i]=384

                    for ennemi in map.salles[joueur.salle].ennemis:
                        if collisions(joueur.attaques.entites[i],ennemi.hitbox_degats):
                            ennemi.points_de_vies-=2*joueur.attaque
                            gerer_knockback_contre_monstres(joueur.attaques.entites[i],ennemi,20,joueur,map,liste_rafraichir,position_ecran_x,position_ecran_y)
                    if collisions(joueur.hitbox,joueur.attaques.entites[i]):
                        liste_rafraichir,joueur=rafraichir_vie(position_ecran_x,position_ecran_y,joueur,liste_rafraichir,joueur.points_de_vies-2*joueur.attaque,joueur.vie_maximum)

                    blocs_a_proximite=[]
                    blocs_a_proximite.append([int((joueur.attaques.entites[i].x+32)/64),int((joueur.attaques.entites[i].y+32)/64)])
                    blocs_a_proximite.append([blocs_a_proximite[0][0]+1,blocs_a_proximite[0][1]])
                    blocs_a_proximite.append([blocs_a_proximite[0][0]+2,blocs_a_proximite[0][1]])
                    blocs_a_proximite.append([blocs_a_proximite[0][0],blocs_a_proximite[0][1]+1])
                    blocs_a_proximite.append([blocs_a_proximite[0][0]+1,blocs_a_proximite[0][1]+1])
                    blocs_a_proximite.append([blocs_a_proximite[0][0]+2,blocs_a_proximite[0][1]+1])
                    blocs_a_proximite.append([blocs_a_proximite[0][0]+1,blocs_a_proximite[0][1]+2])
                    blocs_a_proximite.append([blocs_a_proximite[0][0]+2,blocs_a_proximite[0][1]+2])
                    blocs_a_proximite.append([blocs_a_proximite[0][0],blocs_a_proximite[0][1]+2])

                    for j in range(len(blocs_a_proximite)):

                        if map.salles[joueur.salle].blocs_type[blocs_a_proximite[j][1]][blocs_a_proximite[j][0]]==1:
                            map.salles[joueur.salle].blocs_type[blocs_a_proximite[j][1]][blocs_a_proximite[j][0]]=0
                            map.salles[joueur.salle].image.blit(tileset.subsurface((0,0,64,64)),(blocs_a_proximite[j][0]*64,blocs_a_proximite[j][1]*64))
                            liste_rafraichir.append([map.salles[joueur.salle].image.subsurface((blocs_a_proximite[j][0]*64,blocs_a_proximite[j][1]*64,64,64)),
                                                        ((blocs_a_proximite[j][0]*64)+position_ecran_x,(blocs_a_proximite[j][1]*64)+position_ecran_y,64,64),0])

                if joueur.attaques.entites[i].temps==24:
                    liste_rafraichir.append([map.salles[joueur.salle].image.subsurface((joueur.attaques.entites[i].x,joueur.attaques.entites[i].y,192,192)),
                                             (position_ecran_x+joueur.attaques.entites[i].x,position_ecran_y+joueur.attaques.entites[i].y,192,192),2])
                    del joueur.attaques.entites[i]
                    i-=1
                else:
                    liste_rafraichir.append([joueur.attaques.entites[i].images[2],
                                             (position_ecran_x+joueur.attaques.entites[i].x,position_ecran_y+joueur.attaques.entites[i].y,192,192),2])

                i+=1

    return joueur,map,liste_rafraichir

def deplacer_monstres(map,joueur,tempo,liste_rafraichir,position_ecran_x,position_ecran_y,session):

    for i in range(len(map.salles[joueur.salle].ennemis)):

        if not map.salles[joueur.salle].ennemis[i].mort:

            if map.salles[joueur.salle].ennemis[i].type==0:

                liste_rafraichir.append([map.salles[joueur.salle].image.subsurface((map.salles[joueur.salle].ennemis[i].x,map.salles[joueur.salle].ennemis[i].y,64,64)),
                                             (map.salles[joueur.salle].ennemis[i].x+position_ecran_x,map.salles[joueur.salle].ennemis[i].y+position_ecran_y,64,64),0])



                if map.salles[joueur.salle].ennemis[i].x<joueur.x:
                    map.salles[joueur.salle].ennemis[i].deplacement_x=2
                    if map.salles[joueur.salle].ennemis[i].x+1==joueur.x:
                        map.salles[joueur.salle].ennemis[i].deplacement_x=1

                elif map.salles[joueur.salle].ennemis[i].x>joueur.x:
                    map.salles[joueur.salle].ennemis[i].deplacement_x=-2
                    if map.salles[joueur.salle].ennemis[i].x-1==joueur.x:
                        map.salles[joueur.salle].ennemis[i].deplacement_x=-1

                else:
                    map.salles[joueur.salle].ennemis[i].deplacement_x=0

                if map.salles[joueur.salle].ennemis[i].y<joueur.y:
                    map.salles[joueur.salle].ennemis[i].deplacement_y=2
                    if map.salles[joueur.salle].ennemis[i].y+1==joueur.y:
                        map.salles[joueur.salle].ennemis[i].deplacement_y=1

                elif map.salles[joueur.salle].ennemis[i].y>joueur.y:
                    map.salles[joueur.salle].ennemis[i].deplacement_y=-2
                    if map.salles[joueur.salle].ennemis[i].y-1==joueur.y:
                        map.salles[joueur.salle].ennemis[i].deplacement_y=-1

                else:
                    map.salles[joueur.salle].ennemis[i].deplacement_y=0



                if map.salles[joueur.salle].ennemis[i].deplacement_x!=0:

                    map.salles[joueur.salle].ennemis[i].x+=map.salles[joueur.salle].ennemis[i].deplacement_x

                    blocs_a_proximite=[]
                    blocs_a_proximite.append([int(map.salles[joueur.salle].ennemis[i].x/64),int(map.salles[joueur.salle].ennemis[i].y/64)])
                    blocs_a_proximite.append([blocs_a_proximite[0][0]+1,blocs_a_proximite[0][1]])
                    blocs_a_proximite.append([blocs_a_proximite[0][0],blocs_a_proximite[0][1]+1])
                    blocs_a_proximite.append([blocs_a_proximite[0][0]+1,blocs_a_proximite[0][1]+1])

                    j=-1
                    while j!=0:

                        map.salles[joueur.salle].ennemis[i].hitbox_degats.x=map.salles[joueur.salle].ennemis[i].x
                        map.salles[joueur.salle].ennemis[i].hitbox_deplacement.x=map.salles[joueur.salle].ennemis[i].x+16

                        if j>0:
                            if map.salles[joueur.salle].ennemis[i].deplacement_x>0:
                                map.salles[joueur.salle].ennemis[i].x-=1
                            else:
                                map.salles[joueur.salle].ennemis[i].x+=1

                            blocs_a_proximite=[]
                            blocs_a_proximite.append([int(map.salles[joueur.salle].ennemis[i].x/64),int(map.salles[joueur.salle].ennemis[i].y/64)])
                            blocs_a_proximite.append([blocs_a_proximite[0][0]+1,blocs_a_proximite[0][1]])
                            blocs_a_proximite.append([blocs_a_proximite[0][0],blocs_a_proximite[0][1]+1])
                            blocs_a_proximite.append([blocs_a_proximite[0][0]+1,blocs_a_proximite[0][1]+1])

                        j=0

                        for bloc in blocs_a_proximite:

                            if collisions(map.salles[joueur.salle].ennemis[i].hitbox_deplacement,map.salles[joueur.salle].blocs_hitboxs[bloc[1]][bloc[0]]) \
                            and ((map.salles[joueur.salle].blocs_type[bloc[1]][bloc[0]]>=1 \
                            and map.salles[joueur.salle].blocs_type[bloc[1]][bloc[0]]<=11) \
                            or (map.salles[joueur.salle].blocs_type[bloc[1]][bloc[0]]>=1 \
                            and map.salles[joueur.salle].blocs_type[bloc[1]][bloc[0]]>=1)):
                                j=1
                                break

                if map.salles[joueur.salle].ennemis[i].deplacement_y!=0:

                    map.salles[joueur.salle].ennemis[i].y+=map.salles[joueur.salle].ennemis[i].deplacement_y

                    blocs_a_proximite=[]
                    blocs_a_proximite.append([int(map.salles[joueur.salle].ennemis[i].x/64),int(map.salles[joueur.salle].ennemis[i].y/64)])
                    blocs_a_proximite.append([blocs_a_proximite[0][0]+1,blocs_a_proximite[0][1]])
                    blocs_a_proximite.append([blocs_a_proximite[0][0],blocs_a_proximite[0][1]+1])
                    blocs_a_proximite.append([blocs_a_proximite[0][0]+1,blocs_a_proximite[0][1]+1])

                    j=-1
                    while j!=0:

                        map.salles[joueur.salle].ennemis[i].hitbox_degats.y=map.salles[joueur.salle].ennemis[i].y
                        map.salles[joueur.salle].ennemis[i].hitbox_deplacement.y=map.salles[joueur.salle].ennemis[i].y+16

                        if j>0:
                            if map.salles[joueur.salle].ennemis[i].deplacement_y>0:
                                map.salles[joueur.salle].ennemis[i].y-=1
                            else:
                                map.salles[joueur.salle].ennemis[i].y+=1

                            blocs_a_proximite=[]
                            blocs_a_proximite.append([int(map.salles[joueur.salle].ennemis[i].x/64),int(map.salles[joueur.salle].ennemis[i].y/64)])
                            blocs_a_proximite.append([blocs_a_proximite[0][0]+1,blocs_a_proximite[0][1]])
                            blocs_a_proximite.append([blocs_a_proximite[0][0],blocs_a_proximite[0][1]+1])
                            blocs_a_proximite.append([blocs_a_proximite[0][0]+1,blocs_a_proximite[0][1]+1])

                        j=0

                        for bloc in blocs_a_proximite:

                            if collisions(map.salles[joueur.salle].ennemis[i].hitbox_deplacement,map.salles[joueur.salle].blocs_hitboxs[bloc[1]][bloc[0]]) \
                            and ((map.salles[joueur.salle].blocs_type[bloc[1]][bloc[0]]>=1 \
                            and map.salles[joueur.salle].blocs_type[bloc[1]][bloc[0]]<=11) \
                            or (map.salles[joueur.salle].blocs_type[bloc[1]][bloc[0]]>=1 \
                            and map.salles[joueur.salle].blocs_type[bloc[1]][bloc[0]]>=1)):
                                j=1
                                break



                if collisions(map.salles[joueur.salle].ennemis[i].hitbox_degats,joueur.hitbox):
                    if randrange(100)>(15*session.competences[9]):
                        liste_rafraichir,joueur=rafraichir_vie(position_ecran_x,position_ecran_y,joueur,liste_rafraichir,joueur.points_de_vies-map.salles[joueur.salle].ennemis[i].attaque,joueur.vie_maximum)
                    else:
                        if not joueur.invincible:
                            joueur.invincible=True
                            joueur.temps_depuis_invincible=pygame.time.get_ticks()



                if map.salles[joueur.salle].ennemis[i].deplacement_x>0:
                    liste=[map.salles[joueur.salle].ennemis[i].images.droite[int(tempo/8)],(map.salles[joueur.salle].ennemis[i].x+position_ecran_x,map.salles[joueur.salle].ennemis[i].y+position_ecran_y,64,64),4]
                if map.salles[joueur.salle].ennemis[i].deplacement_x<0:
                    liste=[map.salles[joueur.salle].ennemis[i].images.gauche[int(tempo/8)],(map.salles[joueur.salle].ennemis[i].x+position_ecran_x,map.salles[joueur.salle].ennemis[i].y+position_ecran_y,64,64),4]
                if map.salles[joueur.salle].ennemis[i].deplacement_y>0:
                    liste=[map.salles[joueur.salle].ennemis[i].images.bas[int(tempo/8)],(map.salles[joueur.salle].ennemis[i].x+position_ecran_x,map.salles[joueur.salle].ennemis[i].y+position_ecran_y,64,64),4]
                if map.salles[joueur.salle].ennemis[i].deplacement_y<0:
                    liste=[map.salles[joueur.salle].ennemis[i].images.haut[int(tempo/8)],(map.salles[joueur.salle].ennemis[i].x+position_ecran_x,map.salles[joueur.salle].ennemis[i].y+position_ecran_y,64,64),4]
                if map.salles[joueur.salle].ennemis[i].deplacement_x==0 and map.salles[joueur.salle].ennemis[i].deplacement_y==0:
                    liste=[map.salles[joueur.salle].ennemis[i].images.bas[0],(map.salles[joueur.salle].ennemis[i].x+position_ecran_x,map.salles[joueur.salle].ennemis[i].y+position_ecran_y,64,64),4]

                liste_rafraichir.append(liste)

    return map,liste_rafraichir,joueur

def gerer_mort_monstres(map,joueur,liste_rafraichir,position_ecran_x,position_ecran_y,session):

    i=0
    while i <len(map.salles[joueur.salle].ennemis):

        if map.salles[joueur.salle].ennemis[i].mort:

            if map.salles[joueur.salle].ennemis[i].type==0:

                liste_rafraichir.append([map.salles[joueur.salle].image.subsurface((map.salles[joueur.salle].ennemis[i].x,map.salles[joueur.salle].ennemis[i].y,64,64)),
                                         (map.salles[joueur.salle].ennemis[i].x+position_ecran_x,map.salles[joueur.salle].ennemis[i].y+position_ecran_y,64,64),0])

                if randrange(5)<1+session.competences[6]:
                    map.salles[joueur.salle].objets.append(Objet())
                    map.salles[joueur.salle].objets[len(map.salles[joueur.salle].objets)-1].x=map.salles[joueur.salle].ennemis[i].x
                    map.salles[joueur.salle].objets[len(map.salles[joueur.salle].objets)-1].y=map.salles[joueur.salle].ennemis[i].y
                    map.salles[joueur.salle].objets[len(map.salles[joueur.salle].objets)-1].type=7
                    map.salles[joueur.salle].objets[len(map.salles[joueur.salle].objets)-1].image=\
                        pygame.image.load("images/objets_communs.bmp").subsurface((448,0,64,64))
                    map.salles[joueur.salle].objets[len(map.salles[joueur.salle].objets)-1].image.set_colorkey((255,255,255))
                    map.salles[joueur.salle].objets[len(map.salles[joueur.salle].objets)-1].hitbox.x=map.salles[joueur.salle].ennemis[i].x
                    map.salles[joueur.salle].objets[len(map.salles[joueur.salle].objets)-1].hitbox.y=map.salles[joueur.salle].ennemis[i].y
                    map.salles[joueur.salle].objets[len(map.salles[joueur.salle].objets)-1].hitbox.w=64
                    map.salles[joueur.salle].objets[len(map.salles[joueur.salle].objets)-1].hitbox.h=64

                liste_rafraichir,session=rafraichir_xp(position_ecran_x,position_ecran_y,session,liste_rafraichir,session.xp+10)
                liste_rafraichir,joueur=rafraichir_mana(position_ecran_x,position_ecran_y,joueur,liste_rafraichir,session,joueur.mana+10+(5*session.competences[3]))

                del map.salles[joueur.salle].ennemis[i]
                i-=1
        i+=1

    return map,liste_rafraichir,session

def gerer_invincibilite(joueur):

    if joueur.invincible:
        if pygame.time.get_ticks()<(joueur.temps_depuis_invincible+joueur.temps_invincibilite) \
        and joueur.images.bas[0].get_alpha() is None:

            for i in range(6):
                joueur.images.bas[i].set_alpha(150)
                joueur.images.haut[i].set_alpha(150)
                joueur.images.droite[i].set_alpha(150)
                joueur.images.gauche[i].set_alpha(150)

        if pygame.time.get_ticks()>(joueur.temps_depuis_invincible+joueur.temps_invincibilite):
            for i in range(6):
                joueur.images.bas[i].set_alpha()
                joueur.images.haut[i].set_alpha()
                joueur.images.droite[i].set_alpha()
                joueur.images.gauche[i].set_alpha()
            joueur.invincible=False

    return joueur

def gerer_knockback_contre_monstres(repousseur,repousse,force,joueur,map,liste_rafraichir,position_ecran_x,position_ecran_y):

    liste_rafraichir.append([map.salles[joueur.salle].image.subsurface((repousse.x,repousse.y,64,64)),
                             (repousse.x+position_ecran_x,repousse.y+position_ecran_y,64,64),0])

    from math import fabs

    difference_x=fabs(repousse.x-repousseur.x)
    difference_y=fabs(repousse.y-repousseur.y)

    if difference_x>=difference_y:
        if (repousse.x-repousseur.x)>=0:
            deplacement_x=force
        else:
            deplacement_x=-force
        try:
            deplacement_y=-int((((repousseur.y-repousse.y)*(repousseur.x-repousse.x-deplacement_x))/(repousseur.x-repousse.x))+repousse.y-repousseur.y)
        except:
            deplacement_y=0
    else:
        if (repousse.y-repousseur.y)>=0:
            deplacement_y=force
        else:
            deplacement_y=-force
        try:
            deplacement_x=-int((((repousseur.x-repousse.x)*(repousseur.y-repousse.y-deplacement_y))/(repousseur.y-repousse.y))+repousse.x-repousseur.x)
        except:
            deplacement_x=0

    if deplacement_x!=0:

        repousse.x+=deplacement_x

        blocs_a_proximite=[]
        blocs_a_proximite.append([int(repousse.x/64),int(repousse.y/64)])
        blocs_a_proximite.append([blocs_a_proximite[0][0]+1,blocs_a_proximite[0][1]])
        blocs_a_proximite.append([blocs_a_proximite[0][0],blocs_a_proximite[0][1]+1])
        blocs_a_proximite.append([blocs_a_proximite[0][0]+1,blocs_a_proximite[0][1]+1])

        j=-1
        while j!=0:

            repousse.hitbox_degats.x=repousse.x
            repousse.hitbox_deplacement.x=repousse.x+16

            if j>0:
                if deplacement_x>0:
                    repousse.x-=1
                else:
                    repousse.x+=1

                blocs_a_proximite=[]
                blocs_a_proximite.append([int(repousse.x/64),int(repousse.y/64)])
                blocs_a_proximite.append([blocs_a_proximite[0][0]+1,blocs_a_proximite[0][1]])
                blocs_a_proximite.append([blocs_a_proximite[0][0],blocs_a_proximite[0][1]+1])
                blocs_a_proximite.append([blocs_a_proximite[0][0]+1,blocs_a_proximite[0][1]+1])

            j=0

            for bloc in blocs_a_proximite:

                if collisions(repousse.hitbox_deplacement,map.salles[joueur.salle].blocs_hitboxs[bloc[1]][bloc[0]]) \
                and ((map.salles[joueur.salle].blocs_type[bloc[1]][bloc[0]]>=1 \
                and map.salles[joueur.salle].blocs_type[bloc[1]][bloc[0]]<=11) \
                or (map.salles[joueur.salle].blocs_type[bloc[1]][bloc[0]]>=1 \
                and map.salles[joueur.salle].blocs_type[bloc[1]][bloc[0]]>=1)):
                    j=1
                    break

    if deplacement_y!=0:

        repousse.y+=deplacement_y

        blocs_a_proximite=[]
        blocs_a_proximite.append([int(repousse.x/64),int(repousse.y/64)])
        blocs_a_proximite.append([blocs_a_proximite[0][0]+1,blocs_a_proximite[0][1]])
        blocs_a_proximite.append([blocs_a_proximite[0][0],blocs_a_proximite[0][1]+1])
        blocs_a_proximite.append([blocs_a_proximite[0][0]+1,blocs_a_proximite[0][1]+1])

        j=-1
        while j!=0:

            repousse.hitbox_degats.y=repousse.y
            repousse.hitbox_deplacement.y=repousse.y+16

            if j>0:
                if deplacement_y>0:
                    repousse.y-=1
                else:
                    repousse.y+=1

                blocs_a_proximite=[]
                blocs_a_proximite.append([int(repousse.x/64),int(repousse.y/64)])
                blocs_a_proximite.append([blocs_a_proximite[0][0]+1,blocs_a_proximite[0][1]])
                blocs_a_proximite.append([blocs_a_proximite[0][0],blocs_a_proximite[0][1]+1])
                blocs_a_proximite.append([blocs_a_proximite[0][0]+1,blocs_a_proximite[0][1]+1])

            j=0

            for bloc in blocs_a_proximite:

                if collisions(repousse.hitbox_deplacement,map.salles[joueur.salle].blocs_hitboxs[bloc[1]][bloc[0]]) \
                and ((map.salles[joueur.salle].blocs_type[bloc[1]][bloc[0]]>=1 \
                and map.salles[joueur.salle].blocs_type[bloc[1]][bloc[0]]<=11) \
                or (map.salles[joueur.salle].blocs_type[bloc[1]][bloc[0]]>=1 \
                and map.salles[joueur.salle].blocs_type[bloc[1]][bloc[0]]>=1)):
                    j=1
                    break


    return repousse,liste_rafraichir

def charger_minimap(map,joueur):

    minimap_tileset=pygame.image.load("images/minimap.bmp")
    minimap_tileset.set_colorkey((255,255,255))
    minimap=pygame.Surface((128,88))
    minimap.fill((255,255,255))
    minimap.set_colorkey((255,255,255))
    minimap.blit(minimap_tileset.subsurface((0,0,128,88)),(0,0))

    for y in range(5):
        for x in range(5):
            for salle in map.salles:
                if salle.x==map.salles[joueur.salle].x+(x-2) and salle.y==map.salles[joueur.salle].y+(y-2):
                    if salle.visited:
                        if salle.type_salle==1 or salle.type_salle==2:
                            if salle.objets==[]:
                                minimap.blit(minimap_tileset.subsurface((0,88,24,16)),((x*24)+x+2,(y*16)+y+2))
                            else:
                                minimap.blit(minimap_tileset.subsurface((96,88,24,16)),((x*24)+x+2,(y*16)+y+2))
                        if salle.type_salle==3:
                            minimap.blit(minimap_tileset.subsurface((24,88,24,16)),((x*24)+x+2,(y*16)+y+2))
                        if salle.type_salle==4:
                            minimap.blit(minimap_tileset.subsurface((48,88,24,16)),((x*24)+x+2,(y*16)+y+2))
                        if salle.type_salle==5:
                            minimap.blit(minimap_tileset.subsurface((72,88,24,16)),((x*24)+x+2,(y*16)+y+2))
                    if not salle.visited:
                        if salle.type_salle!=5:
                            minimap.blit(minimap_tileset.subsurface((0,104,24,16)),((x*24)+x+2,(y*16)+y+2))
                        if salle.type_salle==5:
                            minimap.blit(minimap_tileset.subsurface((24,104,24,16)),((x*24)+x+2,(y*16)+y+2))

    minimap.blit(minimap_tileset.subsurface((0,120,24,16)),(52,36))

    minimap.set_alpha(225)

    return minimap

def creer_images_et_positions_menu(menu):

    if menu.type==1:

        nombre_de_lignes=0
        ligne_actuelle=0

        for i in range(len(menu.options)):

            if len(menu.options[i].message)*32<menu.w:
                menu.options[i].chaines=[menu.options[i].message]
            else:
                menu.options[i].chaines=menu.options[i].message.split(" ")

                for mot in menu.options[i].chaines:
                    if len(mot)*32>menu.w:
                        raise ValueError("Les mots sont trop longs")

            plus_longue_chaine=0

            for j in range(len(menu.options[i].chaines)):
                if len(menu.options[i].chaines[j])>plus_longue_chaine:
                    plus_longue_chaine=len(menu.options[i].chaines[j])

            menu.options[i].w=32*plus_longue_chaine
            menu.options[i].x=menu.x+((menu.w//2)-(menu.options[i].w//2))

            nombre_de_lignes+=len(menu.options[i].chaines)

            if nombre_de_lignes*65>menu.h:
                raise ValueError("Les options sont trop epaisses / trop nombreuses")

        for i in range(len(menu.options)):

            menu.options[i].h=64*len(menu.options[i].chaines)
            menu.options[i].y=menu.y+(ligne_actuelle*64)+(((menu.h-(nombre_de_lignes*64))//(len(menu.options)+1))*(i+1))
            ligne_actuelle+=len(menu.options[i].chaines)

            menu.options[i].images=[]
            menu.options[i].images.append(pygame.Surface((menu.options[i].w,menu.options[i].h)))
            menu.options[i].images[0].fill((255,255,255))
            menu.options[i].images[0].set_colorkey((255,255,255))
            menu.options[i].images.append(pygame.Surface((menu.options[i].w,menu.options[i].h)))
            menu.options[i].images[1].fill((255,255,255))
            menu.options[i].images[1].set_colorkey((255,255,255))

            caracteres=pygame.image.load("images/ascii.bmp")
            caracteres_selectionnes=pygame.image.load("images/ascii_selectionnee.bmp")

            caracteres.set_colorkey((255,255,255))
            caracteres_selectionnes.set_colorkey((255,255,255))

            for j in range(len(menu.options[i].chaines)):
                for k in range(len(menu.options[i].chaines[j])):
                    menu.options[i].images[0].blit(caracteres.subsurface(((ord(menu.options[i].chaines[j][k])%10)*32,
                                                                          (ord(menu.options[i].chaines[j][k])//10)*64,32,64)),
                                                   (((menu.options[i].w-(len(menu.options[i].chaines[j])*32))//2)+(k*32),j*64))
                    menu.options[i].images[1].blit(caracteres_selectionnes.subsurface(((ord(menu.options[i].chaines[j][k])%10)*32,
                                                                          (ord(menu.options[i].chaines[j][k])//10)*64,32,64)),(k*32,j*64))

    elif menu.type==2:

        nombre_de_caracteres=0

        for option in menu.options:
            nombre_de_caracteres+=len(option.message)

        if nombre_de_caracteres*32>menu.w:
            raise ValueError("Le nombre d'options / La taille des mots est/sont trop élevé(es).")
        if menu.h<64:
            raise ValueError("Le menu n'est pas assez épais. (<64px)")

        nombre_de_caracteres_actuel=0

        for i in range(len(menu.options)):
            menu.options[i].y=menu.y+((menu.h-64)//2)
            menu.options[i].x=menu.x+(nombre_de_caracteres_actuel*32)+((i+1)*((menu.w-(nombre_de_caracteres*32))//(len(menu.options)+1)))
            menu.options[i].h=64
            menu.options[i].w=len(menu.options[i].message)*32
            menu.options[i].images=[]
            for j in range(2):
                menu.options[i].images.append(pygame.Surface((menu.options[i].w,menu.options[i].h)))
                menu.options[i].images[j].fill((255,255,255))
                menu.options[i].images[j].set_colorkey((255,255,255))
            caracteres=pygame.image.load("images/ascii.bmp")
            caracteres_selectionnes=pygame.image.load("images/ascii_selectionnee.bmp")
            caracteres.set_colorkey((255,255,255))
            caracteres_selectionnes.set_colorkey((255,255,255))
            for j in range(len(menu.options[i].message)):
                menu.options[i].images[0].blit(caracteres.subsurface(((ord(menu.options[i].message[j])%10)*32,(ord(menu.options[i].message[j])//10)*64,32,64)),(j*32,0))
                menu.options[i].images[1].blit(caracteres_selectionnes.subsurface(((ord(menu.options[i].message[j])%10)*32,(ord(menu.options[i].message[j])//10)*64,32,64)),(j*32,0))
            nombre_de_caracteres_actuel+=len(menu.options[i].message)


    return menu

def obtenir_choix_menu_et_afficher_selection(menu,ecran,position_souris,liste_rafraichir):

    choix=0

    for entree in pygame.event.get():
        if entree.type==pygame.MOUSEBUTTONUP:
            if entree.button==1:
                for i in range(len(menu.options)):
                    if entree.pos[0]>menu.options[i].x \
                    and entree.pos[0]<menu.options[i].x+menu.options[i].w \
                    and entree.pos[1]>menu.options[i].y \
                    and entree.pos[1]<menu.options[i].y+menu.options[i].h:
                        choix=i+1

        if entree.type==pygame.MOUSEMOTION:
            position_souris=[entree.pos[0],entree.pos[1]]

    for i in range(len(menu.options)):
        if position_souris[0]>menu.options[i].x \
        and position_souris[0]<menu.options[i].x+menu.options[i].w \
        and position_souris[1]>menu.options[i].y \
        and position_souris[1]<menu.options[i].y+menu.options[i].h:
            liste_rafraichir.append([menu.options[i].images[1],(menu.options[i].x,menu.options[i].y,menu.options[i].w,menu.options[i].h),7])
        else:
            liste_rafraichir.append([menu.options[i].images[0],(menu.options[i].x,menu.options[i].y,menu.options[i].w,menu.options[i].h),7])

    return liste_rafraichir,choix,position_souris

def creer_session(ecran,resolution,liste_rafraichir,liste_messages):

    temps_actuel=pygame.time.get_ticks()

    fond=pygame.image.load("images/fond.bmp")
    liste_rafraichir.append([fond,(0,0,resolution.current_w,resolution.current_h),7])

    caracteres=pygame.image.load("images/ascii.bmp")
    caracteres.set_colorkey((255,255,255))

    image_message=pygame.Surface((resolution.current_w,64))

    global VERSION

    session=Session()
    session.competences=[0,0,0,0,0,0,0,0,0,0,0,0]
    session.points_de_competences=0
    session.sorts=[0,0,0,0,0,0,0,0,0,0,0,0]
    session.points_de_sorts=0
    session.niveau=0
    session.xp=0
    session.partie=False
    session.map=None
    session.joueur=None
    session.version=VERSION
    session.nom=""

    position_souris=[0,0]

    menu=Menu()
    menu.x=0
    menu.y=resolution.current_h-300
    menu.w=resolution.current_w
    menu.h=300
    for i in range(4):
        menu.options.append(Options_Menu())
    menu.options[0].message="VALIDER"
    menu.options[1].message="RETOUR"
    menu.type=1
    menu=creer_images_et_positions_menu(menu)

    nom_fini=False

    while not nom_fini:

        liste_messages,liste_rafraichir=afficher_messages(liste_messages,liste_rafraichir,resolution)
        rafraichir_image(liste_rafraichir,ecran)
        liste_rafraichir=[]
        temps_actuel=gerer_fps(temps_actuel)

        choix=0

        for entree in pygame.event.get():
            if entree.type==pygame.KEYDOWN:
                if entree.dict['unicode'].upper()=="A" \
                or entree.dict['unicode'].upper()=="B" \
                or entree.dict['unicode'].upper()=="C" \
                or entree.dict['unicode'].upper()=="D" \
                or entree.dict['unicode'].upper()=="E" \
                or entree.dict['unicode'].upper()=="F" \
                or entree.dict['unicode'].upper()=="G" \
                or entree.dict['unicode'].upper()=="H" \
                or entree.dict['unicode'].upper()=="I" \
                or entree.dict['unicode'].upper()=="J" \
                or entree.dict['unicode'].upper()=="K" \
                or entree.dict['unicode'].upper()=="L" \
                or entree.dict['unicode'].upper()=="M" \
                or entree.dict['unicode'].upper()=="N" \
                or entree.dict['unicode'].upper()=="O" \
                or entree.dict['unicode'].upper()=="P" \
                or entree.dict['unicode'].upper()=="Q" \
                or entree.dict['unicode'].upper()=="R" \
                or entree.dict['unicode'].upper()=="S" \
                or entree.dict['unicode'].upper()=="T" \
                or entree.dict['unicode'].upper()=="U" \
                or entree.dict['unicode'].upper()=="V" \
                or entree.dict['unicode'].upper()=="W" \
                or entree.dict['unicode'].upper()=="X" \
                or entree.dict['unicode'].upper()=="Y" \
                or entree.dict['unicode'].upper()=="Z":
                    session.nom+=entree.dict['unicode'].upper()
                elif entree.key==pygame.K_BACKSPACE:
                    if session.nom!="":
                        session.nom=session.nom[:-1]
                elif entree.key==pygame.K_RETURN:
                    if session.nom!="":
                        chaine="saves/"+session.nom+".txt"
                        try:
                            a=open(chaine,"r")
                            a.close()
                        except:
                            with open("saves/liste_personnages.txt","a") as liste_personnages:
                                liste_personnages.write("\n"+session.nom)
                            with open(chaine,"wb") as session_personnage:
                                pickler=pickle.Pickler(session_personnage)
                                pickler.dump(session)
                            nom_fini=True

            elif entree.type==pygame.MOUSEBUTTONUP:
                if entree.button==1:
                    for i in range(len(menu.options)):
                        if entree.pos[0]>menu.options[i].x \
                        and entree.pos[0]<menu.options[i].x+menu.options[i].w \
                        and entree.pos[1]>menu.options[i].y \
                        and entree.pos[1]<menu.options[i].y+menu.options[i].h:
                            choix=i+1

            elif entree.type==pygame.MOUSEMOTION:
                position_souris=[entree.pos[0],entree.pos[1]]


        chaine="PSEUDO:"+session.nom

        if pygame.time.get_ticks()%500>0 and pygame.time.get_ticks()%500<250:
            chaine+="_"
        else:
            chaine+=" "

        image_message.blit(fond.subsurface((0,(resolution.current_h-64)//2,resolution.current_w,64)),(0,0))

        if len(session.nom)>15:
            session.nom=session.nom[:15]

        for i in range(len(chaine)):
            image_message.blit(caracteres.subsurface(((ord(chaine[i])%10)*32,(ord(chaine[i])//10)*64,32,64)),(32*i+((resolution.current_w-256-(len(session.nom)*32))//2),0))

        liste_rafraichir.append([image_message,(0,(resolution.current_h-64)//2,resolution.current_w,64),7])

        for i in range(len(menu.options)):
            if position_souris[0]>menu.options[i].x \
            and position_souris[0]<menu.options[i].x+menu.options[i].w \
            and position_souris[1]>menu.options[i].y \
            and position_souris[1]<menu.options[i].y+menu.options[i].h:
                liste_rafraichir.append([menu.options[i].images[1],(menu.options[i].x,menu.options[i].y,menu.options[i].w,menu.options[i].h),7])
            else:
                liste_rafraichir.append([menu.options[i].images[0],(menu.options[i].x,menu.options[i].y,menu.options[i].w,menu.options[i].h),7])

        if choix==1:
            if session.nom!="":
                chaine="saves/"+session.nom+".txt"
                try:
                    a=open(chaine,"r")
                    a.close()
                except:
                    with open("saves/liste_personnages.txt","a") as liste_personnages:
                        liste_personnages.write("\n"+session.nom)
                    with open(chaine,"wb") as session_personnage:
                        pickler=pickle.Pickler(session_personnage)
                        pickler.dump(session)
                    nom_fini=True
        elif choix==2:
            liste_rafraichir.append([pygame.image.load("images/fond.bmp"),(0,0,resolution.current_w,resolution.current_h),7])
            return session,1,liste_rafraichir,liste_messages

    return session,0,liste_rafraichir,liste_messages

def choisir_session(ecran,resolution,liste_rafraichir,liste_messages):

    temps_actuel=pygame.time.get_ticks()

    cadre=0
    cadre_noir=0
    personnage_selectionne=-1

    fond=pygame.image.load("images/fond.bmp")
    liste_rafraichir.append([fond,(0,0,resolution.current_w,resolution.current_h),7])

    continuer=True
    position_souris=[0,0]

    with open("saves/liste_personnages.txt","r") as liste_personnages:
        liste_noms_personnages=liste_personnages.read().split("\n")

    i=0
    while i<len(liste_noms_personnages):
        if liste_noms_personnages[i]=="":
            del liste_noms_personnages[i]
            i-=1
        i+=1

    menu=Menu()
    menu.x=0
    menu.y=0
    menu.w=resolution.current_w
    menu.h=resolution.current_h-128
    for i in range(len(liste_noms_personnages)):
        menu.options.append(Options_Menu())
        menu.options[i].message=liste_noms_personnages[i]
    menu.type=1
    menu=creer_images_et_positions_menu(menu)

    options=Menu()
    options.x=0
    options.y=resolution.current_h-128
    options.w=resolution.current_w
    options.h=128
    for i in range(3):
        options.options.append(Options_Menu())
    options.options[0].message="VALIDER"
    options.options[1].message="RETOUR"
    options.options[2].message="SUPPRIMER"
    options.type=2
    options=creer_images_et_positions_menu(options)


    while continuer:

        choix=[0,0]

        for entree in pygame.event.get():
            if entree.type==pygame.MOUSEBUTTONUP:
                if entree.button==1:
                    for i in range(len(menu.options)):
                        if entree.pos[0]>menu.options[i].x \
                        and entree.pos[0]<menu.options[i].x+menu.options[i].w \
                        and entree.pos[1]>menu.options[i].y \
                        and entree.pos[1]<menu.options[i].y+menu.options[i].h:
                            choix[0]=i+1
                    for i in range(len(options.options)):
                        if entree.pos[0]>options.options[i].x \
                        and entree.pos[0]<options.options[i].x+options.options[i].w \
                        and entree.pos[1]>options.options[i].y \
                        and entree.pos[1]<options.options[i].y+options.options[i].h:
                            choix[1]=i+1

            if entree.type==pygame.MOUSEMOTION:
                position_souris=[entree.pos[0],entree.pos[1]]

        for i in range(len(menu.options)):
            if position_souris[0]>menu.options[i].x \
            and position_souris[0]<menu.options[i].x+menu.options[i].w \
            and position_souris[1]>menu.options[i].y \
            and position_souris[1]<menu.options[i].y+menu.options[i].h:
                ecran.blit(menu.options[i].images[1],(menu.options[i].x,menu.options[i].y))
                liste_rafraichir.append([menu.options[i].images[1],(menu.options[i].x,menu.options[i].y,menu.options[i].w,menu.options[i].h),7])
            else:
                liste_rafraichir.append([menu.options[i].images[0],(menu.options[i].x,menu.options[i].y,menu.options[i].w,menu.options[i].h),7])

        for i in range(len(options.options)):
            if position_souris[0]>options.options[i].x \
            and position_souris[0]<options.options[i].x+options.options[i].w \
            and position_souris[1]>options.options[i].y \
            and position_souris[1]<options.options[i].y+options.options[i].h:
                ecran.blit(options.options[i].images[1],(options.options[i].x,options.options[i].y))
                liste_rafraichir.append([options.options[i].images[1],(options.options[i].x,options.options[i].y,options.options[i].w,options.options[i].h),7])
            else:
                liste_rafraichir.append([options.options[i].images[0],(options.options[i].x,options.options[i].y,options.options[i].w,options.options[i].h),7])

        liste_messages,liste_rafraichir=afficher_messages(liste_messages,liste_rafraichir,resolution)
        rafraichir_image(liste_rafraichir,ecran)
        liste_rafraichir=[]
        temps_actuel=gerer_fps(temps_actuel)

        if cadre!=0:
            liste_rafraichir.append([cadre,(menu.options[personnage_selectionne].x-6,menu.options[personnage_selectionne].y-6,menu.options[personnage_selectionne].w+12,menu.options[personnage_selectionne].h+12),7])

        if choix[0]!=0:
            if cadre_noir!=0:
                liste_rafraichir.append([cadre_noir,(menu.options[personnage_selectionne].x-6,menu.options[personnage_selectionne].y-6,menu.options[personnage_selectionne].w+12,menu.options[personnage_selectionne].h+12),7])
            personnage_selectionne=choix[0]-1
            cadre=pygame.Surface((menu.options[personnage_selectionne].w+12,menu.options[personnage_selectionne].h+12))
            cadre.fill((255,255,255))
            cadre.set_colorkey((255,255,255))
            cadre.subsurface((2,2,menu.options[personnage_selectionne].w+8,menu.options[personnage_selectionne].h+8)).fill((255,255,0))
            cadre.subsurface((4,4,menu.options[personnage_selectionne].w+4,menu.options[personnage_selectionne].h+4)).fill((255,255,255))
            cadre_noir=pygame.Surface((menu.options[personnage_selectionne].w+12,menu.options[personnage_selectionne].h+12))
            cadre_noir.blit(fond.subsurface((menu.options[personnage_selectionne].x-6,menu.options[personnage_selectionne].y-6,menu.options[personnage_selectionne].w+12,menu.options[personnage_selectionne].h+12)),(0,0))

        if personnage_selectionne!=-1 and choix[1]==1:
            with open("saves/"+menu.options[personnage_selectionne].message+".txt","rb") as personnage:
                unpickler=pickle.Unpickler(personnage)
                session=unpickler.load()
            a=0
            continuer=False

        if choix[1]==2:
            a=1
            session=None
            liste_rafraichir.append([pygame.image.load("images/fond.bmp"),(0,0,resolution.current_w,resolution.current_h),7])
            continuer=False

        if personnage_selectionne!=-1 and choix[1]==3:
            cadre=0
            liste_rafraichir.append([cadre_noir,(menu.options[personnage_selectionne].x-6,menu.options[personnage_selectionne].y-6,menu.options[personnage_selectionne].w+12,menu.options[personnage_selectionne].h+12),7])
            cadre_noir=0
            os.chdir(os.getcwd()+"/saves")
            os.remove(menu.options[personnage_selectionne].message+".txt")
            path=os.getcwd().split("\\")
            del path[len(path)-1]
            path="\\".join(path)
            os.chdir(path)

            with open("saves/liste_personnages.txt","r+") as liste_personnages:
                chaine=liste_personnages.read().split("\n")
                del chaine[0]
                i=0
                while i<len(chaine):
                    try:
                        open("saves/"+chaine[i]+".txt","r")
                        i+=1
                    except:
                        del chaine[i]
            with open("saves/liste_personnages.txt","w") as liste_personnages:
                liste_personnages.write("\n"+"\n".join(chaine))

            with open("saves/liste_personnages.txt","r") as liste_personnages:
                liste_noms_personnages=liste_personnages.read().split("\n")
            i=0
            while i<len(liste_noms_personnages):
                if liste_noms_personnages[i]=="":
                    del liste_noms_personnages[i]
                    i-=1
                i+=1
            menu.options=[]
            for i in range(len(liste_noms_personnages)):
                menu.options.append(Options_Menu())
                menu.options[i].message=liste_noms_personnages[i]
            menu=creer_images_et_positions_menu(menu)
            fond=pygame.image.load("images/fond.bmp")
            liste_rafraichir.append([fond,(0,0,resolution.current_w,resolution.current_h),1])
            personnage_selectionne=-1

    return session,a,liste_rafraichir,liste_messages

def gerer_menu_jeu(ecran,position_souris,position_ecran_x,position_ecran_y,raccourcis,joueur):

    menu_fond=pygame.image.load("images/menu_jeu.bmp")
    menu_fond.set_colorkey((255,255,255))
    ecran.blit(menu_fond,(position_ecran_x+130,position_ecran_y+38))
    continuer=True

    menu=Menu()
    menu.x=position_ecran_x+130
    menu.y=position_ecran_y+38
    menu.w=700
    menu.h=500
    for i in range(4):
        menu.options.append(Options_Menu())
    menu.options[0].message="CONTINUER"
    menu.options[1].message="RECOMMENCER LA PARTIE"
    menu.options[2].message="QUITTER LA PARTIE"
    menu.options[3].message="QUITTER LE JEU"
    menu.type=1
    menu=creer_images_et_positions_menu(menu)

    while continuer:

        choix=0

        for entree in pygame.event.get():
            if entree.type==pygame.KEYDOWN:
                if entree.key==raccourcis[0]:
                    continuer=False
                    choix=1
                if entree.key==raccourcis[1]:
                    joueur.deplacement_y-=joueur.vitesse
                if entree.key==raccourcis[2]:
                    joueur.deplacement_y+=joueur.vitesse
                if entree.key==raccourcis[3]:
                    joueur.deplacement_x-=joueur.vitesse
                if entree.key==raccourcis[4]:
                    joueur.deplacement_x+=joueur.vitesse
            if entree.type==pygame.KEYUP:
                if entree.key==raccourcis[1]:
                    joueur.deplacement_y+=joueur.vitesse
                if entree.key==raccourcis[2]:
                    joueur.deplacement_y-=joueur.vitesse
                if entree.key==raccourcis[3]:
                    joueur.deplacement_x+=joueur.vitesse
                if entree.key==raccourcis[4]:
                    joueur.deplacement_x-=joueur.vitesse
            if entree.type==pygame.MOUSEBUTTONUP:
                if entree.button==1:
                    joueur.attaques.autorisation.remove(1)
                    for i in range(len(menu.options)):
                        if entree.pos[0]>menu.options[i].x \
                        and entree.pos[0]<menu.options[i].x+menu.options[i].w \
                        and entree.pos[1]>menu.options[i].y \
                        and entree.pos[1]<menu.options[i].y+menu.options[i].h:
                            continuer=False
                            choix=i+1
            if entree.type==pygame.MOUSEMOTION:
                position_souris=[entree.pos[0],entree.pos[1]]
            if entree.type==pygame.MOUSEBUTTONDOWN:
                if entree.button==1:
                    joueur.attaques.autorisation.append(1)

        for i in range(len(menu.options)):
            ecran.blit(menu.options[i].images[0],(menu.options[i].x,menu.options[i].y))

        for i in range(len(menu.options)):
            if position_souris[0]>menu.options[i].x \
            and position_souris[0]<menu.options[i].x+menu.options[i].w \
            and position_souris[1]>menu.options[i].y \
            and position_souris[1]<menu.options[i].y+menu.options[i].h:
                ecran.blit(menu.options[i].images[1],(menu.options[i].x,menu.options[i].y))

        pygame.display.flip()

        pygame.time.wait(30)

    return choix,joueur

def charger_images_monstres(map):

    personnages=pygame.image.load("images/personnages.bmp")

    for i in range(len(map.salles)):

        for j in range(len(map.salles[i].ennemis)):

            map.salles[i].ennemis[j].images.bas=[]
            map.salles[i].ennemis[j].images.haut=[]
            map.salles[i].ennemis[j].images.droite=[]
            map.salles[i].ennemis[j].images.gauche=[]

            for l in range(6):
                map.salles[i].ennemis[j].images.bas.append(personnages.subsurface(l*64,(map.salles[i].ennemis[j].type+1)*64,64,64))
                map.salles[i].ennemis[j].images.haut.append(personnages.subsurface((l+6)*64,(map.salles[i].ennemis[j].type+1)*64,64,64))
                map.salles[i].ennemis[j].images.droite.append(personnages.subsurface((l+12)*64,(map.salles[i].ennemis[j].type+1)*64,64,64))
                map.salles[i].ennemis[j].images.gauche.append(personnages.subsurface((l+18)*64,(map.salles[i].ennemis[j].type+1)*64,64,64))
                map.salles[i].ennemis[j].images.bas[l].set_colorkey((255,255,255))
                map.salles[i].ennemis[j].images.haut[l].set_colorkey((255,255,255))
                map.salles[i].ennemis[j].images.droite[l].set_colorkey((255,255,255))
                map.salles[i].ennemis[j].images.gauche[l].set_colorkey((255,255,255))

    return map

def charger_images_objets(map):

    objets_communs=pygame.image.load("images/objets_communs.bmp")
    objets_rares=pygame.image.load("images/objets_rares.bmp")

    for i in range(len(map.salles)):

        for j in range(len(map.salles[i].objets)):

            if map.salles[i].objets[j].type<1000:
                objets=objets_communs
                map.salles[i].objets[j].image=objets.subsurface(((map.salles[i].objets[j].type-int(map.salles[i].objets[j].type/10))*64,(int(map.salles[i].objets[j].type/10))*64,64,64))
            if map.salles[i].objets[j].type>=1000:
                objets=objets_rares
                map.salles[i].objets[j].type-=1000
                map.salles[i].objets[j].image=objets.subsurface(((map.salles[i].objets[j].type-int(map.salles[i].objets[j].type/10))*64,(int(map.salles[i].objets[j].type/10))*64,64,64))
                map.salles[i].objets[j].type+=1000

            map.salles[i].objets[j].image.set_colorkey((255,255,255))

    return map

def creer_message(liste_messages,resolution,mots):

    split=False

    if len(mots)*32>resolution.current_w:
        mots=mots.split(" ")
        split=True
        for i in range(len(mots)):
            if len(mots[i])*32>resolution.current_w:
                raise ValueError("Le message est trop long.")
        if len(mots)*64>resolution.current_h:
            raise ValueError("Le message est trop épais.")

    message=Message()
    message.w=0
    if split:
        for i in range(len(mots)):
            if len(mots[i])*32>message.w:
                message.w=len(mots[i])*32
        message.h=(len(mots)*64)+8
    else:
        message.w=len(mots)*32
        message.h=72

    message.w+=8

    message.x=(resolution.current_w-message.w)//2
    message.y=(resolution.current_h-message.h)//2

    message.image=pygame.Surface((message.w,message.h))
    message.image.fill((126,88,63))
    message.image.subsurface((2,2,message.w-4,message.h-4)).fill((205,133,63))

    caracteres=pygame.image.load("images/ascii.bmp")
    caracteres.set_colorkey((255,255,255))

    if split:
        for i in range(len(mots)):
            for j in range(mots[i]):
                message.image.blit(caracteres.subsurface(((ord(mots[i][j])%10)*32,(ord(mots[i][j])//10)*64,32,64)),(4+(j*32),4+(i*64)))
    else:
        for i in range(len(mots)):
            message.image.blit(caracteres.subsurface(((ord(mots[i])%10)*32,(ord(mots[i])//10)*64,32,64)),(4+(i*32),4))

    if len(liste_messages)>0:
        i=0
        while i<len(liste_messages):
            liste_messages[i].y-=message.h+4
            if liste_messages[i].y<0:
                del liste_messages[i]
                i-=1
            i+=1

    message.temps_creation=pygame.time.get_ticks()

    liste_messages.append(message)

    return liste_messages

def afficher_messages(liste_messages,liste_rafraichir,resolution):

    i=0
    global fond

    while i<len(liste_messages):
        liste_rafraichir.append([fond.subsurface((0,liste_messages[i].y,resolution.current_w,liste_messages[i].h)),
                                 (0,liste_messages[i].y,resolution.current_w,liste_messages[i].h),1])
        if liste_messages[i].temps_creation>(pygame.time.get_ticks()-4000):
            liste_rafraichir.append([liste_messages[i].image,(liste_messages[i].x,liste_messages[i].y,liste_messages[i].w,liste_messages[i].h),8])
        else:
            del liste_messages[i]
            i-=1
        i+=1

    return liste_messages,liste_rafraichir

def obtenir_nombre_de_saves():

    with open("saves/liste_personnages.txt") as liste_personnages:
        nombre_de_saves=len(liste_personnages.read().split("\n"))-1
        return nombre_de_saves

def choisir_competences(ecran,resolution,liste_rafraichir,liste_messages,session):

    icones=pygame.image.load("images/competences.bmp")
    fond=pygame.image.load("images/fond.bmp")

    while len(session.competences)<12:
        session.competences.append(0)

    liste=[]
    for i in range(12):
        liste.append(session.competences[i])
    points=session.points_de_competences

    continuer=True
    fenetre=[0,0,0,0,0,-1,-1,-1,-1]

    position_souris=[0,0]
    choix=[-1,-1,0]

    arbre_de_competences=[Menu(),Menu(),Menu(),Menu()]

    for i in range(len(arbre_de_competences)):
        arbre_de_competences[i].x=0
        arbre_de_competences[i].y=(resolution.current_h-128)-((i+1)*((resolution.current_h-128)//len(arbre_de_competences)))
        arbre_de_competences[i].w=resolution.current_w
        arbre_de_competences[i].h=(resolution.current_h-128)//len(arbre_de_competences)
        arbre_de_competences[i].type=2

    arbre_de_competences[0].options.append(Options_Menu())
    arbre_de_competences[0].options[0].images=[icones.subsurface((0,0,64,64)),pygame.Surface((64,64)),icones.subsurface((640,0,64,64))]
    arbre_de_competences[0].options[0].images[1].fill((255,0,0))
    arbre_de_competences[0].options[0].images[1].blit(arbre_de_competences[0].options[0].images[0].subsurface((2,2,60,60)),(2,2))

    for i in range(3):
        arbre_de_competences[1].options.append(Options_Menu())
        arbre_de_competences[1].options[i].images=[icones.subsurface((64+(64*i),0,64,64)),pygame.Surface((64,64)),icones.subsurface((704+(64*i),0,64,64))]
        arbre_de_competences[1].options[i].images[1].fill((255,0,0))
        arbre_de_competences[1].options[i].images[1].blit(arbre_de_competences[1].options[i].images[0].subsurface((2,2,60,60)),(2,2))

    for i in range(4):
        arbre_de_competences[2].options.append(Options_Menu())
        arbre_de_competences[2].options[i].images=[icones.subsurface((256+(64*i),0,64,64)),pygame.Surface((64,64)),icones.subsurface((896+(64*i),0,64,64))]
        arbre_de_competences[2].options[i].images[1].fill((255,0,0))
        arbre_de_competences[2].options[i].images[1].blit(arbre_de_competences[2].options[i].images[0].subsurface((2,2,60,60)),(2,2))

    for i in range(4):
        arbre_de_competences[3].options.append(Options_Menu())
        arbre_de_competences[3].options[i].images=[icones.subsurface(((512+(64*i))%640,((512+(64*i))//640)*64,64,64)),pygame.Surface((64,64)),icones.subsurface((640+(512+(64*i))%640,((512+(64*i))//640)*64,64,64))]
        arbre_de_competences[3].options[i].images[1].fill((255,0,0))
        arbre_de_competences[3].options[i].images[1].blit(arbre_de_competences[3].options[i].images[0].subsurface((2,2,60,60)),(2,2))

    for i in range(len(arbre_de_competences)):
        for j in range(len(arbre_de_competences[i].options)):
            arbre_de_competences[i].options[j].w=64
            arbre_de_competences[i].options[j].h=64
            arbre_de_competences[i].options[j].x=(((resolution.current_w-(len(arbre_de_competences[i].options)*64))//(len(arbre_de_competences[i].options)+1))*(j+1))+(j*64)
            arbre_de_competences[i].options[j].y=arbre_de_competences[i].y+((arbre_de_competences[i].h-64)//2)

    menu=Menu()
    menu.x=0
    menu.y=resolution.current_h-128
    menu.w=resolution.current_w
    menu.h=128
    for i in range(3):
        menu.options.append(Options_Menu())
    menu.options[0].message="VALIDER"
    menu.options[1].message="RETOUR"
    menu.options[2].message="REINITIALISER"
    menu.type=2
    menu=creer_images_et_positions_menu(menu)

    temps_actuel=pygame.time.get_ticks()

    while continuer:

        liste_messages,liste_rafraichir=afficher_messages(liste_messages,liste_rafraichir,resolution)
        temps_actuel=gerer_fps(temps_actuel)
        rafraichir_image(liste_rafraichir,ecran)
        liste_rafraichir=[]

        fenetre[7]=fenetre[5]
        fenetre[8]=fenetre[6]
        fenetre[5]=-1
        fenetre[6]=-1
        if choix[0]!=-1 or choix[1]!=-1:
            fenetre[7]=-1
            fenetre[8]=-1
        choix=[-1,-1,0]

        for entree in pygame.event.get():
            if entree.type==pygame.MOUSEBUTTONUP:
                if entree.button==1:
                    for i in range(len(arbre_de_competences[0].options)):
                        if entree.pos[0]>arbre_de_competences[0].options[i].x \
                        and entree.pos[0]<arbre_de_competences[0].options[i].x+arbre_de_competences[0].options[i].w \
                        and entree.pos[1]>arbre_de_competences[0].options[i].y \
                        and entree.pos[1]<arbre_de_competences[0].options[i].y+arbre_de_competences[0].options[i].h:
                            choix[0]=i
                    for i in range(len(arbre_de_competences[1].options)):
                        if entree.pos[0]>arbre_de_competences[1].options[i].x \
                        and entree.pos[0]<arbre_de_competences[1].options[i].x+arbre_de_competences[1].options[i].w \
                        and entree.pos[1]>arbre_de_competences[1].options[i].y \
                        and entree.pos[1]<arbre_de_competences[1].options[i].y+arbre_de_competences[1].options[i].h:
                            choix[0]=i+len(arbre_de_competences[0].options)
                    for i in range(len(arbre_de_competences[2].options)):
                        if entree.pos[0]>arbre_de_competences[2].options[i].x \
                        and entree.pos[0]<arbre_de_competences[2].options[i].x+arbre_de_competences[2].options[i].w \
                        and entree.pos[1]>arbre_de_competences[2].options[i].y \
                        and entree.pos[1]<arbre_de_competences[2].options[i].y+arbre_de_competences[2].options[i].h:
                            choix[0]=i+len(arbre_de_competences[0].options)+len(arbre_de_competences[1].options)
                    for i in range(len(arbre_de_competences[3].options)):
                        if entree.pos[0]>arbre_de_competences[3].options[i].x \
                        and entree.pos[0]<arbre_de_competences[3].options[i].x+arbre_de_competences[3].options[i].w \
                        and entree.pos[1]>arbre_de_competences[3].options[i].y \
                        and entree.pos[1]<arbre_de_competences[3].options[i].y+arbre_de_competences[3].options[i].h:
                            choix[0]=i+len(arbre_de_competences[0].options)+len(arbre_de_competences[1].options)+len(arbre_de_competences[2].options)
                    for i in range(len(menu.options)):
                        if entree.pos[0]>menu.options[i].x \
                        and entree.pos[0]<menu.options[i].x+menu.options[i].w \
                        and entree.pos[1]>menu.options[i].y \
                        and entree.pos[1]<menu.options[i].y+menu.options[i].h:
                            choix[2]=i+1
                if entree.button==3:
                    for i in range(len(arbre_de_competences[0].options)):
                        if entree.pos[0]>arbre_de_competences[0].options[i].x \
                        and entree.pos[0]<arbre_de_competences[0].options[i].x+arbre_de_competences[0].options[i].w \
                        and entree.pos[1]>arbre_de_competences[0].options[i].y \
                        and entree.pos[1]<arbre_de_competences[0].options[i].y+arbre_de_competences[0].options[i].h:
                            choix[1]=i
                    for i in range(len(arbre_de_competences[1].options)):
                        if entree.pos[0]>arbre_de_competences[1].options[i].x \
                        and entree.pos[0]<arbre_de_competences[1].options[i].x+arbre_de_competences[1].options[i].w \
                        and entree.pos[1]>arbre_de_competences[1].options[i].y \
                        and entree.pos[1]<arbre_de_competences[1].options[i].y+arbre_de_competences[1].options[i].h:
                            choix[1]=i+len(arbre_de_competences[0].options)
                    for i in range(len(arbre_de_competences[2].options)):
                        if entree.pos[0]>arbre_de_competences[2].options[i].x \
                        and entree.pos[0]<arbre_de_competences[2].options[i].x+arbre_de_competences[2].options[i].w \
                        and entree.pos[1]>arbre_de_competences[2].options[i].y \
                        and entree.pos[1]<arbre_de_competences[2].options[i].y+arbre_de_competences[2].options[i].h:
                            choix[1]=i+len(arbre_de_competences[0].options)+len(arbre_de_competences[1].options)
                    for i in range(len(arbre_de_competences[3].options)):
                        if entree.pos[0]>arbre_de_competences[3].options[i].x \
                        and entree.pos[0]<arbre_de_competences[3].options[i].x+arbre_de_competences[3].options[i].w \
                        and entree.pos[1]>arbre_de_competences[3].options[i].y \
                        and entree.pos[1]<arbre_de_competences[3].options[i].y+arbre_de_competences[3].options[i].h:
                            choix[1]=i+len(arbre_de_competences[0].options)+len(arbre_de_competences[1].options)+len(arbre_de_competences[2].options)

            if entree.type==pygame.MOUSEMOTION:
                position_souris=[entree.pos[0],entree.pos[1]]

        liste_impossibles=[False,not liste[0]>=2,not liste[0]>=2,not liste[0]>=2,not liste[0]+liste[1]>=4,not liste[0]+liste[1]>=4,
                           not liste[0]+liste[2]>=4,not liste[0]+liste[3]>=4,not liste[0]+liste[1]+liste[4]>=7,
                           not liste[0]+liste[1]+liste[5]>=6,not liste[0]+liste[2]+liste[6]>=6,not liste[0]+liste[3]+liste[7]>=6]

        k=-1
        for j in range(len(arbre_de_competences)):
            for i in range(len(arbre_de_competences[j].options)):
                k+=1
                if liste[k]>0:
                    liste_rafraichir.append([arbre_de_competences[j].options[i].images[1],(arbre_de_competences[j].options[i].x,
                                        arbre_de_competences[j].options[i].y,arbre_de_competences[j].options[i].w,arbre_de_competences[j].options[i].h),7])
                elif liste[k]==0 and not liste_impossibles[k]:
                    liste_rafraichir.append([arbre_de_competences[j].options[i].images[0],(arbre_de_competences[j].options[i].x,
                                        arbre_de_competences[j].options[i].y,arbre_de_competences[j].options[i].w,arbre_de_competences[j].options[i].h),7])
                elif liste[k]==0 and liste_impossibles[k]:
                    liste_rafraichir.append([arbre_de_competences[j].options[i].images[2],(arbre_de_competences[j].options[i].x,
                                        arbre_de_competences[j].options[i].y,arbre_de_competences[j].options[i].w,arbre_de_competences[j].options[i].h),7])

        for i in range(len(menu.options)):
            if position_souris[0]>menu.options[i].x \
            and position_souris[0]<menu.options[i].x+menu.options[i].w \
            and position_souris[1]>menu.options[i].y \
            and position_souris[1]<menu.options[i].y+menu.options[i].h:
                liste_rafraichir.append([menu.options[i].images[1],(menu.options[i].x,menu.options[i].y,menu.options[i].w,menu.options[i].h),7])
            else:
                liste_rafraichir.append([menu.options[i].images[0],(menu.options[i].x,menu.options[i].y,menu.options[i].w,menu.options[i].h),7])

        for i in range(len(arbre_de_competences)):
            for j in range(len(arbre_de_competences[i].options)):
                if position_souris[0]>arbre_de_competences[i].options[j].x \
                and position_souris[0]<arbre_de_competences[i].options[j].x+arbre_de_competences[i].options[j].w \
                and position_souris[1]>arbre_de_competences[i].options[j].y \
                and position_souris[1]<arbre_de_competences[i].options[j].y+arbre_de_competences[i].options[j].h:
                    fenetre[5]=i
                    fenetre[6]=j



        fenetre_fond=[fenetre[0],fenetre[1],fenetre[2],fenetre[3]]

        fenetre[0]=position_souris[0]
        fenetre[1]=position_souris[1]

        if fenetre[5]!=-1 and fenetre[6]!=-1:
            fenetre=creer_fenetre_competences(fenetre,liste,liste_impossibles)

        if fenetre[0]+fenetre[2]>=resolution.current_w:
            fenetre[0]=resolution.current_w-fenetre[2]
        if fenetre[1]+fenetre[3]>=resolution.current_h:
            fenetre[1]=resolution.current_h-fenetre[3]

        if fenetre[5]!=-1 and fenetre[6]!=-1:
            fenetre=creer_fenetre_competences(fenetre,liste,liste_impossibles)
            liste_rafraichir.append([fenetre[4],(fenetre[0],fenetre[1],fenetre[2],fenetre[3]),8])

        if (fenetre[7]!=-1 and fenetre[8]!=-1) or (fenetre[5]!=-1 and fenetre[6]!=-1):
            liste_rafraichir.append([fond.subsurface((fenetre_fond[0],fenetre_fond[1],fenetre_fond[2],fenetre_fond[3])),(fenetre_fond[0],fenetre_fond[1],fenetre_fond[2],fenetre_fond[3]),7])


        if choix[0]!=-1:
            if choix[0]==0:
                if liste[0]<3 and points>0:
                    liste[0]+=1
                    points-=1
            if choix[0]==1:
                if liste[1]<2 and points>0 and liste[0]>=2:
                    liste[1]+=1
                    points-=1
            if choix[0]==2:
                if liste[2]<2 and points>0 and liste[0]>=2:
                    liste[2]+=1
                    points-=1
            if choix[0]==3:
                if liste[3]<2 and points>0 and liste[0]>=2:
                    liste[3]+=1
                    points-=1
            if choix[0]==4:
                if liste[4]<3 and points>0 and liste[0]+liste[1]>=4:
                    liste[4]+=1
                    points-=1
            if choix[0]==5:
                if liste[5]<2 and points>0 and liste[0]+liste[1]>=4:
                    liste[5]+=1
                    points-=1
            if choix[0]==6:
                if liste[6]<2 and points>0 and liste[0]+liste[2]>=4:
                    liste[6]+=1
                    points-=1
            if choix[0]==7:
                if liste[7]<2 and points>0 and liste[0]+liste[3]>=4:
                    liste[7]+=1
                    points-=1
            if choix[0]==8:
                if liste[8]<2 and points>0 and liste[0]+liste[1]+liste[4]>=7:
                    liste[8]+=1
                    points-=1
            if choix[0]==9:
                if liste[9]<3 and points>0 and liste[0]+liste[1]+liste[5]>=6:
                    liste[9]+=1
                    points-=1
            if choix[0]==10:
                if liste[10]<3 and points>0 and liste[0]+liste[2]+liste[6]>=6:
                    liste[10]+=1
                    points-=1
            if choix[0]==11:
                if liste[11]<3 and points>0 and liste[0]+liste[3]+liste[7]>=6:
                    liste[11]+=1
                    points-=1

        if choix[1]!=-1:
            if choix[1]==0:
                if liste[0]>0\
                and (liste[11]==0 or liste[0]+liste[3]+liste[7]>6)\
                and (liste[7]==0 or liste[0]+liste[3]>4)\
                and (liste[3]==0 or liste[0]>2)\
                and (liste[10]==0 or liste[0]+liste[2]+liste[6]>6)\
                and (liste[6]==0 or liste[0]+liste[2]>4)\
                and (liste[2]==0 or liste[0]>2)\
                and (liste[9]==0 or liste[0]+liste[1]+liste[5]>6)\
                and (liste[5]==0 or liste[0]+liste[1]>4)\
                and (liste[1]==0 or liste[0]>2)\
                and (liste[8]==0 or liste[0]+liste[1]+liste[4]>7)\
                and (liste[4]==0 or liste[0]+liste[1]>4):
                    liste[0]-=1
                    points+=1
            if choix[1]==1:
                if liste[1]>0\
                and (liste[4]==0 or liste[0]+liste[1]>4)\
                and (liste[5]==0 or liste[0]+liste[1]>4)\
                and (liste[8]==0 or liste[0]+liste[1]+liste[4]>7)\
                and (liste[9]==0 or liste[0]+liste[1]+liste[5]>6):
                    liste[1]-=1
                    points+=1
            if choix[1]==2:
                if liste[2]>0\
                and (liste[6]==0 or liste[0]+liste[2]>4)\
                and (liste[10]==0 or liste[0]+liste[2]+liste[6]>6):
                    liste[2]-=1
                    points+=1
            if choix[1]==3:
                if liste[3]>0\
                and (liste[7]==0 or liste[0]+liste[3]>4)\
                and (liste[11]==0 or liste[0]+liste[3]+liste[7]>6):
                    liste[3]-=1
                    points+=1
            if choix[1]==4:
                if liste[4]>0\
                and (liste[8]==0 or liste[0]+liste[1]+liste[4]>7):
                    liste[4]-=1
                    points+=1
            if choix[1]==5:
                if liste[5]>0\
                and (liste[9]==0 or liste[0]+liste[1]+liste[5]>6):
                    liste[5]-=1
                    points+=1
            if choix[1]==6:
                if liste[6]>0\
                and (liste[10]==0 or liste[0]+liste[2]+liste[6]>6):
                    liste[6]-=1
                    points+=1
            if choix[1]==7:
                if liste[7]>0\
                and (liste[11]==0 or liste[0]+liste[3]+liste[7]>6):
                    liste[7]-=1
                    points+=1
            if choix[1]==8:
                if liste[8]>0:
                    liste[8]-=1
                    points+=1
            if choix[1]==9:
                if liste[9]>0:
                    liste[9]-=1
                    points+=1
            if choix[1]==10:
                if liste[10]>0:
                    liste[10]-=1
                    points+=1
            if choix[1]==11:
                if liste[11]>0:
                    liste[11]-=1
                    points+=1
        if choix[2]==1:
            session.points_de_competences=points
            session.competences=liste
            continuer=False
            liste_rafraichir=[]
            ecran.blit(fond,(0,0))
            pygame.display.flip()
        if choix[2]==2:
            continuer=False
            liste_rafraichir=[]
            ecran.blit(fond,(0,0))
            pygame.display.flip()
        if choix[2]==3:
            points=session.niveau
            liste=[0,0,0,0,0,0,0,0,0,0,0,0]

    return session,liste_rafraichir,liste_messages

def creer_fenetre_souris(message_fenetre):

    chaines=message_fenetre.split("\n")
    caracteres=pygame.image.load("images/ascii_mini.bmp")
    caracteres.set_colorkey((0,0,0))

    taille_max=0
    for chaine in chaines:
        if len(chaine)>taille_max:
            taille_max=len(chaine)

    w=6+taille_max*12
    h=6+len(chaines)*22
    fenetre=pygame.Surface((w,h))
    fenetre.fill((155,155,155))
    fenetre.subsurface((2,2,w-4,h-4)).fill((0,0,0))

    for i in range(len(chaines)):
        for j in range(len(chaines[i])):
            fenetre.blit(caracteres.subsurface(((ord(chaines[i][j])%10)*12,(ord(chaines[i][j])//10)*20,12,20)),
            (((w-(len(chaines[i])*12))//2)+j*12,i*22+4))

    return fenetre,w,h

def creer_fenetre_competences(fenetre,liste,liste_impossibles):

    if fenetre[5]==0 and fenetre[6]==0:
        if not (fenetre[7]==0 and fenetre[8]==0):
            chaine="Force brute\n\n" \
                    "Amelioration actuelle:\n"
            if liste[0]==0:
                chaine+="Aucune\n"
            else:
                chaine+="Vos attaques infligent\n" \
                        +str(10*liste[0])+" points de degats supplementaires\n"
            chaine+="\nAmelioration du niveau suivant:\n"
            if liste[0]==3:
                chaine+="Aucune\n"
            else:
                chaine+="Vos attaques infligent\n" \
                        +str(10*(liste[0]+1))+" points de degats supplementaires\n"
            chaine+="\nniveau actuel: "+str(liste[0])+"/3"

            fenetre[4],fenetre[2],fenetre[3]=creer_fenetre_souris(chaine)

    if fenetre[5]==1 and fenetre[6]==0:
        if not (fenetre[7]==1 and fenetre[8]==0):
            chaine="Mitraillette ambulante\n\n" \
                   "Amelioration actuelle:\n"
            if liste[1]==0:
                chaine+="Aucune\n"
            elif liste[1]==1:
                chaine+="Le temps entre deux attaques\n" \
                        "est diminue de 5 %\n"
            elif liste[1]==2:
                chaine+="Le temps entre deux attaques\n" \
                        "est diminue de 15 %\n"
            chaine+="\nAmelioration du niveau suivant:\n"
            if liste[1]==0:
                chaine+="Le temps entre deux attaques\n" \
                        "est diminue de 5 %\n"
            elif liste[1]==1:
                chaine+="Le temps entre deux attaques\n" \
                        "est diminue de 15 %\n"
            elif liste[1]==2:
                chaine+="Aucune\n"
            chaine+="\nniveau actuel: "+str(liste[1])+"/2\n"
            if liste_impossibles[1]:
                chaine+="\nVous ne pouvez pas encore debloquer cette competence"

            fenetre[4],fenetre[2],fenetre[3]=creer_fenetre_souris(chaine)

    if fenetre[5]==1 and fenetre[6]==1:
        if not (fenetre[7]==1 and fenetre[8]==1):
            chaine="Sac a vie\n\n" \
                   "Amelioration actuelle:\n"
            if liste[2]==0:
                chaine+="Aucune\n"
            else:
                chaine+="Vos points de vie maximums sont augmentes de "+str(liste[2]*30)+"\n"
            chaine+="\nAmelioration du niveau suivant:\n"
            if liste[2]==2:
                chaine+="Aucune\n"
            else:
                chaine+="Vos points de vie maximums sont augmentes de "+str((liste[2]+1)*30)+"\n"
            chaine+="\nniveau actuel: "+str(liste[2])+"/2\n"
            if liste_impossibles[2]:
                chaine+="\nVous ne pouvez pas encore debloquer cette competence"

            fenetre[4],fenetre[2],fenetre[3]=creer_fenetre_souris(chaine)

    if fenetre[5]==1 and fenetre[6]==2:
        if not (fenetre[7]==1 and fenetre[8]==2):
            chaine="Sorcier\n\n" \
                   "Amelioration actuelle:\n"
            if liste[3]==0:
                chaine+="Aucune\n"
            else:
                chaine+="Vous gagnez "+str(5*liste[3])+" points de mana supplementaires\n" \
                        "lorsque vous tuez un ennemi\n"
            chaine+="\nAmelioration du niveau suivant:\n"
            if liste[3]==2:
                chaine+="Aucune\n"
            else:
                chaine+="Vous gagnez "+str(5*(liste[3]+1))+" points de mana supplementaires\n" \
                        "lorsque vous tuez un ennemi\n"
            chaine+="\nniveau actuel: "+str(liste[3])+"/2\n"
            if liste_impossibles[3]:
                chaine+="\nVous ne pouvez pas encore debloquer cette competence"

            fenetre[4],fenetre[2],fenetre[3]=creer_fenetre_souris(chaine)

    if fenetre[5]==2 and fenetre[6]==0:
        if not (fenetre[7]==2 and fenetre[8]==0):
            chaine="Canon humain\n\n" \
                   "Amelioration actuelle:\n"
            if liste[4]==0:
                chaine+="Aucune\n"
            elif liste[4]==1:
                chaine+="Vos attaques de base se deplacent 20 % plus vite\n"
            elif liste[4]==2:
                chaine+="Vos attaques de base se deplacent 30 % plus vite\n"
            elif liste[4]==3:
                chaine+="Vos attaques de base se deplacent 50 % plus vite\n"

            chaine+="\nAmelioration du niveau suivant:\n"
            if liste[4]==3:
                chaine+="Aucune\n"
            elif liste[4]==0:
                chaine+="Vos attaques de base se deplacent 20 % plus vite\n"
            elif liste[4]==1:
                chaine+="Vos attaques de base se deplacent 30 % plus vite\n"
            elif liste[4]==2:
                chaine+="Vos attaques de base se deplacent 50 % plus vite\n"
            chaine+="\nniveau actuel: "+str(liste[4])+"/3\n"
            if liste_impossibles[4]:
                chaine+="\nVous ne pouvez pas encore debloquer cette competence"

            fenetre[4],fenetre[2],fenetre[3]=creer_fenetre_souris(chaine)

    if fenetre[5]==2 and fenetre[6]==1:
        if not (fenetre[7]==2 and fenetre[8]==1):
            chaine="Sonic en herbe\n\n" \
                   "Amelioration actuelle:\n"
            if liste[5]==0:
                chaine+="Aucune\n"
            else:
                chaine+="Vous vous deplacez "+str(liste[5]*20)+"% plus vite\n"
            chaine+="\nAmelioration du niveau suivant:\n"
            if liste[5]==2:
                chaine+="Aucune\n"
            else:
                chaine+="Vous vous deplacez "+str((liste[5]+1)*20)+"% plus vite\n"
            chaine+="\nniveau actuel: "+str(liste[5])+"/2\n"
            if liste_impossibles[5]:
                chaine+="\nVous ne pouvez pas encore debloquer cette competence"

            fenetre[4],fenetre[2],fenetre[3]=creer_fenetre_souris(chaine)

    if fenetre[5]==2 and fenetre[6]==2:
        if not (fenetre[7]==2 and fenetre[8]==2):
            chaine="Carnivore\n\n" \
                   "Amelioration actuelle:\n"
            if liste[6]==0:
                chaine+="Aucune\n"
            else:
                chaine+="Vous avez "+str(100+100*liste[6])+"% de chances supplementaires\n" \
                        "d'obtenir un coeur sur les ennemis\n"
            chaine+="\nAmelioration du niveau suivant:\n"
            if liste[6]==2:
                chaine+="Aucune\n"
            else:
                chaine+="Vous avez "+str(100+100*(liste[6]+1))+"% de chances supplementaires\n" \
                        "d'obtenir un coeur sur les ennemis\n"
            chaine+="\nniveau actuel: "+str(liste[6])+"/2\n"
            if liste_impossibles[6]:
                chaine+="\nVous ne pouvez pas encore debloquer cette competence"

            fenetre[4],fenetre[2],fenetre[3]=creer_fenetre_souris(chaine)

    if fenetre[5]==2 and fenetre[6]==3:
        if not (fenetre[7]==2 and fenetre[8]==3):
            chaine="Reservoir magique\n\n" \
                   "Amelioration actuelle:\n"
            if liste[7]==0:
                chaine+="Aucune\n"
            else:
                chaine+="Votre mana maximum augmente de "+str(20*liste[7])+"\n"
            chaine+="\nAmelioration du niveau suivant:\n"
            if liste[7]==2:
                chaine+="Aucune\n"
            else:
                chaine+="Votre mana maximum augmente de "+str(20*(liste[7]+1))+"\n"
            chaine+="\nniveau actuel: "+str(liste[7])+"/2\n"
            if liste_impossibles[7]:
                chaine+="\nVous ne pouvez pas encore debloquer cette competence"

            fenetre[4],fenetre[2],fenetre[3]=creer_fenetre_souris(chaine)

    if fenetre[5]==3 and fenetre[6]==0:
        if not (fenetre[7]==3 and fenetre[8]==0):
            chaine="Bomber-man\n\n" \
                   "Amelioration actuelle:\n"
            if liste[8]==0:
                chaine+="Aucune\n"
            else:
                chaine+="Vos attaques explosent a l'impact et infligent "+str(50*liste[8])+"%\n" \
                        "d'une attaque normale aux ennemis proches\n"
            chaine+="\nAmelioration du niveau suivant:\n"
            if liste[8]==2:
                chaine+="Aucune\n"
            else:
                chaine+="Vos attaques explosent a l'impact et infligent "+str(50*(liste[8]+1))+"%\n" \
                        "d'une attaque normale aux ennemis proches\n"
            chaine+="\nniveau actuel: "+str(liste[8])+"/2\n"
            if liste_impossibles[8]:
                chaine+="\nVous ne pouvez pas encore debloquer cette competence"

            fenetre[4],fenetre[2],fenetre[3]=creer_fenetre_souris(chaine)

    if fenetre[5]==3 and fenetre[6]==1:
        if not (fenetre[7]==3 and fenetre[8]==1):
            chaine="Ninja\n\n" \
                   "Amelioration actuelle:\n"
            if liste[9]==0:
                chaine+="Aucune\n"
            else:
                chaine+="Lorsqu'un ennemi vous touche, vous avez "+str(15*liste[9])+"%\n" \
                        "de chances d'obtenir un temps d'invincibilite sans perdre de points de vie\n"
            chaine+="\nAmelioration du niveau suivant:\n"
            if liste[9]==3:
                chaine+="Aucune\n"
            else:
                chaine+="Lorsqu'un ennemi vous touche, vous avez "+str(15*(liste[9]+1))+"%\n" \
                        "de chances d'obtenir un temps d'invincibilite sans perdre de points de vie\n"
            chaine+="\nniveau actuel: "+str(liste[9])+"/3\n"
            if liste_impossibles[9]:
                chaine+="\nVous ne pouvez pas encore debloquer cette competence"

            fenetre[4],fenetre[2],fenetre[3]=creer_fenetre_souris(chaine)

    if fenetre[5]==3 and fenetre[6]==2:
        if not (fenetre[7]==3 and fenetre[8]==2):
            chaine="Vampire\n\n" \
                   "Amelioration actuelle:\n"
            if liste[10]==0:
                chaine+="Aucune\n"
            else:
                chaine+="Vous regagnez "+str(2*liste[10])+" points de vie a chaque\n" \
                        "fois que vous attaquez un ennemi\n"
            chaine+="\nAmelioration du niveau suivant:\n"
            if liste[10]==3:
                chaine+="Aucune\n"
            else:
                chaine+="Vous regagnez "+str(2*(liste[10]+1))+" points de vie a chaque\n" \
                        "fois que vous attaquez un ennemi\n"
            chaine+="\nniveau actuel: "+str(liste[10])+"/3\n"
            if liste_impossibles[10]:
                chaine+="\nVous ne pouvez pas encore debloquer cette competence"

            fenetre[4],fenetre[2],fenetre[3]=creer_fenetre_souris(chaine)

    if fenetre[5]==3 and fenetre[6]==3:
        if not (fenetre[7]==3 and fenetre[8]==3):
            chaine="Aspirateur magique\n\n" \
                   "Amelioration actuelle:\n"
            if liste[11]==0:
                chaine+="Aucune\n"
            else:
                chaine+="Vous gagnez "+str(liste[11])+" points de mana par seconde\n" \
                        "tant qu'il y a des ennemis dans la meme salle\n"
            chaine+="\nAmelioration du niveau suivant:\n"
            if liste[11]==3:
                chaine+="Aucune\n"
            else:
                chaine+="Vous gagnez "+str(liste[11]+1)+" points de mana par seconde\n" \
                        "tant qu'il y a des ennemis dans la meme salle\n"
            chaine+="\nniveau actuel: "+str(liste[11])+"/3\n"
            if liste_impossibles[11]:
                chaine+="\nVous ne pouvez pas encore debloquer cette competence"

            fenetre[4],fenetre[2],fenetre[3]=creer_fenetre_souris(chaine)

    return fenetre