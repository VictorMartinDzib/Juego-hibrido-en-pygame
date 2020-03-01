import pygame
import os
import sys
from pygame.locals import *

pygame.init()
pygame.mixer.init()
ancho, alto = 1000, 600 #Dimensiones

ventana = pygame.display.set_mode((ancho, alto)) #Objeto surface
pygame.display.set_caption("Pygame")

#Eventos de tiempo
pygame.time.set_timer(USEREVENT+1, 500)
pygame.time.set_timer(USEREVENT+2, 3000)

#Creacion de fondo

fondo = pygame.image.load(os.path.join('images', 'city.png')).convert() #Cargando escenario
fondo = pygame.transform.scale(fondo, (ancho, alto))

fondoA = fondo.get_width()
fondoB = 0
velocidad = 60 #velocidad de repintado

reloj = pygame.time.Clock() #estableciendo reloj
pajaro = [pygame.image.load(os.path.join('images', 'z'+str(x) + '.png')) for x in range(1, 11)]
pajaro = [pygame.transform.scale(pajaro[i], (48, 56))for i in range(0, 10)] #redimensionando

#sonidos
jumpSound = pygame.mixer.Sound('sounds/jumps.wav')
roundSound = pygame.mixer.Sound('sounds/roundss.wav')
delizaSound = pygame.mixer.Sound('sounds/desliza.wav')

