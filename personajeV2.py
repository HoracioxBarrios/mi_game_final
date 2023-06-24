import pygame
from utilidades import *
from animation import *
from configuracion import *
from piso import *
from pydub import AudioSegment
from pydub.playback import play
pygame.init()

sonido_pasos = pygame.mixer.Sound('sounds/correr.wav')
sonido_poder = pygame.mixer.Sound('sounds/poder.wav')
sonido_salto = pygame.mixer.Sound('sounds/salto.wav')

class Personaje:
    def __init__(self) -> None:
        self.quieto_r = get_surface_form_sprite_sheet("sprites\goku2.png", 9, 6, 0, 0, 2, True)
        self.quieto_l = get_surface_form_sprite_sheet("sprites\goku2.png", 9, 6, 0, 0, 2, False)
        self.corriendo_r = get_surface_form_sprite_sheet("sprites\goku2.png", 9, 6, 0, 6, 8, False)
        self.corriendo_l = get_surface_form_sprite_sheet("sprites\goku2.png", 9, 6, 0, 6, 8, True)
        self.saltando_r = get_surface_form_sprite_sheet("sprites\goku2.png", 9, 6, 0, 6, 7, False)
        self.saltando_l = get_surface_form_sprite_sheet("sprites\goku2.png", 9, 6, 0, 6, 7, True)
        self.frame = 0
        self.gravedad = 1
        self.velocidad_caminar = 6
        self.potencia_salto = 10
        self.limite_altura_salto = 10
        ###########################
        self.desplazamiento_x = 0
        self.desplazamiento_y = 0
        self.vel_y = 0 
        ############################
        self.esta_caminando = False
        self.orientacion_x = 1
        self.esta_en_aire = True
        self.dx = 0
        self.dy = 0
        ############################
        self.time_sound = 20
        #Creacion inicial del rectangulo con superficie
        self.animacion = self.quieto_r
        self.imagen = self.animacion[self.frame]#el frame inicia arranca en 0, por ende se renderiza la pocision 0 de la lista de animaciones
        self.ancho_imagen = self.imagen.get_width()
        self.alto_imagen = self.imagen.get_height()
        self.rectangulo_principal = self.imagen.get_rect()
        ################################
        self.pos_x = 0
        self.pos_y = 0
        self.rectangulo_principal.x = 50
        self.rectangulo_principal.y = 0
        ################################
        self.diccionario_rectangulo_colisiones = obtener_rectangulos_colision(self.rectangulo_principal)

    def acciones(self, accion: str):

        match(accion):
            case "caminar_r":
                self.caminar(accion)
            case "caminar_l":
                self.caminar(accion)
            case "saltar":
                self.saltar(accion)
            case "quieto":
                self.quieto()
    def caminar(self, accion):
        print(accion)
        if(not self.esta_en_aire):
            if(accion == "caminar_r"):
                self.orientacion_x = 1
                self.desplazamiento_x = 5
            else:
                self.orientacion_x = -1
                self.desplazamiento_x = -5
    def saltar(self, accion):
        print(accion)
        if(not self.esta_en_aire):
            self.esta_en_aire = True
            if(self.orientacion_x == 1):
                self.desplazamiento_y = -10
            else:
                self.desplazamiento_y = -10

    def quieto(self):
        if(not self.esta_en_aire):
            if(self.orientacion_x == 1):
                self.desplazamiento_x = 0
            else:
                self.desplazamiento_x = 0
    def updater(self, screen_height, pisos, screen):
        self.dx = self.desplazamiento_x
        self.dy = self.desplazamiento_y
        ###################
        self.vel_y += 1
        print(self.vel_y)
        ###################
        if self.vel_y > 10:
            self.vel_y = 10
        ###################
        self.dy += self.vel_y
        # print('vel_y',self.vel_y)
        # print('dy',dy)
        ########################
        for piso in pisos:
            if piso[1].colliderect(self.rectangulo_principal.x + self.dx, self.rectangulo_principal.y, self.ancho_imagen, self.alto_imagen):
                self.dx = 0
            if piso[1].colliderect(self.rectangulo_principal.x, self.rectangulo_principal.y + self.dy, self.ancho_imagen, self.alto_imagen):

            # check if below the ground i.e. jumping
                if self.vel_y < 0:
                    self.dy = piso[1].bottom - self.rectangulo_principal.top
                    self.vel_y = 0
                #check if above the ground i.e. falling
                if self.vel_y >= 0:
                    self.dy = piso[1].top - self.rectangulo_principal.bottom
                    self.vel_y = 0
                    self.esta_en_aire = False
        print(self.esta_en_aire)




        ########################
        self.rectangulo_principal.y += self.dy
        self.rectangulo_principal.x += self.dx

        if self.rectangulo_principal.bottom > screen_height:
            self.rectangulo_principal.bottom = screen_height
            self.dy = 0

        self.dibujar_en_pantalla(screen)
    def dibujar_en_pantalla(self, screen):
        self.imagen = self.animacion[self.frame]
        screen.blit(self.imagen, self.rectangulo_principal)

        
    def verificar_frames(self):
        if (self.frame < len(self.animacion) -1):
            self.frame += 1
        else:
            self.frame = 0

        