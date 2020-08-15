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
				
def check_events(ai_settings, screen, stats, play_button, sb, ship, aliens, bullets):
	if stats.game_pause:
		stats.game_pause = False
		pygame.event.clear()  # 不响应中止期间的事件
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
		elif event.type == pygame.KEYDOWN:
			check_keydown_event(event, ai_settings, screen, ship, bullets)
		elif event.type == pygame.KEYUP:
			check_keyup_event(event, ship)
		elif event.type == pygame.MOUSEBUTTONDOWN:
			mouse_x, mouse_y = pygame.mouse.get_pos()
			check_play_button(ai_settings, screen, stats, play_button, sb, ship, aliens, bullets, mouse_x, mouse_y)

def check_play_button(ai_settings, screen, stats, play_button, sb, ship, aliens, bullets, mouse_x, mouse_y):
	button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
	if button_clicked and not stats.game_active:
		ai_settings.initialize_dynamic_settings()
		pygame.mouse.set_visible(False)
		stats.game_active = True
		# 重置游戏统计信息
		stats.reset_stats()
		sb.prep_score()
		sb.prep_record_score()
		sb.prep_level()
		sb.prep_ships()

		# 清空外星人列表和子弹列表
		bullets.empty()
		aliens.empty()
		# 创建一群新的外星人，并让飞船居中
		create_fleet(ai_settings, screen, ship, aliens)
		ship.center_ship()

				
def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button):
	screen.fill(ai_settings.bg_color)
	ship.blitme()
	# alien.blitme()
	# pygame.sprite.Group.draw：Draws the contained Sprites to the Surface argument.
	# The Group does not keep sprites in any order, so the draw order is arbitrary.
	aliens.draw(screen)
	# Group中的sprites()方法
	# return a list of all the Sprites this group contains.
	# 也就是得到每一个bullet对象
	for bullet in bullets.sprites():
		bullet.draw_bullet()
	# 显示得分
	sb.show_score()
	if not stats.game_active:
		play_button.draw_button()
	# pygame.display.flip()
	# update() is like an optimized version of flip() for software displays.
	pygame.display.update()

def check_high_score(stats, sb):
	if stats.score > stats.high_score:
		stats.high_score = stats.score
		sb.prep_record_score()

def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets):
	# collisions is a dict，发生碰撞的子弹是字典中的一个键，
	# 而与每颗子弹相关的值是一个列表，其中包含该子弹撞到的外星人
	# 每个值都是一个列表，包含被同一颗子弹击落的所有外星人，如：
	# {'子弹A':[外星人1，外星人2，...], '子弹B':[外星人1，外星人2，...],...}
	collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
	# print(collisions.keys(), collisions.values())
	if collisions:
		for aliens in collisions.values():
			stats.score += ai_settings.alien_points * len(aliens)
			sb.prep_score()
		check_high_score(stats, sb)

	if 0 == len(aliens):
		bullets.empty()
		stats.level += 1
		sb.prep_level()
		ai_settings.increase_speed()
		create_fleet(ai_settings, screen, ship, aliens)

def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets):
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
	check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets)

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

def ship_hit(ai_settings, stats, sb, screen, ship, aliens, bullets):
	if stats.ships_left > 0:
		stats.ships_left -= 1
		sb.prep_ships()
		bullets.empty()
		aliens.empty()
		create_fleet(ai_settings, screen, ship, aliens)
		ship.center_ship()
		stats.game_pause = True
		sleep(1)
	else:
		stats.game_active = False
		sb.store_record()
		pygame.mouse.set_visible(True)


def check_aliens_bottom(ai_settings, stats, sb, screen, ship, aliens, bullets):
	screen_rect = screen.get_rect()
	for alien in aliens.sprites():
		if alien.rect.bottom >= screen_rect.bottom:
			ship_hit(ai_settings, stats, sb, screen, ship, aliens, bullets)
			break

def update_aliens(ai_settings, stats, sb, screen, ship, aliens, bullets):
	'''更新所有外星人的位置'''
	check_fleet_edges(ai_settings, aliens)
	aliens.update()

	if pygame.sprite.spritecollideany(ship, aliens, pygame.sprite.collide_mask):
		ship_hit(ai_settings, stats, sb, screen, ship, aliens, bullets)

	check_aliens_bottom(ai_settings, stats, sb, screen, ship, aliens, bullets)
