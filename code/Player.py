import pygame
import glob
from Bullet import Bullet

class Player(pygame.sprite.Sprite):

    def __init__(self, pos, right_limit):
        super().__init__()
         
        # Player sprites
        path = '../graphics/player/player1*.png'
        self.animation_sprites = [pygame.image.load(file).convert_alpha() for file in glob.glob(path)]
        self.current_sprite = 0
        self.image = self.animation_sprites[self.current_sprite]
        self.size = self.image.get_size()
        # Position
        self.rect = self.image.get_rect(midbottom = pos)
        self.right_limit = right_limit - self.size[0]
        # Player's bullets
        self.bullets = pygame.sprite.Group()
        self.ready = True
        self.bullet_time = 0
        self.bullet_timer = 900 # 1000
        # Player movement
        self.speed = 5
        # Player sound
        self.rocket_sound = pygame.mixer.Sound('../sound/player_rocket.wav')
        self.rocket_sound.set_volume(1)
        

    def recharge(self):
        if not self.ready:
            current_time = pygame.time.get_ticks()
            if current_time - self.bullet_time >= self.bullet_timer:
                self.ready = True
      
    
    def shoot_bullet(self):
        self.bullets.add(Bullet(self.rect.midtop, self.rect.y, -1, 'bullet1'))
    
    
    def get_keyboard_input(self):
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
            if self.rect.x < 0:
                self.rect.x = 0
                
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
            if self.rect.x >= self.right_limit:
                self.rect.x = self.right_limit

        if keys[pygame.K_UP] and self.ready:
            self.shoot_bullet()
            self.ready = False
            self.bullet_time = pygame.time.get_ticks()
            self.rocket_sound.play()
      
    
    def update(self):
        self.get_keyboard_input()
        self.recharge()
        self.bullets.update()
        self.current_sprite += 0.2
        if self.current_sprite >= len(self.animation_sprites):
            self.current_sprite = 0
        self.image = self.animation_sprites[int(self.current_sprite)]



        
