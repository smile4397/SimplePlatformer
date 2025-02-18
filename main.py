import pygame #For most of the game
import random #Almost unused, used for the enemy shooting.
import pickle #File handling.
import RandomLevelMaker #To make random level

'''
CREDITS:
Level_01 - (@MamaNeZakon) - https://mamanezakon.itch.io/forest-tileset
Level_02 - David Marah (@aethrall) - https://aethrall.itch.io/demon-woods-parallax-background
Level_03 - Luis Zuno (@ansimuz) - https://ansimuz.itch.io/cyberpunk-street-environment
Music - Alexandr Zhelanov - https://opengameart.org/content/heroic-minority
grunt effect - https://www.noiseforfun.com/2012-sound-effects/dusty-hit/
throw effect - https://www.noiseforfun.com/2014-sound-effects/throw-05/
'''

# CONSTANTS
# Colours
    #Primary colours
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)    
GREEN = (0, 255, 0)
RED =   (255, 0, 0)
BLUE =  (0, 0, 255)
    #Secondary colours
CYAN = (0,255,255)
MAGENTA = (255,0,255)
YELLOW = (255,255,0)
# Screen dimensions
SCREEN_WIDTH    = 800
SCREEN_HEIGHT   = 600

#IMAGE RELATED STUFF
player_images = "pixil-frame-0.png" ##x2 compared to the pixl file

#White assassin
player_image_information = [[4,4,60,78],
                            [68,4,60,78],
                            [132,4,60,78],
                            [4,88,60,78],
                            [68,88,60,78]
                            ]
#Grey assassin
player_image_information_2 = [[4,306,52,72],
                              [62,306,52,72],
                              [120,306,52,72],
                              [178,306,52,72],
                              [236,306,52,72]
                              ]
#The hurt images
player_hurt = [[4,384,52,72],
                [62,384,52,72],
                [120,384,52,72],
                [178,384,52,72],
                [236,384,52,72]
               ]

#Player's "bullets"
KNIFE = [138,102,32,12]
THROWING_KNIFE = [132,122,40,22]

#Grey ghost.
ghost_image_information = [[196,4,42,68],
                           [244,4,42,68],
                           [292,4,42,68],
                           [340,4,42,68],
                           ]
#Blue ghost
ghost_image_2 = [[388,4,48,74],
                [442,4,48,74],
                [496,4,48,74],
                [550,4,48,74]
                 ]
#Pumpkin
pumpkin_image_information = [[178,94,50, 46],
                             [234,94,50, 50],
                             [290,94,50, 52],
                             [348,94,50, 52]
                             ]
#Smile
smile_information = [404,94,42,42]

buttons_dict = {
    "pause_0": [4,172,26,26], #Paused button unhovered
    "pause_1": [4,204,26,26], #Paused button hovered
    "x_0": [36,172,26,26], #X button unhovered
    "x_1": [36,204,26,26], #X button hovered
    "restart_0": [68,172,92,26], #Restart button unhovered
    "restart_1": [68,204,92,26], #Restart button hovered
    "play_0": [4,236,64,64], #Play button unhovered
    "play_1": [74,236,64,64], #Play button hovered
    #save and load buttons
    "save1_0": [144,236,72,26],
    "save1_1": [294,300,72,26],
    "load1_0": [144,268,72,26],
    "load1_1": [294,332,72,26],
    
    "save2_0": [222,236,72,26],
    "save2_1": [372,300,72,26],
    "load2_0": [222,268,72,26],
    "load2_1": [372,332,72,26],
    
    "save3_0": [300,236,72,26],
    "save3_1": [450,300,72,26],
    "load3_0": [300,268,72,26],
    "load3_1": [450,332,72,26],
    }

items_dict = {
    "up": [342,152,26,26], #UP
    "sword": [374,152,26,26], #Sword
    "life": [178,184,26,26], #Life
    "speed": [210,184,26,26], #Speed
    "coin": [310,152,26,26]
    }

#These are for the enemy to shoot.
PINK_ORB = [178,152,26,26]
BLUE_ORB = [210,152,26,26]

#Heart image locations, dimensions.
HEART = [242,152,30,24]
EMPTY_HEART = [276,152,30,24]

Tileset = "pixil-frame-0 (5).png" ##x4 compared to the pixl file.
tiles_dict = {
    "stone": [4,4,64,64],
    "wooden_crate": [72,4,64,64],
    "grass": [140,4,64,64],
    "portal": [4,72,76,116],
    "brick": [84,72,64,64],
    "steel": [152,72,64,64],
    "warning":[220,72,64,64],
    }

#For loading images into the game.
class Sprite_loader():
    def __init__(self, file):
        self.sprite_sheet = pygame.image.load(file).convert()
    def get_image(self,x,y,width,height):
        image = pygame.Surface([width, height]).convert()
        image.blit(self.sprite_sheet, (0,0), (x,y,width,height))
        image.set_colorkey(GREEN)
        return image

