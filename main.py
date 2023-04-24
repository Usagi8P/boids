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
        self.max_perception: float = 40
        self.alignment_force_multiplier: float = 0.4
        self.cohesion_force_multiplier: float = 0.3
        self.separation_force_multiplier: float = 0.4
        self.window_x = window_x
        self.window_y = window_y
        self.x_destination, self.y_destination = self.select_first_destionation(window_x,window_y)
        self.x_velocity, self.y_velocity = self.select_first_velocity()
        self.x_acceleration: float = 0.0
        self.y_acceleration: float = 0.0
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
            self.x_acceleration = self.x_acceleration
            self.y_acceleration = self.y_acceleration
        if not edge_check:
            self.x_acceleration = (x_alignment_force + x_cohesion_force + x_separation_force)
            self.y_acceleration = (y_alignment_force + y_cohesion_force + y_separation_force)
        edge_check = False
        # self.x_acceleration, self.y_acceleration = self.calculate_magnitude(self.x_acceleration, self.y_acceleration)

    def move(self, same_speed: bool):
        self.x_velocity = self.x_acceleration + self.x_velocity
        self.y_velocity = self.y_acceleration + self.y_velocity
        magnitude = self.magnitude_adjustment(self.x_velocity, self.y_velocity)
        if same_speed is True:
            if magnitude >= self.speed + 2:
                self.x_velocity, self.y_velocity = self.calculate_magnitude(self.x_velocity, self.y_velocity) # Possibly limit velocity
                self.x_velocity = self.x_velocity * (self.speed+2)
                self.y_velocity = self.y_velocity * (self.speed+2)
        if same_speed is not True:
            self.x_velocity, self.y_velocity = self.calculate_magnitude(self.x_velocity, self.y_velocity) # Possibly limit velocity
            self.x_velocity = self.x_velocity * self.speed
            self.y_velocity = self.y_velocity * self.speed
        self.x_loc = self.x_velocity + self.x_loc
        self.y_loc = self.y_velocity + self.y_loc
        self.x_acceleration = 0
        self.y_acceleration = 0

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
                self.x_acceleration = self.x_acceleration - turn_speed
                return True
            if self.x_loc <= 0 + avoid_distance:
                self.x_acceleration = self.x_acceleration + turn_speed
                return True
            if self.y_loc >= self.window_y-self.radius*2 - avoid_distance:
                self.y_acceleration = self.y_acceleration - turn_speed
                return True
            if self.y_loc <= 0 + avoid_distance:
                self.y_acceleration = self.y_acceleration + turn_speed
                return True
        return False

    def calculate_magnitude(self,x_adjust, y_adjust) -> tuple[float, float]: 
        movement_magnitude = self.magnitude_adjustment(x_adjust, y_adjust)
        if movement_magnitude > 0.0:
            x_velocity: float = (self.x_loc-self.x_loc+x_adjust) / movement_magnitude
            y_velocity: float = (self.y_loc-self.y_loc+y_adjust) / movement_magnitude
        if movement_magnitude == 0.0:
            x_velocity = 0.0
            y_velocity = 0.0
        return x_velocity, y_velocity

    def magnitude_adjustment(self, x_adjust, y_adjust) -> float:
        movement_magnitude: float = sqrt((self.x_loc-self.x_loc+x_adjust)**2+(self.y_loc-self.y_loc+y_adjust)**2)
        minimum_magnitude = 0.01
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
                    x_individual_separation = (self.x_loc - sprite.x_loc) / (distance*distance)
                    y_individual_separation = (self.y_loc - sprite.y_loc) / (distance*distance)
                    x_separation_forces.append(x_individual_separation)
                    y_separation_forces.append(y_individual_separation)
                if distance == 0:
                    x_separation_forces.append(self. max_perception)
                    y_separation_forces.append(self.max_perception)

        if len(x_separation_forces) == 0:
            return 0.0,0.0

        x_separation_force: float = sum(x_separation_forces)/len(x_separation_forces)
        y_separation_force: float = sum(y_separation_forces)/len(y_separation_forces)

        x_separation_force, y_separation_force = self.calculate_magnitude(x_separation_force, y_separation_force)

        x_separation_force = x_separation_force * self.separation_force_multiplier
        y_separation_force = y_separation_force * self.separation_force_multiplier
        
        return x_separation_force, y_separation_force


def main() -> None:
    window_height: int = 640
    window_width: int = 640
    frames_per_sec: int = 60

    n_boids: int = 50
    edges: bool = False
    same_speed: bool = True

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
            element.calculate_velocity(all_boids, edges=edges)
        
        for element in all_boids:
            element.move(same_speed)
            element.draw(screen)
        
        boid1_txt = font.render(f'Boid1: {round(boid1.x_loc,4)}, {round(boid1.y_loc,4)}',True,(0,0,0))
        boid2_txt = font.render(f'Boid2: {round(boid2.x_velocity,4)}, {round(boid2.y_velocity,4)}',True,(0,0,0))
        screen.blit(boid1_txt,(20,20))
        screen.blit(boid2_txt,(20,40))

        pygame.display.flip()
        frame_rate.tick(frames_per_sec)


if __name__ == "__main__":
    main()