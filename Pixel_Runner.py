import pygame
from sys import exit
from random import randint, choice

class Game():

	def __init__(i):

		global Spawn_Interval, Obstacle_Speed
		Spawn_Interval = 2000
		Obstacle_Speed = 2.7

		i.backgrd = pygame.sprite.Group()
		i.backgrd.add(Display_Image(sky_img,'topleft',0,0))
		i.backgrd.add((Display_Image(ground_img,'topleft',0,300)))

		i.player = pygame.sprite.GroupSingle()
		i.obstacle = pygame.sprite.Group()

		i.surf = pygame.Surface((w,h))
		i.surf.fill(BACKCOL)

		i.timer = 255
		i.countA = Counter(0,i.timer +1,2,'fixed_decrement')
		i.counterA = 0
		i.Obstacle_Spawn_Setting(Spawn_Interval)

	def run(i):
		global game
		x = i.countA.run()

		# Check event -------------------------------------------------------------
		for event in pygame.event.get():
			if event.type == QUIT: exit() 
			elif (event.type == PRESS) and (event.key == SPACE) and (x == 0 ): i.player.sprite.jump()
			elif (event.type == Spawn_Obstacle)                              : i.obstacle.add(Obstacle(choice(['snail','snail','snail','bird','snail'])))
			elif (event.type == Up_Difficulty)                               : i.Increase_Difficulty()
									
		
		# Update frame -------------------------------------------------------------
		i.surf.set_alpha(x)

		i.backgrd.draw(screen)
		i.backgrd.update()

		screen.blit(i.surf,(0,0))

		if x == 180: 
			i.backgrd.add(Display_Image(stand_img,'bottomleft',30,-70,'',0,300))
		if x == 140: 
			game_aud.play(loops = -1,fade_ms = 3500)
		if x == 2:
			i.player.add(Player())
			for sprite in i.backgrd: 
				if sprite.rect.left == 30: sprite.kill()
		if x == 0: 
			i.player.draw(screen)
			i.obstacle.draw(screen)
			
			Current_score = i.Update_Score()
			i.player.update()
			i.obstacle.update()
			
			if pygame.sprite.spritecollide(i.player.sprite,i.obstacle,False,pygame.sprite.collide_rect_ratio(0.85)): 
				game_aud.fadeout(2000)
				collide_aud.play()
				over_aud.play()
				game = Over(Current_score)
			
	def Obstacle_Spawn_Setting(i,timer):
		pygame.time.set_timer(Spawn_Obstacle,timer)

	def Increase_Difficulty(i):
		global Spawn_Interval, Obstacle_Speed 

		Spawn_Interval /= 1.1  # Reduced by by 10%
		Obstacle_Speed *= 1.1  # 110% X faster than previous

		i.Obstacle_Spawn_Setting(int(Spawn_Interval)) # Adjust spawn setting

	def Update_Score(i):
		global Start_Time

		if i.counterA < 100  : 
			screen.blit(ready_img,ready_img.get_rect(center = (400,50)))
			i.counterA += 1
			
		elif i.counterA == 100 :
			start_aud.play()
			i.counterA += 1

		elif i.counterA < 180: 
			screen.blit(go_img,go_img.get_rect(center = (400,50)))
			i.counterA += 1

		elif i.counterA == 180:
			Start_Time = pygame.time.get_ticks()
			i.counterA += 1
			
		else: 
		    score = int((pygame.time.get_ticks() - Start_Time)/1000)
		    score_img = font_type1.render(str(score),False,(64,64,64))
		    screen.blit(score_img,score_img.get_rect(center = (400,50)))
		    return score


