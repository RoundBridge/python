import sys
import pygame

from bullet import Bullet
from alien import Alien

def check_keydown_event(event, ai_settings, screen, ship, bullets):
	if event.key == pygame.K_RIGHT:
		ship.moving_right = True
	elif event.key == pygame.K_LEFT:
		ship.moving_left = True
	elif event.key == pygame.K_SPACE:
		fire_bullet(ai_settings, screen, ship, bullets)
		
def check_keyup_event(event, ship):
	if event.key == pygame.K_RIGHT:
		ship.moving_right = False
	elif event.key == pygame.K_LEFT:
		ship.moving_left = False
	elif event.key == pygame.K_q:
		sys.exit()
				
def check_events(ai_settings, screen, ship, bullets):
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
		elif event.type == pygame.KEYDOWN:
			check_keydown_event(event, ai_settings, screen, ship, bullets)				
		elif event.type == pygame.KEYUP:
			check_keyup_event(event, ship)
				
def update_screen(ai_settings, screen, ship, aliens, bullets):
	screen.fill(ai_settings.bg_color)

	# Group中的sprites()方法
	# return a list of all the Sprites this group contains.
	# 也就是得到每一个bullet对象
	for bullet in bullets.sprites():
		bullet.draw_bullet()
		
	ship.blitme()
	#alien.blitme()
	aliens.draw(screen)  # 参数screen表示绘制到screen上？
	pygame.display.flip()

def update_bullets(bullets):
	# 这个update调用了Bullet类中的update方法
	# Bullet类中的update方法重写了Sprite类中的update方法
	# 原本的Sprite类中的update方法什么也不做，这里在Bullet类中给它赋予了新功能
	# bullets是个容器，即Group，容器中的每个元素都是Bullet类的对象，即子弹
	# Bullet类继承自Sprite类，所以每个子弹都继承了update方法
	# bullets.update()自动对容器中的每个元素执行update方法，也即对每个bullet执行了update方法
	bullets.update()

	for bullet in bullets.copy():
		if bullet.rect.bottom <= 0:
			bullets.remove(bullet)
	#print(len(bullets))	

def fire_bullet(ai_settings, screen, ship, bullets):
	#print(len(bullets))
	if len(bullets) < ai_settings.bullets_allowed:
		new_bullet = Bullet(ai_settings, screen, ship)
		bullets.add(new_bullet)  # 在这个空编组中加入new_bullet

def create_fleet(ai_settings, screen, aliens):
	alien = Alien(ai_settings, screen)
	alien_width = alien.rect.width
	available_space_x = ai_settings.screen_width - 2 * alien_width
	number_aliens_x = int(available_space_x / (2 * alien_width))

	for alien_number in range(number_aliens_x):
		alien = Alien(ai_settings, screen)
		alien.x = alien_width + 2 * alien_width * alien_number
		alien.rect.x = alien.x
		aliens.add(alien)  # 在这个空编组中加入alien对象

