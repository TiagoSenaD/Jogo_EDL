import pygame
from pygame.locals import *
from .personagem import Personagem
from display_utils.game_over import game_over


class Player(Personagem):
    def __init__(self, x, y, largura, altura, cor, vida=3):
        super().__init__(x, y, largura, altura, cor, vida)
        self.vidas_iniciais = vida
        self.moedas = 0 

        #Dano boss no player
        self.tempo_ultimo_dano = 0
        self.tempo_invencibilidade = 1000 #1000ms = 1s
        self.invecivel = False
        self.ultimo_pulo = 0
        self.status =0
        self.rect = pygame.Rect(x, y, largura, altura)

    def move(self, keys, stage,pres):
        dx, dy = 0, 0
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            dx = -1.0
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            dx = 1.0
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            dy = 1.0
        if(pres):
            if keys[pygame.K_w] or keys[pygame.K_UP]:
                # dy = -1.0
                if(self.pulando == False):
                    self.ultimo_pulo = self.y
                    self.pulando = True
                if(self.gravidade == False):
                    self.pular(self.ultimo_pulo)
        else:
            self.gravidade = True

        self.rect.x += dx
        if stage.checar_colisao(self.rect):
            self.rect.x -= dx

        self.rect.y += dy
        if stage.checar_colisao(self.rect):
            self.gravidade = False
            self.pulando = False
            self.pulo = 1
            self.rect.y -= dy+1

        self.x = self.rect.x
        self.y = self.rect.y

    def draw(self, scr):
        super().draw(scr)
        self.draw_life_bar(scr)

    def draw_life_bar(self, scr):
        for i in range(self.vida):
            pygame.draw.rect(scr, (255, 0, 0), (10 + i*35, 10, 30, 10))

    def reseta_invencibilidade(self):
        tempo_atual = pygame.time.get_ticks()
        if (tempo_atual - self.tempo_ultimo_dano > self.tempo_invencibilidade):
            self.invencivel = False

    def take_damage(self, amount):
        self.chapeu = 0
        if (self.invecivel == False):
            self.vida -= amount
            self.invencivel = True
        if (self.vida < 0):
            print("Game Over")
            pygame.quit()
            exit()

    def recuar(self,distancia,x_boss,y_boss):
        if(self.x < x_boss):
            self.x -= distancia
            self.rect.x -= distancia

        else:
            self.x += distancia
            self.rect.x += distancia

        if(self.y <= y_boss):
            self.y -= distancia
            self.rect.y -= distancia

    def pular(self,altura_ultimo_pulo):
        self.pulando = True
        if(altura_ultimo_pulo - self.y < self.limite_pulo):
            self.y -= 3
            self.rect.y -= 3
        else:
            self.gravidade = True
            self.pulando = True

