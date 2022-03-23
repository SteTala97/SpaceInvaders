import pygame
import glob

class Explosion(pygame.sprite.Sprite):
    
    def __init__(self, pos, img):
        super().__init__()

        # Explosion sprites
        path = '../graphics/explosion/' + img + '/*.png'
        self.animation_sprites = [pygame.image.load(file).convert_alpha() for file in glob.glob(path)]
        self.current_sprite = 0
        self.image = self.animation_sprites[self.current_sprite]
        self.terminated = False
        # Position
        self.rect = self.image.get_rect(center = pos)

    def update(self):
        self.current_sprite += 0.2
        if self.current_sprite >= len(self.animation_sprites):
            self.terminated = True
            self.kill()
            return
        self.image = self.animation_sprites[int(self.current_sprite)]