#Controls the player.
class Player(pygame.sprite.Sprite):
    def __init__(self, grunt_sound):
        super().__init__()
        #Makes the left and right frames of the player.
        self.right_frames = animatedFrames(player_images, player_image_information_2, False)
        self.left_frames = animatedFrames(player_images, player_image_information_2, True)
        #Left and right frames while the player is hurt.
        self.hurt_right = animatedFrames(player_images, player_hurt, False)
        self.hurt_left = animatedFrames(player_images, player_hurt, True)

        #The player is facing right at the start and uses the "first right frame"
        self.image = self.right_frames[0] 
        # Rect of the player (x,y,width,height)
        self.rect = self.image.get_rect()
        
        # Set speed vector of player
        self.change_x = 0
        self.change_y = 0

        #Player variables
        self.max_lives = 5 #Maximum amount of lives that the player can have.
        self.lives = 3 #The current amount of lives that the player has.
        self.speed = 6 #How fast that the player can travel. (Pixels per frame)
        self.direction = "R" #The current direction that the player is facing.
        self.dmg = 1 #How much dmg that the player does per "bullet"
        self.dmg_boost_end = 0 #boost timers.
        self.speed_boost_end = 0
        self.hurt_timer = 0
        self.score = 0 #The current score.
        self.hurt = False #Whether the player is hurt or not
        self.level = None #The current level that the player is on 

        self.grunt_sound = grunt_sound #sound of the player being hurt.
 
    def update(self):
        # Move the player.
        # Gravity
        self.calc_grav()
        
        # Move left/right
        self.rect.x += self.change_x
        
        pos = self.rect.x + self.level.world_shift
        #Animated images.
        if self.direction == "R":
            frame = (pos // 30) % len(self.right_frames)
            if self.hurt:
                self.image = self.hurt_right[frame]
            else:
                self.image = self.right_frames[frame]
        else:
            frame = (pos // 30) % len(self.left_frames)
            if self.hurt:
                self.image = self.hurt_left[frame]
            else:
                self.image = self.left_frames[frame]
        
        # See if we hit any barriers
        barrier_hit_list = pygame.sprite.spritecollide(self, self.level.barrier_list, False)
        for block in barrier_hit_list:
            # If we are moving right,
            # set our right side to the left side of the item we hit
            if self.change_x > 0:
                self.rect.right = block.rect.left
            elif self.change_x < 0:
                # Otherwise if we are moving left, do the opposite.
                self.rect.left = block.rect.right
        
        # See if we hit platforms.
        platform_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in platform_hit_list:
            # If we are moving right,
            # set our right side to the left side of the item we hit
            if self.change_x > 0:
                self.rect.right = block.rect.left
            elif self.change_x < 0:
                # Otherwise if we are moving left, do the opposite.
                self.rect.left = block.rect.right
 
        # Move up/down
        self.rect.y += self.change_y
 
        # Check and see if we hit anything
        platform_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in platform_hit_list:
            # Reset our position based on the top/bottom of the object.
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            elif self.change_y < 0:
                self.rect.top = block.rect.bottom
            # Stop our vertical movement
            self.change_y = 0
            #If the platform is a moving platform, move with the platform.
            if isinstance(block, MovingPlatform):
                self.rect.x += block.change_x

        #Checks whether the enemy bullet has hit the player.
        enemy_collision = pygame.sprite.spritecollide(self, self.level.enemy_bullet_list, False)
        #Remove the enemy projectile, take away one of the player's lives, play the hurt sound, set the player as hurt.
        for bullet in enemy_collision:
            bullet.delete()
            self.lives -= 1
            pygame.mixer.Sound.play(self.grunt_sound)
            self.hurt_timer = 30
            self.hurt = True

        #Check whether or not the player collides with a upgrade.
        upgrade_collision = pygame.sprite.spritecollide(self, self.level.upgrade_list, True)
        for upgrade in upgrade_collision:
            upgrade.hit()
        #Checks whether the player hits a coin
        Collidable_hit_list = pygame.sprite.spritecollide(self, self.level.collidable_list, True)
        for coin in Collidable_hit_list:
            self.score += coin.value
            
        #Boost timers.
        current_time = pygame.time.get_ticks()
        if current_time > self.speed_boost_end:
            self.speed = 6
        if current_time > self.dmg_boost_end:
            self.dmg = 1
        #Controls how long the player is hurt for.
        if self.hurt_timer > 0:
            self.hurt_timer -= 1
            if self.hurt_timer == 0:
                self.hurt = False
    
    def calc_grav(self):
        # Calculate effect of gravity.
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += .35
        # See if we are on the ground.
        if self.rect.y >= SCREEN_HEIGHT - self.rect.height and self.change_y >= 0:
            self.change_y = 0
            self.rect.y = SCREEN_HEIGHT - self.rect.height
    def jump(self):
        # Called when user hits 'jump' button. """
 
        # move down a bit and see if there is a platform below us.
        # Move down 2 pixels because it doesn't work well if we only move down
        # 1 when working with a platform moving down.
        self.rect.y += 2
        platform_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        self.rect.y -= 2
 
        # If it is ok to jump, set our speed upwards
        if len(platform_hit_list) > 0 or self.rect.bottom >= SCREEN_HEIGHT:
            self.change_y = -10
 
    # Player-controlled movement:
    def right(self):
        self.change_x = self.speed
        self.direction = "R"
    def left(self):
        self.change_x = self.speed * -1
        self.direction = "L"
    def stop(self):
        self.change_x = 0
    #Timed upgrades go here.
    def speed_boost(self):
        current_time = pygame.time.get_ticks()
        self.speed_boost_end = current_time + 30000
        self.speed = 12
    def dmg_boost(self):
        current_time = pygame.time.get_ticks()
        self.dmg_boost_end = current_time + 30000
        self.dmg = 12

#Draws the lives onto the screen.
class Lives(pygame.sprite.Sprite):
    def __init__(self, player, life_no):
        super().__init__()
        self.player = player
        self.life_no = life_no
        
        file = Sprite_loader(player_images)
        self.heart = file.get_image(HEART[0],HEART[1],HEART[2],HEART[3])
        self.empty_heart = file.get_image(EMPTY_HEART[0],EMPTY_HEART[1],EMPTY_HEART[2],EMPTY_HEART[3])
        
        self.image = self.heart
        self.rect = self.image.get_rect()
        #Position of the lives on the screen.
        self.rect.x = (life_no - 1) * self.rect.width + 35
        self.rect.y = 5
    def update(self):
        #Changes the image dephending on how many lives the player has.
        if self.player.lives <= self.life_no:
            self.image = self.empty_heart
        else:
            self.image = self.heart

class Enemy_Projectile (pygame.sprite.Sprite):
    def __init__(self, x, y, image_data):
        #Initialisation
        super().__init__()
        file = Sprite_loader(player_images)
        self.image = file.get_image(image_data[0], image_data[1], image_data[2], image_data[3])
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y

        #Shooting Related
        #Actual center of the object
        self.pos = pygame.math.Vector2(self.rect.center)
        self.speed = 7
        
        #Game Related
        self.player = None
        self.level = None
    #Updates the sprite each frame
    def update(self):
        self.pos += self.vel
        #Makes it so that the hitbox lines up with the actual center.
        self.rect.center = self.pos
        #the -200/+200 are so that even if the enemy is "off-screen",
        #the enemy is still able to shoot at the player.
        #Otherwise the enemy will create a projectile, but then the projectile is immediately deleted.
        if self.rect.x < -200 or self.rect.x > SCREEN_WIDTH+200 or self.rect.y < 0 or self.rect.y > SCREEN_HEIGHT:
            self.kill()

        platform_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        if platform_hit_list:
            self.kill()
        
    def calc_direction(self, shoot_style=0):
        #Uses Vector2 to move the bullets
        self.pos = pygame.math.Vector2(self.rect.center)
        if shoot_style == 0: #Smart shooting, shoots directly at the player.            
            self.end = self.player.rect.center
            vector = self.end - self.pos
            normal = vector.normalize()
            self.vel = normal * self.speed
        elif shoot_style == 1: #Shoot up
            self.vel = pygame.Vector2(0,-self.speed)
        elif shoot_style == 2: #Shoot down
            self.vel = pygame.Vector2(0,self.speed)
        elif shoot_style == 3: #Shoot left
           self.vel = pygame.Vector2(-self.speed,0)
        elif shoot_style == 4: #Shoot right
            self.vel= pygame.Vector2(self.speed,0)
        elif shoot_style == 5: #Smart shooting but (purposefully) less accurate.
            missing = pygame.Vector2(random.randint(-75,75), random.randint(-75,75))
            self.end = self.player.rect.center + missing
            vector = self.end - self.pos
            normal = vector.normalize()
            self.vel = normal * self.speed
        elif shoot_style == 6: #Shoots in a random direction
            self.end = (random.randint(0,SCREEN_WIDTH), random.randint(0,SCREEN_HEIGHT))
            vector = self.end - self.pos
            normal = vector.normalize()
            self.vel = normal * self.speed
    def delete(self):
        self.kill()
        
#The enemy has a set boundaries.
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, change_x, change_y, boundaries, shoot_style,
                 enemy_image_information, projectile_data, reload_time):
        super().__init__()
        #RECT and IMAGE information, animation related.
        #Makes the left and right frames of the player
        self.right_frames = animatedFrames(player_images, enemy_image_information, True)
        self.left_frames = animatedFrames(player_images, enemy_image_information, False)
        self.image = self.right_frames[0]

        #x,y,width,height
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        #Controls the image of the enemy
        self.frame_counter = 0
        self.direction = "R"

        #Which projectile that the enemy lauches.
        self.projectile_data = projectile_data
        
        #Speed
        self.change_x = change_x
        self.change_y = change_y
        #Boundaries
        self.boundary_left = boundaries[0]
        self.boundary_right = boundaries[1]
        self.boundary_top = boundaries[2]
        self.boundary_bottom = boundaries[3]

        #Shooting related
        self.shoot_timer = 0
        self.reload_time = reload_time
        self.shoot_style = shoot_style

        #Health
        self.health = 1

        #Game related
        self.player = None
        self.level = None
    
    def update(self):
        self.rect.x += self.change_x
        self.rect.y += self.change_y

        #animating the image
        self.frame_counter += 1
        if self.direction == "R":
            frame = (self.frame_counter // 15) % len(self.right_frames)
            self.image = self.right_frames[frame]
        else:
            frame = (self.frame_counter // 15) % len(self.left_frames)
            self.image = self.left_frames[frame]
        #Change direction for the y direction.
        if self.rect.bottom > self.boundary_bottom or self.rect.top < self.boundary_top:
            self.change_y *= -1
        
        cur_pos = self.rect.x - self.level.world_shift
        if cur_pos < self.boundary_left:
            self.change_x *= -1
            self.direction = "L"
        if cur_pos > self.boundary_right:
            self.change_x *= -1
            self.direction = "R"

        self.shoot_timer += 1
        #only shoots at the player if they are close (500 pixels)
        if abs(self.player.rect.x - self.rect.x) < 500:
            if self.shoot_timer >= self.reload_time:
                self.shoot()
                self.shoot_timer = 0
        #remove the sprite, if the sprite has no more "lives"
        if self.health <= 0:
            self.kill()
            self.player.score += 200
            
    #Creates the projectile.
    def shoot(self):
        #x,y,image_file, image_data
        projectile = Enemy_Projectile(self.rect.centerx, self.rect.centery, self.projectile_data)
        projectile.level = self.level
        projectile.player = self.player
        projectile.calc_direction(self.shoot_style)
        self.level.enemy_bullet_list.add(projectile)

#A colliadable is something that the player can "pickup"
class Collidable(pygame.sprite.Sprite):
    def __init__(self, filename, data, value=0):
        super().__init__()
        file = Sprite_loader(filename)
        self.image = file.get_image(data[0], data[1], data[2], data[3])
        self.rect = self.image.get_rect()
        self.value = value

class Power_Up(Collidable):
    def __init__(self, player, filename, data, upgrade_type):
        super().__init__(filename, data, 0)
        self.player = player
        self.upgrade_type = upgrade_type
        self.player = player
    def hit(self):
        #Speed boost
        if self.upgrade_type == 0:
            self.player.speed_boost()
        #Life upgrade
        elif self.upgrade_type == 1:
            if self.player.lives < self.player.max_lives:
                self.player.lives += 1
        #Damage upgrade
        elif self.upgrade_type == 2:
            self.player.dmg_boost()

#The things that the player can shoot.
class Bullet(pygame.sprite.Sprite):
    def __init__ (self,data,x,y):
        super().__init__()
        #Loading the image of the knife
        file = Sprite_loader(player_images)
        self.image = file.get_image(data[0], data[1], data[2], data[3])
        #rect data
        self.rect = self.image.get_rect()
        #other data
        self.level = None
        self.velocity = 8
        self.direction = 1
        self.true_pos = pygame.Vector2(x,y)
    def update(self):
        self.true_pos += (self.velocity * self.direction, 0)
        self.rect.topleft = self.true_pos
        platform_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        if platform_hit_list:
            self.kill()
        #If you hit an enemy, then delete the bullet.
        enemy_hit_list = pygame.sprite.spritecollide(self, self.level.enemy_list, False)
        if enemy_hit_list:
            self.kill()
        #The enemy loses 1 "life"
        for enemy in enemy_hit_list:
            enemy.health -= self.level.player.dmg
            
        #If the bullet goes off the screen, then the bullet is removed
        if self.rect.x < -100 or self.rect.x > SCREEN_WIDTH + 100:
            self.kill()

class Platform(pygame.sprite.Sprite):
    # Platform the user can jump on
    def __init__(self, data):
        # Platform constructor. Assumes constructed with user passing in
        # an array of 5 numbers like what's defined at the top of this code.
        super().__init__()
        file = Sprite_loader(Tileset)
        self.image = file.get_image(data[0], data[1], data[2], data[3])
        self.rect = self.image.get_rect()

#Boundaries of the level
class Barrier(pygame.sprite.Sprite):
    def __init__ (self,x):
        super().__init__()
        self.rect = pygame.Rect(x,0, 30, SCREEN_HEIGHT)

class MovingPlatform(Platform):
    # This is a fancier platform that can actually move.
    def __init__(self, data):
        super().__init__(data)
        
        self.change_x = 0
        self.change_y = 0
     
        self.boundary_top = 0
        self.boundary_bottom = 0
        self.boundary_left = 0
        self.boundary_right = 0
     
        self.player = None
     
        self.level = None
 
    def update(self):
        # Move the platform.
        # If the player is in the way, it will shove the player
        # out of the way. This does NOT handle what happens if a
        # platform shoves a player into another object. Make sure
        # moving platforms have clearance to push the player around
        # or add code to handle what happens if they don't. """
 
        # Move left/right
        self.rect.x += self.change_x
 
        # See if we hit the player
        hit = pygame.sprite.collide_rect(self, self.player)
        if hit:
            # We did hit the player. Shove the player around and
            # assume he/she won't hit anything else.
 
            # If we are moving right, set our right side
            # to the left side of the item we hit
            if self.change_x < 0:
                self.player.rect.right = self.rect.left
            else:
                # Otherwise if we are moving left, do the opposite.
                self.player.rect.left = self.rect.right
 
        # Move up/down
        self.rect.y += self.change_y
 
        # Check and see if we the player
        hit = pygame.sprite.collide_rect(self, self.player)
        if hit:
            # We did hit the player. Shove the player around and
            # assume he/she won't hit anything else.
            # Reset our position based on the top/bottom of the object.
            if self.change_y < 0:
                self.player.rect.bottom = self.rect.top
            else:
                self.player.rect.top = self.rect.bottom
 
        # Check the boundaries and see if we need to reverse
        # direction.
        if self.rect.bottom > self.boundary_bottom or self.rect.top < self.boundary_top:
            self.change_y *= -1
 
        cur_pos = self.rect.x - self.level.world_shift
        if cur_pos < self.boundary_left or cur_pos > self.boundary_right:
            self.change_x *= -1
    
class Level():
    # This is a generic super-class used to define a level.
    # Create a child class for each level with level-specific info.
    def __init__(self, player):
        # Constructor. Pass in a handle to player. Needed for when moving
        # platforms collide with the player.
        self.platform_list = pygame.sprite.Group()
        self.barrier_list = pygame.sprite.Group()
        
        #Things that the player that can collide with.
        self.collidable_list = pygame.sprite.Group()
        self.upgrade_list = pygame.sprite.Group()
        self.portal_sprite = pygame.sprite.GroupSingle()
        
        #enemy related
        self.enemy_list = pygame.sprite.Group()
        self.enemy_bullet_list = pygame.sprite.Group()
        
        #player
        self.player = player
        
        #background related
        self.background_colour = BLUE
        self.gotBackground = True
     
        # How far this world has been scrolled left/right
        self.world_shift = 0
 
    # Update everything on this level
    def update(self):
        # Update everything in this level.
        self.platform_list.update()
        self.enemy_list.update()
        self.enemy_bullet_list.update()

    def draw(self, screen):
        # Draw everything on this level.
        
        #offset is the amount I want all my backgrounds to be set back,
        #so that they don't begin at x = 0, but further back
        offset = 500
        # Draw the background
        screen.fill(self.background_colour) #Colour
        if self.gotBackground:
            screen.blit(self.background_0,(self.world_shift//3 - offset, 0))#Closest background.
            screen.blit(self.background_1,(self.world_shift//6 - offset, 0))
            screen.blit(self.background_2,(self.world_shift//9 - offset, 0))#Furthest Background.
        # Draw all the sprite lists that we have
        self.platform_list.draw(screen)
        #self.barrier_list.draw(screen)
        self.collidable_list.draw(screen)
        self.upgrade_list.draw(screen)
        self.portal_sprite.draw(screen) 
        self.enemy_list.draw(screen)
        self.enemy_bullet_list.draw(screen)

    def shift_world(self, shift_x):
        # When the user moves left/right and we need to scroll everything:

        # Keep track of the shift amount
        self.world_shift += shift_x

        # Shift all of the sprites accordingly.
        for platform in self.platform_list:
            platform.rect.x += shift_x

        for enemy in self.enemy_list:
            enemy.rect.x += shift_x
           
        for bullet in self.enemy_bullet_list:
            bullet.pos += pygame.Vector2(shift_x, 0)
            bullet.rect.center = bullet.pos

        for barrier in self.barrier_list:
            barrier.rect.x += shift_x

        for portal in self.portal_sprite:
            portal.rect.x += shift_x

        for item in self.collidable_list:
            item.rect.x += shift_x

        for upgrade in self.upgrade_list:
            upgrade.rect.x += shift_x

# Create platforms for the level
class Level_01(Level):
    # Definition for level 1.

    def __init__(self, player):
        # Call the parent constructor
        Level.__init__(self, player)

        #This is all for the parallax effect, only 1 background is technically needed.
        self.background_colour = (88,141,190)
        self.background_0 = pygame.image.load("2.png").convert()
        self.background_1 = pygame.image.load("3.png").convert()
        self.background_2 = pygame.image.load("4.png").convert()
        self.background_0.set_colorkey(WHITE)
        self.background_1.set_colorkey(WHITE)
        self.background_2.set_colorkey(WHITE)
        #Even though portal isn't a "Collidable" per say, it is something that the player collides with.
        portal = Collidable(Tileset, tiles_dict["portal"])
        portal.rect.x = 1800
        portal.rect.y = 150
        self.portal_sprite.add(portal)
        #Boundaries
        barriers = [[-200],
                    [2000]
                    ]
        for bar in barriers:
            block = Barrier(bar[0])
            block.player = self.player
            self.barrier_list.add(block)
        #Items
        items = [[items_dict["coin"],800,500,50],
                 [items_dict["coin"],830,500,50],
                 [items_dict["coin"],860,500,100],
                 [items_dict["coin"],890,500,100]
                 ]
        for item in items:
            thing = Collidable(player_images, item[0], item[3])
            thing.rect.x = item[1]
            thing.rect.y = item[2]
            self.collidable_list.add(thing)
        #Upgrades
        upgrades = [[items_dict["sword"], -100, 500,2]
                    ]
        for upgrade in upgrades:
            thing = Power_Up(self.player, player_images, upgrade[0], upgrade[3])
            thing.rect.x = upgrade[1]
            thing.rect.y = upgrade[2]
            self.upgrade_list.add(thing)
        #Platforms
        # Array with width, height, x, and y of platform
        platforms = [[tiles_dict["grass"], 500, 500],
                 [tiles_dict["grass"], 564, 500],
                 [tiles_dict["grass"], 628, 500],
                 [tiles_dict["stone"], 800, 400],
                 [tiles_dict["stone"], 864, 400],
                 [tiles_dict["stone"], 928, 400],
                 [tiles_dict["grass"], 1000, 250],
                 [tiles_dict["grass"], 1064, 250],
                 [tiles_dict["grass"], 1128, 250],
                 ]
        # Go through the array above and add platforms
        for platform in platforms:
            block = Platform(platform[0])
            block.rect.x = platform[1]
            block.rect.y = platform[2]
            block.player = self.player
            self.platform_list.add(block)

        # Add a custom moving platform
        block = MovingPlatform(tiles_dict["wooden_crate"])
        block.rect.x = 1350
        block.rect.y = 280
        block.boundary_left = 1350
        block.boundary_right = 1600
        block.change_x = 1
        block.player = self.player
        block.level = self
        self.platform_list.add(block)

        #Adding a test enemy.
        #x, y, change_x, change_y, boundaries, shoot_style, image_information, reload_time
        enemy = Enemy(1350,100, 2, 1, [1350,1600,100,200], 0, ghost_image_information, BLUE_ORB, 30)
        enemy.player = self.player
        enemy.level = self
        enemy.health = 3
        self.enemy_list.add(enemy)

        enemy = Enemy(400,100, 0, 0, [0,0,0,0], 4, pumpkin_image_information, PINK_ORB, 50)
        enemy.player = self.player
        enemy.level = self
        enemy.health = 3
        self.enemy_list.add(enemy)


# Create platforms for the level
class Level_02(Level):
    # Definition for level 2.
    def __init__(self, player):
        # Call the parent constructor
        Level.__init__(self, player)
        
        self.background_colour = (218,94,83)
        self.background_0 = pygame.image.load("far-trees.png").convert()
        self.background_1 = pygame.image.load("mid-trees.png").convert()
        self.background_2 = pygame.image.load("close-trees.png").convert()
        self.background_0.set_colorkey(WHITE)
        self.background_1.set_colorkey(WHITE)
        self.background_2.set_colorkey(WHITE)

        portal = Collidable(Tileset, tiles_dict["portal"])
        portal.rect.x = 1450
        portal.rect.y = 20
        self.portal_sprite.add(portal)
        
        barriers = [[-200],
                    [2500]
                    ]
        for bar in barriers:
            block = Barrier(bar[0])
            block.player = self.player
            self.barrier_list.add(block)

        
        #Items
        items = [[items_dict["coin"],670,170,200],
                 [items_dict["coin"],700,170,150],
                 [items_dict["coin"],730,170,150],
                 [items_dict["coin"],760,170,150],
                 [items_dict["coin"],1632,100,500],
                 [items_dict["coin"],1632,300,300],
                 [items_dict["coin"],1632,500,100],
                 ]
        
        for item in items:
            thing = Collidable(player_images, item[0], item[3])
            thing.rect.x = item[1]
            thing.rect.y = item[2]
            self.collidable_list.add(thing)
        
        upgrades = [[items_dict["speed"], 800, 400,0],
                    [items_dict["life"], -100, 500,1]
                    ]
        for upgrade in upgrades:
            thing = Power_Up(self.player, player_images, upgrade[0], upgrade[3])
            thing.rect.x = upgrade[1]
            thing.rect.y = upgrade[2]
            self.upgrade_list.add(thing)
        
        # Array with type of platform, and x, y location of the platform.
        platforms = [[tiles_dict["grass"], 450, 500],
                     [tiles_dict["grass"], 514, 500],
                     [tiles_dict["stone"], 692, 436],
                     [tiles_dict["stone"], 756, 436],
                     [tiles_dict["stone"], 820, 436],
                     [tiles_dict["warning"], 628, 224],
                     [tiles_dict["warning"], 692, 224],
                     [tiles_dict["warning"], 756, 224],
                     [tiles_dict["stone"], 948, 308],
                     [tiles_dict["stone"], 1012, 308],
                     [tiles_dict["stone"], 1076, 308],
                     [tiles_dict["steel"], 1204, 436],
                     [tiles_dict["steel"], 1268, 436],
                     [tiles_dict["steel"], 1332, 436],
                 ]
        # Go through the array above and add platforms
        for platform in platforms:
            block = Platform(platform[0])
            block.rect.x = platform[1]
            block.rect.y = platform[2]
            block.player = self.player
            self.platform_list.add(block)

        # Add a custom moving platform
        block = MovingPlatform(tiles_dict["wooden_crate"])
        block.rect.x = 1460
        block.rect.y = 300
        block.boundary_top = 150
        block.boundary_bottom = 412
        block.change_y = -2
        block.player = self.player
        block.level = self
        self.platform_list.add(block)

        #x, y, change_x, change_y, boundaries, shoot_style, image_information, reload_time
        enemy = Enemy(1700,150, 2, -1, [1670,1800,50,550], 0, ghost_image_2, BLUE_ORB, 40)
        enemy.player = self.player
        enemy.level = self
        enemy.health = 5
        self.enemy_list.add(enemy)
# Create platforms for the level
class Level_03(Level):
    # Definition for level 3.
    def __init__(self, player):
        # Call the parent constructor
        Level.__init__(self, player)

        #This is all for the parallax effect, only 1 background is technically needed.
        self.background_colour = (5,44,70)
        self.background_0 = pygame.image.load("far-buildings.png").convert()
        self.background_1 = pygame.image.load("back-buildings.png").convert()
        self.background_2 = pygame.image.load("foreground.png").convert()
        self.background_0.set_colorkey(WHITE)
        self.background_1.set_colorkey(WHITE)
        self.background_2.set_colorkey(WHITE)

        #Even though portal isn't a "Collidable" per say, it is something that the player collides with.
        portal = Collidable(Tileset, tiles_dict["portal"])
        portal.rect.x = 436
        portal.rect.y = 90
        self.portal_sprite.add(portal)
        
        barriers = [[-200],
                    [2000]
                    ]
        for bar in barriers:
            block = Barrier(bar[0])
            block.player = self.player
            self.barrier_list.add(block)

        upgrades = [[items_dict["life"], 1420, 100,1],
                    [items_dict["life"], 1450, 100,1],
                    [items_dict["life"], 1480, 100,1],
                    ]
        for upgrade in upgrades:
            thing = Power_Up(self.player, player_images, upgrade[0], upgrade[3])
            thing.rect.x = upgrade[1]
            thing.rect.y = upgrade[2]
            self.upgrade_list.add(thing)
        
        #Platforms
        # Array with width, height, x, and y of platform
        platforms = [[tiles_dict["grass"], 500, 520],
                     [tiles_dict["grass"], 564, 520],
                     [tiles_dict["grass"], 692, 460],
                     [tiles_dict["grass"], 756, 460],
                     [tiles_dict["grass"], 820, 460],
                     [tiles_dict["stone"], 948, 396],
                     [tiles_dict["stone"], 1012, 396],
                     [tiles_dict["steel"], 1132, 520],
                     [tiles_dict["steel"], 1196, 520],
                     [tiles_dict["warning"], 1132, 256],
                     [tiles_dict["warning"], 1196, 256],
                     [tiles_dict["brick"], 948, 156],
                     [tiles_dict["brick"], 884, 156],
                     [tiles_dict["stone"], 756, 216],
                     [tiles_dict["stone"], 692, 216],
                     [tiles_dict["steel"], 500, 216],
                     [tiles_dict["steel"], 436, 216],
                     [tiles_dict["steel"], 372, 216],
                     [tiles_dict["warning"], 1324, 396],
                     [tiles_dict["warning"], 1388, 396],
                     [tiles_dict["stone"], 1388, 130],
                     [tiles_dict["stone"], 1452, 130],
                     ]
        # Go through the array above and add platforms
        for platform in platforms:
            block = Platform(platform[0])
            block.rect.x = platform[1]
            block.rect.y = platform[2]
            block.player = self.player
            self.platform_list.add(block)

        #x, y, change_x, change_y, boundaries, shoot_style, image_information, reload_time
        enemy = Enemy(1324,150, 0, 0, [0,0,0,0], 3, ghost_image_2, BLUE_ORB, 40)
        enemy.player = self.player
        enemy.level = self
        self.enemy_list.add(enemy)

        #x, y, change_x, change_y, boundaries, shoot_style, image_information, reload_time
        enemy = Enemy(1516,300, 1, 0, [1452,1580,300,300], 3, ghost_image_2, BLUE_ORB, 50)
        enemy.player = self.player
        enemy.level = self
        self.enemy_list.add(enemy)
        
class Level_Random(Level):
    #Test random level.
    def __init__(self, player, number_of_platforms):
        Level.__init__(self, player)
        #There is no background for level 4
        self.gotBackground = False
        
        level, enemy_list = RandomLevelMaker.makePlatforms(number_of_platforms)
        for platform in level:
            block = Platform(platform[0])
            block.rect.x = platform[1]
            block.rect.y = platform[2]
            block.player = self.player
            self.platform_list.add(block)

        #monsters = [ghost_image_2, ghost_image_information, pumpkin_image_information]
        for item in enemy_list:
            image_data = random.choice([ghost_image_2, ghost_image_information, pumpkin_image_information])
            orb = random.choice([PINK_ORB, BLUE_ORB])
            enemy = Enemy(item[0],item[1], 0, 0, [0,0,0,0], 0, image_data, orb, 50)
            enemy.player = self.player
            enemy.level = self
            self.enemy_list.add(enemy)
        
        #Even though portal isn't a "Collidable" per say, it is something that the player collides with.
        portal = Collidable(Tileset, tiles_dict["portal"])
        #Put the portal after the last platform.
        portal.rect.x = level[-1][1] + 80
        portal.rect.y = level[-1][2] - 128
        self.portal_sprite.add(portal)

        #Left and the right barrier.
        leftBarrier = Barrier(-400)
        leftBarrier.rect.x = -400 #400 behind the starting position
        leftBarrier.rect.y = 0
        leftBarrier.player = self.player
        self.barrier_list.add(leftBarrier)

        rightBarrier = Barrier((level[-1][1] + 500))
        rightBarrier.rect.x = level[-1][1] + 500 #500 after the last platform.
        rightBarrier.rect.y = 0
        rightBarrier.player = self.player
        self.barrier_list.add(rightBarrier)
        
#Makes a button
class Button(pygame.sprite.Sprite):
    # (x, y, width, height) for the dimensions
    # colour for the uncollided, colour2 for collided.
    def __init__(self, x, y, image_0, image_1, scale):
        super().__init__()
        file = Sprite_loader(player_images)
        state_0 = file.get_image(image_0[0],image_0[1],image_0[2],image_0[3])
        state_1 = file.get_image(image_1[0],image_1[1],image_1[2],image_1[3])

        #scales the button to size
        self.state_0 = pygame.transform.scale(state_0, (image_0[2]*scale,image_0[3]*scale))
        self.state_1 = pygame.transform.scale(state_1, (image_1[2]*scale,image_1[3]*scale))
        
        self.image = self.state_0
        #Rect attributes.
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def isOver(self, mouse):
        #checks for collision with the mouse.
        if self.rect.collidepoint(mouse):
            #Changes the image if the mouse is over the button
            self.image = self.state_1
            #for another function to be called
            return True
        else:
            #Sets the colour to the default colour.
            self.image = self.state_0
        return False
    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))

#Input box, allows the player to enter their name when they win.
class InputBox(pygame.sprite.Sprite):
    def __init__(self,x,y,width,height, FONT, text=""):
        self.rect = pygame.Rect(x,y,width,height)
        self.colour_1 = RED
        self.colour_2 = GREEN
        self.colour = self.colour_1
        self.font = FONT
        self.text = text
        self.text_surface = FONT.render(text,True,WHITE)
        self.active = False
    
    def event_handling(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                if self.active == True:
                    self.active = False
                else:
                    self.active = True
                self.text = "" #Clears the text box if you reclick on to it.
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    if len(self.text) > 15:
                        self.text = self.text[:15]
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
        self.text_surface = self.font.render(self.text, True, WHITE)
        #Makes sure that the amount of characters that are physically displayed
        #On screen doesn't overlap the box.
        if len(self.text) > 8:
            self.text_surface = self.font.render(self.text[-8:],True,WHITE)
        #Changes the colour dephending on whether or not you can type in the box.
        if self.active:
            self.colour = self.colour_1
        else:
            self.colour = self.colour_2
    def draw (self, screen):
        screen.blit(self.text_surface, (self.rect.x+5, self.rect.y+5))
        pygame.draw.rect(screen, self.colour, self.rect, 2)

###FUNCTIONS###

#function for the animated frames of the game. (player and enemies)
def animatedFrames(image_sheet,image_data, flipped):
    #image_sheet is the image that the function needs to pull from
    #image data needs to contain the (x location, y location, width, height) of
    # the frame
    #flipped is a boolean of whether the image is horizontally flipped.
    picture = Sprite_loader(image_sheet)
    frames = []
    for image in image_data:
        x = image[0]
        y = image[1]
        width = image[2]
        height = image[3]
        frame = picture.get_image(x,y,width,height)
        #frame is the image to be transformed
        #if flipped is true, then the image is flipped horizontally
        #I don't ever need to flip images vertically, so 3rd parameter is False
        frame = pygame.transform.flip(frame, flipped, False)
        frames.append(frame)
    return frames

#Writing data and reading data into the program.
def writeData(filename, data):
    pickle_out = open(filename, "wb")
    pickle.dump(data, pickle_out)
    pickle_out.close()
    
def readData(filename):
    pickle_in = open(filename, "rb")
    new_list = pickle.load(pickle_in)
    return new_list

def highscoreChecker(arr):
    ##Bubble Sort
    n = len(arr)
    # Traverse through all array elements 
    for i in range(n): 
        # Last i elements are already in place 
        for j in range(0, n-i-1): 
            # traverse the array from 0 to n-i-1 
            # Swap if the element found is greater 
            # than the next element
            if arr[j][1] < arr[j+1][1]: 
                arr[j], arr[j+1] = arr[j+1], arr[j]
    while len(arr) > 5:
        arr.pop()
    return arr

#Intro Screen.
def intro(screen, clock, FONT, x_button):
    background = pygame.image.load("Intro screen.png").convert()
    background.set_colorkey(WHITE)

    #Play the game
    play_button = Button(334,234, buttons_dict["play_0"], buttons_dict["play_1"],2)
    
    game_quit = False
    intro = True
    while intro:
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                intro = False
                game_quit = True
            if event.type == pygame.KEYDOWN:
                # Escape and p allow you to close the paused screen.
                if event.key == pygame.K_p:
                    intro = False
                if event.key == pygame.K_ESCAPE:
                    intro = False
            
            # Checks for mouse click on the buttons.
            # "x button" also allows you to close the pause screen.
            if event.type == pygame.MOUSEBUTTONDOWN:
                if x_button.isOver(mouse_pos):
                    intro = False
                    game_quit = True
                if play_button.isOver(mouse_pos):
                    intro = False
        
        x_button.isOver(mouse_pos) #allows for the changing of colours/picture.
        play_button.isOver(mouse_pos)
        ###
        screen.fill(WHITE)
        screen.blit(background, (0,0))
        x_button.draw(screen)
        play_button.draw(screen)
        pygame.display.flip()
        clock.tick(60)
        ###
    
    #When the game_quit is returned to be true, then the main game loop ends.
    #This just avoids using global variables.
    return game_quit, game_quit

#Paused State.
def pause(screen, clock, FONT, x_button, prelives, lvl, prescore, save_file):
    background = pygame.image.load("Paused screen.png").convert()
    background.set_colorkey(WHITE)
    #defining each button.
    play_button = Button(334,184, buttons_dict["play_0"], buttons_dict["play_1"],2)
    save_button0 = Button(92,400, buttons_dict["save1_0"], buttons_dict["save1_1"],2)
    load_button0 = Button(92,470, buttons_dict["load1_0"], buttons_dict["load1_1"],2)
    save_button1 = Button(328,400, buttons_dict["save2_0"], buttons_dict["save2_1"],2)
    load_button1 = Button(328,470, buttons_dict["load2_0"], buttons_dict["load2_1"],2)
    save_button2 = Button(564,400, buttons_dict["save3_0"], buttons_dict["save3_1"],2)
    load_button2 = Button(564,470, buttons_dict["load3_0"], buttons_dict["load3_1"],2)
    #Button list
    button_list = [x_button, play_button,
                   save_button0,load_button0,save_button1,
                   load_button1,save_button2,load_button2]
    #For my different while loops
    save_list = [save_button0,save_button1,save_button2,]
    load_list = [load_button0,load_button1,load_button2,]

    #To escape from the different game loops.
    done = False
    finished = False
    #Allows the program to change which save file the player is accessing.
    load_save = -1

    #Pause loops.
    paused = True
    while paused:
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                paused = False
                done = True
                finished = True
            if event.type == pygame.KEYDOWN:
                # Escape allows you to close the paused screen.
                if event.key == pygame.K_ESCAPE:
                    paused = False
            # Checks for mouse click on the buttons.
            # "x button" also allows you to close the pause screen.
            if event.type == pygame.MOUSEBUTTONDOWN:
                if x_button.isOver(mouse_pos):
                    paused = False
                    done = True
                    finished = True
                if play_button.isOver(mouse_pos):
                    paused = False
                #Save and load save buttons.
                for n in range(0,2):
                    if save_list[n].isOver(mouse_pos):
                        save_file[n] = [prelives, lvl, prescore]
                        writeData("save files.pickle", save_file)
                    if load_list[n].isOver(mouse_pos):
                        load_save = n
                        paused = False
                        done = True
        #When the mouse is hovered over, the button changes image.
        for button in button_list:
            button.isOver(mouse_pos) #allows for the changing of colours/picture.
        ###
        screen.fill(WHITE)
        screen.blit(background, (0,0))
        #Draw the buttons.
        for button in button_list:
            button.draw(screen)
        pygame.display.flip()
        clock.tick(60)
        ###

    #This just avoids using global variables.
    return done, finished, save_file, load_save

def winScreen(screen, clock, FONT, x_button, highscores, score):
    background = pygame.image.load("Win screen.png").convert()
    background.set_colorkey(WHITE)
    #Adds a new button so that the player can restart the game.
    restart_button = Button(600, 525, buttons_dict["restart_0"], buttons_dict["restart_1"],2)
    #Input box so that the player can enter their name for the highscores.
    input_box = InputBox(325,447,140,32,FONT)

    #Whether the player would like to resart
    restart = False
    #So that the input box is deleted when the use presses enter.
    entered = False

    #Win screen loop
    win_screen = True
    while win_screen:
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                win_screen = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    entered = True
            # Checks for mouse click on the buttons.
            # "x button" also allows you to close the win screen.
            # "restart_button" allows the player to restart the game.
            if event.type == pygame.MOUSEBUTTONDOWN:
                if restart_button.isOver(mouse_pos):
                    win_screen = False
                    restart = True
                if x_button.isOver(mouse_pos):
                    win_screen = False
            input_box.event_handling(event)
        
        restart_button.isOver(mouse_pos) #allows for the changing of colours/picture.
        x_button.isOver(mouse_pos)
        
        screen.fill(WHITE)
        screen.blit(background,(0,0))
        #Display the text onto the screen.
        score_text = FONT.render(str(score), True, WHITE)
        screen.blit(score_text,[377,515])
        #Shows the highscores.
        for x in range (len(highscores)):
            highscore_name = FONT.render(highscores[x][0],True, WHITE)
            highscore_score = FONT.render(str(highscores[x][1]),True, WHITE)
            screen.blit(highscore_name, [0,(x+1)*50 + 80])
            screen.blit(highscore_score, [600,(x+1)*50 + 80])
        #Draw the buttons and input box.
        restart_button.draw(screen)
        x_button.draw(screen)
        if not entered:
            input_box.draw(screen)
        pygame.display.flip()
        clock.tick(60)

    #Adding the new highscore to the game.
    if input_box.text == "":
        name = "Unknown"
    else:
        name = input_box.text
    if len(name) > 15:
        name = name[:15]
    highscores.append([name,score])
    highscores = highscoreChecker(highscores)
    writeData("hiscores.pickle", highscores)
    
    return True, (not restart), highscores

def gameOver(screen, clock, FONT, x_button):
    background = pygame.image.load("game over screen.png").convert()
    background.set_colorkey(WHITE)
    #Adds a new button so that the player can restart the game.
    restart_button = Button(262, 261, buttons_dict["restart_0"], buttons_dict["restart_1"],3)
    #Whether the player would like to restart.
    restart = False
    #Game over loop.
    loop = True
    while loop:
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                loop = False
            # Checks for mouse click on the buttons.
            # "x button" also allows you to close the pause screen.
            # "restart_button" allows the player to restart the game.
            if event.type == pygame.MOUSEBUTTONDOWN:
                if restart_button.isOver(mouse_pos):
                    loop = False
                    restart = True
                if x_button.isOver(mouse_pos):
                    loop = False
                    
        restart_button.isOver(mouse_pos) #allows for the changing of colours/picture.
        x_button.isOver(mouse_pos)
        ###
        screen.fill(WHITE)
        screen.blit(background,(0,0))
        text = FONT.render("Game Over", True, BLACK)
        screen.blit(text, [250,250])
        #Draw buttons.
        restart_button.draw(screen)
        x_button.draw(screen)
        pygame.display.flip()
        clock.tick(60)
        ###
    
    return True, (not restart)

# Main Program
def main():
    #intialise the mixer, this is just for sound files.
    pygame.mixer.pre_init(22050, -16, 2, 256)
    #Initialise pygame
    pygame.init()
    # Set the height and width of the screen
    size = [SCREEN_WIDTH, SCREEN_HEIGHT] ## 800 x 600
    screen = pygame.display.set_mode(size)
    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()

    #The title inside the title bar when the game is run.
    pygame.display.set_caption("Platformer Thingy. Smile =)")
    #The font that the game uses.
    FONT = pygame.font.SysFont("Inkfree",25,True, False)
    
    #Music files and sound files.
    grunt = pygame.mixer.Sound("NFF-dusty-hit.wav")
    throw = pygame.mixer.Sound("NFF-throw-05.wav")
    #pygame.mixer.music.load("musicfile.mp3")

    #Related to the save files and highscores.
    #Default values are the values that the player should start with.
    #3 lives, level "0", score "0"
    default_values = [3,0,0]
    try:
        save_file = readData("save files.pickle")
    #Exception is used incase that this is the first time opening the program,
    #and therefore needs to create the pickle file.
    except FileNotFoundError:
        empty_list = []
        pickle_out = open("save files.pickle", "wb")
        pickle.dump(empty_list, pickle_out)
        pickle_out.close()
        save_file = []
    while len(save_file) < 3:
        save_file.append(default_values)
    save_state = -1
    #Do the same for highscores as I've done to the save files.
    try:
        highscores = readData("hiscores.pickle")
    except FileNotFoundError:
        empty_list = []
        pickle_out = open("hiscores.pickle", "wb")
        pickle.dump(empty_list, pickle_out)
        pickle_out.close()
        highscores = []
    print(highscores)
    # Create the player
    player = Player(grunt)

    #Finished is concerned with the restart functionality.
    finished = False
    while not finished:
        #When save_state = -1, then the game is using the default values.
        if save_state == -1:
            lives = default_values[0]
            current_level_no = default_values[1]
            score = default_values[2]
        else:
            if save_state < len(save_file):
                data = save_file[save_state]
                lives = data[0]
                current_level_no = data[1]
                score = data[2]
        #So that if the player wants to restart, they will be using the starting values
        #rather than the save file values.
        save_state = -1

        # Create all the levels
        level_list = []
        level_list.append(Level_01(player))
        level_list.append(Level_02(player))
        level_list.append(Level_03(player))
        level_list.append(Level_Random(player, 50))
        # Set the current level
        current_level = level_list[current_level_no]

        #groups, which allow the game to update and draw all the sprites
        active_sprite_list = pygame.sprite.Group()
        
        #player related.
        player.level = current_level
        player.rect.x = 340
        player.rect.y = SCREEN_HEIGHT - player.rect.height
        player.lives = lives
        player.score = score
        active_sprite_list.add(player)
        #Prescore and prelives for save files, so that the player can't farm life upgrades and score
        prelives = player.lives
        prescore = player.score
        
        # Making buttons
        x_button = Button(772, 5, buttons_dict["x_0"], buttons_dict["x_1"], 1)
        pause_button = Button(739, 5, buttons_dict["pause_0"], buttons_dict["pause_1"],1)

        #Creating the hearts that are shown.
        heart_list = pygame.sprite.Group()
        for x in range(player.max_lives):
            life = Lives(player, x)
            active_sprite_list.add(life)
            
        # loading save files.
        load_save = False

        # allows for the knifes to have a "cooldown" time.
        prev_bullet_time = pygame.time.get_ticks()

        #Show how long the player has been playing.
        start_time = pygame.time.get_ticks()
        
        # Loop until the user clicks the close button.
        done = False

        #Play the music.
        #pygame.mixer.music.play(-1)

        #Gives the game an intro screen.
        done, finished = intro(screen, clock, FONT, x_button)
        # -------- Main Program Loop -----------
        while not done:
            mouse_pos = pygame.mouse.get_pos() # gets the mouse position.
            for event in pygame.event.get():
                #Closes the program when the player presses the close button.
                if event.type == pygame.QUIT:
                    done = True
                    finished = True

                if event.type == pygame.KEYDOWN:
                    #controls movement of the player
                    if event.key == pygame.K_a:
                        player.left()
                    if event.key == pygame.K_d:
                        player.right()
                    if event.key == pygame.K_w:
                        player.jump()
                        
                    if event.key == pygame.K_ESCAPE: #close the program.
                        done = True
                        finished = True

                #when wasd are let go, the player stops moving.
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_a and player.change_x < 0:
                        player.stop()
                    if event.key == pygame.K_d and player.change_x > 0:
                        player.stop()

                #Checks for mouse click on the buttons.
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if x_button.isOver(mouse_pos):
                        #closes the program.
                        done = True
                        finished = True
                    elif pause_button.isOver(mouse_pos):
                        #opens the pause screen.
                        done, finished, save_file, save_state = pause(screen, clock, FONT, x_button, prelives, current_level_no, prescore, save_file)

                #Changes the colour/picture of the buttons when hovered over.
                x_button.isOver(mouse_pos)
                pause_button.isOver(mouse_pos)

            #Bullets with cooldown.
            keys = pygame.key.get_pressed()
            if keys[pygame.K_j]:
                current_time = pygame.time.get_ticks()
                #Controls a delay before another bullet can be shot. (500ms)
                if current_time - prev_bullet_time > 500:
                    #Create the bullet: image data, x location, y location
                    #x location is set to the players x location
                    #y location is set to half way into the player
                    bullet = Bullet(THROWING_KNIFE,
                                    player.rect.x,
                                    player.rect.y + (player.rect.height//2))
                    #The bullet needs to know which level it is on, so that it can collide with other
                    #objects.
                    bullet.level = current_level
                    #Checks whether the player is facing left, if so, the direction is flipped
                    #and so is the image.
                    if player.direction == "L":
                        bullet.direction = -1
                        bullet.image = pygame.transform.flip(bullet.image, True,False)
                    #Add to lists
                    active_sprite_list.add(bullet)
                    prev_bullet_time = current_time
                    pygame.mixer.Sound.play(throw)

            # Update the sprites on the screen.
            active_sprite_list.update()
            # Update items in the level
            current_level.update()

            # If the player gets near the right side, shift the world left (-x)
            if player.rect.right >= 500:
                diff = player.rect.right - 500
                player.rect.right = 500
                current_level.shift_world(-diff)

            # If the player gets near the left side, shift the world right (+x)
            if player.rect.left <= 120:
                diff = 120 - player.rect.left
                player.rect.left = 120
                current_level.shift_world(diff)

            #Controls level increases.
            portal_hit_list = pygame.sprite.spritecollide(player, current_level.portal_sprite, False)
            if portal_hit_list:
                current_level_no += 1
                #If there are no more levels left to go, then show the win screen.
                if current_level_no > len(level_list) - 1:
                    done, finished, highscores = winScreen(screen, clock, FONT, x_button, highscores, player.score)
                else:
                    current_level = level_list[current_level_no]
                    current_level.world_shift = 0
                    player.rect.x = 340
                    player.rect.y = SCREEN_HEIGHT - player.rect.height
                    player.level = current_level
                    prelives = player.lives
                    prescore = player.score
            #Kills the player if they don't have any lives left.
            if player.lives <= 0:
                done, finished = gameOver(screen, clock, FONT, x_button)
            #Loads a new save file.
            if save_state >= 0:
                done = True

            #Timer
            timer = pygame.time.get_ticks() - start_time
            minutes = (int(timer//1000))//60 #Time in minutes
            seconds = (int(timer//1000))%60 #Seconds spare.
            if seconds < 10:
                seconds = "0" + str(seconds)
            else:
                seconds = str(seconds)
            timer_formatted = str(minutes) + ":" + seconds
            timer_text = FONT.render(timer_formatted, True, YELLOW)
            
            # ALL CODE TO DRAW SHOULD GO BELOW THIS COMMENT
            current_level.draw(screen)
            active_sprite_list.draw(screen)
            
            x_button.draw(screen)
            pause_button.draw(screen)

            #Text based blitting
            score_text = FONT.render("Score: " + str(player.score), True, YELLOW)
            screen.blit(score_text, [5,30])
            screen.blit(timer_text, [5,60])
            # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT

            # Limit to 60 frames per second
            clock.tick(60)

            # update the screen to show what has been drawn.
            pygame.display.flip()
    
    #QUIT THE GAME
    pygame.quit()
    #quit()

if __name__ == "__main__":
    main()
