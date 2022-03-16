import pygame
import glob

class Bullet(pygame.sprite.Sprite):
    
    def __init__(self, pos, y_limit, speed, img):
        super().__init__()
        
        # Bullet sprites
        path = '../graphics/bullet/' + img + '*.png'
        self.animation_sprites = [pygame.image.load(file).convert_alpha() for file in glob.glob(path)]
        self.current_sprite = 0
        self.image =  self.animation_sprites[self.current_sprite]
        self.size = self.image.get_size()
        # Position
        self.rect = self.image.get_rect(center = pos)
        self.y_limit = y_limit
        # If speed == 1, it means that it's an enemy bullet, than make it
        # a bit slower than the player's bullet
        self.speed = speed * 3 if speed == 1 else speed * 5
    
        
    def destroy_bullet(self):
        if self.rect.y <= 0 - self.size[1] or self.rect.y >= self.y_limit + self.size[1]:
            self.kill()
            
    def update(self):
        self.rect.y += self.speed
        self.destroy_bullet()
        # Animation
        self.current_sprite += 0.2
        if self.current_sprite >= len(self.animation_sprites):
            self.current_sprite = 0
        self.image = self.animation_sprites[int(self.current_sprite)]
        
        
        
        
        
        
        

        