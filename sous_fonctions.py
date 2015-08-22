# -*- coding:Utf-8 -*

import os
import pickle
import time
from random import randrange
from classes import *

VERSION = "0.1.1"

FOND = pygame.image.load("images/fond.bmp")
TILESET = pygame.image.load("images/tileset.bmp")
PERSONNAGES = pygame.image.load("images/personnages.bmp")
OBJETS = pygame.image.load("images/objets_communs.bmp")
OBJETS_RARES = pygame.image.load("images/objets_rares.bmp")
INTERFACE = pygame.image.load("images/interface.bmp")
CARACTERES = pygame.image.load("images/ascii.bmp")
CARACTERES_SELECTIONNES = pygame.image.load("images/ascii_selectionnee.bmp")
CARACTERES_MINI = pygame.image.load("images/ascii_mini.bmp")
ATTAQUES_JOUEUR = pygame.image.load("images/attaques_joueur.bmp")
MINIMAP = pygame.image.load("images/minimap.bmp")
FOND_MENU_JEU = pygame.image.load("images/menu_jeu.bmp")
ICONES_COMPETENCES = pygame.image.load("images/competences.bmp")

PERSONNAGES.set_colorkey((255, 255, 255))
OBJETS.set_colorkey((255, 255, 255))
OBJETS_RARES.set_colorkey((255, 255, 255))
INTERFACE.set_colorkey((255, 255, 255))
CARACTERES.set_colorkey((255, 255, 255))
CARACTERES_SELECTIONNES.set_colorkey((255, 255, 255))
CARACTERES_MINI.set_colorkey((0, 0, 0))
ATTAQUES_JOUEUR.set_colorkey((255, 255, 255))
MINIMAP.set_colorkey((255, 255, 255))
FOND_MENU_JEU.set_colorkey((255, 255, 255))
ICONES_COMPETENCES.set_colorkey((255, 255, 255))


def placer_salles(niveau):

    nombre_de_salles = randrange(8+niveau, 10+(2*niveau))  # OBTENIR LE NOMBRE DE SALLES NORMALES/TRESOR
    if nombre_de_salles > 150:
        nombre_de_salles = 150

    nombre_de_salles_au_tresor_verouillees = randrange(niveau+1)  # OBTENIR LE NOMBRE DE SALLES VEROUILLEES
    if nombre_de_salles_au_tresor_verouillees > 50:
        nombre_de_salles_au_tresor_verouillees = 50

    tableau = []  # CREER LE TABLEAU DE SALLES POUR CONNAITRE LEUR EMPLACEMENT ( VIDE POUR LE MOMENT )
    for i in range(nombre_de_salles+1):
        tableau.append([0]*nombre_de_salles)

    x = nombre_de_salles//2  # PLACER LE SPAWN
    y = nombre_de_salles//2
    tableau[y][x] = 2

    i = 0

    # PLACER TOUTES LES SALLES DANS LE TABLEAU

    while i < (nombre_de_salles+nombre_de_salles_au_tresor_verouillees):

        m = randrange(1000)  # OBTENIR LE TYPE DE SALLE: NORMALE/TRESOR
        if 0 <= m <= 25:
            prototype = 2
        else:
            prototype = 0

        if i == nombre_de_salles-1:  # OBTENIR LE TYPE DE SALLE: FINALE
            prototype = 3

        if i > nombre_de_salles-1:  # PLACER LES SALLES VEROUILLEES, APRES AVOIR PLACE LES SALLES NORMALES/TRESOR
            while True:
                xa = randrange(nombre_de_salles)
                ya = randrange(nombre_de_salles)
                try:
                    if tableau[ya][xa] == 0 and \
                       ((tableau[ya+1][xa] != 0 and tableau[ya+1][xa] != 5)
                       or (tableau[ya-1][xa] != 0 and tableau[ya-1][xa] != 5)
                       or (tableau[ya][xa+1] != 0 and tableau[ya][xa+1] != 5)
                       or (tableau[ya][xa-1] != 0 and tableau[ya][xa-1] != 5)):
                        tableau[ya][xa] = 5
                        i += 1
                        break
                except:
                    continue
            continue

        n = randrange(4)  # PLACER LES SALLES: NORMALE/TRESOR/FINALE ; AVEC LA TECHNIQUE DU NAIN BOURRE

        if n == 0 and x < (nombre_de_salles-1):
            if tableau[y][x+1] == 0:
                tableau[y][x+1] = 1+prototype
                i += 1
            x += 1
        if n == 1 and x > 0:
            if tableau[y][x-1] == 0:
                tableau[y][x-1] = 1+prototype
                i += 1
            x -= 1
        if n == 2 and y < (nombre_de_salles-1):
            if tableau[y+1][x] == 0:
                tableau[y+1][x] = 1+prototype
                i += 1
            y += 1
        if n == 3 and y > 0:
            if tableau[y-1][x] == 0:
                tableau[y-1][x] = 1+prototype
                i += 1
            y -= 1

    # REMPLIR LA VARIABLE MAP A PARTIR DU TABLEAU

    map = Map(nombre_de_salles+1+nombre_de_salles_au_tresor_verouillees)
    map.salles = []
    for i in range(map.nombre_de_salles):
        map.salles.append(Salle())

    for i in range(len(tableau)):
        map.carte_map.append(list(tableau[i]))

    map.niveau = niveau

    i = 0
    for j in range(nombre_de_salles):
        for k in range(nombre_de_salles):
            if tableau[j][k] != 0:
                map.salles[i].type_salle = tableau[j][k]
                map.salles[i].x = k
                map.salles[i].y = j
                i += 1

    return map


def generer_salles(map):

    fichier = open("patterns.txt", "r")  # RECUPERATION DES PATTERNS DE SALLES

    chaine_obtenue = fichier.read()
    liste_paternes = chaine_obtenue.split("\n")

    for i in range(len(liste_paternes)):
        liste_paternes[i] = liste_paternes[i].split(" ")

    # GENERATION DE L'INTERIEUR DES SALLES

    for i in range(map.nombre_de_salles):

        if map.salles[i].type_salle == 1:  # REMPLIR LES SALLES NORMALES
            a = randrange(int(len(liste_paternes)/10))

            chaine_obtenue = ""
            j = 0
            while chaine_obtenue != [str(a)]:
                chaine_obtenue = liste_paternes[j]
                j += 1

            while liste_paternes[j] != [str(a+1)]:
                for l in range(9):
                    map.salles[i].blocs_type.append(list(liste_paternes[j]))
                    j += 1

            h = 0
            g = 0
            for j in range(9):  # AJOUTER LES OBJETS ET MONSTRES POTENTIELS A PARTIR DES PATTERNS

                for k in range(15):

                    if map.salles[i].blocs_type[j][k] == "1001":

                        map.salles[i].blocs_type[j][k] = 1
                        map.salles[i].objets_potentiels.append(Objet())
                        map.salles[i].objets_potentiels[h].x = k*64
                        map.salles[i].objets_potentiels[h].y = j*64
                        h += 1

                    elif map.salles[i].blocs_type[j][k] == "2000":

                        map.salles[i].blocs_type[j][k] = 0
                        map.salles[i].ennemis_potentiels.append(Ennemis())
                        map.salles[i].ennemis_potentiels[g].x = k*64
                        map.salles[i].ennemis_potentiels[g].y = j*64
                        g += 1

        elif map.salles[i].type_salle == 2 or \
                map.salles[i].type_salle == 3 or \
                map.salles[i].type_salle == 5:  # REMPLIR LES SALLES DE SPAWN/DE TRESOR/VEROUILLEES

            map.salles[i].blocs_type = \
                [
                    [9, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 8],
                    [3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3],
                    [3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3],
                    [3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3],
                    [3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3],
                    [3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3],
                    [3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3],
                    [3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3],
                    [11, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 10],
                ]

        elif map.salles[i].type_salle == 4:  # REMPLIR LES SALLES FINALES

            map.salles[i].blocs_type = \
                [
                    [9, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 8],
                    [3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3],
                    [3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3],
                    [3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3],
                    [3, 0, 0, 0, 0, 0, 0, 12, 0, 0, 0, 0, 0, 0, 3],
                    [3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3],
                    [3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3],
                    [3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3],
                    [11, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 10],
                ]

        # AJOUTER LES PORTES

        for j in range(map.nombre_de_salles):

                # LES PORTES NORMALES

                if map.salles[i].x+1 == map.salles[j].x and \
                   map.salles[i].y == map.salles[j].y and \
                   map.salles[j].type_salle != 5:
                    map.salles[i].blocs_type[4][14] = 6

                if map.salles[i].x-1 == map.salles[j].x and \
                   map.salles[i].y == map.salles[j].y and \
                   map.salles[j].type_salle != 5:
                    map.salles[i].blocs_type[4][0] = 7

                if map.salles[i].y+1 == map.salles[j].y and \
                   map.salles[i].x == map.salles[j].x and \
                   map.salles[j].type_salle != 5:
                    map.salles[i].blocs_type[8][7] = 5

                if map.salles[i].y-1 == map.salles[j].y and \
                   map.salles[i].x == map.salles[j].x and \
                   map.salles[j].type_salle != 5:
                    map.salles[i].blocs_type[0][7] = 4

                # LES PORTES VEROUILLEES

                if map.salles[i].x+1 == map.salles[j].x and \
                   map.salles[i].y == map.salles[j].y and \
                   map.salles[j].type_salle == 5:
                    map.salles[i].blocs_type[4][14] = 20

                if map.salles[i].x-1 == map.salles[j].x and \
                   map.salles[i].y == map.salles[j].y and \
                   map.salles[j].type_salle == 5:
                    map.salles[i].blocs_type[4][0] = 21

                if map.salles[i].y+1 == map.salles[j].y and \
                   map.salles[i].x == map.salles[j].x and \
                   map.salles[j].type_salle == 5:
                    map.salles[i].blocs_type[8][7] = 19

                if map.salles[i].y-1 == map.salles[j].y and \
                   map.salles[i].x == map.salles[j].x and \
                   map.salles[j].type_salle == 5:
                    map.salles[i].blocs_type[0][7] = 18

        map.salles[i].visited = False

    return map


