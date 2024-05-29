import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Game settings
GRAVITY = 0.25
FLAP_POWER = -6.5
PIPE_GAP = 200  # Increase the gap between pipes
PIPE_WIDTH = 80
PIPE_HEIGHT = 500
PIPE_VELOCITY = -4
INITIAL_PIPE_DELAY = 100  # Delay before the first pipe appears
PIPE_INTERVAL = 300  # Increase the distance between pipes

# Load images
BIRD_IMAGE = pygame.image.load("bird.png")
BACKGROUND_IMAGE = pygame.image.load("background.png")
PIPE_IMAGE = pygame.image.load("pipe.png")
BASE_IMAGE = pygame.image.load("base.png")

# Scale images
BIRD_IMAGE = pygame.transform.scale(BIRD_IMAGE, (34, 24))
PIPE_IMAGE = pygame.transform.scale(PIPE_IMAGE, (PIPE_WIDTH, PIPE_HEIGHT))
BASE_IMAGE = pygame.transform.scale(BASE_IMAGE, (SCREEN_WIDTH, 112))

# Screen setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird Clone")

# Clock for controlling frame rate
clock = pygame.time.Clock()

class Bird:
    def __init__(self):
        self.image = BIRD_IMAGE
        self.x = 50
        self.y = SCREEN_HEIGHT // 2
        self.y_velocity = 0
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def update(self):
        self.y_velocity += GRAVITY
        self.y += self.y_velocity
        self.rect.y = self.y

    def flap(self):
        self.y_velocity = FLAP_POWER

    def draw(self):
        screen.blit(self.image, self.rect.topleft)

class Pipe:
    def __init__(self):
        self.x = SCREEN_WIDTH
        self.height = random.randint(150, 450)
        self.top_pipe = pygame.transform.flip(PIPE_IMAGE, False, True)
        self.bottom_pipe = PIPE_IMAGE
        self.passed = False
        self.top_rect = self.top_pipe.get_rect(midbottom=(self.x, self.height - PIPE_GAP // 2))
        self.bottom_rect = self.bottom_pipe.get_rect(midtop=(self.x, self.height + PIPE_GAP // 2))

    def update(self):
        self.x += PIPE_VELOCITY
        self.top_rect.x = self.x
        self.bottom_rect.x = self.x

    def draw(self):
        screen.blit(self.top_pipe, self.top_rect.topleft)
        screen.blit(self.bottom_pipe, self.bottom_rect.topleft)

def check_collision(bird, pipes):
    for pipe in pipes:
        if bird.rect.colliderect(pipe.top_rect) or bird.rect.colliderect(pipe.bottom_rect):
            return True
    if bird.rect.top <= 0 or bird.rect.bottom >= SCREEN_HEIGHT - BASE_IMAGE.get_height():
        return True
    return False

def main():
    running = True
    bird = Bird()
    pipes = []
    base_x = 0
    score = 0
    font = pygame.font.SysFont(None, 55)
    frame_count = 0  # Counter to manage the delay for the first pipe

    while running:
        screen.blit(BACKGROUND_IMAGE, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird.flap()

        bird.update()

        if frame_count > INITIAL_PIPE_DELAY and (not pipes or pipes[-1].x < SCREEN_WIDTH - PIPE_INTERVAL):
            pipes.append(Pipe())

        for pipe in pipes:
            pipe.update()
            pipe.draw()
            if pipe.x + PIPE_WIDTH < 0:
                pipes.remove(pipe)
            if not pipe.passed and pipe.x < bird.x:
                pipe.passed = True
                score += 1

        screen.blit(BASE_IMAGE, (base_x, SCREEN_HEIGHT - BASE_IMAGE.get_height()))
        base_x -= 4
        if base_x <= -SCREEN_WIDTH:
            base_x = 0

        bird.draw()

        if check_collision(bird, pipes):
            running = False

        score_text = font.render(str(score), True, WHITE)
        screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 50))

        pygame.display.update()
        clock.tick(60)
        frame_count += 1 

    pygame.quit()

if __name__ == "__main__":
    main()
 