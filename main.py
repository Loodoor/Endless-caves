# -*- coding:utf_8 -*

import pygame._view
import sys
from fonctions import *
from sous_fonctions import *

VERSION = "0.3.1"

# INITIALISATION DE PYGAME ET OBTENTION DE LA RESOLUTION DE L'UTILISATEUR

pygame.display.init()
resolution = pygame.display.Info()
ecran = pygame.display.set_mode((resolution.current_w, resolution.current_h), pygame.FULLSCREEN | pygame.DOUBLEBUF | pygame.HWSURFACE)

# INITIALISATION DE VARIABLES

cible = ["           1            ",
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
data = pygame.cursors.compile(cible, "1", "0")
pygame.mouse.set_cursor((24, 24), (11, 11), data[0], data[1])

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

# VERIFICATION DE SESSION.SORTS

with open("saves/liste_personnages.txt", "r") as liste_personnages:
    liste = liste_personnages.read().split("\n")
    i = 0
    while i < len(liste):
        if liste[i] == str():
            del liste[i]
            i -= 1
        i += 1
    for i in range(len(liste)):
        with open("saves/"+liste[i]+".txt", "rb") as fichier_session:
            depickler = pickle.Unpickler(fichier_session)
            session_test = depickler.load()
        if len(session_test.sorts) > 2:
            session_test.sorts = session_test.sorts[:2]
        while len(session_test.sorts) < 2:
            session_test.sorts += [0]
        with open("saves/"+liste[i]+".txt", "wb") as fichier_session:
            pickler = pickle.Pickler(fichier_session)
            pickler.dump(session_test)

# CREATION / VERIFICATION DU DOSSIER DE SCREENSHOTS

try:
    os.chdir(os.getcwd()+"\\screenshots")
    path = os.getcwd().split("\\")
    del path[len(path)-1]
    os.chdir("\\".join(path))
except:
    os.mkdir(os.getcwd()+"\\screenshots")

# OBTENTION / CREATION DES RACCOURCIS

raccourcis = [[pygame.K_w, "Defaut"],
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
            raccourcis[i] = raccourcis_obtenus[i].split("=")
            raccourcis[i][0] = int(raccourcis[i][0])
except:
    pass

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
            creer_message(liste_messages, resolution, "Vous ne pouvez pas creer plus de 3 sessions")

    elif choix == 2:  # CHOISIR UN PERSONNAGE

        liste_rafraichir = mettre_fond(ecran)
        session, a, liste_rafraichir, liste_messages = choisir_session(ecran, resolution, liste_rafraichir, liste_messages)
        if a == 0:
            session_continuer = True
        else:
            temps_actuel = pygame.time.get_ticks()
            liste_rafraichir = mettre_fond(ecran)

    elif choix == 3:  # CHOISIR LES CONTROLES

        liste_rafraichir = mettre_fond(ecran)
        raccourcis = choisir_raccourcis(ecran, resolution, liste_rafraichir, liste_messages, raccourcis)
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

        if session.partie:  # S'IL Y A UNE SAUVEGARDE DE PARTIE
            if choix == 1:  # CONTINUER LA PARTIE

                etage = session.etage
                etage = charger_images_monstres(etage)
                etage = charger_images_objets(etage)
                for i in range(etage.nombre_de_salles):
                    etage = generer_images_salles(etage, i)
                for salle in etage.salles:
                    for ennemi in salle.ennemis:
                        ennemi.paralyse = False

                joueur = session.joueur
                joueur = charger_image_joueur(joueur)
                joueur.attaques.autorisation = []
                joueur.temps_depuis_invincible = 0
                joueur.attaques.temps_derniere_attaque = 0
                joueur.attaques.entites = []
                jeu_continuer = True
                niveau = etage.niveau
                sort_selectionne = 0
                joueur.sorts_actifs = list()
                joueur.sorts_temps_activation = list()
                for i in range(len(session.sorts)):
                    joueur.sorts_actifs.append(False)
                    joueur.sorts_temps_activation.append(0)

            elif choix == 2:  # RECOMMENCER UNE PARTIE

                joueur = reset_stats_joueur(joueur, session)
                joueur.attaques.autorisation = list()
                jeu_continuer = True
                sort_selectionne = 0
                niveau = 0
                joueur.sorts = list(session.sorts)
                joueur.sorts_actifs = list()
                joueur.sorts_temps_activation = list()
                for i in range(len(session.sorts)):
                    joueur.sorts_actifs.append(False)
                    joueur.sorts_temps_activation.append(0)
                session.partie = False

            elif choix == 3:  # ARBRE DE COMPETENCES

                liste_rafraichir = mettre_fond(ecran)
                session, liste_rafraichir, liste_messages = \
                    choisir_competences(ecran, resolution, liste_rafraichir, liste_messages, session)
                liste_rafraichir = mettre_fond(ecran)
                temps_actuel = pygame.time.get_ticks()

            elif choix == 4:  # ARBRE DE SORTS
                liste_rafraichir = mettre_fond(ecran)
                session, liste_rafraichir, liste_messages = \
                    choisir_sorts(ecran, resolution, liste_rafraichir, liste_messages, session)
                liste_rafraichir = mettre_fond(ecran)
                temps_actuel = pygame.time.get_ticks()

            elif choix == 5:  # ACHETER
                liste_rafraichir = mettre_fond(ecran)
                liste_rafraichir, liste_messages, session = \
                    achat_equipement(ecran, resolution, liste_rafraichir, liste_messages, session)
                liste_rafraichir = mettre_fond(ecran)
                temps_actuel = pygame.time.get_ticks()

            elif choix == 6:  # INVENTAIRE
                liste_rafraichir = mettre_fond(ecran)
                liste_rafraichir, liste_messages, session = \
                    menu_inventaire(ecran, resolution, liste_rafraichir, liste_messages, session)
                liste_rafraichir = mettre_fond(ecran)
                temps_actuel = pygame.time.get_ticks()

            elif choix == 7:  # QUITTER LA SESSION

                chaine = "saves/"+session.nom+".txt"
                with open(chaine, "wb") as sauvegarde:
                    pickler = pickle.Pickler(sauvegarde)
                    pickler.dump(session)
                liste_rafraichir = mettre_fond(ecran)
                session_continuer = False

        else:  # S'IL N'Y A PAS DE SAUVEGARDE DE PARTIE
            if choix == 1:  # NOUVELLE PARTIE

                joueur = reset_stats_joueur(joueur, session)
                joueur.attaques.autorisation = list()
                jeu_continuer = True
                sort_selectionne = 0
                niveau = 0
                joueur.sorts = list(session.sorts)
                joueur.sorts_actifs = list()
                joueur.sorts_temps_activation = list()
                for i in range(len(session.sorts)):
                    joueur.sorts_actifs.append(False)
                    joueur.sorts_temps_activation.append(0)

            elif choix == 2:  # ARBRE DE COMPETENCES

                liste_rafraichir = mettre_fond(ecran)
                session, liste_rafraichir, liste_messages = \
                    choisir_competences(ecran, resolution, liste_rafraichir, liste_messages, session)
                liste_rafraichir = mettre_fond(ecran)
                temps_actuel = pygame.time.get_ticks()

            elif choix == 3:  # ARBRE DE SORTS
                liste_rafraichir = mettre_fond(ecran)
                session, liste_rafraichir, liste_messages = \
                    choisir_sorts(ecran, resolution, liste_rafraichir, liste_messages, session)
                liste_rafraichir = mettre_fond(ecran)
                temps_actuel = pygame.time.get_ticks()

            elif choix == 4:  # ACHETER
                liste_rafraichir = mettre_fond(ecran)
                liste_rafraichir, liste_messages, session = \
                    achat_equipement(ecran, resolution, liste_rafraichir, liste_messages, session)
                liste_rafraichir = mettre_fond(ecran)
                temps_actuel = pygame.time.get_ticks()

            elif choix == 5:  # INVENTAIRE
                liste_rafraichir = mettre_fond(ecran)
                liste_rafraichir, liste_messages, session = \
                    menu_inventaire(ecran, resolution, liste_rafraichir, liste_messages, session)
                liste_rafraichir = mettre_fond(ecran)
                temps_actuel = pygame.time.get_ticks()

            elif choix == 6:  # QUITTER LA SESSION

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
                etage = generer_map(niveau)

            boucle_jeu_continuer = True

            while boucle_jeu_continuer:  # CHARGEMENT DE LA NOUVELLE SALLE

                if not session.partie:

                    joueur = initialiser_joueur(etage, joueur)
                    etage = initialiser_salle(etage, joueur)
                    etage = generer_images_salles(etage, joueur.salle)
                    minietage = charger_minimap(etage, joueur)

                if session.partie:

                    etage = session.etage
                    joueur = session.joueur
                    minietage = charger_minimap(etage, joueur)

                liste_rafraichir = []
                joueur.attaques.entites = []

                afficher_interface(position_ecran_x, position_ecran_y, ecran, joueur, session)
                liste_rafraichir, sort_selectionne = changer_selection_sort(liste_rafraichir, position_ecran_x, position_ecran_y, joueur, sort_selectionne, sort_selectionne)
                ecran.blit(etage.salles[joueur.salle].image, (position_ecran_x, position_ecran_y))
                ecran.blit(joueur.images.bas[0], (position_ecran_x+joueur.x, position_ecran_y+joueur.y))
                ecran.blit(minietage, (position_ecran_x+824, position_ecran_y+10))
                pygame.display.flip()

                tempo = 0
                salle_continuer = True

                session.partie = False

                while salle_continuer:  # BOUCLE DU JEU

                    choix = 0

                    # GERER RAFRAICHISSEMENT DE L'IMAGE, FPS, ET TEMPO

                    liste_rafraichir, temps_actuel, tempo = gerer_temps(ecran, tempo, liste_rafraichir, temps_actuel)

                    # OBTENIR LES ENTREES UTILISATEUR ET LES TRAITER

                    touches = pygame.key.get_pressed()
                    joueur.deplacement_y = 0
                    joueur.deplacement_x = 0
                    if touches[raccourcis[0][0]] and not touches[raccourcis[1][0]]:
                        joueur.deplacement_y = -joueur.vitesse
                    if touches[raccourcis[1][0]] and not touches[raccourcis[0][0]]:
                        joueur.deplacement_y = joueur.vitesse
                    if touches[raccourcis[2][0]] and not touches[raccourcis[3][0]]:
                        joueur.deplacement_x = -joueur.vitesse
                    if touches[raccourcis[3][0]] and not touches[raccourcis[2][0]]:
                        joueur.deplacement_x = joueur.vitesse

                    touches = pygame.mouse.get_pressed()
                    if touches[0] and 1 not in joueur.attaques.autorisation:
                        joueur.attaques.autorisation.append(1)
                    if not touches[0] and 1 in joueur.attaques.autorisation:
                        joueur.attaques.autorisation.remove(1)

                    for entree in pygame.event.get():

                        if entree.type == pygame.KEYDOWN:
                            if entree.key == pygame.K_ESCAPE:
                                choix, joueur = gerer_menu_jeu(ecran, position_souris, position_ecran_x, position_ecran_y, raccourcis, joueur)
                                temps_actuel = pygame.time.get_ticks()

                        if entree.type == pygame.KEYUP:
                            if entree.key == raccourcis[4][0]:
                                if joueur.bombes > 0:
                                    joueur.attaques.autorisation.append(2)
                                    rafraichir_bombes(position_ecran_x, position_ecran_y, joueur, liste_rafraichir, joueur.bombes-1)
                            if entree.key == pygame.K_PRINT:
                                pygame.image.save(ecran, "screenshots/"+str(int(time.time()))+".png")
                            if entree.key == raccourcis[5][0]:
                                joueur, liste_rafraichir, sort_valide = enlever_mana_sorts(position_ecran_x, position_ecran_y, joueur, liste_rafraichir, session, 0)
                                if sort_valide:
                                    joueur.sorts_actifs[0] = True
                                joueur.sorts_temps_activation[0] = pygame.time.get_ticks()
                            if entree.key == raccourcis[6][0]:
                                joueur, liste_rafraichir, sort_valide = enlever_mana_sorts(position_ecran_x, position_ecran_y, joueur, liste_rafraichir, session, 1)
                                if sort_valide:
                                    joueur.sorts_actifs[1] = True
                                joueur.sorts_temps_activation[1] = pygame.time.get_ticks()
                            if entree.key == raccourcis[7][0]:
                                liste_rafraichir, joueur = regarder_la_map(etage, ecran, joueur, position_ecran_x, position_ecran_y, session, sort_selectionne, minietage, resolution, raccourcis)

                        if entree.type == pygame.MOUSEBUTTONDOWN:
                            if entree.button == 1:
                                if position_ecran_x+960 < entree.pos[0] < position_ecran_x+1024 and \
                                   position_ecran_y+576 < entree.pos[1] < position_ecran_y+640:
                                    liste_rafraichir, joueur = regarder_la_map(etage, ecran, joueur, position_ecran_x, position_ecran_y, session, sort_selectionne, minietage, resolution, raccourcis)
                            if entree.button == 4:
                                liste_rafraichir, sort_selectionne = \
                                    changer_selection_sort(liste_rafraichir, position_ecran_x, position_ecran_y, joueur, sort_selectionne, sort_selectionne-1)
                            if entree.button == 5:
                                liste_rafraichir, sort_selectionne = \
                                    changer_selection_sort(liste_rafraichir, position_ecran_x, position_ecran_y, joueur, sort_selectionne, sort_selectionne+1)

                        if entree.type == pygame.MOUSEBUTTONUP:
                            if entree.button == 3:
                                joueur, liste_rafraichir, sort_valide = \
                                    enlever_mana_sorts(position_ecran_x, position_ecran_y, joueur, liste_rafraichir, session, sort_selectionne)
                                if sort_valide:
                                    joueur.sorts_actifs[sort_selectionne] = True
                                joueur.sorts_temps_activation[sort_selectionne] = pygame.time.get_ticks()

                        if entree.type == pygame.MOUSEMOTION:
                            liste_rafraichir = afficher_bouton_map(position_ecran_x, position_ecran_y, entree, liste_rafraichir)
                            joueur.attaques.position_souris = [entree.pos[0], entree.pos[1]]

                    # DIFFERENTES CHOSES A GERER PENDANT QUE LE JEU TOURNE

                    liste_rafraichir, blocs_a_proximite = deplacer_personnage(etage, joueur, liste_rafraichir, tempo, position_ecran_x, position_ecran_y)

                    if joueur.deplacement_x != 0 or joueur.deplacement_y != 0:

                        for i in range(4):

                            if collisions(joueur.hitbox, etage.salles[joueur.salle].blocs_hitboxs[blocs_a_proximite[i][1]][blocs_a_proximite[i][0]]):
                                if 13 <= etage.salles[joueur.salle].blocs_type[blocs_a_proximite[i][1]][blocs_a_proximite[i][0]] <= 17:
                                    salle_continuer = False

                                if etage.salles[joueur.salle].blocs_type[blocs_a_proximite[i][1]][blocs_a_proximite[i][0]] == 13:
                                    boucle_jeu_continuer = False

                        etage, joueur, liste_rafraichir = ramasser_objets(etage, joueur, liste_rafraichir, position_ecran_x, position_ecran_y)

                    etage, liste_rafraichir, joueur = gerer_portes(etage, joueur, liste_rafraichir, position_ecran_x, position_ecran_y)

                    liste_rafraichir = afficher_objets(etage, liste_rafraichir, position_ecran_x, position_ecran_y, joueur)

                    joueur, etage = creer_attaque(joueur, position_ecran_x, position_ecran_y, session, etage, tempo)

                    joueur, etage, liste_rafraichir = gerer_attaques(joueur, position_ecran_x, position_ecran_y, etage, liste_rafraichir, session)

                    etage, liste_rafraichir, joueur = deplacer_monstres(etage, joueur, tempo, liste_rafraichir, position_ecran_x, position_ecran_y, session)

                    etage, liste_rafraichir, session = gerer_mort_monstres(etage, joueur, liste_rafraichir, position_ecran_x, position_ecran_y, session)

                    joueur = gerer_invincibilite(joueur)

                    liste_rafraichir, session, joueur = rafraichir_niveau_session(position_ecran_x, position_ecran_y, session, liste_rafraichir, joueur, etage)

                    liste_rafraichir = afficher_minibar(etage, joueur, position_ecran_x, position_ecran_y, liste_rafraichir)

                    liste_rafraichir, joueur = afficher_animation_joueur(joueur, etage, position_ecran_x, position_ecran_y, liste_rafraichir)

                    etage = gerer_poison(joueur, etage)

                    liste_rafraichir.append([etage.salles[joueur.salle].image.subsurface((824, 10, 126, 88)), (position_ecran_x+824, position_ecran_y+10, 126, 88), 1])
                    liste_rafraichir.append([minietage, (position_ecran_x+824, position_ecran_y+10, 126, 88), 6])

                    # GERER LA MORT DU PERSONNAGE

                    if joueur.points_de_vies <= 0:
                        if joueur.nombre_de_vies <= 0:
                            liste_rafraichir, temps_actuel, tempo = gerer_temps(ecran, tempo, liste_rafraichir, temps_actuel)
                            salle_continuer = False
                            boucle_jeu_continuer = False
                            jeu_continuer = False
                            afficher_game_over(ecran, resolution)
                            liste_rafraichir = mettre_fond(ecran)
                            liste_rafraichir, liste_messages, session = \
                                fin_de_partie(ecran, resolution, liste_rafraichir, liste_messages, session, etage)
                            liste_rafraichir = mettre_fond(ecran)
                            menu_session = creer_menu_session(resolution, session)
                            pygame.event.clear()
                            temps_actuel = pygame.time.get_ticks()
                        else:
                            liste_rafraichir, joueur = rafraichir_nombre_de_vies(position_ecran_x, position_ecran_y, joueur, liste_rafraichir, joueur.nombre_de_vies-1)
                            liste_rafraichir, joueur = rafraichir_vie(position_ecran_x, position_ecran_y, joueur, liste_rafraichir, joueur.vie_maximum, joueur.vie_maximum)

                    # GERER LE MENU DU JEU

                    if choix == 1:  # CONTINUER LE JEU

                        liste_rafraichir.append([etage.salles[joueur.salle].image.subsurface((130, 38, 700, 500)), (position_ecran_x+130, position_ecran_y+38, 700, 500), 1])

                    if choix == 2:  # RECOMMENCER LA PARTIE

                        liste_rafraichir = mettre_fond(ecran)
                        salle_continuer = False
                        boucle_jeu_continuer = False
                        joueur = reset_stats_joueur(joueur, session)
                        joueur.attaques.autorisation = []
                        niveau = 0
                        joueur.sorts = list(session.sorts)
                        joueur.sorts_actifs = list()
                        joueur.sorts_temps_activation = list()
                        for i in range(len(session.sorts)):
                            joueur.sorts_actifs.append(False)
                            joueur.sorts_temps_activation.append(0)

                    if choix == 3:  # QUITTER LA PARTIE

                        session.partie = True
                        session.etage = etage
                        session.joueur = joueur
                        salle_continuer = False
                        boucle_jeu_continuer = False
                        jeu_continuer = False
                        liste_rafraichir = mettre_fond(ecran)
                        menu_session = creer_menu_session(resolution, session)

                    if choix == 4:  # QUITTER LE JEU

                        session.partie = True
                        session.etage = etage
                        if joueur.animation_tete.activee:
                            joueur.animation_tete.activee = False
                        session.joueur = joueur

                        chaine = "saves/"+session.nom+".txt"
                        with open(chaine, "wb") as sauvegarde:
                            pickler = pickle.Pickler(sauvegarde)
                            pickler.dump(session)
                        sys.exit(0)