def generer_images_salles(map, i):

    global TILESET
    map.salles[i].image = pygame.Surface((960, 576))

    for j in range(9):
        for h in range(15):
            map.salles[i].blocs_type[j][h] = int(map.salles[i].blocs_type[j][h])
            map.salles[i].image.blit(TILESET.subsurface((map.salles[i].blocs_type[j][h] % 10)*64,
                                                        (map.salles[i].blocs_type[j][h]//10)*64, 64, 64),
                                     (h*64, j*64))

    return map


def generer_hitboxs(map, i):

    for y in range(9):

        map.salles[i].blocs_hitboxs.append([])
        for x in range(15):

            map.salles[i].blocs_hitboxs[y].append(Hitbox())
            map.salles[i].blocs_hitboxs[y][x].x = x*64
            map.salles[i].blocs_hitboxs[y][x].y = y*64
            map.salles[i].blocs_hitboxs[y][x].w = 64
            map.salles[i].blocs_hitboxs[y][x].h = 64

    return map


def charger_image_joueur(joueur):

    global PERSONNAGES

    joueur.images.bas = []
    joueur.images.haut = []
    joueur.images.droite = []
    joueur.images.gauche = []

    for l in range(6):
        joueur.images.bas.append(PERSONNAGES.subsurface(l*64, 0, 64, 64))
        joueur.images.haut.append(PERSONNAGES.subsurface((l+6)*64, 0, 64, 64))
        joueur.images.droite.append(PERSONNAGES.subsurface((l+12)*64, 0, 64, 64))
        joueur.images.gauche.append(PERSONNAGES.subsurface((l+18)*64, 0, 64, 64))
        joueur.images.bas[l].set_colorkey((255, 255, 255))
        joueur.images.haut[l].set_colorkey((255, 255, 255))
        joueur.images.droite[l].set_colorkey((255, 255, 255))
        joueur.images.gauche[l].set_colorkey((255, 255, 255))

    return joueur


def initialiser_joueur(map, joueur):

    # PLACER LE JOUEUR DANS LA SALLE ACTUELLE

    if joueur.salle == -1:  # SI LE JOUEUR COMMENCE UN NOUVEL ETAGE
        joueur.x = 448
        joueur.y = 256
        i = 0
        while map.salles[i].type_salle != 2:
            i += 1
        joueur.salle = i
    else:  # POUR PASSER D'UNE SALLE A L'AUTRE
        i = 0
        if joueur.x >= 832:
            joueur.x = 64
            joueur.y = 256
            while map.salles[joueur.salle].x != (map.salles[i].x-1) or map.salles[joueur.salle].y != map.salles[i].y:
                i += 1
        elif joueur.x < 128:
            joueur.x = 832
            joueur.y = 256
            while map.salles[joueur.salle].x != (map.salles[i].x+1) or map.salles[joueur.salle].y != map.salles[i].y:
                i += 1
        elif joueur.y >= 448:
            joueur.x = 448
            joueur.y = 64
            while map.salles[joueur.salle].y != (map.salles[i].y-1) or map.salles[joueur.salle].x != map.salles[i].x:
                i += 1
        elif joueur.y < 128:
            joueur.x = 448
            joueur.y = 448
            while map.salles[joueur.salle].y != (map.salles[i].y+1) or map.salles[joueur.salle].x != map.salles[i].x:
                i += 1

        joueur.salle = i

    return joueur


def initialiser_ennemis(map, joueur):

    if not map.salles[joueur.salle].visited:

        if map.salles[joueur.salle].type_salle == 1:  # GENERATION D'ENNEMIS POUR LES SALLES NORMALES

            global PERSONNAGES

            if randrange(2) == 0:  # UNE CHANCE SUR DEUX D'AVOIR DES ENNEMIS

                for i in range(randrange(len(map.salles[joueur.salle].ennemis_potentiels))):
                    map.salles[joueur.salle].ennemis.append(Ennemis())

                    map.salles[joueur.salle].ennemis[i].x = map.salles[joueur.salle].ennemis_potentiels[i].x
                    map.salles[joueur.salle].ennemis[i].y = map.salles[joueur.salle].ennemis_potentiels[i].y

                    map.salles[joueur.salle].ennemis[i].type = randrange((PERSONNAGES.get_size()[1]//64)-1)

                    map.salles[joueur.salle].ennemis[i].attaque = 10+(map.niveau*map.niveau)\
                        - ((map.niveau*randrange(map.niveau))//2)
                    map.salles[joueur.salle].ennemis[i].points_de_vies_maximum = map.salles[joueur.salle].ennemis[i].attaque*10
                    map.salles[joueur.salle].ennemis[i].points_de_vies = map.salles[joueur.salle].ennemis[i].points_de_vies_maximum

                    map.salles[joueur.salle].ennemis[i].hitbox_degats.x = map.salles[joueur.salle].ennemis[i].x
                    map.salles[joueur.salle].ennemis[i].hitbox_degats.y = map.salles[joueur.salle].ennemis[i].y
                    map.salles[joueur.salle].ennemis[i].hitbox_degats.w = 64
                    map.salles[joueur.salle].ennemis[i].hitbox_degats.h = 64
                    map.salles[joueur.salle].ennemis[i].hitbox_deplacement.x = map.salles[joueur.salle].ennemis[i].x+16
                    map.salles[joueur.salle].ennemis[i].hitbox_deplacement.y = map.salles[joueur.salle].ennemis[i].y+16
                    map.salles[joueur.salle].ennemis[i].hitbox_deplacement.w = 32
                    map.salles[joueur.salle].ennemis[i].hitbox_deplacement.h = 48

                    map.salles[joueur.salle].ennemis[i].mort = False

                    map.salles[joueur.salle].ennemis[i].minibarre = Minibarre()
                    map.salles[joueur.salle].ennemis[i].minibarre.x = map.salles[joueur.salle].ennemis[i].x
                    map.salles[joueur.salle].ennemis[i].minibarre.y = map.salles[joueur.salle].ennemis[i].y+66
                    map.salles[joueur.salle].ennemis[i].minibarre.w = 64
                    map.salles[joueur.salle].ennemis[i].minibarre.h = 8
                    map.salles[joueur.salle].ennemis[i].minibarre.image = pygame.Surface((64, 8))
                    map.salles[joueur.salle].ennemis[i].minibarre.image.fill((0, 0, 0))
                    map.salles[joueur.salle].ennemis[i].minibarre.image.set_colorkey((255, 255, 255))

                    for l in range(6):
                        map.salles[joueur.salle].ennemis[i].images.bas.append(
                            PERSONNAGES.subsurface((l*64, (map.salles[joueur.salle].ennemis[i].type+1)*64, 64, 64)))
                        map.salles[joueur.salle].ennemis[i].images.haut.append(
                            PERSONNAGES.subsurface(((l+6)*64, (map.salles[joueur.salle].ennemis[i].type+1)*64, 64, 64)))
                        map.salles[joueur.salle].ennemis[i].images.droite.append(
                            PERSONNAGES.subsurface(((l+12)*64, (map.salles[joueur.salle].ennemis[i].type+1)*64, 64, 64)))
                        map.salles[joueur.salle].ennemis[i].images.gauche.append(
                            PERSONNAGES.subsurface(((l+18)*64, (map.salles[joueur.salle].ennemis[i].type+1)*64, 64, 64)))
                        map.salles[joueur.salle].ennemis[i].images.bas[l].set_colorkey((255, 255, 255))
                        map.salles[joueur.salle].ennemis[i].images.haut[l].set_colorkey((255, 255, 255))
                        map.salles[joueur.salle].ennemis[i].images.droite[l].set_colorkey((255, 255, 255))
                        map.salles[joueur.salle].ennemis[i].images.gauche[l].set_colorkey((255, 255, 255))

    return map


def initialiser_objets(map, joueur):

    if not map.salles[joueur.salle].visited:

        # GENERATION D'OBJETS DANS LES SALLES NORMALES

        if map.salles[joueur.salle].type_salle == 1:

            global OBJETS

            compteur = 0
            for i in range(len(map.salles[joueur.salle].objets_potentiels)):

                if randrange(3) == 0:  # LA PROBABILITE D'AVOIR LE Xeme OBJET = 1/(3*X)

                    n = randrange(len(map.salles[joueur.salle].objets_potentiels))
                    map.salles[joueur.salle].objets.append(Objet())
                    map.salles[joueur.salle].objets[compteur].x = map.salles[joueur.salle].objets_potentiels[n].x
                    map.salles[joueur.salle].objets[compteur].y = map.salles[joueur.salle].objets_potentiels[n].y
                    map.salles[joueur.salle].objets[compteur].hitbox.x = map.salles[joueur.salle].objets[compteur].x
                    map.salles[joueur.salle].objets[compteur].hitbox.y = map.salles[joueur.salle].objets[compteur].y
                    map.salles[joueur.salle].objets[compteur].hitbox.w = 64
                    map.salles[joueur.salle].objets[compteur].hitbox.h = 64
                    map.salles[joueur.salle].blocs_type[map.salles[joueur.salle].objets[compteur].y//64][map.salles[joueur.salle].objets[compteur].x//64] = 0

                    type = randrange(100)  # CHOISIR L'OBJET
                    if type < 25:
                        map.salles[joueur.salle].objets[compteur].type = 0
                    elif 50 > type >= 25:
                        map.salles[joueur.salle].objets[compteur].type = 2
                    elif 75 > type >= 50:
                        map.salles[joueur.salle].objets[compteur].type = 4
                    elif 85 > type >= 75:
                        map.salles[joueur.salle].objets[compteur].type = 1
                    elif 92 > type >= 85:
                        map.salles[joueur.salle].objets[compteur].type = 3
                    elif 97 > type >= 92:
                        map.salles[joueur.salle].objets[compteur].type = 5
                    elif 100 > type >= 97:
                        map.salles[joueur.salle].objets[compteur].type = 6

                    map.salles[joueur.salle].objets[compteur].image = \
                        OBJETS.subsurface(((map.salles[joueur.salle].objets[compteur].type % 10)*64,
                                           (map.salles[joueur.salle].objets[compteur].type//10)*64, 64, 64))
                    map.salles[joueur.salle].objets[compteur].image.set_colorkey((255, 255, 255))

                    del map.salles[joueur.salle].objets_potentiels[n]
                    compteur += 1
                else:
                    break

        # GENERATION D'UN OBJET RARE DANS LES SALLES VEROUILLEES/SALLES DE TRESOR

        elif map.salles[joueur.salle].type_salle == 3 or map.salles[joueur.salle].type_salle == 5:

            global OBJETS_RARES

            objet = Objet()
            objet.x = 448
            objet.y = 256
            objet.type = 1000+randrange(8)
            objet.image = OBJETS_RARES.subsurface((((objet.type-1000) % 10)*64, ((objet.type-1000)//10)*64, 64, 64))
            objet.image.set_colorkey((255, 255, 255))
            objet.hitbox.x = 448
            objet.hitbox.y = 256
            objet.hitbox.w = 64
            objet.hitbox.h = 64
            map.salles[joueur.salle].objets.append(objet)
            map.salles[joueur.salle].blocs_type[map.salles[joueur.salle].objets[0].y//64][map.salles[joueur.salle].objets[0].x//64] = 0

    return map


def rafraichir_image(liste_rafraichir, ecran):

    # FONCTION TRES IMPORTANTE !

    liste = []
    for i in range(9):
        for j in range(len(liste_rafraichir)):
            if liste_rafraichir[j][2] == i:
                ecran.blit(liste_rafraichir[j][0], liste_rafraichir[j][1])
                liste.append(liste_rafraichir[j][1])

    pygame.display.update(liste)

    return 0


def collisions(rect_un, rect_deux):

    # RENVOI TRUE S'IL Y A COLLISION ENTRE DEUX RECTANGLES

    if rect_un.x >= rect_deux.x + rect_deux.w or \
       rect_deux.x >= rect_un.x + rect_un.w or \
       rect_un.y >= rect_deux.y + rect_deux.h or \
       rect_deux.y >= rect_un.y + rect_un.h:
        return False
    else:
        return True


def gerer_portes(map, joueur, liste_rafraichir, position_ecran_x, position_ecran_y):

    global TILESET

    # OUVRIR LES PORTES NORMALES ET LES TRAPES

    if len(map.salles[joueur.salle].ennemis) == 0 and not map.salles[joueur.salle].visited:
        map.salles[joueur.salle].visited = True

        if map.salles[joueur.salle].blocs_type[0][7] == 4:
            map.salles[joueur.salle].blocs_type[0][7] = 14
            map.salles[joueur.salle].image.blit(TILESET.subsurface((256, 64, 64, 64)), (448, 0))
            liste_rafraichir.append([map.salles[joueur.salle].image.subsurface((448, 0, 64, 64)),
                                     (448+position_ecran_x, position_ecran_y, 64, 64), 0])

        if map.salles[joueur.salle].blocs_type[4][0] == 7:
            map.salles[joueur.salle].blocs_type[4][0] = 17
            map.salles[joueur.salle].image.blit(TILESET.subsurface((448, 64, 64, 64)), (0, 256))
            liste_rafraichir.append([map.salles[joueur.salle].image.subsurface((0, 256, 64, 64)),
                                     (position_ecran_x, 256+position_ecran_y, 64, 64), 0])

        if map.salles[joueur.salle].blocs_type[8][7] == 5:
            map.salles[joueur.salle].blocs_type[8][7] = 15
            map.salles[joueur.salle].image.blit(TILESET.subsurface((320, 64, 64, 64)), (448, 512))
            liste_rafraichir.append([map.salles[joueur.salle].image.subsurface((448, 512, 64, 64)),
                                     (448+position_ecran_x, 512+position_ecran_y, 64, 64), 0])

        if map.salles[joueur.salle].blocs_type[4][14] == 6:
            map.salles[joueur.salle].blocs_type[4][14] = 16
            map.salles[joueur.salle].image.blit(TILESET.subsurface((384, 64, 64, 64)), (896, 256))
            liste_rafraichir.append([map.salles[joueur.salle].image.subsurface((896, 256, 64, 64)),
                                     (896+position_ecran_x, 256+position_ecran_y, 64, 64), 0])

        if map.salles[joueur.salle].type_salle == 4:
            map.salles[joueur.salle].blocs_type[4][7] = 13
            map.salles[joueur.salle].image.blit(TILESET.subsurface((192, 64, 64, 64)), (448, 256))
            liste_rafraichir.append([map.salles[joueur.salle].image.subsurface((448, 256, 64, 64)),
                                     (448+position_ecran_x, 256+position_ecran_y, 64, 64), 0])

    # OUVRIR LES PORTES VEROUILLEES

    if len(map.salles[joueur.salle].ennemis) == 0 and \
       (map.salles[joueur.salle].blocs_type[0][7] == 18 or
       map.salles[joueur.salle].blocs_type[4][0] == 21 or
       map.salles[joueur.salle].blocs_type[8][7] == 19 or
       map.salles[joueur.salle].blocs_type[4][14] == 20):

        salle_ouverte = -1

        if map.salles[joueur.salle].blocs_type[0][7] == 18 and \
           496 > joueur.x > 432 and \
           joueur.y == 48 and \
           joueur.deplacement_y < 0 and \
           joueur.cles:
            liste_rafraichir, joueur =\
                rafraichir_cles(position_ecran_x, position_ecran_y, joueur, liste_rafraichir, joueur.cles-1)
            map.salles[joueur.salle].blocs_type[0][7] = 14
            map.salles[joueur.salle].image.blit(TILESET.subsurface((256, 64, 64, 64)), (448, 0))
            liste_rafraichir.append([map.salles[joueur.salle].image.subsurface((448, 0, 64, 64)),
                                     (448+position_ecran_x, position_ecran_y, 64, 64), 0])

            for i in range(len(map.salles)):
                if map.salles[joueur.salle].x == map.salles[i].x and \
                   map.salles[joueur.salle].y == map.salles[i].y+1:
                    salle_ouverte = i

        if map.salles[joueur.salle].blocs_type[4][0] == 21 and \
           304 > joueur.y > 240 and \
           joueur.x == 48 and \
           joueur.deplacement_x < 0 and \
           joueur.cles:
            liste_rafraichir, joueur =\
                rafraichir_cles(position_ecran_x, position_ecran_y, joueur, liste_rafraichir, joueur.cles-1)
            map.salles[joueur.salle].blocs_type[4][0] = 17
            map.salles[joueur.salle].image.blit(TILESET.subsurface((448, 64, 64, 64)), (0, 256))
            liste_rafraichir.append([map.salles[joueur.salle].image.subsurface((0, 256, 64, 64)),
                                     (position_ecran_x, 256+position_ecran_y, 64, 64), 0])

            for i in range(len(map.salles)):
                if map.salles[joueur.salle].x == map.salles[i].x+1 and \
                   map.salles[joueur.salle].y == map.salles[i].y:
                    salle_ouverte = i

        if map.salles[joueur.salle].blocs_type[8][7] == 19 and \
           496 > joueur.x > 432 and \
           joueur.y == 448 and \
           joueur.deplacement_y > 0 and \
           joueur.cles:
            liste_rafraichir, joueur =\
                rafraichir_cles(position_ecran_x, position_ecran_y, joueur, liste_rafraichir, joueur.cles-1)
            map.salles[joueur.salle].blocs_type[8][7] = 15
            map.salles[joueur.salle].image.blit(TILESET.subsurface((320, 64, 64, 64)), (448, 512))
            liste_rafraichir.append([map.salles[joueur.salle].image.subsurface((448, 512, 64, 64)),
                                     (448+position_ecran_x, 512+position_ecran_y, 64, 64), 0])

            for i in range(len(map.salles)):
                if map.salles[joueur.salle].x == map.salles[i].x and \
                   map.salles[joueur.salle].y == map.salles[i].y-1:
                    salle_ouverte = i

        if map.salles[joueur.salle].blocs_type[4][14] == 20 and \
           joueur.x == 848 and \
           304 > joueur.y > 240 and \
           joueur.deplacement_x > 0 and \
           joueur.cles:
            liste_rafraichir, joueur =\
                rafraichir_cles(position_ecran_x, position_ecran_y, joueur, liste_rafraichir, joueur.cles-1)
            map.salles[joueur.salle].blocs_type[4][14] = 16
            map.salles[joueur.salle].image.blit(TILESET.subsurface((384, 64, 64, 64)), (896, 256))
            liste_rafraichir.append([map.salles[joueur.salle].image.subsurface((896, 256, 64, 64)),
                                     (896+position_ecran_x, 256+position_ecran_y, 64, 64), 0])

            for i in range(len(map.salles)):
                if map.salles[joueur.salle].x == map.salles[i].x-1 and \
                   map.salles[joueur.salle].y == map.salles[i].y:
                    salle_ouverte = i

        # TRANSFORMER TOUTES LES PORTES VEROUILLEES DE LA SALLE QUE L'ON VIENT DE DEBLOQUER

        if salle_ouverte != -1:
            for i in range(len(map.salles)):
                if map.salles[i].x == map.salles[salle_ouverte].x and \
                   map.salles[i].y == map.salles[salle_ouverte].y-1 and \
                   i != joueur.salle:
                    if map.salles[i].visited:
                        map.salles[i].blocs_type[8][7] = 15
                    else:
                        map.salles[i].blocs_type[8][7] = 5

                if map.salles[i].x == map.salles[salle_ouverte].x-1 and \
                   map.salles[i].y == map.salles[salle_ouverte].y and \
                   i != joueur.salle:
                    if map.salles[i].visited:
                        map.salles[i].blocs_type[4][14] = 16
                    else:
                        map.salles[i].blocs_type[4][14] = 6

                if map.salles[i].x == map.salles[salle_ouverte].x and \
                   map.salles[i].y == map.salles[salle_ouverte].y+1 and \
                   i != joueur.salle:
                    if map.salles[i].visited:
                        map.salles[i].blocs_type[0][7] = 14
                    else:
                        map.salles[i].blocs_type[0][7] = 4

                if map.salles[i].x == map.salles[salle_ouverte].x+1 and \
                   map.salles[i].y == map.salles[salle_ouverte].y and \
                   i != joueur.salle:
                    if map.salles[i].visited:
                        map.salles[i].blocs_type[4][0] = 17
                    else:
                        map.salles[i].blocs_type[4][0] = 7

    return map, liste_rafraichir, joueur


def gerer_fps(temps_actuel):

    temps_precedent = temps_actuel
    temps_actuel = pygame.time.get_ticks()

    print(temps_actuel-temps_precedent)

    if (temps_actuel-temps_precedent) < 35:
        pygame.time.wait(30-(temps_actuel-temps_precedent))
        temps_actuel = pygame.time.get_ticks()

    return temps_actuel


def afficher_objets(map, liste_rafraichir, position_ecran_x, position_ecran_y, joueur):

    for i in range(len(map.salles[joueur.salle].objets)):
        liste_rafraichir.append([map.salles[joueur.salle].objets[i].image,
                                 (map.salles[joueur.salle].objets[i].x+position_ecran_x,
                                  map.salles[joueur.salle].objets[i].y+position_ecran_y, 64, 64), 1])

    return liste_rafraichir


def deplacer_personnage(map, joueur, liste_rafraichir, tempo, position_ecran_x, position_ecran_y):

    # EFFACER IMAGE JOUEUR

    liste_rafraichir.append([map.salles[joueur.salle].image.subsurface((joueur.x, joueur.y, 64, 64)),
                             (joueur.x+position_ecran_x, joueur.y+position_ecran_y, 64, 64), 0])

    # DEPLACER LE JOUEUR

    if joueur.deplacement_x != 0:  # DEPLACER SUR L'AXE DES X

        joueur.x += joueur.deplacement_x

        blocs_a_proximite = list()
        blocs_a_proximite.append([joueur.x//64, joueur.y//64])
        blocs_a_proximite.append([blocs_a_proximite[0][0]+1, blocs_a_proximite[0][1]])
        blocs_a_proximite.append([blocs_a_proximite[0][0], blocs_a_proximite[0][1]+1])
        blocs_a_proximite.append([blocs_a_proximite[0][0]+1, blocs_a_proximite[0][1]+1])

        joueur.hitbox.x = joueur.x+16
        joueur.hitbox.y = joueur.y+16

        for i in range(4):  # FAIRE RECULER LE JOUEUR DE 1 TANT QU'IL EST EN COLLISION AVEC LE DECORS

            while collisions(joueur.hitbox, map.salles[joueur.salle].blocs_hitboxs[blocs_a_proximite[i][1]][blocs_a_proximite[i][0]]) and \
                (11 >= map.salles[joueur.salle].blocs_type[blocs_a_proximite[i][1]][blocs_a_proximite[i][0]] >= 1 or
                 21 >= map.salles[joueur.salle].blocs_type[blocs_a_proximite[i][1]][blocs_a_proximite[i][0]] >= 18):

                if joueur.deplacement_x > 0:
                    joueur.x -= 1
                else:
                    joueur.x += 1

                joueur.hitbox.x = joueur.x+16

                if joueur.x//64 != blocs_a_proximite[0][0]:
                    blocs_a_proximite = list()
                    blocs_a_proximite.append([joueur.x//64, joueur.y//64])
                    blocs_a_proximite.append([blocs_a_proximite[0][0]+1, blocs_a_proximite[0][1]])
                    blocs_a_proximite.append([blocs_a_proximite[0][0], blocs_a_proximite[0][1]+1])
                    blocs_a_proximite.append([blocs_a_proximite[0][0]+1, blocs_a_proximite[0][1]+1])

    if joueur.deplacement_y != 0:  # DEPLACER SUR L'AXE DES Y

        joueur.y += joueur.deplacement_y

        blocs_a_proximite = list()
        blocs_a_proximite.append([joueur.x//64, joueur.y//64])
        blocs_a_proximite.append([blocs_a_proximite[0][0]+1, blocs_a_proximite[0][1]])
        blocs_a_proximite.append([blocs_a_proximite[0][0], blocs_a_proximite[0][1]+1])
        blocs_a_proximite.append([blocs_a_proximite[0][0]+1, blocs_a_proximite[0][1]+1])

        joueur.hitbox.x = joueur.x+16
        joueur.hitbox.y = joueur.y+16

        for i in range(4):  # FAIRE RECULER LE JOUEUR DE 1 TANT QU'IL EST EN COLLISION AVEC LE DECORS

            while collisions(joueur.hitbox, map.salles[joueur.salle].blocs_hitboxs[blocs_a_proximite[i][1]][blocs_a_proximite[i][0]]) and \
                (11 >= map.salles[joueur.salle].blocs_type[blocs_a_proximite[i][1]][blocs_a_proximite[i][0]] >= 1 or
                 21 >= map.salles[joueur.salle].blocs_type[blocs_a_proximite[i][1]][blocs_a_proximite[i][0]] >= 18):

                if joueur.deplacement_y > 0:
                    joueur.y -= 1
                else:
                    joueur.y += 1

                joueur.hitbox.y = joueur.y+16

                if joueur.y//64 != blocs_a_proximite[0][1]:
                    blocs_a_proximite = list()
                    blocs_a_proximite.append([joueur.x//64, joueur.y//64])
                    blocs_a_proximite.append([blocs_a_proximite[0][0]+1, blocs_a_proximite[0][1]])
                    blocs_a_proximite.append([blocs_a_proximite[0][0], blocs_a_proximite[0][1]+1])
                    blocs_a_proximite.append([blocs_a_proximite[0][0]+1, blocs_a_proximite[0][1]+1])

    # AFFICHER LE JOUEUR APRES LE DEPLACEMENT

    if joueur.deplacement_x > 0 and \
       joueur.attaques.autorisation == [] and \
       joueur.deplacement_y == 0:  # SI LE JOUEUR N'ATTAQUE PAS
        liste_rafraichir.append([joueur.images.droite[tempo//8],
                                 (joueur.x+position_ecran_x, joueur.y+position_ecran_y, 64, 64), 4])
    if joueur.deplacement_x < 0 and \
       joueur.attaques.autorisation == [] and \
       joueur.deplacement_y == 0:
        liste_rafraichir.append([joueur.images.gauche[tempo//8],
                                 (joueur.x+position_ecran_x, joueur.y+position_ecran_y, 64, 64), 4])
    if joueur.deplacement_y > 0 and joueur.attaques.autorisation == []:
        liste_rafraichir.append([joueur.images.bas[tempo//8],
                                 (joueur.x+position_ecran_x, joueur.y+position_ecran_y, 64, 64), 4])
    if joueur.deplacement_y < 0 and joueur.attaques.autorisation == []:
        liste_rafraichir.append([joueur.images.haut[tempo//8],
                                 (joueur.x+position_ecran_x, joueur.y+position_ecran_y, 64, 64), 4])
    if joueur.deplacement_x == 0 and joueur.deplacement_y == 0 and joueur.attaques.autorisation == []:
        liste_rafraichir.append([joueur.images.bas[0],
                                 (joueur.x+position_ecran_x, joueur.y+position_ecran_y, 64, 64), 4])

    if joueur.deplacement_x > 0 and \
       joueur.attaques.autorisation != [] and \
       joueur.deplacement_y == 0:  # SI LE JOUEUR ATTAQUE
        liste_rafraichir.append([joueur.images.droite[3+(tempo//8)],
                                 (joueur.x+position_ecran_x, joueur.y+position_ecran_y, 64, 64), 4])
    if joueur.deplacement_x < 0 and \
       joueur.attaques.autorisation != [] and \
       joueur.deplacement_y == 0:
        liste_rafraichir.append([joueur.images.gauche[3+(tempo//8)],
                                 (joueur.x+position_ecran_x, joueur.y+position_ecran_y, 64, 64), 4])
    if joueur.deplacement_y > 0 and joueur.attaques.autorisation != []:
        liste_rafraichir.append([joueur.images.bas[3+(tempo//8)],
                                 (joueur.x+position_ecran_x, joueur.y+position_ecran_y, 64, 64), 4])
    if joueur.deplacement_y < 0 and joueur.attaques.autorisation != []:
        liste_rafraichir.append([joueur.images.haut[3+(tempo//8)],
                                 (joueur.x+position_ecran_x, joueur.y+position_ecran_y, 64, 64), 4])
    if joueur.deplacement_x == 0 and joueur.deplacement_y == 0 and joueur.attaques.autorisation != []:
        liste_rafraichir.append([joueur.images.bas[3],
                                 (joueur.x+position_ecran_x, joueur.y+position_ecran_y, 64, 64), 4])

    blocs_a_proximite = list()
    blocs_a_proximite.append([joueur.x//64, joueur.y//64])
    blocs_a_proximite.append([blocs_a_proximite[0][0]+1, blocs_a_proximite[0][1]])
    blocs_a_proximite.append([blocs_a_proximite[0][0], blocs_a_proximite[0][1]+1])
    blocs_a_proximite.append([blocs_a_proximite[0][0]+1, blocs_a_proximite[0][1]+1])

    return liste_rafraichir, blocs_a_proximite


def gerer_tempo(tempo):
    return (tempo+1)%24


def ramasser_objets(map, joueur, liste_rafraichir, position_ecran_x, position_ecran_y):

    i = 0

    # VERIFIER S'IL Y A COLLISION, REGARDER LE TYPE D'OBJET, AJOUTER LA STAT, ET SUPPRIMER L'OBJET

    while i < len(map.salles[joueur.salle].objets):

        if collisions(joueur.hitbox, map.salles[joueur.salle].objets[i].hitbox):

            if map.salles[joueur.salle].objets[i].type == 0:
                liste_rafraichir, joueur = \
                    rafraichir_bombes(position_ecran_x, position_ecran_y, joueur, liste_rafraichir, joueur.bombes+1)
            if map.salles[joueur.salle].objets[i].type == 1:
                liste_rafraichir, joueur = \
                    rafraichir_bombes(position_ecran_x, position_ecran_y, joueur, liste_rafraichir, joueur.bombes+3)
            if map.salles[joueur.salle].objets[i].type == 2:
                liste_rafraichir, joueur = \
                    rafraichir_cles(position_ecran_x, position_ecran_y, joueur, liste_rafraichir, joueur.cles+1)
            if map.salles[joueur.salle].objets[i].type == 3:
                liste_rafraichir, joueur = \
                    rafraichir_cles(position_ecran_x, position_ecran_y, joueur, liste_rafraichir, joueur.cles+3)
            if map.salles[joueur.salle].objets[i].type == 4:
                liste_rafraichir, joueur = \
                    rafraichir_argent(position_ecran_x, position_ecran_y, joueur, liste_rafraichir, joueur.argent+1)
            if map.salles[joueur.salle].objets[i].type == 5:
                liste_rafraichir, joueur = \
                    rafraichir_argent(position_ecran_x, position_ecran_y, joueur, liste_rafraichir, joueur.argent+5)
            if map.salles[joueur.salle].objets[i].type == 6:
                liste_rafraichir, joueur = \
                    rafraichir_argent(position_ecran_x, position_ecran_y, joueur, liste_rafraichir, joueur.argent+10)
            if map.salles[joueur.salle].objets[i].type == 7:
                liste_rafraichir, joueur = rafraichir_vie(position_ecran_x, position_ecran_y, joueur, liste_rafraichir,
                                                          joueur.points_de_vies+10, joueur.vie_maximum)
            if map.salles[joueur.salle].objets[i].type == 1000:
                liste_rafraichir, joueur = \
                    rafraichir_bombes(position_ecran_x, position_ecran_y, joueur, liste_rafraichir, 99)
            if map.salles[joueur.salle].objets[i].type == 1001:
                liste_rafraichir, joueur = \
                    rafraichir_cles(position_ecran_x, position_ecran_y, joueur, liste_rafraichir, 99)
            if map.salles[joueur.salle].objets[i].type == 1002:
                liste_rafraichir, joueur = \
                    rafraichir_argent(position_ecran_x, position_ecran_y, joueur, liste_rafraichir, joueur.argent+50)
            if map.salles[joueur.salle].objets[i].type == 1003:
                joueur.vitesse += 1
            if map.salles[joueur.salle].objets[i].type == 1004 or \
               map.salles[joueur.salle].objets[i].type == 1005:
                joueur.attaque += 2
            if map.salles[joueur.salle].objets[i].type == 1006 or \
               map.salles[joueur.salle].objets[i].type == 1007:
                liste_rafraichir, joueur = rafraichir_vie(position_ecran_x, position_ecran_y, joueur,
                                                          liste_rafraichir, joueur.points_de_vies+5, joueur.vie_maximum+5)

            if joueur.vitesse > 10:
                joueur.vitesse = 10
            if joueur.vitesse_attaque < 75:
                joueur.vitesse_attaque = 75
            if joueur.deplacement_x > 0:
                joueur.deplacement_x = joueur.vitesse
            if joueur.deplacement_x < 0:
                joueur.deplacement_x = -joueur.vitesse
            if joueur.deplacement_y > 0:
                joueur.deplacement_y = joueur.vitesse
            if joueur.deplacement_y < 0:
                joueur.deplacement_y = -joueur.vitesse

            liste_rafraichir.append([map.salles[joueur.salle].image.subsurface(
                (map.salles[joueur.salle].objets[i].x, map.salles[joueur.salle].objets[i].y, 64, 64)),
                (map.salles[joueur.salle].objets[i].x+position_ecran_x,
                 map.salles[joueur.salle].objets[i].y+position_ecran_y, 64, 64), 1])

            del map.salles[joueur.salle].objets[i]
            i -= 1
        i += 1

    return map, joueur, liste_rafraichir


def afficher_interface(position_ecran_x, position_ecran_y, ecran, joueur, session):

    global INTERFACE
    global CARACTERES
    global OBJETS

    # AFFICHER LE FOND DE L'INTERFACE

    for i in range(15):
        ecran.blit(INTERFACE.subsurface((0, 64, 64, 64)), (position_ecran_x+(64*i), position_ecran_y-64))
        ecran.blit(INTERFACE.subsurface((0, 64, 64, 64)), (position_ecran_x+(64*i), position_ecran_y+576))
        if i < 9:
            ecran.blit(INTERFACE.subsurface((0, 64, 64, 64)), (position_ecran_x+960, position_ecran_y+(i*64)))

    for i in range(3):
        ecran.blit(INTERFACE.subsurface((84, 64, 2, 64)), (position_ecran_x+(144*(i+1)), position_ecran_y-64))
        ecran.blit(INTERFACE.subsurface((64, 64, 20, 64)), (position_ecran_x+(144*i)+64, position_ecran_y-64))

    # AFFICHER LE NOMBRE DE BOMBES

    ecran.blit(OBJETS.subsurface((0, 0, 64, 64)), (position_ecran_x, position_ecran_y-64))
    ecran.blit(INTERFACE.subsurface(((joueur.bombes//10)*30, 0, 30, 64)), (position_ecran_x+84, position_ecran_y-64))
    ecran.blit(INTERFACE.subsurface(((joueur.bombes % 10)*30, 0, 30, 64)), (position_ecran_x+114, position_ecran_y-64))

    # AFFICHER LE NOMBRE DE CLES

    ecran.blit(OBJETS.subsurface((128, 0, 64, 64)), (position_ecran_x+144, position_ecran_y-64))
    ecran.blit(INTERFACE.subsurface(((joueur.cles//10)*30, 0, 30, 64)), (position_ecran_x+228, position_ecran_y-64))
    ecran.blit(INTERFACE.subsurface(((joueur.cles % 10)*30, 0, 30, 64)), (position_ecran_x+258, position_ecran_y-64))

    # AFFICHER LE NOMBRE DE PIECES

    ecran.blit(OBJETS.subsurface((384, 0, 64, 64)), (position_ecran_x+288, position_ecran_y-64))
    ecran.blit(INTERFACE.subsurface(((joueur.argent//10)*30, 0, 30, 64)), (position_ecran_x+372, position_ecran_y-64))
    ecran.blit(INTERFACE.subsurface(((joueur.argent % 10)*30, 0, 30, 64)), (position_ecran_x+402, position_ecran_y-64))

    # AFFICHER LA BARRE DE VIE

    for i in range(int((joueur.points_de_vies/joueur.vie_maximum)*450)):
        ecran.blit(INTERFACE.subsurface((86, 64, 1, 32)), (position_ecran_x+510+i, position_ecran_y-64))
    for i in range(450-int((joueur.points_de_vies/joueur.vie_maximum)*450)):
        ecran.blit(INTERFACE.subsurface((86, 96, 1, 32)), (position_ecran_x+959-i, position_ecran_y-64))
    ecran.blit(INTERFACE.subsurface((84, 64, 2, 32)), (position_ecran_x+510, position_ecran_y-64))

    # AFFICHER LA BARRE DE MANA

    mana_max = 100+(20*session.competences[7])

    for i in range(450):
        if i <= int(joueur.mana*(450/mana_max)):
            ecran.blit(INTERFACE.subsurface((87, 64, 1, 32)), (position_ecran_x+510+i, position_ecran_y-32))
        else:
            ecran.blit(INTERFACE.subsurface((86, 96, 1, 32)), (position_ecran_x+510+i, position_ecran_y-32))
    ecran.blit(INTERFACE.subsurface((84, 64, 2, 32)), (position_ecran_x+510, position_ecran_y-32))

    # AFFICHER LE CUBE HP/MANA

    ecran.blit(INTERFACE.subsurface((0, 128, 64, 64)), (position_ecran_x+446, position_ecran_y-64))

    # AFFICHER LE NOMBRE DE VIES

    mot = "Vies:"
    for i in range(len(mot)):
        ecran.blit(pygame.transform.scale(CARACTERES.subsurface(((ord(mot[i]) % 10)*32, (ord(mot[i])//10)*64, 32, 64)),
                                          (30, 60)), (position_ecran_x+(30*i)+2, position_ecran_y+578))
    ecran.blit(INTERFACE.subsurface(((joueur.nombre_de_vies//10)*30, 0, 30, 64)),
               (position_ecran_x+150, position_ecran_y+576))
    ecran.blit(INTERFACE.subsurface(((joueur.nombre_de_vies % 10)*30, 0, 30, 64)),
               (position_ecran_x+180, position_ecran_y+576))

    # AFFICHER LE NOMBRE DE NIVEAUX

    mot = "Niveau:"
    for i in range(len(mot)):
        ecran.blit(pygame.transform.scale(CARACTERES.subsurface(((ord(mot[i]) % 10)*32, (ord(mot[i])//10)*64, 32, 64)),
                                          (30, 60)), (position_ecran_x+(30*i)+688, position_ecran_y+578))
    ecran.blit(INTERFACE.subsurface(((session.niveau//10)*30, 0, 30, 64)),
               (position_ecran_x+898, position_ecran_y+576))
    ecran.blit(INTERFACE.subsurface(((session.niveau % 10)*30, 0, 30, 64)),
               (position_ecran_x+928, position_ecran_y+576))

    # AFFICHER LA BARRE D'EXPERIENCE

    ecran.blit(INTERFACE.subsurface((64, 192, 64, 32)), (position_ecran_x+960, position_ecran_y+288))
    ecran.blit(INTERFACE.subsurface((0, 194, 64, 2)), (position_ecran_x+960, position_ecran_y+574))
    ecran.blit(INTERFACE.subsurface((0, 194, 64, 2)), (position_ecran_x+960, position_ecran_y+320))
    for i in range(252):
        if i < (session.xp*252)//int(100*(1.8**session.niveau)):
            ecran.blit(INTERFACE.subsurface((0, 192, 64, 1)), (position_ecran_x+960, position_ecran_y+573-i))
        else:
            ecran.blit(INTERFACE.subsurface((0, 193, 64, 1)), (position_ecran_x+960, position_ecran_y+573-i))

    pygame.display.flip()

    return 0


def rafraichir_bombes(position_ecran_x, position_ecran_y, joueur, liste_rafraichir, nouvelle_valeur):

    global INTERFACE

    if nouvelle_valeur > 99:
        nouvelle_valeur = 99

    if nouvelle_valeur != joueur.bombes:  # AFFICHER LES UNITES

        liste_rafraichir.append([INTERFACE.subsurface(((nouvelle_valeur % 10)*30, 0, 30, 64)),
                                 (position_ecran_x+114, position_ecran_y-64, 30, 64), 6])
        liste_rafraichir.append([INTERFACE.subsurface((114, 128, 30, 64)),
                                 (position_ecran_x+114, position_ecran_y-64, 30, 64), 5])

        if nouvelle_valeur//10 != joueur.bombes//10:  # AFFICHER LES DIZAINES

            liste_rafraichir.append([INTERFACE.subsurface(((nouvelle_valeur//10)*30, 0, 30, 64)),
                                     (position_ecran_x+84, position_ecran_y-64, 30, 64), 6])
            liste_rafraichir.append([INTERFACE.subsurface((84, 128, 30, 64)),
                                     (position_ecran_x+84, position_ecran_y-64, 30, 64), 5])

        joueur.bombes = nouvelle_valeur

    return liste_rafraichir, joueur


def rafraichir_cles(position_ecran_x, position_ecran_y, joueur, liste_rafraichir, nouvelle_valeur):

    global INTERFACE

    if nouvelle_valeur > 99:
        nouvelle_valeur = 99

    if nouvelle_valeur != joueur.cles:  # AFFICHER LES UNITES

        liste_rafraichir.append([INTERFACE.subsurface(((nouvelle_valeur % 10)*30, 0, 30, 64)),
                                 (position_ecran_x+258, position_ecran_y-64, 30, 64), 6])

        liste_rafraichir.append([INTERFACE.subsurface((66, 128, 30, 64)),
                                 (position_ecran_x+258, position_ecran_y-64, 30, 64), 5])

        if nouvelle_valeur//10 != joueur.cles//10:  # AFFICHER LES DIZAINES

            liste_rafraichir.append([INTERFACE.subsurface(((nouvelle_valeur//10)*30, 0, 30, 64)),
                                     (position_ecran_x+228, position_ecran_y-64, 30, 64), 6])

            liste_rafraichir.append([INTERFACE.subsurface((100, 128, 30, 64)),
                                     (position_ecran_x+228, position_ecran_y-64, 30, 64), 5])

        joueur.cles = nouvelle_valeur

    return liste_rafraichir, joueur


def rafraichir_argent(position_ecran_x, position_ecran_y, joueur, liste_rafraichir, nouvelle_valeur):

    global INTERFACE

    if nouvelle_valeur >= 99:  # FAIRE GAGNER UNE VIE
        nouvelle_valeur -= 99
        liste_rafraichir, joueur = rafraichir_nombre_de_vies(position_ecran_x, position_ecran_y,
                                                             joueur, liste_rafraichir, joueur.nombre_de_vies+1)

    if nouvelle_valeur != joueur.argent:  # AFFICHER LES UNITES

        liste_rafraichir.append([INTERFACE.subsurface(((nouvelle_valeur % 10)*30, 0, 30, 64)),
                                 (position_ecran_x+402, position_ecran_y-64, 30, 64), 6])

        liste_rafraichir.append([INTERFACE.subsurface((82, 128, 30, 64)),
                                 (position_ecran_x+402, position_ecran_y-64, 30, 64), 5])

        if nouvelle_valeur//10 != joueur.argent//10:  # AFFICHER LES DIZAINES

            liste_rafraichir.append([INTERFACE.subsurface(((nouvelle_valeur//10)*30, 0, 30, 64)),
                                     (position_ecran_x+372, position_ecran_y-64, 30, 64), 6])

            liste_rafraichir.append([INTERFACE.subsurface((116, 128, 30, 64)),
                                     (position_ecran_x+372, position_ecran_y-64, 30, 64), 5])

        joueur.argent = nouvelle_valeur

    return liste_rafraichir, joueur


def rafraichir_vie(position_ecran_x, position_ecran_y, joueur, liste_rafraichir, nouvelle_vie, nouvelle_vie_maximum):

    if (not joueur.invincible) or nouvelle_vie > joueur.points_de_vies:

        if nouvelle_vie < 0:
            nouvelle_vie = 0
        if nouvelle_vie > nouvelle_vie_maximum:
            nouvelle_vie = nouvelle_vie_maximum
        if nouvelle_vie < joueur.points_de_vies:
            joueur.invincible = True
            joueur.temps_depuis_invincible = pygame.time.get_ticks()

        # CALCULER LA DIFFERENCE EN PIXELS DE LA BARRE DE VIE AVANT/APRES

        a = (int((joueur.points_de_vies/joueur.vie_maximum)*450))-(int((nouvelle_vie/nouvelle_vie_maximum)*450))

        if a > 0:  # ENLEVER DE LA VIE

            bout_de_barre = pygame.Surface((a, 28))
            bout_de_barre.fill((42, 42, 42))
            liste_rafraichir.append([bout_de_barre,
                                     (position_ecran_x+510+(int((nouvelle_vie/nouvelle_vie_maximum)*450)),
                                      position_ecran_y-62, a, 28), 6])

        if a < 0:  # AJOUTER DE LA VIE

            bout_de_barre = pygame.Surface((-a, 28))
            bout_de_barre.fill((237, 28, 36))
            liste_rafraichir.append([bout_de_barre,
                                     (position_ecran_x+510+(int((joueur.points_de_vies/joueur.vie_maximum)*450)),
                                      position_ecran_y-62, -a, 28), 6])

        joueur.points_de_vies = nouvelle_vie
        joueur.vie_maximum = nouvelle_vie_maximum

    return liste_rafraichir, joueur


def rafraichir_nombre_de_vies(position_ecran_x, position_ecran_y, joueur, liste_rafraichir, nouvelle_valeur):

    global INTERFACE

    if nouvelle_valeur > 99:
        nouvelle_valeur = 99

    if nouvelle_valeur != joueur.nombre_de_vies:  # AFFICHER LES UNITES

        liste_rafraichir.append([INTERFACE.subsurface(((nouvelle_valeur % 10)*30, 0, 30, 64)),
                                 (position_ecran_x+180, position_ecran_y+576, 30, 64), 6])

        liste_rafraichir.append([INTERFACE.subsurface((116, 128, 30, 64)),
                                 (position_ecran_x+180, position_ecran_y+576, 30, 64), 5])

        if nouvelle_valeur//10 != joueur.nombre_de_vies//10:  # AFFICHER LES DIZAINES

            liste_rafraichir.append([INTERFACE.subsurface(((nouvelle_valeur//10)*30, 0, 30, 64)),
                                     (position_ecran_x+150, position_ecran_y+576, 30, 64), 6])

            liste_rafraichir.append([INTERFACE.subsurface((86, 128, 30, 64)),
                                     (position_ecran_x+150, position_ecran_y+576, 30, 64), 5])

        joueur.nombre_de_vies = nouvelle_valeur

    return liste_rafraichir, joueur


def rafraichir_mana(position_ecran_x, position_ecran_y, joueur, liste_rafraichir, session, nouveau_mana):

    mana_max = 100+(20*session.competences[7])

    if nouveau_mana < 0:
        nouveau_mana = 0
    if nouveau_mana > mana_max:
        nouveau_mana = mana_max

    # CALCULER LA DIFFERENCE EN PIXELS DE LA BARRE DE MANA AVANT/APRES

    a = int(joueur.mana*(450/mana_max))-int(nouveau_mana*(450/mana_max))

    if a > 0:  # ENLEVER DU MANA

        bout_de_barre = pygame.Surface((a, 28))
        bout_de_barre.fill((42, 42, 42))
        liste_rafraichir.append([bout_de_barre, (position_ecran_x+510+int(nouveau_mana*(450/mana_max)),
                                                 position_ecran_y-30, a, 28), 6])

    if a < 0:  # AJOUTER DU MANA

        bout_de_barre = pygame.Surface((-a, 28))
        bout_de_barre.fill((63, 72, 204))
        liste_rafraichir.append([bout_de_barre, (position_ecran_x+510+int(joueur.mana*(450/mana_max)),
                                                 position_ecran_y-30, -a, 28), 6])

    joueur.mana = nouveau_mana

    return liste_rafraichir, joueur


def rafraichir_niveau_session(position_ecran_x, position_ecran_y, session, liste_rafraichir):

    global INTERFACE

    # FAIRE MONTER UN OU PLUSIEURS NIVEAU SI BESOIN

    i = 0
    while session.xp >= int(100*(1.8**session.niveau)):
        liste_rafraichir, session = rafraichir_xp(position_ecran_x, position_ecran_y, session, liste_rafraichir,
                                                  session.xp-int(100*(1.8**session.niveau)))
        session.niveau += 1
        session.points_de_competences += 1
        session.points_de_sorts += 1
        i += 1

    if session.niveau > 15:
        session.niveau = 15
        liste_rafraichir, session = rafraichir_xp(position_ecran_x, position_ecran_y, session, liste_rafraichir, 674664)

    if i > 0:  # AFFICHER LES UNITES

        liste_rafraichir.append([INTERFACE.subsurface(((session.niveau % 10)*30, 0, 30, 64)),
                                 (position_ecran_x+928, position_ecran_y+576, 30, 64), 6])

        liste_rafraichir.append([INTERFACE.subsurface((96, 128, 30, 64)),
                                 (position_ecran_x+928, position_ecran_y+576, 30, 64), 5])

        if session.niveau//10 != (session.niveau-i)//10:  # AFFICHER LES DIZAINES

            liste_rafraichir.append([INTERFACE.subsurface(((session.niveau//10)*30, 0, 30, 64)),
                                     (position_ecran_x+898, position_ecran_y+576, 30, 64), 6])

            liste_rafraichir.append([INTERFACE.subsurface((66, 128, 30, 64)),
                                     (position_ecran_x+898, position_ecran_y+576, 30, 64), 5])

    return liste_rafraichir, session


def rafraichir_xp(position_ecran_x, position_ecran_y, session, liste_rafraichir, nouvelle_valeur):

    a = ((session.xp*252)//int(100*(1.8**session.niveau)))-((nouvelle_valeur*252)//int(100*(1.8**session.niveau)))

    if a > 0:

        bout_de_barre = pygame.Surface((60, a))
        bout_de_barre.fill((42, 42, 42))
        liste_rafraichir.append([bout_de_barre,
                                 (position_ecran_x+962,
                                  position_ecran_y+574-((session.xp*252)//int(100*(1.8**session.niveau))),
                                  60, a), 6])

    if a < 0:

        bout_de_barre = pygame.Surface((60, -a))
        bout_de_barre.fill((34, 177, 76))
        liste_rafraichir.append([bout_de_barre,
                                 (position_ecran_x+962,
                                  position_ecran_y+574-((session.xp*252)//int(100*(1.8**session.niveau)))+a,
                                  60, -a), 6])

    session.xp = nouvelle_valeur

    return liste_rafraichir, session


def creer_attaque(joueur, position_ecran_x, position_ecran_y, session):

    global ATTAQUES_JOUEUR

    for i in range(len(joueur.attaques.autorisation)):

        if joueur.attaques.autorisation[i] == 1:

            if pygame.time.get_ticks() >= joueur.attaques.temps_derniere_attaque+joueur.vitesse_attaque:

                try:
                    joueur.attaques.temps_derniere_attaque = pygame.time.get_ticks()

                    entite = Entite_Attaque()
                    entite.x = joueur.x+27
                    entite.y = joueur.y+27
                    entite.type = 1
                    entite.images = [ATTAQUES_JOUEUR.subsurface((0, 0, 20, 20)),
                                     ATTAQUES_JOUEUR.subsurface((20, 0, 40, 40)),
                                     ATTAQUES_JOUEUR.subsurface((320, 0, 96, 96)),
                                     ATTAQUES_JOUEUR.subsurface((416, 0, 96, 96))]
                    entite.detruit = False
                    entite.temps = 0

                    difference_x = joueur.attaques.position_souris[0]-(joueur.x+position_ecran_x+27)
                    difference_y = joueur.attaques.position_souris[1]-(joueur.y+position_ecran_y+27)

                    if difference_x < 0:
                        difference_x_absolue = -difference_x
                    else:
                        difference_x_absolue = difference_x

                    if difference_y < 0:
                        difference_y_absolue = -difference_y
                    else:
                        difference_y_absolue = difference_y

                    if difference_y_absolue > difference_x_absolue:
                        if difference_y < 0:
                            entite.deplacement_y = -15
                            if session.competences[4] == 1:
                                entite.deplacement_y = -18
                            elif session.competences[4] == 2:
                                entite.deplacement_y = -20
                            elif session.competences[4] == 3:
                                entite.deplacement_y = -23
                        else:
                            entite.deplacement_y = 15
                            if session.competences[4] == 1:
                                entite.deplacement_y = 18
                            elif session.competences[4] == 2:
                                entite.deplacement_y = 20
                            elif session.competences[4] == 3:
                                entite.deplacement_y = 23
                        entite.deplacement_x = (entite.deplacement_y*difference_x)/difference_y

                    else:
                        if difference_x < 0:
                            entite.deplacement_x = -15
                            if session.competences[4] == 1:
                                entite.deplacement_x = -18
                            elif session.competences[4] == 2:
                                entite.deplacement_x = -20
                            elif session.competences[4] == 3:
                                entite.deplacement_x = -23
                        else:
                            entite.deplacement_x = 15
                            if session.competences[4] == 1:
                                entite.deplacement_x = 18
                            elif session.competences[4] == 2:
                                entite.deplacement_x = 20
                            elif session.competences[4] == 3:
                                entite.deplacement_x = 23
                        entite.deplacement_y = (entite.deplacement_x*difference_y)/difference_x

                    joueur.attaques.entites.append(entite)

                except ZeroDivisionError:  # SI LE JOUEUR CLIQUE SUR SA POSITION ( AU PIXEL PRES )
                    continue

        if joueur.attaques.autorisation[i] == 2:

            entite = Entite_Attaque()
            entite.x = joueur.x
            entite.y = joueur.y
            entite.type = 2
            entite.images = [ATTAQUES_JOUEUR.subsurface((0, 40, 64, 64)),
                             ATTAQUES_JOUEUR.subsurface((64, 40, 64, 64)),
                             ATTAQUES_JOUEUR.subsurface((128, 40, 192, 192))]
            entite.detruit = False
            entite.temps = 0
            entite.w = 192
            entite.h = 192

            joueur.attaques.entites.append(entite)

            joueur.attaques.autorisation.remove(2)

    return joueur


def gerer_attaques(joueur, position_ecran_x, position_ecran_y, map, liste_rafraichir, session):

    global TILESET

    i = 0

    while i < len(joueur.attaques.entites):

        # ATTAQUES DE BASE

        if joueur.attaques.entites[i].type == 1:

            if not joueur.attaques.entites[i].detruit:  # LORS DU VOYAGE DES ATTAQUES DE BASE

                # EFFACER LE PROJECTILE

                liste_rafraichir.append([map.salles[joueur.salle].image.subsurface(
                    (joueur.attaques.entites[i].x, joueur.attaques.entites[i].y, 20, 20)),
                    (joueur.attaques.entites[i].x+position_ecran_x,
                     joueur.attaques.entites[i].y+position_ecran_y,
                     20, 20), 2])

                # DEPLACER LE PROJECTILE

                collision = 0

                joueur.attaques.entites[i].x += joueur.attaques.entites[i].deplacement_x
                joueur.attaques.entites[i].y += joueur.attaques.entites[i].deplacement_y

                # REGARDER S'IL Y A COLLISION AVEC LE DECORS

                bloc_a_proximite = [int(joueur.attaques.entites[i].y//64), int(joueur.attaques.entites[i].x//64)]
                if 11 >= map.salles[joueur.salle].blocs_type[bloc_a_proximite[0]][bloc_a_proximite[1]] >= 1 or \
                   21 >= map.salles[joueur.salle].blocs_type[bloc_a_proximite[0]][bloc_a_proximite[1]] >= 14:
                    collision = 1

                # REGARDER S'IL Y A COLLISION AVEC UN MONSTRE

                for j in range(len(map.salles[joueur.salle].ennemis)):
                    if collisions(joueur.attaques.entites[i], map.salles[joueur.salle].ennemis[j].hitbox_degats):

                        collision = 1
                        map.salles[joueur.salle].ennemis[j].points_de_vies -= joueur.attaque

                        if session.competences[10] > 0:
                            liste_rafraichir, joueur = rafraichir_vie(position_ecran_x, position_ecran_y, joueur,
                                                                      liste_rafraichir,
                                                                      joueur.points_de_vies+(2*session.competences[10]),
                                                                      joueur.vie_maximum)

                        if map.salles[joueur.salle].ennemis[j].points_de_vies <= 0:
                            map.salles[joueur.salle].ennemis[j].mort = True

                        joueur.attaques.entites[i].x = map.salles[joueur.salle].ennemis[j].x+22
                        joueur.attaques.entites[i].y = map.salles[joueur.salle].ennemis[j].y+22
                        break

                # AFFICHER LE PROJECTILE S'IL N'Y A PAS COLLISION / L'INSCIRE COMME DETRUIT

                if collision == 0:
                    liste_rafraichir.append([joueur.attaques.entites[i].images[0],
                                             (int(joueur.attaques.entites[i].x)+position_ecran_x,
                                              int(joueur.attaques.entites[i].y)+position_ecran_y,
                                              20, 20), 2])

                if collision == 1:
                    joueur.attaques.entites[i].detruit = True
                    joueur.attaques.entites[i].temps = 0

                i += 1

            else:  # LORS DE LA DESTRUCTION DES ATTAQUES DE BASE

                joueur.attaques.entites[i].temps += 1

                # AVEC LES PROJECTILS EXPLOSIFS

                if session.competences[8] > 0:

                    if joueur.attaques.entites[i].temps == 1:  # AJUSTER LA POSITION

                        joueur.attaques.entites[i].x -= 38
                        joueur.attaques.entites[i].y -= 38
                        if joueur.attaques.entites[i].deplacement_x <= 0:
                            joueur.attaques.entites[i].x -= 48
                        if joueur.attaques.entites[i].deplacement_y <= 0:
                            joueur.attaques.entites[i].y -= 48

                        if joueur.attaques.entites[i].x < 0:
                            joueur.attaques.entites[i].x = 0
                        if joueur.attaques.entites[i].y < 0:
                            joueur.attaques.entites[i].y = 0
                        if joueur.attaques.entites[i].x > 864:
                            joueur.attaques.entites[i].x = 864
                        if joueur.attaques.entites[i].y > 480:
                            joueur.attaques.entites[i].y = 480

                    if joueur.attaques.entites[i].temps < 7:  # AFFICHER LE DEBUT D'EXPLOSION
                        liste_rafraichir.append([joueur.attaques.entites[i].images[2],
                                                 (int(joueur.attaques.entites[i].x)+position_ecran_x,
                                                  int(joueur.attaques.entites[i].y)+position_ecran_y,
                                                  96, 96), 2])
                        i += 1

                    elif joueur.attaques.entites[i].temps == 7:  # EFFACER LE DEBUT D'EXPLOSION ET INFLIGER LES DEGATS
                        liste_rafraichir.append([map.salles[joueur.salle].image.subsurface(
                            (joueur.attaques.entites[i].x, joueur.attaques.entites[i].y, 96, 96)),
                            (int(joueur.attaques.entites[i].x)+position_ecran_x,
                             int(joueur.attaques.entites[i].y)+position_ecran_y,
                             96, 96), 2])

                        for ennemi in map.salles[joueur.salle].ennemis:
                            if (((ennemi.x+32)-(joueur.attaques.entites[i].x+48))**2)+(((ennemi.y+32)-(joueur.attaques.entites[i].y+48))**2) <= 4096:
                                ennemi.points_de_vies -= 50*session.competences[8]
                                if ennemi.points_de_vies <= 0:
                                    ennemi.mort = True

                    elif 6 < joueur.attaques.entites[i].temps < 24:  # AFFICHER LA GROSSE EXPLOSION
                        liste_rafraichir.append([joueur.attaques.entites[i].images[3],
                                                 (int(joueur.attaques.entites[i].x)+position_ecran_x,
                                                  int(joueur.attaques.entites[i].y)+position_ecran_y,
                                                  96, 96), 2])
                        i += 1

                    elif joueur.attaques.entites[i].temps == 24:  # EFFACER DEFINITIVEMENT L'ATTAQUE
                        liste_rafraichir.append([map.salles[joueur.salle].image.subsurface(
                            (joueur.attaques.entites[i].x, joueur.attaques.entites[i].y, 96, 96)),
                            (int(joueur.attaques.entites[i].x)+position_ecran_x,
                             int(joueur.attaques.entites[i].y)+position_ecran_y,
                             96, 96), 2])

                        del joueur.attaques.entites[i]

                # SANS LES PROJECTILS EXPLOSIFS

                if session.competences[8] == 0:

                    if joueur.attaques.entites[i].temps == 1:  # AJUSTER LA POSITION

                        joueur.attaques.entites[i].x -= 10
                        joueur.attaques.entites[i].y -= 10
                        if joueur.attaques.entites[i].deplacement_x <= 0:
                            joueur.attaques.entites[i].x -= 20
                        if joueur.attaques.entites[i].deplacement_y <= 0:
                            joueur.attaques.entites[i].y -= 20

                        if joueur.attaques.entites[i].x < 0:
                            joueur.attaques.entites[i].x = 0
                        if joueur.attaques.entites[i].y < 0:
                            joueur.attaques.entites[i].y = 0
                        if joueur.attaques.entites[i].x > 920:
                            joueur.attaques.entites[i].x = 920
                        if joueur.attaques.entites[i].y > 536:
                            joueur.attaques.entites[i].y = 536

                    if joueur.attaques.entites[i].temps < 24:  # AFFICHER L'IMPACT
                        liste_rafraichir.append([joueur.attaques.entites[i].images[1],
                                                 (int(joueur.attaques.entites[i].x)+position_ecran_x,
                                                  int(joueur.attaques.entites[i].y)+position_ecran_y,
                                                  40, 40), 2])
                        i += 1

                    elif joueur.attaques.entites[i].temps == 24:  # EFFACER DEFINITIVEMENT L'ATTAQUE
                        liste_rafraichir.append([map.salles[joueur.salle].image.subsurface(
                            (joueur.attaques.entites[i].x, joueur.attaques.entites[i].y, 40, 40)),
                            (int(joueur.attaques.entites[i].x)+position_ecran_x,
                             int(joueur.attaques.entites[i].y)+position_ecran_y,
                             40, 40), 2])

                        del joueur.attaques.entites[i]

        # BOMBES

        elif joueur.attaques.entites[i].type == 2:

            if not joueur.attaques.entites[i].detruit:  # LORSQU'ELLE CLIGNOTE

                joueur.attaques.entites[i].temps += 1
                liste_rafraichir.append([map.salles[joueur.salle].image.subsurface(
                    (joueur.attaques.entites[i].x, joueur.attaques.entites[i].y, 64, 64)),
                    (position_ecran_x+joueur.attaques.entites[i].x,
                     position_ecran_y+joueur.attaques.entites[i].y,
                     64, 64), 2])

                if joueur.attaques.entites[i].temps == 144:
                    joueur.attaques.entites[i].detruit = True
                    joueur.attaques.entites[i].temps = 0

                if joueur.attaques.entites[i].temps % 16 < 8:
                    liste_rafraichir.append([joueur.attaques.entites[i].images[0],
                                             (position_ecran_x+joueur.attaques.entites[i].x,
                                              position_ecran_y+joueur.attaques.entites[i].y,
                                              64, 64), 2])
                else:
                    liste_rafraichir.append([joueur.attaques.entites[i].images[1],
                                             (position_ecran_x+joueur.attaques.entites[i].x,
                                              position_ecran_y+joueur.attaques.entites[i].y,
                                              64, 64), 2])

                i += 1

            else:  # LORSQU'ELLE EXPLOSE

                joueur.attaques.entites[i].temps += 1

                if joueur.attaques.entites[i].temps == 1:

                    joueur.attaques.entites[i].x -= 64
                    joueur.attaques.entites[i].y -= 64

                    if joueur.attaques.entites[i].x < 0:
                        joueur.attaques.entites[i].x = 0
                    elif joueur.attaques.entites[i].x > 768:
                        joueur.attaques.entites[i].x = 768
                    if joueur.attaques.entites[i].y < 0:
                        joueur.attaques.entites[i].y = 0
                    elif joueur.attaques.entites[i].y > 384:
                        joueur.attaques.entites[i] = 384

                    for ennemi in map.salles[joueur.salle].ennemis:  # SI LA BOMBE TOUCHE DES ENNEMIS
                        if collisions(joueur.attaques.entites[i], ennemi.hitbox_degats):
                            ennemi.points_de_vies -= 2*joueur.attaque

                    if collisions(joueur.hitbox, joueur.attaques.entites[i]):  # SI LA BOMBE TOUCHE LE JOUEUR
                        liste_rafraichir, joueur = \
                            rafraichir_vie(position_ecran_x, position_ecran_y, joueur, liste_rafraichir,
                                           joueur.points_de_vies-2*joueur.attaque, joueur.vie_maximum)

                    # DETRUIRE LES BLOCS A PROXIMITE

                    blocs_a_proximite = list([[(joueur.attaques.entites[i].x+32)//64,
                                          (joueur.attaques.entites[i].y+32)//64]])
                    blocs_a_proximite.append([blocs_a_proximite[0][0]+1, blocs_a_proximite[0][1]])
                    blocs_a_proximite.append([blocs_a_proximite[0][0]+2, blocs_a_proximite[0][1]])
                    blocs_a_proximite.append([blocs_a_proximite[0][0], blocs_a_proximite[0][1]+1])
                    blocs_a_proximite.append([blocs_a_proximite[0][0]+1, blocs_a_proximite[0][1]+1])
                    blocs_a_proximite.append([blocs_a_proximite[0][0]+2, blocs_a_proximite[0][1]+1])
                    blocs_a_proximite.append([blocs_a_proximite[0][0]+1, blocs_a_proximite[0][1]+2])
                    blocs_a_proximite.append([blocs_a_proximite[0][0]+2, blocs_a_proximite[0][1]+2])
                    blocs_a_proximite.append([blocs_a_proximite[0][0], blocs_a_proximite[0][1]+2])

                    for j in range(len(blocs_a_proximite)):
                        if map.salles[joueur.salle].blocs_type[blocs_a_proximite[j][1]][blocs_a_proximite[j][0]] == 1:
                            map.salles[joueur.salle].blocs_type[blocs_a_proximite[j][1]][blocs_a_proximite[j][0]] = 0
                            map.salles[joueur.salle].image.blit(
                                TILESET.subsurface((0, 0, 64, 64)),
                                (blocs_a_proximite[j][0]*64, blocs_a_proximite[j][1]*64))
                            liste_rafraichir.append([map.salles[joueur.salle].image.subsurface(
                                (blocs_a_proximite[j][0]*64, blocs_a_proximite[j][1]*64, 64, 64)),
                                ((blocs_a_proximite[j][0]*64)+position_ecran_x,
                                 (blocs_a_proximite[j][1]*64)+position_ecran_y,
                                 64, 64), 0])

                if joueur.attaques.entites[i].temps == 24:  # DETRUIRE DEFINITIVEMENT LA BOMBE
                    liste_rafraichir.append([map.salles[joueur.salle].image.subsurface(
                        (joueur.attaques.entites[i].x, joueur.attaques.entites[i].y, 192, 192)),
                        (position_ecran_x+joueur.attaques.entites[i].x, position_ecran_y+joueur.attaques.entites[i].y,
                         192, 192), 2])
                    del joueur.attaques.entites[i]
                    i -= 1
                else:  # AFFICHER LA FUMEE
                    liste_rafraichir.append([joueur.attaques.entites[i].images[2],
                                             (position_ecran_x+joueur.attaques.entites[i].x,
                                              position_ecran_y+joueur.attaques.entites[i].y,
                                              192, 192), 2])

                i += 1

    return joueur, map, liste_rafraichir


def deplacer_monstres(map, joueur, tempo, liste_rafraichir, position_ecran_x, position_ecran_y, session):

    for i in range(len(map.salles[joueur.salle].ennemis)):

        if not map.salles[joueur.salle].ennemis[i].mort:  # LA MORT DES MONSTRES EST GEREE DANS UNE AUTRE FONCTION

            # MONSTRES DE BASE

            if map.salles[joueur.salle].ennemis[i].type == 0:

                # EFFACER LE MONSTRE

                liste_rafraichir.append([map.salles[joueur.salle].image.subsurface(
                    (map.salles[joueur.salle].ennemis[i].x, map.salles[joueur.salle].ennemis[i].y, 64, 64)),
                    (map.salles[joueur.salle].ennemis[i].x+position_ecran_x,
                     map.salles[joueur.salle].ennemis[i].y+position_ecran_y,
                     64, 64), 0])

                # CALCULER LA TRAJECTOIRE DU MONSTRE

                if map.salles[joueur.salle].ennemis[i].x < joueur.x:
                    map.salles[joueur.salle].ennemis[i].deplacement_x = 2
                    if map.salles[joueur.salle].ennemis[i].x+1 == joueur.x:
                        map.salles[joueur.salle].ennemis[i].deplacement_x = 1

                elif map.salles[joueur.salle].ennemis[i].x > joueur.x:
                    map.salles[joueur.salle].ennemis[i].deplacement_x = -2
                    if map.salles[joueur.salle].ennemis[i].x-1 == joueur.x:
                        map.salles[joueur.salle].ennemis[i].deplacement_x = -1

                else:
                    map.salles[joueur.salle].ennemis[i].deplacement_x = 0

                if map.salles[joueur.salle].ennemis[i].y < joueur.y:
                    map.salles[joueur.salle].ennemis[i].deplacement_y = 2
                    if map.salles[joueur.salle].ennemis[i].y+1 == joueur.y:
                        map.salles[joueur.salle].ennemis[i].deplacement_y = 1

                elif map.salles[joueur.salle].ennemis[i].y > joueur.y:
                    map.salles[joueur.salle].ennemis[i].deplacement_y = -2
                    if map.salles[joueur.salle].ennemis[i].y-1 == joueur.y:
                        map.salles[joueur.salle].ennemis[i].deplacement_y = -1

                else:
                    map.salles[joueur.salle].ennemis[i].deplacement_y = 0

                # DEPLACER LE MONSTRE SUR L'AXE DES X

                if map.salles[joueur.salle].ennemis[i].deplacement_x != 0:

                    map.salles[joueur.salle].ennemis[i].x += map.salles[joueur.salle].ennemis[i].deplacement_x
                    map.salles[joueur.salle].ennemis[i].hitbox_degats.x = map.salles[joueur.salle].ennemis[i].x
                    map.salles[joueur.salle].ennemis[i].hitbox_deplacement.x = map.salles[joueur.salle].ennemis[i].x+16

                    blocs_a_proximite = list([[map.salles[joueur.salle].ennemis[i].x//64,
                                               map.salles[joueur.salle].ennemis[i].y//64]])
                    blocs_a_proximite.append([blocs_a_proximite[0][0]+1, blocs_a_proximite[0][1]])
                    blocs_a_proximite.append([blocs_a_proximite[0][0], blocs_a_proximite[0][1]+1])
                    blocs_a_proximite.append([blocs_a_proximite[0][0]+1, blocs_a_proximite[0][1]+1])

                    for bloc in blocs_a_proximite:

                        while collisions(map.salles[joueur.salle].ennemis[i].hitbox_deplacement,
                                         map.salles[joueur.salle].blocs_hitboxs[bloc[1]][bloc[0]]) and \
                                (11 >= map.salles[joueur.salle].blocs_type[bloc[1]][bloc[0]] >= 1 or
                                 21 >= map.salles[joueur.salle].blocs_type[bloc[1]][bloc[0]] >= 14):

                            map.salles[joueur.salle].ennemis[i].hitbox_degats.x = map.salles[joueur.salle].ennemis[i].x
                            map.salles[joueur.salle].ennemis[i].hitbox_deplacement.x = map.salles[joueur.salle].ennemis[i].x+16

                            if map.salles[joueur.salle].ennemis[i].deplacement_x > 0:
                                map.salles[joueur.salle].ennemis[i].x -= 1
                            else:
                                map.salles[joueur.salle].ennemis[i].x += 1

                            if map.salles[joueur.salle].ennemis[i].x//64 != blocs_a_proximite[0][0]:
                                blocs_a_proximite[0][0] = map.salles[joueur.salle].ennemis[i].x//64
                                blocs_a_proximite[1][0] = blocs_a_proximite[0][0]+1
                                blocs_a_proximite[2][0] = blocs_a_proximite[0][0]
                                blocs_a_proximite[3][0] = blocs_a_proximite[0][0]+1

                # DEPLACER LE MONSTRE SUR L'AXE DES Y

                if map.salles[joueur.salle].ennemis[i].deplacement_y != 0:

                    map.salles[joueur.salle].ennemis[i].y += map.salles[joueur.salle].ennemis[i].deplacement_y
                    map.salles[joueur.salle].ennemis[i].hitbox_degats.y = map.salles[joueur.salle].ennemis[i].y
                    map.salles[joueur.salle].ennemis[i].hitbox_deplacement.y = map.salles[joueur.salle].ennemis[i].y+16

                    blocs_a_proximite = list([[map.salles[joueur.salle].ennemis[i].x//64,
                                               map.salles[joueur.salle].ennemis[i].y//64]])
                    blocs_a_proximite.append([blocs_a_proximite[0][0]+1, blocs_a_proximite[0][1]])
                    blocs_a_proximite.append([blocs_a_proximite[0][0], blocs_a_proximite[0][1]+1])
                    blocs_a_proximite.append([blocs_a_proximite[0][0]+1, blocs_a_proximite[0][1]+1])

                    for bloc in blocs_a_proximite:

                        while collisions(map.salles[joueur.salle].ennemis[i].hitbox_deplacement,
                                         map.salles[joueur.salle].blocs_hitboxs[bloc[1]][bloc[0]]) and \
                                (11 >= map.salles[joueur.salle].blocs_type[bloc[1]][bloc[0]] >= 1 or
                                 21 >= map.salles[joueur.salle].blocs_type[bloc[1]][bloc[0]] >= 14):

                            map.salles[joueur.salle].ennemis[i].hitbox_degats.y = map.salles[joueur.salle].ennemis[i].y
                            map.salles[joueur.salle].ennemis[i].hitbox_deplacement.y = map.salles[joueur.salle].ennemis[i].y+16

                            if map.salles[joueur.salle].ennemis[i].deplacement_y > 0:
                                map.salles[joueur.salle].ennemis[i].y -= 1
                            else:
                                map.salles[joueur.salle].ennemis[i].y += 1

                            if map.salles[joueur.salle].ennemis[i].y//64 != blocs_a_proximite[0][1]:
                                blocs_a_proximite[0][1] = map.salles[joueur.salle].ennemis[i].y//64
                                blocs_a_proximite[1][1] = blocs_a_proximite[0][1]
                                blocs_a_proximite[2][1] = blocs_a_proximite[0][1]+1
                                blocs_a_proximite[3][1] = blocs_a_proximite[2][1]

                # GERER LA PERTE DE PV DU JOUEUR / LA POSSIBILITE QU'IL ESQUIVE AVEC LA COMPETENCE APPROPRIEE

                if collisions(map.salles[joueur.salle].ennemis[i].hitbox_degats, joueur.hitbox):
                    if randrange(100) > (15*session.competences[9]):
                        liste_rafraichir, joueur = \
                            rafraichir_vie(position_ecran_x, position_ecran_y, joueur, liste_rafraichir,
                                           joueur.points_de_vies-map.salles[joueur.salle].ennemis[i].attaque,
                                           joueur.vie_maximum)
                    else:
                        if not joueur.invincible:
                            joueur.invincible = True
                            joueur.temps_depuis_invincible = pygame.time.get_ticks()

                # AFFICHER LE MONSTRE APRES DEPLACEMENT

                if map.salles[joueur.salle].ennemis[i].deplacement_x > 0 and \
                   map.salles[joueur.salle].ennemis[i].deplacement_y == 0:
                    liste_rafraichir.append([map.salles[joueur.salle].ennemis[i].images.droite[tempo//8],
                                             (map.salles[joueur.salle].ennemis[i].x+position_ecran_x,
                                              map.salles[joueur.salle].ennemis[i].y+position_ecran_y,
                                              64, 64), 4])
                if map.salles[joueur.salle].ennemis[i].deplacement_x < 0 and \
                   map.salles[joueur.salle].ennemis[i].deplacement_y == 0:
                    liste_rafraichir.append([map.salles[joueur.salle].ennemis[i].images.gauche[tempo//8],
                                             (map.salles[joueur.salle].ennemis[i].x+position_ecran_x,
                                              map.salles[joueur.salle].ennemis[i].y+position_ecran_y,
                                              64, 64), 4])
                if map.salles[joueur.salle].ennemis[i].deplacement_y > 0:
                    liste_rafraichir.append([map.salles[joueur.salle].ennemis[i].images.bas[tempo//8],
                                             (map.salles[joueur.salle].ennemis[i].x+position_ecran_x,
                                              map.salles[joueur.salle].ennemis[i].y+position_ecran_y,
                                              64, 64), 4])
                if map.salles[joueur.salle].ennemis[i].deplacement_y < 0:
                    liste_rafraichir.append([map.salles[joueur.salle].ennemis[i].images.haut[tempo//8],
                                             (map.salles[joueur.salle].ennemis[i].x+position_ecran_x,
                                              map.salles[joueur.salle].ennemis[i].y+position_ecran_y,
                                              64, 64), 4])
                if map.salles[joueur.salle].ennemis[i].deplacement_x == 0 and \
                   map.salles[joueur.salle].ennemis[i].deplacement_y == 0:
                    liste_rafraichir.append([map.salles[joueur.salle].ennemis[i].images.bas[0],
                                             (map.salles[joueur.salle].ennemis[i].x+position_ecran_x,
                                              map.salles[joueur.salle].ennemis[i].y+position_ecran_y,
                                              64, 64), 4])

    return map, liste_rafraichir, joueur


def gerer_mort_monstres(map, joueur, liste_rafraichir, position_ecran_x, position_ecran_y, session):

    global OBJETS

    i = 0
    while i < len(map.salles[joueur.salle].ennemis):

        if map.salles[joueur.salle].ennemis[i].mort:

            if map.salles[joueur.salle].ennemis[i].type == 0:  # MORT DES MONSTRES DE BASE

                # EFFACER MONSTRE

                liste_rafraichir.append([map.salles[joueur.salle].image.subsurface(
                    (map.salles[joueur.salle].ennemis[i].x, map.salles[joueur.salle].ennemis[i].y, 64, 64)),
                    (map.salles[joueur.salle].ennemis[i].x+position_ecran_x,
                     map.salles[joueur.salle].ennemis[i].y+position_ecran_y,
                     64, 64), 0])

                # EFFACER BARRE DE VIE DU MONSTRE

                liste_rafraichir.append([map.salles[joueur.salle].image.subsurface(
                    (map.salles[joueur.salle].ennemis[i].minibarre.x,
                     map.salles[joueur.salle].ennemis[i].minibarre.y, 64, 8)),
                    (position_ecran_x+map.salles[joueur.salle].ennemis[i].minibarre.x,
                     position_ecran_y+map.salles[joueur.salle].ennemis[i].minibarre.y, 64, 8), 1])

                # OBTENIR UN COEUR

                if randrange(5) < 1+session.competences[6]:
                    objet = Objet()
                    objet.x = map.salles[joueur.salle].ennemis[i].x
                    objet.y = map.salles[joueur.salle].ennemis[i].y
                    objet.type = 7
                    objet.image = OBJETS.subsurface((448, 0, 64, 64))
                    objet.hitbox.x = map.salles[joueur.salle].ennemis[i].x
                    objet.hitbox.y = map.salles[joueur.salle].ennemis[i].y
                    objet.hitbox.w = 64
                    objet.hitbox.h = 64
                    map.salles[joueur.salle].objets.append(objet)

                # OBTENIR EXPERIENCE

                liste_rafraichir, session = \
                    rafraichir_xp(position_ecran_x, position_ecran_y, session, liste_rafraichir, session.xp+10)

                # RECUPERER MANA

                liste_rafraichir, joueur = \
                    rafraichir_mana(position_ecran_x, position_ecran_y, joueur, liste_rafraichir,
                                    session, joueur.mana+10+(5*session.competences[3]))

                del map.salles[joueur.salle].ennemis[i]
                i -= 1

        i += 1

    return map, liste_rafraichir, session


def gerer_invincibilite(joueur):

    if joueur.invincible:

        # METTRE LE PERSONNAGE EN TRANSPARENCE

        if pygame.time.get_ticks() < (joueur.temps_depuis_invincible+joueur.temps_invincibilite) and \
           joueur.images.bas[0].get_alpha() is None:

            for i in range(6):
                joueur.images.bas[i].set_alpha(150)
                joueur.images.haut[i].set_alpha(150)
                joueur.images.droite[i].set_alpha(150)
                joueur.images.gauche[i].set_alpha(150)

        # REMETTRE LE PERSONNAGE OPAQUE

        if pygame.time.get_ticks() > (joueur.temps_depuis_invincible+joueur.temps_invincibilite):

            for i in range(6):
                joueur.images.bas[i].set_alpha()
                joueur.images.haut[i].set_alpha()
                joueur.images.droite[i].set_alpha()
                joueur.images.gauche[i].set_alpha()

            joueur.invincible = False

    return joueur


def charger_minimap(map, joueur):

    # CREER L'IMAGE DE LA MINIMAP

    global MINIMAP

    minimap = pygame.Surface((128, 88))
    minimap.fill((255, 255, 255))
    minimap.set_colorkey((255, 255, 255))
    minimap.blit(MINIMAP.subsurface((0, 0, 128, 88)), (0, 0))

    for y in range(5):
        for x in range(5):
            for salle in map.salles:
                if salle.x == map.salles[joueur.salle].x+(x-2) and salle.y == map.salles[joueur.salle].y+(y-2):
                    if salle.visited:
                        if salle.type_salle == 1 or \
                           salle.type_salle == 2:
                            if salle.objets == list():
                                minimap.blit(MINIMAP.subsurface((0, 88, 24, 16)), ((x*24)+x+2, (y*16)+y+2))
                            else:
                                minimap.blit(MINIMAP.subsurface((96, 88, 24, 16)), ((x*24)+x+2, (y*16)+y+2))
                        if salle.type_salle == 3:
                            minimap.blit(MINIMAP.subsurface((24, 88, 24, 16)), ((x*24)+x+2, (y*16)+y+2))
                        if salle.type_salle == 4:
                            minimap.blit(MINIMAP.subsurface((48, 88, 24, 16)), ((x*24)+x+2, (y*16)+y+2))
                        if salle.type_salle == 5:
                            minimap.blit(MINIMAP.subsurface((72, 88, 24, 16)), ((x*24)+x+2, (y*16)+y+2))
                    if not salle.visited:
                        if salle.type_salle != 5:
                            minimap.blit(MINIMAP.subsurface((0, 104, 24, 16)), ((x*24)+x+2, (y*16)+y+2))
                        if salle.type_salle == 5:
                            minimap.blit(MINIMAP.subsurface((24, 104, 24, 16)), ((x*24)+x+2, (y*16)+y+2))

    minimap.blit(MINIMAP.subsurface((0, 120, 24, 16)), (52, 36))
    minimap.set_alpha(215)

    return minimap


def creer_images_et_positions_menu(menu):

    global CARACTERES
    global CARACTERES_SELECTIONNES

    if menu.type == 1:  # CREER DES MENUS VERTICAUX

        nombre_de_lignes = 0
        ligne_actuelle = 0

        for i in range(len(menu.options)):

            # DECOUPER LES MESSAGES DE L'OPTION EN CHAINES SI BESOIN ET LEVER DES EXCEPTIONS S'IL Y A TROP DE TEXTE

            if len(menu.options[i].message)*32 < menu.w:
                menu.options[i].chaines = [menu.options[i].message]
            else:
                menu.options[i].chaines = menu.options[i].message.split(" ")

                for mot in menu.options[i].chaines:
                    if len(mot)*32 > menu.w:
                        raise ValueError("Les mots sont trop longs")

            nombre_de_lignes += len(menu.options[i].chaines)
            if nombre_de_lignes*65 > menu.h:
                raise ValueError("Les options sont trop epaisses / trop nombreuses")

            # CALCULER LES COORDONNEES DE L'OPTION

            plus_longue_chaine_option = 0

            for j in range(len(menu.options[i].chaines)):
                if len(menu.options[i].chaines[j]) > plus_longue_chaine_option:
                    plus_longue_chaine_option = len(menu.options[i].chaines[j])

            menu.options[i].w = 32*plus_longue_chaine_option
            menu.options[i].x = menu.x+((menu.w//2)-(menu.options[i].w//2))

            # CREER L'IMAGE DE L'OPTION

        for i in range(len(menu.options)):

            menu.options[i].h = 64*len(menu.options[i].chaines)
            menu.options[i].y = menu.y+ligne_actuelle*64+((menu.h-nombre_de_lignes*64)//(len(menu.options)+1))*(i+1)
            ligne_actuelle += len(menu.options[i].chaines)

            menu.options[i].images = list()
            menu.options[i].images.append(pygame.Surface((menu.options[i].w, menu.options[i].h)))
            menu.options[i].images[0].fill((255, 255, 255))
            menu.options[i].images[0].set_colorkey((255, 255, 255))
            menu.options[i].images.append(pygame.Surface((menu.options[i].w, menu.options[i].h)))
            menu.options[i].images[1].fill((255, 255, 255))
            menu.options[i].images[1].set_colorkey((255, 255, 255))

            for j in range(len(menu.options[i].chaines)):
                for k in range(len(menu.options[i].chaines[j])):
                    menu.options[i].images[0].blit(CARACTERES.subsurface(
                        ((ord(menu.options[i].chaines[j][k]) % 10)*32,
                         (ord(menu.options[i].chaines[j][k])//10)*64, 32, 64)),
                        (((menu.options[i].w-(len(menu.options[i].chaines[j])*32))//2)+(k*32), j*64))

                    menu.options[i].images[1].blit(CARACTERES_SELECTIONNES.subsurface(
                        ((ord(menu.options[i].chaines[j][k]) % 10)*32,
                         (ord(menu.options[i].chaines[j][k])//10)*64, 32, 64)),
                        (k*32, j*64))

    elif menu.type == 2:  # CREER DES MENUS HORIZONTAUX

        # LEVER DES EXCEPTIONS S'IL Y A TROP DE TEXTE

        nombre_de_caracteres = 0
        for option in menu.options:
            nombre_de_caracteres += len(option.message)

        if nombre_de_caracteres*32 > menu.w:
            raise ValueError("Le nombre d'options / La taille des mots est/sont trop élevé(es).")
        if menu.h < 64:
            raise ValueError("Le menu n'est pas assez épais. (<64px)")

        # CREER LES OPTIONS

        nombre_de_caracteres_actuel = 0
        for i in range(len(menu.options)):

            # CALCULER LES COORDONEES DE L'OPTION

            menu.options[i].y = menu.y+((menu.h-64)//2)
            menu.options[i].x = menu.x+(nombre_de_caracteres_actuel*32)+((i+1)*((menu.w-nombre_de_caracteres*32)//(len(menu.options)+1)))
            menu.options[i].h = 64
            menu.options[i].w = len(menu.options[i].message)*32

            # CREER L'IMAGE DE L'OPTION

            menu.options[i].images = list()
            for j in range(2):
                menu.options[i].images.append(pygame.Surface((menu.options[i].w, menu.options[i].h)))
                menu.options[i].images[j].fill((255, 255, 255))
                menu.options[i].images[j].set_colorkey((255, 255, 255))

            for j in range(len(menu.options[i].message)):
                menu.options[i].images[0].blit(CARACTERES.subsurface(
                    ((ord(menu.options[i].message[j]) % 10)*32, (ord(menu.options[i].message[j])//10)*64, 32, 64)),
                    (j*32, 0))
                menu.options[i].images[1].blit(CARACTERES_SELECTIONNES.subsurface(
                    ((ord(menu.options[i].message[j]) % 10)*32, (ord(menu.options[i].message[j])//10)*64, 32, 64)),
                    (j*32, 0))

            nombre_de_caracteres_actuel += len(menu.options[i].message)

    return menu


def obtenir_choix_menu_et_afficher_selection(menu, position_souris, liste_rafraichir):

    choix = 0

    # OBTENIR LE CHOIX A PARTIR DES ENTREES UTILISATEUR S'IL Y EN A

    for entree in pygame.event.get():
        if entree.type == pygame.MOUSEBUTTONUP:
            if entree.button == 1:
                for i in range(len(menu.options)):
                    if menu.options[i].x+menu.options[i].w > entree.pos[0] > menu.options[i].x and \
                       menu.options[i].y+menu.options[i].h > entree.pos[1] > menu.options[i].y:
                        choix = i+1
        if entree.type == pygame.MOUSEMOTION:
            position_souris = [entree.pos[0],entree.pos[1]]

    # AFFICHER LE MENU

    for i in range(len(menu.options)):
        if menu.options[i].x+menu.options[i].w > position_souris[0] > menu.options[i].x and \
           menu.options[i].y+menu.options[i].h > position_souris[1] > menu.options[i].y:
            liste_rafraichir.append([menu.options[i].images[1],
                                     (menu.options[i].x, menu.options[i].y, menu.options[i].w, menu.options[i].h), 7])
        else:
            liste_rafraichir.append([menu.options[i].images[0],
                                     (menu.options[i].x, menu.options[i].y, menu.options[i].w, menu.options[i].h), 7])

    return liste_rafraichir, choix, position_souris


def creer_session(ecran, resolution, liste_rafraichir, liste_messages):

    global FOND
    global CARACTERES

    global VERSION

    # ACTIVER LA REPETITION DES TOUCHES

    pygame.key.set_repeat(150,100)

    # CREER UNE SESSION VIDE

    session = Session()
    session.competences = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    session.points_de_competences = 0
    session.sorts = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    session.points_de_sorts = 0
    session.niveau = 0
    session.xp = 0
    session.partie = False
    session.map = None
    session.joueur = None
    session.version = VERSION
    session.nom = str()

    # CREER LE MENU

    menu = Menu()
    menu.x = 0
    menu.y = resolution.current_h-300
    menu.w = resolution.current_w
    menu.h = 300
    for i in range(4):
        menu.options.append(Options_Menu())
    menu.options[0].message = "Valider"
    menu.options[1].message = "Retour"
    menu.type = 1
    menu = creer_images_et_positions_menu(menu)

    # INITIALISER QUELQUES VARIABLES

    tempo = 0
    nom_fini = False
    position_souris = [0, 0]
    image_message = pygame.Surface((resolution.current_w, 64))

    temps_actuel = pygame.time.get_ticks()

    # BOUCLE DE DEMANDE DE NOM DE SESSION

    while not nom_fini:

        # RAFRAICHIR IMAGE

        liste_messages, liste_rafraichir = afficher_messages(liste_messages, liste_rafraichir, resolution)
        liste_rafraichir, temps_actuel, tempo = gerer_temps(ecran, tempo, liste_rafraichir, temps_actuel)

        # GERER ENTREES UTILISATEUR

        choix = 0

        for entree in pygame.event.get():
            if entree.type == pygame.KEYDOWN:
                if entree.unicode != str():
                    if 122 >= ord(entree.unicode) >= 97 or \
                       90 >= ord(entree.unicode) >= 65:  # AJOUTER DES LETTRES
                        session.nom += entree.unicode
                if entree.key == pygame.K_BACKSPACE:  # EFFACER UNE LETTRE
                    if session.nom != "":
                        session.nom = session.nom[:-1]
                if entree.key == pygame.K_RETURN:  # VALIDER
                    choix = 1

            elif entree.type == pygame.MOUSEBUTTONUP:  # OBTENIR LE CHOIX
                if entree.button == 1:
                    for i in range(len(menu.options)):
                        if menu.options[i].x+menu.options[i].w > entree.pos[0] > menu.options[i].x and \
                           menu.options[i].y+menu.options[i].h > entree.pos[1] > menu.options[i].y:
                            choix = i+1

            elif entree.type == pygame.MOUSEMOTION:
                position_souris = [entree.pos[0], entree.pos[1]]

        # AFFICHER LE NOM INCOMPLET

        if len(session.nom) > 15:
            session.nom = session.nom[:15]

        chaine = "Pseudo:"+session.nom

        if 250 > pygame.time.get_ticks() % 500 > 0:  # AJOUTER UN CURSEUR CLIGNOTANT
            chaine += "_"
        else:
            chaine += " "

        image_message.blit(FOND.subsurface((0, (resolution.current_h-64)//2, resolution.current_w, 64)), (0, 0))

        for i in range(len(chaine)):
            image_message.blit(CARACTERES.subsurface(((ord(chaine[i]) % 10)*32, (ord(chaine[i])//10)*64, 32, 64)),
                               (32*i+((resolution.current_w-256-(len(session.nom)*32))//2), 0))

        liste_rafraichir.append([image_message, (0, (resolution.current_h-64)//2, resolution.current_w, 64), 7])

        # AFFICHER LE MENU

        for i in range(len(menu.options)):
            if menu.options[i].x+menu.options[i].w > position_souris[0] > menu.options[i].x and \
               menu.options[i].y+menu.options[i].h > position_souris[1] > menu.options[i].y:
                liste_rafraichir.append([menu.options[i].images[1], (menu.options[i].x, menu.options[i].y,
                                                                     menu.options[i].w, menu.options[i].h), 7])
            else:
                liste_rafraichir.append([menu.options[i].images[0], (menu.options[i].x, menu.options[i].y,
                                                                     menu.options[i].w, menu.options[i].h), 7])

        # GERER LES CHOIX

        if choix == 1:  # VALIDER
            if session.nom != "":
                chaine = "saves/"+session.nom+".txt"
                try:
                    a = open(chaine, "r")
                    a.close()
                except:
                    with open("saves/liste_personnages.txt", "a") as liste_personnages:
                        liste_personnages.write("\n"+session.nom)
                    with open(chaine, "wb") as session_personnage:
                        pickler = pickle.Pickler(session_personnage)
                        pickler.dump(session)
                    nom_fini = True
                pygame.key.set_repeat()

        elif choix == 2:  # RETOUR
            pygame.key.set_repeat()
            return session, 1, liste_rafraichir, liste_messages

    return session, 0, liste_rafraichir, liste_messages


def choisir_session(ecran, resolution, liste_rafraichir, liste_messages):

    global FOND

    # OBTENIR LA LISTE DES PERSONNAGES CREES

    with open("saves/liste_personnages.txt", "r") as liste_personnages:
        liste_noms_personnages = liste_personnages.read().split("\n")

    i = 0
    while i < len(liste_noms_personnages):
        if liste_noms_personnages[i] == "":
            del liste_noms_personnages[i]
            i -= 1
        i += 1

    # CREER LE MENU QUI CONTIENT TOUT LES PERSONNAGES

    menu = Menu()
    menu.x = 0
    menu.y = 0
    menu.w = resolution.current_w
    menu.h = resolution.current_h-128
    for i in range(len(liste_noms_personnages)):
        menu.options.append(Options_Menu())
        menu.options[i].message = liste_noms_personnages[i]
    menu.type = 1
    menu = creer_images_et_positions_menu(menu)

    # CREER LE MENU VALIDER/RETOUR/SUPPRIMER

    options = Menu()
    options.x = 0
    options.y = resolution.current_h-128
    options.w = resolution.current_w
    options.h = 128
    for i in range(3):
        options.options.append(Options_Menu())
    options.options[0].message = "Valider"
    options.options[1].message = "Retour"
    options.options[2].message = "Supprimer"
    options.type = 2
    options = creer_images_et_positions_menu(options)

    # INITIALISER QUELQUES VARIABLES

    cadre = 0
    tempo = 0
    cadre_noir = 0
    personnage_selectionne = -1
    continuer = True
    position_souris = [0, 0]

    temps_actuel = pygame.time.get_ticks()

    while continuer:

        choix = [0, 0]

        # RAFRAICHIR L'IMAGE

        liste_messages, liste_rafraichir = afficher_messages(liste_messages, liste_rafraichir, resolution)
        liste_rafraichir, temps_actuel, tempo = gerer_temps(ecran, tempo, liste_rafraichir, temps_actuel)

        # OBTENIR LE CHOIX DE L'UTILISATEUR

        for entree in pygame.event.get():
            if entree.type == pygame.MOUSEBUTTONUP:
                if entree.button == 1:
                    for i in range(len(menu.options)):
                        if menu.options[i].x+menu.options[i].w > entree.pos[0] > menu.options[i].x and \
                           menu.options[i].y+menu.options[i].h > entree.pos[1] > menu.options[i].y:
                            choix[0] = i+1
                    for i in range(len(options.options)):
                        if options.options[i].x+options.options[i].w > entree.pos[0] > options.options[i].x and \
                           options.options[i].y+options.options[i].h > entree.pos[1] > options.options[i].y:
                            choix[1] = i+1

            if entree.type == pygame.MOUSEMOTION:
                position_souris = [entree.pos[0], entree.pos[1]]

        # AFFICHER LA LISTE DES PERSONNAGES

        for i in range(len(menu.options)):
            if menu.options[i].x+menu.options[i].w > position_souris[0] > menu.options[i].x and \
               menu.options[i].y+menu.options[i].h > position_souris[1] > menu.options[i].y:
                liste_rafraichir.append([menu.options[i].images[1], (menu.options[i].x, menu.options[i].y,
                                                                     menu.options[i].w, menu.options[i].h), 7])
            else:
                liste_rafraichir.append([menu.options[i].images[0], (menu.options[i].x, menu.options[i].y,
                                                                     menu.options[i].w, menu.options[i].h), 7])

        # AFFICHER LE MENU VALIDER/RETOUR/SUPPRIMER

        for i in range(len(options.options)):
            if options.options[i].x+options.options[i].w > position_souris[0] > options.options[i].x and \
               options.options[i].y+options.options[i].h > position_souris[1] > options.options[i].y:
                liste_rafraichir.append([options.options[i].images[1], (options.options[i].x, options.options[i].y,
                                                                        options.options[i].w, options.options[i].h), 7])
            else:
                liste_rafraichir.append([options.options[i].images[0], (options.options[i].x, options.options[i].y,
                                                                        options.options[i].w, options.options[i].h), 7])

        # AFFICHER LE CADRE AUTOUR DU PERSONNAGE SELECTIONNE S'IL Y EN A UN

        if cadre != 0:
            liste_rafraichir.append([cadre, (menu.options[personnage_selectionne].x-6,
                                             menu.options[personnage_selectionne].y-6,
                                             menu.options[personnage_selectionne].w+12,
                                             menu.options[personnage_selectionne].h+12), 7])

        # SELECTIONNER UN PERSONNAGE

        if choix[0] != 0:
            if cadre_noir != 0:
                liste_rafraichir.append([cadre_noir, (menu.options[personnage_selectionne].x-6,
                                                      menu.options[personnage_selectionne].y-6,
                                                      menu.options[personnage_selectionne].w+12,
                                                      menu.options[personnage_selectionne].h+12), 7])
            personnage_selectionne = choix[0]-1
            cadre = \
                pygame.Surface((menu.options[personnage_selectionne].w+12, menu.options[personnage_selectionne].h+12))
            cadre.fill((255, 255, 255))
            cadre.set_colorkey((255, 255, 255))
            cadre.subsurface((2, 2, menu.options[personnage_selectionne].w+8, menu.options[personnage_selectionne].h+8)).fill((255, 255, 0))
            cadre.subsurface((4, 4, menu.options[personnage_selectionne].w+4, menu.options[personnage_selectionne].h+4)).fill((255, 255, 255))
            cadre_noir = \
                pygame.Surface((menu.options[personnage_selectionne].w+12, menu.options[personnage_selectionne].h+12))
            cadre_noir.blit(FOND.subsurface((menu.options[personnage_selectionne].x-6,
                                             menu.options[personnage_selectionne].y-6,
                                             menu.options[personnage_selectionne].w+12,
                                             menu.options[personnage_selectionne].h+12)), (0, 0))

        # VALIDER

        if personnage_selectionne != -1 and choix[1] == 1:
            with open("saves/"+menu.options[personnage_selectionne].message+".txt", "rb") as personnage:
                unpickler = pickle.Unpickler(personnage)
                session = unpickler.load()
            a = 0
            continuer = False

        # RETOUR

        if choix[1] == 2:
            a = 1
            session = None
            continuer = False

        # SUPPRIMER

        if personnage_selectionne != -1 and choix[1] == 3:

            # EFFACER LE PERSONNAGE ET LA SELECTION

            cadre = 0
            liste_rafraichir.append([cadre_noir, (menu.options[personnage_selectionne].x-6,
                                                  menu.options[personnage_selectionne].y-6,
                                                  menu.options[personnage_selectionne].w+12,
                                                  menu.options[personnage_selectionne].h+12), 7])
            cadre_noir = 0
            os.remove("saves/"+menu.options[personnage_selectionne].message+".txt")

            # METTRE A JOUR LA LISTE DES PERSONNAGES

            with open("saves/liste_personnages.txt", "r+") as liste_personnages:
                chaine = liste_personnages.read().split("\n")
                del chaine[0]
                i = 0
                while i < len(chaine):
                    try:
                        a = open("saves/"+chaine[i]+".txt", "r")
                        a.close()
                        i += 1
                    except:
                        del chaine[i]
            with open("saves/liste_personnages.txt", "w") as liste_personnages:
                liste_personnages.write("\n"+"\n".join(chaine))

            # METTRE A JOUR LE MENU

            with open("saves/liste_personnages.txt", "r") as liste_personnages:
                liste_noms_personnages = liste_personnages.read().split("\n")
            i = 0
            while i < len(liste_noms_personnages):
                if liste_noms_personnages[i] == "":
                    del liste_noms_personnages[i]
                    i -= 1
                i += 1
            menu.options = []
            for i in range(len(liste_noms_personnages)):
                menu.options.append(Options_Menu())
                menu.options[i].message = liste_noms_personnages[i]
            menu = creer_images_et_positions_menu(menu)
            liste_rafraichir = mettre_fond(ecran)
            personnage_selectionne = -1

    return session, a, liste_rafraichir, liste_messages


def gerer_menu_jeu(ecran, position_souris, position_ecran_x, position_ecran_y, raccourcis, joueur):

    # AFFICHER L'IMAGE DE FOND DU MENU

    global FOND_MENU_JEU
    liste_rafraichir = [[FOND_MENU_JEU, (position_ecran_x+130, position_ecran_y+38, 700, 500), 7]]

    # CREER LE MENU

    menu = Menu()
    menu.x = position_ecran_x+130
    menu.y = position_ecran_y+38
    menu.w = 700
    menu.h = 500
    for i in range(4):
        menu.options.append(Options_Menu())
    menu.options[0].message = "Continuer"
    menu.options[1].message = "Recommencer la partie"
    menu.options[2].message = "Quitter la partie"
    menu.options[3].message = "Quitter le jeu"
    menu.type = 1
    menu = creer_images_et_positions_menu(menu)

    # COMMENCER LA BOUCLE

    continuer = True
    tempo = 0
    temps_actuel = pygame.time.get_ticks()

    while continuer:

        choix = 0

        # RAFRAICHIR L'IMAGE

        liste_rafraichir, temps_actuel, tempo = gerer_temps(ecran, tempo, liste_rafraichir, temps_actuel)

        # GERER LES ENTREES UTILISATEUR FAIRE ATTENTION, L'UTILISATEUR PEUT AVOIR OUBLIE DE LACHE CERTAINES TOUCHES,
        # OU PEU EN AVOIR ENFONCEES D'AUTRES PUIS QUITTE LE MENU

        for entree in pygame.event.get():
            if entree.type == pygame.KEYDOWN:
                if entree.key == pygame.K_ESCAPE:
                    continuer = False
                    choix = 1
                if entree.key == raccourcis[0][0]:
                    joueur.deplacement_y -= joueur.vitesse
                if entree.key == raccourcis[1][0]:
                    joueur.deplacement_y += joueur.vitesse
                if entree.key == raccourcis[2][0]:
                    joueur.deplacement_x -= joueur.vitesse
                if entree.key == raccourcis[3][0]:
                    joueur.deplacement_x += joueur.vitesse
            if entree.type == pygame.KEYUP:
                if entree.key == raccourcis[0][0]:
                    joueur.deplacement_y += joueur.vitesse
                if entree.key == raccourcis[1][0]:
                    joueur.deplacement_y -= joueur.vitesse
                if entree.key == raccourcis[2][0]:
                    joueur.deplacement_x += joueur.vitesse
                if entree.key == raccourcis[3][0]:
                    joueur.deplacement_x -= joueur.vitesse

            if entree.type == pygame.MOUSEBUTTONUP:
                if entree.button == 1:
                    joueur.attaques.autorisation.remove(1)
                    for i in range(len(menu.options)):
                        if menu.options[i].x+menu.options[i].w > entree.pos[0] > menu.options[i].x and \
                           menu.options[i].y+menu.options[i].h > entree.pos[1] > menu.options[i].y:
                            continuer = False
                            choix = i+1

            if entree.type == pygame.MOUSEMOTION:
                position_souris = [entree.pos[0], entree.pos[1]]

            if entree.type == pygame.MOUSEBUTTONDOWN:
                if entree.button == 1:
                    joueur.attaques.autorisation.append(1)

        # AFFICHER LE MENU

        for i in range(len(menu.options)):
            if menu.options[i].x+menu.options[i].w > position_souris[0] > menu.options[i].x and \
               menu.options[i].y+menu.options[i].h > position_souris[1] > menu.options[i].y:
                liste_rafraichir.append([menu.options[i].images[1],
                                         (menu.options[i].x, menu.options[i].y,
                                          menu.options[i].w, menu.options[i].h), 7])
            else:
                liste_rafraichir.append([menu.options[i].images[0],
                                         (menu.options[i].x, menu.options[i].y,
                                          menu.options[i].w, menu.options[i].h), 7])

    return choix, joueur


def charger_images_monstres(map):

    global PERSONNAGES

    for i in range(len(map.salles)):
        for j in range(len(map.salles[i].ennemis)):

            # CHARGER LES SKINS DES MONSTRES

            map.salles[i].ennemis[j].images.bas = []
            map.salles[i].ennemis[j].images.haut = []
            map.salles[i].ennemis[j].images.droite = []
            map.salles[i].ennemis[j].images.gauche = []

            for l in range(6):
                map.salles[i].ennemis[j].images.bas.append(
                    PERSONNAGES.subsurface((l*64, (map.salles[i].ennemis[j].type+1)*64, 64, 64)))
                map.salles[i].ennemis[j].images.haut.append(
                    PERSONNAGES.subsurface(((l+6)*64, (map.salles[i].ennemis[j].type+1)*64, 64, 64)))
                map.salles[i].ennemis[j].images.droite.append(
                    PERSONNAGES.subsurface(((l+12)*64, (map.salles[i].ennemis[j].type+1)*64, 64, 64)))
                map.salles[i].ennemis[j].images.gauche.append(
                    PERSONNAGES.subsurface(((l+18)*64, (map.salles[i].ennemis[j].type+1)*64, 64, 64)))
                map.salles[i].ennemis[j].images.bas[l].set_colorkey((255, 255, 255))
                map.salles[i].ennemis[j].images.haut[l].set_colorkey((255, 255, 255))
                map.salles[i].ennemis[j].images.droite[l].set_colorkey((255, 255, 255))
                map.salles[i].ennemis[j].images.gauche[l].set_colorkey((255, 255, 255))

            # CHARGER LA MINIBARRE DES MONSTRES

            map.salles[i].ennemis[j].minibarre.image = pygame.Surface((64, 8))
            map.salles[i].ennemis[j].minibarre.image.fill((0, 0, 0))
            map.salles[i].ennemis[j].minibarre.image.set_colorkey((255, 255, 255))
            map.salles[i].ennemis[j].minibarre.image.fill(
                (255, 0, 0), (2, 2, int((map.salles[i].ennemis[j].points_de_vies/map.salles[i].ennemis[j].points_de_vies_maximum)*60), 4))
            map.salles[i].ennemis[j].minibarre.image.fill(
                (255, 255, 255), (2+int((map.salles[i].ennemis[j].points_de_vies/map.salles[i].ennemis[j].points_de_vies_maximum)*60), 2,
                                  62-(2+int((map.salles[i].ennemis[j].points_de_vies/map.salles[i].ennemis[j].points_de_vies_maximum)*60)), 4))

    return map


def charger_images_objets(map):

    global OBJETS
    global OBJETS_RARES

    for i in range(len(map.salles)):

        for j in range(len(map.salles[i].objets)):

            if map.salles[i].objets[j].type < 1000:
                map.salles[i].objets[j].image = \
                    OBJETS.subsurface(((map.salles[i].objets[j].type % 10)*64,
                                       (map.salles[i].objets[j].type//10)*64, 64, 64))

            if map.salles[i].objets[j].type >= 1000:
                map.salles[i].objets[j].type -= 1000
                map.salles[i].objets[j].image = \
                    OBJETS_RARES.subsurface(((map.salles[i].objets[j].type % 10)*64,
                                             (int(map.salles[i].objets[j].type/10))*64, 64, 64))
                map.salles[i].objets[j].type += 1000

            map.salles[i].objets[j].image.set_colorkey((255, 255, 255))

    return map


def creer_message(liste_messages, resolution, mots):

    global CARACTERES

    # DECOUPER LE MESSAGE SI BESOIN

    split = False
    if len(mots)*32 > resolution.current_w:
        mots = mots.split(" ")
        split = True
        for i in range(len(mots)):
            if len(mots[i])*32 > resolution.current_w:
                raise ValueError("Le message est trop long.")
        if len(mots)*64 > resolution.current_h:
            raise ValueError("Le message est trop épais.")

    # CREER LE MESSAGE

    message = Message()
    message.w = 0
    if split:
        for i in range(len(mots)):
            if len(mots[i])*32 > message.w:
                message.w = len(mots[i])*32
        message.h = (len(mots)*64)+8
    else:
        message.w = len(mots)*32
        message.h = 72
    message.w += 8

    message.x = (resolution.current_w-message.w)//2
    message.y = (resolution.current_h-message.h)//2

    message.image = pygame.Surface((message.w, message.h))
    message.image.fill((126, 88, 63))
    message.image.fill((205, 133, 63), (2, 2, message.w-4, message.h-4))

    if split:
        for i in range(len(mots)):
            for j in range(mots[i]):
                message.image.blit(CARACTERES.subsurface(((ord(mots[i][j]) % 10)*32, (ord(mots[i][j])//10)*64, 32, 64)),
                                   (4+(j*32), 4+(i*64)))
    else:
        for i in range(len(mots)):
            message.image.blit(CARACTERES.subsurface(((ord(mots[i]) % 10)*32, (ord(mots[i])//10)*64, 32, 64)),
                               (4+(i*32), 4))

    # DECALER LES AUTRES MESSAGES

    if len(liste_messages) > 0:
        i = 0
        while i < len(liste_messages):
            liste_messages[i].y -= message.h+4
            if liste_messages[i].y < 0:
                del liste_messages[i]
                i -= 1
            i += 1

    # AJOUTER LE MESSAGE A LA LISTE

    message.temps_creation = pygame.time.get_ticks()

    liste_messages.append(message)

    return liste_messages


def afficher_messages(liste_messages, liste_rafraichir, resolution):

    i = 0
    global FOND

    while i < len(liste_messages):
        liste_rafraichir.append([FOND.subsurface((0, liste_messages[i].y, resolution.current_w, liste_messages[i].h)),
                                 (0, liste_messages[i].y, resolution.current_w, liste_messages[i].h), 1])
        if liste_messages[i].temps_creation > (pygame.time.get_ticks()-4000) and i >= len(liste_messages)-3:
            liste_rafraichir.append([liste_messages[i].image, (liste_messages[i].x, liste_messages[i].y,
                                                               liste_messages[i].w, liste_messages[i].h), 8])
        else:
            del liste_messages[i]
            i -= 1
        i += 1

    return liste_messages, liste_rafraichir


def nombre_de_saves():

    with open("saves/liste_personnages.txt") as liste_personnages:
        liste_saves = liste_personnages.read().split("\n")
        i = 0
        while i < len(liste_saves):
            if liste_saves[i] == "":
                del liste_saves[i]
                i -= 1
            i += 1

        return len(liste_saves)


def choisir_competences(ecran, resolution, liste_rafraichir, liste_messages, session):

    global ICONES_COMPETENCES
    global FOND
    global CARACTERES

    # CREER UNE LISTE DE MENUS QUI CONTIENNENT LES ETAGES DE COMPETENCES

    arbre_de_competences = [Menu(), Menu(), Menu(), Menu()]

    for i in range(len(arbre_de_competences)):
        arbre_de_competences[i].x = 0
        arbre_de_competences[i].y = \
            (resolution.current_h-128)-((i+1)*((resolution.current_h-256)//len(arbre_de_competences)))
        arbre_de_competences[i].w = resolution.current_w
        arbre_de_competences[i].h = (resolution.current_h-256)//len(arbre_de_competences)
        arbre_de_competences[i].type = 2

    # ETAGE 0

    arbre_de_competences[0].options.append(Options_Menu())
    arbre_de_competences[0].options[0].images = [ICONES_COMPETENCES.subsurface((0, 0, 64, 64)),
                                                 pygame.Surface((64, 64)),
                                                 ICONES_COMPETENCES.subsurface((640, 0, 64, 64))]
    arbre_de_competences[0].options[0].images[1].fill((255, 0, 0))
    arbre_de_competences[0].options[0].images[1].blit(
        arbre_de_competences[0].options[0].images[0].subsurface((2, 2, 60, 60)), (2, 2))

    # ETAGE 1

    for i in range(3):
        arbre_de_competences[1].options.append(Options_Menu())
        arbre_de_competences[1].options[i].images = [ICONES_COMPETENCES.subsurface((64+(64*i), 0, 64, 64)),
                                                     pygame.Surface((64, 64)),
                                                     ICONES_COMPETENCES.subsurface((704+(64*i), 0, 64, 64))]
        arbre_de_competences[1].options[i].images[1].fill((255, 0, 0))
        arbre_de_competences[1].options[i].images[1].blit(
            arbre_de_competences[1].options[i].images[0].subsurface((2, 2, 60, 60)), (2, 2))

    # ETAGE 2

    for i in range(4):
        arbre_de_competences[2].options.append(Options_Menu())
        arbre_de_competences[2].options[i].images = [ICONES_COMPETENCES.subsurface((256+(64*i), 0, 64, 64)),
                                                     pygame.Surface((64, 64)),
                                                     ICONES_COMPETENCES.subsurface((896+(64*i), 0, 64, 64))]
        arbre_de_competences[2].options[i].images[1].fill((255, 0, 0))
        arbre_de_competences[2].options[i].images[1].blit(
            arbre_de_competences[2].options[i].images[0].subsurface((2, 2, 60, 60)), (2, 2))

    # ETAGE 3

    for i in range(4):
        arbre_de_competences[3].options.append(Options_Menu())
        arbre_de_competences[3].options[i].images = [ICONES_COMPETENCES.subsurface(((512+(64*i)) % 640, ((512+(64*i))//640)*64, 64, 64)),
                                                     pygame.Surface((64, 64)),
                                                     ICONES_COMPETENCES.subsurface((640+(512+(64*i)) % 640, ((512+(64*i))//640)*64, 64, 64))]
        arbre_de_competences[3].options[i].images[1].fill((255, 0, 0))
        arbre_de_competences[3].options[i].images[1].blit(
            arbre_de_competences[3].options[i].images[0].subsurface((2, 2, 60, 60)), (2, 2))

    # CALCULER L'EMPLACEMENT DE CHAQUE OPTION

    for i in range(len(arbre_de_competences)):
        for j in range(len(arbre_de_competences[i].options)):
            arbre_de_competences[i].options[j].w = 64
            arbre_de_competences[i].options[j].h = 64
            arbre_de_competences[i].options[j].x = (((resolution.current_w-(len(arbre_de_competences[i].options)*64))//(len(arbre_de_competences[i].options)+1))*(j+1))+(j*64)
            arbre_de_competences[i].options[j].y = arbre_de_competences[i].y+((arbre_de_competences[i].h-64)//2)

    # CREER LE MENU VALIDER/RETOUR/REINITIALISER

    menu = Menu()
    menu.x = 0
    menu.y = resolution.current_h-128
    menu.w = resolution.current_w
    menu.h = 128
    for i in range(3):
        menu.options.append(Options_Menu())
    menu.options[0].message = "Valider"
    menu.options[1].message = "Retour"
    menu.options[2].message = "Reinitialiser"
    menu.type = 2
    menu = creer_images_et_positions_menu(menu)

    # INITIALISER QUELQUES VARIABLES

    while len(session.competences) < 12:
        session.competences.append(0)
    liste = list(session.competences)
    points = session.points_de_competences

    # texte = [x, y, w, h, message, image, points]
    texte = [0, 32, 0, 64, "Points restants: "+str(points), 0, points]
    texte[5] = pygame.Surface((len(texte[4])*32, 64))
    texte[5].set_colorkey((255, 255, 255))
    texte[5].fill((255, 255, 255))
    for i in range(len(texte[4])):
        texte[5].blit(CARACTERES.subsurface(((ord(texte[4][i]) % 10)*32, (ord(texte[4][i])//10)*64, 32, 64)),
                      (32*i, 0))
    texte[0] = (resolution.current_w-(len(texte[4])*32))//2
    texte[2] = len(texte[4])*32

    continuer = True
    tempo = 0

    # fenetre = [x, y, w, h, image, arbre y, arbre x, ancien arbre y, ancien arbre x]
    fenetre = [0, 0, 0, 0, 0, -1, -1, -1, -1]
    position_souris = [0, 0]
    choix = [-1, -1, 0]

    temps_actuel = pygame.time.get_ticks()

    # PAGE DE COMPETENCES

    while continuer:

        # AFFICHER LE NOMBRE DE POINTS RESTANTS

        liste_rafraichir.append([FOND.subsurface((texte[0], texte[1], texte[2], texte[3])),
                                 (texte[0], texte[1], texte[2], texte[3]), 1])

        if points != texte[6]:
            texte[6] = points
            texte[4] = "Points restants: "+str(points)
            texte[5] = pygame.Surface((len(texte[4])*32, 64))
            texte[5].set_colorkey((255, 255, 255))
            texte[5].fill((255, 255, 255))
            for i in range(len(texte[4])):
                texte[5].blit(CARACTERES.subsurface(((ord(texte[4][i]) % 10)*32, (ord(texte[4][i])//10)*64, 32, 64)),
                              (32*i, 0))
            texte[0] = (resolution.current_w-(len(texte[4])*32))//2
            texte[2] = len(texte[4])*32

        liste_rafraichir.append([texte[5], (texte[0], texte[1], texte[2], texte[3]), 7])

        # RAFRAICHIR IMAGE

        liste_messages, liste_rafraichir = afficher_messages(liste_messages, liste_rafraichir, resolution)
        liste_rafraichir, temps_actuel, tempo = gerer_temps(ecran, tempo, liste_rafraichir, temps_actuel)

        # MISE A JOUR DE CERTAINES VARIABLES

        fenetre_effaceur = [fenetre[0], fenetre[1], fenetre[2], fenetre[3]]
        fenetre[7] = fenetre[5]
        fenetre[8] = fenetre[6]
        fenetre[5] = -1
        fenetre[6] = -1
        if choix[0] != -1 or choix[1] != -1:
            fenetre[7] = -1
            fenetre[8] = -1
        choix = [-1, -1, 0]

        # GERER LES ENTREES UTILISATEUR

        for entree in pygame.event.get():
            if entree.type == pygame.MOUSEBUTTONUP:
                if entree.button == 1:
                    a = -1
                    for etage in arbre_de_competences:
                        for i in range(len(etage.options)):
                            a += 1
                            if etage.options[i].x+etage.options[i].w > entree.pos[0] > etage.options[i].x and \
                               etage.options[i].y+etage.options[i].h > entree.pos[1] > etage.options[i].y:
                                choix[0] = a
                    for i in range(len(menu.options)):
                        if menu.options[i].x+menu.options[i].w > entree.pos[0] > menu.options[i].x and \
                           menu.options[i].y+menu.options[i].h > entree.pos[1] > menu.options[i].y:
                            choix[2] = i+1

                if entree.button == 3:
                    a = -1
                    for etage in arbre_de_competences:
                        for i in range(len(etage.options)):
                            a += 1
                            if etage.options[i].x+etage.options[i].w > entree.pos[0] > etage.options[i].x and \
                               etage.options[i].y+etage.options[i].h > entree.pos[1] > etage.options[i].y:
                                choix[1] = a

            if entree.type == pygame.MOUSEMOTION:
                position_souris = [entree.pos[0], entree.pos[1]]

        # CREER UNE LISTE DE BOOLEENS: TRUE SI LA COMPETENCE NE PEUT ETRE UP

        liste_impossibles = [False,
                             not liste[0] >= 2,
                             not liste[0] >= 2,
                             not liste[0] >= 2,
                             not liste[0]+liste[1] >= 4,
                             not liste[0]+liste[1] >= 4,
                             not liste[0]+liste[2] >= 4,
                             not liste[0]+liste[3] >= 4,
                             not liste[0]+liste[1]+liste[4] >= 7,
                             not liste[0]+liste[1]+liste[5] >= 6,
                             not liste[0]+liste[2]+liste[6] >= 6,
                             not liste[0]+liste[3]+liste[7] >= 6]

        # AFFICHER L'ARBRE DE COMPETENCES ET OBTENIR LA COMPETENCE VISEE AVEC LA SOURIS

        a = -1
        for j in range(len(arbre_de_competences)):
            for i in range(len(arbre_de_competences[j].options)):
                a += 1
                if liste[a] > 0:
                    liste_rafraichir.append([arbre_de_competences[j].options[i].images[1],
                                             (arbre_de_competences[j].options[i].x,
                                              arbre_de_competences[j].options[i].y,
                                              arbre_de_competences[j].options[i].w,
                                              arbre_de_competences[j].options[i].h), 7])
                elif liste[a] == 0 and not liste_impossibles[a]:
                    liste_rafraichir.append([arbre_de_competences[j].options[i].images[0],
                                             (arbre_de_competences[j].options[i].x,
                                              arbre_de_competences[j].options[i].y,
                                              arbre_de_competences[j].options[i].w,
                                              arbre_de_competences[j].options[i].h), 7])
                elif liste[a] == 0 and liste_impossibles[a]:
                    liste_rafraichir.append([arbre_de_competences[j].options[i].images[2],
                                             (arbre_de_competences[j].options[i].x,
                                              arbre_de_competences[j].options[i].y,
                                              arbre_de_competences[j].options[i].w,
                                              arbre_de_competences[j].options[i].h), 7])

                if arbre_de_competences[j].options[i].x+arbre_de_competences[j].options[i].w > position_souris[0] > arbre_de_competences[j].options[i].x and \
                   arbre_de_competences[j].options[i].y+arbre_de_competences[j].options[i].h > position_souris[1] > arbre_de_competences[j].options[i].y:
                    fenetre[5] = j
                    fenetre[6] = i

        # AFFICHER LE MENU

        for i in range(len(menu.options)):
            if menu.options[i].x+menu.options[i].w > position_souris[0] > menu.options[i].x and \
               menu.options[i].y+menu.options[i].h > position_souris[1] > menu.options[i].y:
                liste_rafraichir.append([menu.options[i].images[1], (menu.options[i].x, menu.options[i].y,
                                                                     menu.options[i].w, menu.options[i].h), 7])
            else:
                liste_rafraichir.append([menu.options[i].images[0], (menu.options[i].x, menu.options[i].y,
                                                                     menu.options[i].w, menu.options[i].h), 7])

        # CREER UNE FENETRE SI BESOIN

        fenetre[0] = position_souris[0]
        fenetre[1] = position_souris[1]

        if fenetre[5] != -1 and fenetre[6] != -1:
            fenetre = creer_fenetre_competences(fenetre, liste, liste_impossibles)

        # AJUSTER L'EMPLACEMENT DE LA FENETRE SI BESOIN

        if fenetre[0]+fenetre[2] >= resolution.current_w:
            fenetre[0] = resolution.current_w-fenetre[2]
        if fenetre[1]+fenetre[3] >= resolution.current_h:
            fenetre[1] = resolution.current_h-fenetre[3]

        # EFFACER PUIS REAFFICHER LA FENETRE

        if (fenetre[7] != -1 and fenetre[8] != -1) or (fenetre[5] != -1 and fenetre[6] != -1):
            liste_rafraichir.append([
                FOND.subsurface((fenetre_effaceur[0], fenetre_effaceur[1], fenetre_effaceur[2], fenetre_effaceur[3])),
                (fenetre_effaceur[0], fenetre_effaceur[1], fenetre_effaceur[2], fenetre_effaceur[3]), 0])

        if fenetre[5] != -1 and fenetre[6] != -1:
            liste_rafraichir.append([fenetre[4], (fenetre[0], fenetre[1], fenetre[2], fenetre[3]), 8])

        # AJOUTER DES POINTS AUX COMPETENCES

        if choix[0] != -1:
            if choix[0] == 0:
                if liste[0] < 3 and points > 0:
                    liste[0] += 1
                    points -= 1
            if choix[0] == 1:
                if liste[1] < 2 and points > 0 and liste[0] >= 2:
                    liste[1] += 1
                    points -= 1
            if choix[0] == 2:
                if liste[2] < 2 and points > 0 and liste[0] >= 2:
                    liste[2] += 1
                    points -= 1
            if choix[0] == 3:
                if liste[3] < 2 and points > 0 and liste[0] >= 2:
                    liste[3] += 1
                    points -= 1
            if choix[0] == 4:
                if liste[4] < 3 and points > 0 and liste[0]+liste[1] >= 4:
                    liste[4] += 1
                    points -= 1
            if choix[0] == 5:
                if liste[5] < 2 and points > 0 and liste[0]+liste[1] >= 4:
                    liste[5] += 1
                    points -= 1
            if choix[0] == 6:
                if liste[6] < 2 and points > 0 and liste[0]+liste[2] >= 4:
                    liste[6] += 1
                    points -= 1
            if choix[0] == 7:
                if liste[7] < 2 and points > 0 and liste[0]+liste[3] >= 4:
                    liste[7] += 1
                    points -= 1
            if choix[0] == 8:
                if liste[8] < 2 and points > 0 and liste[0]+liste[1]+liste[4] >= 7:
                    liste[8] += 1
                    points -= 1
            if choix[0] == 9:
                if liste[9] < 3 and points > 0 and liste[0]+liste[1]+liste[5] >= 6:
                    liste[9] += 1
                    points -= 1
            if choix[0] == 10:
                if liste[10] < 3 and points > 0 and liste[0]+liste[2]+liste[6] >= 6:
                    liste[10] += 1
                    points -= 1
            if choix[0] == 11:
                if liste[11] < 3 and points > 0 and liste[0]+liste[3]+liste[7] >= 6:
                    liste[11] += 1
                    points -= 1

        # RETIRER DES POINTS AUX COMPETENCES

        if choix[1] != -1:
            if choix[1] == 0:
                if liste[0] > 0 and \
                   (liste[11] == 0 or liste[0]+liste[3]+liste[7] > 6) and \
                   (liste[7] == 0 or liste[0]+liste[3] > 4) and \
                   (liste[3] == 0 or liste[0] > 2) and \
                   (liste[10] == 0 or liste[0]+liste[2]+liste[6] > 6) and \
                   (liste[6] == 0 or liste[0]+liste[2] > 4) and \
                   (liste[2] == 0 or liste[0] > 2) and \
                   (liste[9] == 0 or liste[0]+liste[1]+liste[5] > 6) and \
                   (liste[5] == 0 or liste[0]+liste[1] > 4) and \
                   (liste[1] == 0 or liste[0] > 2) and \
                   (liste[8] == 0 or liste[0]+liste[1]+liste[4] > 7) and \
                   (liste[4] == 0 or liste[0]+liste[1] > 4):
                    liste[0] -= 1
                    points += 1
            if choix[1] == 1:
                if liste[1] > 0 and \
                   (liste[4] == 0 or liste[0]+liste[1] > 4) and \
                   (liste[5] == 0 or liste[0]+liste[1] > 4) and \
                   (liste[8] == 0 or liste[0]+liste[1]+liste[4] > 7) and \
                   (liste[9] == 0 or liste[0]+liste[1]+liste[5] > 6):
                    liste[1] -= 1
                    points += 1
            if choix[1] == 2:
                if liste[2] > 0 and \
                   (liste[6] == 0 or liste[0]+liste[2] > 4) and \
                   (liste[10] == 0 or liste[0]+liste[2]+liste[6] > 6):
                    liste[2] -= 1
                    points += 1
            if choix[1] == 3:
                if liste[3] > 0 and \
                   (liste[7] == 0 or liste[0]+liste[3] > 4) and \
                   (liste[11] == 0 or liste[0]+liste[3]+liste[7] > 6):
                    liste[3] -= 1
                    points += 1
            if choix[1] == 4:
                if liste[4] > 0 and (liste[8] == 0 or liste[0]+liste[1]+liste[4] > 7):
                    liste[4] -= 1
                    points += 1
            if choix[1] == 5:
                if liste[5] > 0 and (liste[9] == 0 or liste[0]+liste[1]+liste[5] > 6):
                    liste[5] -= 1
                    points += 1
            if choix[1] == 6:
                if liste[6] > 0 and (liste[10] == 0 or liste[0]+liste[2]+liste[6] > 6):
                    liste[6] -= 1
                    points += 1
            if choix[1] == 7:
                if liste[7] > 0 and (liste[11] == 0 or liste[0]+liste[3]+liste[7] > 6):
                    liste[7] -= 1
                    points += 1
            if choix[1] == 8:
                if liste[8] > 0:
                    liste[8] -= 1
                    points += 1
            if choix[1] == 9:
                if liste[9] > 0:
                    liste[9] -= 1
                    points += 1
            if choix[1] == 10:
                if liste[10] > 0:
                    liste[10] -= 1
                    points += 1
            if choix[1] == 11:
                if liste[11] > 0:
                    liste[11] -= 1
                    points += 1

        # VALIDER/RETOUR/REINITIALISER

        if choix[2] == 1:
            session.points_de_competences = points
            session.competences = liste
            continuer = False
        if choix[2] == 2:
            continuer = False
        if choix[2] == 3:
            points = session.niveau
            liste = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    return session, liste_rafraichir, liste_messages


def creer_fenetre_souris(message_fenetre):

    global CARACTERES_MINI

    chaines = message_fenetre.split("\n")

    taille_max = 0
    for chaine in chaines:
        if len(chaine) > taille_max:
            taille_max = len(chaine)

    w = 6+taille_max*12
    h = 6+len(chaines)*22
    fenetre_image = pygame.Surface((w, h))
    fenetre_image.fill((155, 155, 155))
    fenetre_image.fill((0, 0, 0), (2, 2, w-4, h-4))

    for i in range(len(chaines)):
        for j in range(len(chaines[i])):
            fenetre_image.blit(
                CARACTERES_MINI.subsurface(((ord(chaines[i][j]) % 10)*12, (ord(chaines[i][j])//10)*20, 12, 20)),
                (((w-(len(chaines[i])*12))//2)+j*12, i*22+4))

    return fenetre_image, w, h


def creer_fenetre_competences(fenetre, liste, liste_impossibles):

    if fenetre[5] == 0 and fenetre[6] == 0:
        if not (fenetre[7] == 0 and fenetre[8] == 0):
            chaine = "Force brute\n\n" \
                     "Amelioration actuelle:\n"

            if liste[0] == 0:
                chaine += "Aucune\n"
            else:
                chaine += "Vos attaques infligent\n" + \
                          str(10*liste[0])+" points de degats supplementaires\n"

            chaine += "\nAmelioration du niveau suivant:\n"

            if liste[0] == 3:
                chaine += "Aucune\n"
            else:
                chaine += "Vos attaques infligent\n" + \
                          str(10*(liste[0]+1))+" points de degats supplementaires\n"

            chaine += "\nniveau actuel: "+str(liste[0])+"/3"

            fenetre[4], fenetre[2], fenetre[3] = creer_fenetre_souris(chaine)

    if fenetre[5] == 1 and fenetre[6] == 0:
        if not (fenetre[7] == 1 and fenetre[8] == 0):
            chaine = "Mitraillette ambulante\n\n" \
                     "Amelioration actuelle:\n"

            if liste[1] == 0:
                chaine += "Aucune\n"
            elif liste[1] == 1:
                chaine += "Le temps entre deux attaques\n" \
                          "est diminue de 5 %\n"
            elif liste[1] == 2:
                chaine += "Le temps entre deux attaques\n" \
                          "est diminue de 15 %\n"

            chaine += "\nAmelioration du niveau suivant:\n"

            if liste[1] == 0:
                chaine += "Le temps entre deux attaques\n" \
                          "est diminue de 5 %\n"
            elif liste[1] == 1:
                chaine += "Le temps entre deux attaques\n" \
                          "est diminue de 15 %\n"
            elif liste[1] == 2:
                chaine += "Aucune\n"

            chaine += "\nniveau actuel: "+str(liste[1])+"/2\n"

            if liste_impossibles[1]:
                chaine += "\nVous ne pouvez pas encore debloquer cette competence"

            fenetre[4], fenetre[2], fenetre[3] = creer_fenetre_souris(chaine)

    if fenetre[5] == 1 and fenetre[6] == 1:
        if not (fenetre[7] == 1 and fenetre[8] == 1):
            chaine = "Sac a vie\n\n" \
                     "Amelioration actuelle:\n"

            if liste[2] == 0:
                chaine += "Aucune\n"
            else:
                chaine += "Vos points de vie maximums sont augmentes de "+str(liste[2]*30)+"\n"

            chaine += "\nAmelioration du niveau suivant:\n"

            if liste[2] == 2:
                chaine += "Aucune\n"
            else:
                chaine += "Vos points de vie maximums sont augmentes de "+str((liste[2]+1)*30)+"\n"

            chaine += "\nniveau actuel: "+str(liste[2])+"/2\n"

            if liste_impossibles[2]:
                chaine += "\nVous ne pouvez pas encore debloquer cette competence"

            fenetre[4], fenetre[2], fenetre[3] = creer_fenetre_souris(chaine)

    if fenetre[5] == 1 and fenetre[6] == 2:
        if not (fenetre[7] == 1 and fenetre[8] == 2):
            chaine = "Sorcier\n\n" \
                     "Amelioration actuelle:\n"

            if liste[3] == 0:
                chaine += "Aucune\n"
            else:
                chaine += "Vous gagnez "+str(5*liste[3])+" points de mana supplementaires\n" \
                          "lorsque vous tuez un ennemi\n"

            chaine += "\nAmelioration du niveau suivant:\n"

            if liste[3] == 2:
                chaine += "Aucune\n"
            else:
                chaine += "Vous gagnez "+str(5*(liste[3]+1))+" points de mana supplementaires\n" \
                          "lorsque vous tuez un ennemi\n"

            chaine += "\nniveau actuel: "+str(liste[3])+"/2\n"

            if liste_impossibles[3]:
                chaine += "\nVous ne pouvez pas encore debloquer cette competence"

            fenetre[4], fenetre[2], fenetre[3] = creer_fenetre_souris(chaine)

    if fenetre[5] == 2 and fenetre[6] == 0:
        if not (fenetre[7] == 2 and fenetre[8] == 0):
            chaine = "Canon humain\n\n" \
                     "Amelioration actuelle:\n"

            if liste[4] == 0:
                chaine += "Aucune\n"
            elif liste[4] == 1:
                chaine += "Vos attaques de base se deplacent 20 % plus vite\n"
            elif liste[4] == 2:
                chaine += "Vos attaques de base se deplacent 30 % plus vite\n"
            elif liste[4] == 3:
                chaine += "Vos attaques de base se deplacent 50 % plus vite\n"

            chaine += "\nAmelioration du niveau suivant:\n"

            if liste[4] == 3:
                chaine += "Aucune\n"
            elif liste[4] == 0:
                chaine += "Vos attaques de base se deplacent 20 % plus vite\n"
            elif liste[4] == 1:
                chaine += "Vos attaques de base se deplacent 30 % plus vite\n"
            elif liste[4] == 2:
                chaine += "Vos attaques de base se deplacent 50 % plus vite\n"

            chaine += "\nniveau actuel: "+str(liste[4])+"/3\n"

            if liste_impossibles[4]:
                chaine += "\nVous ne pouvez pas encore debloquer cette competence"

            fenetre[4], fenetre[2], fenetre[3] = creer_fenetre_souris(chaine)

    if fenetre[5] == 2 and fenetre[6] == 1:
        if not (fenetre[7] == 2 and fenetre[8] == 1):
            chaine = "Sonic en herbe\n\n" \
                     "Amelioration actuelle:\n"

            if liste[5] == 0:
                chaine += "Aucune\n"
            else:
                chaine += "Vous vous deplacez "+str(liste[5]*20)+"% plus vite\n"

            chaine += "\nAmelioration du niveau suivant:\n"

            if liste[5] == 2:
                chaine += "Aucune\n"
            else:
                chaine += "Vous vous deplacez "+str((liste[5]+1)*20)+"% plus vite\n"

            chaine += "\nniveau actuel: "+str(liste[5])+"/2\n"

            if liste_impossibles[5]:
                chaine += "\nVous ne pouvez pas encore debloquer cette competence"

            fenetre[4], fenetre[2], fenetre[3] = creer_fenetre_souris(chaine)

    if fenetre[5] == 2 and fenetre[6] == 2:
        if not (fenetre[7] == 2 and fenetre[8] == 2):
            chaine = "Carnivore\n\n" \
                     "Amelioration actuelle:\n"

            if liste[6] == 0:
                chaine += "Aucune\n"
            else:
                chaine += "Vous avez "+str(100+100*liste[6])+"% de chances supplementaires\n" \
                          "d'obtenir un coeur sur les ennemis\n"

            chaine += "\nAmelioration du niveau suivant:\n"

            if liste[6] == 2:
                chaine += "Aucune\n"
            else:
                chaine += "Vous avez "+str(100+100*(liste[6]+1))+"% de chances supplementaires\n" \
                          "d'obtenir un coeur sur les ennemis\n"

            chaine += "\nniveau actuel: "+str(liste[6])+"/2\n"

            if liste_impossibles[6]:
                chaine += "\nVous ne pouvez pas encore debloquer cette competence"

            fenetre[4], fenetre[2], fenetre[3] = creer_fenetre_souris(chaine)

    if fenetre[5] == 2 and fenetre[6] == 3:
        if not (fenetre[7] == 2 and fenetre[8] == 3):
            chaine = "Reservoir magique\n\n" \
                     "Amelioration actuelle:\n"

            if liste[7] == 0:
                chaine += "Aucune\n"
            else:
                chaine += "Votre mana maximum augmente de "+str(20*liste[7])+"\n"

            chaine += "\nAmelioration du niveau suivant:\n"

            if liste[7] == 2:
                chaine += "Aucune\n"
            else:
                chaine += "Votre mana maximum augmente de "+str(20*(liste[7]+1))+"\n"

            chaine += "\nniveau actuel: "+str(liste[7])+"/2\n"

            if liste_impossibles[7]:
                chaine += "\nVous ne pouvez pas encore debloquer cette competence"

            fenetre[4], fenetre[2], fenetre[3] = creer_fenetre_souris(chaine)

    if fenetre[5] == 3 and fenetre[6] == 0:
        if not (fenetre[7] == 3 and fenetre[8] == 0):
            chaine = "Bomber-man\n\n" \
                     "Amelioration actuelle:\n"

            if liste[8] == 0:
                chaine += "Aucune\n"
            else:
                chaine += "Vos attaques explosent a l'impact et infligent "+str(50*liste[8])+"%\n" \
                          "d'une attaque normale aux ennemis proches\n"

            chaine += "\nAmelioration du niveau suivant:\n"

            if liste[8] == 2:
                chaine += "Aucune\n"
            else:
                chaine += "Vos attaques explosent a l'impact et infligent "+str(50*(liste[8]+1))+"%\n" \
                          "d'une attaque normale aux ennemis proches\n"

            chaine += "\nniveau actuel: "+str(liste[8])+"/2\n"

            if liste_impossibles[8]:
                chaine += "\nVous ne pouvez pas encore debloquer cette competence"

            fenetre[4], fenetre[2], fenetre[3] = creer_fenetre_souris(chaine)

    if fenetre[5] == 3 and fenetre[6] == 1:
        if not (fenetre[7] == 3 and fenetre[8] == 1):
            chaine = "Ninja\n\n" \
                     "Amelioration actuelle:\n"

            if liste[9] == 0:
                chaine += "Aucune\n"
            else:
                chaine += "Lorsqu'un ennemi vous touche, vous avez "+str(15*liste[9])+"%\n" \
                          "de chances d'obtenir un temps d'invincibilite\nsans perdre de points de vie\n"

            chaine += "\nAmelioration du niveau suivant:\n"

            if liste[9] == 3:
                chaine += "Aucune\n"
            else:
                chaine += "Lorsqu'un ennemi vous touche, vous avez "+str(15*(liste[9]+1))+"%\n" \
                          "de chances d'obtenir un temps d'invincibilite\nsans perdre de points de vie\n"

            chaine += "\nniveau actuel: "+str(liste[9])+"/3\n"

            if liste_impossibles[9]:
                chaine += "\nVous ne pouvez pas encore debloquer cette competence"

            fenetre[4], fenetre[2], fenetre[3] = creer_fenetre_souris(chaine)

    if fenetre[5] == 3 and fenetre[6] == 2:
        if not (fenetre[7] == 3 and fenetre[8] == 2):
            chaine = "Vampire\n\n" \
                     "Amelioration actuelle:\n"

            if liste[10] == 0:
                chaine += "Aucune\n"
            else:
                chaine += "Vous regagnez "+str(2*liste[10])+" points de vie a chaque\n" \
                          "fois que vous attaquez un ennemi\n"

            chaine += "\nAmelioration du niveau suivant:\n"

            if liste[10] == 3:
                chaine += "Aucune\n"
            else:
                chaine += "Vous regagnez "+str(2*(liste[10]+1))+" points de vie a chaque\n" \
                          "fois que vous attaquez un ennemi\n"

            chaine += "\nniveau actuel: "+str(liste[10])+"/3\n"

            if liste_impossibles[10]:
                chaine += "\nVous ne pouvez pas encore debloquer cette competence"

            fenetre[4], fenetre[2], fenetre[3] = creer_fenetre_souris(chaine)

    if fenetre[5] == 3 and fenetre[6] == 3:
        if not (fenetre[7] == 3 and fenetre[8] == 3):
            chaine = "Aspirateur magique\n\n" \
                     "Amelioration actuelle:\n"

            if liste[11] == 0:
                chaine += "Aucune\n"
            else:
                chaine += "Vous gagnez "+str(liste[11])+" points de mana par seconde\n" \
                          "tant qu'il y a des ennemis dans la meme salle\n"

            chaine += "\nAmelioration du niveau suivant:\n"

            if liste[11] == 3:
                chaine += "Aucune\n"
            else:
                chaine += "Vous gagnez "+str(liste[11]+1)+" points de mana par seconde\n" \
                          "tant qu'il y a des ennemis dans la meme salle\n"

            chaine += "\nniveau actuel: "+str(liste[11])+"/3\n"

            if liste_impossibles[11]:
                chaine += "\nVous ne pouvez pas encore debloquer cette competence"

            fenetre[4], fenetre[2], fenetre[3] = creer_fenetre_souris(chaine)

    return fenetre


def mettre_fond(ecran):

    global FOND

    ecran.blit(FOND, (0, 0))
    pygame.display.flip()
    liste_rafraichir = list()

    return liste_rafraichir


def gerer_temps(ecran, tempo, liste_rafraichir, temps_actuel):

    rafraichir_image(liste_rafraichir, ecran)
    liste_rafraichir = []
    temps_actuel = gerer_fps(temps_actuel)
    tempo = gerer_tempo(tempo)

    return liste_rafraichir, temps_actuel, tempo


def afficher_minibar(map, joueur, position_ecran_x, position_ecran_y, liste_rafraichir):

    for ennemi in map.salles[joueur.salle].ennemis:

        # EFFACER L'ANCIENNE MINIBARRE

        liste_rafraichir.append([map.salles[joueur.salle].image.subsurface(
            (ennemi.minibarre.x, ennemi.minibarre.y, 64, 8)),
            (position_ecran_x+ennemi.minibarre.x, position_ecran_y+ennemi.minibarre.y, 64, 8), 1])

        # RECALCULER LA POSITION ET RECREER L'IMAGE DE LA MINIBARRE

        ennemi.minibarre.x = ennemi.x
        ennemi.minibarre.y = ennemi.y+66

        ennemi.minibarre.image.fill((255, 0, 0),
                                    (2, 2, int((ennemi.points_de_vies/ennemi.points_de_vies_maximum)*60), 4))
        ennemi.minibarre.image.fill((255, 255, 255),
                                    (2+int((ennemi.points_de_vies/ennemi.points_de_vies_maximum)*60), 2,
                                     62-(2+int((ennemi.points_de_vies/ennemi.points_de_vies_maximum)*60)), 4))

        # AFFICHER LA NOUVELLE MINIBARRE AU NOUVEL EMPLACEMENT

        liste_rafraichir.append([ennemi.minibarre.image,
                                (position_ecran_x+ennemi.minibarre.x, position_ecran_y+ennemi.minibarre.y,
                                 ennemi.minibarre.w, ennemi.minibarre.h), 5])

    return liste_rafraichir


def afficher_game_over(ecran, resolution, niveau):

    global CARACTERES

    messages = ["Game over", "", "Etage atteint:"+str(niveau-1)]
    for i in range(len(messages)):
        for j in range(len(messages[i])):
            ecran.blit(pygame.transform.scale2x(CARACTERES.subsurface(((ord(messages[i][j]) % 10)*32, (ord(messages[i][j])//10)*64, 32, 64))),
                       (((resolution.current_w-(64*len(messages[i])))//2)+(64*j),
                        ((resolution.current_h-(130*len(messages)))//2)+(130*i)))

    pygame.display.flip()

    pygame.time.wait(5000)

    return 0


def choisir_raccourcis(ecran, resolution, liste_rafraichir, raccourcis):

    global CARACTERES
    global CARACTERES_SELECTIONNES

    # CALCULER L'ESPACE DISPONIBLE ENTRE LES BORDS ET LE TEXTE

    espace_restant = (resolution.current_w-984)//4

    # CREER ET AFFICHER L'INTERFACE

    cadre_noir = pygame.Surface((resolution.current_w, resolution.current_h))
    cadre_noir.fill((255, 255, 255))
    cadre_noir.fill((150, 150, 150), (98, 98, resolution.current_w-196, resolution.current_h-266))
    cadre_noir.fill((0, 0, 0), (100, 100, resolution.current_w-200, resolution.current_h-270))
    cadre_noir.fill((150, 150, 150), (resolution.current_w-114, 100, 2, resolution.current_h-270))
    cadre_noir.fill((200, 200, 200), (resolution.current_w-112, 100, 12, resolution.current_h-270))
    cadre_noir.fill((150, 150, 150), (resolution.current_w-306-(2*espace_restant), 100, 2, resolution.current_h-270))
    cadre_noir.set_colorkey((255, 255, 255))
    liste_rafraichir.append([cadre_noir, (0, 0, resolution.current_w, resolution.current_h), 0])
    del cadre_noir

    # RECUPERER UNE COPIE DES RACCOURCIS

    try:
        with open("raccourcis.txt", "r") as fichier_raccourcis:
            raccourcis_copie = fichier_raccourcis.read().split("\n")
            for i in range(len(raccourcis_copie)):
                raccourcis_copie[i] = raccourcis_copie[i].split("=")
                raccourcis_copie[i][0] = int(raccourcis_copie[i][0])
    except:
        raccourcis_copie = [[pygame.K_w, "Defaut"],
                            [pygame.K_s, "Defaut"],
                            [pygame.K_a, "Defaut"],
                            [pygame.K_d, "Defaut"],
                            [pygame.K_e, "Defaut"]]

    # CREER LE MENU VALIDER/RETOUR

    menu = Menu()
    menu.x = 0
    menu.y = resolution.current_h-170
    menu.w = resolution.current_w
    menu.h = 170
    for i in range(2):
        menu.options.append(Options_Menu())
    menu.options[0].message = "Valider"
    menu.options[1].message = "Retour"
    menu.type = 2
    menu = creer_images_et_positions_menu(menu)

    # CREER LE MENU DE DESCRIPTION DES TOUCHES

    menu_description = Menu()
    for i in range(5):
        menu_description.options.append(Options_Menu())
    menu_description.options[0].message = "Avancer"
    menu_description.options[1].message = "Reculer"
    menu_description.options[2].message = "Aller a droite"
    menu_description.options[3].message = "Aller a gauche"
    menu_description.options[4].message = "Poser une bombe"
    menu_description.x = 100
    menu_description.y = 100
    menu_description.w = resolution.current_w-(408+2*espace_restant)
    menu_description.h = len(menu_description.options)*192
    menu_description.type = 1
    menu_description = creer_images_et_positions_menu(menu_description)

    # CREER LA LISTE OU SE TROUVE LE NOM DES TOUCHES

    menu_touches = Menu()
    for i in range(len(menu_description.options)):
        menu_touches.options.append(Options_Menu())
        menu_touches.options[i].message = raccourcis_copie[i][1]
    menu_touches.x = resolution.current_w-306-(2*espace_restant)
    menu_touches.y = 100
    menu_touches.w = 192+(2*espace_restant)
    menu_touches.h = menu_description.h
    menu_touches.type = 1
    menu_touches = creer_images_et_positions_menu(menu_touches)

    # INITIALISER QUELQUES VARIABLES

    # liste_cadre = [x, y, w, h, image]
    liste_cadre = [0, 0, 0, 0, 0]
    choix = [0, 0]
    position_souris = [0, 0]
    continuer = True
    tempo = 0
    temps_actuel = pygame.time.get_ticks()

    # BOUCLE DU MENU

    while continuer:

        # RAFRAICHIR L'IMAGE ET LE CHOIX DE L'UTILISATEUR

        liste_rafraichir, temps_actuel, tempo = gerer_temps(ecran, tempo, liste_rafraichir, temps_actuel)
        choix = [0, choix[1]]

        # GERER LES ENTREES UTILISATEURS

        for entree in pygame.event.get():

            if entree.type == pygame.KEYDOWN:  # CHANGER LE RACCOURCIS
                if entree.unicode != str() and choix != 0:

                    raccourcis_copie[choix[1]-1] = [entree.key, entree.unicode.upper()]

                    # EFFACER LE CADRE

                    if liste_cadre[1] < resolution.current_h-170 and liste_cadre[1]+liste_cadre[3] > 100:
                        if liste_cadre[1]+liste_cadre[3] <= resolution.current_h-170 and liste_cadre[1] >= 100:
                            liste_rafraichir.append([
                                pygame.Surface((liste_cadre[2], liste_cadre[3])),
                                (liste_cadre[0], liste_cadre[1], liste_cadre[2], liste_cadre[3]), 0])
                        if liste_cadre[1]+liste_cadre[3] > resolution.current_h-170:
                            liste_rafraichir.append([
                                pygame.Surface((liste_cadre[2], resolution.current_h-170-liste_cadre[1])),
                                (liste_cadre[0], liste_cadre[1], liste_cadre[2],
                                 resolution.current_h-170-liste_cadre[1]), 0])
                        if liste_cadre[1] < 100:
                            liste_rafraichir.append([
                                pygame.Surface((liste_cadre[2], liste_cadre[3]-(100-liste_cadre[1]))),
                                (liste_cadre[0], liste_cadre[1], liste_cadre[2], liste_cadre[3]), 0])

                    # EFFACER L'ANCIENNE TOUCHE

                    if menu_touches.options[choix[1]-1].y < resolution.current_h-170 and \
                       menu_touches.options[choix[1]-1].y+menu_touches.options[choix[1]-1].h > 100:

                        if menu_touches.options[choix[1]-1].y+menu_touches.options[choix[1]-1].h <= resolution.current_h-170 and \
                           menu_touches.options[choix[1]-1].y >= 100:
                            liste_rafraichir.append(
                                [pygame.Surface((menu_touches.options[choix[1]-1].w, menu_touches.options[choix[1]-1].h)),
                                 (menu_touches.options[choix[1]-1].x, menu_touches.options[choix[1]-1].y,
                                  menu_touches.options[choix[1]-1].w, menu_touches.options[choix[1]-1].h), 7])

                        if menu_touches.options[choix[1]-1].y+menu_touches.options[choix[1]-1].h > resolution.current_h-170:
                            liste_rafraichir.append([pygame.Surface(
                                (menu_touches.options[choix[1]-1].w, resolution.current_h-170-menu_touches.options[choix[1]-1].y)),
                                (menu_touches.options[choix[1]-1].x, menu_touches.options[choix[1]-1].y,
                                 menu_touches.options[choix[1]-1].w, resolution.current_h-170-menu_touches.options[choix[1]-1].y), 7])

                        if menu_touches.options[i].y < 100:
                            liste_rafraichir.append([pygame.Surface(
                                (menu_touches.options[choix[1]-1].w, menu_touches.options[choix[1]-1].h-(100-menu_touches.options[choix[1]-1].y))),
                                (menu_touches.options[choix[1]-1].x, 100, menu_touches.options[choix[1]-1].w,
                                 menu_touches.options[choix[1]-1].h-(100-menu_touches.options[choix[1]-1].y)), 7])

                    # CHANGER LA LISTE DES TOUCHES

                    menu_touches.options[choix[1]-1].message = entree.unicode.upper()
                    menu_touches.options[choix[1]-1].w = 32*len(menu_touches.options[choix[1]-1].message)
                    menu_touches.options[choix[1]-1].x = menu_touches.x+((menu_touches.w//2)-(menu_touches.options[choix[1]-1].w//2))
                    menu_touches.options[choix[1]-1].images[0] = pygame.Surface((menu_touches.options[choix[1]-1].w, 64))
                    menu_touches.options[choix[1]-1].images[0].fill((255, 255, 255))
                    menu_touches.options[choix[1]-1].images[0].set_colorkey((255, 255, 255))
                    menu_touches.options[choix[1]-1].images[1] = pygame.Surface((menu_touches.options[choix[1]-1].w, 64))
                    menu_touches.options[choix[1]-1].images[1].fill((255, 255, 255))
                    menu_touches.options[choix[1]-1].images[1].set_colorkey((255, 255, 255))
                    for i in range(len(menu_touches.options[choix[1]-1].message)):
                        menu_touches.options[choix[1]-1].images[0].blit(CARACTERES.subsurface(
                            ((ord(menu_touches.options[choix[1]-1].message[i]) % 10)*32,
                             (ord(menu_touches.options[choix[1]-1].message[i])//10)*64, 32, 64)), (32*i, 0))
                        menu_touches.options[choix[1]-1].images[1].blit(CARACTERES_SELECTIONNES.subsurface(
                            ((ord(menu_touches.options[choix[1]-1].message[i]) % 10)*32,
                             (ord(menu_touches.options[choix[1]-1].message[i])//10)*64, 32, 64)), (32*i, 0))

                    choix[1] = 0

            if entree.type == pygame.MOUSEMOTION:  # LES MOUVEMENTS DE SOURIS
                position_souris = [entree.pos[0], entree.pos[1]]

            if entree.type == pygame.MOUSEBUTTONUP:

                if entree.button == 1:  # LES CLIQUES

                    for i in range(len(menu.options)):  # LE MENU VALIDER/RETOUR
                        if menu.options[i].x+menu.options[i].w > entree.pos[0] > menu.options[i].x and \
                           menu.options[i].y+menu.options[i].h > entree.pos[1] > menu.options[i].y:
                            choix[0] = i+1

                    for i in range(len(menu_description.options)):  # LE MENU DE DESCRIPTION DES TOUCHES
                        if menu_description.options[i].x+menu_description.options[i].w > entree.pos[0] > menu_description.options[i].x and \
                           menu_description.options[i].y+menu_description.options[i].h > entree.pos[1] > menu_description.options[i].y and \
                           100 < entree.pos[0] < resolution.current_w-100 and 100 < entree.pos[1] < resolution.current_h-170:
                            choix[1] = i+1

                            # EFFACER LE CADRE

                            if liste_cadre[4] != 0:
                                if liste_cadre[1] < resolution.current_h-170 and liste_cadre[1]+liste_cadre[3] > 100:
                                    if liste_cadre[1]+liste_cadre[3] <= resolution.current_h-170 and liste_cadre[1] >= 100:
                                        liste_rafraichir.append([
                                            pygame.Surface((liste_cadre[2], liste_cadre[3])),
                                            (liste_cadre[0], liste_cadre[1], liste_cadre[2], liste_cadre[3]), 0])
                                    if liste_cadre[1]+liste_cadre[3] > resolution.current_h-170:
                                        liste_rafraichir.append([
                                            pygame.Surface((liste_cadre[2], resolution.current_h-170-liste_cadre[1])),
                                            (liste_cadre[0], liste_cadre[1], liste_cadre[2],
                                             resolution.current_h-170-liste_cadre[1]), 0])
                                    if liste_cadre[1] < 100:
                                        liste_rafraichir.append([
                                            pygame.Surface((liste_cadre[2], liste_cadre[3]-(100-liste_cadre[1]))),
                                            (liste_cadre[0], liste_cadre[1], liste_cadre[2], liste_cadre[3]), 0])

                            # CREER LES NOUVELLES COORDONNEES DU CADRE

                            liste_cadre[0] = menu_description.options[i].x-4
                            liste_cadre[1] = menu_description.options[i].y-4
                            liste_cadre[2] = menu_description.options[i].w+8
                            liste_cadre[3] = menu_description.options[i].h+8
                            liste_cadre[4] = pygame.Surface((liste_cadre[2], liste_cadre[3]))
                            liste_cadre[4].fill((255, 255, 0))
                            liste_cadre[4].fill((255, 255, 255), (2, 2, menu_description.options[i].w+4, menu_description.options[i].h+4))
                            liste_cadre[4].set_colorkey((255, 255, 255))

                if 4 <= entree.button <= 5:  # FAIRE DEFILER LE MENU
                    if (menu_description.options[len(menu_description.options)-1].y >= resolution.current_h-298 and
                       entree.button == 5) or (menu_description.options[0].y <= 164 and entree.button == 4):

                        # EFFACER LE MENU DE DESCRIPTIONS PUIS LE DEPLACER

                        for i in range(len(menu_description.options)):

                            if menu_description.options[i].y < resolution.current_h-170 and \
                               menu_description.options[i].y+menu_description.options[i].h > 100:

                                if menu_description.options[i].y+menu_description.options[i].h <= resolution.current_h-170 and \
                                   menu_description.options[i].y >= 100:
                                    liste_rafraichir.append(
                                        [pygame.Surface((menu_description.options[i].w, menu_description.options[i].h)),
                                         (menu_description.options[i].x, menu_description.options[i].y,
                                          menu_description.options[i].w, menu_description.options[i].h), 7])

                                if menu_description.options[i].y+menu_description.options[i].h > resolution.current_h-170:
                                    liste_rafraichir.append([pygame.Surface(
                                        (menu_description.options[i].w, resolution.current_h-170-menu_description.options[i].y)),
                                        (menu_description.options[i].x, menu_description.options[i].y,
                                         menu_description.options[i].w, resolution.current_h-170-menu_description.options[i].y), 7])

                                if menu_description.options[i].y < 100:
                                    liste_rafraichir.append([pygame.Surface(
                                        (menu_description.options[i].w, menu_description.options[i].h-(100-menu_description.options[i].y))),
                                        (menu_description.options[i].x, 100, menu_description.options[i].w,
                                         menu_description.options[i].h-(100-menu_description.options[i].y)), 7])

                            if entree.button == 5:
                                menu_description.options[i].y -= 30
                            if entree.button == 4:
                                menu_description.options[i].y += 30

                        # EFFACER LA LISTE DES TOUCHES PUIS LA DEPLACER

                        for i in range(len(menu_touches.options)):

                            if menu_touches.options[i].y < resolution.current_h-170 and \
                               menu_touches.options[i].y+menu_touches.options[i].h > 100:

                                if menu_touches.options[i].y+menu_touches.options[i].h <= resolution.current_h-170 and \
                                   menu_touches.options[i].y >= 100:
                                    liste_rafraichir.append(
                                        [pygame.Surface((menu_touches.options[i].w, menu_touches.options[i].h)),
                                         (menu_touches.options[i].x, menu_touches.options[i].y,
                                          menu_touches.options[i].w, menu_touches.options[i].h), 7])

                                if menu_touches.options[i].y+menu_touches.options[i].h > resolution.current_h-170:
                                    liste_rafraichir.append([pygame.Surface(
                                        (menu_touches.options[i].w, resolution.current_h-170-menu_touches.options[i].y)),
                                        (menu_touches.options[i].x, menu_touches.options[i].y,
                                         menu_touches.options[i].w, resolution.current_h-170-menu_touches.options[i].y), 7])

                                if menu_touches.options[i].y < 100:
                                    liste_rafraichir.append([pygame.Surface(
                                        (menu_touches.options[i].w, menu_touches.options[i].h-(100-menu_touches.options[i].y))),
                                        (menu_touches.options[i].x, 100, menu_touches.options[i].w,
                                         menu_touches.options[i].h-(100-menu_touches.options[i].y)), 7])

                            if entree.button == 5:
                                menu_touches.options[i].y -= 30
                            if entree.button == 4:
                                menu_touches.options[i].y += 30

                        # EFFACER LE CADRE PUIS LE DEPLACER

                        if liste_cadre[4] != 0:
                            if liste_cadre[1] < resolution.current_h-170 and liste_cadre[1]+liste_cadre[3] > 100:
                                if liste_cadre[1]+liste_cadre[3] <= resolution.current_h-170 and liste_cadre[1] >= 100:
                                    liste_rafraichir.append([
                                        pygame.Surface((liste_cadre[2], liste_cadre[3])),
                                        (liste_cadre[0], liste_cadre[1], liste_cadre[2], liste_cadre[3]), 0])
                                if liste_cadre[1]+liste_cadre[3] > resolution.current_h-170:
                                    liste_rafraichir.append([
                                        pygame.Surface((liste_cadre[2], resolution.current_h-170-liste_cadre[1])),
                                        (liste_cadre[0], liste_cadre[1], liste_cadre[2],
                                         resolution.current_h-170-liste_cadre[1]), 0])
                                if liste_cadre[1] < 100:
                                    liste_rafraichir.append([
                                        pygame.Surface((liste_cadre[2], liste_cadre[3]-(100-liste_cadre[1]))),
                                        (liste_cadre[0], liste_cadre[1], liste_cadre[2], liste_cadre[3]), 0])

                            if entree.button == 5:
                                liste_cadre[1] -= 30
                            if entree.button == 4:
                                liste_cadre[1] += 30

        # AFFICHER LE MENU VALIDER/RETOUR

        for i in range(len(menu.options)):
            if menu.options[i].x+menu.options[i].w > position_souris[0] > menu.options[i].x and \
               menu.options[i].y+menu.options[i].h > position_souris[1] > menu.options[i].y:
                liste_rafraichir.append([menu.options[i].images[1],
                                         (menu.options[i].x, menu.options[i].y,
                                          menu.options[i].w, menu.options[i].h), 7])
            else:
                liste_rafraichir.append([menu.options[i].images[0],
                                         (menu.options[i].x, menu.options[i].y,
                                          menu.options[i].w, menu.options[i].h), 7])

        # AFFICHER LA LISTE DES TOUCHES

        for i in range(len(menu_touches.options)):
            if menu_touches.options[i].y < resolution.current_h-170 and \
               menu_touches.options[i].y+menu_touches.options[i].h > 100:

                if menu_touches.options[i].y+menu_touches.options[i].h <= resolution.current_h-170 and \
                   menu_touches.options[i].y >= 100:
                    liste_rafraichir.append([menu_touches.options[i].images[0],
                                             (menu_touches.options[i].x, menu_touches.options[i].y,
                                              menu_touches.options[i].w, menu_touches.options[i].h), 7])

                if menu_touches.options[i].y+menu_touches.options[i].h > resolution.current_h-170:
                    liste_rafraichir.append([menu_touches.options[i].images[0].subsurface(
                        (0, 0, menu_touches.options[i].w, resolution.current_h-170-menu_touches.options[i].y)),
                        (menu_touches.options[i].x, menu_touches.options[i].y,
                         menu_touches.options[i].w, resolution.current_h-170-menu_touches.options[i].y), 7])

                if menu_touches.options[i].y < 100:
                    liste_rafraichir.append([menu_touches.options[i].images[0].subsurface(
                        (0, 100-menu_touches.options[i].y, menu_touches.options[i].w,
                         menu_touches.options[i].h-(100-menu_touches.options[i].y))),
                        (menu_touches.options[i].x, 100, menu_touches.options[i].w,
                         menu_touches.options[i].h-(100-menu_touches.options[i].y)), 7])

        # AFFICHER LE MENU DE DESCRIPTION DES TOUCHES

        for i in range(len(menu_description.options)):
            if menu_description.options[i].y < resolution.current_h-170 and \
               menu_description.options[i].y+menu_description.options[i].h > 100:

                # SI LA DESCRIPTION EST ENTIERE

                if menu_description.options[i].y+menu_description.options[i].h <= resolution.current_h-170 and \
                   menu_description.options[i].y >= 100:

                    if menu_description.options[i].x+menu_description.options[i].w > position_souris[0] > menu_description.options[i].x and \
                       menu_description.options[i].y+menu_description.options[i].h > position_souris[1] > menu_description.options[i].y and \
                       100 < position_souris[0] < resolution.current_w-100 and 100 < position_souris[1] < resolution.current_h-170:
                        liste_rafraichir.append([menu_description.options[i].images[1],
                                                 (menu_description.options[i].x, menu_description.options[i].y,
                                                  menu_description.options[i].w, menu_description.options[i].h), 7])
                    else:
                        liste_rafraichir.append([menu_description.options[i].images[0],
                                                 (menu_description.options[i].x, menu_description.options[i].y,
                                                  menu_description.options[i].w, menu_description.options[i].h), 7])

                # SI LA DESCRIPTION EST TROP BASSE

                if menu_description.options[i].y+menu_description.options[i].h > resolution.current_h-170:

                    if menu_description.options[i].x+menu_description.options[i].w > position_souris[0] > menu_description.options[i].x and \
                       menu_description.options[i].y+menu_description.options[i].h > position_souris[1] > menu_description.options[i].y and \
                       100 < position_souris[0] < resolution.current_w-100 and 100 < position_souris[1] < resolution.current_h-170:
                        liste_rafraichir.append([menu_description.options[i].images[1].subsurface(
                            (0, 0, menu_description.options[i].w, resolution.current_h-170-menu_description.options[i].y)),
                            (menu_description.options[i].x, menu_description.options[i].y,
                             menu_description.options[i].w, menu_description.options[i].h), 7])
                    else:
                        liste_rafraichir.append([menu_description.options[i].images[0].subsurface(
                            (0, 0, menu_description.options[i].w, resolution.current_h-170-menu_description.options[i].y)),
                            (menu_description.options[i].x, menu_description.options[i].y,
                             menu_description.options[i].w, resolution.current_h-170-menu_description.options[i].y), 7])

                # SI LA DESCRIPTION EST TROP HAUTE

                if menu_touches.options[i].y < 100:

                    if menu_description.options[i].x+menu_description.options[i].w > position_souris[0] > menu_description.options[i].x and \
                       menu_description.options[i].y+menu_description.options[i].h > position_souris[1] > menu_description.options[i].y and \
                       100 < position_souris[0] < resolution.current_w-100 and 100 < position_souris[1] < resolution.current_h-170:
                        liste_rafraichir.append([menu_description.options[i].images[1].subsurface(
                            (0, 100-menu_description.options[i].y, menu_description.options[i].w,
                             menu_description.options[i].y+menu_description.options[i].h-100)),
                            (menu_description.options[i].x, 100, menu_description.options[i].w,
                             menu_description.options[i].y+menu_description.options[i].h-100), 7])
                    else:
                        liste_rafraichir.append([menu_description.options[i].images[0].subsurface(
                            (0, 100-menu_description.options[i].y, menu_description.options[i].w,
                             menu_description.options[i].y+menu_description.options[i].h-100)),
                            (menu_description.options[i].x, 100, menu_description.options[i].w,
                             menu_description.options[i].y+menu_description.options[i].h-100), 7])

        # AFFICHER LE CADRE

        if choix[1] != 0:
            if liste_cadre[1] < resolution.current_h-170 and liste_cadre[1]+liste_cadre[3] > 100:
                if liste_cadre[1]+liste_cadre[3] < resolution.current_h-170 and liste_cadre[1] > 100:
                    liste_rafraichir.append([liste_cadre[4],
                                             (liste_cadre[0], liste_cadre[1], liste_cadre[2], liste_cadre[3]), 7])
                if liste_cadre[1]+liste_cadre[3] > resolution.current_h-170:
                    liste_rafraichir.append(
                        [liste_cadre[4].subsurface((0, 0, liste_cadre[2], resolution.current_h-170-liste_cadre[1])),
                         (liste_cadre[0], liste_cadre[1], liste_cadre[2], resolution.current_h-170-liste_cadre[1]), 7])
                if liste_cadre[1] < 100:
                    liste_rafraichir.append([liste_cadre[4].subsurface(
                        (0, 100-liste_cadre[1], liste_cadre[2], liste_cadre[3]-(100-liste_cadre[1]))),
                        (liste_cadre[0], liste_cadre[1], liste_cadre[2], liste_cadre[3]), 7])

        # GERER LES CHOIX

        if choix[0] == 1:  # VALIDER
            with open("raccourcis.txt", "w+") as fichier_raccourcis:
                chaine = []
                for raccourci in raccourcis_copie:
                    raccourci[0] = str(raccourci[0])
                    chaine.append("=".join(raccourci))
                chaine = "\n".join(chaine)
                fichier_raccourcis.write(chaine)
                continuer = False

            with open("raccourcis.txt", "r") as fichier_raccourcis:
                raccourcis = fichier_raccourcis.read().split("\n")
            for i in range(len(raccourcis)):
                raccourcis[i] = raccourcis[i].split("=")
                raccourcis[i][0] = int(raccourcis[i][0])

        if choix[0] == 2:  # RETOUR
            continuer = False

    return raccourcis
