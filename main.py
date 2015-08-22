# -*- coding:Utf-8 -*

import pygame._view
import sys
from fonctions import *
from sous_fonctions import *

VERSION = "0.1.1"

# INITIALISATION DE PYGAME ET OBTENTION DE LA RESOLUTION DE L'UTILISATEUR

pygame.display.init()
resolution = pygame.display.Info()
ecran = pygame.display.set_mode((resolution.current_w, resolution.current_h), pygame.FULLSCREEN | pygame.DOUBLEBUF | pygame.HWSURFACE)

# INITIALISATION DE VARIABLES

programme_continuer = True
jeu_continuer = False
session_continuer = False

position_souris = [0, 0]
liste_messages = []
temps_actuel = 0
tempo = 0

joueur = Joueur()
joueur = charger_image_joueur(joueur)

position_ecran_x = (resolution.current_w/2)-512
position_ecran_y = (resolution.current_h/2)-288

joueur.hitbox.w = 32
joueur.hitbox.h = 48

# CREATION / VERIFICATION DES DOSSIERS DE SAUVEGARDE

try:
    os.chdir(os.getcwd()+"\\saves")
    path = os.getcwd().split("\\")
    del path[len(path)-1]
    os.chdir("\\".join(path))
except:
    os.mkdir(os.getcwd()+"\\saves")

a = open("saves/liste_personnages.txt", "a")
a.close()
del a

with open("saves/liste_personnages.txt", "r+") as liste_personnages:
    chaine = liste_personnages.read().split("\n")
    del chaine[0]
    i = 0
    while i < len(chaine):
        try:
            open("saves/"+chaine[i]+".txt", "r")
            i += 1
        except:
            del chaine[i]

with open("saves/liste_personnages.txt", "w") as liste_personnages:
    liste_personnages.write("\n"+"\n".join(chaine))


del liste_personnages
del chaine
del i

# CREATION / VERIFICATION DU DOSSIER DE SCREENSHOTS

try:
    os.chdir(os.getcwd()+"\\screenshots")
    path = os.getcwd().split("\\")
    del path[len(path)-1]
    os.chdir("\\".join(path))
except:
    os.mkdir(os.getcwd()+"\\screenshots")

# OBTENTION / CREATION DES RACCOURCIS

try:
    with open("raccourcis.txt", "r") as fichier_raccourcis:
        raccourcis = fichier_raccourcis.read().split("\n")
        for i in range(len(raccourcis)):
            raccourcis[i] = raccourcis[i].split("=")
            raccourcis[i][0] = int(raccourcis[i][0])
except:
    raccourcis = [[pygame.K_w, "Defaut"],
                  [pygame.K_s, "Defaut"],
                  [pygame.K_a, "Defaut"],
                  [pygame.K_d, "Defaut"],
                  [pygame.K_e, "Defaut"]]

# DEBUT PROGRAMME

liste_rafraichir = mettre_fond(ecran)
menu_programme = creer_menu_programme(resolution)

