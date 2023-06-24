import pygame
from utilidades import *
from animation import *
from configuracion import *
from piso import *
from pydub import AudioSegment
from pydub.playback import play
pygame.init()

sonido_pasos = pygame.mixer.Sound('sounds\Efectos DBz/correr.wav')
sonido_poder = pygame.mixer.Sound('sounds\Efectos DBz/poder.wav')
sonido_salto = pygame.mixer.Sound('sounds\Efectos DBz/salto.wav')

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
        self.velocidad_caminar = 10
        self.potencia_salto = 20
        self.limite_altura_salto = 10
        ###########################
        self.desplazamiento_x = 0
        self.desplazamiento_y = 0
        self.vel_y = 0 
        ############################
        self.esta_caminando = False
        self.orientacion_x = 1
        self.esta_en_aire = False
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
        self.rectangulo_principal.y = 650
        ################################
        self.diccionario_rectangulo_colisiones = obtener_rectangulos_colision(self.rectangulo_principal)

    def acciones(self, accion: str):

        match(accion):
            case "caminar_r":
                self.caminar(accion)
            case "caminar_l":
                self.caminar(accion)
            case "saltar":
                self.saltar()
            case "quieto":
                self.quieto()
    def caminar(self, accion):
        if(not self.esta_en_aire):
            if(accion == "caminar_r"):
                self.orientacion_x = 1
                self.cambiar_animacion(self.corriendo_r)
                self.desplazamiento_x = self.velocidad_caminar
                self.esta_caminando = True
            else:
                self.orientacion_x = -1
                self.cambiar_animacion(self.corriendo_l)
                self.desplazamiento_x = -self.velocidad_caminar
                self.esta_caminando = True
            
    def controlar_sonido_caminar(self):
        if(self.esta_caminando and self.time_sound <= 0 and not self.esta_en_aire):
                sonido_pasos.set_volume(0.2)
                sonido_pasos.play()
                self.time_sound = 7
        else:
            self.time_sound -= 1
            
    def saltar(self):
        if(not self.esta_en_aire):
            self.esta_en_aire = True
            sonido_salto.set_volume(0.1)
            sonido_salto.play()
            if(self.orientacion_x == 1):
                self.vel_y = -self.potencia_salto
                self.cambiar_animacion(self.saltando_r)
            else:
                self.vel_y  = -self.potencia_salto
                self.cambiar_animacion(self.saltando_l)


    def quieto(self):
        if(not self.esta_en_aire):
            self.esta_caminando = False
            if(self.orientacion_x == 1):
                self.desplazamiento_x = 0
                self.cambiar_animacion(self.quieto_r)
            elif(self.orientacion_x == -1):
                self.desplazamiento_x = 0
                self.cambiar_animacion(self.quieto_l)
            

    def updater(self, screen_height, pisos, screen):
        self.controlar_sonido_caminar()
        self.dx = self.desplazamiento_x
        self.dy = 0
        self.verificar_frames()
        ###################
        self.vel_y += 1
        ###################
        if self.vel_y > 10:
            self.vel_y = 10
        ###################
        self.dy += self.vel_y
        # print('vel_y',self.vel_y)
        # print('dy',dy)
        # print(self.dy)
        # print(self.esta_en_aire)

        if(self.dy > 1):
            self.esta_en_aire = True
            if(self.orientacion_x == 1):
                self.cambiar_animacion(self.saltando_r)
            else:
                self.cambiar_animacion(self.saltando_l)
        
        
        ########################
        for piso in pisos:
            if piso[1].colliderect(self.rectangulo_principal.x + self.dx, self.rectangulo_principal.y, self.ancho_imagen, self.alto_imagen):
                self.dx = 0

            if piso[1].colliderect(self.rectangulo_principal.x, self.rectangulo_principal.y + self.dy, self.ancho_imagen, self.alto_imagen):
                # Check if below the ground (jumping)
                if self.vel_y < 0:
                    self.dy = piso[1].bottom - self.rectangulo_principal.top
                    self.vel_y = 0
                # Check if above the ground (falling)
                elif self.vel_y >= 0:
                    self.dy = piso[1].top - self.rectangulo_principal.bottom
                    self.vel_y = 0
                    self.esta_en_aire = False
                    
        
                        


                
        ########################
        self.rectangulo_principal.y += self.dy
        self.rectangulo_principal.x += self.dx

        if self.rectangulo_principal.bottom > screen_height:
            self.rectangulo_principal.bottom = screen_height
            self.dy = 0

        self.dibujar_en_pantalla(screen)
        
        
       #rompia:  index fuera de rango
    # def dibujar_en_pantalla(self, screen):
    #     self.imagen = self.animacion[self.frame]
    #     screen.blit(self.imagen, self.rectangulo_principal)

    def dibujar_en_pantalla(self, screen):
        if self.frame >= len(self.animacion):
            self.frame = 0
        self.imagen = self.animacion[self.frame]
        screen.blit(self.imagen, self.rectangulo_principal)
    
        
        
        
    def verificar_frames(self):
        if (self.frame < len(self.animacion) -1):
            self.frame += 1
        else:
            self.frame = 0
    def cambiar_animacion(self, nueva_lista_animaciones: list[pygame.Rect]):
        self.animacion = nueva_lista_animaciones

        