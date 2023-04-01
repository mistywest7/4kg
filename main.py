from pygame import *
from random import *
# music
#mixer.init()
#mixer.music.load('fire.ogg')
#mixer.music.play()
#fire_sound = mixer.Sound('fire.ogg')
# create window with background
win_width = 700
win_height = 500
display.set_caption("Shooter")
window = display.set_mode((win_width, win_height))
#background = transform.scale(image.load(img_back), (win_width, win_height))
background = transform.scale(image.load("space-g41c957f1c_1280.png"), (win_width, win_height))
# images
img_back = 'galaxy.png'
img_hero = 'rocket.png'
lost = 0
score = 0

font.init()
font2 = font.Font(None, 36)
font1 = font.Font(None, 80)
win = font1.render('YOU WIN!', True, (255, 255, 255))
lose = font1.render('YOU LOSE!', True, (180, 0, 0))
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y


    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.y = 0
            self.rect.x = randint(80, win_width -80)
            lost += 1


class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < win_height - 100:
            self.rect.y += self.speed

    def fire(self):
        bullet = Bullet('Bullet.png', self.rect.centerx, self.rect.top, 15, 20, 15)
        bullets.add(bullet)



class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed

        if self.rect.y < 0:
            self.kill()


lost += 1

monsters =sprite.Group()
for i in range(6):
    monster = Enemy('ufo.png' , randint(80, win_width -80), -40, 80, 50, randint(1, 5))
    monsters.add(monster)

bullets = sprite.Group()

ship = Player(img_hero, 5, win_height - 100, 60, 80, 10)

finish = False
run = True
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                ship.fire()




    if not finish:
        window.blit(background, (0, 0))
        ship.update()
        ship.reset()
        monsters.update()
        monsters.draw(window)
        bullets.update()
        bullets.draw(window)

        colides = sprite.groupcollide(monsters, bullets, True, True)
        for c in colides:
            score += 1
            monster = Enemy('ufo.png', randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)

        if sprite.spritecollide(ship, monsters, False) or lost > 5:
            finish = True
            window.blit(lose, (200, 200))

        if score > 10:
            finish = True
            window.blit(win,(200, 200))


        text = font2.render('score:' + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))

        text_lose = font2.render('missed:' + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))
        display.update()
    time.delay(50)

