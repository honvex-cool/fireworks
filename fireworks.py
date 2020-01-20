import random
import pygame
import math


class Display(object):


    EXISTS = False

    def __init__(self, width=0, height=0, firework_interval=1.0, tps=30):
        if Display.EXISTS:
            raise Exception()
        Display.EXISTS = True
        pygame.init()

        pygame.display.set_caption("Fireworks!")
        self.screen = pygame.display.set_mode((width, height), pygame.FULLSCREEN)
        screen_info = pygame.display.Info()
        self.width = screen_info.current_w
        self.height = screen_info.current_h

        self.fireworks = []
        self.tps = tps

        self.firework_interval = firework_interval
        self.time_since_last_firework = 0
        self.running = True
    
    def __del__(self):
        pygame.quit()
        Display.EXISTS = False
    
    def play(self):
        clock = pygame.time.Clock()
        while self.running:
            delta_time = clock.tick(self.tps) / 1000.0
            self.update(delta_time)
            self.draw(delta_time)
            pygame.display.update()

    def update(self, dt):
        self.handle_events()
        self.add_firework(dt)
        self.update_fireworks()
        self.remove_finished_fireworks()

    def draw(self, dt):
        self.screen.fill((0, 0, 0))
        for firework in self.fireworks:
            firework.draw(self.screen)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                self.running = False
                break

    def add_firework(self, dt):
        self.time_since_last_firework += dt
        while self.time_since_last_firework >= self.firework_interval:
            self.fireworks.append(Firework(self.width, self.height))
            self.time_since_last_firework -= self.firework_interval

    def update_fireworks(self):
        for firework in self.fireworks:
            firework.update()

    def remove_finished_fireworks(self):
        new_fireworks = []
        for firework in self.fireworks:
            if not firework.has_finished():
                new_fireworks.append(firework)
        self.fireworks = new_fireworks
        if len(self.fireworks) > 10:
            print("Red alert! Save my GPU!")


class Firework(object):
    

    MIN_WIDTH = 1
    MAX_WIDTH = 5

    MIN_RAYS = 5
    MAX_RAYS = 10

    SCALE_CHANGE = 2
    WIDTH_CHANGE_CYCLE_LENGTH = 50

    def __init__(self, display_width, display_height):
        self.x = random.randint(0, display_width)
        self.y = random.randint(0, display_height)

        self.width = random.randint(Firework.MIN_WIDTH, Firework.MAX_WIDTH)
        self.layers = 5
        self.rays = random.randint(Firework.MIN_RAYS, Firework.MAX_RAYS)
        self.angle_between_rays = 2 * math.pi / self.rays
        
        self.color = (random.randrange(256), random.randrange(256), random.randrange(256))
        
        self.scale = 0

    def has_finished(self):
        return self.width <= 0

    def draw(self, screen):
        for layer in range(1, self.layers + 1):
            for ray in range(self.rays):
                angle = self.ray_angle(ray, layer)
                x_offset, y_offset = self.dot_offsets(angle, layer)
                center = (int(self.x + x_offset), int(self.y + y_offset))
                pygame.draw.circle(screen, self.color, center, self.width)

    def update(self):
        self.scale += Firework.SCALE_CHANGE
        if self.scale % (Firework.SCALE_CHANGE * Firework.WIDTH_CHANGE_CYCLE_LENGTH) == 0:
            self.width -= 1

    def ray_angle(self, ray_index, layer):
        return self.angle_between_rays * (ray_index + (layer % 2) * 0.5)

    def dot_offsets(self, angle, layer):
        coefficient = layer * self.scale / self.layers
        return math.cos(angle) * coefficient, math.sin(angle) * coefficient

