import pygame
import os
from random import randrange

pygame.display.init()
resolution=pygame.display.Info()
ecran=pygame.display.set_mode((resolution.current_w,resolution.current_h),pygame.FULLSCREEN | pygame.DOUBLEBUF | pygame.HWSURFACE )
salles=pygame.image.load("images/minimapgrand.bmp")
salles.set_colorkey((255,255,255))
nombre_de_cases_max=(resolution.current_w//124)*(resolution.current_h//84)-1

liste=[]
x=496
y=336
liste.append([x,y])

for i in range(randrange(nombre_de_cases_max)):

	continuer=True
	
	while continuer:
		x=randrange(resolution.current_w//124)*124
		y=randrange(resolution.current_h//84)*84
		
		for j in range(len(liste)):
			
			if ((x==liste[j][0] and y==liste[j][1]+84)
			or (x==liste[j][0] and y==liste[j][1]-84)
			or (x==liste[j][0]+124 and y==liste[j][1])
			or (x==liste[j][0]-124 and y==liste[j][1])):
				continuer=False
				liste.append([x,y])
				break

for i in range(len(liste)):
	
	a=randrange(12)

	if a<=7:
		ecran.blit(salles.subsurface((0,0,120,80)),(liste[i][0],liste[i][1]))
	elif a>7 and a <=9:
		ecran.blit(salles.subsurface((480,0,120,80)),(liste[i][0],liste[i][1]))
	elif a==10:
		ecran.blit(salles.subsurface((360,0,120,80)),(liste[i][0],liste[i][1]))
	elif a==11:
		ecran.blit(salles.subsurface((120,0,120,80)),(liste[i][0],liste[i][1]))
	pygame.display.flip()

while True:

    if pygame.event.poll().type==pygame.MOUSEBUTTONUP:
        break