while programme_continuer:  # MENU PRINCIPALE

    liste_rafraichir, choix, position_souris = obtenir_choix_menu_et_afficher_selection(menu_programme, position_souris, liste_rafraichir)

    liste_messages, liste_rafraichir = afficher_messages(liste_messages, liste_rafraichir, resolution)
    liste_rafraichir, temps_actuel, tempo = gerer_temps(ecran, tempo, liste_rafraichir, temps_actuel)

    if choix == 1:  # CREER UN NOUVEAU PERSONNAGE

        if nombre_de_saves() < 3:
            liste_rafraichir = mettre_fond(ecran)
            session, a, liste_rafraichir, liste_messages = creer_session(ecran, resolution, liste_rafraichir, liste_messages)
            if a == 0:
                session_continuer = True
            else:
                temps_actuel = pygame.time.get_ticks()
                liste_rafraichir = mettre_fond(ecran)
        else:
            creer_message(liste_messages, resolution, "VOUS NE POUVEZ PAS CREER PLUS DE 3 SESSIONS")

    elif choix == 2:  # CHOISIR UN PERSONNAGE

        liste_rafraichir = mettre_fond(ecran)
        session, a, liste_rafraichir, liste_messages = choisir_session(ecran, resolution, liste_rafraichir, liste_messages)
        if a == 0:
            session_continuer = True
        else:
            temps_actuel = pygame.time.get_ticks()
            liste_rafraichir = mettre_fond(ecran)

    elif choix == 3:

        liste_rafraichir = mettre_fond(ecran)
        raccourcis = choisir_raccourcis(ecran, resolution, liste_rafraichir, raccourcis)
        liste_rafraichir = mettre_fond(ecran)
        temps_actuel = pygame.time.get_ticks()

    elif choix == 4:  # QUITTER LE JEU

        sys.exit(0)

    if session_continuer:  # PREPARER A ALLER DANS LE MENU DU PERSONNAGE
        temps_actuel = pygame.time.get_ticks()
        liste_rafraichir = mettre_fond(ecran)
        menu_session = creer_menu_session(resolution, session)

    while session_continuer:  # MENU DU PERSONNAGE

        liste_rafraichir, choix, position_souris = obtenir_choix_menu_et_afficher_selection(menu_session, position_souris, liste_rafraichir)

        liste_messages, liste_rafraichir = afficher_messages(liste_messages, liste_rafraichir, resolution)
        liste_rafraichir, temps_actuel, tempo = gerer_temps(ecran, tempo, liste_rafraichir, temps_actuel)

        if choix == 1 and not session.partie:  # NOUVELLE PARTIE

            joueur = reset_stats_joueur(joueur, session)
            joueur.attaques.autorisation = list()
            jeu_continuer = True
            niveau = 0

        elif choix == 1 and session.partie:  # CONTINUER LA PARTIE

            map = session.map
            map = charger_images_monstres(map)
            map = charger_images_objets(map)
            for i in range(map.nombre_de_salles):
                map = generer_images_salles(map, i)

            joueur = session.joueur
            joueur = charger_image_joueur(joueur)
            joueur.attaques.autorisation = []
            joueur.temps_depuis_invincible = 0
            joueur.attaques.temps_derniere_attaque = 0
            joueur.attaques.entites = []
            jeu_continuer = True
            niveau = map.niveau

        elif choix == 2:  # ARBRE DE COMPETENCES

            liste_rafraichir = mettre_fond(ecran)
            session, liste_rafraichir, liste_messages = \
                choisir_competences(ecran, resolution, liste_rafraichir, liste_messages, session)
            liste_rafraichir = mettre_fond(ecran)
            temps_actuel = pygame.time.get_ticks()

        elif choix == 4:  # QUITTER LA SESSION

            chaine = "saves/"+session.nom+".txt"
            with open(chaine, "wb") as sauvegarde:
                pickler = pickle.Pickler(sauvegarde)
                pickler.dump(session)
            liste_rafraichir = mettre_fond(ecran)
            session_continuer = False

        if jeu_continuer:  # PREPARER A LA BOUCLE DU JEU
            temps_actuel = pygame.time.get_ticks()
            liste_rafraichir = mettre_fond(ecran)

        while jeu_continuer:  # CREATION D'UN NOUVEL ETAGE

            if not session.partie:

                joueur.salle = -1
                niveau += 1
                map = generer_map(niveau)

            boucle_jeu_continuer = True

            while boucle_jeu_continuer:  # CHARGEMENT DE LA NOUVELLE SALLE

                if not session.partie:

                    joueur = initialiser_joueur(map, joueur)
                    map = initialiser_salle(map, joueur)
                    map = generer_images_salles(map, joueur.salle)
                    minimap = charger_minimap(map, joueur)

                if session.partie:

                    map = session.map
                    joueur = session.joueur
                    minimap = charger_minimap(map, joueur)

                liste_rafraichir = []
                joueur.attaques.entites = []

                afficher_interface(position_ecran_x, position_ecran_y, ecran, joueur, session)
                ecran.blit(map.salles[joueur.salle].image, (position_ecran_x, position_ecran_y))
                ecran.blit(joueur.images.bas[0], (position_ecran_x+joueur.x, position_ecran_y+joueur.y))
                ecran.blit(minimap, (position_ecran_x+824, position_ecran_y+10))
                pygame.display.flip()

                tempo = 0
                salle_continuer = True

                session.partie = False

                while salle_continuer:  # BOUCLE DU JEU

                    choix = 0

                    # GERER RAFRAICHISSEMENT DE L'IMAGE, FPS, ET TEMPO

                    liste_rafraichir, temps_actuel, tempo = gerer_temps(ecran, tempo, liste_rafraichir, temps_actuel)

                    # OBTENIR LES ENTREES UTILISATEUR ET LES TRAITER

                    for entree in pygame.event.get():

                        if entree.type == pygame.KEYDOWN:
                            if entree.key == pygame.K_ESCAPE:
                                choix, joueur = gerer_menu_jeu(ecran, position_souris, position_ecran_x, position_ecran_y, raccourcis, joueur)
                                temps_actuel = pygame.time.get_ticks()
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
                            if entree.key == raccourcis[4][0]:
                                if joueur.bombes > 0:
                                    joueur.attaques.autorisation.append(2)
                                    rafraichir_bombes(position_ecran_x, position_ecran_y, joueur, liste_rafraichir, joueur.bombes-1)
                            if entree.key == pygame.K_PRINT:
                                pygame.image.save(ecran,"screenshots/"+str(int(time.time()))+".png")

                        if entree.type == pygame.MOUSEBUTTONDOWN:
                            if entree.button == 1:
                                joueur.attaques.autorisation.append(1)

                        if entree.type == pygame.MOUSEBUTTONUP:
                            if entree.button == 1:
                                joueur.attaques.autorisation.remove(1)

                        if entree.type == pygame.MOUSEMOTION:
                            joueur.attaques.position_souris = [entree.pos[0], entree.pos[1]]

                    # DIFFERENTES CHOSES A GERER PENDANT QUE LE JEU TOURNE

                    liste_rafraichir, blocs_a_proximite = deplacer_personnage(map, joueur, liste_rafraichir, tempo, position_ecran_x, position_ecran_y)

                    if joueur.deplacement_x != 0 or joueur.deplacement_y != 0:

                        for i in range(4):

                            if collisions(joueur.hitbox, map.salles[joueur.salle].blocs_hitboxs[blocs_a_proximite[i][1]][blocs_a_proximite[i][0]]):
                                if 13 <= map.salles[joueur.salle].blocs_type[blocs_a_proximite[i][1]][blocs_a_proximite[i][0]] <= 17:
                                    salle_continuer = False

                                if map.salles[joueur.salle].blocs_type[blocs_a_proximite[i][1]][blocs_a_proximite[i][0]] == 13:
                                    boucle_jeu_continuer = False

                        map, joueur, liste_rafraichir = ramasser_objets(map, joueur, liste_rafraichir, position_ecran_x, position_ecran_y)

                    map, liste_rafraichir, joueur = gerer_portes(map, joueur, liste_rafraichir, position_ecran_x, position_ecran_y)

                    liste_rafraichir = afficher_objets(map, liste_rafraichir, position_ecran_x, position_ecran_y, joueur)

                    joueur = creer_attaque(joueur, position_ecran_x, position_ecran_y, session)

                    joueur, map, liste_rafraichir = gerer_attaques(joueur, position_ecran_x, position_ecran_y, map, liste_rafraichir, session)

                    map, liste_rafraichir, joueur = deplacer_monstres(map, joueur, tempo, liste_rafraichir, position_ecran_x, position_ecran_y, session)

                    map, liste_rafraichir, session = gerer_mort_monstres(map, joueur, liste_rafraichir, position_ecran_x, position_ecran_y, session)

                    joueur = gerer_invincibilite(joueur)

                    liste_rafraichir, session = rafraichir_niveau_session(position_ecran_x, position_ecran_y, session, liste_rafraichir)

                    liste_rafraichir = afficher_minibar(map, joueur, position_ecran_x, position_ecran_y, liste_rafraichir)

                    liste_rafraichir.append([map.salles[joueur.salle].image.subsurface((824, 10, 126, 88)), (position_ecran_x+824, position_ecran_y+10, 126, 88), 1])
                    liste_rafraichir.append([minimap, (position_ecran_x+824, position_ecran_y+10, 126, 88), 6])

                    if session.competences[11] > 0 and len(map.salles[joueur.salle].ennemis) > 0 and tempo == 3:
                        liste_rafraichir, joueur = rafraichir_mana(position_ecran_x, position_ecran_y, joueur, liste_rafraichir, session, joueur.mana+session.competences[11])

                    # GERER LA MORT DU PERSONNAGE

                    if joueur.points_de_vies <= 0:
                        if joueur.nombre_de_vies <= 0:
                            salle_continuer = False
                            boucle_jeu_continuer = False
                            jeu_continuer = False
                            menu_session = creer_menu_session(resolution, session)

                            afficher_game_over(ecran, resolution, niveau)

                            liste_rafraichir = []
                            liste_rafraichir = mettre_fond(ecran)
                        else:
                            liste_rafraichir, joueur = rafraichir_nombre_de_vies(position_ecran_x, position_ecran_y, joueur, liste_rafraichir, joueur.nombre_de_vies-1)
                            liste_rafraichir, joueur = rafraichir_vie(position_ecran_x, position_ecran_y, joueur, liste_rafraichir, joueur.vie_maximum, joueur.vie_maximum)

                    # GERER LE MENU DU JEU

                    if choix == 1:  # CONTINUER LE JEU

                        liste_rafraichir.append([map.salles[joueur.salle].image.subsurface((130, 38, 700, 500)), (position_ecran_x+130, position_ecran_y+38, 700, 500), 1])

                    if choix == 2:  # RECOMMENCER LA PARTIE

                        liste_rafraichir = mettre_fond(ecran)
                        salle_continuer = False
                        boucle_jeu_continuer = False
                        joueur = reset_stats_joueur(joueur, session)
                        joueur.attaques.autorisation = []
                        niveau = 0

                    if choix == 3:  # QUITTER LA PARTIE

                        session.partie = True
                        session.map = map
                        session.joueur = joueur
                        salle_continuer = False
                        boucle_jeu_continuer = False
                        jeu_continuer = False
                        liste_rafraichir = mettre_fond(ecran)

                    if choix == 4:  # QUITTER LE JEU

                        session.partie = True
                        session.map = map
                        session.joueur = joueur

                        chaine = "saves/"+session.nom+".txt"
                        with open(chaine, "wb") as sauvegarde:
                            pickler = pickle.Pickler(sauvegarde)
                            pickler.dump(session)
                        sys.exit(0)
