from pygame import *
from random import randint
from time import time as timer
 
#music
mixer.init()
mixer.music.load("space.ogg")
mixer.music.play()
fire_sound = mixer.Sound("fire.ogg")
 
#font and captions
font.init()
font1 = font.Font(None,80)
font2 = font.Font(None,36)
win_message = font1.render("YOU WIN!", True, (255,255,255))
lose_message = font1.render("YOU LOST!", True, (180,0,0))
 
#images
img_rocket = "rocket.png"
img_ufo = "ufo.png"
img_ufo2 = "ufo_1.png"
img_bullet = "bullet.png"
 
score = 0
missed = 0
max_missed = 6
 
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        sprite.Sprite.__init__(self)    #inherit sprites features
        self.image = transform.scale(image.load(player_image),(size_x,size_y)) 
        self.speed = player_speed
        #Invisble rectangle
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
 
    def reset(self):
        window.blit(self.image,(self.rect.x, self.rect.y))
 
class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width-80:
            self.rect.x += self.speed
 
    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, 15)
        bullets.add(bullet)
 
class Enemy(GameSprite):
    #enemy movement
    def update(self):
        self.rect.y += self.speed
        #Dissapears n respawn above
        if self.rect.y > win_height:
            global missed
            self.rect.x = randint(80, win_width-80 )
            self.rect.y = 0
            missed += 1
 
class Bullet(GameSprite):
    def update(self):
        #movement
        self.rect.y -= self.speed
        #dissapears when reaching top of screen
        if self.rect.y < 0:
            self.kill()
 
#Create window
win_width = 700
win_height = 500
display.set_caption("Shooter")
window = display.set_mode((win_width,win_height))
background = transform.scale(image.load("galaxy.jpg"),(win_width,win_height))
 
#Sprites
rocket = Player(img_rocket, 5, win_height - 100, 80, 100, 10)
 
ufos = sprite.Group()
for i in range(1,6):
    ufo =  Enemy(img_ufo, randint(80, win_width-80), -40, 80, 50, randint(2,5))
    ufos.add(ufo)
 
bullets = sprite.Group()
 
# new_ufos = sprite.Group()
# for i in range(1,3):
#     new_ufo =  Enemy(img_ufo2, randint(80, win_width-80), -40, 80, 50, randint(1,3))
#     new_ufos.add(new_ufo)
 
finish = False
#Main game loop
run = True

rel_time = False
num_fire = 0

while run == True:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                
                if num_fire < 5 and rel_time == False:
                        num_fire += 1
                        fire_sound.play()
                        rocket.fire()

                if num_fire >= 5 and rel_time == False:
                        num_fire += 1
                        last_timer = timer()
                        rel_time = True
                        
 
    
    
    if finish == False:
        window.blit(background,(0,0))
 
        rocket.update()
        rocket.reset()
 
        text_score = font2.render("Score: " + str(score), 1,(99,53,23))
        text_lose =  font2.render("Missed: "+ str(missed), 1,(255,255,255)) 
        window.blit(text_score, (10,20))
        window.blit(text_lose, (10,50))      
 
        ufos.update()
        ufos.draw(window)
        # new_ufos.update()
        # new_ufos.draw(window)
        bullets.update()
        bullets.draw(window)

        #Reloading
        if rel_time == True:
            now_time = timer()

            if now_time - last_timer < 2:
                reload_text = font2.render("Wait,Reloading..",1,(150,0,0))
                window.blit(reload_text, (260,460))
            else:
                num_fire = 0
                rel_time = False


 
        #if bullet collide with ufos, returns a list of all ufos collided
        collides = sprite.groupcollide(ufos, bullets, True, True)
        for c in collides:
            score += 1
            ufo = Enemy(img_ufo, randint(80, win_width-80), -40, 80, 50, randint(2,5))
            ufos.add(ufo)
        #if bullet collide with new ufo
        # collides = sprite.groupcollide(new_ufos, bullets, True, True)
        # for c in collides:
        #     score += 1
        #     new_ufo =  Enemy(img_ufo2, randint(80, win_width-80), -40, 80, 50, randint(1,3))
        #     new_ufos.add(new_ufo)
        #(Lose condition) if rocket collide with ufo
        if sprite.spritecollide(rocket, ufos, False) or missed > max_missed:
            finish = True
            window.blit(lose_message, (200,200))
        #(Win condition)
        if score >= 10:
            finish = True
            window.blit(win_message, (200,200))
 
        display.update()
    time.delay(40)

    

    if finish == False:
        window.blit