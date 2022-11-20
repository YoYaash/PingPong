from pygame import *
# ──────▄▀▄─────▄▀▄
# ─────▄█░░▀▀▀▀▀░░█▄
# ─▄▄──█░░░░░░░░░░░█──▄▄
# █▄▄█─█░░▀░░┬░░▀░░█─█▄▄█
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, width, height):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (width, height))
        self.speed = player_speed
        #Rect
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
 
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
 
class Player(GameSprite):
    def update_r(self):
        keys = key.get_pressed()
        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < win_height-80:
            self.rect.y += self.speed
 
    def update_l(self):
        keys = key.get_pressed()
        if keys[K_w] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_s] and self.rect.y < win_height-80:
            self.rect.y += self.speed
 
#Game window
win_width = 600
win_height = 500
window = display.set_mode((win_width, win_height))
window.fill((40, 60, 120))
 
#Adding sprites
racket1 = Player("racket.png", 30, 200, 4, 50, 125)
racket2 = Player("racket.png", 520, 200, 4, 50, 125)
ball = GameSprite("tennis_ball.png", 200, 200, 4, 50 ,50)
#Fonts
font.init()
font = font.Font(None,35)
p1_lose = font.render("PLAYER 2 WINS!", True, (150,2,2))
p2_lose = font.render("PLAYER 1 WINS!", True, (150,2,2))
#Game state
FPS = 60
clock = time.Clock()
game = True
finish =  False
speed_x = 2 #-2
speed_y = 2 #-2
while game == True:
    #Allow to close the window
    for e in event.get():
        if e.type == QUIT:
            game = False
 
    if finish == False:
        window.fill((40, 60, 120))
        racket1.update_l()
        racket2.update_r()
        #ball movement
        ball.rect.x += speed_x
        ball.rect.y += speed_y
        #ball touches racket
        if sprite.collide_rect(racket1, ball) or sprite.collide_rect(racket2, ball):
            speed_x *= -1
            speed_y *= -1
        #reach edge of screen bounce
        if ball.rect.y > win_height - 50 or ball.rect.y<0:
            speed_y *= -1
        #player 1 lose
        if ball.rect.x < 0:
            finish = True
            window.blit(p1_lose, (200,200))
        #player 2 lose
        if ball.rect.x > win_width:
            finish = True
            window.blit(p2_lose, (200,200))
        racket1.reset()
        racket2.reset()
        ball.reset()
 
    display.update()
    clock.tick(FPS)