class Intro():

	def __init__(i):

		i.backgrd = pygame.sprite.Group()
		i.backgrd.add(Display_Image(game_logo_img,'center',400,550,'fadein',250))

		i.surf = pygame.Surface((w,h))
		i.surf.fill(BACKCOL)

		i.timer , i.y = 60,60 
		i.countA = Counter(0,i.timer +1,1,'fixed_increment')

		intro_aud.play()

	def run(i):
		global game
		x = i.countA.run()

		# Check event -------------------------------------------------------------
		for event in pygame.event.get():
			if event.type == QUIT: exit() 
			elif (event.type == PRESS) and (event.key == SPACE) and (x == i.y + 1): 
				intro_aud.fadeout(1000)
				press_aud.play()
				i.y += 1
									
		
		# Update frame -------------------------------------------------------------
		screen.blit(i.surf,(0,0))
		i.backgrd.draw(screen)
		i.backgrd.update()

		if i.timer > x :screen.blit(i.surf,(0,235))
		elif i.timer == x :
			i.backgrd.add(Display_Image(intro_text1_img,'center',400,300))
			i.backgrd.add(Display_Image(intro_text2_img,'center',400,340,'blinking'))

		if pygame.mixer.get_busy() == False: game = Game()


class Over():

	def __init__(i,score):

		i.final_score = score

		i.backgrd = pygame.sprite.Group()
		i.backgrd.add(Display_Image(sky_img,'topleft',0,0))
		i.backgrd.add((Display_Image(ground_img,'topleft',0,300)))

		i.blink = pygame.sprite.Group()
		i.blink.add(Display_Image(intro_text2_img,'center',400,330,'blinking'))

		i.counterA = 0
		i.counterB = 0
		i.counterC = 0
		i.status = False

		i.surf = pygame.Surface((w,h))
		i.surf.set_alpha(200)

	def run(i):
		global game

		# Check event -------------------------------------------------------------
		for event in pygame.event.get():
			if event.type == QUIT: exit() 
			elif (event.type == PRESS) and (event.key == SPACE) and (i.status): 
				press_aud.play()
				game = Intro()


		# Update frame -------------------------------------------------------------
		
		if i.counterA == 0 :
			if pygame.mixer.get_busy() == False: 
				i.counterA += 1

		elif i.counterA == 1:

			i.backgrd.draw(screen)
			screen.blit(i.surf,(0,0))
			screen.blit(game_over_img,game_over_img.get_rect(center = (400,50)))
			screen.blit(over_text1_img,over_text1_img.get_rect(center = (400,140)))

			if i.Count_Score(): 
				i.blink.draw(screen)
				i.blink.update()
				i.status = True	


	def Count_Score(i):
		
		score_img = font_type1.render(str(i.counterB),False,'White')
		screen.blit(score_img,score_img.get_rect(center = (400,180)))

		if i.final_score > i.counterB: 
			i.counterC += 1

			if i.counterC == 5: 
				i.counterB += 1
				coin_aud.play()
				i.counterC = 0

			return False
		else: 
			return True


class Display_Image (pygame.sprite.Sprite):

	def __init__(i,image,which_point,pos_x,pos_y,appear='',popup=0,popdown=0):
		super().__init__()

		# Note: Documentation
			# which_point - 'topleft','center', bottomleft
			# appear      - 'fadein', 'blinking'
			# popup       - (int) smaller than pos_y
			# popdown     - (int) larger than pos_y

		i.image = image
		i.appear = appear
		i.popup = popup
		i.popdown = popdown

		if   which_point == 'topleft'     : i.rect = i.image.get_rect(topleft = (pos_x,pos_y))
		elif which_point == 'center'      : i.rect = i.image.get_rect(center = (pos_x,pos_y))
		elif which_point == 'bottomleft'  : i.rect = i.image.get_rect(bottomleft = (pos_x,pos_y))
			
		if   i.appear == 'fadein'      : i.countA = Counter(0,255,1.25,'fixed_increment')
		elif i.appear == 'blinking'    : i.countA = Counter(0,255,3.7,'back_forth')

		if   i.popup   : i.countB = Counter(i.popup,pos_y,9,'fixed_decrement')
		elif i.popdown : i.countB = Counter(pos_y,i.popdown,9,'fixed_increment')


	def update(i):
		if i.appear: i.image.set_alpha(i.countA.run())
		if (i.popup) or (i.popdown) : i.rect.bottom = i.countB.run()
