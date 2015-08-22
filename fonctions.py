# -*- coding:Utf-8 -*

from sous_fonctions import *

VERSION = "0.1.1"


def generer_map(niveau):

    map = placer_salles(niveau)
    map = generer_salles(map)

    for i in range(map.nombre_de_salles):
        map = generer_hitboxs(map, i)

    return map


def reset_stats_joueur(joueur, session):

    joueur.argent = 0
    joueur.attaque = 40+(10*session.competences[0])
    joueur.bombes = 1
    joueur.cles = 1
    joueur.points_de_vies = 100+(30*session.competences[2])
    joueur.vie_maximum = 100+(30*session.competences[2])
    joueur.nombre_de_vies = 0
    joueur.vitesse = 5+session.competences[5]
    joueur.mana = 100+(20*session.competences[7])
    joueur.deplacement_x = 0
    joueur.deplacement_y = 0
    if session.competences[1] == 0:
        joueur.vitesse_attaque = 500
    elif session.competences[1] == 1:
        joueur.vitesse_attaque = 475
    elif session.competences[1] == 2:
        joueur.vitesse_attaque = 425

    joueur.temps_invincibilite = 1000
    joueur.temps_depuis_invincible = 0
    joueur.invincible = False

    for i in range(6):
        joueur.images.bas[i].set_alpha()
        joueur.images.haut[i].set_alpha()
        joueur.images.droite[i].set_alpha()
        joueur.images.gauche[i].set_alpha()

    return joueur


def initialiser_salle(map, joueur):

    map = initialiser_ennemis(map, joueur)
    map = initialiser_objets(map, joueur)

    return map


def creer_menu_session(resolution, session):

    menu_session = Menu()
    menu_session.x = 0
    menu_session.y = 128
    menu_session.w = resolution.current_w
    menu_session.h = resolution.current_h-128
    for i in range(4):
        menu_session.options.append(Options_Menu())
    if session.partie:
        menu_session.options[0].message = "Continuer la partie"
    if not session.partie:
        menu_session.options[0].message = "Nouvelle partie"
    menu_session.options[1].message = "Arbre de competences"
    menu_session.options[2].message = "Arbre de sorts"
    menu_session.options[3].message = "Quitter"
    menu_session.type = 1
    menu_session = creer_images_et_positions_menu(menu_session)

    return menu_session


def creer_menu_programme(resolution):

    menu_programme = Menu()
    menu_programme.x = 0
    menu_programme.y = 128
    menu_programme.w = resolution.current_w
    menu_programme.h = resolution.current_h-128
    for i in range(4):
        menu_programme.options.append(Options_Menu())

    menu_programme.options[0].message = "Nouveau personnage"
    menu_programme.options[1].message = "Liste des personnages"
    menu_programme.options[2].message = "Controles"
    menu_programme.options[3].message = "Quitter le jeu"
    menu_programme.type = 1
    menu_programme = creer_images_et_positions_menu(menu_programme)

    return menu_programme
