# -*- coding:utf_8 -*

import pygame

VERSION = "0.2.1"


class Salle:

    def __init__(self):

        self.image = pygame.Surface((960, 576))
        self.blocs_type = []
        self.blocs_hitboxs = []
        self.x = 0
        self.y = 0
        self.type_salle = 0
        self.visited = False
        self.objets = list()
        self.objets_potentiels = list()
        self.ennemis = list()
        self.ennemis_potentiels = list()


class Map:

    def __init__(self, nombre_de_salles):

        self.niveau = 0
        self.salles = []
        self.nombre_de_salles = nombre_de_salles
        self.carte_map = []


class Ennemis:

    def __init__(self):

        self.x = 0
        self.y = 0
        self.type = 0
        self.attaque = 0
        self.points_de_vies = 0
        self.points_de_vies_maximum = 0
        self.images = Image()
        self.hitbox_deplacement = Hitbox()
        self.hitbox_degats = Hitbox()
        self.mort = False
        self.deplacement_x = 0
        self.deplacement_y = 0
        self.attaques = Attaque()
        self.minibarre = Minibarre()
        self.paralyse = False
        self.fin_paralyse = 0
        self.temps_dernier_poison = 0
        self.empoisonne = False
        self.fin_empoisonne = 0


class Objet:

    def __init__(self):

        self.x = 0
        self.y = 0
        self.type = 0
        self.image = pygame.Surface((64, 64))
        self.hitbox = Hitbox()


class Joueur:

    def __init__(self):

        self.x = 0
        self.y = 0
        self.hitbox = Hitbox()
        self.salle = 0
        self.images = Image()
        self.deplacement_x = 0
        self.deplacement_y = 0

        self.attaque = 0
        self.vitesse = 0
        self.vitesse_attaque = 0
        self.points_de_vies = 0
        self.vie_maximum = 0
        self.nombre_de_vies = 0
        self.mana = 0
        self.argent = 0
        self.cles = 0
        self.bombes = 0
        self.temps_invincibilite = 0

        self.invincible = False
        self.temps_depuis_invincible = 0

        self.attaques = Attaque()
        self.sorts_actifs = list()
        self.sorts = list()
        self.sorts_temps_activation = list()

        self.animation_tete = Animation()


class Image:

    def __init__(self):

        self.haut = []
        self.bas = []
        self.gauche = []
        self.droite = []


class Hitbox:

    def __init__(self):

        self.x = 0
        self.y = 0
        self.w = 0
        self.h = 0


class Entite_Attaque:

    def __init__(self):

        self.x = 0
        self.y = 0
        self.type = 0
        self.deplacement_x = 0
        self.deplacement_y = 0
        self.images = []
        self.w = 0
        self.h = 0
        self.detruit = False
        self.temps = 0


class Attaque:

    def __init__(self):

        self.temps_derniere_attaque = 0
        self.entites = []
        self.autorisation = []
        self.position_souris = []


class Menu:

    def __init__(self):

        self.options = []
        self.x = 0
        self.y = 0
        self.w = 0
        self.h = 0
        self.type = 0


class Options_Menu:

    def __init__(self):

        self.message = ""
        self.chaines = []
        self.images = []
        self.x = 0
        self.y = 0
        self.w = 0
        self.h = 0


class Session:

    def __init__(self):

        self.nom = ""
        self.competences = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.points_de_competences = 0
        self.sorts = [0, 0]
        self.points_de_sorts = 0
        self.niveau = 0
        self.xp = 0
        self.partie = False
        self.map = 0
        self.joueur = 0
        self.version = VERSION


class Message:

    def __init__(self):

        self.x = 0
        self.y = 0
        self.w = 0
        self.h = 0
        self.image = 0
        self.temps_creation = 0


class Minibarre:

    def __init__(self):

        self.x = 0
        self.y = 0
        self.w = 0
        self.h = 0
        self.image = 0


class Animation:

    def __init__(self):

        self.activee = False
        self.images = list()
        self.temps_restant = 0
        self.temps_total = 0
        self.x = 0
        self.y = 0
        self.w = 0
        self.h = 0