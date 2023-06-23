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
        self.sonido = AudioSegment.from_wav('sounds/correr.wav') 
        self.frame = 0
        self.gravedad = gravedad
        self.velocidad_caminar = velocidad_caminar
        self.potencia_salto = potencia_salto
        self.limite_altura_salto = 15
        ###########################
        self.pos_x = 0
        self.pos_y = 0
        self.desplazamiento_x = 0
        self.desplazamiento_y = 0 
        ############################
        self.puede_controlar_personaje = True
        self.esta_caminando = False
        self.mirando_derecha = True
        self.esta_en_aire = True
        ############################
        self.time_sound = 20
        #Creacion inicial del rectangulo con superficie
        self.animacion = self.quieto_r
        self.imagen = self.animacion[self.frame]#el frame inicia arranca en 0, por ende se renderiza la pocision 0 de la lista de animaciones
        self.rectangulo_principal = self.imagen.get_rect()
        self.rectangulo_principal.x = pos_init_x_personaje
        self.rectangulo_principal.y = pos_init_y_personaje
        self.diccionario_rectangulo_colisiones = obtener_rectangulos_colision(self.rectangulo_principal)


    def actions(self, accion: str):
        match(accion):
            case "caminar_r":
                self.caminar(accion)
            case "caminar_l":
                self.caminar(accion)
            case "quieto":
                 self.quieto()
            case "saltar":
                self.saltar()

    def caminar(self, accion: str):
        match (accion):
            case "caminar_r":
                if not self.esta_en_aire:
                    if(not self.mirando_derecha and not self.esta_caminando):
                        self.cambiar_animacion(self.quieto_r)
                    self.esta_caminando = True
                    self.mirando_derecha = True 
                    self.desplazamiento_x = self.velocidad_caminar
            case "caminar_l":
                if not self.esta_en_aire:
                    if(self.mirando_derecha and not self.esta_caminando):
                        self.cambiar_animacion(self.quieto_l)
                    self.esta_caminando = True
                    self.cambiar_animacion(self.corriendo_l)
                    self.mirando_derecha = not self.mirando_derecha
                    self.desplazamiento_x = -self.velocidad_caminar
    def quieto(self):
        self.esta_caminando = False
        sonido_pasos.stop()
        if self.mirando_derecha:
            self.cambiar_animacion(self.quieto_r)
        else:
            self.cambiar_animacion(self.quieto_l)
        self.desplazamiento_x = 0  

    def saltar(self):
        if not self.esta_en_aire:
            self.esta_en_aire = True
            sonido_salto.set_volume(0.1)
            sonido_salto.play()
            self.desplazamiento_y = self.potencia_salto
            if self.mirando_derecha:
                self.cambiar_animacion(self.saltando_r)
            else:
                self.cambiar_animacion(self.saltando_l)
            

    def dibujar_componentes(self, screen, lista_pisos: list[Piso]):
        '''
        dibuja en pantalla
        '''
        self.dibijar_personaje(screen)
        self.dibujar_plataforma(screen, lista_pisos)


    def updater(self, lista_pisos: list[Piso]):
        self.verificar_desplazamiento_rectangulo_x()
        self.verificar_desplazamiento_rectangulo_y()
        self.aplicar_gravedad(lista_pisos)
        self.verificar_fames()
        if(self.esta_caminando and self.time_sound <= 0 and not self.esta_en_aire):
            sonido_pasos.set_volume(0.2)
            sonido_pasos.play()
            self.time_sound = 10
        else:
            self.time_sound -= 1

        print(self.time_sound)

    def aplicar_gravedad(self, lista_pisos:list[Piso]):
        if(self.esta_en_aire):
            sonido_pasos.stop()
            if self.desplazamiento_y + gravedad < self.limite_altura_salto:
                self.desplazamiento_y += gravedad
            #Verificamos colision con los pisos
        self.verificar_colision(lista_pisos)
            

    def verificar_colision(self, lista_pisos:list[Piso]):
            # self.rectangulo_principal.bottom = piso.rectangulo_principal.top
            for piso in lista_pisos:       
                colisiono = self.diccionario_rectangulo_colisiones["lado_abajo"].colliderect(piso.colisiones_rectangulo_princial["lado_arriba"])
                if(colisiono):
                    self.diccionario_rectangulo_colisiones["lado_abajo"].top = self.diccionario_rectangulo_colisiones["main"].bottom
                    self.esta_en_aire = False
                    self.desplazamiento_y = 0
                    if(self.esta_caminando and self.mirando_derecha):
                        self.cambiar_animacion(self.corriendo_r)
                    elif(self.esta_caminando and not self.mirando_derecha):
                        self.cambiar_animacion(self.corriendo_l)
                    break
                else:
                    self.esta_en_aire = True
                
    
    def verificar_fames(self):
        if (self.frame < len(self.animacion) -1):
                self.frame += 1
        else:
            self.frame = 0

    def dibujar_plataforma(self, screen, lista_pisos: list[Piso]):
        for piso in lista_pisos:
            if(piso.tipo == "piso"):
                screen.blit(piso.imagen, piso.rectangulo_principal)
        for piso in lista_pisos:
            if(piso.tipo == "plataforma"):
                screen.blit(piso.imagen, piso.rectangulo_principal)

    def dibijar_personaje(self, screen):
        self.imagen = self.animacion[self.frame]
        screen.blit(self.imagen, self.rectangulo_principal)
    
    def cambiar_animacion(self, nueva_lista_animaciones: list[pygame.Rect]):
        self.animacion = nueva_lista_animaciones

    def verificar_desplazamiento_rectangulo_x(self):
        for lado in self.diccionario_rectangulo_colisiones:
            self.diccionario_rectangulo_colisiones[lado].x += self.desplazamiento_x
    def verificar_desplazamiento_rectangulo_y(self):
        for lado in self.diccionario_rectangulo_colisiones:
            self.diccionario_rectangulo_colisiones[lado].y += self.desplazamiento_y



 