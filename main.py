import pygame
from pygame.locals import *
import random
from math import sqrt

pygame.init()

class Boid(pygame.sprite.Sprite):
    def __init__(self, x_loc, y_loc, window_x, window_y, radius = 3, speed = 2, color = (0,0,0)) -> None:
        super().__init__()
        self.x_loc: float = x_loc
        self.y_loc: float = y_loc
        self.radius: float = radius
        self.speed: float = speed
        self.max_perception: float = 20
        self.alignment_force_multiplier: float = 0.6
        self.cohesion_force_multiplier: float = 0.6
        self.separation_force_multiplier: float = 0.8
        self.window_x = window_x
        self.window_y = window_y
        self.x_destination, self.y_destination = self.select_first_destionation(window_x,window_y)
        self.x_velocity, self.y_velocity = self.select_first_velocity()
        self.x_desired_velocity = self.x_velocity
        self.y_desired_velocity = self.y_velocity
        self.image = pygame.Surface((radius*2, radius*2), flags=pygame.SRCALPHA)
        self.color = color
        pygame.draw.circle(self.image, self.color, (radius,radius), radius)

    def draw(self, surface):
        surface.blit(self.image,(self.x_loc, self.y_loc))

    def select_first_velocity(self) -> tuple[float,float]:
        x_velocity = random.uniform(-1.0, 1.0)
        y_velocity = random.uniform(-1.0, 1.0)
        x_velocity, y_velocity = self.calculate_magnitude(x_velocity, y_velocity)
        # print(x_velocity)
        # print(y_velocity)
        # print('___')
        return x_velocity, y_velocity

    def select_first_destionation(self, window_x, window_y) -> tuple[float,float]:
        x_destination = window_x * random.random()
        y_destination = window_y * random.random()
        # print(x_destination)
        # print(y_destination)
        # print('___')
        return x_destination, y_destination

    def calculate_velocity(self, sprite_group, edges=False):
        x_alignment_force, y_alignment_force = self.alignment(sprite_group)
        x_cohesion_force, y_cohesion_force = self.cohesion(sprite_group)
        x_separation_force, y_separation_force = self.separation(sprite_group)
        edge_check = self.check_edge(edges)
        if edge_check:
            self.x_desired_velocity = self.x_desired_velocity * self.speed
            self.y_desired_velocity = self.y_desired_velocity * self.speed
        if not edge_check:
            self.x_desired_velocity = (self.x_desired_velocity + x_alignment_force + x_cohesion_force + x_separation_force)
            self.y_desired_velocity = (self.y_desired_velocity + y_alignment_force + y_cohesion_force + y_separation_force)
        edge_check = False
        self.x_desired_velocity, self.y_desired_velocity = self.calculate_magnitude(self.x_desired_velocity, self.y_desired_velocity)

    def move(self):
        self.x_velocity = self.x_desired_velocity
        self.y_velocity = self.y_desired_velocity
        self.x_loc = self.x_velocity * self.speed + self.x_loc
        self.y_loc = self.y_velocity * self.speed + self.y_loc

    def check_edge(self, edges=False) -> bool:
        if edges is False:
            if self.x_loc > self.window_x:
                self.x_loc = 0
            if self.x_loc < 0:
                self.x_loc = self.window_x
            if self.y_loc > self.window_y:
                self.y_loc = 0
            if self.y_loc < 0:
                self.y_loc = self.window_y
        if edges is True:
            avoid_distance = 40
            turn_speed = 0.05
            if self.x_loc >= self.window_x-self.radius*2 - avoid_distance:
                self.x_desired_velocity = self.x_desired_velocity - turn_speed
                return True
            if self.x_loc <= 0 + avoid_distance:
                self.x_desired_velocity = self.x_desired_velocity + turn_speed
                return True
            if self.y_loc >= self.window_y-self.radius*2 - avoid_distance:
                self.y_desired_velocity = self.y_desired_velocity - turn_speed
                return True
            if self.y_loc <= 0 + avoid_distance:
                self.y_desired_velocity = self.y_desired_velocity + turn_speed
                return True
        return False

    def calculate_magnitude(self,x_adjust, y_adjust) -> tuple[float, float]: 
        movement_magnitude: float = sqrt((self.x_loc-self.x_loc+x_adjust)**2+(self.y_loc-self.y_loc+y_adjust)**2)
        movement_magnitude = self.magnitude_adjustment(movement_magnitude)
        if movement_magnitude > 0.0:
            x_velocity: float = (self.x_loc-self.x_loc+x_adjust) / movement_magnitude
            y_velocity: float = (self.y_loc-self.y_loc+y_adjust) / movement_magnitude
        if movement_magnitude == 0.0:
            x_velocity = 0.0
            y_velocity = 0.0
        return x_velocity, y_velocity

    def magnitude_adjustment(self, movement_magnitude: float) -> float:
        minimum_magnitude = 0.05
        if movement_magnitude < minimum_magnitude:
            return 0.0
        return movement_magnitude

    def alignment(self, sprite_group) -> tuple[float,float]:
        x_velocities: list[float] = []
        y_velocities: list[float] = []
        
        for sprite in sprite_group:
            if sprite is not self:
                distance = sqrt((self.x_loc - sprite.x_loc)**2 + (self.y_loc - sprite.y_loc)**2)
                if distance <= self.max_perception:
                    x_velocities.append(sprite.x_velocity)
                    y_velocities.append(sprite.y_velocity)


        if len(x_velocities) == 0:
            return 0.0, 0.0
        
        x_average_speed: float = sum(x_velocities)/len(x_velocities)
        y_average_speed: float = sum(y_velocities)/len(y_velocities)

        x_alignment_force = x_average_speed - self.x_velocity
        y_alignment_force = y_average_speed - self.y_velocity

        x_alignment_force, y_alignment_force = self.calculate_magnitude(x_alignment_force, y_alignment_force)

        x_alignment_force = x_alignment_force * self.alignment_force_multiplier
        y_alignment_force = y_alignment_force * self.alignment_force_multiplier

        # print(x_alignment_force, " ", y_alignment_force)

        return x_alignment_force, y_alignment_force  

    def cohesion(self,sprite_group) -> tuple[float,float]:
        x_locations: list[float] = []
        y_locations: list[float] = []
        
        for sprite in sprite_group:
            if sprite is not self:
                distance = sqrt((self.x_loc - sprite.x_loc)**2 + (self.y_loc - sprite.y_loc)**2)
                if distance <= self.max_perception:
                    x_locations.append(sprite.x_loc)
                    y_locations.append(sprite.y_loc)
        
        if len(x_locations) == 0:
            return 0.0,0.0
        
        x_average_location: float = sum(x_locations)/len(x_locations)
        y_average_location: float = sum(y_locations)/len(y_locations)

        x_cohesion_force: float = x_average_location - self.x_loc
        y_cohesion_force: float = y_average_location - self.y_loc

        x_cohesion_force, y_cohesion_force = self.calculate_magnitude(x_cohesion_force, y_cohesion_force)

        x_cohesion_force = x_cohesion_force * self.cohesion_force_multiplier
        y_cohesion_force = y_cohesion_force * self.cohesion_force_multiplier

        return x_cohesion_force, y_cohesion_force
    
    def separation(self, sprite_group) -> tuple[float,float]:
        x_separation_forces: list[float] = []
        y_separation_forces: list[float] = []

        for sprite in sprite_group:
            if sprite is not self:
                distance = sqrt((self.x_loc - sprite.x_loc)**2 + (self.y_loc - sprite.y_loc)**2)
                if distance <= self.max_perception and distance > 0:
                    x_individual_separation = (self.x_loc - sprite.x_loc) / (distance)
                    y_individual_separation = (self.y_loc - sprite.y_loc) / (distance)
                    x_separation_forces.append(x_individual_separation)
                    y_separation_forces.append(y_individual_separation)
                if distance == 0:
                    x_separation_forces.append(self. max_perception)
                    y_separation_forces.append(self.max_perception)

        if len(x_separation_forces) == 0:
            return 0.0,0.0

        x_separation_force: float = sum(x_separation_forces)/len(x_separation_forces)
        y_separation_force: float = sum(y_separation_forces)/len(y_separation_forces)

        # x_separation_force, y_separation_force = self.calculate_magnitude(x_separation_force, y_separation_force)

        x_separation_force = x_separation_force * self.separation_force_multiplier
        y_separation_force = y_separation_force * self.separation_force_multiplier
        
        return x_separation_force, y_separation_force


