from pygame import *
from random import randint
from time import sleep

win_width = 700
win_height = 500

window = display.set_mode((win_width,win_height))
display.set_caption("Шутер")

background = image.load('galaxy.jpg')
background = transform.scale(background,(win_width, win_height))

clock = time.Clock()
FPS = 60

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()

kills = 0
lost = 0

class GameSprite(sprite.Sprite):
	def __init__(self, img, w, h, x, y, speed):
		sprite.Sprite.__init__(self)
		self.w = w
		self.h = h
		self.image = image.load(img)
		self.image = transform.scale(self.image, (self.w, self.h))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.speed = speed
	def reset(self):
		window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
	def __init__(self, img, w, h, x, y, speed):
		GameSprite.__init__(self, img, w, h, x, y, speed)
	def update(self):
		keys = key.get_pressed()
		if keys[K_LEFT] and self.rect.x > 0:
			self.rect.x -= self.speed
		elif keys[K_RIGHT] and self.rect.x + self.w < win_width:
			self.rect.x += self.speed
	def fire(self):
		bullet = Bullet(img='bullet.png' ,w=20,h=40 ,x=self.rect.x, y=self.rect.y, speed=10)
		bullets.add(bullet) 

class UFO(GameSprite):
	def __init__(self, img, w, h, x, y, speed):
		GameSprite.__init__(self, img, w, h, x, y, speed)
	def update(self):
		global lost, text_lost
		self.rect.y += self.speed
		if self.rect.y > win_height:
			lost += 1
			text_lost = font14.render("Пропущено:" + str(lost),True,(255,255,255))
			self.rect.y = 0 
			self.rect.x = randint(0,win_width-self.w)

class Bullet(GameSprite):
	def __init__(self, img, w, h, x, y, speed):
		GameSprite.__init__(self, img, w, h, x, y, speed)
	def update(self):
		self.rect.y -= self.speed
		if self.rect.y+self.h <= 0:
			self.kill()

font.init()
font14=font.SysFont('Arial',14)
text_killed = font14.render("Убито:" + str(kills),True,(255,255,255))
text_lost = font14.render("Пропущено:" + str(lost),True,(255,255,255))

font24=font.SysFont('Arial',24)
text_win = font24.render("Победа",True,(255,255,255))
text_lost1 = font24.render("Проигрыш",True,(255,255,255))

player = Player(img ='rocket.png', w=50, h= 50, x= 450, y=450, speed=10)
bullets = sprite.Group()
enemies = sprite.Group()
for i in range(5):
	enemy = UFO(img ='ufo.png', w= 60, h= 50, x= randint(0, win_width-50), y=0, speed=10)
	enemies.add(enemy)

while True:
	window.blit(background,(0,0))
	window.blit(text_killed, (0, 10))
	window.blit(text_lost, (0, 50))
	enemies.draw(window)
	enemies.update()
	bullets.draw(window)
	bullets.update()
	player.reset()
	player.update()
	display.update()
	hits = sprite.groupcollide(bullets, enemies, True, True)
	for i in hits:
		kills += 1
		text_killed = font14.render("Убито:" + str(kills),True,(255,255,255))
		enemy = UFO(img ='ufo.png', w= 60, h= 50, x= randint(0, win_width-50), y=0, speed=10)
		enemies.add(enemy)
	if kills >= 10:
		window.blit(text_win, (win_width//2,win_height//2))
		display.update()
		sleep(1)
		quit()
	if lost > 30:
		window.blit(text_lost1, (win_width//2,win_height//2))
		display.update()
		sleep(1)
		quit()
	for i in event.get(): 
		if i.type==QUIT:
			quit()
		if i.type == KEYDOWN:
			if i.key == K_SPACE:
				player.fire()
	clock.tick(FPS)