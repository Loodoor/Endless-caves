#-*- coding:Utf-8 -*

import sys
import os
import time
import pygame
import pickle
import pygame._view
from random import randrange
from classes import *
from fonctions import *
from sous_fonctions import *


VERSION=0.1



# INITIALISATION DE PYGAME



pygame.display.init()
resolution=pygame.display.Info()
ecran=pygame.display.set_mode((resolution.current_w,resolution.current_h),pygame.FULLSCREEN | pygame.DOUBLEBUF | pygame.HWSURFACE)



# INITIALISATION DE VARIABLES



programme_continuer=True
jeu_continuer=False
session_continuer=False
position_souris=[0,0]
liste_rafraichir=[]
liste_messages=[]
temps_actuel=0

joueur=Joueur()
joueur=charger_image_joueur(joueur)

position_ecran_x=(resolution.current_w/2)-512
position_ecran_y=(resolution.current_h/2)-288

raccourcis=[pygame.K_ESCAPE,
            pygame.K_w,
            pygame.K_s,
            pygame.K_a,
            pygame.K_d,
            pygame.K_e]
joueur.hitbox.w=32
joueur.hitbox.h=48



# CREATION / VERIFICATION DES DOSSIERS DE SAUVEGARDE



try:
    os.chdir(os.getcwd()+"\\saves")
    path=os.getcwd().split("\\")
    del path[len(path)-1]
    os.chdir("\\".join(path))
except:
    os.mkdir(os.getcwd()+"\\saves")

a=open("saves/liste_personnages.txt","a")
a.close()
del a

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


del liste_personnages
del chaine
del i



# DEBUT PROGRAMME


fond=pygame.image.load("images/fond.bmp")
ecran.blit(fond,(0,0))
pygame.display.flip()
menu_programme=creer_menu_programme(resolution)

