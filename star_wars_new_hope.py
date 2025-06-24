import pygame
import sys
import random

pygame.init()

# === Инициализация аудио ===
pygame.mixer.music.load('sounds/John Williams - Main Theme ( OST _Звёздные войны_) (online-audio-converter.com).ogg')
pygame.mixer.music.play(-1) # Играть вечно

pygame.mouse.set_visible(False)  # Полностью скрываем системный курсор

screen_width, screen_height = 1920, 1080
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Новая надежда")
clock = pygame.time.Clock()

# Загрузка изображений
try:
    starship = pygame.image.load('img/x-wing.png').convert_alpha()
    starship = pygame.transform.scale(starship, (150, 150))

    enemy_img = pygame.image.load('img/sid_enemy.png').convert_alpha()
    enemy_img = pygame.transform.scale(enemy_img, (100, 80))

    red_laser = pygame.image.load('img/player_laser.png').convert_alpha()
    red_laser = pygame.transform.scale(red_laser, (80, 70))

    green_laser = pygame.image.load('img/Green_Laser.png').convert_alpha()
    green_laser = pygame.transform.scale(green_laser, (80, 90))

    try:
        background = pygame.image.load('img/star_death.jpg').convert()
        print(f"Фон загружен. Оригинальный размер: {background.get_size()}")
        background = pygame.transform.smoothscale(background, (screen_width, screen_height))
        print(f"Фон масштабирован до: {background.get_size()}")
    except Exception as e:
        print(f"Ошибка загрузки фона: {e}")
        background = None

    explosion_img = pygame.image.load('img/explosion_sid.png').convert_alpha()
    explosion_img = pygame.transform.scale(explosion_img, (100, 100))

    # Система очков
    score = 0
    font = pygame.font.SysFont('Arial', 36)

    # При уничтожении врага:
    score += 100

    # В отрисовке:
    score_text = font.render(f"Очки: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

except Exception as e:
    print(f"Ошибка загрузки изображений: {e}")
    sys.exit()

# Параметры оружия врагов
ENEMY_GUN_OFFSET = 20  # Отступ от краёв корабля врага

# Инициализация игрока
player_x = (screen_width - starship.get_width()) // 2
player_y = screen_height - starship.get_height() - 10
player_speed = 5
player_lasers = []
laser_speed = 10
player_health = 100

# Инициализация врагов
enemies = []
enemy_speed = 2
enemy_spawn_timer = 0
enemy_spawn_delay = 60  # 1 враг в секунду (60 FPS)

# Лазеры врагов
enemy_lasers = []
enemy_laser_speed = 7  # Быстрее, чем у игрока
enemy_shoot_timer = 0
enemy_shoot_delay = 90  # 1.5 секунды между залпами

# Система взрывов
explosions = [] # Каждый элемент: [x, y, текущий_радиус]

game_over = False


def spawn_enemy():
    x = random.randint(50, screen_width - 50 - enemy_img.get_width())
    y = random.randint(-100, -40)  # Появляются выше экрана
    enemies.append([x, y])
    print(f"Создан враг на позиции ({x}, {y}). Всего врагов: {len(enemies)}")

def enemy_shoot():
    if not enemies:
        return

    for enemy in enemies:
        if enemy[1] > 0 and random.random() < 0.015: # 1.5% шанс выстрела
            # Координаты двух точек выстрела (по бокам врага)
            left_gun_x = enemy[0] + ENEMY_GUN_OFFSET # Левый ствол
            right_gun_x = enemy[0] + enemy_img.get_width() - ENEMY_GUN_OFFSET - green_laser.get_width() # Правый ствол
            gun_y = enemy[1] + enemy_img.get_height()

            # Создаём два лазера
            enemy_lasers.append([left_gun_x, gun_y])
            enemy_lasers.append([right_gun_x, gun_y])

            print("Враг выстрелил двойным залпом!")  # Для отладки

while not game_over:
    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: # Левая кнопка мыши
                # Выстрел игрока - два лазера
                player_lasers.append([player_x + 10, player_y - red_laser.get_height()])
                player_lasers.append([player_x + 30, player_y - red_laser.get_height()])
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                game_over = True

    # Получаем позицию мыши и устанавливаем центр корабля на курсор
    mouse_x, mouse_y = pygame.mouse.get_pos()
    player_x = mouse_x - starship.get_width() // 2
    player_y = mouse_y - starship.get_height() // 2

    # Ограничиваем движение в пределах экрана
    player_x = max(0, min(player_x, screen_width - starship.get_width()))
    player_y = max(0, min(player_y, screen_height - starship.get_height()))

    # Спавн врагов
    enemy_spawn_timer += 1
    if enemy_spawn_timer >= enemy_spawn_delay:
        spawn_enemy()
        enemy_spawn_timer = 0

    # Стрельба врагов
    enemy_shoot()

    # Движение лазеров игрока
    for laser in player_lasers[:]:
        laser[1] -= laser_speed
        if laser[1] < 0:
            player_lasers.remove(laser)

    player_rect = pygame.Rect(player_x, player_y, starship.get_width(), starship.get_height())
    # Проверка попаданий лазеров игрока во врагов
    for laser in player_lasers[:]:
        laser_rect = pygame.Rect(laser[0], laser[1], red_laser.get_width(), red_laser.get_height())

        for enemy in enemies[:]:
            enemy_rect = pygame.Rect(enemy[0], enemy[1], enemy_img.get_width(), enemy_img.get_height())

            if laser_rect.colliderect(enemy_rect):
                if laser in player_lasers:
                    player_lasers.remove(laser)
                if enemy in enemies:
                    # Добавляем взрыв в список вместо непосредственной отрисовки
                    explosions.append([enemy[0]+25, enemy[1]+25, 5]) # [x, y, начальный_радиус]
                    enemies.remove(enemy)
                    score += 10
                print("Враг уничтожен!")
                break

    # Движение лазеров врагов (ИСПРАВЛЕНО: теперь летят ВНИЗ)
    for laser in enemy_lasers[:]:
        laser[1] += enemy_laser_speed  # Было -=, теперь +=
        if laser[1] > screen_height:
            enemy_lasers.remove(laser)

    for laser in enemy_lasers[:]:
        laser_rect = pygame.Rect(laser[0], laser[1], green_laser.get_width(), green_laser.get_height())

        if player_rect.colliderect(laser_rect):
            enemy_lasers.remove(laser)
            print("Попадание по игроку!")
            # Здесь можно добавить систему здоровья:
            player_health -= 1
            if player_health <= 0: game_over = True

    # Движение врагов
    for enemy in list(enemies):
        enemy[1] += enemy_speed * 0.5 # Уменьшаем скорость вертикального движения

        # Плавное горизонтальное движение с инерцией
        if 'dx' not in enemy:
            enemy.append(0) # enemy[2] - горизонтальная скорость
        enemy[0] += enemy[2]

        # Случайное изменение направления
        if random.random() < 0.02: # 2% шанс изменить направление
            enemy[2] = random.choice([-1, 0, 1]) * enemy_speed

        # Удержание в границах экрана
        if enemy[0] < 0:
            enemy[0] = 0
            enemy[2] *= -0.5 # Отскок от границы
        elif enemy[0] > screen_width - enemy_img.get_width():
            enemy[0] = screen_width - enemy_img.get_width()
            enemy[2] *= -0.5

        # Удаление вышедших за пределы
        if enemy[1] > screen_height + 50:
            enemies.remove(enemy)
            print("Враг удалён (вышел за экран)")

    # Отрисовка

    if background:
        screen.blit(background, (0, 0))  # Сначала рисуем фон
    else:
        screen.fill((0, 0, 0))  # Фолбэк на чёрный фон

    # 2. Лазеры врагов (под кораблями)
    for laser in enemy_lasers:
        screen.blit(green_laser, (laser[0], laser[1]))

    # 3. Враги
    for enemy in enemies:
        screen.blit(enemy_img, (enemy[0], enemy[1]))

    # 4. Взрывы (после врагов, но под игроком)
    for explosion in explosions[:]: # Делаем копию списка для безопасного удаления
        if explosion_img:
            # Отрисовываем изображение взрыва
            screen.blit(explosion_img, (explosion[0]-25, explosion[1]-25))
        else:
            # Фолбэк на жёлтый круг
            pygame.draw.circle(screen, (255, 200, 0), (explosion[0], explosion[1]), explosion[2])
        explosion[2] += 1 # Увеличиваем радиус взрыва
        if explosion[2] > 30: # Удаляем старые взрывы
            explosions.remove(explosion)

        # 5. Игрок (поверх взрывов)
    screen.blit(starship, (player_x, player_y))

    # 6. Лазеры игрока (поверх кораблей)
    for laser in player_lasers:
        screen.blit(red_laser, (laser[0], laser[1]))

    # 7. Интерфейс (очки, здоровье)
    score_text = font.render(f"Очки: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

    health_text = font.render(f"Здоровье: {player_health}", True, (255, 255, 255))
    screen.blit(health_text, (10, 50))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()