class Counter():

	def __init__(i,start,end,increment,type):

		# Note: Counter type documentation
			# forth_back
			# back_forth
			# fixed_increment
			# fixed_decrement

		i.start = start
		i.end   = end
		i.step  = increment

		if type == 'forth_back':
			i.counter = start
			i.status = 'increase'
			i.checker = 'on'

		elif type == 'back_forth':
			i.counter = end
			i.status = 'decrease'
			i.checker = 'on'

		elif type == 'fixed_increment':
			i.counter = start
			i.status = 'increase'
			i.checker = 'off'

		elif type == 'fixed_decrement':
			i.counter = end
			i.status = 'decrease'
			i.checker = 'off'

	def run(i):

		return_value = i.counter

		if   (i.counter <  i.end) and (i.status == 'increase'):
			
			if (i.counter + i.step > i.end)   : i.counter   = i.end
			else                              : i.counter  += i.step
	
		elif (i.counter == i.end) and (i.status == 'increase') and (i.checker == 'on'):
			i.status = 'decrease'
			i.counter  -= i.step

		elif (i.counter > i.start) and (i.status == 'decrease'): 
			
			if (i.counter - i.step < i.start) : i.counter = i.start
			else                              : i.counter -= i.step

		elif (i.counter == i.start) and (i.status == 'decrease') and (i.checker == 'on'):
			i.status = 'increase'
			i.counter += i.step


		return return_value

class Player(pygame.sprite.Sprite):

	def __init__(self):
		super().__init__()

		# Animation sequence
		self.img_list = [walk1_img,walk2_img,jump_img]
		self.img_switch = 0

		# Player default state
		self.image = walk1_img
		self.rect = walk1_img.get_rect(bottomleft=(30,300))
		self.radius = 38

		# Jump variables
		self.jump_loop = False
		self.jump_sound = press_aud
		self.jump_pos = 0 

	def jump(self):
 		if self.jump_loop == False:
 			self.jump_sound.play()
 			self.jump_loop = True
 			self.jump_pos = -9
       
	def update(self):
		if self.jump_loop == True:
			
			# Jump animation
			self.jump_pos += Object_Gravity
			self.rect.centery += self.jump_pos
			self.image = self.img_list[2]

			if (self.rect.bottom > 296): 
				self.rect.bottom = 300
				self.jump_loop = False
		else:

			# Waking Animation - switch between image[0] & image [1]
			self.img_switch += 0.08
			if self.img_switch >= 1.9: self.img_switch = 0 # Reset 
			
			self.image = self.img_list[int(self.img_switch)]

		#pygame.draw.circle(screen,'Red',self.rect.center,self.radius)
		#pygame.draw.rect(screen,'Red',self.rect)

class Obstacle(pygame.sprite.Sprite):

	def __init__(self,type):
		super().__init__()

		# Spawn snail or bird
		if type == "snail":
			self.img_list = [snail1_img,snail2_img]
			self.image = snail1_img
			self.rect = self.image.get_rect(bottomleft = (randint(830,1000),300))
			self.radius = (self.rect.width * 0.7)/2
		elif type == "bird":
			self.img_list = [bird1_img,bird2_img]
			self.image = bird1_img
			self.rect = self.image.get_rect(bottomleft = (randint(830,1000),200))
			self.radius = (self.rect.width * 0.7)/2

	def update(self):
		# Obstacle moving (-ve) x-axis
		self.rect.x -= Obstacle_Speed

		# Obstacle animation
		# See .case study to alternate "0" and "1" as x-position changes
		# << Snail >>
		if self.rect.bottom == 300:

			if int((self.rect.centerx/50)%2) == 0: self.image = self.img_list[0]
			else                                 : self.image = self.img_list[1]				
		
		# << Bird >>
		elif self.rect.bottom == 200: 
			
			if int((self.rect.centerx/100)%2) == 0: self.image = self.img_list[0]
			else                                  : self.image = self.img_list[1]

		# Delete onstacle if move out of screen
		if self.rect.right < 0:
			self.kill()

		#pygame.draw.circle(screen,'Blue',self.rect.center,self.radius)
		#pygame.draw.rect(screen,'Blue',self.rect)