while programme_continuer: # MENU PRINCIPALE



    liste_rafraichir,choix,position_souris=obtenir_choix_menu_et_afficher_selection(menu_programme,ecran,position_souris,liste_rafraichir)

    liste_messages,liste_rafraichir=afficher_messages(liste_messages,liste_rafraichir,resolution)
    rafraichir_image(liste_rafraichir,ecran)
    liste_rafraichir=[]
    temps_actuel=gerer_fps(temps_actuel)

    if choix==1:
        if obtenir_nombre_de_saves()<3:
            a=0
            session,a,liste_rafraichir,liste_messages=creer_session(ecran,resolution,liste_rafraichir,liste_messages)
            if a==0:
                session_continuer=True
                menu_session=creer_menu_session(resolution,session)
        else:
            creer_message(liste_messages,resolution,"VOUS NE POUVEZ PAS CREER PLUS DE 3 SESSIONS")
    elif choix==2:
        a=0
        session,a,liste_rafraichir,liste_messages=choisir_session(ecran,resolution,liste_rafraichir,liste_messages)
        if a==0:
            session_continuer=True
            menu_session=creer_menu_session(resolution,session)
        else:
            temps_actuel=pygame.time.get_ticks()
    elif choix==4:
        sys.exit(0)

    if session_continuer:
        liste_rafraichir=[]
        fond=pygame.image.load("images/fond.bmp")
        ecran.blit(fond,(0,0))
        pygame.display.flip()



    while session_continuer: # MENU DU PERSONNAGE



        liste_rafraichir,choix,position_souris=obtenir_choix_menu_et_afficher_selection(menu_session,ecran,position_souris,liste_rafraichir)

        liste_messages,liste_rafraichir=afficher_messages(liste_messages,liste_rafraichir,resolution)
        rafraichir_image(liste_rafraichir,ecran)
        liste_rafraichir=[]
        temps_actuel=gerer_fps(temps_actuel)

        if choix==1 and not session.partie:
            liste_rafraichir=[]
            fond=pygame.image.load("images/fond.bmp")
            ecran.blit(fond,(0,0))
            pygame.display.flip()
            jeu_continuer=True
            joueur=reset_stats_joueur(joueur,session)
            joueur.attaques.autorisation=[]
            niveau=0
        elif choix==1 and session.partie:
            liste_rafraichir=[]
            fond=pygame.image.load("images/fond.bmp")
            ecran.blit(fond,(0,0))
            pygame.display.flip()
            jeu_continuer=True
            map=session.map
            map=charger_images_monstres(map)
            map=charger_images_objets(map)
            for i in range(map.nombre_de_salles):
                map=generer_images_salles(map,i)
            joueur=session.joueur
            joueur=charger_image_joueur(joueur)
            joueur.attaques.autorisation=[]
            joueur.temps_depuis_invincible=0
            joueur.attaques.temps_derniere_attaque=0
            joueur.attaques.entites=[]
            niveau=map.niveau
        elif choix==2:
            ecran.blit(fond,(0,0))
            pygame.display.flip()
            session,liste_rafraichir,liste_messages=choisir_competences(ecran,resolution,liste_rafraichir,liste_messages,session)
        elif choix==4:
            chaine="saves/"+session.nom+".txt"
            with open(chaine,"wb") as sauvegarde:
                pickler=pickle.Pickler(sauvegarde)
                pickler.dump(session)
            liste_rafraichir=[]
            fond=pygame.image.load("images/fond.bmp")
            ecran.blit(fond,(0,0))
            pygame.display.flip()
            session_continuer=False



        while jeu_continuer: # CREATION D'UN NOUVEAU NIVEAU


            if not session.partie:

                joueur.salle=-1
                niveau+=1
                map=generer_map(niveau)

            boucle_jeu_continuer=True



            while boucle_jeu_continuer: # CHARGEMENT DE LA NOUVELLE SALLE



                if not session.partie:

                    joueur=initialiser_joueur(map,joueur)
                    map=initialiser_salle(map,joueur)
                    map=generer_images_salles(map,joueur.salle)
                    minimap=charger_minimap(map,joueur)

                if session.partie:

                    map=session.map
                    joueur=session.joueur
                    minimap=charger_minimap(map,joueur)

                liste_rafraichir=[]
                joueur.attaques.entites=[]

                afficher_interface(position_ecran_x,position_ecran_y,ecran,joueur,session)
                ecran.blit(map.salles[joueur.salle].image,(position_ecran_x,position_ecran_y))
                ecran.blit(joueur.images.bas[0],(position_ecran_x+joueur.x,position_ecran_y+joueur.y))
                ecran.blit(minimap,(position_ecran_x+824,position_ecran_y+10))
                pygame.display.flip()

                tempo=0
                temps_actuel=pygame.time.get_ticks()
                salle_continuer=True

                session.partie=False



                while salle_continuer: # BOUCLE DU JEU

                    choix=0


                    rafraichir_image(liste_rafraichir,ecran)
                    liste_rafraichir=[]



                    for entree in pygame.event.get():

                        if entree.type==pygame.KEYDOWN:
                            if entree.key==raccourcis[0]:
                                choix,joueur=gerer_menu_jeu(ecran,position_souris,position_ecran_x,position_ecran_y,raccourcis,joueur)
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
                            if entree.key==raccourcis[5]:
                                if joueur.bombes>0:
                                    joueur.attaques.autorisation.append(2)
                                    rafraichir_bombes(position_ecran_x,position_ecran_y,joueur,liste_rafraichir,joueur.bombes-1)

                        if entree.type==pygame.MOUSEBUTTONDOWN:
                            if entree.button==1:
                                joueur.attaques.autorisation.append(1)

                        if entree.type==pygame.MOUSEBUTTONUP:
                            if entree.button==1:
                                joueur.attaques.autorisation.remove(1)

                        if entree.type==pygame.MOUSEMOTION:
                            joueur.attaques.position_souris=[entree.pos[0],entree.pos[1]]



                    tempo=gerer_tempo(tempo)

                    temps_actuel=gerer_fps(temps_actuel)



                    liste_rafraichir,blocs_a_proximite=deplacer_personnage(map,joueur,liste_rafraichir,tempo,position_ecran_x,position_ecran_y)

                    if joueur.deplacement_x!=0 or joueur.deplacement_y!=0:

                        for i in range(4):

                            if collisions(joueur.hitbox, map.salles[joueur.salle].blocs_hitboxs[blocs_a_proximite[i][1]][blocs_a_proximite[i][0]]):
                                if map.salles[joueur.salle].blocs_type[blocs_a_proximite[i][1]][blocs_a_proximite[i][0]]>=13 \
                                and map.salles[joueur.salle].blocs_type[blocs_a_proximite[i][1]][blocs_a_proximite[i][0]]<=17:
                                    salle_continuer=False

                                if map.salles[joueur.salle].blocs_type[blocs_a_proximite[i][1]][blocs_a_proximite[i][0]]==13:
                                    boucle_jeu_continuer=False


                        map,joueur,liste_rafraichir=ramasser_objets(map,joueur,liste_rafraichir,position_ecran_x,position_ecran_y)



                    map,liste_rafraichir,joueur=gerer_portes(map,joueur,liste_rafraichir,position_ecran_x,position_ecran_y)

                    liste_rafraichir=afficher_objets(map,liste_rafraichir,position_ecran_x,position_ecran_y,joueur)

                    joueur=creer_attaque(joueur,position_ecran_x,position_ecran_y,session)

                    joueur,map,liste_rafraichir=gerer_attaques(joueur,position_ecran_x,position_ecran_y,map,liste_rafraichir,session)

                    map,liste_rafraichir,joueur=deplacer_monstres(map,joueur,tempo,liste_rafraichir,position_ecran_x,position_ecran_y,session)

                    map,liste_rafraichir,session=gerer_mort_monstres(map,joueur,liste_rafraichir,position_ecran_x,position_ecran_y,session)

                    joueur=gerer_invincibilite(joueur)

                    liste_rafraichir,session=rafraichir_niveau_session(position_ecran_x,position_ecran_y,session,liste_rafraichir)

                    liste_rafraichir.append([map.salles[joueur.salle].image.subsurface((824,10,126,88)),(position_ecran_x+824,position_ecran_y+10,126,88),1])
                    liste_rafraichir.append([minimap,(position_ecran_x+824,position_ecran_y+10,126,88),5])

                    if session.competences[11]>0 and len(map.salles[joueur.salle].ennemis)>0 and tempo==3:
                        liste_rafraichir,joueur=rafraichir_mana(position_ecran_x,position_ecran_y,joueur,liste_rafraichir,session,joueur.mana+session.competences[11])

                    if joueur.points_de_vies<=0 and joueur.nombre_de_vies<=0:
                        salle_continuer=False
                        boucle_jeu_continuer=False
                        jeu_continuer=False
                        menu_session=creer_menu_session(resolution,session)
                        liste_rafraichir=[]
                        fond=pygame.image.load("images/fond.bmp")
                        ecran.blit(fond,(0,0))
                        pygame.display.flip()
                    elif joueur.points_de_vies<=0 and joueur.nombre_de_vies>0:
                        liste_rafraichir,joueur=rafraichir_nombre_de_vies(position_ecran_x,position_ecran_y,joueur,liste_rafraichir,joueur.nombre_de_vies-1)
                        liste_rafraichir,joueur=rafraichir_vie(position_ecran_x,position_ecran_y,joueur,liste_rafraichir,joueur.vie_maximum,joueur.vie_maximum)

                    if choix==1:
                        liste_rafraichir.append([map.salles[joueur.salle].image.subsurface((130,38,700,500)),(position_ecran_x+130,position_ecran_y+38,700,500),1])
                    if choix==2:
                        liste_rafraichir=[]
                        fond=pygame.image.load("images/fond.bmp")
                        ecran.blit(fond,(0,0))
                        pygame.display.flip()
                        salle_continuer=False
                        boucle_jeu_continuer=False
                        joueur=reset_stats_joueur(joueur,session)
                        joueur.attaques.autorisation=[]
                        niveau=0
                    if choix==3:
                        session.partie=True
                        session.map=map
                        session.joueur=joueur
                        salle_continuer=False
                        boucle_jeu_continuer=False
                        jeu_continuer=False
                        liste_rafraichir=[]
                        fond=pygame.image.load("images/fond.bmp")
                        ecran.blit(fond,(0,0))
                        pygame.display.flip()
                    if choix==4:
                        session.partie=True
                        session.map=map
                        session.joueur=joueur
                        chaine="saves/"+session.nom+".txt"
                        with open(chaine,"wb") as sauvegarde:
                            pickler=pickle.Pickler(sauvegarde)
                            pickler.dump(session)
                        sys.exit(0)