def main() -> None:
    window_height: int = 640
    window_width: int = 640
    frames_per_sec: int = 60

    n_boids: int = 75

    frame_rate: pygame.time.Clock = pygame.time.Clock()
    screen = pygame.display.set_mode((window_width,window_height), pygame.SCALED)
    pygame.display.set_caption("Boids")

    boid1: Boid = Boid(window_height/2, window_width/3, window_width, window_height, color=(233,150,122))
    boid2: Boid = Boid(window_height/2, window_width/2, window_width, window_height, color=(233,150,122))

    all_boids: pygame.sprite.Group = pygame.sprite.Group()

    if n_boids > 0:
        for _ in range(n_boids):
            x_location = window_width * random.random()
            y_location = window_height * random.random()
            all_boids.add(Boid(x_location, y_location, window_width, window_height))

    all_boids.add(boid1)
    all_boids.add(boid2)

    font = pygame.font.Font('freesansbold.ttf',20)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()

        screen.fill((255,255,255))
        for element in all_boids:
            element.calculate_velocity(all_boids, edges=True)
        
        for element in all_boids:
            element.move()
            element.draw(screen)
        
        boid1_txt = font.render(f'Boid1: {round(boid1.x_loc,4)}, {round(boid1.y_loc,4)}',True,(0,0,0))
        boid2_txt = font.render(f'Boid2: {round(boid2.x_velocity,4)}, {round(boid2.y_velocity,4)}',True,(0,0,0))
        screen.blit(boid1_txt,(20,20))
        screen.blit(boid2_txt,(20,40))

        pygame.display.flip()
        frame_rate.tick(frames_per_sec)


if __name__ == "__main__":
    main()