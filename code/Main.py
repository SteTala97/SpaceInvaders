import pygame
from Player import Player
from Enemy import Enemy, SpecialEnemy
from Bullet import Bullet
from Explosion import Explosion
from random import choice, randint
import sys


class Game:

    def __init__(self):
        
        pygame.init()
        
        self.score = 0
        self.game_over = False
        self.play_again = False
        
        # Screen setup
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.backbround = pygame.image.load('../graphics/background/bg_earth_moon2.png').convert_alpha()
        
        # Icon and window caption
        pygame.display.set_caption("Space Invaders")
        try:
            self.icon = pygame.image.load('../graphics/icon/icon.png')
            pygame.display.set_icon(self.icon)
        except:
            print("\n -Icon image loading failed! Setting the default one-")
            
        # Fonts used for score and messages to the player
        self.font_score = pygame.font.Font('../graphics/fonts/font1.otf', 20)
        self.font_gameover_msg = pygame.font.Font('../graphics/fonts/font1.otf', 60)
        self.font_play_again_msg = pygame.font.Font('../graphics/fonts/font1.otf', 25)
        self.font_quit_msg = pygame.font.Font('../graphics/fonts/font1.otf', 35)
        self.pause_message_font = pygame.font.Font('../graphics/fonts/font1.otf', 75)
        self.pause_key_msg_font = pygame.font.Font('../graphics/fonts/font1.otf', 30)
        
        # Player setup
        player_sprite = Player((WIDTH / 2, HEIGHT - 3), WIDTH)
        self.player = pygame.sprite.GroupSingle(player_sprite)
        
        # Enemy setup
        self.enemies = pygame.sprite.Group()
        self.offset_x = 50 # distance along x-axis
        self.offset_y = 50 # distance along y-axis
        self.load_enemies(rows = 3, cols = 10)
        self.enemy_bullets = pygame.sprite.Group()
        self.enemy_direction = 1
        self.enemy_update_x_timer = 10 # Used to prevent bug with 'move_enemy_down()'
        
        # Special enemy setup
        self.special = pygame.sprite.GroupSingle()
        self.spawn_time_min = 300
        self.spawn_time_max = 600
        self.spawn_time = randint(self.spawn_time_min, self.spawn_time_max)
       
        # Sound effects
        self.main_theme = pygame.mixer.Sound('../sound/main_soundtrack.wav')
        self.main_theme.set_volume(2.0)
        self.main_theme.play(loops = -1) 
        self.enemy_rocket_sound = pygame.mixer.Sound('../sound/enemy_rocket.wav')
        self.enemy_rocket_sound.set_volume(0.3)
        self.enemy_destroyed_sound = pygame.mixer.Sound('../sound/enemy_explosion.wav')
        self.enemy_destroyed_sound.set_volume(0.5)
        self.special_enemy_sound = pygame.mixer.Sound('../sound/special_enemy.wav')
        self.special_enemy_sound.set_volume(0.75)
        self.special_enemy_destroyed_sound = pygame.mixer.Sound('../sound/special_enemy_destroyed.wav')
        self.special_enemy_destroyed_sound.set_volume(1.5)
        self.gameover_sound = pygame.mixer.Sound('../sound/game_over.wav')
        self.gameover_sound.set_volume(2.0)
        self.quit_game_sound = pygame.mixer.Sound('../sound/quit_game.wav')
        self.quit_game_sound.set_volume(2.0)
        self.victory_sound = pygame.mixer.Sound('../sound/medieval.wav')
        self.victory_sound.set_volume(2.0)
        self.pause_sound = pygame.mixer.Sound('../sound/pause.wav')
        self.pause_sound.set_volume(2.0)

        # Explosions
        self.explosions = pygame.sprite.Group()
    
    
    def load_enemies(self, rows, cols):
        y = 40
        for i in range(rows):
            x = 10
            for j in range(cols):
                if i == 0:
                    img_name = 'enemy3'
                    reward = 200
                elif i == 1:
                    img_name = 'enemy2'
                    reward = 150
                else:
                    img_name = 'enemy1'
                    reward = 100
                    
                self.enemies.add(Enemy(x, y, img_name, reward))
                x += self.offset_x
            y += self.offset_y
            
            
    def special_enemy_spawn(self):
        self.spawn_time -= 1
        if self.spawn_time <= 0:
            self.special.add(SpecialEnemy(WIDTH, choice([1, -1])))
            self.special_enemy_sound.play(loops = -1) 
            self.spawn_time = 10000 # so it does not spawn before it dies/disappear
            
            
    def enemy_fire(self):
        if self.enemies.sprites():
            random_enemy = choice(self.enemies.sprites())
            bullet_img = random_enemy.name + '_bullet'
            bullet_sprite = Bullet(random_enemy.rect.midbottom, WIDTH, 1, bullet_img)
            self.enemy_bullets.add(bullet_sprite)
            self.enemy_rocket_sound.play()
            
    
    def check_enemy_position(self):
        enemies = self.enemies.sprites()
        self.enemy_update_x_timer -= 1
        for enemy in enemies:
            if (enemy.rect.right >= WIDTH or enemy.rect.left <= 0) and self.enemy_update_x_timer <= 0:
                self.enemy_update_x_timer = 10
                self.move_enemy_down()
                self.enemy_direction *= -1
                # TODO: add positively incremental speed
                
    
    def check_special_enemy_position(self):
        if self.special.sprites():
            if self.special.sprite.rect.center[0] < -120 or self.special.sprite.rect.center[0] > WIDTH + 120:
                self.special_enemy_sound.stop()
                self.spawn_time = randint(self.spawn_time_min, self.spawn_time_max)
                
                
    def move_enemy_down(self):
        if self.enemies:
            for enemy in self.enemies.sprites():
                enemy.rect.y += 16
    
    
    def check_for_collisions(self):
        # Player's bullets
        if self.player.sprite.bullets:
            for bullet in self.player.sprite.bullets:

                # Player hit an enemy
                enemy_hit = pygame.sprite.spritecollide(bullet, self.enemies, True)
                if enemy_hit:
                    for enemy in enemy_hit:
                        self.score += enemy.killing_reward
                        self.explosions.add(Explosion(bullet.rect.center, enemy.name))
                    bullet.kill()
                    self.enemy_destroyed_sound.play()

                # Player hit a special enemy
                elif pygame.sprite.spritecollide(bullet, self.special, True):
                    self.score += 500
                    self.explosions.add(Explosion(bullet.rect.midtop, "special"))
                    bullet.kill()
                    self.special_enemy_destroyed_sound.play()
                    self.special_enemy_sound.stop()
                    self.spawn_time = randint(self.spawn_time_min, self.spawn_time_max)

                # Player hit an enemy bullet
                elif self.enemy_bullets:
                    bullet_hit = pygame.sprite.spritecollide(bullet, self.enemy_bullets, True)
                    if bullet_hit:
                        self.explosions.add(Explosion(bullet.rect.midtop, "bullet"))
                        bullet.kill()
                        # TODO: PUT SOUND HERE <---
                
        # Enemy's bullets
        if self.enemy_bullets:
            for bullet in self.enemy_bullets:
                # Enemy hit the player
                if pygame.sprite.spritecollide(bullet, self.player, False):
                    bullet.kill()
                    self.game_over_menu(2)
        
        # Enemy
        if self.enemies:
            for enemy in self.enemies:
                # Enemy reached the player
                if pygame.sprite.spritecollide(enemy, self.player, False) or enemy.rect.y >= HEIGHT:
                    self.game_over_menu(3)


    def update_explosions(self):
        if self.explosions:
            for explosion in self.explosions:
                explosion.update()
                if explosion.terminated:
                    self.explosions.remove(explosion)
                    
    
    def display_score(self):
        rendered_score = self.font_score.render(f'Score : {self.score}', False, 'white')
        score_rect = rendered_score.get_rect(topleft = (5, 5))
        screen.blit(rendered_score, score_rect)
         
        
    def check_enemy_left(self):
        if not self.enemies.sprites():
            self.game_over_menu(1)
            
    
    def display_winning_message(self):
        win_message = self.font_gameover_msg.render('YOU WON, EARTH IS SAVED!', False, 'white')
        win_rect = win_message.get_rect(center = (WIDTH / 2, HEIGHT / 3 + 30))
        win_msg_bg = pygame.Surface(win_message.get_size())
        win_msg_bg.fill((25, 25, 25))
        win_msg_bg.blit(win_message, (0, 0))
        screen.blit(win_msg_bg, win_rect)
        
        
    def display_defeat_message1(self):
        defeat_message = self.font_gameover_msg.render('Oh shit man, they got you!', False, 'white')
        defeat_rect = defeat_message.get_rect(center = (WIDTH / 2, HEIGHT / 3 + 30))
        defeat_msg_bg = pygame.Surface(defeat_message.get_size())
        defeat_msg_bg.fill((25, 25, 25))
        defeat_msg_bg.blit(defeat_message, (0, 0))
        screen.blit(defeat_msg_bg, defeat_rect)
        
        
    def display_defeat_message2(self):
        defeat_message = self.font_gameover_msg.render("Too late man, get the hell out!", False, 'white')
        defeat_rect = defeat_message.get_rect(center = (WIDTH / 2, HEIGHT / 3 + 30))
        defeat_msg_bg = pygame.Surface(defeat_message.get_size())
        defeat_msg_bg.fill((25, 25, 25))
        defeat_msg_bg.blit(defeat_message, (0, 0))
        screen.blit(defeat_msg_bg, defeat_rect)
            
    
    def display_play_again_message(self):
        playagain_msg = self.font_play_again_msg.render('Press ENTER to play again or ESC to quit',
                                                        False, 'white')
        playagain_rect = playagain_msg.get_rect(center = (WIDTH / 2, HEIGHT / 2))
        playagain_msg_bg = pygame.Surface(playagain_msg.get_size())
        playagain_msg_bg.fill((25, 25, 25))
        playagain_msg_bg.blit(playagain_msg, (0, 0))
        screen.blit(playagain_msg_bg, playagain_rect)
        
        
    def display_quitting_message(self):
        quit_msg = self.font_quit_msg.render('Are you sure? ENTER to play again or ESC to quit',
                                             False, 'white')
        quit_rect = quit_msg.get_rect(center = (WIDTH / 2, HEIGHT / 2))
        quit_msg_bg = pygame.Surface(quit_msg.get_size())
        quit_msg_bg.fill((25, 25, 25))
        quit_msg_bg.blit(quit_msg, (0, 0))
        screen.blit(quit_msg_bg, quit_rect)
     
        
    def pause(self):
        pygame.mixer.pause()
        self.pause_sound.play()
        
        # Pause message
        pause_msg = 'PAUSED'
        pause_msg = self.pause_message_font.render(pause_msg, True, 'white')
        pause_msg_rect = pause_msg.get_rect(midbottom = (WIDTH / 2, HEIGHT / 2 - 10))
        
        # Keyboard command message
        pause_key_msg = 'press SPACE to continue'
        pause_key_msg = self.pause_key_msg_font.render(pause_key_msg, True, 'white')
        pause_key_msg_rect = pause_key_msg.get_rect(center = (WIDTH / 2, HEIGHT / 2))

        # Add transparent background behind text
        pause_msg_bg1 = pygame.Surface(pause_msg.get_size())
        pause_msg_bg1.fill((25, 25, 25))
        pause_msg_bg1.blit(pause_msg, (0, 0))
        pause_msg_bg2 = pygame.Surface(pause_key_msg.get_size())            
        pause_msg_bg2.fill((25, 25, 25))
        pause_msg_bg2.blit(pause_key_msg, (0, 0))
        
        # Draw and update screen
        screen.blit(pause_msg_bg1, pause_msg_rect)
        screen.blit(pause_msg_bg2, pause_key_msg_rect)
        pygame.display.flip()
        
        # Hold on until a valid keyboard input is given
        paused = True
        while paused:
            # Event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    paused = False
                    pygame.quit()
                    sys.exit()
                    break
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        paused = False
                    elif event.key == pygame.K_ESCAPE:
                        paused = False
                        pygame.quit()
                        sys.exit()
                        
        pygame.mixer.unpause()
        
        
    def game_over_menu(self, flag):
        pygame.mixer.stop()
        
        # flag == 0 : the player wants to quit the game
        # flag == 1 : the player won the game
        # flag == 2 : the player got hit by the enemy, he's dead
        # flag == 3 : the player got reached by the enemy, he lost
        if flag == 0:
            self.quit_game_sound.play()
            self.display_quitting_message()
        else:
            if flag == 1:
                self.victory_sound.play()
                self.display_winning_message()
            else:
                self.gameover_sound.play()
                if flag == 2:
                    self.display_defeat_message1()
                if flag == 3:
                    self.display_defeat_message2()
            self.display_play_again_message()
            
        pygame.display.flip()
        # Hold on until a valid keyboard input is given
        paused = True
        while paused:
            # Event loop 
            for event in pygame.event.get():
                etype = event.type
                if etype == pygame.QUIT or etype == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.play_again = False
                    self.game_over = True
                    paused = False
                elif etype == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    self.play_again = True 
                    paused = False
        
        
    def run(self):
        # Update
        self.player.update()
        self.enemy_bullets.update()
        self.enemies.update(self.enemy_direction)
        self.check_enemy_position()
        self.special_enemy_spawn()
        self.check_special_enemy_position()
        self.special.update()
        self.check_for_collisions()
        self.update_explosions()
        # Draw
        self.display_score()
        self.player.sprite.bullets.draw(screen)
        self.player.draw(screen)
        self.enemies.draw(screen)
        self.special.draw(screen)
        self.enemy_bullets.draw(screen)
        self.explosions.draw(screen)
        self.check_enemy_left()
        
            
        
def main():
    pygame.init()
    
    global screen
    global HEIGHT
    global WIDTH
    
    HEIGHT, WIDTH = (600, 900)
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    
    clock = pygame.time.Clock()
    
    game = Game()
    
    ENEMY_FIRE = pygame.USEREVENT + 1
    pygame.time.set_timer(ENEMY_FIRE, 1000)
    
    while not game.game_over:
        if game.play_again:
            pygame.mixer.stop()
            game = Game()
            
        for event in pygame.event.get():
            etype = event.type
            if etype == pygame.QUIT or etype == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                game.game_over_menu(0)
            if etype == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game.pause()
            if event.type == ENEMY_FIRE:
                game.enemy_fire()
        
        # Frame rate set to 60fps
        clock.tick(60)
        #print("clock =", clock)
        
        # Draw background
        screen.blit(game.backbround, (0,0))
        
        # Run the game and update the display
        game.run()
        pygame.display.flip()
        
    
    pygame.mixer.stop()
    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()

