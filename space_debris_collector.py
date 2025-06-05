import pygame
import random
import math
import asyncio
import platform

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Debris Collector")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Player settings
PLAYER_SIZE = 40
player_pos = [WIDTH // 2, HEIGHT - 60]
player_speed = 5
player_angle = 0

# Debris and obstacle settings
DEBRIS_SIZE = 10
OBSTACLE_SIZE = 20
debris_list = []
obstacles = []
DEBRIS_SPAWN_RATE = 0.02
OBSTACLE_SPAWN_RATE = 0.01

# Game variables
score = 0
font = pygame.font.SysFont("arial", 24)
clock = pygame.time.Clock()
FPS = 60

class Debris:
    def __init__(self):
        self.x = random.randint(0, WIDTH)
        self.y = 0
        self.speed = random.uniform(2, 5)

    def move(self):
        self.y += self.speed
        return self.y < HEIGHT

    def draw(self):
        pygame.draw.circle(screen, GREEN, (int(self.x), int(self.y)), DEBRIS_SIZE)

class Obstacle:
    def __init__(self):
        self.x = random.randint(0, WIDTH)
        self.y = 0
        self.speed = random.uniform(3, 6)

    def move(self):
        self.y += self.speed
        return self.y < HEIGHT

    def draw(self):
        pygame.draw.circle(screen, RED, (int(self.x), int(self.y)), OBSTACLE_SIZE)

def draw_player():
    # Simple triangular spaceship
    points = [
        (player_pos[0], player_pos[1] - PLAYER_SIZE // 2),  # Top
        (player_pos[0] - PLAYER_SIZE // 2, player_pos[1] + PLAYER_SIZE // 2),  # Bottom left
        (player_pos[0] + PLAYER_SIZE // 2, player_pos[1] + PLAYER_SIZE // 2)  # Bottom right
    ]
    rotated_points = []
    for x, y in points:
        # Rotate points around player center
        x -= player_pos[0]
        y -= player_pos[1]
        new_x = x * math.cos(math.radians(player_angle)) - y * math.sin(math.radians(player_angle))
        new_y = x * math.sin(math.radians(player_angle)) + y * math.cos(math.radians(player_angle))
        rotated_points.append((new_x + player_pos[0], new_y + player_pos[1]))
    pygame.draw.polygon(screen, WHITE, rotated_points)

def check_collision(pos1, size1, pos2, size2):
    distance = math.hypot(pos1[0] - pos2[0], pos1[1] - pos2[1])
    return distance < (size1 + size2) / 2

async def main():
    global score, player_angle
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Player movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_pos[0] > PLAYER_SIZE // 2:
            player_pos[0] -= player_speed
        if keys[pygame.K_RIGHT] and player_pos[0] < WIDTH - PLAYER_SIZE // 2:
            player_pos[0] += player_speed
        if keys[pygame.K_UP] and player_pos[1] > PLAYER_SIZE // 2:
            player_pos[1] -= player_speed
        if keys[pygame.K_DOWN] and player_pos[1] < HEIGHT - PLAYER_SIZE // 2:
            player_pos[1] += player_speed
        if keys[pygame.K_a]:
            player_angle += 5
        if keys[pygame.K_d]:
            player_angle -= 5

        # Spawn debris and obstacles
        if random.random() < DEBRIS_SPAWN_RATE:
            debris_list.append(Debris())
        if random.random() < OBSTACLE_SPAWN_RATE:
            obstacles.append(Obstacle())

        # Update debris
        debris_list[:] = [d for d in debris_list if d.move()]
        for d in debris_list[:]:
            if check_collision(player_pos, PLAYER_SIZE, [d.x, d.y], DEBRIS_SIZE):
                debris_list.remove(d)
                score += 10

        # Update obstacles
        obstacles[:] = [o for o in obstacles if o.move()]
        for o in obstacles:
            if check_collision(player_pos, PLAYER_SIZE, [o.x, o.y], OBSTACLE_SIZE):
                running = False

        # Draw everything
        screen.fill(BLACK)
        for d in debris_list:
            d.draw()
        for o in obstacles:
            o.draw()
        draw_player()
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))
        pygame.display.flip()
        clock.tick(FPS)
        await asyncio.sleep(1.0 / FPS)

    pygame.quit()

if platform.system() == "Emscripten":
    asyncio.ensure_future(main())
else:
    if __name__ == "__main__":
        asyncio.run(main())
