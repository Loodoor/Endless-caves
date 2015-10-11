# -*- coding:utf_8 -*

import pygame
import time

surface = pygame.image.load("joueur.bmp")
surface_finale = pygame.Surface((surface.get_size()[0]*2, surface.get_size()[1]*2))
for i in range(surface_finale.get_size()[1]):
    for j in range(surface_finale.get_size()[0]):
        surface_finale.blit(surface.subsurface((j//2, i//2, 1, 1)), (j, i))

pygame.image.save(surface_finale, str(int(time.time()))+".bmp")
