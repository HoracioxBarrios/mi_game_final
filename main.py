import pygame
import sys
from configuracion import *
from personaje import *
from piso import *
from modo_dev import *
pygame.init()
# cambio
pygame.mixer.music.load('sounds\intro_dbz.mp3')
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.1)
def generar_pisos(path: str, tipo, y, inicio, fin):
    lista_pisos: list[Piso] = []
    for x in range(inicio, fin, 100):
        lista_pisos.append(Piso(path, x, y, tipo))
    return lista_pisos



screen = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Db Z")
relog = pygame.time.Clock()

fondo = pygame.image.load("location\game_background_1.png")
fondo = pygame.transform.scale(fondo, (ANCHO, ALTO))

color_blue = (0,0,255)
color_rojo = (255,0,0)
color_green = (0,255,0)
personaje = Personaje()

lista_piso: list[Piso] = generar_pisos("sprites/StoneBlock.png", 'plataforma', 500, 200, 400)

lista_piso2 = generar_pisos("sprites/StoneBlock.png", 'piso', 700, 0, ANCHO)
lista_piso.extend(lista_piso2)


while (True):

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_x:
                cambiar_modo()
        teclas = pygame.key.get_pressed()

        if(teclas[pygame.K_RIGHT]):
            if(teclas[pygame.K_SPACE]):
                personaje.actions('saltar')
            else:
                personaje.actions('caminar_r')
        elif(teclas[pygame.K_LEFT]):
            if(teclas[pygame.K_SPACE]):
                personaje.actions('saltar')
            else:
                personaje.actions('caminar_l')
        elif(teclas[pygame.K_SPACE]):
            personaje.actions('saltar')
        else:
            personaje.actions("quieto")
    personaje.updater(lista_piso)
    personaje.dibujar_componentes(screen, lista_piso)


    if get_modo():
        for piso in lista_piso:
            pygame.draw.rect(screen, color_blue, piso.rectangulo_principal, 3)
            pygame.draw.rect(screen, color_rojo, piso.colisiones_rectangulo_princial["lado_arriba"], 3)
            pygame.draw.rect(screen, color_rojo, piso.colisiones_rectangulo_princial["lado_abajo"], 3)
            pygame.draw.rect(screen, color_rojo, piso.colisiones_rectangulo_princial["lado_izquierda"], 3)
            pygame.draw.rect(screen, color_rojo, piso.colisiones_rectangulo_princial["lado_derecha"], 3)     

            pygame.draw.rect(screen, color_blue, personaje.rectangulo_principal, 3)
            pygame.draw.rect(screen, color_rojo, personaje.diccionario_rectangulo_colisiones["lado_arriba"], 3)
            pygame.draw.rect(screen, color_rojo, personaje.diccionario_rectangulo_colisiones["lado_abajo"], 3)
            pygame.draw.rect(screen, color_rojo, personaje.diccionario_rectangulo_colisiones["lado_izquierda"], 3)
            pygame.draw.rect(screen, color_rojo, personaje.diccionario_rectangulo_colisiones["lado_derecha"], 3) 

    pygame.display.flip()
    screen.blit(fondo, fondo.get_rect())

    delta_ms = relog.tick(FPS)
