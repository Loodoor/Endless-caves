# -*- coding:utf_8 -*

import os
import pickle
import time
from math import acos, degrees
from random import randrange
from classes import *

VERSION = "0.3.0"

FOND = pygame.image.load("images/fond.bmp")
TILESET = pygame.image.load("images/tileset.bmp")
PERSONNAGES = pygame.image.load("images/personnages.bmp")
OBJETS = pygame.image.load("images/objets_communs.bmp")
OBJETS_RARES = pygame.image.load("images/objets_rares.bmp")
INTERFACE = pygame.image.load("images/interface.bmp")
CARACTERES = pygame.image.load("images/ascii.bmp")
CARACTERES_SELECTIONNES = pygame.image.load("images/ascii_selectionnee.bmp")
CARACTERES_32 = pygame.image.load("images/ascii_32.bmp")
CARACTERES_SELECTIONNES_32 = pygame.image.load("images/ascii_selectionnee_32.bmp")
CARACTERES_MINI = pygame.image.load("images/ascii_mini.bmp")
ATTAQUES_JOUEUR = pygame.image.load("images/attaques_joueur.bmp")
MINIMAP = pygame.image.load("images/minimap.bmp")
FOND_MENU_JEU = pygame.image.load("images/menu_jeu.bmp")
ICONES_COMPETENCES = pygame.image.load("images/competences.bmp")
ANIMATIONS_JOUEUR = pygame.image.load("images/animations_joueur.bmp")
ICONES_SORTS = pygame.image.load("images/icones_sorts.bmp")
ATTAQUES_MONSTRES = pygame.image.load("images/attaques_monstres.bmp")
MENU_INVENTAIRE = pygame.image.load("images/menu_inventaire.bmp")
ITEMS = pygame.image.load("images/items.bmp")

PERSONNAGES.set_colorkey((255, 255, 255))
OBJETS.set_colorkey((255, 255, 255))
OBJETS_RARES.set_colorkey((255, 255, 255))
INTERFACE.set_colorkey((255, 255, 255))
CARACTERES.set_colorkey((255, 255, 255))
CARACTERES_SELECTIONNES.set_colorkey((255, 255, 255))
CARACTERES_32.set_colorkey((255, 255, 255))
CARACTERES_SELECTIONNES_32.set_colorkey((255, 255, 255))
CARACTERES_MINI.set_colorkey((0, 0, 0))
ATTAQUES_JOUEUR.set_colorkey((255, 255, 255))
MINIMAP.set_colorkey((255, 255, 255))
FOND_MENU_JEU.set_colorkey((255, 255, 255))
ICONES_COMPETENCES.set_colorkey((255, 255, 255))
ANIMATIONS_JOUEUR.set_colorkey((255, 255, 255))
ICONES_SORTS.set_colorkey((255, 255, 255))
ATTAQUES_MONSTRES.set_colorkey((255, 255, 255))
MENU_INVENTAIRE.set_colorkey((255, 255, 255))
ITEMS.set_colorkey((255, 255, 255))


