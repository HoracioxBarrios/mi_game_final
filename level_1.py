import pygame, sys
from pygame.locals import *
from personajeV2 import *
from creador_mundo import *
pygame.init()

WHITE = (255,255,255)



WIDTH = 1000
HEIGTH = 700
screen = pygame.display.set_mode((WIDTH, HEIGTH))
pygame.display.set_caption("Dragon ball")

#-------------------------------- Mundo
#grid
tile_size = 50
margin = 0 # sin margen inferior
relog = pygame.time.Clock()
#fondo
bg_fondo = pygame.image.load("location\game_background_1.png")
bg_fondo = pygame.transform.scale(bg_fondo, (WIDTH, HEIGTH))


world_data = leerJson('stages.json')
stage = world_data["stages"][0]["stage_1"]
print(stage)

path_music_world = world_data["stages"][0]["musica_path"] 
world = World(stage, tile_size, 'sprites\StoneBlock.png', screen, path_music_world)

#-------------------------------- Personaje
personaje = Personaje()
world.play_music(0.2, -1)

while True:
    
    screen.blit(bg_fondo, (0, 0))
    tile_list = world.draw()
    
    dibujar_grid(screen, WHITE, tile_size, WIDTH, HEIGTH, 0)
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    key = pygame.key.get_pressed()
    
    if key[pygame.K_SPACE]:
       personaje.acciones('saltar')
    if key[pygame.K_LEFT]:
        personaje.acciones('caminar_l')
    if key[pygame.K_RIGHT]:
        personaje.acciones('caminar_r')
    if key[pygame.K_LEFT] == False and key[pygame.K_RIGHT] == False:
        personaje.acciones('quieto')
             
    personaje.updater(HEIGTH, tile_list, screen)
    personaje.dibujar_en_pantalla(screen)
        	
    pygame.display.update()

    delta_ms = relog.tick(FPS)