def Audio():
	global press_aud, coin_aud, collide_aud, over_aud, game_aud, intro_aud, start_aud

	# AUDIO
	press_aud   = pygame.mixer.Sound('Resource/audio/button_pressed.mp3')
	coin_aud    = pygame.mixer.Sound('Resource/audio/coin.mp3')
	collide_aud = pygame.mixer.Sound('Resource/audio/collision.mp3')
	over_aud    = pygame.mixer.Sound('Resource/audio/game_over.mp3')
	game_aud    = pygame.mixer.Sound('Resource/audio/game_running.mp3')
	intro_aud   = pygame.mixer.Sound('Resource/audio/intro.mp3')
	start_aud   = pygame.mixer.Sound('Resource/audio/start_game.mp3')
def Font():
	global font_type1, font_type2

	# FONT STYLE
	font_type1 = pygame.font.Font("Resource/font/Pixeltype.ttf",50)
	font_type2 = pygame.font.Font("Resource/font/Arcade_Classic.ttf",40)
def Image():
	global sky_img, ground_img, bird1_img, bird2_img, game_over_img, go_img, ready_img, score_img
	global game_logo_img, walk1_img, walk2_img, jump_img, stand_img,snail1_img, snail2_img
	global intro_text1_img, intro_text2_img, over_text1_img

	# Background
	sky_img    = pygame.image.load('Resource/graphic/backgrd/sky.png').convert_alpha()
	ground_img = pygame.image.load('Resource/graphic/backgrd/ground.png').convert_alpha()

	# Bird
	bird1_img = pygame.image.load('Resource/graphic/bird/bird1.png').convert_alpha()
	bird2_img = pygame.image.load('Resource/graphic/bird/bird2.png').convert_alpha()

	# Effects
	game_over_img = pygame.image.load('Resource/graphic/effect/game_over.png').convert_alpha()
	go_img        = pygame.image.load('Resource/graphic/effect/go.png').convert_alpha()
	ready_img     = pygame.image.load('Resource/graphic/effect/ready.png').convert_alpha()
	score_img     = pygame.image.load('Resource/graphic/effect/score.png').convert_alpha()

	# Intro
	game_logo_img = pygame.image.load('Resource/graphic/intro/game_logo.png').convert_alpha()

	# Player
	walk1_img = pygame.image.load('Resource/graphic/player/walk1.png').convert_alpha()
	walk2_img = pygame.image.load('Resource/graphic/player/walk2.png').convert_alpha()
	jump_img  = pygame.image.load('Resource/graphic/player/jump.png').convert_alpha()
	stand_img = pygame.image.load('Resource/graphic/player/stand.png').convert_alpha()

	# Snail
	snail1_img = pygame.image.load('Resource/graphic/snail/snail1.png').convert_alpha()
	snail2_img = pygame.image.load('Resource/graphic/snail/snail2.png').convert_alpha()

	# Rendered
	intro_text1_img = font_type2.render("TO  PLAY",False,'White')
	intro_text2_img = font_type2.render("PRESS   SPACEBAR",False,'White')
	over_text1_img = font_type2.render("YOUR  SCORE",False,'White')
def Setup():
	global screen, clock, game, PRESS, SPACE, QUIT, BACKCOL,w,h
	global Object_Gravity, Start_Time, Spawn_Obstacle, Up_Difficulty

	pygame.init()
	clock = pygame.time.Clock()

	# SCREEN PROPERTIES
	w,h = 800,400
	screen = pygame.display.set_mode((w,h))
	pygame.display.set_caption("Pixel Runner")

	# ASSET
	Audio()
	Font()
	Image()

	# SHORT CUTS
	PRESS = pygame.KEYDOWN
	SPACE = pygame.K_SPACE
	QUIT = pygame.QUIT
	BACKCOL = (34,62,108)

	# FIXED GLOBAL VARIABLE
	Object_Gravity = 0.27
	Start_Time = 0

	# CUSTOM EVENT TIMER
	Spawn_Obstacle = pygame.USEREVENT + 1
	Up_Difficulty = pygame.USEREVENT + 2

	# OTHERS
	# -- As time increases, make the game more difficult 
	# -- Every 50,000 millisecond, make obstacle spawn faster & move quicker
	pygame.time.set_timer(Up_Difficulty,40000)

	# INITIALIZE GAME
	game = Intro()


#---------------------------------------------------------------------
Setup()

while True:

	game.run()
	
	clock.tick(60)
	pygame.display.flip()