def placer_salles(niveau):

    # OBTENIR LE NOMBRE DE SALLES

    nombre_de_salles_normales_ou_tresor = randrange(8+niveau, 10+(2*niveau))
    if nombre_de_salles_normales_ou_tresor > 150:
        nombre_de_salles_normales_ou_tresor = 150

    if nombre_de_salles_normales_ou_tresor//10 != 0:
        nombre_de_salles_verouillees = randrange(niveau, niveau+(nombre_de_salles_normales_ou_tresor//10))
    else:
        nombre_de_salles_verouillees = niveau
    if nombre_de_salles_verouillees > 20:
        nombre_de_salles_verouillees = 20

    nombre_de_salles_total = nombre_de_salles_normales_ou_tresor+nombre_de_salles_verouillees+2
    # salles_verouillees + salles_normales_&_tresor + spawn + salle_de_boss

    # CREER UN TABLEAU QUI SERVIRA DE CARTE DE L'ETAGE

    tableau = list()
    for i in range(nombre_de_salles_normales_ou_tresor):
        tableau.append(list())
        for j in range(nombre_de_salles_normales_ou_tresor):
            tableau[i].append(0)

    # PLACER LE SPAWN

    tableau[len(tableau)//2][len(tableau)//2] = 2

    # PLACER LES SALLES NORMALES / TRESOR

    for i in range(nombre_de_salles_normales_ou_tresor):
        type = randrange(15)
        x, y = 1, 1
        while not((tableau[y][x] == 0 and tableau[y+1][x] != 0) or
                  (tableau[y][x] == 0 and tableau[y-1][x] != 0) or
                  (tableau[y][x] == 0 and tableau[y][x+1] != 0) or
                  (tableau[y][x] == 0 and tableau[y][x-1] != 0)):
            x = randrange(1, len(tableau)-2)
            y = randrange(1, len(tableau)-2)
        if type == 0:
            tableau[y][x] = 3
        else:
            tableau[y][x] = 1

    # PLACER LA SALLE DE BOSS

    x, y = 1, 1
    while not ((tableau[y][x] == 0 and tableau[y+1][x] != 0) or
               (tableau[y][x] == 0 and tableau[y-1][x] != 0) or
               (tableau[y][x] == 0 and tableau[y][x+1] != 0) or
               (tableau[y][x] == 0 and tableau[y][x-1] != 0)):
        x = randrange(1, len(tableau)-2)
        y = randrange(1, len(tableau)-2)
    tableau[y][x] = 4

    # PLACER LES SALLES VEROUILLEES

    for i in range(nombre_de_salles_verouillees):
        x, y = 1, 1
        while not ((tableau[y][x] == 0 and tableau[y+1][x] != 0 and tableau[y+1][x] != 5) or
                  (tableau[y][x] == 0 and tableau[y-1][x] != 0 and tableau[y-1][x] != 5) or
                  (tableau[y][x] == 0 and tableau[y][x+1] != 0 and tableau[y][x+1] != 5) or
                  (tableau[y][x] == 0 and tableau[y][x-1] != 0 and tableau[y][x-1] != 5)):
            x = randrange(1, len(tableau)-2)
            y = randrange(1, len(tableau)-2)
        tableau[y][x] = 5

    # CREER LA VARIABLE ETAGE ET LA REMPLIR

    etage = Map(nombre_de_salles_total)

    etage.salles = list()
    for i in range(etage.nombre_de_salles):
        etage.salles.append(Salle())

    etage.carte_map = list()
    for i in range(len(tableau)):
        etage.carte_map.append(list())
        for j in range(len(tableau[i])):
            etage.carte_map[i].append(tableau[i][j])

    etage.niveau = niveau

    i = 0
    for y in range(len(etage.carte_map)):
        for x in range(len(etage.carte_map[y])):
            if etage.carte_map[y][x] != 0:
                etage.salles[i].type_salle = etage.carte_map[y][x]
                etage.salles[i].x = x
                etage.salles[i].y = y
                i += 1

    return etage


def generer_salles(etage):

    fichier = open("patterns.txt", "r")  # RECUPERATION DES PATTERNS DE SALLES

    chaine_obtenue = fichier.read()
    liste_paternes = chaine_obtenue.split("\n")

    for i in range(len(liste_paternes)):
        liste_paternes[i] = liste_paternes[i].split(" ")

    # GENERATION DE L'INTERIEUR DES SALLES

    for i in range(etage.nombre_de_salles):

        if etage.salles[i].type_salle == 1:  # REMPLIR LES SALLES NORMALES
            a = randrange(int(len(liste_paternes)/10))

            chaine_obtenue = ""
            j = 0
            while chaine_obtenue != [str(a)]:
                chaine_obtenue = liste_paternes[j]
                j += 1

            while liste_paternes[j] != [str(a+1)]:
                for l in range(9):
                    etage.salles[i].blocs_type.append(list(liste_paternes[j]))
                    j += 1

            h = 0
            g = 0
            for j in range(9):  # AJOUTER LES OBJETS ET MONSTRES POTENTIELS A PARTIR DES PATTERNS

                for k in range(15):

                    if etage.salles[i].blocs_type[j][k] == "1001":

                        etage.salles[i].blocs_type[j][k] = 1
                        etage.salles[i].objets_potentiels.append(Objet())
                        etage.salles[i].objets_potentiels[h].x = k*64
                        etage.salles[i].objets_potentiels[h].y = j*64
                        h += 1

                    elif etage.salles[i].blocs_type[j][k] == "2000":

                        etage.salles[i].blocs_type[j][k] = 0
                        etage.salles[i].ennemis_potentiels.append(Ennemis())
                        etage.salles[i].ennemis_potentiels[g].x = k*64
                        etage.salles[i].ennemis_potentiels[g].y = j*64
                        g += 1

        elif etage.salles[i].type_salle == 2 or \
                etage.salles[i].type_salle == 3 or \
                etage.salles[i].type_salle == 5:  # REMPLIR LES SALLES DE SPAWN/DE TRESOR/VEROUILLEES

            etage.salles[i].blocs_type = \
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

        elif etage.salles[i].type_salle == 4:  # REMPLIR LES SALLES FINALES

            etage.salles[i].blocs_type = \
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

        for j in range(etage.nombre_de_salles):

                # LES PORTES NORMALES

                if etage.salles[i].x+1 == etage.salles[j].x and \
                   etage.salles[i].y == etage.salles[j].y and \
                   etage.salles[j].type_salle != 5:
                    etage.salles[i].blocs_type[4][14] = 6

                if etage.salles[i].x-1 == etage.salles[j].x and \
                   etage.salles[i].y == etage.salles[j].y and \
                   etage.salles[j].type_salle != 5:
                    etage.salles[i].blocs_type[4][0] = 7

                if etage.salles[i].y+1 == etage.salles[j].y and \
                   etage.salles[i].x == etage.salles[j].x and \
                   etage.salles[j].type_salle != 5:
                    etage.salles[i].blocs_type[8][7] = 5

                if etage.salles[i].y-1 == etage.salles[j].y and \
                   etage.salles[i].x == etage.salles[j].x and \
                   etage.salles[j].type_salle != 5:
                    etage.salles[i].blocs_type[0][7] = 4

                # LES PORTES VEROUILLEES

                if etage.salles[i].x+1 == etage.salles[j].x and \
                   etage.salles[i].y == etage.salles[j].y and \
                   etage.salles[j].type_salle == 5:
                    etage.salles[i].blocs_type[4][14] = 20

                if etage.salles[i].x-1 == etage.salles[j].x and \
                   etage.salles[i].y == etage.salles[j].y and \
                   etage.salles[j].type_salle == 5:
                    etage.salles[i].blocs_type[4][0] = 21

                if etage.salles[i].y+1 == etage.salles[j].y and \
                   etage.salles[i].x == etage.salles[j].x and \
                   etage.salles[j].type_salle == 5:
                    etage.salles[i].blocs_type[8][7] = 19

                if etage.salles[i].y-1 == etage.salles[j].y and \
                   etage.salles[i].x == etage.salles[j].x and \
                   etage.salles[j].type_salle == 5:
                    etage.salles[i].blocs_type[0][7] = 18

        etage.salles[i].visited = False

    return etage


def generer_images_salles(etage, i):

    global TILESET
    etage.salles[i].image = pygame.Surface((960, 576))

    for j in range(9):
        for h in range(15):
            etage.salles[i].blocs_type[j][h] = int(etage.salles[i].blocs_type[j][h])
            etage.salles[i].image.blit(TILESET.subsurface((etage.salles[i].blocs_type[j][h] % 10)*64,
                                                        (etage.salles[i].blocs_type[j][h]//10)*64, 64, 64),
                                     (h*64, j*64))

    return etage


def generer_hitboxs(etage, i):

    for y in range(9):

        etage.salles[i].blocs_hitboxs.append([])
        for x in range(15):

            etage.salles[i].blocs_hitboxs[y].append(Hitbox())
            etage.salles[i].blocs_hitboxs[y][x].x = x*64
            etage.salles[i].blocs_hitboxs[y][x].y = y*64
            etage.salles[i].blocs_hitboxs[y][x].w = 64
            etage.salles[i].blocs_hitboxs[y][x].h = 64

    return etage


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


def initialiser_joueur(etage, joueur):

    # PLACER LE JOUEUR DANS LA SALLE ACTUELLE

    if joueur.salle == -1:  # SI LE JOUEUR COMMENCE UN NOUVEL ETAGE
        joueur.x = 448
        joueur.y = 256
        i = 0
        while etage.salles[i].type_salle != 2:
            i += 1
        joueur.salle = i
    else:  # POUR PASSER D'UNE SALLE A L'AUTRE
        i = 0
        if joueur.x >= 832:
            joueur.x = 64
            joueur.y = 256
            while etage.salles[joueur.salle].x != (etage.salles[i].x-1) or etage.salles[joueur.salle].y != etage.salles[i].y:
                i += 1
        elif joueur.x < 128:
            joueur.x = 832
            joueur.y = 256
            while etage.salles[joueur.salle].x != (etage.salles[i].x+1) or etage.salles[joueur.salle].y != etage.salles[i].y:
                i += 1
        elif joueur.y >= 448:
            joueur.x = 448
            joueur.y = 64
            while etage.salles[joueur.salle].y != (etage.salles[i].y-1) or etage.salles[joueur.salle].x != etage.salles[i].x:
                i += 1
        elif joueur.y < 128:
            joueur.x = 448
            joueur.y = 448
            while etage.salles[joueur.salle].y != (etage.salles[i].y+1) or etage.salles[joueur.salle].x != etage.salles[i].x:
                i += 1

        joueur.salle = i

    return joueur


def initialiser_ennemis(etage, joueur):

    if not etage.salles[joueur.salle].visited:

        if etage.salles[joueur.salle].type_salle == 1:  # GENERATION D'ENNEMIS POUR LES SALLES NORMALES

            global PERSONNAGES

            if randrange(2) == 0:  # UNE CHANCE SUR DEUX D'AVOIR DES ENNEMIS

                for i in range(randrange(len(etage.salles[joueur.salle].ennemis_potentiels))):
                    etage.salles[joueur.salle].ennemis.append(Ennemis())

                    etage.salles[joueur.salle].ennemis[i].x = etage.salles[joueur.salle].ennemis_potentiels[i].x
                    etage.salles[joueur.salle].ennemis[i].y = etage.salles[joueur.salle].ennemis_potentiels[i].y

                    etage.salles[joueur.salle].ennemis[i].type = randrange((PERSONNAGES.get_size()[1]//64)-1)

                    etage.salles[joueur.salle].ennemis[i].attaque = 10+(etage.niveau*etage.niveau)\
                        - ((etage.niveau*randrange(etage.niveau))//2)
                    etage.salles[joueur.salle].ennemis[i].points_de_vies_maximum = etage.salles[joueur.salle].ennemis[i].attaque*10
                    etage.salles[joueur.salle].ennemis[i].points_de_vies = etage.salles[joueur.salle].ennemis[i].points_de_vies_maximum

                    etage.salles[joueur.salle].ennemis[i].hitbox_degats.x = etage.salles[joueur.salle].ennemis[i].x
                    etage.salles[joueur.salle].ennemis[i].hitbox_degats.y = etage.salles[joueur.salle].ennemis[i].y
                    etage.salles[joueur.salle].ennemis[i].hitbox_degats.w = 64
                    etage.salles[joueur.salle].ennemis[i].hitbox_degats.h = 64
                    etage.salles[joueur.salle].ennemis[i].hitbox_deplacement.x = etage.salles[joueur.salle].ennemis[i].x+16
                    etage.salles[joueur.salle].ennemis[i].hitbox_deplacement.y = etage.salles[joueur.salle].ennemis[i].y+16
                    etage.salles[joueur.salle].ennemis[i].hitbox_deplacement.w = 32
                    etage.salles[joueur.salle].ennemis[i].hitbox_deplacement.h = 48

                    etage.salles[joueur.salle].ennemis[i].mort = False

                    etage.salles[joueur.salle].ennemis[i].minibarre = Minibarre()
                    etage.salles[joueur.salle].ennemis[i].minibarre.x = etage.salles[joueur.salle].ennemis[i].x
                    etage.salles[joueur.salle].ennemis[i].minibarre.y = etage.salles[joueur.salle].ennemis[i].y+66
                    etage.salles[joueur.salle].ennemis[i].minibarre.w = 64
                    etage.salles[joueur.salle].ennemis[i].minibarre.h = 8
                    etage.salles[joueur.salle].ennemis[i].minibarre.image = pygame.Surface((64, 8))
                    etage.salles[joueur.salle].ennemis[i].minibarre.image.fill((0, 0, 0))
                    etage.salles[joueur.salle].ennemis[i].minibarre.image.set_colorkey((255, 255, 255))

                    for l in range(6):
                        etage.salles[joueur.salle].ennemis[i].images.bas.append(
                            PERSONNAGES.subsurface((l*64, (etage.salles[joueur.salle].ennemis[i].type+1)*64, 64, 64)))
                        etage.salles[joueur.salle].ennemis[i].images.haut.append(
                            PERSONNAGES.subsurface(((l+6)*64, (etage.salles[joueur.salle].ennemis[i].type+1)*64, 64, 64)))
                        etage.salles[joueur.salle].ennemis[i].images.droite.append(
                            PERSONNAGES.subsurface(((l+12)*64, (etage.salles[joueur.salle].ennemis[i].type+1)*64, 64, 64)))
                        etage.salles[joueur.salle].ennemis[i].images.gauche.append(
                            PERSONNAGES.subsurface(((l+18)*64, (etage.salles[joueur.salle].ennemis[i].type+1)*64, 64, 64)))
                        etage.salles[joueur.salle].ennemis[i].images.bas[l].set_colorkey((255, 255, 255))
                        etage.salles[joueur.salle].ennemis[i].images.haut[l].set_colorkey((255, 255, 255))
                        etage.salles[joueur.salle].ennemis[i].images.droite[l].set_colorkey((255, 255, 255))
                        etage.salles[joueur.salle].ennemis[i].images.gauche[l].set_colorkey((255, 255, 255))

                    etage.salles[joueur.salle].ennemis[i].images.bas.append(
                        PERSONNAGES.subsurface((1536, (etage.salles[joueur.salle].ennemis[i].type+1)*64, 64, 64)))
                    etage.salles[joueur.salle].ennemis[i].images.bas[6].set_colorkey((255, 255, 255))
    return etage


def initialiser_objets(etage, joueur):

    if not etage.salles[joueur.salle].visited:

        # GENERATION D'OBJETS DANS LES SALLES NORMALES

        if etage.salles[joueur.salle].type_salle == 1:

            global OBJETS

            compteur = 0
            for i in range(len(etage.salles[joueur.salle].objets_potentiels)):

                if randrange(3) == 0:  # LA PROBABILITE D'AVOIR LE Xeme OBJET = 1/(3*X)

                    n = randrange(len(etage.salles[joueur.salle].objets_potentiels))
                    etage.salles[joueur.salle].objets.append(Objet())
                    etage.salles[joueur.salle].objets[compteur].x = etage.salles[joueur.salle].objets_potentiels[n].x
                    etage.salles[joueur.salle].objets[compteur].y = etage.salles[joueur.salle].objets_potentiels[n].y
                    etage.salles[joueur.salle].objets[compteur].hitbox.x = etage.salles[joueur.salle].objets[compteur].x
                    etage.salles[joueur.salle].objets[compteur].hitbox.y = etage.salles[joueur.salle].objets[compteur].y
                    etage.salles[joueur.salle].objets[compteur].hitbox.w = 64
                    etage.salles[joueur.salle].objets[compteur].hitbox.h = 64
                    etage.salles[joueur.salle].blocs_type[etage.salles[joueur.salle].objets[compteur].y//64][etage.salles[joueur.salle].objets[compteur].x//64] = 0

                    type = randrange(100)  # CHOISIR L'OBJET
                    if type < 25:
                        etage.salles[joueur.salle].objets[compteur].type = 0
                    elif 50 > type >= 25:
                        etage.salles[joueur.salle].objets[compteur].type = 2
                    elif 75 > type >= 50:
                        etage.salles[joueur.salle].objets[compteur].type = 4
                    elif 85 > type >= 75:
                        etage.salles[joueur.salle].objets[compteur].type = 1
                    elif 92 > type >= 85:
                        etage.salles[joueur.salle].objets[compteur].type = 3
                    elif 97 > type >= 92:
                        etage.salles[joueur.salle].objets[compteur].type = 5
                    elif 100 > type >= 97:
                        etage.salles[joueur.salle].objets[compteur].type = 6

                    etage.salles[joueur.salle].objets[compteur].image = \
                        OBJETS.subsurface(((etage.salles[joueur.salle].objets[compteur].type % 10)*64,
                                           (etage.salles[joueur.salle].objets[compteur].type//10)*64, 64, 64))
                    etage.salles[joueur.salle].objets[compteur].image.set_colorkey((255, 255, 255))

                    del etage.salles[joueur.salle].objets_potentiels[n]
                    compteur += 1
                else:
                    break

        # GENERATION D'UN OBJET RARE DANS LES SALLES VEROUILLEES/SALLES DE TRESOR

        elif etage.salles[joueur.salle].type_salle == 3 or etage.salles[joueur.salle].type_salle == 5:

            global OBJETS_RARES

            objet = Objet()
            objet.x = 448
            objet.y = 256
            objet.type = 1000+randrange(10)
            objet.image = OBJETS_RARES.subsurface((((objet.type-1000) % 10)*64, ((objet.type-1000)//10)*64, 64, 64))
            objet.image.set_colorkey((255, 255, 255))
            objet.hitbox.x = 448
            objet.hitbox.y = 256
            objet.hitbox.w = 64
            objet.hitbox.h = 64
            etage.salles[joueur.salle].objets.append(objet)
            etage.salles[joueur.salle].blocs_type[etage.salles[joueur.salle].objets[0].y//64][etage.salles[joueur.salle].objets[0].x//64] = 0

    return etage


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


def gerer_portes(etage, joueur, liste_rafraichir, position_ecran_x, position_ecran_y):

    global TILESET

    # OUVRIR LES PORTES NORMALES ET LES TRAPES

    if len(etage.salles[joueur.salle].ennemis) == 0 and not etage.salles[joueur.salle].visited:
        etage.salles[joueur.salle].visited = True

        if etage.salles[joueur.salle].blocs_type[0][7] == 4:
            etage.salles[joueur.salle].blocs_type[0][7] = 14
            etage.salles[joueur.salle].image.blit(TILESET.subsurface((256, 64, 64, 64)), (448, 0))
            liste_rafraichir.append([etage.salles[joueur.salle].image.subsurface((448, 0, 64, 64)),
                                     (448+position_ecran_x, position_ecran_y, 64, 64), 0])

        if etage.salles[joueur.salle].blocs_type[4][0] == 7:
            etage.salles[joueur.salle].blocs_type[4][0] = 17
            etage.salles[joueur.salle].image.blit(TILESET.subsurface((448, 64, 64, 64)), (0, 256))
            liste_rafraichir.append([etage.salles[joueur.salle].image.subsurface((0, 256, 64, 64)),
                                     (position_ecran_x, 256+position_ecran_y, 64, 64), 0])

        if etage.salles[joueur.salle].blocs_type[8][7] == 5:
            etage.salles[joueur.salle].blocs_type[8][7] = 15
            etage.salles[joueur.salle].image.blit(TILESET.subsurface((320, 64, 64, 64)), (448, 512))
            liste_rafraichir.append([etage.salles[joueur.salle].image.subsurface((448, 512, 64, 64)),
                                     (448+position_ecran_x, 512+position_ecran_y, 64, 64), 0])

        if etage.salles[joueur.salle].blocs_type[4][14] == 6:
            etage.salles[joueur.salle].blocs_type[4][14] = 16
            etage.salles[joueur.salle].image.blit(TILESET.subsurface((384, 64, 64, 64)), (896, 256))
            liste_rafraichir.append([etage.salles[joueur.salle].image.subsurface((896, 256, 64, 64)),
                                     (896+position_ecran_x, 256+position_ecran_y, 64, 64), 0])

        if etage.salles[joueur.salle].type_salle == 4:
            etage.salles[joueur.salle].blocs_type[4][7] = 13
            etage.salles[joueur.salle].image.blit(TILESET.subsurface((192, 64, 64, 64)), (448, 256))
            liste_rafraichir.append([etage.salles[joueur.salle].image.subsurface((448, 256, 64, 64)),
                                     (448+position_ecran_x, 256+position_ecran_y, 64, 64), 0])

    # OUVRIR LES PORTES VEROUILLEES

    if len(etage.salles[joueur.salle].ennemis) == 0 and \
       (etage.salles[joueur.salle].blocs_type[0][7] == 18 or
       etage.salles[joueur.salle].blocs_type[4][0] == 21 or
       etage.salles[joueur.salle].blocs_type[8][7] == 19 or
       etage.salles[joueur.salle].blocs_type[4][14] == 20):

        salle_ouverte = -1

        if etage.salles[joueur.salle].blocs_type[0][7] == 18 and \
           496 > joueur.x > 432 and \
           joueur.y == 48 and \
           joueur.deplacement_y < 0 and \
           joueur.cles:
            liste_rafraichir, joueur =\
                rafraichir_cles(position_ecran_x, position_ecran_y, joueur, liste_rafraichir, joueur.cles-1)
            etage.salles[joueur.salle].blocs_type[0][7] = 14
            etage.salles[joueur.salle].image.blit(TILESET.subsurface((256, 64, 64, 64)), (448, 0))
            liste_rafraichir.append([etage.salles[joueur.salle].image.subsurface((448, 0, 64, 64)),
                                     (448+position_ecran_x, position_ecran_y, 64, 64), 0])

            for i in range(len(etage.salles)):
                if etage.salles[joueur.salle].x == etage.salles[i].x and \
                   etage.salles[joueur.salle].y == etage.salles[i].y+1:
                    salle_ouverte = i

        if etage.salles[joueur.salle].blocs_type[4][0] == 21 and \
           304 > joueur.y > 240 and \
           joueur.x == 48 and \
           joueur.deplacement_x < 0 and \
           joueur.cles:
            liste_rafraichir, joueur =\
                rafraichir_cles(position_ecran_x, position_ecran_y, joueur, liste_rafraichir, joueur.cles-1)
            etage.salles[joueur.salle].blocs_type[4][0] = 17
            etage.salles[joueur.salle].image.blit(TILESET.subsurface((448, 64, 64, 64)), (0, 256))
            liste_rafraichir.append([etage.salles[joueur.salle].image.subsurface((0, 256, 64, 64)),
                                     (position_ecran_x, 256+position_ecran_y, 64, 64), 0])

            for i in range(len(etage.salles)):
                if etage.salles[joueur.salle].x == etage.salles[i].x+1 and \
                   etage.salles[joueur.salle].y == etage.salles[i].y:
                    salle_ouverte = i

        if etage.salles[joueur.salle].blocs_type[8][7] == 19 and \
           496 > joueur.x > 432 and \
           joueur.y == 448 and \
           joueur.deplacement_y > 0 and \
           joueur.cles:
            liste_rafraichir, joueur =\
                rafraichir_cles(position_ecran_x, position_ecran_y, joueur, liste_rafraichir, joueur.cles-1)
            etage.salles[joueur.salle].blocs_type[8][7] = 15
            etage.salles[joueur.salle].image.blit(TILESET.subsurface((320, 64, 64, 64)), (448, 512))
            liste_rafraichir.append([etage.salles[joueur.salle].image.subsurface((448, 512, 64, 64)),
                                     (448+position_ecran_x, 512+position_ecran_y, 64, 64), 0])

            for i in range(len(etage.salles)):
                if etage.salles[joueur.salle].x == etage.salles[i].x and \
                   etage.salles[joueur.salle].y == etage.salles[i].y-1:
                    salle_ouverte = i

        if etage.salles[joueur.salle].blocs_type[4][14] == 20 and \
           joueur.x == 848 and \
           304 > joueur.y > 240 and \
           joueur.deplacement_x > 0 and \
           joueur.cles:
            liste_rafraichir, joueur =\
                rafraichir_cles(position_ecran_x, position_ecran_y, joueur, liste_rafraichir, joueur.cles-1)
            etage.salles[joueur.salle].blocs_type[4][14] = 16
            etage.salles[joueur.salle].image.blit(TILESET.subsurface((384, 64, 64, 64)), (896, 256))
            liste_rafraichir.append([etage.salles[joueur.salle].image.subsurface((896, 256, 64, 64)),
                                     (896+position_ecran_x, 256+position_ecran_y, 64, 64), 0])

            for i in range(len(etage.salles)):
                if etage.salles[joueur.salle].x == etage.salles[i].x-1 and \
                   etage.salles[joueur.salle].y == etage.salles[i].y:
                    salle_ouverte = i

        # TRANSFORMER TOUTES LES PORTES VEROUILLEES DE LA SALLE QUE L'ON VIENT DE DEBLOQUER

        if salle_ouverte != -1:
            for i in range(len(etage.salles)):
                if etage.salles[i].x == etage.salles[salle_ouverte].x and \
                   etage.salles[i].y == etage.salles[salle_ouverte].y-1 and \
                   i != joueur.salle:
                    if etage.salles[i].visited:
                        etage.salles[i].blocs_type[8][7] = 15
                    else:
                        etage.salles[i].blocs_type[8][7] = 5

                if etage.salles[i].x == etage.salles[salle_ouverte].x-1 and \
                   etage.salles[i].y == etage.salles[salle_ouverte].y and \
                   i != joueur.salle:
                    if etage.salles[i].visited:
                        etage.salles[i].blocs_type[4][14] = 16
                    else:
                        etage.salles[i].blocs_type[4][14] = 6

                if etage.salles[i].x == etage.salles[salle_ouverte].x and \
                   etage.salles[i].y == etage.salles[salle_ouverte].y+1 and \
                   i != joueur.salle:
                    if etage.salles[i].visited:
                        etage.salles[i].blocs_type[0][7] = 14
                    else:
                        etage.salles[i].blocs_type[0][7] = 4

                if etage.salles[i].x == etage.salles[salle_ouverte].x+1 and \
                   etage.salles[i].y == etage.salles[salle_ouverte].y and \
                   i != joueur.salle:
                    if etage.salles[i].visited:
                        etage.salles[i].blocs_type[4][0] = 17
                    else:
                        etage.salles[i].blocs_type[4][0] = 7

    return etage, liste_rafraichir, joueur


def gerer_fps(temps_actuel):

    temps_precedent = temps_actuel
    temps_actuel = pygame.time.get_ticks()

    print(temps_actuel-temps_precedent)

    if (temps_actuel-temps_precedent) < 35:
        pygame.time.wait(30-(temps_actuel-temps_precedent))
        temps_actuel = pygame.time.get_ticks()

    return temps_actuel


def afficher_objets(etage, liste_rafraichir, position_ecran_x, position_ecran_y, joueur):

    for i in range(len(etage.salles[joueur.salle].objets)):
        liste_rafraichir.append([etage.salles[joueur.salle].objets[i].image,
                                 (etage.salles[joueur.salle].objets[i].x+position_ecran_x,
                                  etage.salles[joueur.salle].objets[i].y+position_ecran_y, 64, 64), 1])

    return liste_rafraichir


def deplacer_personnage(etage, joueur, liste_rafraichir, tempo, position_ecran_x, position_ecran_y):

    # EFFACER IMAGE JOUEUR

    liste_rafraichir.append([etage.salles[joueur.salle].image.subsurface((joueur.x, joueur.y, 64, 64)),
                             (joueur.x+position_ecran_x, joueur.y+position_ecran_y, 64, 64), 0])

    # DEPLACER LE JOUEUR

    if joueur.deplacement_x != 0:  # DEPLACER SUR L'AXE DES X

        if joueur.sorts_actifs[1] and \
           joueur.sorts[1] == 8 or \
           joueur.sorts[1] == 10 or \
           joueur.sorts[1] == 13 or \
           joueur.sorts[1] == 14:
            if joueur.sorts_temps_activation[1] > pygame.time.get_ticks()-10000:
                joueur.x += int(1.5*joueur.deplacement_x)
            else:
                joueur.sorts_actifs[1] = False
                joueur.x += joueur.deplacement_x
        else:
            joueur.x += joueur.deplacement_x

        blocs_a_proximite = list()
        blocs_a_proximite.append([joueur.x//64, joueur.y//64])
        blocs_a_proximite.append([blocs_a_proximite[0][0]+1, blocs_a_proximite[0][1]])
        blocs_a_proximite.append([blocs_a_proximite[0][0], blocs_a_proximite[0][1]+1])
        blocs_a_proximite.append([blocs_a_proximite[0][0]+1, blocs_a_proximite[0][1]+1])

        joueur.hitbox.x = joueur.x+16
        joueur.hitbox.y = joueur.y+16

        for i in range(4):  # FAIRE RECULER LE JOUEUR DE 1 TANT QU'IL EST EN COLLISION AVEC LE DECORS

            while collisions(joueur.hitbox, etage.salles[joueur.salle].blocs_hitboxs[blocs_a_proximite[i][1]][blocs_a_proximite[i][0]]) and \
                (11 >= etage.salles[joueur.salle].blocs_type[blocs_a_proximite[i][1]][blocs_a_proximite[i][0]] >= 1 or
                 21 >= etage.salles[joueur.salle].blocs_type[blocs_a_proximite[i][1]][blocs_a_proximite[i][0]] >= 18):

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

        if joueur.sorts_actifs[1] and \
           joueur.sorts[1] == 8 or \
           joueur.sorts[1] == 10 or \
           joueur.sorts[1] == 13 or \
           joueur.sorts[1] == 14:
            if joueur.sorts_temps_activation[1] > pygame.time.get_ticks()-10000:
                joueur.y += int(1.5*joueur.deplacement_y)
            else:
                joueur.sorts_actifs[1] = False
                joueur.y += joueur.deplacement_y
        else:
            joueur.y += joueur.deplacement_y

        blocs_a_proximite = list()
        blocs_a_proximite.append([joueur.x//64, joueur.y//64])
        blocs_a_proximite.append([blocs_a_proximite[0][0]+1, blocs_a_proximite[0][1]])
        blocs_a_proximite.append([blocs_a_proximite[0][0], blocs_a_proximite[0][1]+1])
        blocs_a_proximite.append([blocs_a_proximite[0][0]+1, blocs_a_proximite[0][1]+1])

        joueur.hitbox.x = joueur.x+16
        joueur.hitbox.y = joueur.y+16

        for i in range(4):  # FAIRE RECULER LE JOUEUR DE 1 TANT QU'IL EST EN COLLISION AVEC LE DECORS

            while collisions(joueur.hitbox, etage.salles[joueur.salle].blocs_hitboxs[blocs_a_proximite[i][1]][blocs_a_proximite[i][0]]) and \
                (11 >= etage.salles[joueur.salle].blocs_type[blocs_a_proximite[i][1]][blocs_a_proximite[i][0]] >= 1 or
                 21 >= etage.salles[joueur.salle].blocs_type[blocs_a_proximite[i][1]][blocs_a_proximite[i][0]] >= 18):

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
    return (tempo+1) % 24


def ramasser_objets(etage, joueur, liste_rafraichir, position_ecran_x, position_ecran_y):

    global ANIMATIONS_JOUEUR

    # VERIFIER S'IL Y A COLLISION, REGARDER LE TYPE D'OBJET, AJOUTER LA STAT, ET SUPPRIMER L'OBJET

    i = 0
    while i < len(etage.salles[joueur.salle].objets):

        if collisions(joueur.hitbox, etage.salles[joueur.salle].objets[i].hitbox):

            # OBJETS COMMUNS

            if etage.salles[joueur.salle].objets[i].type == 0:
                liste_rafraichir, joueur = \
                    rafraichir_bombes(position_ecran_x, position_ecran_y, joueur, liste_rafraichir, joueur.bombes+1)

            if etage.salles[joueur.salle].objets[i].type == 1:
                liste_rafraichir, joueur = \
                    rafraichir_bombes(position_ecran_x, position_ecran_y, joueur, liste_rafraichir, joueur.bombes+3)

            if etage.salles[joueur.salle].objets[i].type == 2:
                liste_rafraichir, joueur = \
                    rafraichir_cles(position_ecran_x, position_ecran_y, joueur, liste_rafraichir, joueur.cles+1)

            if etage.salles[joueur.salle].objets[i].type == 3:
                liste_rafraichir, joueur = \
                    rafraichir_cles(position_ecran_x, position_ecran_y, joueur, liste_rafraichir, joueur.cles+3)

            if etage.salles[joueur.salle].objets[i].type == 4:
                liste_rafraichir, joueur = \
                    rafraichir_argent(position_ecran_x, position_ecran_y, joueur, liste_rafraichir, etage, joueur.argent+1)

            if etage.salles[joueur.salle].objets[i].type == 5:
                liste_rafraichir, joueur = \
                    rafraichir_argent(position_ecran_x, position_ecran_y, joueur, liste_rafraichir, etage, joueur.argent+5)

            if etage.salles[joueur.salle].objets[i].type == 6:
                liste_rafraichir, joueur = \
                    rafraichir_argent(position_ecran_x, position_ecran_y, joueur, liste_rafraichir, etage, joueur.argent+10)

            if etage.salles[joueur.salle].objets[i].type == 7:
                liste_rafraichir, joueur = rafraichir_vie(position_ecran_x, position_ecran_y, joueur, liste_rafraichir,
                                                          joueur.points_de_vies+10, joueur.vie_maximum)

            # OBJETS RARES

            if etage.salles[joueur.salle].objets[i].type == 1000:
                liste_rafraichir, joueur = \
                    rafraichir_bombes(position_ecran_x, position_ecran_y, joueur, liste_rafraichir, joueur.bombes+10)

            if etage.salles[joueur.salle].objets[i].type == 1001:
                liste_rafraichir, joueur = \
                    rafraichir_cles(position_ecran_x, position_ecran_y, joueur, liste_rafraichir, joueur.cles+10)

            if etage.salles[joueur.salle].objets[i].type == 1002:
                liste_rafraichir, joueur = \
                    rafraichir_argent(position_ecran_x, position_ecran_y, joueur, liste_rafraichir, etage, joueur.argent+50)

            if etage.salles[joueur.salle].objets[i].type == 1003:
                joueur.vitesse += 1
                if joueur.animation_tete.activee:
                    liste_rafraichir.append([etage.salles[joueur.salle].image.subsurface(
                        (joueur.animation_tete.x, joueur.animation_tete.y,
                         joueur.animation_tete.w, joueur.animation_tete.h)),
                        (joueur.animation_tete.x+position_ecran_x, joueur.animation_tete.y+position_ecran_y,
                         joueur.animation_tete.w, joueur.animation_tete.h), 0])
                joueur.animation_tete.activee = True
                joueur.animation_tete.temps_restant = 24
                joueur.animation_tete.temps_total = 24
                joueur.animation_tete.x = joueur.x
                joueur.animation_tete.y = joueur.y-25
                joueur.animation_tete.w = 64
                joueur.animation_tete.h = 20
                joueur.animation_tete.images = [ANIMATIONS_JOUEUR.subsurface((0, 20, 64, 20)),
                                                ANIMATIONS_JOUEUR.subsurface((64, 20, 64, 20)),
                                                ANIMATIONS_JOUEUR.subsurface((128, 20, 64, 20)),
                                                ANIMATIONS_JOUEUR.subsurface((192, 20, 64, 20)),
                                                ANIMATIONS_JOUEUR.subsurface((256, 20, 64, 20))]

            if etage.salles[joueur.salle].objets[i].type == 1004 or \
               etage.salles[joueur.salle].objets[i].type == 1005:
                joueur.attaque += 10
                if joueur.animation_tete.activee:
                    liste_rafraichir.append([etage.salles[joueur.salle].image.subsurface(
                        (joueur.animation_tete.x, joueur.animation_tete.y,
                         joueur.animation_tete.w, joueur.animation_tete.h)),
                        (joueur.animation_tete.x+position_ecran_x, joueur.animation_tete.y+position_ecran_y,
                         joueur.animation_tete.w, joueur.animation_tete.h), 0])
                joueur.animation_tete.activee = True
                joueur.animation_tete.temps_restant = 24
                joueur.animation_tete.temps_total = 24
                joueur.animation_tete.x = joueur.x
                joueur.animation_tete.y = joueur.y-25
                joueur.animation_tete.w = 64
                joueur.animation_tete.h = 20
                joueur.animation_tete.images = [ANIMATIONS_JOUEUR.subsurface((0, 40, 64, 20)),
                                                ANIMATIONS_JOUEUR.subsurface((64, 40, 64, 20)),
                                                ANIMATIONS_JOUEUR.subsurface((128, 40, 64, 20)),
                                                ANIMATIONS_JOUEUR.subsurface((192, 40, 64, 20)),
                                                ANIMATIONS_JOUEUR.subsurface((256, 40, 64, 20))]

            if etage.salles[joueur.salle].objets[i].type == 1006 or \
               etage.salles[joueur.salle].objets[i].type == 1007:
                liste_rafraichir, joueur = rafraichir_vie(position_ecran_x, position_ecran_y, joueur,
                                                          liste_rafraichir, joueur.points_de_vies+25, joueur.vie_maximum+25)
                if joueur.animation_tete.activee:
                    liste_rafraichir.append([etage.salles[joueur.salle].image.subsurface(
                        (joueur.animation_tete.x, joueur.animation_tete.y,
                         joueur.animation_tete.w, joueur.animation_tete.h)),
                        (joueur.animation_tete.x+position_ecran_x, joueur.animation_tete.y+position_ecran_y,
                         joueur.animation_tete.w, joueur.animation_tete.h), 0])
                joueur.animation_tete.activee = True
                joueur.animation_tete.temps_restant = 24
                joueur.animation_tete.temps_total = 24
                joueur.animation_tete.x = joueur.x
                joueur.animation_tete.y = joueur.y-25
                joueur.animation_tete.w = 64
                joueur.animation_tete.h = 20
                joueur.animation_tete.images = [ANIMATIONS_JOUEUR.subsurface((0, 0, 64, 20)),
                                                ANIMATIONS_JOUEUR.subsurface((64, 0, 64, 20)),
                                                ANIMATIONS_JOUEUR.subsurface((128, 0, 64, 20)),
                                                ANIMATIONS_JOUEUR.subsurface((192, 0, 64, 20)),
                                                ANIMATIONS_JOUEUR.subsurface((256, 0, 64, 20))]

            if etage.salles[joueur.salle].objets[i].type == 1008 or \
               etage.salles[joueur.salle].objets[i].type == 1009:
                joueur.vitesse_attaque = int(joueur.vitesse_attaque*0.9)
                if joueur.animation_tete.activee:
                    liste_rafraichir.append([etage.salles[joueur.salle].image.subsurface(
                        (joueur.animation_tete.x, joueur.animation_tete.y,
                         joueur.animation_tete.w, joueur.animation_tete.h)),
                        (joueur.animation_tete.x+position_ecran_x, joueur.animation_tete.y+position_ecran_y,
                         joueur.animation_tete.w, joueur.animation_tete.h), 0])
                joueur.animation_tete.activee = True
                joueur.animation_tete.temps_restant = 24
                joueur.animation_tete.temps_total = 24
                joueur.animation_tete.x = joueur.x
                joueur.animation_tete.y = joueur.y-25
                joueur.animation_tete.w = 64
                joueur.animation_tete.h = 20
                joueur.animation_tete.images = [ANIMATIONS_JOUEUR.subsurface((0, 60, 64, 20)),
                                                ANIMATIONS_JOUEUR.subsurface((64, 60, 64, 20)),
                                                ANIMATIONS_JOUEUR.subsurface((128, 60, 64, 20)),
                                                ANIMATIONS_JOUEUR.subsurface((192, 60, 64, 20)),
                                                ANIMATIONS_JOUEUR.subsurface((256, 60, 64, 20))]

            if joueur.vitesse > 9:
                joueur.vitesse = 9
            if joueur.vitesse_attaque < 150:
                joueur.vitesse_attaque = 150
            if joueur.deplacement_x > 0:
                joueur.deplacement_x = joueur.vitesse
            if joueur.deplacement_x < 0:
                joueur.deplacement_x = -joueur.vitesse
            if joueur.deplacement_y > 0:
                joueur.deplacement_y = joueur.vitesse
            if joueur.deplacement_y < 0:
                joueur.deplacement_y = -joueur.vitesse

            liste_rafraichir.append([etage.salles[joueur.salle].image.subsurface(
                (etage.salles[joueur.salle].objets[i].x, etage.salles[joueur.salle].objets[i].y, 64, 64)),
                (etage.salles[joueur.salle].objets[i].x+position_ecran_x,
                 etage.salles[joueur.salle].objets[i].y+position_ecran_y, 64, 64), 1])

            del etage.salles[joueur.salle].objets[i]
            i -= 1
        i += 1

    return etage, joueur, liste_rafraichir


def afficher_interface(position_ecran_x, position_ecran_y, ecran, joueur, session):

    global INTERFACE
    global CARACTERES
    global OBJETS
    global ICONES_SORTS

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

    mana_max = 100+(10*session.competences[7])

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

    # AFFICHER LA BARRE DE SORTS

    for i in range(len(joueur.sorts)):
        if joueur.sorts[i] != 0:
            ecran.blit(ICONES_SORTS.subsurface(((joueur.sorts[i]-1) % 10)*64, ((joueur.sorts[i]-1)//10)*64, 64, 64),
                       (position_ecran_x+960, position_ecran_y+(64*i)))
        else:
            icone = pygame.Surface((64, 64))
            icone.fill((150, 150, 150))
            ecran.blit(icone,(position_ecran_x+960, position_ecran_y+(64*i)))

    # AFFICHER LE BOUTON MAP

    ecran.blit(INTERFACE.subsurface((0, 225, 64, 64)), (position_ecran_x+960, position_ecran_y+576, 64, 64))

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


def rafraichir_argent(position_ecran_x, position_ecran_y, joueur, liste_rafraichir, etage, nouvelle_valeur):

    global INTERFACE
    global ANIMATIONS_JOUEUR

    if nouvelle_valeur >= 99:  # FAIRE GAGNER UNE VIE
        nouvelle_valeur -= 99
        liste_rafraichir, joueur = rafraichir_nombre_de_vies(position_ecran_x, position_ecran_y,
                                                             joueur, liste_rafraichir, joueur.nombre_de_vies+1)
        if joueur.animation_tete.activee:
            liste_rafraichir.append([etage.salles[joueur.salle].image.subsurface(
                (joueur.animation_tete.x, joueur.animation_tete.y,
                 joueur.animation_tete.w, joueur.animation_tete.h)),
                (joueur.animation_tete.x+position_ecran_x, joueur.animation_tete.y+position_ecran_y,
                 joueur.animation_tete.w, joueur.animation_tete.h), 0])
        joueur.animation_tete.activee = True
        joueur.animation_tete.temps_restant = 60
        joueur.animation_tete.temps_total = 60
        joueur.animation_tete.x = joueur.x
        joueur.animation_tete.y = joueur.y-25
        joueur.animation_tete.w = 64
        joueur.animation_tete.h = 20
        joueur.animation_tete.images = [ANIMATIONS_JOUEUR.subsurface((0, 80, 64, 20))]

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

        # PRENDRE EN COMPTE L'ARMURE

        if nouvelle_vie < joueur.points_de_vies:
            nouvelle_vie = joueur.points_de_vies-int((joueur.points_de_vies-nouvelle_vie)/(0.01*joueur.armure+1))

        # PRENDRE EN COMPTE L'INVINCIBILITE, NE PAS MODIFIER TROP HAUT OU TROP BAS LES PV...

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

    mana_max = 100+(10*session.competences[7])

    if nouveau_mana < 0:
        nouveau_mana = 0
    if nouveau_mana > mana_max:
        nouveau_mana = mana_max

    # CALCULER LA DIFFERENCE EN PIXELS DE LA BARRE DE MANA AVANT/APRES

    a = int(joueur.mana*(450/mana_max))-int(nouveau_mana*(450/mana_max))

    if a > 0:  # ENLEVER DU MANA

        bout_de_barre = pygame.Surface((a, 28))
        bout_de_barre.fill((42, 42, 42))
        liste_rafraichir.append([bout_de_barre, (position_ecran_x+511+int(nouveau_mana*(450/mana_max)),
                                                 position_ecran_y-30, a, 28), 6])

    if a < 0:  # AJOUTER DU MANA

        bout_de_barre = pygame.Surface((-a, 28))
        bout_de_barre.fill((63, 72, 204))
        liste_rafraichir.append([bout_de_barre, (position_ecran_x+511+int(joueur.mana*(450/mana_max)),
                                                 position_ecran_y-30, -a, 28), 6])

    joueur.mana = nouveau_mana

    return liste_rafraichir, joueur


def rafraichir_niveau_session(position_ecran_x, position_ecran_y, session, liste_rafraichir, joueur, etage):

    global INTERFACE
    global ANIMATIONS_JOUEUR

    # FAIRE MONTER UN OU PLUSIEURS NIVEAU SI BESOIN

    i = 0
    while session.xp >= int(100*(1.8**session.niveau)):
        liste_rafraichir, session = rafraichir_xp(position_ecran_x, position_ecran_y, session,
                                                  liste_rafraichir, session.xp-int(100*(1.8**session.niveau)))
        session.niveau += 1
        session.points_de_competences += 1
        session.points_de_sorts += 1

        if joueur.animation_tete.activee:
            liste_rafraichir.append([etage.salles[joueur.salle].image.subsurface(
                (joueur.animation_tete.x, joueur.animation_tete.y,
                 joueur.animation_tete.w, joueur.animation_tete.h)),
                (joueur.animation_tete.x+position_ecran_x, joueur.animation_tete.y+position_ecran_y,
                 joueur.animation_tete.w, joueur.animation_tete.h), 0])
        joueur.animation_tete.activee = True
        joueur.animation_tete.temps_restant = 120
        joueur.animation_tete.temps_total = 120
        joueur.animation_tete.x = joueur.x
        joueur.animation_tete.y = joueur.y-25
        joueur.animation_tete.w = 64
        joueur.animation_tete.h = 20
        joueur.animation_tete.images = [ANIMATIONS_JOUEUR.subsurface((64, 80, 64, 20))]

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

    return liste_rafraichir, session, joueur


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


def creer_attaque(joueur, position_ecran_x, position_ecran_y, session, etage, tempo):

    global ATTAQUES_JOUEUR
    global ATTAQUES_MONSTRES

    for i in range(len(joueur.attaques.autorisation)):

        if joueur.attaques.autorisation[i] == 1:

            if joueur.sorts_actifs[1] and \
               joueur.sorts[1] == 10 or \
               joueur.sorts[1] == 13 or \
               joueur.sorts[1] == 14:
                if joueur.sorts_temps_activation[1] > pygame.time.get_ticks()-10000:
                    temps_autorise = joueur.attaques.temps_derniere_attaque+int(0.66*joueur.vitesse_attaque)
                else:
                    joueur.sorts_actifs[1] = False
                    temps_autorise = joueur.attaques.temps_derniere_attaque+joueur.vitesse_attaque
            else:
                temps_autorise = joueur.attaques.temps_derniere_attaque+joueur.vitesse_attaque

            if pygame.time.get_ticks() >= temps_autorise:

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

                difference_x = (joueur.attaques.position_souris[0]-10)-(joueur.x+position_ecran_x+27)
                difference_y = (joueur.attaques.position_souris[1]-10)-(joueur.y+position_ecran_y+27)

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
                        entite.deplacement_y = -15-(1.5*session.competences[4])
                    else:
                        entite.deplacement_y = 15+(1.5*session.competences[4])
                    entite.deplacement_x = (entite.deplacement_y*difference_x)/difference_y

                else:
                    if difference_x < 0:
                        entite.deplacement_x = -15-(1.5*session.competences[4])
                    else:
                        entite.deplacement_x = 15+(1.5*session.competences[4])
                    try:
                        entite.deplacement_y = (entite.deplacement_x*difference_y)/difference_x
                    except ZeroDivisionError:
                        entite.deplacement_y = (entite.deplacement_x*difference_y)/1

                joueur.attaques.entites.append(entite)

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

    if joueur.sorts_actifs[0]:
        if joueur.sorts[0] == 1 or \
           joueur.sorts[0] == 3 or \
           joueur.sorts[0] == 6 or \
           joueur.sorts[0] == 7:

            entite = Entite_Attaque()
            entite.x = joueur.x+27
            entite.y = joueur.y+27
            entite.type = 3
            entite.images = [ATTAQUES_JOUEUR.subsurface((60, 0, 22, 22)),
                             ATTAQUES_JOUEUR.subsurface((82, 0, 40, 40))]
            entite.detruit = False
            entite.temps = 0

            difference_x = (joueur.attaques.position_souris[0]-11)-(joueur.x+position_ecran_x+27)
            difference_y = (joueur.attaques.position_souris[1]-11)-(joueur.y+position_ecran_y+27)

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
                else:
                    entite.deplacement_y = 15
                entite.deplacement_x = (entite.deplacement_y*difference_x)/difference_y

            else:
                if difference_x < 0:
                    entite.deplacement_x = -15
                else:
                    entite.deplacement_x = 15
                try:
                    entite.deplacement_y = (entite.deplacement_x*difference_y)/difference_x
                except ZeroDivisionError:
                    entite.deplacement_y = (entite.deplacement_x*difference_y)/1

            joueur.attaques.entites.append(entite)
            joueur.sorts_actifs[0] = False

        elif joueur.sorts[0] == 4:
            for ennemi in etage.salles[joueur.salle].ennemis:
                ennemi.paralyse = True
                ennemi.fin_paralyse = pygame.time.get_ticks() + 2500
                joueur.sorts_actifs[0] = False

        elif joueur.sorts[0] == 2 or joueur.sorts[0] == 5:
            entite = Entite_Attaque()
            entite.x = joueur.x-80
            entite.y = joueur.y-80
            if entite.x > 736:
                entite.x = 736
            if entite.x < 0:
                entite.x = 0
            if entite.y > 352:
                entite.y = 352
            if entite.y < 0:
                entite.y = 0
            entite.w = 224
            entite.h = 224
            entite.type = 4
            entite.images = pygame.transform.scale2x(pygame.transform.scale2x(ATTAQUES_JOUEUR.subsurface((0, 104, 56, 56))))
            entite.detruit = False
            joueur.attaques.entites.append(entite)
            joueur.sorts_actifs[0] = False

    if joueur.sorts_actifs[1]:
        if joueur.sorts[1] == 9:

            entite = Entite_Attaque()
            entite.x = joueur.x-64
            entite.y = joueur.y-64
            if entite.x > 768:
                entite.x = 768
            if entite.x < 0:
                entite.x = 0
            if entite.y > 384:
                entite.y = 384
            if entite.y < 0:
                entite.y = 0
            entite.w = 192
            entite.h = 192
            entite.type = 5
            entite.images = ATTAQUES_JOUEUR.subsurface((0, 232, 192, 192))
            entite.detruit = False
            joueur.attaques.entites.append(entite)
            joueur.sorts_actifs[1] = False

        if joueur.sorts[1] == 11:

            entite = Entite_Attaque()
            entite.x = joueur.attaques.position_souris[0]-position_ecran_x-96
            entite.y = joueur.attaques.position_souris[1]-position_ecran_y-96
            if entite.x > 768:
                entite.x = 768
            if entite.x < 0:
                entite.x = 0
            if entite.y > 384:
                entite.y = 384
            if entite.y < 0:
                entite.y = 0
            entite.w = 192
            entite.h = 192
            entite.type = 5
            entite.images = ATTAQUES_JOUEUR.subsurface((0, 232, 192, 192))
            entite.detruit = False
            joueur.attaques.entites.append(entite)
            joueur.sorts_actifs[1] = False

        if joueur.sorts[1] == 12:

            entite = Entite_Attaque()
            entite.x = joueur.x-160
            entite.y = joueur.y-160
            if entite.x > 576:
                entite.x = 576
            if entite.x < 0:
                entite.x = 0
            if entite.y > 192:
                entite.y = 192
            if entite.y < 0:
                entite.y = 0
            entite.w = 384
            entite.h = 384
            entite.type = 6
            entite.images = pygame.transform.scale2x(ATTAQUES_JOUEUR.subsurface((0, 232, 192, 192)))
            entite.detruit = False
            joueur.attaques.entites.append(entite)
            joueur.sorts_actifs[1] = False

    if tempo == 20:
        for ennemi in etage.salles[joueur.salle].ennemis:
            if ennemi.type == 1 and not ennemi.paralyse:
                entite = Entite_Attaque()
                entite.x = ennemi.x+16
                entite.y = ennemi.y+16
                entite.type = 7
                entite.images = [ATTAQUES_MONSTRES.subsurface((0, 0, 32, 32)),
                                 ATTAQUES_MONSTRES.subsurface((32, 0, 32, 32))]

                difference_x = (joueur.x+16)-(ennemi.x+16)
                difference_y = (joueur.y+32)-(ennemi.y+16)
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
                        entite.deplacement_y = -12
                    else:
                        entite.deplacement_y = 12
                    entite.deplacement_x = (entite.deplacement_y*difference_x)/difference_y

                else:
                    if difference_x < 0:
                        entite.deplacement_x = -12
                    else:
                        entite.deplacement_x = 12
                    try:
                        entite.deplacement_y = (entite.deplacement_x*difference_y)/difference_x
                    except ZeroDivisionError:
                        entite.deplacement_y = (entite.deplacement_x*difference_y)/1

                if joueur.x < ennemi.x and joueur.y < ennemi.y:
                    entite.images[0] = pygame.transform.rotate(entite.images[0], degrees(acos((ennemi.y-joueur.y)/((ennemi.y-joueur.y)**2+(ennemi.x-joueur.x)**2)**(1/2))))
                if joueur.x < ennemi.x and joueur.y == ennemi.y:
                    entite.images[0] = pygame.transform.rotate(entite.images[0], 90)
                if joueur.x < ennemi.x and joueur.y > ennemi.y:
                    entite.images[0] = pygame.transform.rotate(entite.images[0], 90+degrees(acos((ennemi.x-joueur.x)/((joueur.y-ennemi.y)**2+(ennemi.x-joueur.x)**2)**(1/2))))
                if joueur.x == ennemi.x and joueur.y > ennemi.y:
                    entite.images[0] = pygame.transform.rotate(entite.images[0], 180)
                if joueur.x > ennemi.x and joueur.y > ennemi.y:
                    entite.images[0] = pygame.transform.rotate(entite.images[0], 180+degrees(acos((joueur.y-ennemi.y)/((joueur.y-ennemi.y)**2+(joueur.x-ennemi.x)**2)**(1/2))))
                if joueur.x > ennemi.x and joueur.y == ennemi.y:
                    entite.images[0] = pygame.transform.rotate(entite.images[0], 270)
                if joueur.x > ennemi.x and joueur.y < ennemi.y:
                    entite.images[0] = pygame.transform.rotate(entite.images[0], 270+degrees(acos((joueur.x-ennemi.x)/((ennemi.y-joueur.y)**2+(joueur.x-ennemi.x)**2)**(1/2))))

                ennemi.attaques.entites.append(entite)

    return joueur, etage


def gerer_attaques(joueur, position_ecran_x, position_ecran_y, etage, liste_rafraichir, session):

    global TILESET
    global ATTAQUES_JOUEUR

    i = 0

    # ATTAQUES DU JOUEUR

    while i < len(joueur.attaques.entites):

        # ATTAQUES DE BASE

        if joueur.attaques.entites[i].type == 1:

            if not joueur.attaques.entites[i].detruit:  # LORS DU VOYAGE DES ATTAQUES DE BASE

                # EFFACER LE PROJECTILE

                liste_rafraichir.append([etage.salles[joueur.salle].image.subsurface(
                    (joueur.attaques.entites[i].x, joueur.attaques.entites[i].y, 20, 20)),
                    (joueur.attaques.entites[i].x+position_ecran_x,
                     joueur.attaques.entites[i].y+position_ecran_y,
                     20, 20), 0])

                # DEPLACER LE PROJECTILE

                collision = 0

                joueur.attaques.entites[i].x += joueur.attaques.entites[i].deplacement_x
                joueur.attaques.entites[i].y += joueur.attaques.entites[i].deplacement_y

                # REGARDER S'IL Y A COLLISION AVEC LE DECORS

                bloc_a_proximite = [int(joueur.attaques.entites[i].y//64), int(joueur.attaques.entites[i].x//64)]

                if joueur.sorts_actifs[1] and joueur.sorts[1] == 13:
                    if joueur.sorts_temps_activation[1] > pygame.time.get_ticks()-10000:
                        if 11 >= etage.salles[joueur.salle].blocs_type[bloc_a_proximite[0]][bloc_a_proximite[1]] >= 2 or \
                           21 >= etage.salles[joueur.salle].blocs_type[bloc_a_proximite[0]][bloc_a_proximite[1]] >= 14:
                            collision = 1
                    else:
                        joueur.sorts_actifs[1] = False
                        if 11 >= etage.salles[joueur.salle].blocs_type[bloc_a_proximite[0]][bloc_a_proximite[1]] >= 1 or \
                           21 >= etage.salles[joueur.salle].blocs_type[bloc_a_proximite[0]][bloc_a_proximite[1]] >= 14:
                            collision = 1
                else:
                    if 11 >= etage.salles[joueur.salle].blocs_type[bloc_a_proximite[0]][bloc_a_proximite[1]] >= 1 or \
                       21 >= etage.salles[joueur.salle].blocs_type[bloc_a_proximite[0]][bloc_a_proximite[1]] >= 14:
                        collision = 1

                # REGARDER S'IL Y A COLLISION AVEC UN MONSTRE

                for j in range(len(etage.salles[joueur.salle].ennemis)):
                    if collisions(joueur.attaques.entites[i], etage.salles[joueur.salle].ennemis[j].hitbox_degats):

                        collision = 1

                        if etage.salles[joueur.salle].ennemis[j].paralyse and joueur.sorts[0] == 5:
                            degats = 5*joueur.attaque
                        else:
                            degats = joueur.attaque

                        if joueur.sorts_actifs[1] and joueur.sorts[1] == 14:
                            if joueur.sorts_temps_activation[1] > pygame.time.get_ticks()-10000:
                                for ennemi in etage.salles[joueur.salle].ennemis:
                                    ennemi.points_de_vies -= int(degats/len(etage.salles[joueur.salle].ennemis))
                                    if ennemi.points_de_vies <= 0:
                                        ennemi.mort = True
                            else:
                                joueur.sorts_actifs[1] = False
                                etage.salles[joueur.salle].ennemis[j].points_de_vies -= degats
                        else:
                            etage.salles[joueur.salle].ennemis[j].points_de_vies -= degats

                        if session.competences[10] > 0:
                            liste_rafraichir, joueur = rafraichir_vie(position_ecran_x, position_ecran_y, joueur,
                                                                      liste_rafraichir,
                                                                      joueur.points_de_vies+session.competences[10],
                                                                      joueur.vie_maximum)
                        if session.competences[11] > 0:
                            liste_rafraichir, joueur = \
                                rafraichir_mana(position_ecran_x, position_ecran_y, joueur, liste_rafraichir,
                                                session, joueur.mana+session.competences[11])

                        if etage.salles[joueur.salle].ennemis[j].points_de_vies <= 0:
                            etage.salles[joueur.salle].ennemis[j].mort = True

                        joueur.attaques.entites[i].x = etage.salles[joueur.salle].ennemis[j].x+22
                        joueur.attaques.entites[i].y = etage.salles[joueur.salle].ennemis[j].y+22
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

                    if joueur.attaques.entites[i].temps == 1:

                        # AJUSTER LA POSITION

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
                        liste_rafraichir.append([etage.salles[joueur.salle].image.subsurface(
                            (joueur.attaques.entites[i].x, joueur.attaques.entites[i].y, 96, 96)),
                            (int(joueur.attaques.entites[i].x)+position_ecran_x,
                             int(joueur.attaques.entites[i].y)+position_ecran_y,
                             96, 96), 2])

                        for ennemi in etage.salles[joueur.salle].ennemis:
                            if (((ennemi.x+32)-(joueur.attaques.entites[i].x+48))**2)+(((ennemi.y+32)-(joueur.attaques.entites[i].y+48))**2) <= 4096:
                                ennemi.points_de_vies -= 25*session.competences[8]
                                if ennemi.points_de_vies <= 0:
                                    ennemi.mort = True

                    elif 6 < joueur.attaques.entites[i].temps < 24:  # AFFICHER LA GROSSE EXPLOSION
                        liste_rafraichir.append([joueur.attaques.entites[i].images[3],
                                                 (int(joueur.attaques.entites[i].x)+position_ecran_x,
                                                  int(joueur.attaques.entites[i].y)+position_ecran_y,
                                                  96, 96), 2])
                        i += 1

                    elif joueur.attaques.entites[i].temps == 24:  # EFFACER DEFINITIVEMENT L'ATTAQUE
                        liste_rafraichir.append([etage.salles[joueur.salle].image.subsurface(
                            (joueur.attaques.entites[i].x, joueur.attaques.entites[i].y, 96, 96)),
                            (int(joueur.attaques.entites[i].x)+position_ecran_x,
                             int(joueur.attaques.entites[i].y)+position_ecran_y,
                             96, 96), 0])

                        del joueur.attaques.entites[i]

                # SANS LES PROJECTILS EXPLOSIFS

                if session.competences[8] == 0:

                    if joueur.attaques.entites[i].temps == 1:

                        # AJUSTER LA POSITION

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
                        liste_rafraichir.append([etage.salles[joueur.salle].image.subsurface(
                            (joueur.attaques.entites[i].x, joueur.attaques.entites[i].y, 40, 40)),
                            (int(joueur.attaques.entites[i].x)+position_ecran_x,
                             int(joueur.attaques.entites[i].y)+position_ecran_y,
                             40, 40), 0])

                        del joueur.attaques.entites[i]

        # BOMBES

        elif joueur.attaques.entites[i].type == 2:

            if not joueur.attaques.entites[i].detruit:  # LORSQU'ELLE CLIGNOTE

                joueur.attaques.entites[i].temps += 1
                liste_rafraichir.append([etage.salles[joueur.salle].image.subsurface(
                    (joueur.attaques.entites[i].x, joueur.attaques.entites[i].y, 64, 64)),
                    (position_ecran_x+joueur.attaques.entites[i].x,
                     position_ecran_y+joueur.attaques.entites[i].y,
                     64, 64), 0])

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

                    for ennemi in etage.salles[joueur.salle].ennemis:  # SI LA BOMBE TOUCHE DES ENNEMIS
                        if collisions(joueur.attaques.entites[i], ennemi.hitbox_degats):
                            ennemi.points_de_vies -= 2*joueur.attaque
                            if ennemi.points_de_vies <= 0:
                                ennemi.mort = True

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
                        if etage.salles[joueur.salle].blocs_type[blocs_a_proximite[j][1]][blocs_a_proximite[j][0]] == 1:
                            etage.salles[joueur.salle].blocs_type[blocs_a_proximite[j][1]][blocs_a_proximite[j][0]] = 0
                            etage.salles[joueur.salle].image.blit(
                                TILESET.subsurface((0, 0, 64, 64)),
                                (blocs_a_proximite[j][0]*64, blocs_a_proximite[j][1]*64))
                            liste_rafraichir.append([etage.salles[joueur.salle].image.subsurface(
                                (blocs_a_proximite[j][0]*64, blocs_a_proximite[j][1]*64, 64, 64)),
                                ((blocs_a_proximite[j][0]*64)+position_ecran_x,
                                 (blocs_a_proximite[j][1]*64)+position_ecran_y,
                                 64, 64), 0])

                if joueur.attaques.entites[i].temps == 24:  # DETRUIRE DEFINITIVEMENT LA BOMBE
                    liste_rafraichir.append([etage.salles[joueur.salle].image.subsurface(
                        (joueur.attaques.entites[i].x, joueur.attaques.entites[i].y, 192, 192)),
                        (position_ecran_x+joueur.attaques.entites[i].x, position_ecran_y+joueur.attaques.entites[i].y,
                         192, 192), 0])
                    del joueur.attaques.entites[i]
                    i -= 1
                else:  # AFFICHER LA FUMEE
                    liste_rafraichir.append([joueur.attaques.entites[i].images[2],
                                             (position_ecran_x+joueur.attaques.entites[i].x,
                                              position_ecran_y+joueur.attaques.entites[i].y,
                                              192, 192), 2])

                i += 1

        # ATTAQUES PARALYSANTES

        elif joueur.attaques.entites[i].type == 3:

            if not joueur.attaques.entites[i].detruit:  # LORS DU VOYAGE DES ATTAQUES DE BASE

                # EFFACER LE PROJECTILE

                liste_rafraichir.append([etage.salles[joueur.salle].image.subsurface(
                    (joueur.attaques.entites[i].x, joueur.attaques.entites[i].y, 22, 22)),
                    (joueur.attaques.entites[i].x+position_ecran_x,
                     joueur.attaques.entites[i].y+position_ecran_y,
                     22, 22), 2])

                # DEPLACER LE PROJECTILE

                collision = 0

                joueur.attaques.entites[i].x += joueur.attaques.entites[i].deplacement_x
                joueur.attaques.entites[i].y += joueur.attaques.entites[i].deplacement_y

                # REGARDER S'IL Y A COLLISION AVEC LE DECORS

                bloc_a_proximite = [int(joueur.attaques.entites[i].y//64), int(joueur.attaques.entites[i].x//64)]

                if joueur.sorts[0] == 6:
                    if 11 >= etage.salles[joueur.salle].blocs_type[bloc_a_proximite[0]][bloc_a_proximite[1]] >= 2 or \
                       21 >= etage.salles[joueur.salle].blocs_type[bloc_a_proximite[0]][bloc_a_proximite[1]] >= 14:
                        collision = 1
                else:
                    if 11 >= etage.salles[joueur.salle].blocs_type[bloc_a_proximite[0]][bloc_a_proximite[1]] >= 1 or \
                       21 >= etage.salles[joueur.salle].blocs_type[bloc_a_proximite[0]][bloc_a_proximite[1]] >= 14:
                        collision = 1

                # REGARDER S'IL Y A COLLISION AVEC UN MONSTRE

                for j in range(len(etage.salles[joueur.salle].ennemis)):
                    if collisions(joueur.attaques.entites[i], etage.salles[joueur.salle].ennemis[j].hitbox_degats):

                        etage.salles[joueur.salle].ennemis[j].paralyse = True
                        etage.salles[joueur.salle].ennemis[j].fin_paralyse = pygame.time.get_ticks() + 3000

                        if joueur.sorts[0] == 3 or joueur.sorts[0] == 6:
                            etage.salles[joueur.salle].ennemis[j].empoisonne = True
                            etage.salles[joueur.salle].ennemis[j].fin_empoisonne = pygame.time.get_ticks() + 5000
                            etage.salles[joueur.salle].ennemis[j].temps_dernier_poison = 0

                        if joueur.sorts[0] == 7:
                            etage.salles[joueur.salle].ennemis[j].empoisonne = True
                            etage.salles[joueur.salle].ennemis[j].temps_dernier_poison = 0

                        if joueur.sorts[0] != 6:
                            joueur.attaques.entites[i].x = etage.salles[joueur.salle].ennemis[j].x+20
                            joueur.attaques.entites[i].y = etage.salles[joueur.salle].ennemis[j].y+20
                            collision = 1
                            break

                # AFFICHER LE PROJECTILE S'IL N'Y A PAS COLLISION / L'INSCIRE COMME DETRUIT

                if collision == 0:
                    liste_rafraichir.append([joueur.attaques.entites[i].images[0],
                                             (int(joueur.attaques.entites[i].x)+position_ecran_x,
                                              int(joueur.attaques.entites[i].y)+position_ecran_y,
                                              22, 22), 2])

                if collision == 1:
                    joueur.attaques.entites[i].detruit = True
                    joueur.attaques.entites[i].temps = 0

                i += 1

            else:  # LORS DE LA DESTRUCTION DES ATTAQUES PARALYSANTES

                joueur.attaques.entites[i].temps += 1

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
                    liste_rafraichir.append([etage.salles[joueur.salle].image.subsurface(
                        (joueur.attaques.entites[i].x, joueur.attaques.entites[i].y, 40, 40)),
                        (int(joueur.attaques.entites[i].x)+position_ecran_x,
                         int(joueur.attaques.entites[i].y)+position_ecran_y,
                         40, 40), 0])

                    del joueur.attaques.entites[i]

        # NUAGE PARALYSANT

        elif joueur.attaques.entites[i].type == 4:
            if not joueur.attaques.entites[i].detruit:
                for ennemi in etage.salles[joueur.salle].ennemis: # PARALYSER LES ENNEMIS PROCHES
                    if ((ennemi.hitbox_degats.x+32)-(joueur.attaques.entites[i].x+112))**2+((ennemi.hitbox_degats.y+32)-(joueur.attaques.entites[i].y+112))**2 <= 16384:
                        ennemi.paralyse = True
                        ennemi.fin_paralyse = pygame.time.get_ticks()+2500
                joueur.attaques.entites[i].detruit = True
                joueur.attaques.entites[i].temps = 0
            if joueur.attaques.entites[i].detruit:
                joueur.attaques.entites[i].temps += 1
                if joueur.attaques.entites[i].temps == 24:  # EFFACER LE NUAGE
                    liste_rafraichir.append([etage.salles[joueur.salle].image.subsurface(
                        (joueur.attaques.entites[i].x, joueur.attaques.entites[i].y,
                         joueur.attaques.entites[i].w, joueur.attaques.entites[i].h)),
                        (joueur.attaques.entites[i].x+position_ecran_x, joueur.attaques.entites[i].y+position_ecran_y,
                         joueur.attaques.entites[i].w, joueur.attaques.entites[i].h), 0])
                    del joueur.attaques.entites[i]
                else:  # AFFICHER LE NUAGE
                    liste_rafraichir.append([joueur.attaques.entites[i].images,
                        (joueur.attaques.entites[i].x+position_ecran_x, joueur.attaques.entites[i].y+position_ecran_y,
                         joueur.attaques.entites[i].w, joueur.attaques.entites[i].h), 2])
                    i += 1

        # EXPLOSION TEMPORELLE

        elif joueur.attaques.entites[i].type == 5:
            if not joueur.attaques.entites[i].detruit:
                for ennemi in etage.salles[joueur.salle].ennemis: # INFLIGE DES DEGATS AUX ENNEMIS PROCHES
                    if ((ennemi.hitbox_degats.x+32)-(joueur.attaques.entites[i].x+96))**2+((ennemi.hitbox_degats.y+32)-(joueur.attaques.entites[i].y+96))**2 <= 9216:
                        ennemi.points_de_vies -= 2*joueur.attaque
                        if ennemi.points_de_vies <= 0:
                            ennemi.mort = True
                joueur.attaques.entites[i].detruit = True
                joueur.attaques.entites[i].temps = 0
            if joueur.attaques.entites[i].detruit:
                joueur.attaques.entites[i].temps += 1
                if joueur.attaques.entites[i].temps == 24:  # EFFACER L'EXPLOSION
                    liste_rafraichir.append([etage.salles[joueur.salle].image.subsurface(
                        (joueur.attaques.entites[i].x, joueur.attaques.entites[i].y,
                         joueur.attaques.entites[i].w, joueur.attaques.entites[i].h)),
                        (joueur.attaques.entites[i].x+position_ecran_x, joueur.attaques.entites[i].y+position_ecran_y,
                         joueur.attaques.entites[i].w, joueur.attaques.entites[i].h), 0])
                    del joueur.attaques.entites[i]
                else:  # AFFICHER L'EXPLOSION
                    liste_rafraichir.append([joueur.attaques.entites[i].images,
                        (joueur.attaques.entites[i].x+position_ecran_x, joueur.attaques.entites[i].y+position_ecran_y,
                         joueur.attaques.entites[i].w, joueur.attaques.entites[i].h), 2])
                    i += 1

        # GROSSE EXPLOSION TEMPORELLE

        elif joueur.attaques.entites[i].type == 6:
            if not joueur.attaques.entites[i].detruit:
                for ennemi in etage.salles[joueur.salle].ennemis: # INFLIGE DES DEGATS AUX ENNEMIS PROCHES
                    if ((ennemi.hitbox_degats.x+32)-(joueur.attaques.entites[i].x+192))**2+((ennemi.hitbox_degats.y+32)-(joueur.attaques.entites[i].y+192))**2 <= 36864:
                        ennemi.points_de_vies -= 2*joueur.attaque
                        if ennemi.points_de_vies <= 0:
                            ennemi.mort = True
                joueur.attaques.entites[i].detruit = True
                joueur.attaques.entites[i].temps = 0
            if joueur.attaques.entites[i].detruit:
                joueur.attaques.entites[i].temps += 1
                if joueur.attaques.entites[i].temps == 24:  # EFFACER L'EXPLOSION
                    liste_rafraichir.append([etage.salles[joueur.salle].image.subsurface(
                        (joueur.attaques.entites[i].x, joueur.attaques.entites[i].y,
                         joueur.attaques.entites[i].w, joueur.attaques.entites[i].h)),
                        (joueur.attaques.entites[i].x+position_ecran_x, joueur.attaques.entites[i].y+position_ecran_y,
                         joueur.attaques.entites[i].w, joueur.attaques.entites[i].h), 0])
                    del joueur.attaques.entites[i]
                else:  # AFFICHER L'EXPLOSION
                    liste_rafraichir.append([joueur.attaques.entites[i].images,
                        (joueur.attaques.entites[i].x+position_ecran_x, joueur.attaques.entites[i].y+position_ecran_y,
                         joueur.attaques.entites[i].w, joueur.attaques.entites[i].h), 2])
                    i += 1

    # ATTAQUES DES MONSTRES

    for ennemi in etage.salles[joueur.salle].ennemis:

        i = 0
        while i < len(ennemi.attaques.entites):

            # ATTAQUES DE BASE DES MONSTRES A DISTANCE

            if ennemi.attaques.entites[i].type == 7:

                if not ennemi.attaques.entites[i].detruit:  # LORS DU VOYAGE DES ATTAQUES

                    w = ennemi.attaques.entites[i].images[0].get_size()[0]
                    h = ennemi.attaques.entites[i].images[0].get_size()[1]

                    # EFFACER LE PROJECTILE

                    liste_rafraichir.append([etage.salles[joueur.salle].image.subsurface(
                        (ennemi.attaques.entites[i].x+16-w//2, ennemi.attaques.entites[i].y+16-h//2, w, h)),
                        (ennemi.attaques.entites[i].x+position_ecran_x+16-w//2,
                         ennemi.attaques.entites[i].y+position_ecran_y+16-h//2, w, h), 0])

                    # DEPLACER LE PROJECTILE

                    collision = 0

                    ennemi.attaques.entites[i].x = int(ennemi.attaques.entites[i].x+ennemi.attaques.entites[i].deplacement_x)
                    ennemi.attaques.entites[i].y = int(ennemi.attaques.entites[i].y+ennemi.attaques.entites[i].deplacement_y)

                    # REGARDER S'IL Y A COLLISION AVEC LE DECORS

                    bloc_a_proximite = [int(ennemi.attaques.entites[i].y//64), int(ennemi.attaques.entites[i].x//64)]
                    if 11 >= etage.salles[joueur.salle].blocs_type[bloc_a_proximite[0]][bloc_a_proximite[1]] >= 1 or \
                       21 >= etage.salles[joueur.salle].blocs_type[bloc_a_proximite[0]][bloc_a_proximite[1]] >= 14:
                        collision = 1

                    # REGARDER S'IL Y A COLLISION AVEC LE JOUEUR

                    if collisions(ennemi.attaques.entites[i], joueur):
                        if randrange(100) >= (5*session.competences[9]):
                            liste_rafraichir, joueur = \
                                rafraichir_vie(position_ecran_x, position_ecran_y, joueur, liste_rafraichir,
                                               joueur.points_de_vies-ennemi.attaque//2, joueur.vie_maximum)
                        else:
                            if not joueur.invincible:
                                joueur.invincible = True
                                joueur.temps_depuis_invincible = pygame.time.get_ticks()
                        collision = 1
                        ennemi.attaques.entites[i].x = joueur.x
                        ennemi.attaques.entites[i].y = joueur.y

                    # REGARDER S'IL Y A COLLISION AVEC UN AUTRE ENNEMI

                    for j in range(len(etage.salles[joueur.salle].ennemis)):
                        if etage.salles[joueur.salle].ennemis[j] is not ennemi and \
                           collisions(ennemi.attaques.entites[i], etage.salles[joueur.salle].ennemis[j].hitbox_degats):
                            collision = 1
                            etage.salles[joueur.salle].ennemis[j].points_de_vies -= ennemi.attaque
                            if etage.salles[joueur.salle].ennemis[j].points_de_vies <= 0:
                                etage.salles[joueur.salle].ennemis[j].mort = True
                            ennemi.attaques.entites[i].x = etage.salles[joueur.salle].ennemis[j].x+16
                            ennemi.attaques.entites[i].y = etage.salles[joueur.salle].ennemis[j].y+16

                    # AFFICHER LE PROJECTILE S'IL N'Y A PAS COLLISION / L'INSCIRE COMME DETRUIT

                    if collision == 0:
                        liste_rafraichir.append([ennemi.attaques.entites[i].images[0],
                                                 (ennemi.attaques.entites[i].x+position_ecran_x+16-w//2,
                                                  ennemi.attaques.entites[i].y+position_ecran_y+16-h//2, w, h), 2])

                    if collision == 1:
                        ennemi.attaques.entites[i].detruit = True
                        ennemi.attaques.entites[i].temps = 0

                    i += 1

                else:  # LORS DE LA DESTRUCTION DES ATTAQUES DES MONSTRES A DISTANCE

                    ennemi.attaques.entites[i].temps += 1

                    if ennemi.attaques.entites[i].temps == 1:

                        # AJUSTER LA POSITION

                        if ennemi.attaques.entites[i].deplacement_x <= 0:
                            ennemi.attaques.entites[i].x -= 16
                        if ennemi.attaques.entites[i].deplacement_y <= 0:
                            ennemi.attaques.entites[i].y -= 16

                        if ennemi.attaques.entites[i].x < 0:
                            ennemi.attaques.entites[i].x = 0
                        if ennemi.attaques.entites[i].y < 0:
                            ennemi.attaques.entites[i].y = 0
                        if ennemi.attaques.entites[i].x > 928:
                            ennemi.attaques.entites[i].x = 928
                        if ennemi.attaques.entites[i].y > 544:
                            ennemi.attaques.entites[i].y = 544

                    if ennemi.attaques.entites[i].temps < 24:  # AFFICHER L'IMPACT
                        liste_rafraichir.append([ennemi.attaques.entites[i].images[1],
                                                 (ennemi.attaques.entites[i].x+position_ecran_x,
                                                  ennemi.attaques.entites[i].y+position_ecran_y,
                                                  32, 32), 2])
                        i += 1

                    elif ennemi.attaques.entites[i].temps == 24:  # EFFACER DEFINITIVEMENT L'ATTAQUE
                        liste_rafraichir.append([etage.salles[joueur.salle].image.subsurface(
                            (ennemi.attaques.entites[i].x, ennemi.attaques.entites[i].y, 32, 32)),
                            (ennemi.attaques.entites[i].x+position_ecran_x,
                             ennemi.attaques.entites[i].y+position_ecran_y, 32, 32), 0])

                        del ennemi.attaques.entites[i]

    return joueur, etage, liste_rafraichir


def deplacer_monstres(etage, joueur, tempo, liste_rafraichir, position_ecran_x, position_ecran_y, session):

    for i in range(len(etage.salles[joueur.salle].ennemis)):

        if not etage.salles[joueur.salle].ennemis[i].mort:  # LA MORT DES MONSTRES EST GEREE DANS UNE AUTRE FONCTION

            # MONSTRES DE BASE

            if etage.salles[joueur.salle].ennemis[i].type == 0:

                # EFFACER LE MONSTRE

                liste_rafraichir.append([etage.salles[joueur.salle].image.subsurface(
                    (etage.salles[joueur.salle].ennemis[i].x, etage.salles[joueur.salle].ennemis[i].y, 64, 64)),
                    (etage.salles[joueur.salle].ennemis[i].x+position_ecran_x,
                     etage.salles[joueur.salle].ennemis[i].y+position_ecran_y,
                     64, 64), 0])

                # CALCULER LA TRAJECTOIRE DU MONSTRE

                if etage.salles[joueur.salle].ennemis[i].x < joueur.x:
                    etage.salles[joueur.salle].ennemis[i].deplacement_x = 2
                    if etage.salles[joueur.salle].ennemis[i].x+1 == joueur.x:
                        etage.salles[joueur.salle].ennemis[i].deplacement_x = 1

                elif etage.salles[joueur.salle].ennemis[i].x > joueur.x:
                    etage.salles[joueur.salle].ennemis[i].deplacement_x = -2
                    if etage.salles[joueur.salle].ennemis[i].x-1 == joueur.x:
                        etage.salles[joueur.salle].ennemis[i].deplacement_x = -1

                else:
                    etage.salles[joueur.salle].ennemis[i].deplacement_x = 0

                if etage.salles[joueur.salle].ennemis[i].y < joueur.y:
                    etage.salles[joueur.salle].ennemis[i].deplacement_y = 2
                    if etage.salles[joueur.salle].ennemis[i].y+1 == joueur.y:
                        etage.salles[joueur.salle].ennemis[i].deplacement_y = 1

                elif etage.salles[joueur.salle].ennemis[i].y > joueur.y:
                    etage.salles[joueur.salle].ennemis[i].deplacement_y = -2
                    if etage.salles[joueur.salle].ennemis[i].y-1 == joueur.y:
                        etage.salles[joueur.salle].ennemis[i].deplacement_y = -1

                else:
                    etage.salles[joueur.salle].ennemis[i].deplacement_y = 0

                if etage.salles[joueur.salle].ennemis[i].paralyse and \
                   pygame.time.get_ticks() < etage.salles[joueur.salle].ennemis[i].fin_paralyse:
                    etage.salles[joueur.salle].ennemis[i].deplacement_x = 0
                    etage.salles[joueur.salle].ennemis[i].deplacement_y = 0
                if etage.salles[joueur.salle].ennemis[i].paralyse and \
                   pygame.time.get_ticks() >= etage.salles[joueur.salle].ennemis[i].fin_paralyse:
                    etage.salles[joueur.salle].ennemis[i].paralyse = False

                # DEPLACER LE MONSTRE SUR L'AXE DES X

                if etage.salles[joueur.salle].ennemis[i].deplacement_x != 0:

                    etage.salles[joueur.salle].ennemis[i].x += etage.salles[joueur.salle].ennemis[i].deplacement_x
                    etage.salles[joueur.salle].ennemis[i].hitbox_degats.x = etage.salles[joueur.salle].ennemis[i].x
                    etage.salles[joueur.salle].ennemis[i].hitbox_deplacement.x = etage.salles[joueur.salle].ennemis[i].x+16

                    blocs_a_proximite = list([[etage.salles[joueur.salle].ennemis[i].x//64,
                                               etage.salles[joueur.salle].ennemis[i].y//64]])
                    blocs_a_proximite.append([blocs_a_proximite[0][0]+1, blocs_a_proximite[0][1]])
                    blocs_a_proximite.append([blocs_a_proximite[0][0], blocs_a_proximite[0][1]+1])
                    blocs_a_proximite.append([blocs_a_proximite[0][0]+1, blocs_a_proximite[0][1]+1])

                    for bloc in blocs_a_proximite:

                        while collisions(etage.salles[joueur.salle].ennemis[i].hitbox_deplacement,
                                         etage.salles[joueur.salle].blocs_hitboxs[bloc[1]][bloc[0]]) and \
                                (11 >= etage.salles[joueur.salle].blocs_type[bloc[1]][bloc[0]] >= 1 or
                                 21 >= etage.salles[joueur.salle].blocs_type[bloc[1]][bloc[0]] >= 14):

                            etage.salles[joueur.salle].ennemis[i].hitbox_degats.x = etage.salles[joueur.salle].ennemis[i].x
                            etage.salles[joueur.salle].ennemis[i].hitbox_deplacement.x = etage.salles[joueur.salle].ennemis[i].x+16

                            if etage.salles[joueur.salle].ennemis[i].deplacement_x > 0:
                                etage.salles[joueur.salle].ennemis[i].x -= 1
                            else:
                                etage.salles[joueur.salle].ennemis[i].x += 1

                            if etage.salles[joueur.salle].ennemis[i].x//64 != blocs_a_proximite[0][0]:
                                blocs_a_proximite[0][0] = etage.salles[joueur.salle].ennemis[i].x//64
                                blocs_a_proximite[1][0] = blocs_a_proximite[0][0]+1
                                blocs_a_proximite[2][0] = blocs_a_proximite[0][0]
                                blocs_a_proximite[3][0] = blocs_a_proximite[0][0]+1

                    for k in range(len(etage.salles[joueur.salle].ennemis)):

                        if k != i:
                            while collisions(etage.salles[joueur.salle].ennemis[i].hitbox_deplacement,
                                             etage.salles[joueur.salle].ennemis[k].hitbox_deplacement):

                                etage.salles[joueur.salle].ennemis[i].hitbox_degats.x = etage.salles[joueur.salle].ennemis[i].x
                                etage.salles[joueur.salle].ennemis[i].hitbox_deplacement.x = etage.salles[joueur.salle].ennemis[i].x+16

                                if etage.salles[joueur.salle].ennemis[i].deplacement_x > 0:
                                    etage.salles[joueur.salle].ennemis[i].x -= 1
                                else:
                                    etage.salles[joueur.salle].ennemis[i].x += 1

                                if etage.salles[joueur.salle].ennemis[i].x//64 != blocs_a_proximite[0][0]:
                                    blocs_a_proximite[0][0] = etage.salles[joueur.salle].ennemis[i].x//64
                                    blocs_a_proximite[1][0] = blocs_a_proximite[0][0]+1
                                    blocs_a_proximite[2][0] = blocs_a_proximite[0][0]
                                    blocs_a_proximite[3][0] = blocs_a_proximite[0][0]+1

                # DEPLACER LE MONSTRE SUR L'AXE DES Y

                if etage.salles[joueur.salle].ennemis[i].deplacement_y != 0:

                    etage.salles[joueur.salle].ennemis[i].y += etage.salles[joueur.salle].ennemis[i].deplacement_y
                    etage.salles[joueur.salle].ennemis[i].hitbox_degats.y = etage.salles[joueur.salle].ennemis[i].y
                    etage.salles[joueur.salle].ennemis[i].hitbox_deplacement.y = etage.salles[joueur.salle].ennemis[i].y+16

                    blocs_a_proximite = list([[etage.salles[joueur.salle].ennemis[i].x//64,
                                               etage.salles[joueur.salle].ennemis[i].y//64]])
                    blocs_a_proximite.append([blocs_a_proximite[0][0]+1, blocs_a_proximite[0][1]])
                    blocs_a_proximite.append([blocs_a_proximite[0][0], blocs_a_proximite[0][1]+1])
                    blocs_a_proximite.append([blocs_a_proximite[0][0]+1, blocs_a_proximite[0][1]+1])

                    for bloc in blocs_a_proximite:

                        while collisions(etage.salles[joueur.salle].ennemis[i].hitbox_deplacement,
                                         etage.salles[joueur.salle].blocs_hitboxs[bloc[1]][bloc[0]]) and \
                                (11 >= etage.salles[joueur.salle].blocs_type[bloc[1]][bloc[0]] >= 1 or
                                 21 >= etage.salles[joueur.salle].blocs_type[bloc[1]][bloc[0]] >= 14):

                            etage.salles[joueur.salle].ennemis[i].hitbox_degats.y = etage.salles[joueur.salle].ennemis[i].y
                            etage.salles[joueur.salle].ennemis[i].hitbox_deplacement.y = etage.salles[joueur.salle].ennemis[i].y+16

                            if etage.salles[joueur.salle].ennemis[i].deplacement_y > 0:
                                etage.salles[joueur.salle].ennemis[i].y -= 1
                            else:
                                etage.salles[joueur.salle].ennemis[i].y += 1

                            if etage.salles[joueur.salle].ennemis[i].y//64 != blocs_a_proximite[0][1]:
                                blocs_a_proximite[0][1] = etage.salles[joueur.salle].ennemis[i].y//64
                                blocs_a_proximite[1][1] = blocs_a_proximite[0][1]
                                blocs_a_proximite[2][1] = blocs_a_proximite[0][1]+1
                                blocs_a_proximite[3][1] = blocs_a_proximite[2][1]

                    for k in range(len(etage.salles[joueur.salle].ennemis)):

                        if k != i:
                            while collisions(etage.salles[joueur.salle].ennemis[i].hitbox_deplacement,
                                             etage.salles[joueur.salle].ennemis[k].hitbox_deplacement):

                                etage.salles[joueur.salle].ennemis[i].hitbox_degats.y = etage.salles[joueur.salle].ennemis[i].y
                                etage.salles[joueur.salle].ennemis[i].hitbox_deplacement.y = etage.salles[joueur.salle].ennemis[i].y+16

                                if etage.salles[joueur.salle].ennemis[i].deplacement_y > 0:
                                    etage.salles[joueur.salle].ennemis[i].y -= 1
                                else:
                                    etage.salles[joueur.salle].ennemis[i].y += 1

                                if etage.salles[joueur.salle].ennemis[i].y//64 != blocs_a_proximite[0][1]:
                                    blocs_a_proximite[0][1] = etage.salles[joueur.salle].ennemis[i].y//64
                                    blocs_a_proximite[1][1] = blocs_a_proximite[0][1]
                                    blocs_a_proximite[2][1] = blocs_a_proximite[0][1]+1
                                    blocs_a_proximite[3][1] = blocs_a_proximite[2][1]

                # GERER LA PERTE DE PV DU JOUEUR / LA POSSIBILITE QU'IL ESQUIVE AVEC LA COMPETENCE APPROPRIEE

                if collisions(etage.salles[joueur.salle].ennemis[i].hitbox_degats, joueur.hitbox):
                    if randrange(100) >= (5*session.competences[9]):
                        liste_rafraichir, joueur = \
                            rafraichir_vie(position_ecran_x, position_ecran_y, joueur, liste_rafraichir,
                                           joueur.points_de_vies-etage.salles[joueur.salle].ennemis[i].attaque,
                                           joueur.vie_maximum)
                    else:
                        if not joueur.invincible:
                            joueur.invincible = True
                            joueur.temps_depuis_invincible = pygame.time.get_ticks()

                # AFFICHER LE MONSTRE APRES DEPLACEMENT

                if etage.salles[joueur.salle].ennemis[i].deplacement_x > 0 and \
                   etage.salles[joueur.salle].ennemis[i].deplacement_y == 0:
                    liste_rafraichir.append([etage.salles[joueur.salle].ennemis[i].images.droite[tempo//8],
                                             (etage.salles[joueur.salle].ennemis[i].x+position_ecran_x,
                                              etage.salles[joueur.salle].ennemis[i].y+position_ecran_y,
                                              64, 64), 3])
                if etage.salles[joueur.salle].ennemis[i].deplacement_x < 0 and \
                   etage.salles[joueur.salle].ennemis[i].deplacement_y == 0:
                    liste_rafraichir.append([etage.salles[joueur.salle].ennemis[i].images.gauche[tempo//8],
                                             (etage.salles[joueur.salle].ennemis[i].x+position_ecran_x,
                                              etage.salles[joueur.salle].ennemis[i].y+position_ecran_y,
                                              64, 64), 3])
                if etage.salles[joueur.salle].ennemis[i].deplacement_y > 0:
                    liste_rafraichir.append([etage.salles[joueur.salle].ennemis[i].images.bas[tempo//8],
                                             (etage.salles[joueur.salle].ennemis[i].x+position_ecran_x,
                                              etage.salles[joueur.salle].ennemis[i].y+position_ecran_y,
                                              64, 64), 3])
                if etage.salles[joueur.salle].ennemis[i].deplacement_y < 0:
                    liste_rafraichir.append([etage.salles[joueur.salle].ennemis[i].images.haut[tempo//8],
                                             (etage.salles[joueur.salle].ennemis[i].x+position_ecran_x,
                                              etage.salles[joueur.salle].ennemis[i].y+position_ecran_y,
                                              64, 64), 3])
                if etage.salles[joueur.salle].ennemis[i].deplacement_y == 0 and \
                   etage.salles[joueur.salle].ennemis[i].deplacement_x == 0:
                    liste_rafraichir.append([etage.salles[joueur.salle].ennemis[i].images.bas[0],
                                             (etage.salles[joueur.salle].ennemis[i].x+position_ecran_x,
                                              etage.salles[joueur.salle].ennemis[i].y+position_ecran_y,
                                              64, 64), 3])

                # AFFICHER LE MONSTRE S'IL EST PARALYSE

                if etage.salles[joueur.salle].ennemis[i].paralyse:
                    liste_rafraichir.append([etage.salles[joueur.salle].ennemis[i].images.bas[6],
                                             (etage.salles[joueur.salle].ennemis[i].x+position_ecran_x,
                                              etage.salles[joueur.salle].ennemis[i].y+position_ecran_y,
                                              64, 64), 3])

            # MONSTRES A DISTANCE

            if etage.salles[joueur.salle].ennemis[i].type == 1:

                # EFFACER LE MONSTRE

                liste_rafraichir.append([etage.salles[joueur.salle].image.subsurface(
                    (etage.salles[joueur.salle].ennemis[i].x, etage.salles[joueur.salle].ennemis[i].y, 64, 64)),
                    (etage.salles[joueur.salle].ennemis[i].x+position_ecran_x,
                     etage.salles[joueur.salle].ennemis[i].y+position_ecran_y,
                     64, 64), 0])

                # GERER LA PARALYSIE DU MONSTRE

                if etage.salles[joueur.salle].ennemis[i].paralyse and \
                   pygame.time.get_ticks() < etage.salles[joueur.salle].ennemis[i].fin_paralyse:
                    etage.salles[joueur.salle].ennemis[i].deplacement_x = 0
                    etage.salles[joueur.salle].ennemis[i].deplacement_y = 0
                if etage.salles[joueur.salle].ennemis[i].paralyse and \
                   pygame.time.get_ticks() >= etage.salles[joueur.salle].ennemis[i].fin_paralyse:
                    etage.salles[joueur.salle].ennemis[i].paralyse = False

                # GERER LA PERTE DE PV DU JOUEUR / LA POSSIBILITE QU'IL ESQUIVE AVEC LA COMPETENCE APPROPRIEE

                if collisions(etage.salles[joueur.salle].ennemis[i].hitbox_degats, joueur.hitbox):
                    if randrange(100) >= (5*session.competences[9]):
                        liste_rafraichir, joueur = \
                            rafraichir_vie(position_ecran_x, position_ecran_y, joueur, liste_rafraichir,
                                           joueur.points_de_vies-etage.salles[joueur.salle].ennemis[i].attaque,
                                           joueur.vie_maximum)
                    else:
                        if not joueur.invincible:
                            joueur.invincible = True
                            joueur.temps_depuis_invincible = pygame.time.get_ticks()

                # AFFICHER LE MONSTRE

                if etage.salles[joueur.salle].ennemis[i].paralyse:
                    liste_rafraichir.append([etage.salles[joueur.salle].ennemis[i].images.bas[6],
                                             (etage.salles[joueur.salle].ennemis[i].x+position_ecran_x,
                                              etage.salles[joueur.salle].ennemis[i].y+position_ecran_y,
                                              64, 64), 3])
                else:
                    liste_rafraichir.append([etage.salles[joueur.salle].ennemis[i].images.bas[tempo//8],
                                         (etage.salles[joueur.salle].ennemis[i].x+position_ecran_x,
                                          etage.salles[joueur.salle].ennemis[i].y+position_ecran_y,
                                          64, 64), 3])

    return etage, liste_rafraichir, joueur


def gerer_mort_monstres(etage, joueur, liste_rafraichir, position_ecran_x, position_ecran_y, session):

    global OBJETS

    i = 0
    while i < len(etage.salles[joueur.salle].ennemis):

        if etage.salles[joueur.salle].ennemis[i].mort:

            # MORT DES MONSTRES DE BASE

            if etage.salles[joueur.salle].ennemis[i].type == 0:

                # EFFACER MONSTRE

                liste_rafraichir.append([etage.salles[joueur.salle].image.subsurface(
                    (etage.salles[joueur.salle].ennemis[i].x, etage.salles[joueur.salle].ennemis[i].y, 64, 64)),
                    (etage.salles[joueur.salle].ennemis[i].x+position_ecran_x,
                     etage.salles[joueur.salle].ennemis[i].y+position_ecran_y,
                     64, 64), 0])

                # EFFACER BARRE DE VIE DU MONSTRE

                liste_rafraichir.append([etage.salles[joueur.salle].image.subsurface(
                    (etage.salles[joueur.salle].ennemis[i].minibarre.x,
                     etage.salles[joueur.salle].ennemis[i].minibarre.y, 64, 8)),
                    (position_ecran_x+etage.salles[joueur.salle].ennemis[i].minibarre.x,
                     position_ecran_y+etage.salles[joueur.salle].ennemis[i].minibarre.y, 64, 8), 1])

                # OBTENIR UN COEUR

                if randrange(25) < 5+session.competences[6]:
                    objet = Objet()
                    objet.x = etage.salles[joueur.salle].ennemis[i].x
                    objet.y = etage.salles[joueur.salle].ennemis[i].y
                    objet.type = 7
                    objet.image = OBJETS.subsurface((448, 0, 64, 64))
                    objet.hitbox.x = etage.salles[joueur.salle].ennemis[i].x
                    objet.hitbox.y = etage.salles[joueur.salle].ennemis[i].y
                    objet.hitbox.w = 64
                    objet.hitbox.h = 64
                    etage.salles[joueur.salle].objets.append(objet)

                # OBTENIR EXPERIENCE

                liste_rafraichir, session = \
                    rafraichir_xp(position_ecran_x, position_ecran_y, session, liste_rafraichir, session.xp+10)

                # RECUPERER MANA

                liste_rafraichir, joueur = \
                    rafraichir_mana(position_ecran_x, position_ecran_y, joueur, liste_rafraichir,
                                    session, joueur.mana+5+(2*session.competences[3]))

                del etage.salles[joueur.salle].ennemis[i]
                i -= 1

            # MORT DES MONSTRES A DISTANCE

            elif etage.salles[joueur.salle].ennemis[i].type == 1:

                # EFFACER LES ATTAQUES DU MONSTRE

                for attaque in etage.salles[joueur.salle].ennemis[i].attaques.entites:

                    # EFFACER LES PROJECTILES ENCORE EN VOL

                    if not attaque.detruit:

                        w = attaque.images[0].get_size()[0]
                        h = attaque.images[0].get_size()[1]

                        liste_rafraichir.append([etage.salles[joueur.salle].image.subsurface(
                            (attaque.x+16-w//2, attaque.y+16-h//2, w, h)),
                            (attaque.x+position_ecran_x+16-w//2, attaque.y+position_ecran_y+16-h//2, w, h), 4])

                    # EFFACER LES IMPACTS

                    else:
                        liste_rafraichir.append([etage.salles[joueur.salle].image.subsurface(
                            (attaque.x, attaque.y, 32, 32)),
                            (attaque.x+position_ecran_x, attaque.y+position_ecran_y, 32, 32), 4])

                # EFFACER MONSTRE

                liste_rafraichir.append([etage.salles[joueur.salle].image.subsurface(
                    (etage.salles[joueur.salle].ennemis[i].x, etage.salles[joueur.salle].ennemis[i].y, 64, 64)),
                    (etage.salles[joueur.salle].ennemis[i].x+position_ecran_x,
                     etage.salles[joueur.salle].ennemis[i].y+position_ecran_y,
                     64, 64), 0])

                # EFFACER BARRE DE VIE DU MONSTRE

                liste_rafraichir.append([etage.salles[joueur.salle].image.subsurface(
                    (etage.salles[joueur.salle].ennemis[i].minibarre.x,
                     etage.salles[joueur.salle].ennemis[i].minibarre.y, 64, 8)),
                    (position_ecran_x+etage.salles[joueur.salle].ennemis[i].minibarre.x,
                     position_ecran_y+etage.salles[joueur.salle].ennemis[i].minibarre.y, 64, 8), 1])

                # OBTENIR UN COEUR

                if randrange(25) < 5+session.competences[6]:
                    objet = Objet()
                    objet.x = etage.salles[joueur.salle].ennemis[i].x
                    objet.y = etage.salles[joueur.salle].ennemis[i].y
                    objet.type = 7
                    objet.image = OBJETS.subsurface((448, 0, 64, 64))
                    objet.hitbox.x = etage.salles[joueur.salle].ennemis[i].x
                    objet.hitbox.y = etage.salles[joueur.salle].ennemis[i].y
                    objet.hitbox.w = 64
                    objet.hitbox.h = 64
                    etage.salles[joueur.salle].objets.append(objet)

                # OBTENIR EXPERIENCE

                liste_rafraichir, session = \
                    rafraichir_xp(position_ecran_x, position_ecran_y, session, liste_rafraichir, session.xp+10)

                # RECUPERER MANA

                liste_rafraichir, joueur = \
                    rafraichir_mana(position_ecran_x, position_ecran_y, joueur, liste_rafraichir,
                                    session, joueur.mana+5+(2*session.competences[3]))

                del etage.salles[joueur.salle].ennemis[i]
                i -= 1

        i += 1

    return etage, liste_rafraichir, session


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


def charger_minimap(etage, joueur):

    # CREER L'IMAGE DE LA MINIMAP

    global MINIMAP

    minimap = pygame.Surface((128, 88))
    minimap.fill((255, 255, 255))
    minimap.set_colorkey((255, 255, 255))
    minimap.blit(MINIMAP.subsurface((0, 0, 128, 88)), (0, 0))

    for y in range(5):
        for x in range(5):
            for salle in etage.salles:
                if salle.x == etage.salles[joueur.salle].x+(x-2) and salle.y == etage.salles[joueur.salle].y+(y-2):
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
    global CARACTERES_32
    global CARACTERES_SELECTIONNES_32

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

    if menu.type == 3:  # CREER DES MENUS VERTICAUX *32

        nombre_de_lignes = 0
        ligne_actuelle = 0

        for i in range(len(menu.options)):

            # DECOUPER LES MESSAGES DE L'OPTION EN CHAINES SI BESOIN ET LEVER DES EXCEPTIONS S'IL Y A TROP DE TEXTE

            if len(menu.options[i].message)*16 < menu.w:
                menu.options[i].chaines = [menu.options[i].message]
            else:
                menu.options[i].chaines = menu.options[i].message.split(" ")

                for mot in menu.options[i].chaines:
                    if len(mot)*16 > menu.w:
                        raise ValueError("Les mots sont trop longs")

            nombre_de_lignes += len(menu.options[i].chaines)
            if nombre_de_lignes*33 > menu.h:
                raise ValueError("Les options sont trop epaisses / trop nombreuses")

            # CALCULER LES COORDONNEES DE L'OPTION

            plus_longue_chaine_option = 0

            for j in range(len(menu.options[i].chaines)):
                if len(menu.options[i].chaines[j]) > plus_longue_chaine_option:
                    plus_longue_chaine_option = len(menu.options[i].chaines[j])

            menu.options[i].w = 16*plus_longue_chaine_option
            menu.options[i].x = menu.x+((menu.w//2)-(menu.options[i].w//2))

            # CREER L'IMAGE DE L'OPTION

        for i in range(len(menu.options)):

            menu.options[i].h = 32*len(menu.options[i].chaines)
            menu.options[i].y = menu.y+ligne_actuelle*32+((menu.h-nombre_de_lignes*32)//(len(menu.options)+1))*(i+1)
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
                    menu.options[i].images[0].blit(CARACTERES_32.subsurface(
                        ((ord(menu.options[i].chaines[j][k]) % 10)*16,
                         (ord(menu.options[i].chaines[j][k])//10)*32, 16, 32)),
                        (((menu.options[i].w-(len(menu.options[i].chaines[j])*16))//2)+(k*16), j*32))

                    menu.options[i].images[1].blit(CARACTERES_SELECTIONNES_32.subsurface(
                        ((ord(menu.options[i].chaines[j][k]) % 10)*16,
                         (ord(menu.options[i].chaines[j][k])//10)*32, 16, 32)),
                        (k*16, j*32))

    elif menu.type == 4:  # CREER DES MENUS HORIZONTAUX *32

        # LEVER DES EXCEPTIONS S'IL Y A TROP DE TEXTE

        nombre_de_caracteres = 0
        for option in menu.options:
            nombre_de_caracteres += len(option.message)

        if nombre_de_caracteres*17 > menu.w:
            raise ValueError("Le nombre d'options / La taille des mots est/sont trop élevé(es).")
        if menu.h < 32:
            raise ValueError("Le menu n'est pas assez épais. (<64px)")

        # CREER LES OPTIONS

        nombre_de_caracteres_actuel = 0
        for i in range(len(menu.options)):

            # CALCULER LES COORDONEES DE L'OPTION

            menu.options[i].y = menu.y+((menu.h-32)//2)
            menu.options[i].x = menu.x+(nombre_de_caracteres_actuel*16)+((i+1)*((menu.w-nombre_de_caracteres*16)//(len(menu.options)+1)))
            menu.options[i].h = 32
            menu.options[i].w = len(menu.options[i].message)*16

            # CREER L'IMAGE DE L'OPTION

            menu.options[i].images = list()
            for j in range(2):
                menu.options[i].images.append(pygame.Surface((menu.options[i].w, menu.options[i].h)))
                menu.options[i].images[j].fill((255, 255, 255))
                menu.options[i].images[j].set_colorkey((255, 255, 255))

            for j in range(len(menu.options[i].message)):
                menu.options[i].images[0].blit(CARACTERES_32.subsurface(
                    ((ord(menu.options[i].message[j]) % 10)*16, (ord(menu.options[i].message[j])//10)*32, 16, 32)),
                    (j*16, 0))
                menu.options[i].images[1].blit(CARACTERES_SELECTIONNES_32.subsurface(
                    ((ord(menu.options[i].message[j]) % 10)*16, (ord(menu.options[i].message[j])//10)*32, 16, 32)),
                    (j*16, 0))

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
            position_souris = [entree.pos[0], entree.pos[1]]

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

    pygame.key.set_repeat(150, 100)

    # CREER UNE SESSION VIDE

    session = Session()
    session.competences = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    session.points_de_competences = 0
    session.sorts = [0, 0]
    session.points_de_sorts = 0
    session.niveau = 0
    session.xp = 0
    session.partie = False
    session.map = None
    session.joueur = None
    session.version = VERSION
    session.nom = str()
    session.pieces = 0

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

            if entree.type == pygame.MOUSEBUTTONUP:
                if entree.button == 1:
                    for i in range(len(menu.options)):
                        if menu.options[i].x+menu.options[i].w > entree.pos[0] > menu.options[i].x and \
                           menu.options[i].y+menu.options[i].h > entree.pos[1] > menu.options[i].y:
                            continuer = False
                            choix = i+1

            if entree.type == pygame.MOUSEMOTION:
                position_souris = [entree.pos[0], entree.pos[1]]

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


def charger_images_monstres(etage):

    global PERSONNAGES

    for i in range(len(etage.salles)):
        for j in range(len(etage.salles[i].ennemis)):

            # CHARGER LES SKINS DES MONSTRES

            etage.salles[i].ennemis[j].images.bas = []
            etage.salles[i].ennemis[j].images.haut = []
            etage.salles[i].ennemis[j].images.droite = []
            etage.salles[i].ennemis[j].images.gauche = []

            for l in range(6):
                etage.salles[i].ennemis[j].images.bas.append(
                    PERSONNAGES.subsurface((l*64, (etage.salles[i].ennemis[j].type+1)*64, 64, 64)))
                etage.salles[i].ennemis[j].images.haut.append(
                    PERSONNAGES.subsurface(((l+6)*64, (etage.salles[i].ennemis[j].type+1)*64, 64, 64)))
                etage.salles[i].ennemis[j].images.droite.append(
                    PERSONNAGES.subsurface(((l+12)*64, (etage.salles[i].ennemis[j].type+1)*64, 64, 64)))
                etage.salles[i].ennemis[j].images.gauche.append(
                    PERSONNAGES.subsurface(((l+18)*64, (etage.salles[i].ennemis[j].type+1)*64, 64, 64)))
                etage.salles[i].ennemis[j].images.bas[l].set_colorkey((255, 255, 255))
                etage.salles[i].ennemis[j].images.haut[l].set_colorkey((255, 255, 255))
                etage.salles[i].ennemis[j].images.droite[l].set_colorkey((255, 255, 255))
                etage.salles[i].ennemis[j].images.gauche[l].set_colorkey((255, 255, 255))

            etage.salles[i].ennemis[j].images.bas.append(
                PERSONNAGES.subsurface((1536, (etage.salles[i].ennemis[j].type+1)*64, 64, 64)))
            etage.salles[i].ennemis[j].images.bas[6].set_colorkey((255, 255, 255))

            # CHARGER LA MINIBARRE DES MONSTRES

            etage.salles[i].ennemis[j].minibarre.image = pygame.Surface((64, 8))
            etage.salles[i].ennemis[j].minibarre.image.fill((0, 0, 0))
            etage.salles[i].ennemis[j].minibarre.image.set_colorkey((255, 255, 255))
            etage.salles[i].ennemis[j].minibarre.image.fill(
                (255, 0, 0), (2, 2, int((etage.salles[i].ennemis[j].points_de_vies/etage.salles[i].ennemis[j].points_de_vies_maximum)*60), 4))
            etage.salles[i].ennemis[j].minibarre.image.fill(
                (255, 255, 255), (2+int((etage.salles[i].ennemis[j].points_de_vies/etage.salles[i].ennemis[j].points_de_vies_maximum)*60), 2,
                                  62-(2+int((etage.salles[i].ennemis[j].points_de_vies/etage.salles[i].ennemis[j].points_de_vies_maximum)*60)), 4))

            # ANNULER LES ATTAQUES DES MONSTRES

            etage.salles[i].ennemis[j].attaques = Attaque()

    return etage


def charger_images_objets(etage):

    global OBJETS
    global OBJETS_RARES

    for i in range(len(etage.salles)):

        for j in range(len(etage.salles[i].objets)):

            if etage.salles[i].objets[j].type < 1000:
                etage.salles[i].objets[j].image = \
                    OBJETS.subsurface(((etage.salles[i].objets[j].type % 10)*64,
                                       (etage.salles[i].objets[j].type//10)*64, 64, 64))

            if etage.salles[i].objets[j].type >= 1000:
                etage.salles[i].objets[j].type -= 1000
                etage.salles[i].objets[j].image = \
                    OBJETS_RARES.subsurface(((etage.salles[i].objets[j].type % 10)*64,
                                             (int(etage.salles[i].objets[j].type/10))*64, 64, 64))
                etage.salles[i].objets[j].type += 1000

            etage.salles[i].objets[j].image.set_colorkey((255, 255, 255))

    return etage


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
    message.image.fill((100, 100, 255))
    message.image.fill((200, 200, 255), (2, 2, message.w-4, message.h-4))

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
    menu.options[2].message = "Réinitialiser"
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

        # MISE A JOUR ET EFFACAGE DE LA FENETRE

        fenetre_effaceur = [fenetre[0], fenetre[1], fenetre[2], fenetre[3]]
        fenetre[5], fenetre[6], fenetre[7], fenetre[8] = -1, -1, fenetre[5], fenetre[6]

        if (fenetre[7] != -1 and fenetre[8] != -1) or (fenetre[5] != -1 and fenetre[6] != -1):
            liste_rafraichir.append([
                FOND.subsurface((fenetre_effaceur[0], fenetre_effaceur[1], fenetre_effaceur[2], fenetre_effaceur[3])),
                (fenetre_effaceur[0], fenetre_effaceur[1], fenetre_effaceur[2], fenetre_effaceur[3]), 0])

        if choix[0] != -1 or choix[1] != -1:
            fenetre[7], fenetre[8] = -1, -1
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

        # AFFICHER LA FENETRE

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
                          str(2*liste[0])+" points de degats supplementaires\n"

            chaine += "\nAmelioration du niveau suivant:\n"

            if liste[0] == 3:
                chaine += "Aucune\n"
            else:
                chaine += "Vos attaques infligent\n" + \
                          str(2*(liste[0]+1))+" points de degats supplementaires\n"

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
                chaine += "Vos points de vie maximums sont augmentes de "+str(liste[2]*10)+"\n"

            chaine += "\nAmelioration du niveau suivant:\n"

            if liste[2] == 2:
                chaine += "Aucune\n"
            else:
                chaine += "Vos points de vie maximums sont augmentes de "+str((liste[2]+1)*10)+"\n"

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
                chaine += "Vous gagnez "+str(2*liste[3])+" points de mana supplementaires\n" \
                          "lorsque vous tuez un ennemi\n"

            chaine += "\nAmelioration du niveau suivant:\n"

            if liste[3] == 2:
                chaine += "Aucune\n"
            else:
                chaine += "Vous gagnez "+str(2*(liste[3]+1))+" points de mana supplementaires\n" \
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
            else:
                chaine += "Vos attaques de base se deplacent "+str(10*liste[4])+" % plus vite\n"

            chaine += "\nAmelioration du niveau suivant:\n"

            if liste[4] == 3:
                chaine += "Aucune\n"
            else:
                chaine += "Vos attaques de base se deplacent "+str(10*(liste[4]+1))+" % plus vite\n"

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
                chaine += "Vous avez "+str(20*liste[6])+"% de chances supplementaires\n" \
                          "d'obtenir un coeur sur les ennemis\n"

            chaine += "\nAmelioration du niveau suivant:\n"

            if liste[6] == 2:
                chaine += "Aucune\n"
            else:
                chaine += "Vous avez "+str(20*(liste[6]+1))+"% de chances supplementaires\n" \
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
                chaine += "Votre mana maximum augmente de "+str(10*liste[7])+"\n"

            chaine += "\nAmelioration du niveau suivant:\n"

            if liste[7] == 2:
                chaine += "Aucune\n"
            else:
                chaine += "Votre mana maximum augmente de "+str(10*(liste[7]+1))+"\n"

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
                chaine += "Vos attaques explosent a l'impact et infligent "+str(25*liste[8])+"%\n" \
                          "d'une attaque normale aux ennemis proches\n"

            chaine += "\nAmelioration du niveau suivant:\n"

            if liste[8] == 2:
                chaine += "Aucune\n"
            else:
                chaine += "Vos attaques explosent a l'impact et infligent "+str(25*(liste[8]+1))+"%\n" \
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
                chaine += "Lorsqu'un ennemi vous touche, vous avez "+str(5*liste[9])+"%\n" \
                          "de chances d'obtenir un temps d'invincibilite\nsans perdre de points de vie\n"

            chaine += "\nAmelioration du niveau suivant:\n"

            if liste[9] == 3:
                chaine += "Aucune\n"
            else:
                chaine += "Lorsqu'un ennemi vous touche, vous avez "+str(5*(liste[9]+1))+"%\n" \
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
                chaine += "Vous regagnez "+str(liste[10])+" points de vie a chaque\n" \
                          "fois que vous attaquez un ennemi \n" \
                          "avec une attaque de base\n"

            chaine += "\nAmelioration du niveau suivant:\n"

            if liste[10] == 3:
                chaine += "Aucune\n"
            else:
                chaine += "Vous regagnez "+str(liste[10]+1)+" points de vie a chaque\n" \
                          "fois que vous attaquez un ennemi \n" \
                          "avec une attaque de base\n"

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
                chaine += "Vous gagnez "+str(liste[11])+" points de mana a chaque\n" \
                          "fois que vous attaquez un ennemi\n" \
                          "avec une attaque de base\n"

            chaine += "\nAmelioration du niveau suivant:\n"

            if liste[11] == 3:
                chaine += "Aucune\n"
            else:
                chaine += "Vous gagnez "+str(liste[11]+1)+" points de mana a chaque\n" \
                          "fois que vous attaquez un ennemi\n" \
                          "avec une attaque de base\n"

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


def afficher_minibar(etage, joueur, position_ecran_x, position_ecran_y, liste_rafraichir):

    for ennemi in etage.salles[joueur.salle].ennemis:

        # EFFACER L'ANCIENNE MINIBARRE

        liste_rafraichir.append([etage.salles[joueur.salle].image.subsurface(
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


def afficher_game_over(ecran, resolution):

    global CARACTERES

    messages = ["Game over"]
    for i in range(len(messages)):
        for j in range(len(messages[i])):
            ecran.blit(pygame.transform.scale2x(CARACTERES.subsurface(((ord(messages[i][j]) % 10)*32, (ord(messages[i][j])//10)*64, 32, 64))),
                       (((resolution.current_w-(64*len(messages[i])))//2)+(64*j),
                        ((resolution.current_h-(130*len(messages)))//2)+(130*i)))

    pygame.display.flip()

    pygame.time.wait(3000)

    return 0


def choisir_raccourcis(ecran, resolution, liste_rafraichir, liste_messages, raccourcis):

    global CARACTERES
    global CARACTERES_SELECTIONNES
    global FOND

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

    # RECUPERER UNE COPIE DES RACCOURCIS

    raccourcis_copie = [[pygame.K_w, "Defaut"],
                        [pygame.K_s, "Defaut"],
                        [pygame.K_a, "Defaut"],
                        [pygame.K_d, "Defaut"],
                        [pygame.K_e, "Defaut"],
                        [pygame.K_EXCLAIM, "Defaut"],
                        [pygame.K_AT, "Defaut"],
                        [pygame.K_SEMICOLON, "Defaut"]]
    try:
        with open("raccourcis.txt", "r") as fichier_raccourcis:
            raccourcis_obtenus = fichier_raccourcis.read().split("\n")
            for i in range(len(raccourcis_obtenus)):
                raccourcis_copie[i] = raccourcis_obtenus[i].split("=")
                raccourcis_copie[i][0] = int(raccourcis_copie[i][0])
    except:
        pass

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
    for i in range(8):
        menu_description.options.append(Options_Menu())
    menu_description.options[0].message = "Avancer"
    menu_description.options[1].message = "Reculer"
    menu_description.options[2].message = "Aller a gauche"
    menu_description.options[3].message = "Aller a droite"
    menu_description.options[4].message = "Poser une bombe"
    menu_description.options[5].message = "Sort 1"
    menu_description.options[6].message = "Sort 2"
    menu_description.options[7].message = "Afficher la carte"
    menu_description.x = 100
    menu_description.y = 100
    menu_description.w = resolution.current_w-(408+2*espace_restant)
    menu_description.h = len(menu_description.options)*128
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

        liste_messages, liste_rafraichir = afficher_messages(liste_messages, liste_rafraichir, resolution)
        liste_rafraichir, temps_actuel, tempo = gerer_temps(ecran, tempo, liste_rafraichir, temps_actuel)
        choix[0] = 0

        # GERER LES ENTREES UTILISATEURS

        for entree in pygame.event.get():

            if entree.type == pygame.KEYDOWN:  # CHANGER LE RACCOURCIS
                if entree.unicode != str() and choix[1] != 0:

                    raccourcis_copie[choix[1]-1] = [entree.key, entree.unicode]

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
                                pygame.Surface((liste_cadre[2], liste_cadre[3]-100+liste_cadre[1])),
                                (liste_cadre[0], 100, liste_cadre[2], liste_cadre[3]-100+liste_cadre[1]), 0])

                    # EFFACER LE MESSAGE D'AIDE

                    chaine = "Appuyez sur une touche"
                    espace_restant = (resolution.current_w-32*len(chaine))//2
                    liste_rafraichir.append([FOND.subsurface((espace_restant, 18, len(chaine)*32, 64)),
                                             (espace_restant, 18, len(chaine)*32, 64), 0])

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

                        if menu_touches.options[choix[1]-1].y < 100:
                            liste_rafraichir.append([pygame.Surface(
                                (menu_touches.options[choix[1]-1].w, menu_touches.options[choix[1]-1].h-(100-menu_touches.options[choix[1]-1].y))),
                                (menu_touches.options[choix[1]-1].x, 100, menu_touches.options[choix[1]-1].w,
                                 menu_touches.options[choix[1]-1].h-(100-menu_touches.options[choix[1]-1].y)), 7])

                    # CHANGER LA LISTE DES TOUCHES

                    menu_touches.options[choix[1]-1].message = entree.unicode
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

                            # EFFACER LE CADRE S'IL Y EN A UN

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
                                            pygame.Surface((liste_cadre[2], liste_cadre[3]-100+liste_cadre[1])),
                                            (liste_cadre[0], 100, liste_cadre[2], liste_cadre[3]-100+liste_cadre[1]), 0])

                            # CREER LES NOUVELLES COORDONNEES DU CADRE

                            liste_cadre[0] = menu_description.options[i].x-4
                            liste_cadre[1] = menu_description.options[i].y-4
                            liste_cadre[2] = menu_description.options[i].w+8
                            liste_cadre[3] = menu_description.options[i].h+8
                            liste_cadre[4] = pygame.Surface((liste_cadre[2], liste_cadre[3]))
                            liste_cadre[4].fill((255, 255, 0))
                            liste_cadre[4].fill((255, 255, 255), (2, 2, menu_description.options[i].w+4, menu_description.options[i].h+4))
                            liste_cadre[4].set_colorkey((255, 255, 255))

                            # AFFICHER LE CADRE

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
                                        (liste_cadre[0], 100, liste_cadre[2], liste_cadre[3]-(100-liste_cadre[1])), 7])

                            # EFFACER LE MESSAGE D'AIDE

                            chaine = "Selectionnez un raccourcis"
                            espace_restant = (resolution.current_w-32*len(chaine))//2
                            liste_rafraichir.append([FOND.subsurface((espace_restant, 18, len(chaine)*32, 64)),
                                                     (espace_restant, 18, len(chaine)*32, 64), 0])

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

                        # EFFACER LE CADRE, LE DEPLACER ET LE REAFFICHER

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
                                        (liste_cadre[0], 100, liste_cadre[2], liste_cadre[3]-(100-liste_cadre[1])), 0])

                            if entree.button == 5:
                                liste_cadre[1] -= 30
                            if entree.button == 4:
                                liste_cadre[1] += 30

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
                                        (liste_cadre[0], 100, liste_cadre[2], liste_cadre[3]-(100-liste_cadre[1])), 7])

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

                if menu_description.options[i].y < 100:

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

        # AFFICHER LES MESSAGES D'AIDE

        if choix[1]==0:
            chaine = "Selectionnez un raccourcis"
        else:
            chaine = "Appuyez sur une touche"
        espace_restant = (resolution.current_w-32*len(chaine))//2
        for i in range(len(chaine)):
            liste_rafraichir.append([CARACTERES.subsurface(((ord(chaine[i]) % 10)*32, (ord(chaine[i])//10)*64, 32, 64)),
                                     (espace_restant+(32*i), 18, 32, 64), 7])

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


def afficher_animation_joueur(joueur, etage, position_ecran_x, position_ecran_y, liste_rafraichir):

    if joueur.animation_tete.activee:

        if joueur.animation_tete.temps_restant == 0:
            liste_rafraichir.append([etage.salles[joueur.salle].image.subsurface(
                        (joueur.animation_tete.x, joueur.animation_tete.y,
                         joueur.animation_tete.w, joueur.animation_tete.h)),
                        (joueur.animation_tete.x+position_ecran_x, joueur.animation_tete.y+position_ecran_y,
                         joueur.animation_tete.w, joueur.animation_tete.h), 0])
            joueur.animation_tete.activee = False
        else:
            liste_rafraichir.append([etage.salles[joueur.salle].image.subsurface(
                (joueur.animation_tete.x, joueur.animation_tete.y,
                 joueur.animation_tete.w, joueur.animation_tete.h)),
                (joueur.animation_tete.x+position_ecran_x, joueur.animation_tete.y+position_ecran_y,
                 joueur.animation_tete.w, joueur.animation_tete.h), 0])

            joueur.animation_tete.x = joueur.x
            joueur.animation_tete.y = joueur.y-25
            a = int(len(joueur.animation_tete.images)-((joueur.animation_tete.temps_restant*len(joueur.animation_tete.images))/joueur.animation_tete.temps_total))

            liste_rafraichir.append([joueur.animation_tete.images[a], (joueur.animation_tete.x+position_ecran_x,
                                                                       joueur.animation_tete.y+position_ecran_y,
                                                                       joueur.animation_tete.w,
                                                                       joueur.animation_tete.h), 4])
            joueur.animation_tete.temps_restant -= 1

    return liste_rafraichir, joueur


def choisir_sorts(ecran, resolution, liste_rafraichir, liste_messages, session):

    global ICONES_SORTS
    global CARACTERES
    global FOND

    # CREER LE MENU VALIDER/RETOUR/REINITIALISER

    menu = Menu()
    menu.x = 0
    menu.y = resolution.current_h-96
    menu.w = resolution.current_w
    menu.h = 96
    for i in range(3):
        menu.options.append(Options_Menu())

    menu.options[0].message = "Valider"
    menu.options[1].message = "Retour"
    menu.options[2].message = "Réinitialiser"
    menu.type = 2
    menu = creer_images_et_positions_menu(menu)

    # CREER LE MENU DES ONGLETS

    menu_onglets = Menu()
    menu_onglets.x = 0
    menu_onglets.y = 96
    menu_onglets.w = resolution.current_w
    menu_onglets.h = 128
    for i in range(2):
        menu_onglets.options.append(Options_Menu())

    menu_onglets.options[0].message = "Poisons"
    menu_onglets.options[1].message = "Maitrise du temps"
    menu_onglets.type = 2
    menu_onglets = creer_images_et_positions_menu(menu_onglets)

    # INITIALISATION DE VARIABLES

    liste = list()
    for i in range(len(menu_onglets.options)):
        liste.append(session.sorts[i])
    points = session.points_de_sorts

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

    # choix = [onglet, menu, competence_ajouter, competence_retirer]
    choix = [1, 0, 0, 0]
    position_souris = [0, 0]
    tempo = 0
    temps_actuel = pygame.time.get_ticks()
    continuer = True

    # BOUCLE DE LA PAGE

    while continuer:

        # ONGLET POISONS

        if choix[0] == 1:

            liste_rafraichir = mettre_fond(ecran)
            # fenetre = [x, y, w, h, image, arbre y, arbre x, ancien arbre y, ancien arbre x]
            fenetre = [0, 0, 0, 0, 0, -1, -1, -1, -1]

            # AFFICHER L'ONGLET SELECTIONNE

            trait = pygame.Surface((resolution.current_w, 2))
            trait.fill((255, 255, 0))
            liste_rafraichir.append([trait, (0, menu_onglets.options[choix[0]-1].y+menu_onglets.options[choix[0]-1].h,
                                             resolution.current_w, 2), 1])
            liste_rafraichir.append([
                FOND.subsurface((menu_onglets.options[choix[0]-1].x, menu_onglets.options[choix[0]-1].y+menu_onglets.options[choix[0]-1].h,
                                 menu_onglets.options[choix[0]-1].w, 2)),
                (menu_onglets.options[choix[0]-1].x, menu_onglets.options[choix[0]-1].y+menu_onglets.options[choix[0]-1].h,
                 menu_onglets.options[choix[0]-1].w, 2), 2])

            for i in range(len(menu_onglets.options)):

                trait = pygame.Surface((2, menu_onglets.options[i].h))
                trait.fill((255, 255, 0))
                liste_rafraichir.append([trait, (menu_onglets.options[i].x-2, menu_onglets.options[i].y,
                                                 2, menu_onglets.options[i].h), 1])

                trait = pygame.Surface((menu_onglets.options[i].w, 2))
                trait.fill((255, 255, 0))
                liste_rafraichir.append([trait, (menu_onglets.options[i].x, menu_onglets.options[i].y-2,
                                                 menu_onglets.options[i].w, 2), 1])

                trait = pygame.Surface((2, menu_onglets.options[i].h))
                trait.fill((255, 255, 0))
                liste_rafraichir.append([trait, (menu_onglets.options[i].x+menu_onglets.options[i].w,
                                                 menu_onglets.options[i].y, 2, menu_onglets.options[i].h), 1])

            # CREER L'ARBRE DES SORTS DE POISONS

            arbre_de_sorts = [Menu(), Menu(), Menu()]

            for i in range(len(arbre_de_sorts)):
                arbre_de_sorts[i].x = 0
                arbre_de_sorts[i].y = 224+(resolution.current_h-320)-((i+1)*((resolution.current_h-320)//len(arbre_de_sorts)))
                arbre_de_sorts[i].w = resolution.current_w
                arbre_de_sorts[i].h = (resolution.current_h-320)//len(arbre_de_sorts)
                arbre_de_sorts[i].type = 2

            # ETAGE 0

            arbre_de_sorts[0].options.append(Options_Menu())
            arbre_de_sorts[0].options[0].images = [pygame.Surface((64, 64)),
                                                   pygame.Surface((64, 64)),
                                                   ICONES_SORTS.subsurface((640, 0, 64, 64))]
            arbre_de_sorts[0].options[0].images[1].fill((255, 0, 0))
            arbre_de_sorts[0].options[0].images[1].blit(ICONES_SORTS.subsurface((2, 2, 60, 60)), (2, 2))
            arbre_de_sorts[0].options[0].images[0].fill((0, 0, 255))
            arbre_de_sorts[0].options[0].images[0].blit(ICONES_SORTS.subsurface((2, 2, 60, 60)), (2, 2))

            # ETAGE 1

            for i in range(2):
                arbre_de_sorts[1].options.append(Options_Menu())
                arbre_de_sorts[1].options[i].images = [pygame.Surface((64, 64)),
                                                       pygame.Surface((64, 64)),
                                                       ICONES_SORTS.subsurface((704+(64*i), 0, 64, 64))]
                arbre_de_sorts[1].options[i].images[1].fill((255, 0, 0))
                arbre_de_sorts[1].options[i].images[1].blit(ICONES_SORTS.subsurface((66+(64*i), 2, 60, 60)), (2, 2))
                arbre_de_sorts[1].options[i].images[0].fill((0, 0, 255))
                arbre_de_sorts[1].options[i].images[0].blit(ICONES_SORTS.subsurface((66+(64*i), 2, 60, 60)), (2, 2))

            # ETAGE 2

            for i in range(4):
                arbre_de_sorts[2].options.append(Options_Menu())
                arbre_de_sorts[2].options[i].images = [pygame.Surface((64, 64)),
                                                       pygame.Surface((64, 64)),
                                                       ICONES_SORTS.subsurface((832+(64*i), 0, 64, 64))]
                arbre_de_sorts[2].options[i].images[1].fill((255, 0, 0))
                arbre_de_sorts[2].options[i].images[1].blit(ICONES_SORTS.subsurface((194+(64*i), 2, 60, 60)), (2, 2))
                arbre_de_sorts[2].options[i].images[0].fill((0, 0, 255))
                arbre_de_sorts[2].options[i].images[0].blit(ICONES_SORTS.subsurface((194+(64*i), 2, 60, 60)), (2, 2))

            # CALCULER L'EMPLACEMENT DE CHAQUE OPTION

            for i in range(len(arbre_de_sorts)):
                for j in range(len(arbre_de_sorts[i].options)):
                    arbre_de_sorts[i].options[j].w = 64
                    arbre_de_sorts[i].options[j].h = 64
                    arbre_de_sorts[i].options[j].x = (((resolution.current_w-(len(arbre_de_sorts[i].options)*64))//(len(arbre_de_sorts[i].options)+1))*(j+1))+(j*64)
                    arbre_de_sorts[i].options[j].y = arbre_de_sorts[i].y+((arbre_de_sorts[i].h-64)//2)

            # BOUCLE DE L'ONGLET

            while choix[0] == 1:

                # RAFRAICHIR L'IMAGE

                liste_messages, liste_rafraichir = afficher_messages(liste_messages, liste_rafraichir, resolution)
                liste_rafraichir, temps_actuel, tempo = gerer_temps(ecran, tempo, liste_rafraichir, temps_actuel)

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

                # DEFINIR L'ETAT DE L'ARBRE

                liste_valides = [liste[0] != 0,
                                 (liste[0] == 2 or liste[0] == 4 or liste[0] == 5),
                                 (liste[0] == 3 or liste[0] == 6 or liste[0] == 7),
                                 liste[0] == 4,
                                 liste[0] == 5,
                                 liste[0] == 6,
                                 liste[0] == 7]

                liste_impossibles = [False,
                                     (not liste_valides[0] or liste_valides[2]),
                                     (not liste_valides[0] or liste_valides[1]),
                                     (not liste_valides[1] or liste_valides[4]),
                                     (not liste_valides[1] or liste_valides[3]),
                                     (not liste_valides[2] or liste_valides[6]),
                                     (not liste_valides[2] or liste_valides[5])]

                # RAFRAICHIR LES DONNEES DE LA FENETRE ET L'EFFACER

                fenetre_effaceur = [fenetre[0], fenetre[1], fenetre[2], fenetre[3]]
                fenetre[5], fenetre[6], fenetre[7], fenetre[8] = -1, -1, fenetre[5], fenetre[6]

                if (fenetre[7] != -1 and fenetre[8] != -1) or (fenetre[5] != -1 and fenetre[6] != -1):
                    liste_rafraichir.append([
                        FOND.subsurface((fenetre_effaceur[0], fenetre_effaceur[1], fenetre_effaceur[2], fenetre_effaceur[3])),
                        (fenetre_effaceur[0], fenetre_effaceur[1], fenetre_effaceur[2], fenetre_effaceur[3]), 0])

                if choix[2] != 0 or fenetre[3] != 0:
                    fenetre[7], fenetre[8] = -1, -1
                choix = [choix[0], 0, 0, 0]

                # GERER LES ENTREES UTILISATEUR

                for entree in pygame.event.get():
                    if entree.type == pygame.MOUSEBUTTONUP:

                        if entree.button == 1:
                            for i in range(len(menu.options)):
                                if menu.options[i].x+menu.options[i].w > entree.pos[0] > menu.options[i].x and \
                                   menu.options[i].y+menu.options[i].h > entree.pos[1] > menu.options[i].y:
                                    choix[1] = i+1
                            for i in range(len(menu_onglets.options)):
                                if menu_onglets.options[i].x+menu_onglets.options[i].w > entree.pos[0] > menu_onglets.options[i].x and \
                                   menu_onglets.options[i].y+menu_onglets.options[i].h > entree.pos[1] > menu_onglets.options[i].y:
                                    choix[0] = i+1
                            if arbre_de_sorts[0].options[0].x+arbre_de_sorts[0].options[0].w > entree.pos[0] > arbre_de_sorts[0].options[0].x and \
                               arbre_de_sorts[0].options[0].y+arbre_de_sorts[0].options[0].h > entree.pos[1] > arbre_de_sorts[0].options[0].y:
                                choix[2] = 1
                            for i in range(len(arbre_de_sorts[1].options)):
                                if arbre_de_sorts[1].options[i].x+arbre_de_sorts[1].options[i].w > entree.pos[0] > arbre_de_sorts[1].options[i].x and \
                                   arbre_de_sorts[1].options[i].y+arbre_de_sorts[1].options[i].h > entree.pos[1] > arbre_de_sorts[1].options[i].y:
                                    choix[2] = i+2
                            for i in range(len(arbre_de_sorts[2].options)):
                                if arbre_de_sorts[2].options[i].x+arbre_de_sorts[2].options[i].w > entree.pos[0] > arbre_de_sorts[2].options[i].x and \
                                   arbre_de_sorts[2].options[i].y+arbre_de_sorts[2].options[i].h > entree.pos[1] > arbre_de_sorts[2].options[i].y:
                                    choix[2] = i+4

                        if entree.button == 3:
                            if arbre_de_sorts[0].options[0].x+arbre_de_sorts[0].options[0].w > entree.pos[0] > arbre_de_sorts[0].options[0].x and \
                               arbre_de_sorts[0].options[0].y+arbre_de_sorts[0].options[0].h > entree.pos[1] > arbre_de_sorts[0].options[0].y:
                                choix[3] = 1
                            for i in range(len(arbre_de_sorts[1].options)):
                                if arbre_de_sorts[1].options[i].x+arbre_de_sorts[1].options[i].w > entree.pos[0] > arbre_de_sorts[1].options[i].x and \
                                   arbre_de_sorts[1].options[i].y+arbre_de_sorts[1].options[i].h > entree.pos[1] > arbre_de_sorts[1].options[i].y:
                                    choix[3] = i+2
                            for i in range(len(arbre_de_sorts[2].options)):
                                if arbre_de_sorts[2].options[i].x+arbre_de_sorts[2].options[i].w > entree.pos[0] > arbre_de_sorts[2].options[i].x and \
                                   arbre_de_sorts[2].options[i].y+arbre_de_sorts[2].options[i].h > entree.pos[1] > arbre_de_sorts[2].options[i].y:
                                    choix[3] = i+4

                    if entree.type == pygame.MOUSEMOTION:
                        position_souris = [entree.pos[0], entree.pos[1]]

                # AFFICHER LE MENU VALIDER/RETOUR/REINITIALISER

                for i in range(len(menu.options)):
                    if menu.options[i].x+menu.options[i].w > position_souris[0] > menu.options[i].x and \
                       menu.options[i].y+menu.options[i].h > position_souris[1] > menu.options[i].y:
                        liste_rafraichir.append([menu.options[i].images[1], (menu.options[i].x, menu.options[i].y,
                                                                             menu.options[i].w, menu.options[i].h), 7])
                    else:
                        liste_rafraichir.append([menu.options[i].images[0], (menu.options[i].x, menu.options[i].y,
                                                                             menu.options[i].w, menu.options[i].h), 7])

                # AFFICHER LE MENU DES ONGLETS

                for i in range(len(menu_onglets.options)):
                    if menu_onglets.options[i].x+menu_onglets.options[i].w > position_souris[0] > menu_onglets.options[i].x and \
                       menu_onglets.options[i].y+menu_onglets.options[i].h > position_souris[1] > menu_onglets.options[i].y:
                        liste_rafraichir.append([menu_onglets.options[i].images[1],
                                                 (menu_onglets.options[i].x, menu_onglets.options[i].y,
                                                  menu_onglets.options[i].w, menu_onglets.options[i].h), 7])
                    else:
                        liste_rafraichir.append([menu_onglets.options[i].images[0],
                                                 (menu_onglets.options[i].x, menu_onglets.options[i].y,
                                                  menu_onglets.options[i].w, menu_onglets.options[i].h), 7])

                # AFFICHER L'ARBRE DE SORTS

                i = 0
                for j in range(len(arbre_de_sorts)):
                    for k in range(len(arbre_de_sorts[j].options)):
                        if liste_valides[i]:
                            liste_rafraichir.append(
                                [arbre_de_sorts[j].options[k].images[1],
                                 (arbre_de_sorts[j].options[k].x, arbre_de_sorts[j].options[k].y,
                                  arbre_de_sorts[j].options[k].w, arbre_de_sorts[j].options[k].h,), 7])
                        if liste_impossibles[i]:
                            liste_rafraichir.append(
                                [arbre_de_sorts[j].options[k].images[2],
                                 (arbre_de_sorts[j].options[k].x, arbre_de_sorts[j].options[k].y,
                                  arbre_de_sorts[j].options[k].w, arbre_de_sorts[j].options[k].h,), 7])
                        if not liste_impossibles[i] and not liste_valides[i]:
                            liste_rafraichir.append(
                                [arbre_de_sorts[j].options[k].images[0],
                                 (arbre_de_sorts[j].options[k].x, arbre_de_sorts[j].options[k].y,
                                  arbre_de_sorts[j].options[k].w, arbre_de_sorts[j].options[k].h,), 7])
                        i += 1

                        if arbre_de_sorts[j].options[k].x+arbre_de_sorts[j].options[k].w > position_souris[0] > arbre_de_sorts[j].options[k].x and \
                           arbre_de_sorts[j].options[k].y+arbre_de_sorts[j].options[k].h > position_souris[1] > arbre_de_sorts[j].options[k].y:
                            fenetre[5] = j
                            fenetre[6] = k

                # AFFICHER LA FENETRE

                fenetre[0] = position_souris[0]
                fenetre[1] = position_souris[1]

                if fenetre[5] != -1 and fenetre[6] != -1:
                    fenetre = creer_fenetre_sorts_poisons(fenetre, liste, liste_impossibles, liste_valides)

                if fenetre[0]+fenetre[2] >= resolution.current_w:
                    fenetre[0] = resolution.current_w-fenetre[2]
                if fenetre[1]+fenetre[3] >= resolution.current_h:
                    fenetre[1] = resolution.current_h-fenetre[3]

                if fenetre[5] != -1 and fenetre[6] != -1:
                    liste_rafraichir.append([fenetre[4], (fenetre[0], fenetre[1], fenetre[2], fenetre[3]), 8])

                # GERER LES CHOIX

                if choix[1] == 1:
                    session.sorts = list()
                    for i in range(len(menu_onglets.options)):
                        session.sorts.append(liste[i])
                    session.points_de_sorts = points
                    choix[0] = 0
                    continuer = False
                if choix[1] == 2:
                    if len(session.sorts) > len(menu_onglets.options):
                        session.sorts = list(session.sorts[:len(menu_onglets.options)])
                    while len(session.sorts) < len(menu_onglets.options):
                        session.sorts.append(0)
                    choix[0] = 0
                    continuer = False
                if choix[1] == 3:
                    liste = list()
                    for i in range(len(menu_onglets.options)):
                        liste.append(0)
                    points = session.niveau

                if choix[2] != 0:
                    if not liste_impossibles[choix[2]-1] and not liste_valides[choix[2]-1] and points > 0:
                        liste[0] = choix[2]
                        points -= 1

                if choix[3] != 0:
                    if choix[3] == 1 and liste[0] == 1:
                        liste[0] = 0
                        points += 1
                    if (choix[3] == 2 and liste[0] == 2) or (choix[3] == 3 and liste[0] == 3):
                        liste[0] = 1
                        points += 1
                    if (choix[3] == 4 and liste[0] == 4) or (choix[3] == 5 and liste[0] == 5):
                        liste[0] = 2
                        points += 1
                    if (choix[3] == 6 and liste[0] == 6) or (choix[3] == 7 and liste[0] == 7):
                        liste[0] = 3
                        points += 1

        # ONGLET MAITRISE DU TEMPS

        if choix[0] == 2:

            liste_rafraichir = mettre_fond(ecran)
            # fenetre = [x, y, w, h, image, arbre y, arbre x, ancien arbre y, ancien arbre x]
            fenetre = [0, 0, 0, 0, 0, -1, -1, -1, -1]

            # AFFICHER L'ONGLET SELECTIONNE

            trait = pygame.Surface((resolution.current_w, 2))
            trait.fill((255, 255, 0))
            liste_rafraichir.append([trait, (0, menu_onglets.options[choix[0]-1].y+menu_onglets.options[choix[0]-1].h,
                                             resolution.current_w, 2), 1])
            liste_rafraichir.append([
                FOND.subsurface((menu_onglets.options[choix[0]-1].x, menu_onglets.options[choix[0]-1].y+menu_onglets.options[choix[0]-1].h,
                                 menu_onglets.options[choix[0]-1].w, 2)),
                (menu_onglets.options[choix[0]-1].x, menu_onglets.options[choix[0]-1].y+menu_onglets.options[choix[0]-1].h,
                 menu_onglets.options[choix[0]-1].w, 2), 2])

            for i in range(len(menu_onglets.options)):

                trait = pygame.Surface((2, menu_onglets.options[i].h))
                trait.fill((255, 255, 0))
                liste_rafraichir.append([trait, (menu_onglets.options[i].x-2, menu_onglets.options[i].y,
                                                 2, menu_onglets.options[i].h), 1])

                trait = pygame.Surface((menu_onglets.options[i].w, 2))
                trait.fill((255, 255, 0))
                liste_rafraichir.append([trait, (menu_onglets.options[i].x, menu_onglets.options[i].y-2,
                                                 menu_onglets.options[i].w, 2), 1])

                trait = pygame.Surface((2, menu_onglets.options[i].h))
                trait.fill((255, 255, 0))
                liste_rafraichir.append([trait, (menu_onglets.options[i].x+menu_onglets.options[i].w,
                                                 menu_onglets.options[i].y, 2, menu_onglets.options[i].h), 1])

            # CREER L'ARBRE DES SORTS DE MAITRISE DU TEMPS

            arbre_de_sorts = [Menu(), Menu(), Menu()]

            for i in range(len(arbre_de_sorts)):
                arbre_de_sorts[i].x = 0
                arbre_de_sorts[i].y = 224+(resolution.current_h-320)-((i+1)*((resolution.current_h-320)//len(arbre_de_sorts)))
                arbre_de_sorts[i].w = resolution.current_w
                arbre_de_sorts[i].h = (resolution.current_h-320)//len(arbre_de_sorts)
                arbre_de_sorts[i].type = 2

            # ETAGE 0

            arbre_de_sorts[0].options.append(Options_Menu())
            arbre_de_sorts[0].options[0].images = [pygame.Surface((64, 64)),
                                                   pygame.Surface((64, 64)),
                                                   ICONES_SORTS.subsurface((1088, 0, 64, 64))]
            arbre_de_sorts[0].options[0].images[1].fill((255, 0, 0))
            arbre_de_sorts[0].options[0].images[1].blit(ICONES_SORTS.subsurface((450, 2, 60, 60)), (2, 2))
            arbre_de_sorts[0].options[0].images[0].fill((0, 0, 255))
            arbre_de_sorts[0].options[0].images[0].blit(ICONES_SORTS.subsurface((450, 2, 60, 60)), (2, 2))

            # ETAGE 1

            for i in range(2):
                arbre_de_sorts[1].options.append(Options_Menu())
                arbre_de_sorts[1].options[i].images = [pygame.Surface((64, 64)),
                                                       pygame.Surface((64, 64)),
                                                       ICONES_SORTS.subsurface((1152+(64*i), 0, 64, 64))]
                arbre_de_sorts[1].options[i].images[1].fill((255, 0, 0))
                arbre_de_sorts[1].options[i].images[1].blit(ICONES_SORTS.subsurface((514+(64*i), 2, 60, 60)), (2, 2))
                arbre_de_sorts[1].options[i].images[0].fill((0, 0, 255))
                arbre_de_sorts[1].options[i].images[0].blit(ICONES_SORTS.subsurface((514+(64*i), 2, 60, 60)), (2, 2))

            # ETAGE 2

            for i in range(4):
                arbre_de_sorts[2].options.append(Options_Menu())
                arbre_de_sorts[2].options[i].images = [pygame.Surface((64, 64)),
                                                       pygame.Surface((64, 64)),
                                                       ICONES_SORTS.subsurface((640+(64*i), 64, 64, 64))]
                arbre_de_sorts[2].options[i].images[1].fill((255, 0, 0))
                arbre_de_sorts[2].options[i].images[1].blit(ICONES_SORTS.subsurface((2+(64*i), 66, 60, 60)), (2, 2))
                arbre_de_sorts[2].options[i].images[0].fill((0, 0, 255))
                arbre_de_sorts[2].options[i].images[0].blit(ICONES_SORTS.subsurface((2+(64*i), 66, 60, 60)), (2, 2))

            # CALCULER L'EMPLACEMENT DE CHAQUE OPTION

            for i in range(len(arbre_de_sorts)):
                for j in range(len(arbre_de_sorts[i].options)):
                    arbre_de_sorts[i].options[j].w = 64
                    arbre_de_sorts[i].options[j].h = 64
                    arbre_de_sorts[i].options[j].x = (((resolution.current_w-(len(arbre_de_sorts[i].options)*64))//(len(arbre_de_sorts[i].options)+1))*(j+1))+(j*64)
                    arbre_de_sorts[i].options[j].y = arbre_de_sorts[i].y+((arbre_de_sorts[i].h-64)//2)

            # BOUCLE DE L'ONGLET

            while choix[0] == 2:

                # RAFRAICHIR L'IMAGE

                liste_messages, liste_rafraichir = afficher_messages(liste_messages, liste_rafraichir, resolution)
                liste_rafraichir, temps_actuel, tempo = gerer_temps(ecran, tempo, liste_rafraichir, temps_actuel)

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

                # DEFINIR L'ETAT DE L'ARBRE

                liste_valides = [liste[1] != 0,
                                 (liste[1] == 9 or liste[1] == 11 or liste[1] == 12),
                                 (liste[1] == 10 or liste[1] == 13 or liste[1] == 14),
                                 liste[1] == 11,
                                 liste[1] == 12,
                                 liste[1] == 13,
                                 liste[1] == 14]

                liste_impossibles = [False,
                                     (not liste_valides[0] or liste_valides[2]),
                                     (not liste_valides[0] or liste_valides[1]),
                                     (not liste_valides[1] or liste_valides[4]),
                                     (not liste_valides[1] or liste_valides[3]),
                                     (not liste_valides[2] or liste_valides[6]),
                                     (not liste_valides[2] or liste_valides[5])]

                # RAFRAICHIR LES DONNEES DE LA FENETRE ET L'EFFACER

                fenetre_effaceur = [fenetre[0], fenetre[1], fenetre[2], fenetre[3]]
                fenetre[5], fenetre[6], fenetre[7], fenetre[8] = -1, -1, fenetre[5], fenetre[6]

                if (fenetre[7] != -1 and fenetre[8] != -1) or (fenetre[5] != -1 and fenetre[6] != -1):
                    liste_rafraichir.append([
                        FOND.subsurface((fenetre_effaceur[0], fenetre_effaceur[1], fenetre_effaceur[2], fenetre_effaceur[3])),
                        (fenetre_effaceur[0], fenetre_effaceur[1], fenetre_effaceur[2], fenetre_effaceur[3]), 0])

                if choix[2] != 0 or fenetre[3] != 0:
                    fenetre[7], fenetre[8] = -1, -1
                choix = [choix[0], 0, 0, 0]

                # GERER LES ENTREES UTILISATEUR

                for entree in pygame.event.get():
                    if entree.type == pygame.MOUSEBUTTONUP:
                        if entree.button == 1:
                            for i in range(len(menu.options)):
                                if menu.options[i].x+menu.options[i].w > entree.pos[0] > menu.options[i].x and \
                                   menu.options[i].y+menu.options[i].h > entree.pos[1] > menu.options[i].y:
                                    choix[1] = i+1
                            for i in range(len(menu_onglets.options)):
                                if menu_onglets.options[i].x+menu_onglets.options[i].w > entree.pos[0] > menu_onglets.options[i].x and \
                                   menu_onglets.options[i].y+menu_onglets.options[i].h > entree.pos[1] > menu_onglets.options[i].y:
                                    choix[0] = i+1
                            if arbre_de_sorts[0].options[0].x+arbre_de_sorts[0].options[0].w > entree.pos[0] > arbre_de_sorts[0].options[0].x and \
                               arbre_de_sorts[0].options[0].y+arbre_de_sorts[0].options[0].h > entree.pos[1] > arbre_de_sorts[0].options[0].y:
                                choix[2] = 8
                            for i in range(len(arbre_de_sorts[1].options)):
                                if arbre_de_sorts[1].options[i].x+arbre_de_sorts[1].options[i].w > entree.pos[0] > arbre_de_sorts[1].options[i].x and \
                                   arbre_de_sorts[1].options[i].y+arbre_de_sorts[1].options[i].h > entree.pos[1] > arbre_de_sorts[1].options[i].y:
                                    choix[2] = i+9
                            for i in range(len(arbre_de_sorts[2].options)):
                                if arbre_de_sorts[2].options[i].x+arbre_de_sorts[2].options[i].w > entree.pos[0] > arbre_de_sorts[2].options[i].x and \
                                   arbre_de_sorts[2].options[i].y+arbre_de_sorts[2].options[i].h > entree.pos[1] > arbre_de_sorts[2].options[i].y:
                                    choix[2] = i+11

                        if entree.button == 3:
                            if arbre_de_sorts[0].options[0].x+arbre_de_sorts[0].options[0].w > entree.pos[0] > arbre_de_sorts[0].options[0].x and \
                               arbre_de_sorts[0].options[0].y+arbre_de_sorts[0].options[0].h > entree.pos[1] > arbre_de_sorts[0].options[0].y:
                                choix[3] = 8
                            for i in range(len(arbre_de_sorts[1].options)):
                                if arbre_de_sorts[1].options[i].x+arbre_de_sorts[1].options[i].w > entree.pos[0] > arbre_de_sorts[1].options[i].x and \
                                   arbre_de_sorts[1].options[i].y+arbre_de_sorts[1].options[i].h > entree.pos[1] > arbre_de_sorts[1].options[i].y:
                                    choix[3] = i+9
                            for i in range(len(arbre_de_sorts[2].options)):
                                if arbre_de_sorts[2].options[i].x+arbre_de_sorts[2].options[i].w > entree.pos[0] > arbre_de_sorts[2].options[i].x and \
                                   arbre_de_sorts[2].options[i].y+arbre_de_sorts[2].options[i].h > entree.pos[1] > arbre_de_sorts[2].options[i].y:
                                    choix[3] = i+11

                    if entree.type == pygame.MOUSEMOTION:
                        position_souris = [entree.pos[0], entree.pos[1]]

                # AFFICHER LE MENU VALIDER/RETOUR/REINITIALISER

                for i in range(len(menu.options)):
                    if menu.options[i].x+menu.options[i].w > position_souris[0] > menu.options[i].x and \
                       menu.options[i].y+menu.options[i].h > position_souris[1] > menu.options[i].y:
                        liste_rafraichir.append([menu.options[i].images[1], (menu.options[i].x, menu.options[i].y,
                                                                             menu.options[i].w, menu.options[i].h), 7])
                    else:
                        liste_rafraichir.append([menu.options[i].images[0], (menu.options[i].x, menu.options[i].y,
                                                                             menu.options[i].w, menu.options[i].h), 7])

                # AFFICHER LE MENU DES ONGLETS

                for i in range(len(menu_onglets.options)):
                    if menu_onglets.options[i].x+menu_onglets.options[i].w > position_souris[0] > menu_onglets.options[i].x and \
                       menu_onglets.options[i].y+menu_onglets.options[i].h > position_souris[1] > menu_onglets.options[i].y:
                        liste_rafraichir.append([menu_onglets.options[i].images[1],
                                                 (menu_onglets.options[i].x, menu_onglets.options[i].y,
                                                  menu_onglets.options[i].w, menu_onglets.options[i].h), 7])
                    else:
                        liste_rafraichir.append([menu_onglets.options[i].images[0],
                                                 (menu_onglets.options[i].x, menu_onglets.options[i].y,
                                                  menu_onglets.options[i].w, menu_onglets.options[i].h), 7])

                # AFFICHER L'ARBRE DE SORTS

                i = 0
                for j in range(len(arbre_de_sorts)):
                    for k in range(len(arbre_de_sorts[j].options)):
                        if liste_valides[i]:
                            liste_rafraichir.append(
                                [arbre_de_sorts[j].options[k].images[1],
                                 (arbre_de_sorts[j].options[k].x, arbre_de_sorts[j].options[k].y,
                                  arbre_de_sorts[j].options[k].w, arbre_de_sorts[j].options[k].h,), 7])
                        if liste_impossibles[i]:
                            liste_rafraichir.append(
                                [arbre_de_sorts[j].options[k].images[2],
                                 (arbre_de_sorts[j].options[k].x, arbre_de_sorts[j].options[k].y,
                                  arbre_de_sorts[j].options[k].w, arbre_de_sorts[j].options[k].h,), 7])
                        if not liste_impossibles[i] and not liste_valides[i]:
                            liste_rafraichir.append(
                                [arbre_de_sorts[j].options[k].images[0],
                                 (arbre_de_sorts[j].options[k].x, arbre_de_sorts[j].options[k].y,
                                  arbre_de_sorts[j].options[k].w, arbre_de_sorts[j].options[k].h,), 7])
                        i += 1
                        if arbre_de_sorts[j].options[k].x+arbre_de_sorts[j].options[k].w > position_souris[0] > arbre_de_sorts[j].options[k].x and \
                           arbre_de_sorts[j].options[k].y+arbre_de_sorts[j].options[k].h > position_souris[1] > arbre_de_sorts[j].options[k].y:
                            fenetre[5] = j
                            fenetre[6] = k

                # AFFICHER LA FENETRE

                fenetre[0] = position_souris[0]
                fenetre[1] = position_souris[1]

                if fenetre[5] != -1 and fenetre[6] != -1:
                    fenetre = creer_fenetre_sorts_maitrise_du_temps(fenetre, liste, liste_impossibles, liste_valides)

                if fenetre[0]+fenetre[2] >= resolution.current_w:
                    fenetre[0] = resolution.current_w-fenetre[2]
                if fenetre[1]+fenetre[3] >= resolution.current_h:
                    fenetre[1] = resolution.current_h-fenetre[3]

                if fenetre[5] != -1 and fenetre[6] != -1:
                    liste_rafraichir.append([fenetre[4], (fenetre[0], fenetre[1], fenetre[2], fenetre[3]), 8])

                # GERER LES CHOIX

                if choix[1] == 1:
                    session.sorts = list()
                    for i in range(len(menu_onglets.options)):
                        session.sorts.append(liste[i])
                    session.points_de_sorts = points
                    choix[0] = 0
                    continuer = False
                if choix[1] == 2:
                    if len(session.sorts) > len(menu_onglets.options):
                        session.sorts = list(session.sorts[:len(menu_onglets.options)])
                    while len(session.sorts) < len(menu_onglets.options):
                        session.sorts.append(0)
                    choix[0] = 0
                    continuer = False
                if choix[1] == 3:
                    liste = list()
                    for i in range(len(menu_onglets.options)):
                        liste.append(0)
                    points = session.niveau

                if choix[2] != 0:
                    if not liste_impossibles[choix[2]-8] and not liste_valides[choix[2]-8] and points > 0:
                        liste[1] = choix[2]
                        points -= 1

                if choix[3] != 0:
                    if choix[3] == 8 and liste[1] == 8:
                        liste[1] = 0
                        points += 1
                    if (choix[3] == 9 and liste[1] == 9) or (choix[3] == 10 and liste[1] == 10):
                        liste[1] = 8
                        points += 1
                    if (choix[3] == 11 and liste[1] == 11) or (choix[3] == 12 and liste[1] == 12):
                        liste[1] = 9
                        points += 1
                    if (choix[3] == 13 and liste[1] == 13) or (choix[3] == 14 and liste[1] == 14):
                        liste[1] = 10
                        points += 1

    return session, liste_rafraichir, liste_messages


def creer_fenetre_sorts_poisons(fenetre, liste, liste_impossibles, liste_valides):

    if fenetre[5] == 0 and fenetre[6] == 0:
        if not (fenetre[7] == 0 and fenetre[8] == 0):

            chaine = "Poison paralysant\n" \
                     "\n" \
                     "Vous lancez une attaques empoisonnee,\n" \
                     "si elle touche un ennemi, celui ci est\n" \
                     "paralyse pendant 3 secondes"
            chaine += "\n\nCout: 25 points de mana"
            if liste_valides[0]:
                chaine += "\n\nCe sort a ete debloquee"
            else:
                chaine += "\n\nCliquez sur l'icone pour debloquer ce sort"

            fenetre[4], fenetre[2], fenetre[3] = creer_fenetre_souris(chaine)
    if fenetre[5] == 1 and fenetre[6] == 0:
        if not (fenetre[7] == 1 and fenetre[8] == 0):

            chaine = "Nuage paralysant\n" \
                     "\n" \
                     "Votre attaque se disperse instantanement en\n" \
                     "un nuage empoisonnes autour de vous. Si un\n" \
                     "ennemi se trouve dans ce nuage, il\n" \
                     "est paralyse pendant 2.5 secondes"
            chaine += "\n\nCout: 30 points de mana"
            if liste[0] == 0:
                chaine += "\n\nVous ne pouvez pas debloquer ce sort"
            elif liste_valides[1]:
                chaine += "\n\nCe sort a ete debloquee"
            elif liste[0] == 1:
                chaine += "\n\nCliquez sur l'icone pour debloquer ce sort"
            else:
                chaine += "\n\nVous avez choisi une autre branche"

            fenetre[4], fenetre[2], fenetre[3] = creer_fenetre_souris(chaine)
    if fenetre[5] == 1 and fenetre[6] == 1:
        if not (fenetre[7] == 1 and fenetre[8] == 1):

            chaine = "Maladie\n" \
                     "\n" \
                     "En plus de la paralysie de 3 secondes,\n" \
                     "votre attaque provoque une perte reguliere de\n" \
                     "points de vies pendant 5 secondes, infligeant\n" \
                     "un total de 125% des degats d'une attaque de base"
            chaine += "\n\nCout: 40 points de mana"
            if liste[0] == 0:
                chaine += "\n\nVous ne pouvez pas debloquer ce sort"
            elif liste_valides[2]:
                chaine += "\n\nCe sort a ete debloquee"
            elif liste[0] == 1:
                chaine += "\n\nCliquez sur l'icone pour debloquer ce sort"
            else:
                chaine += "\n\nVous avez choisi une autre branche"

            fenetre[4], fenetre[2], fenetre[3] = creer_fenetre_souris(chaine)
    if fenetre[5] == 2 and fenetre[6] == 0:
        if not (fenetre[7] == 2 and fenetre[8] == 0):

            chaine = "Gros nuage paralysant\n" \
                     "\n" \
                     "Ce sort paralyse desormais\n" \
                     "tous les ennemis presents dans la salle\n" \
                     "pendant 2.5 secondes"
            chaine += "\n\nCout: 50 points de mana"
            if liste[0] == 0 or liste[0] == 1:
                chaine += "\n\nVous ne pouvez pas debloquer ce sort"
            elif liste_valides[3]:
                chaine += "\n\nCe sort a ete debloquee"
            elif liste[0] == 2:
                chaine += "\n\nCliquez sur l'icone pour debloquer ce sort"
            else:
                chaine += "\n\nVous avez choisi une autre branche"

            fenetre[4], fenetre[2], fenetre[3] = creer_fenetre_souris(chaine)
    if fenetre[5] == 2 and fenetre[6] == 1:
        if not (fenetre[7] == 2 and fenetre[8] == 1):

            chaine = "Poison affaiblissant\n" \
                     "\n" \
                     "Les ennemis paralyses par ce sort\n" \
                     "subissent 400% de degats supplementaires\n" \
                     "par vos attaques de base durant la paralysie"
            chaine += "\n\nCout: 45 points de mana"
            if liste[0] == 0 or liste[0] == 1:
                chaine += "\n\nVous ne pouvez pas debloquer ce sort"
            elif liste_valides[4]:
                chaine += "\n\nCe sort a ete debloquee"
            elif liste[0] == 2:
                chaine += "\n\nCliquez sur l'icone pour debloquer ce sort"
            else:
                chaine += "\n\nVous avez choisi une autre branche"

            fenetre[4], fenetre[2], fenetre[3] = creer_fenetre_souris(chaine)
    if fenetre[5] == 2 and fenetre[6] == 2:
        if not (fenetre[7] == 2 and fenetre[8] == 2):

            chaine = "Pandemie\n" \
                     "\n" \
                     "Le sort traverse maintenant les ennemis"
            chaine += "\n\nCout: 60 points de mana"
            if liste[0] == 0 or liste[0] == 1:
                chaine += "\n\nVous ne pouvez pas debloquer ce sort"
            elif liste_valides[5]:
                chaine += "\n\nCe sort a ete debloquee"
            elif liste[0] == 3:
                chaine += "\n\nCliquez sur l'icone pour debloquer ce sort"
            else:
                chaine += "\n\nVous avez choisi une autre branche"

            fenetre[4], fenetre[2], fenetre[3] = creer_fenetre_souris(chaine)
    if fenetre[5] == 2 and fenetre[6] == 3:
        if not (fenetre[7] == 2 and fenetre[8] == 3):

            chaine = "Peste\n" \
                     "\n" \
                     "La perte reguliere de points de vie est remplacee\n" \
                     "par une perte permanente de 5% des points de vie\n" \
                     "restant de l'ennemi par seconde,\n" \
                     "les degats minimum sont de 1"
            chaine += "\n\nCout: 45 points de mana"
            if liste[0] == 0 or liste[0] == 1:
                chaine += "\n\nVous ne pouvez pas debloquer ce sort"
            elif liste_valides[6]:
                chaine += "\n\nCe sort a ete debloquee"
            elif liste[0] == 3:
                chaine += "\n\nCliquez sur l'icone pour debloquer ce sort"
            else:
                chaine += "\n\nVous avez choisi une autre branche"

            fenetre[4], fenetre[2], fenetre[3] = creer_fenetre_souris(chaine)

    return fenetre


def creer_fenetre_sorts_maitrise_du_temps(fenetre, liste, liste_impossibles, liste_valides):

    if fenetre[5] == 0 and fenetre[6] == 0:
        if not (fenetre[7] == 0 and fenetre[8] == 0):

            chaine = "Distorsion\n" \
                     "\n" \
                     "Vous ralentissez le temps autour\n" \
                     "de vous afin de vous deplacer\n" \
                     "50% plus vite pendant 10 secondes"
            chaine += "\n\nCout: 15 points de mana"
            if liste_valides[0]:
                chaine += "\n\nCe sort a ete debloque"
            else:
                chaine += "\n\nCliquez sur l'icone pour debloquer ce sort"

            fenetre[4], fenetre[2], fenetre[3] = creer_fenetre_souris(chaine)
    if fenetre[5] == 1 and fenetre[6] == 0:
        if not (fenetre[7] == 1 and fenetre[8] == 0):

            chaine = "Effondrement\n" \
                     "\n" \
                     "Le temps s'effondre sur lui meme\n" \
                     "provoquant une explosion autour\n" \
                     "de vous, infligeant 200% des degats\n" \
                     "d'une attaque de base aux ennemis\n" \
                     "proches"
            chaine += "\n\nCout: 35 points de mana"
            if liste_valides[1]:
                chaine += "\n\nCe sort a ete debloque"
            elif liste[1] == 8:
                chaine += "\n\nCliquez sur l'icone pour debloquer ce sort"
            elif liste[1] == 0:
                chaine += "\n\nVous ne pouvez pas debloquer ce sort"
            else:
                chaine += "\n\nVous avez choisi une autre branche"

            fenetre[4], fenetre[2], fenetre[3] = creer_fenetre_souris(chaine)
    if fenetre[5] == 1 and fenetre[6] == 1:
        if not (fenetre[7] == 1 and fenetre[8] == 1):

            chaine = "Acceleration\n" \
                     "\n" \
                     "Vous arrivez mieu a vous controler\n" \
                     "pendant le ralentissement du temps,\n" \
                     "ce qui vous permet d'augmenter votre\n" \
                     "vitesse d'attaque de 50% pendant 10 secondes"
            chaine += "\n\nCout: 40 points de mana"
            if liste_valides[2]:
                chaine += "\n\nCe sort a ete debloque"
            elif liste[1] == 8:
                chaine += "\n\nCliquez sur l'icone pour debloquer ce sort"
            elif liste[1] == 0:
                chaine += "\n\nVous ne pouvez pas debloquer ce sort"
            else:
                chaine += "\n\nVous avez choisi une autre branche"

            fenetre[4], fenetre[2], fenetre[3] = creer_fenetre_souris(chaine)
    if fenetre[5] == 2 and fenetre[6] == 0:
        if not (fenetre[7] == 2 and fenetre[8] == 0):

            chaine = "Effondrement distant\n" \
                     "\n" \
                     "L'explosion peut maintenant\n" \
                     "etre provoquee n'importe ou\n" \
                     "dans la salle"
            chaine += "\n\nCout: 60 points de mana"
            if liste_valides[3]:
                chaine += "\n\nCe sort a ete debloque"
            elif liste[1] == 9:
                chaine += "\n\nCliquez sur l'icone pour debloquer ce sort"
            elif liste[1] == 0 or liste[1] == 8:
                chaine += "\n\nVous ne pouvez pas debloquer ce sort"
            else:
                chaine += "\n\nVous avez choisi une autre branche"

            fenetre[4], fenetre[2], fenetre[3] = creer_fenetre_souris(chaine)
    if fenetre[5] == 2 and fenetre[6] == 1:
        if not (fenetre[7] == 2 and fenetre[8] == 1):

            chaine = "Implosion\n" \
                     "\n" \
                     "Le temps implose autour de vous\n" \
                     "doublant la portee de l'explosion"
            chaine += "\n\nCout: 55 points de mana"
            if liste_valides[4]:
                chaine += "\n\nCe sort a ete debloque"
            elif liste[1] == 9:
                chaine += "\n\nCliquez sur l'icone pour debloquer ce sort"
            elif liste[1] == 0 or liste[1] == 8:
                chaine += "\n\nVous ne pouvez pas debloquer ce sort"
            else:
                chaine += "\n\nVous avez choisi une autre branche"

            fenetre[4], fenetre[2], fenetre[3] = creer_fenetre_souris(chaine)
    if fenetre[5] == 2 and fenetre[6] == 2:
        if not (fenetre[7] == 2 and fenetre[8] == 2):

            chaine = "Irrealite\n" \
                     "\n" \
                     "En plus des effets precedants, les\n" \
                     "attaques de bases traversent les rochers\n" \
                     "pendant 10 secondes"
            chaine += "\n\nCout: 75 points de mana"
            if liste_valides[5]:
                chaine += "\n\nCe sort a ete debloque"
            elif liste[1] == 10:
                chaine += "\n\nCliquez sur l'icone pour debloquer ce sort"
            elif liste[1] == 0 or liste[1] == 8:
                chaine += "\n\nVous ne pouvez pas debloquer ce sort"
            else:
                chaine += "\n\nVous avez choisi une autre branche"

            fenetre[4], fenetre[2], fenetre[3] = creer_fenetre_souris(chaine)
    if fenetre[5] == 2 and fenetre[6] == 3:
        if not (fenetre[7] == 2 and fenetre[8] == 3):

            chaine = "Equilibre\n" \
                     "\n" \
                     "En plus des effets precedants, pendant\n" \
                     "10 secondes, lorsque votre attaque touche\n" \
                     "un ennemi, les degats sont equitablement repartis\n" \
                     "entre tout les ennemis present dans la salle"
            chaine += "\n\nCout: 40 points de mana"
            if liste_valides[6]:
                chaine += "\n\nCe sort a ete debloque"
            elif liste[1] == 10:
                chaine += "\n\nCliquez sur l'icone pour debloquer ce sort"
            elif liste[1] == 0 or liste[1] == 8:
                chaine += "\n\nVous ne pouvez pas debloquer ce sort"
            else:
                chaine += "\n\nVous avez choisi une autre branche"

            fenetre[4], fenetre[2], fenetre[3] = creer_fenetre_souris(chaine)

    return fenetre


def changer_selection_sort(liste_rafraichir, position_ecran_x, position_ecran_y, joueur, sort_selectionne, nouveau_sort_selectionne):

    global ICONES_SORTS

    nouveau_sort_selectionne %= len(joueur.sorts) # OBTENIR LE VRAI SORT SELECTIONNE

    if joueur.sorts[sort_selectionne] != 0:  # AFFICHER L'ICONE NORMALE DE SORT S'IL Y EN A UNE
        liste_rafraichir.append([ICONES_SORTS.subsurface((((joueur.sorts[sort_selectionne]-1) % 10)*64,
                                                          ((joueur.sorts[sort_selectionne]-1)//10)*64, 64, 64)),
                                 (position_ecran_x+960, position_ecran_y+(64*sort_selectionne), 64, 64), 6])
    else:  # SINON AFFICHER UN CARRE GRIS
        icone = pygame.Surface((64, 64))
        icone.fill((150, 150, 150))
        liste_rafraichir.append([icone, (position_ecran_x+960, position_ecran_y+(64*sort_selectionne), 64, 64), 6])

    icone_selectionnee = pygame.Surface((64, 64))  # CREER UNE ICONE SELECTIONNEE
    icone_selectionnee.fill((254, 254, 254))
    if joueur.sorts[nouveau_sort_selectionne] != 0:  # S'IL Y A UN SORT
        icone_selectionnee.blit(ICONES_SORTS.subsurface((((joueur.sorts[nouveau_sort_selectionne]-1) % 10)*64+2,
                                                         ((joueur.sorts[nouveau_sort_selectionne]-1)//10)*64+2, 60, 60)), (2, 2))
    else:  # SINON ON CREER UN CARRE GRIS SELECTIONNE
        icone_selectionnee.fill((150, 150, 150), (2, 2, 60, 60))

    liste_rafraichir.append([icone_selectionnee,
                             (position_ecran_x+960, position_ecran_y+(64*nouveau_sort_selectionne), 64, 64), 6])

    sort_selectionne = nouveau_sort_selectionne

    return liste_rafraichir, sort_selectionne


def gerer_poison(joueur, etage):

    if joueur.sorts[0] == 3 or joueur.sorts[0] == 6:  # LES EMPOISONNEMENTS NORMAUX, A DUREE LIMITEE
        for ennemi in etage.salles[joueur.salle].ennemis:
            if ennemi.empoisonne and \
               pygame.time.get_ticks() >= ennemi.fin_empoisonne-4500 and \
               pygame.time.get_ticks()//500 >= (ennemi.temps_dernier_poison//500)+2:
                ennemi.temps_dernier_poison = pygame.time.get_ticks()
                ennemi.points_de_vies -= int(0.25*joueur.attaque)
                if ennemi.points_de_vies <= 0:
                    ennemi.mort = True
            if ennemi.empoisonne and pygame.time.get_ticks() > ennemi.fin_empoisonne:
                ennemi.empoisonne = False

    if joueur.sorts[0] == 7:  # L'EMPOISONNEMENT DEFINITIF
        for ennemi in etage.salles[joueur.salle].ennemis:
            if ennemi.empoisonne and \
               pygame.time.get_ticks() >= ennemi.fin_empoisonne-4500 and \
               pygame.time.get_ticks()//500 >= (ennemi.temps_dernier_poison//500)+2:
                ennemi.temps_dernier_poison = pygame.time.get_ticks()
                ennemi.points_de_vies = int(0.95*ennemi.points_de_vies)
                if ennemi.points_de_vies <= 0:
                    ennemi.mort = True

    return etage


def enlever_mana_sorts(position_ecran_x, position_ecran_y, joueur, liste_rafraichir, session, sort_selectionne):

    sort_valide = False
    mana_a_enlever = 0

    if joueur.sorts[sort_selectionne] == 8:
        mana_a_enlever = 15
    if joueur.sorts[sort_selectionne] == 1:
        mana_a_enlever = 25
    if joueur.sorts[sort_selectionne] == 2:
        mana_a_enlever = 30
    if joueur.sorts[sort_selectionne] == 9:
        mana_a_enlever = 35
    if joueur.sorts[sort_selectionne] == 3 or \
       joueur.sorts[sort_selectionne] == 10 or \
       joueur.sorts[sort_selectionne] == 14:
        mana_a_enlever = 40
    if joueur.sorts[sort_selectionne] == 5 or \
       joueur.sorts[sort_selectionne] == 7:
        mana_a_enlever = 45
    if joueur.sorts[sort_selectionne] == 4:
        mana_a_enlever = 50
    if joueur.sorts[sort_selectionne] == 12:
        mana_a_enlever = 55
    if joueur.sorts[sort_selectionne] == 6 or \
       joueur.sorts[sort_selectionne] == 11:
        mana_a_enlever = 60
    if joueur.sorts[sort_selectionne] == 13:
        mana_a_enlever = 75

    if joueur.mana-mana_a_enlever >= 0:
        liste_rafraichir, joueur = rafraichir_mana(position_ecran_x, position_ecran_y, joueur, liste_rafraichir,
                                                   session, joueur.mana-mana_a_enlever)
        sort_valide = True

    return joueur, liste_rafraichir, sort_valide


def regarder_la_map(etage, ecran, joueur, position_ecran_x, position_ecran_y, session, sort_selectionne, minimap, resolution, raccourcis):

    global MINIMAP
    global INTERFACE

    # CREER L'IMAGE DE LA CARTE

    carte = pygame.Surface((len(etage.carte_map[0])*50, len(etage.carte_map)*34))
    carte.fill((255, 255, 255))
    carte.set_colorkey((255, 255, 255))
    for y in range(len(etage.carte_map)):
        for x in range(len(etage.carte_map[y])):
            for salle in etage.salles:
                if salle.x == x and salle.y == y:
                    if salle.visited:
                        if salle.type_salle == 1 or \
                           salle.type_salle == 2:
                            if salle.objets == list():
                                carte.blit(pygame.transform.scale2x(MINIMAP.subsurface((0, 88, 24, 16))), (x*50, y*34))
                            else:
                                carte.blit(pygame.transform.scale2x(MINIMAP.subsurface((96, 88, 24, 16))), (x*50, y*34))
                        if salle.type_salle == 3:
                            carte.blit(pygame.transform.scale2x(MINIMAP.subsurface((24, 88, 24, 16))), (x*50, y*34))
                        if salle.type_salle == 4:
                            carte.blit(pygame.transform.scale2x(MINIMAP.subsurface((48, 88, 24, 16))), (x*50, y*34))
                        if salle.type_salle == 5:
                            carte.blit(pygame.transform.scale2x(MINIMAP.subsurface((72, 88, 24, 16))), (x*50, y*34))
                    if not salle.visited:
                        if salle.type_salle != 5:
                            carte.blit(pygame.transform.scale2x(MINIMAP.subsurface((0, 104, 24, 16))), (x*50, y*34))
                        if salle.type_salle == 5:
                            carte.blit(pygame.transform.scale2x(MINIMAP.subsurface((24, 104, 24, 16))), (x*50, y*34))

    # CREER L'EFFACEUR DE LA CARTE

    carte_effaceur = pygame.Surface((len(etage.carte_map[0])*50, len(etage.carte_map)*34))
    carte_effaceur.fill((255, 255, 255))

    # METTRE L'ECRAN EN BLANC ET AFFICHER LE BOUTON POUR RETOURNER AU JEU

    ecran.fill((255, 255, 255))
    ecran.blit(INTERFACE.subsurface((0, 225, 64, 64)), (resolution.current_w-64, 0))
    pygame.display.flip()

    # INITIALISATION DE VARIABLES

    position_carte = [(resolution.current_w-carte.get_size()[0])//2, (resolution.current_h-carte.get_size()[1])//2]
    position_souris = [0, 0]
    push = False
    push_positions = [0, 0, position_carte[0], position_carte[1]]
    liste_rafraichir = []
    tempo = 0
    temps_actuel = pygame.time.get_ticks()
    continuer = True

    # BOUCLE

    while continuer:

        # RAFRAICHIR L'IMAGE

        liste_rafraichir, temps_actuel, tempo = gerer_temps(ecran, tempo, liste_rafraichir, temps_actuel)

        # GERER LES ENTREES UTILISATEUR

        for entree in pygame.event.get():
            if entree.type == pygame.KEYUP:
                if entree.key == raccourcis[7][0]:
                    continuer = False
            if entree.type == pygame.MOUSEBUTTONDOWN:
                if entree.button == 1:
                    push = True
                    push_positions = [entree.pos[0], entree.pos[1], position_carte[0], position_carte[1]]
            if entree.type == pygame.MOUSEBUTTONUP:
                if entree.button == 1:
                    push = False
                    if resolution.current_w-64 < entree.pos[0] < resolution.current_w and \
                       0 < entree.pos[1] < 64:
                        continuer = False
            if entree.type == pygame.MOUSEMOTION:
                if push:
                    liste_rafraichir.append([carte_effaceur, (position_carte[0], position_carte[1],
                                                              carte.get_size()[0], carte.get_size()[1]), 0])
                    position_carte = [push_positions[2]+(entree.pos[0]-push_positions[0]),push_positions[3]+(entree.pos[1]-push_positions[1])]
                position_souris = [entree.pos[0], entree.pos[1]]

        # EMPECHER LA CARTE DE PARTIR TROP LOIN

        if position_carte[0]+carte.get_size()[0] < 0:
            position_carte[0] = -carte.get_size()[0]
        if position_carte[0] > resolution.current_w:
            position_carte[0] = resolution.current_w
        if position_carte[1]+carte.get_size()[1] < 0:
            position_carte[1] = -carte.get_size()[1]
        if position_carte[1] > resolution.current_h:
            position_carte[1] = resolution.current_h

        # AFFICHER LA CARTE

        liste_rafraichir.append([carte, (position_carte[0], position_carte[1],
                                         carte.get_size()[0], carte.get_size()[1]), 1])

        # AFFICHER LE BOUTON

        if resolution.current_w-64 < position_souris[0] < resolution.current_w and \
           0 < position_souris[1] < 64:
            liste_rafraichir.append([INTERFACE.subsurface((64, 225, 64, 64)),
                                     (resolution.current_w-64, 0, 64, 64), 6])
        else:
            liste_rafraichir.append([INTERFACE.subsurface((0, 225, 64, 64)),
                                     (resolution.current_w-64, 0, 64, 64), 6])

    # AFFICHER LE JEU

    liste_rafraichir = mettre_fond(ecran)
    afficher_interface(position_ecran_x, position_ecran_y, ecran, joueur, session)
    liste_rafraichir, sort_selectionne = changer_selection_sort(liste_rafraichir, position_ecran_x, position_ecran_y, joueur, sort_selectionne, sort_selectionne)
    ecran.blit(etage.salles[joueur.salle].image, (position_ecran_x, position_ecran_y))
    ecran.blit(joueur.images.bas[0], (position_ecran_x+joueur.x, position_ecran_y+joueur.y))
    ecran.blit(minimap, (position_ecran_x+824, position_ecran_y+10))
    pygame.display.flip()

    return liste_rafraichir, joueur


def afficher_bouton_map(position_ecran_x, position_ecran_y, entree, liste_rafraichir):

    global INTERFACE

    if position_ecran_x+960 < entree.pos[0] < position_ecran_x+1024 and \
       position_ecran_y+576 < entree.pos[1] < position_ecran_y+640:
        liste_rafraichir.append([INTERFACE.subsurface((64, 225, 64, 64)),
                                 (position_ecran_x+960, position_ecran_y+576, 64, 64), 6])
    else:
        liste_rafraichir.append([INTERFACE.subsurface((0, 225, 64, 64)),
                                 (position_ecran_x+960, position_ecran_y+576, 64, 64), 6])

    return liste_rafraichir


def fin_de_partie(ecran, resolution, liste_rafraichir, liste_messages, session, etage):

    global CARACTERES

    texte = ["Etage(s) parcouru(s):"+str(etage.niveau-1),
             "Argent gagné: "+str(((etage.niveau-1)*5)**2)+"$",
             "Argent actuel: "+str(session.argent+((etage.niveau-1)*5)**2)+"$"]
    session.argent += ((etage.niveau-1)*5)**2
    for y in range(len(texte)):
        for x in range(len(texte[y])):
            ecran.blit(CARACTERES.subsurface(((ord(texte[y][x]) % 10)*32, (ord(texte[y][x])//10)*64, 32, 64)),
                       ((resolution.current_w-(32*len(texte[y])))//2+32*x,
                        ((resolution.current_h-64*len(texte)-128)//len(texte))*(y+1)))
    pygame.display.flip()

    menu = Menu()
    menu.x = 0
    menu.y = resolution.current_h-128
    menu.w = resolution.current_w
    menu.h = 128
    for i in range(1):
        menu.options.append(Options_Menu())
    menu.options[0].message = "Menu"
    menu.type = 2
    menu = creer_images_et_positions_menu(menu)

    choix = 0
    tempo = 0
    position_souris = [0, 0]
    continuer = True
    temps_actuel = pygame.time.get_ticks()

    while continuer:

        # RAFRAICHIR L'IMAGE

        liste_messages, liste_rafraichir = afficher_messages(liste_messages, liste_rafraichir, resolution)
        liste_rafraichir, temps_actuel, tempo = gerer_temps(ecran, tempo, liste_rafraichir, temps_actuel)

        # AFFICHER LE MENU ET OBTENIR LE CHOIX DE L'UTILISATEUR

        liste_rafraichir, choix, position_souris = \
            obtenir_choix_menu_et_afficher_selection(menu, position_souris, liste_rafraichir)

        # GERER LES CHOIX

        if choix == 1:
            continuer = False

    return liste_rafraichir, liste_messages, session


def achat_equipement(ecran, resolution, liste_rafraichir, liste_messages, session):

    global CARACTERES
    global FOND

    # METTRE A JOUR L'INVENTAIRE SI CE N'EST PAS DEJA LE CAS

    for i in range(96-len(session.inventaire)):
        session.inventaire.append(0)

    # CREER ET AFFICHER L'INTERFACE

    cadre_noir = pygame.Surface((resolution.current_w, resolution.current_h))
    cadre_noir.fill((255, 255, 255))
    cadre_noir.fill((150, 150, 150), (98, 98, resolution.current_w-196, resolution.current_h-266))
    cadre_noir.fill((0, 0, 0), (100, 100, resolution.current_w-200, resolution.current_h-270))
    cadre_noir.set_colorkey((255, 255, 255))
    liste_rafraichir.append([cadre_noir, (0, 0, resolution.current_w, resolution.current_h), 0])

    # CREER LE MENU "MENU/ACHETER"

    menu = Menu()
    menu.x = 0
    menu.y = resolution.current_h-170
    menu.w = resolution.current_w
    menu.h = 170
    for i in range(2):
        menu.options.append(Options_Menu())
    menu.options[0].message = "Menu"
    menu.options[1].message = "Acheter"
    menu.type = 2
    menu = creer_images_et_positions_menu(menu)

    # CREER LE MENU DES ACHETABLES

    achetables = Menu()
    for i in range(4):
        achetables.options.append(Options_Menu())
    achetables.options[0].message = "300$ - Casque en cuir"
    achetables.options[1].message = "500$ - Plastron en cuir"
    achetables.options[2].message = "450$ - Jambieres en cuir"
    achetables.options[3].message = "250$ - Bottes en cuir"
    achetables.x = 100
    achetables.y = 100
    achetables.w = resolution.current_w-200
    achetables.h = len(achetables.options)*64
    achetables.type = 3
    achetables = creer_images_et_positions_menu(achetables)

    # CREER LE TEXTE QUI INDIQUE L'ARGENT RESTANT

    texte = [0, 0, 0, 0, "Argent: "+str(session.argent)+"$", pygame.Surface((1,64))]
    texte[2] = len(texte[4])*32
    texte[3] = 64
    texte[0] = (resolution.current_w-texte[2])//2
    texte[1] = 18
    texte[5] = pygame.Surface((texte[2], texte[3]))
    texte[5].fill((255, 255, 255))
    texte[5].set_colorkey((255, 255, 255))
    for i in range(len(texte[4])):
        texte[5].blit(CARACTERES.subsurface(((ord(texte[4][i]) % 10)*32, (ord(texte[4][i])//10)*64, 32, 64)), (i*32, 0))
    liste_rafraichir.append([texte[5],(texte[0], texte[1], texte[2], texte[3]), 7])

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

        liste_messages, liste_rafraichir = afficher_messages(liste_messages, liste_rafraichir, resolution)
        liste_rafraichir, temps_actuel, tempo = gerer_temps(ecran, tempo, liste_rafraichir, temps_actuel)
        choix[0] = 0

        # GERER LES ENTREES UTILISATEURS

        for entree in pygame.event.get():

            if entree.type == pygame.MOUSEMOTION:  # LES MOUVEMENTS DE SOURIS
                position_souris = [entree.pos[0], entree.pos[1]]

            if entree.type == pygame.MOUSEBUTTONUP:

                if entree.button == 1:  # LES CLIQUES

                    for i in range(len(menu.options)):  # LE MENU "MENU/ACHETER"
                        if menu.options[i].x+menu.options[i].w > entree.pos[0] > menu.options[i].x and \
                           menu.options[i].y+menu.options[i].h > entree.pos[1] > menu.options[i].y:
                            choix[0] = i+1

                    for i in range(len(achetables.options)):  # LE MENU DES ACHETABLES
                        if achetables.options[i].x+achetables.options[i].w > entree.pos[0] > achetables.options[i].x and \
                           achetables.options[i].y+achetables.options[i].h > entree.pos[1] > achetables.options[i].y and \
                           100 < entree.pos[0] < resolution.current_w-100 and 100 < entree.pos[1] < resolution.current_h-170:
                            choix[1] = i+1

                            # EFFACER LE CADRE S'IL Y EN A UN

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
                                            pygame.Surface((liste_cadre[2], liste_cadre[3]-100+liste_cadre[1])),
                                            (liste_cadre[0], 100, liste_cadre[2], liste_cadre[3]-100+liste_cadre[1]), 0])

                            # CREER LES NOUVELLES COORDONNEES DU CADRE

                            liste_cadre[0] = achetables.options[i].x-2
                            liste_cadre[1] = achetables.options[i].y-2
                            liste_cadre[2] = achetables.options[i].w+4
                            liste_cadre[3] = achetables.options[i].h+4
                            liste_cadre[4] = pygame.Surface((liste_cadre[2], liste_cadre[3]))
                            liste_cadre[4].fill((255, 255, 0))
                            liste_cadre[4].fill((255, 255, 255), (1, 1, achetables.options[i].w+2, achetables.options[i].h+2))
                            liste_cadre[4].set_colorkey((255, 255, 255))

                            # AFFICHER LE CADRE

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
                                        (liste_cadre[0], 100, liste_cadre[2], liste_cadre[3]-(100-liste_cadre[1])), 7])

                if 4 <= entree.button <= 5:  # FAIRE DEFILER LE MENU
                    if (achetables.options[len(achetables.options)-1].y >= resolution.current_h-298 and
                       entree.button == 5) or (achetables.options[0].y <= 164 and entree.button == 4):

                        # EFFACER LE MENU DES ACHETABLES PUIS LE DEPLACER

                        for i in range(len(achetables.options)):

                            if achetables.options[i].y < resolution.current_h-170 and \
                               achetables.options[i].y+achetables.options[i].h > 100:

                                if achetables.options[i].y+achetables.options[i].h <= resolution.current_h-170 and \
                                   achetables.options[i].y >= 100:
                                    liste_rafraichir.append(
                                        [pygame.Surface((achetables.options[i].w, achetables.options[i].h)),
                                         (achetables.options[i].x, achetables.options[i].y,
                                          achetables.options[i].w, achetables.options[i].h), 7])

                                if achetables.options[i].y+achetables.options[i].h > resolution.current_h-170:
                                    liste_rafraichir.append([pygame.Surface(
                                        (achetables.options[i].w, resolution.current_h-170-achetables.options[i].y)),
                                        (achetables.options[i].x, achetables.options[i].y,
                                         achetables.options[i].w, resolution.current_h-170-achetables.options[i].y), 7])

                                if achetables.options[i].y < 100:
                                    liste_rafraichir.append([pygame.Surface(
                                        (achetables.options[i].w, achetables.options[i].h-(100-achetables.options[i].y))),
                                        (achetables.options[i].x, 100, achetables.options[i].w,
                                         achetables.options[i].h-(100-achetables.options[i].y)), 7])
                            if entree.button == 5:
                                achetables.options[i].y -= 30
                            if entree.button == 4:
                                achetables.options[i].y += 30

                        # EFFACER LE CADRE, LE DEPLACER et le REAFFICHER

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
                                        (liste_cadre[0], 100, liste_cadre[2], liste_cadre[3]-(100-liste_cadre[1])), 0])

                            if entree.button == 5:
                                liste_cadre[1] -= 30
                            if entree.button == 4:
                                liste_cadre[1] += 30

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
                                        (liste_cadre[0], 100, liste_cadre[2], liste_cadre[3]-(100-liste_cadre[1])), 7])

        # AFFICHER LE MENU "MENU/ACHETER"

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

        # AFFICHER LE MENU DES ACHETABLES

        for i in range(len(achetables.options)):
            if achetables.options[i].y < resolution.current_h-170 and \
               achetables.options[i].y+achetables.options[i].h > 100:

                # SI L'ACHETABLE EST ENTIER

                if achetables.options[i].y+achetables.options[i].h <= resolution.current_h-170 and \
                   achetables.options[i].y >= 100:

                    if achetables.options[i].x+achetables.options[i].w > position_souris[0] > achetables.options[i].x and \
                       achetables.options[i].y+achetables.options[i].h > position_souris[1] > achetables.options[i].y and \
                       100 < position_souris[0] < resolution.current_w-100 and 100 < position_souris[1] < resolution.current_h-170:
                        liste_rafraichir.append([achetables.options[i].images[1],
                                                 (achetables.options[i].x, achetables.options[i].y,
                                                  achetables.options[i].w, achetables.options[i].h), 7])
                    else:
                        liste_rafraichir.append([achetables.options[i].images[0],
                                                 (achetables.options[i].x, achetables.options[i].y,
                                                  achetables.options[i].w, achetables.options[i].h), 7])

                # SI L'ACHETABLE EST TROP BAS

                if achetables.options[i].y+achetables.options[i].h > resolution.current_h-170:

                    if achetables.options[i].x+achetables.options[i].w > position_souris[0] > achetables.options[i].x and \
                       achetables.options[i].y+achetables.options[i].h > position_souris[1] > achetables.options[i].y and \
                       100 < position_souris[0] < resolution.current_w-100 and 100 < position_souris[1] < resolution.current_h-170:
                        liste_rafraichir.append([achetables.options[i].images[1].subsurface(
                            (0, 0, achetables.options[i].w, resolution.current_h-170-achetables.options[i].y)),
                            (achetables.options[i].x, achetables.options[i].y,
                             achetables.options[i].w, achetables.options[i].h), 7])
                    else:
                        liste_rafraichir.append([achetables.options[i].images[0].subsurface(
                            (0, 0, achetables.options[i].w, resolution.current_h-170-achetables.options[i].y)),
                            (achetables.options[i].x, achetables.options[i].y,
                             achetables.options[i].w, resolution.current_h-170-achetables.options[i].y), 7])

                # SI L'ACHETABLE EST TROP HAUTE

                if achetables.options[i].y < 100:

                    if achetables.options[i].x+achetables.options[i].w > position_souris[0] > achetables.options[i].x and \
                       achetables.options[i].y+achetables.options[i].h > position_souris[1] > achetables.options[i].y and \
                       100 < position_souris[0] < resolution.current_w-100 and 100 < position_souris[1] < resolution.current_h-170:
                        liste_rafraichir.append([achetables.options[i].images[1].subsurface(
                            (0, 100-achetables.options[i].y, achetables.options[i].w,
                             achetables.options[i].y+achetables.options[i].h-100)),
                            (achetables.options[i].x, 100, achetables.options[i].w,
                             achetables.options[i].y+achetables.options[i].h-100), 7])
                    else:
                        liste_rafraichir.append([achetables.options[i].images[0].subsurface(
                            (0, 100-achetables.options[i].y, achetables.options[i].w,
                             achetables.options[i].y+achetables.options[i].h-100)),
                            (achetables.options[i].x, 100, achetables.options[i].w,
                             achetables.options[i].y+achetables.options[i].h-100), 7])

        # GERER LES CHOIX

        if choix[0] == 1:  # MENU
            continuer = False

        if choix[0] == 2:  # ACHETER
            if choix[1] != 0:
                if choix[1] == 1 and session.argent >= 300:
                    for i in range(len(session.inventaire)):
                        if session.inventaire[i] == 0:
                            session.inventaire[i] = 1
                            session.argent -= 300
                            break
                if choix[1] == 2 and session.argent >= 500:
                    for i in range(len(session.inventaire)):
                        if session.inventaire[i] == 0:
                            session.inventaire[i] = 2
                            session.argent -= 500
                            break
                if choix[1] == 3 and session.argent >= 450:
                    for i in range(len(session.inventaire)):
                        if session.inventaire[i] == 0:
                            session.inventaire[i] = 3
                            session.argent -= 450
                            break
                if choix[1] == 4 and session.argent >= 250:
                    for i in range(len(session.inventaire)):
                        if session.inventaire[i] == 0:
                            session.inventaire[i] = 4
                            session.argent -= 250
                            break

            # METTRE A JOUR L'AFFICHAGE DE L'ARGENT

            liste_rafraichir.append([FOND.subsurface((texte[0], texte[1], texte[2], texte[3])),
                                     (texte[0], texte[1], texte[2], texte[3]),0])
            texte[4] = "Argent: "+str(session.argent)+"$"
            texte[2] = len(texte[4])*32
            texte[3] = 64
            texte[0] = (resolution.current_w-texte[2])//2
            texte[1] = 18
            texte[5] = pygame.Surface((texte[2], texte[3]))
            texte[5].fill((255, 255, 255))
            texte[5].set_colorkey((255, 255, 255))
            for i in range(len(texte[4])):
                texte[5].blit(CARACTERES.subsurface(((ord(texte[4][i]) % 10)*32,
                                                     (ord(texte[4][i])//10)*64, 32, 64)), (i*32, 0))
            liste_rafraichir.append([texte[5],(texte[0], texte[1], texte[2], texte[3]), 7])

    return liste_rafraichir, liste_messages, session


def menu_inventaire(ecran, resolution, liste_rafraichir, liste_messages, session):

    global MENU_INVENTAIRE
    global FOND
    global ITEMS

    # CREER LES CURSEURS

    curseur = ["           1            ",
               "           1            ",
               "        11 1 11         ",
               "      11001110011       ",
               "     10011 1 11001      ",
               "    1011   1   1101     ",
               "   101     1     101    ",
               "   101     1     101    ",
               "  101      1      101   ",
               "  101      1      101   ",
               "   1       1       1    ",
               "11111111111111111111111 ",
               "   1       1       1    ",
               "  101      1      101   ",
               "  101      1      101   ",
               "   101     1     101    ",
               "   101     1     101    ",
               "    1011   1   1101     ",
               "     10011 1 11001      ",
               "      11001110011       ",
               "        11 1 11         ",
               "           1            ",
               "           1            ",
               "                        "]

    data_cible = pygame.cursors.compile(curseur, "1", "0")

    curseur = ["        11111111        ",
               "      110000000011      ",
               "    1100000000000011    ",
               "   100000000000000001   ",
               "  10000000000000000001  ",
               "  10110000000000001101  ",
               " 1001010000000000101001 ",
               " 1001001000000001001001 ",
               "100010001000000100010001",
               "100010000100001000010001",
               "100010000010010000010001",
               "100010000001100000010001",
               "100010000000100000010001",
               "100010000000010000010001",
               "100010000000001000010001",
               "100010000000000100010001",
               " 1001000000000001001001 ",
               " 1001000000000000101001 ",
               "  10100000000000001101  ",
               "  10000000000000000001  ",
               "   100000000000000001   ",
               "    1100000000000011    ",
               "      110000000011      ",
               "        11111111        "]

    data_item = pygame.cursors.compile(curseur, "0", "1")

    # CREER LE FOND AVEC LE PERSONNAGE

    fond = pygame.Surface((resolution.current_w, resolution.current_h))
    fond.blit(FOND, (0, 0))
    fond.blit(MENU_INVENTAIRE.subsurface((0, 64, 336, 512)),
              ((resolution.current_w//2-336)//2, (resolution.current_h-512)//2))
    ecran.blit(fond, (0, 0))
    pygame.display.flip()

    # METTRE A JOUR L'INVENTAIRE ET L'EQUIPEMENT SI CE N'EST PAS DEJA LE CAS

    for i in range(96-len(session.inventaire)):
        session.inventaire.append(0)
    for i in range(4-len(session.equipement)):
        session.equipement.append(0)

    # CREER LE BOUTON DE RETOUR AU MENU

    menu = Menu()
    menu.x = 0
    menu.y = resolution.current_h-128
    menu.w = resolution.current_w//2
    menu.h = 128
    menu.options.append(Options_Menu())
    menu.options[0].message = "Menu"
    menu.type = 2
    menu = creer_images_et_positions_menu(menu)

    # CREER LES CASES DE L'INVENTAIRE ET LES AFFICHER

    cases = Menu()
    cases.x = resolution.current_w//2
    cases.y = 0
    cases.w = resolution.current_w//2
    cases.h = resolution.current_h

    for i in range(96):

        # COORDONNEES DE LA CASE

        cases.options.append(Options_Menu())
        cases.options[i].w = int(64*resolution.current_w/1024)
        cases.options[i].h = cases.options[i].w
        cases.options[i].x = (resolution.current_w//2)+cases.options[i].w*(i % 8)
        cases.options[i].y = cases.options[i].h*(i//8)

        # CREER L'IMAGE

        cases.options[i].images = [pygame.Surface((64, 64)), pygame.Surface((64, 64))]

        cases.options[i].images[0].fill((255, 255, 255))
        cases.options[i].images[1].fill((255, 255, 255))
        cases.options[i].images[0].set_colorkey((255, 255, 255))
        cases.options[i].images[1].set_colorkey((255, 255, 255))

        cases.options[i].images[0].blit(MENU_INVENTAIRE.subsurface((0, 0, 64, 64)), (0, 0))
        cases.options[i].images[1].blit(MENU_INVENTAIRE.subsurface((64, 0, 64, 64)), (0, 0))

        cases.options[i].images[0].blit(ITEMS.subsurface(((session.inventaire[i] % 10)*52,
                                                          (session.inventaire[i]//10)*52, 52, 52)), (6, 6))
        cases.options[i].images[1].blit(ITEMS.subsurface(((session.inventaire[i] % 10)*52,
                                                          (session.inventaire[i]//10)*52, 52, 52)), (6, 6))

        # AGRANDIR PUIS AFFICHER L'IMAGE

        cases.options[i].images[0] = pygame.transform.scale(cases.options[i].images[0],
                                                            (cases.options[i].w, cases.options[i].h))
        cases.options[i].images[1] = pygame.transform.scale(cases.options[i].images[1],
                                                            (cases.options[i].w, cases.options[i].h))

        liste_rafraichir.append([cases.options[i].images[0], (cases.options[i].x, cases.options[i].y,
                                                             cases.options[i].w, cases.options[i].h), 7])

    # CREER LES CASES D'EQUIPEMENT

    equipement = Menu()
    equipement.x = 0
    equipement.y = 0
    equipement.w = resolution.current_w//2
    equipement.h = resolution.current_h-128

    for i in range(4):

        # COORDONNEES DE LA CASE

        equipement.options.append(Options_Menu())
        equipement.options[i].w = int(64*resolution.current_w/1024)
        equipement.options[i].h = equipement.options[i].w
        equipement.options[i].x = (resolution.current_w//2-336)//2+(336-equipement.options[i].w)//2
        equipement.options[i].y = \
            (resolution.current_h-512)//2+i*(equipement.options[i].w+(512-4*equipement.options[i].w)//4)

        # CREER L'IMAGE

        equipement.options[i].images = [pygame.Surface((64, 64)), pygame.Surface((64, 64))]

        equipement.options[i].images[0].fill((255, 255, 255))
        equipement.options[i].images[1].fill((255, 255, 255))
        equipement.options[i].images[0].set_colorkey((255, 255, 255))
        equipement.options[i].images[1].set_colorkey((255, 255, 255))

        equipement.options[i].images[0].blit(MENU_INVENTAIRE.subsurface((0, 0, 64, 64)), (0, 0))
        equipement.options[i].images[1].blit(MENU_INVENTAIRE.subsurface((64, 0, 64, 64)), (0, 0))

        equipement.options[i].images[0].blit(ITEMS.subsurface(((session.equipement[i] % 10)*52,
                                                          (session.equipement[i]//10)*52, 52, 52)), (6, 6))
        equipement.options[i].images[1].blit(ITEMS.subsurface(((session.equipement[i] % 10)*52,
                                                          (session.equipement[i]//10)*52, 52, 52)), (6, 6))

        # AGRANDIR PUIS METTRE EN TRANSPARENCE L'IMAGE

        equipement.options[i].images[0] = pygame.transform.scale(equipement.options[i].images[0],
                                                            (equipement.options[i].w, equipement.options[i].h))
        equipement.options[i].images[1] = pygame.transform.scale(equipement.options[i].images[1],
                                                            (equipement.options[i].w, equipement.options[i].h))
        equipement.options[i].images[0].set_alpha(225)
        equipement.options[i].images[1].set_alpha(225)

    # INITIALISATION DE VARIABLES AVANT LA BOUCLE

    liste_casques = [0, 1]
    liste_plastrons = [0, 2]
    liste_jambieres = [0, 3]
    liste_bottes = [0, 4]
    choix = [0, 0]
    tempo = 0
    case_selectionnee = -1
    item_selectionne = 0
    position_souris = [0, 0]
    continuer = True
    temps_actuel = pygame.time.get_ticks()

    while continuer:

        # RAFRAICHIR L'IMAGE

        liste_messages, liste_rafraichir = afficher_messages(liste_messages, liste_rafraichir, resolution)
        liste_rafraichir, temps_actuel, tempo = gerer_temps(ecran, tempo, liste_rafraichir, temps_actuel)

        choix[0] = 0

        # GERER LES ENTREES UTILISATEUR

        for entree in pygame.event.get():
            if entree.type == pygame.MOUSEMOTION:
                position_souris = [entree.pos[0], entree.pos[1]]
            if entree.type == pygame.MOUSEBUTTONUP:
                if entree.button == 1:

                    # CLIQUER SUR UNE OPTION DU MENU

                    for i in range(len(menu.options)):
                        if menu.options[i].x+menu.options[i].w > entree.pos[0] > menu.options[i].x and \
                           menu.options[i].y+menu.options[i].h > entree.pos[1] > menu.options[i].y:
                            choix[0] = i+1

                    # CLIQUER SUR UNE CASE D'EQUIPEMENT

                    for i in range(len(equipement.options)):
                        if equipement.options[i].x+equipement.options[i].w > entree.pos[0] > equipement.options[i].x and \
                           equipement.options[i].y+equipement.options[i].h > entree.pos[1] > equipement.options[i].y:

                            # PRENDRE L'ITEM ET DEPOSER LE NOUVEAU EN VERIFIANT QU'IL EST POSSIBLE DE METTRE L'ITEM

                            if i == 0 and item_selectionne in liste_casques:
                                item_selectionne, session.equipement[i] = session.equipement[i], item_selectionne
                            elif i == 1 and item_selectionne in liste_plastrons:
                                item_selectionne, session.equipement[i] = session.equipement[i], item_selectionne
                            elif i == 2 and item_selectionne in liste_jambieres:
                                item_selectionne, session.equipement[i] = session.equipement[i], item_selectionne
                            elif i == 3 and item_selectionne in liste_bottes:
                                item_selectionne, session.equipement[i] = session.equipement[i], item_selectionne

                            # RECREER L'IMAGE DE LA CASE

                            equipement.options[i].images = [pygame.Surface((64, 64)), pygame.Surface((64, 64))]
                            equipement.options[i].images[0].fill((255, 255, 255))
                            equipement.options[i].images[1].fill((255, 255, 255))
                            equipement.options[i].images[0].set_colorkey((255, 255, 255))
                            equipement.options[i].images[1].set_colorkey((255, 255, 255))
                            equipement.options[i].images[0].blit(MENU_INVENTAIRE.subsurface((0, 0, 64, 64)), (0, 0))
                            equipement.options[i].images[1].blit(MENU_INVENTAIRE.subsurface((64, 0, 64, 64)), (0, 0))
                            equipement.options[i].images[0].blit(ITEMS.subsurface(((session.equipement[i] % 10)*52,
                                                                                   (session.equipement[i]//10)*52, 52, 52)), (6, 6))
                            equipement.options[i].images[1].blit(ITEMS.subsurface(((session.equipement[i] % 10)*52,
                                                                                   (session.equipement[i]//10)*52, 52, 52)), (6, 6))

                            # AGRANDIR PUIS METTRE EN TRANSPARENCE LA CASE

                            equipement.options[i].images[0] = pygame.transform.scale(equipement.options[i].images[0],
                                                                                     (equipement.options[i].w, equipement.options[i].h))
                            equipement.options[i].images[1] = pygame.transform.scale(equipement.options[i].images[1],
                                                                                     (equipement.options[i].w, equipement.options[i].h))
                            equipement.options[i].images[0].set_alpha(225)
                            equipement.options[i].images[1].set_alpha(225)

                            # AJUSTER LE CURSEUR

                            if item_selectionne == 0:
                                pygame.mouse.set_cursor((24, 24), (11, 11), data_cible[0], data_cible[1])
                            else:
                                pygame.mouse.set_cursor((24, 24), (11, 11), data_item[0], data_item[1])

                    # CLIQUER SUR UN ITEM

                    for i in range(len(cases.options)):
                        if cases.options[i].x+cases.options[i].w > entree.pos[0] > cases.options[i].x and \
                           cases.options[i].y+cases.options[i].h > entree.pos[1] > cases.options[i].y:

                            # PRENDRE L'ITEM ET DEPOSER LE NOUVEAU

                            case_selectionnee = -1
                            item_selectionne, session.inventaire[i] = session.inventaire[i], item_selectionne

                            # RECREER L'IMAGE DE LA CASE

                            cases.options[i].images = [pygame.Surface((64, 64)), pygame.Surface((64, 64))]
                            cases.options[i].images[0].fill((255, 255, 255))
                            cases.options[i].images[1].fill((255, 255, 255))
                            cases.options[i].images[0].set_colorkey((255, 255, 255))
                            cases.options[i].images[1].set_colorkey((255, 255, 255))
                            cases.options[i].images[0].blit(MENU_INVENTAIRE.subsurface((0, 0, 64, 64)), (0, 0))
                            cases.options[i].images[1].blit(MENU_INVENTAIRE.subsurface((64, 0, 64, 64)), (0, 0))
                            cases.options[i].images[0].blit(ITEMS.subsurface(((session.inventaire[i] % 10)*52,
                                                                              (session.inventaire[i]//10)*52, 52, 52)), (6, 6))
                            cases.options[i].images[1].blit(ITEMS.subsurface(((session.inventaire[i] % 10)*52,
                                                                              (session.inventaire[i]//10)*52, 52, 52)), (6, 6))

                            # AGRANDIR PUIS AFFICHER LA CASE

                            cases.options[i].images[0] = pygame.transform.scale(cases.options[i].images[0],
                                                                                (cases.options[i].w, cases.options[i].h))
                            cases.options[i].images[1] = pygame.transform.scale(cases.options[i].images[1],
                                                                                (cases.options[i].w, cases.options[i].h))
                            liste_rafraichir.append([fond.subsurface((cases.options[i].x, cases.options[i].y,
                                                                      cases.options[i].w, cases.options[i].h)),
                                                     (cases.options[i].x, cases.options[i].y,
                                                      cases.options[i].w, cases.options[i].h), 0])
                            liste_rafraichir.append([cases.options[i].images[0],
                                                     (cases.options[i].x, cases.options[i].y,
                                                      cases.options[i].w, cases.options[i].h), 7])

                            # AJUSTER LE CURSEUR

                            if item_selectionne == 0:
                                pygame.mouse.set_cursor((24, 24), (11, 11), data_cible[0], data_cible[1])
                            else:
                                pygame.mouse.set_cursor((24, 24), (11, 11), data_item[0], data_item[1])

        # AFFICHER LE BOUTON DE RETOUR AU MENU

        for i in range(len(menu.options)):
            if menu.options[i].x+menu.options[i].w > position_souris[0] > menu.options[i].x and \
               menu.options[i].y+menu.options[i].h > position_souris[1] > menu.options[i].y:
                liste_rafraichir.append([menu.options[i].images[1],
                                         (menu.options[i].x, menu.options[i].y, menu.options[i].w, menu.options[i].h), 7])
            else:
                liste_rafraichir.append([menu.options[i].images[0],
                                         (menu.options[i].x, menu.options[i].y, menu.options[i].w, menu.options[i].h), 7])

        # AFFICHER LES CHANGEMENTS DE CASE

        for i in range(len(cases.options)):
            if cases.options[i].x+cases.options[i].w > position_souris[0] > cases.options[i].x and \
               cases.options[i].y+cases.options[i].h > position_souris[1] > cases.options[i].y and \
               case_selectionnee != i:
                liste_rafraichir.append([cases.options[i].images[1],
                                         (cases.options[i].x, cases.options[i].y, cases.options[i].w, cases.options[i].h), 7])
                if case_selectionnee != -1:
                    liste_rafraichir.append([fond.subsurface((cases.options[case_selectionnee].x, cases.options[case_selectionnee].y,
                                             cases.options[case_selectionnee].w, cases.options[case_selectionnee].h)),
                                            (cases.options[case_selectionnee].x, cases.options[case_selectionnee].y,
                                             cases.options[case_selectionnee].w, cases.options[case_selectionnee].h), 0])
                    liste_rafraichir.append([cases.options[case_selectionnee].images[0],
                                            (cases.options[case_selectionnee].x, cases.options[case_selectionnee].y,
                                             cases.options[case_selectionnee].w, cases.options[case_selectionnee].h), 7])
                case_selectionnee = i

        if case_selectionnee != -1 and position_souris[0] < resolution.current_w//2:
            liste_rafraichir.append([fond.subsurface((cases.options[case_selectionnee].x, cases.options[case_selectionnee].y,
                                     cases.options[case_selectionnee].w, cases.options[case_selectionnee].h)),
                                    (cases.options[case_selectionnee].x, cases.options[case_selectionnee].y,
                                     cases.options[case_selectionnee].w, cases.options[case_selectionnee].h), 0])
            liste_rafraichir.append([cases.options[case_selectionnee].images[0],
                                    (cases.options[case_selectionnee].x, cases.options[case_selectionnee].y,
                                     cases.options[case_selectionnee].w, cases.options[case_selectionnee].h), 7])
            case_selectionnee = -1

        # AFFICHER LES CASES D'EQUIPEMENT

        for i in range(len(equipement.options)):
            liste_rafraichir.append([fond.subsurface((equipement.options[i].x, equipement.options[i].y, equipement.options[i].w, equipement.options[i].h)),
                                     (equipement.options[i].x, equipement.options[i].y, equipement.options[i].w, equipement.options[i].h), 7])
            if equipement.options[i].x+equipement.options[i].w > position_souris[0] > equipement.options[i].x and \
               equipement.options[i].y+equipement.options[i].h > position_souris[1] > equipement.options[i].y:
                liste_rafraichir.append([equipement.options[i].images[1],
                                         (equipement.options[i].x, equipement.options[i].y, equipement.options[i].w, equipement.options[i].h), 7])
            else:
                liste_rafraichir.append([equipement.options[i].images[0],
                                         (equipement.options[i].x, equipement.options[i].y, equipement.options[i].w, equipement.options[i].h), 7])

        # GERER LES CHOIX

        if choix[0] == 1:
            continuer = False

    # CALCULER L'ARMURE

    session.armure = 0
    # liste qui associe a un type d'item ses points d'armure
    liste_armure_equipement = [0, 1, 2, 2, 1]
    for item in session.equipement:
        session.armure += liste_armure_equipement[item]

    # CHANGER LE CURSEUR

    pygame.mouse.set_cursor((24, 24), (11, 11), data_cible[0], data_cible[1])

    # DEPOSER/DETRUIRE L'ITEM SELECTIONNE S'IL Y EN A UN

    if item_selectionne != 0:
        for i, item in enumerate(session.inventaire):
            if item == 0:
                session.inventaire[i] = item_selectionne
                break

    return liste_rafraichir, liste_messages, session
