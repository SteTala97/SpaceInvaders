import pygame
import glob

class Enemy(pygame.sprite.Sprite):
    
    def __init__(self, x, y, img, reward):
        super().__init__()
        
        # Enemy sprites
        path = '../graphics/enemy/' + img + '*.png'
        self.name = img
        self.animation_sprites = [pygame.image.load(file).convert_alpha() for file in glob.glob(path)]
        self.current_sprite = 0
        self.image = self.animation_sprites[self.current_sprite]
        self.size = self.image.get_size()
        # Position
        self.rect = self.image.get_rect(topleft = (x, y))
        # Enemy speed
        self.speed = 1
        # Score reward when destroyed
        self.killing_reward = reward
    
    def update(self, direction):
        self.rect.x += direction * self.speed
        # Animation
        self.current_sprite += 0.1
        if self.current_sprite >= len(self.animation_sprites):
            self.current_sprite = 0
        self.image = self.animation_sprites[int(self.current_sprite)]
        
        

class SpecialEnemy(pygame.sprite.Sprite):
    
    def __init__(self, screen_width, direction):
        super().__init__()
        
        path = '../graphics/enemy/special_enemy1*.png'
        self.animation_sprites = [pygame.image.load(file).convert_alpha() for file in glob.glob(path)]
        self.current_sprite = 0
        self.image = self.animation_sprites[self.current_sprite]
        self.size = self.image.get_size()
        
        # Direction == 1 => the special enemy goes from left to right
        # Direction == -1 => the special enemy goes from right to left 
        self.direction = direction
        if direction == 1:
            x = -100
        else:
            x = screen_width + 100
        self.rect = self.image.get_rect(center = (x, self.size[1] / 2 + 5))
        self.x_limit = screen_width

        self.speed = 2


    def update(self):
        self.rect.x += self.speed * self.direction
        self.current_sprite += 0.1
        if self.current_sprite >= len(self.animation_sprites):
            self.current_sprite = 0
        self.image = self.animation_sprites[int(self.current_sprite)]        
        
    