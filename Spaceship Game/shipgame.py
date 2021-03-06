"""Star Ship"""
"""The player controls a UFO at the bottom of the screen. They may move left and right
    using the left and right arrow keys and shoot using the space bar. Players must shoot
    the falling stars before it hits the player. If all stars are cleared, a new fleet will
    spawn at faster speed. If a player gets hit three times by the stars, the game is over.
    
    Usage in console: python shipgame.py"""

import sys
from time import sleep

import pygame

from ufo import UFO
from settings import Settings
from ammo import Ammo
from bubble import Bubble
from stats import Stats
from button import Button
from score import Scoreboard

class StarShip:
    """General class containing game assets and behaviour"""
    
    def __init__(self):
        """Initialize the game"""
        pygame.init()
        
        #Create game window and display game title in the top bar
        self.settings = Settings() #Get game settings
        self.screen = pygame.display.set_mode((self.settings.width, self.settings.height)) #Get game display
        self.stats = Stats(self)
        pygame.display.set_caption("Star Ship") #Top bar title
        
        #Button object
        self.start_button = Button(self, "Start")

        #UFO object
        self.ufo = UFO(self)

        #Ammo object
        self.ammos = pygame.sprite.Group()

        #Bubble object
        self.bubbles = pygame.sprite.Group()
        self.lots_of_bubbles()

        self.sb = Scoreboard(self)

    def lots_of_bubbles(self):
        """Generate a lot of bubbles"""
        bubble = Bubble(self)
        bubble_width, bubble_height =  bubble.rect.size
        space_x = self.settings.width - (2 * bubble_width)
        bubble_count = space_x // (2*bubble_width)

        #Height of available space that bubbles can fit on screen
        ufo_height = self.ufo.rect.height
        space_y = (self.settings.height - bubble_height - ufo_height)
        num_rows = space_y // (2*bubble_height)

        #Create a row of bubbles
        for row in range(num_rows):
            for num_of_bubbles in range(bubble_count):
                self.create_bubble(num_of_bubbles, row)

    def create_bubble(self, num_of_bubbles, row):
        """Create a bubble object"""
        #Create bubble imagine in current row
        bubble = Bubble(self)
        bubble_width, bubble_height = bubble.rect.size
        bubble.x = bubble_width + 2 * bubble_width * num_of_bubbles
        bubble.rect.x = bubble.x
        bubble.rect.y = bubble.rect.height + 2* bubble.rect.height * row
        self.bubbles.add(bubble)
        
    def update_bubbles(self):
        self.check_edges()
        self.bubbles.update()

        if pygame.sprite.spritecollideany(self.ufo, self.bubbles):
            self.hit()

    def check_edges(self):
        """"Check if bubbles reached the edge of the screen"""
        for bubble in self.bubbles.sprites():
            if bubble.check_edges():
                self.change_directions()
                break

    def check_bottom(self):
        """Check if bubbles reached the bottom of the screen"""
        screen_rect = self.screen.get_rect()
        for bubble in self.bubbles.sprites():
            if bubble.rect.bottom >= screen_rect.bottom:
                self.hit()
                break

    def change_directions(self):
        """Drop row position and change the horizontal movement"""
        for bubble in self.bubbles.sprites():
            bubble.rect.y += self.settings.drop_speed
        self.settings.direction *= -1

    def hit(self):
        """When ship gets hit by a bubble"""
        #Take away one life of ship
        if self.stats.remaining_tries >0:
            self.stats.remaining_tries -= 1
            self.sb.set_ships()

            self.bubbles.empty()
            self.ammos.empty()

            self.update_bubbles()
            self.ufo.center_ship()

            #Pause
            sleep(0.5)

        else:
            self.stats.active = False
    
    def check_button(self, pos):
        """Start new game when player clicks the start button"""
        clicked = self.start_button.rect.collidepoint(pos)
        if clicked and not self.stats.active:
            self.settings.init_dynamic_settings()
            self.stats.reset()
            self.bubbles.empty()
            self.ammos.empty()
            self.lots_of_bubbles()
            self.ufo.center_ship()

            #Play the game
            self.stats.active = True
            self.sb.set_score()
            self.sb.set_level()
            self.sb.set_ships()

    def events(self):
        """Check if the game is running or not"""
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    self._check_keydown(event)
                elif event.type == pygame.KEYUP:
                    self._check_keyup(event)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    self.check_button(pos)
                    
    def _check_keydown(self, event):
        """Check for keydown events"""
        if event.key == pygame.K_RIGHT:
            self.ufo.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ufo.moving_left = True
        elif event.key == pygame.K_SPACE:
            self.fire() #Fire a bullet
        elif event.key == pygame.K_q:
            sys.exit()
    
    def _check_keyup(self, event):
        """Check for keyup events"""
        if event.key == pygame.K_RIGHT:
            self.ufo.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ufo.moving_left = False         

    def fire(self):
        """Creates a bullet and adds to the group"""
        #Users may shoot 4 bullets in a fixed interval
        if len(self.ammos) < self.settings.ammo_limit:
            new_ammo = Ammo(self)
            self.ammos.add(new_ammo)
                    
    def bullet_update(self):
        """Function that will update all bullets on screen"""
        
        #Update positions
        self.ammos.update()

        #Clear bullets that have disappeared
        for ammo in self.ammos.copy():
            if ammo.rect.bottom <= 0:
                self.ammos.remove(ammo)

        #Check for object collisions
        collisions = pygame.sprite.groupcollide(self.ammos, self.bubbles, True, True)

        if collisions:
            for bubbles in collisions.values():
                self.stats.score += self.settings.points * len(bubbles)
            self.sb.create_score()
            self.sb.check_high_score()

        if not self.bubbles:
            self.ammos.empty()
            self.lots_of_bubbles()
            self.settings.speedup()
            self.stats.level += 1
            self.sb.set_level()

    def update(self):
        """Update and draw the current screen"""
        #Draw most current screen
        self.screen.fill(self.settings.bg_color) #Draw the background colour
        self.ufo.blitme()

        self.bubbles.draw(self.screen)
            
        #Show start button if game is in an inactive state
        if not self.stats.active:
            self.start_button.create_button()

        #Draw scoreboard on screen
        self.sb.display_score()

        #Draw bullet to screen
        for ammo in self.ammos.sprites():
            ammo.draw()

         #Display the current screen
        pygame.display.flip()
        
    def run_game(self):
        """Run the main game loop"""
        while True:
            self.events() #Check if the game is running

            if self.stats.active:
                self.ufo.update() #Update the position of the ufo based on key presses
                self.bullet_update()
                self.update_bubbles()
            
            self.update() #Update the screen
            
if __name__ == '__main__':
    #Run the game
    ss = StarShip()
    ss.run_game()
    
    #000332060