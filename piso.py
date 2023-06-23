import pygame
from utilidades import *
class Piso:
    def __init__(self, path, x, y, tipo) -> None:
        self.piso_superficie = get_surface_form_sprite_sheet(path, 1,1,0,0,1, False)
        self.pos_init_x = x
        self.pos_init_y = y
        self.frame = 0
        self.tipo = tipo
        self.animacion = self.piso_superficie
        self.imagen = self.animacion[self.frame]
        self.rectangulo_principal = self.imagen.get_rect()
        self.rectangulo_principal.x = x
        self.rectangulo_principal.y = y
        self.colisiones_rectangulo_princial = obtener_rectangulos_colision(self.rectangulo_principal)