#####################################################################################
#CLASE JUGADOR
class jugador(object):

	personje = [pygame.image.load(os.path.join('images', 'z'+str(x) + '.png')) for x in range(1, 11)]
	personje = [pygame.transform.scale(pajaro[i], (88, 115))for i in range(0, 10)] #redimensionando
	saltitos = [1,1,1,1,1,1,2,2,2,2,2,2,2,2,2,2,2,2,3,3,3,3,3,3,3,3,3,3,3,3,4,4,4,4,4,4,4,4,4,4,4,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,-1,-1,-1,-1,-1,-1,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-3,-3,-3,-3,-3,-3,-3,-3,-3,-3,-3,-3,-4,-4,-4,-4,-4,-4,-4,-4,-4,-4,-4,-4]

	def __init__(self, x, y, ancho, alto):
		self.x = x
		self.y = y
		self.ancho = ancho
		self.alto = alto
		self.correr = False
		self.saltar = False
		self.deslizar = False
		self.morir = False
		self.super_speed = False
		self.contadorSaltos = 1
		self.correrCount = 1
		self.Y = self.y
		self.deslizarContador = 1

	def dibujar(self, ventana):

		if self.deslizar:
			#a la variable y se le asigna el arreglo de lista de saltos
			self.y += self.saltitos[self.deslizarContador] * 0.3 #se multiplica por el valor que define la altura
			#activamos el sonido
			jumpSound.play()
			#validamos el contador
			if self.deslizarContador >= 108:
				self.deslizarContador = 1
				self.deslizar = False
				self.correrCount = 0
				self.y = self.Y
				jumpSound.stop()
			
			#redibujamos el sprite
			ventana.blit(self.personje[7], (self.x, self.y))
			#incrementamos en 1#
			self.deslizarContador += 1
			
			self.hitbox = (self.x+4, self.y, self.ancho -14, self.alto-5)
			
		elif self.saltar: #Si saltar es verdadero entonces
			#a la variable y se le asigna el arreglo de lista de saltos
			self.y -= self.saltitos[self.contadorSaltos] * 1 #se multiplica por el valor que define la altura
			#activamos el sonido
			jumpSound.play()
			#validamos el contador
			if self.contadorSaltos >= 108:
				self.contadorSaltos = 1
				self.saltar = False
				self.correrCount = 0
				self.y = self.Y
				jumpSound.stop()
			
			#redibujamos el sprite
			ventana.blit(self.personje[1], (self.x, self.y))
			#incrementamos en 1#
			self.contadorSaltos += 1
			
			self.hitbox = (self.x+4, self.y, self.ancho -14, self.alto-5)
			
		elif self.morir:
			pass
		else:
			if self.correrCount >= 60:
				self.correrCount = 1
			ventana.blit(self.personje[self.correrCount//6], (self.x, self.y))
			self.correrCount += 1
			self.hitbox = (self.x+4, self.y, self.ancho -14, self.alto-7)
			#print(self.contadorSaltos//6)

#clase sonic
son = [pygame.image.load(os.path.join('images/sonic', 'sonic ('+str(x) + ').png')) for x in range(0, 76)]

class Sonic(jugador):
	sonic = [pygame.transform.scale(son[i], (88, 115))for i in range(11, 18)] #redimensionando
	sonic_salto = [pygame.transform.scale(son[56], (88, 115)),
	pygame.transform.scale(son[58], (88, 115))]#$[pygame.transform.scale(son[i], (48, 60))for i in range(11, 18)]
	sonic_desliza =  [pygame.transform.scale(son[65], (88, 115)),
	pygame.transform.scale(son[62], (88, 115)),
	pygame.transform.scale(son[63], (88, 115))]
	sonic_speed = [pygame.transform.scale(son[i], (88, 115))for i in range(27, 37)]
	sonic_rueda = [pygame.transform.scale(son[i], (88, 115))for i in range(37, 44)]
	time_run = 0
	saltitos = [1,1,1,1,1,1,2,2,2,2,2,2,2,2,2,2,2,2,3,3,3,3,3,3,3,3,3,3,3,3,4,4,4,4,4,4,4,4,4,4,4,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,-1,-1,-1,-1,-1,-1,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-3,-3,-3,-3,-3,-3,-3,-3,-3,-3,-3,-3,-4,-4,-4,-4,-4,-4,-4,-4,-4,-4,-4,-4]
	start_speed = False
	def dibujar(self, ventana):

		if self.deslizar:
			#a la variable y se le asigna el arreglo de lista de saltos
			self.y += self.saltitos[self.deslizarContador] * 0.15 #se multiplica por el valor que define la altura
			#activamos el sonido
			delizaSound.play()
			#validamos el contador
			if self.deslizarContador >= 108:
				self.deslizarContador = 1
				self.deslizar = False
				self.correrCount = 0
				self.y = self.Y
				delizaSound.stop()
			
			#redibujamos el sprite
			ventana.blit(self.sonic_desliza[self.deslizarContador//36], (self.x, self.y))
			#incrementamos en 1#
			self.deslizarContador += 1
			
			self.hitbox = (self.x+4, self.y, self.ancho -14, self.alto-5)
			
		elif self.saltar: #Si saltar es verdadero entonces
			#a la variable y se le asigna el arreglo de lista de saltos
			self.y -= self.saltitos[self.contadorSaltos] * 2 #se multiplica por el valor que define la altura
			#activamos el sonido

			if(self.contadorSaltos < 8):
				jumpSound.play()
			#validamos el contador
			if self.contadorSaltos >= 108:
				self.contadorSaltos = 1
				self.saltar = False
				self.correrCount = 0
				self.y = self.Y
				jumpSound.stop()
			
			#redibujamos el sprite
			if(self.contadorSaltos >= 27):
				ventana.blit(self.sonic_salto[1], (self.x, self.y))
			else:
				ventana.blit(self.sonic_salto[0], (self.x, self.y))
			#incrementamos en 1#
			self.contadorSaltos += 1
			print(self.contadorSaltos)
			self.hitbox = (self.x+4, self.y, self.ancho -14, self.alto-5)
			
		elif self.super_speed:
			roundSound.play()
			if self.correrCount >= 42:
				self.correrCount = 1
				self.time_run += 1
			ventana.blit(self.sonic_rueda[self.correrCount//6], (self.x, self.y))
			self.correrCount += 1
			self.hitbox = (self.x+4, self.y, self.ancho -14, self.alto-7)
			#print(self.contadorSaltos//6)
			if(self.time_run > 15):
				roundSound.stop()
				self.time_run = 0
				self.super_speed = False

		elif self.start_speed:
			if self.correrCount >= 60:
				self.correrCount = 1
				self.start_speed = False
				self.super_speed = True
			ventana.blit(self.sonic_speed[self.correrCount//6], (self.x, self.y))
			self.correrCount += 1
			self.hitbox = (self.x+4, self.y, self.ancho -14, self.alto-7)

		else:
			if self.correrCount >= 42:
				self.correrCount = 1
			ventana.blit(self.sonic[self.correrCount//6], (self.x, self.y))
			self.correrCount += 1
			self.hitbox = (self.x+4, self.y, self.ancho -14, self.alto-7)
			#print(self.contadorSaltos//6)

################################################################################################
def repintando(i): #funcion para repintar el escenario
	fuente = pygame.font.SysFont('comicsans', 40)
	texto = fuente.render('Puntos: ' + str(puntaje), 1, (255,255,255))
	ventana.blit(fondo, (fondoA, 0))  #primer escenario
	ventana.blit(fondo, (fondoB, 0)) #escenario siguiente
	ventana.blit(pajaro[i], (1,1)) 
	zelda.dibujar(ventana)
	ventana.blit(texto, (780, 10))
	sonic_player.dibujar(ventana)
 	#zelda2.dibujar(ventana)
    #zelda3.dibujar(ventana)
	pygame.display.update() 

################################################################################################
#Funcion para control de teclas

def teclado(teclas):
	if teclas[pygame.K_SPACE] or teclas[pygame.K_UP]:
		print("Saltando")
		if not sonic_player.saltar and not sonic_player.deslizar:
			sonic_player.saltar = True
       
	if teclas[pygame.K_DOWN]:
		if not sonic_player.deslizar and not sonic_player.saltar:
			sonic_player.deslizar = True
		print("Deslizando")

	if teclas[pygame.K_RIGHT]:
		if not sonic_player.super_speed and not sonic_player.deslizar:
			#velocidad = int(temp_vel + (temp_vel*0.7))
			sonic_player.start_speed = True
		print("Super speed activada..")

#Creando objeto jugador		
zelda = jugador(150, 400, 88, 115)
sonic_player = Sonic(300, 400, 88, 115)

i = 1
temp_vel = 0
puntaje = 0

while 1:

	repintando(i)
	fondoA -= 1.4  
	fondoB -= 1.4
	
	for evento in pygame.event.get(): #Recorriendo eventos en ejecucion
		if evento.type == pygame.QUIT: #Si coincide con quit, cerrar programa
			pygame.quit()
			sys.exit()
		if evento.type == USEREVENT+1:
			velocidad += 0.5
			
			

		####################################################################
		#programando teclado

		teclado(pygame.key.get_pressed()) #pasando parametro de tecla pulsada
	

	if fondoA < -fondo.get_width(): #si el fondoA ha pasado por toda la pantalla, reasignar ancho
		fondoA = fondo.get_width()
    
	if fondoB < -fondo.get_width(): #si el fondoB ha pasado por toda la pantalla, reasignar ancho
		fondoB = fondo.get_width()

	i = i + 1
	if i == 10:
		i = 1

	if(sonic_player.super_speed):
		reloj.tick(int(velocidad*20))
	else:
		reloj.tick(velocidad)

	print(velocidad)
	 #poniendo velocidad
	puntaje += 1
