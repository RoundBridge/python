import sys
import pygame

from bullet import Bullet
from alien import Alien
from time import sleep

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
	# alien.blitme()
	# pygame.sprite.Group.draw：Draws the contained Sprites to the Surface argument.
	# The Group does not keep sprites in any order, so the draw order is arbitrary.
	aliens.draw(screen)
	pygame.display.flip()

def check_bullet_alien_collisions(ai_settings, screen, ship, aliens, bullets):
	# collisions is a dict，包含了发生碰撞的子弹和外星人，键是子弹，值是外星人
	collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
	# print(collisions.keys(), collisions.values())
	if 0 == len(aliens):
		bullets.empty()
		create_fleet(ai_settings, screen, ship, aliens)

def update_bullets(ai_settings, screen, ship, aliens, bullets):
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
	# print(len(bullets))
	check_bullet_alien_collisions(ai_settings, screen, ship, aliens, bullets)

def fire_bullet(ai_settings, screen, ship, bullets):
	#print(len(bullets))
	if len(bullets) < ai_settings.bullets_allowed:
		new_bullet = Bullet(ai_settings, screen, ship)
		bullets.add(new_bullet)  # 在这个空编组中加入new_bullet

def get_number_aliens_x(ai_settings, alien_width):
	'''获取屏幕中一行能容纳多少外星人'''
	available_space_x = ai_settings.screen_width - 2 * alien_width
	number_aliens_x = int(available_space_x / (2 * alien_width))
	return number_aliens_x

def get_number_rows(ai_settings, ship_height, alien_height):
	'''获取屏幕中能容纳多少行外星人'''
	available_space_y = ai_settings.screen_height - alien_height / 2 - ship_height
	number_rows = int(available_space_y / (2 * alien_height))

	# print('screen_height: ', ai_settings.screen_height)
	# print('alien_height: ', alien_height)
	# print('ship_height: ', ship_height)
	# print('available_space_y: ', available_space_y)
	# print('number_rows: ', number_rows)

	return number_rows

def create_alien(ai_settings, screen, aliens, alien_number, row_number):
	'''创建一个外星人，并将其加入到编组中'''
	alien = Alien(ai_settings, screen)
	alien_width = alien.rect.width
	alien_height = alien.rect.height
	alien.x = alien_width + 2 * alien_width * alien_number
	alien.rect.x = alien.x
	# 行与行之间的间隔设成半个外星人高度
	alien.y = row_number * alien_height * 3 / 2 + alien_height / 2
	alien.rect.y = alien.y
	aliens.add(alien)

def create_fleet(ai_settings, screen, ship, aliens):
	alien = Alien(ai_settings, screen)
	number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
	number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)

	for row_number in range(number_rows):
		for alien_number in range(number_aliens_x):
			create_alien(ai_settings, screen, aliens, alien_number, row_number)

def change_fleet_direction(ai_settings):
	ai_settings.fleet_direction *= -1  # 用"*="的方式，一个函数既可以将方向改成向左，也可以改成向右

def check_fleet_edges(ai_settings, aliens):
	for alien in aliens.sprites():  # 由于Group中的元素是无序存放的，故这里需要每个都检查
		if alien.check_edges():
			change_fleet_direction(ai_settings)
			break  # 只要有一个碰到边缘就可以停止检测了

def ship_hit(ai_settings, stats, screen, ship, aliens, bullets):
	if stats.ships_left > 0:
		stats.ships_left -= 1
		bullets.empty()
		aliens.empty()
		create_fleet(ai_settings, screen, ship, aliens)
		ship.center_ship()
		sleep(1)
	else:
		stats.game_active = False


def check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets):
	screen_rect = screen.get_rect()
	for alien in aliens.sprites():
		if alien.rect.bottom >= screen_rect.bottom:
			ship_hit(ai_settings, stats, screen, ship, aliens, bullets)
			break

def update_aliens(ai_settings, stats, screen, ship, aliens, bullets):
	'''更新所有外星人的位置'''
	check_fleet_edges(ai_settings, aliens)
	aliens.update()

	if pygame.sprite.spritecollideany(ship, aliens):
		ship_hit(ai_settings, stats, screen, ship, aliens, bullets)

	check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets)
