import pygame
from pygame.locals import *
import random
from boid import Boid
from input_options import InputBox, Text, RadioButton, Button


def main() -> None:
    pygame.init()
    
    window_height: int = 640
    window_width: int = 640
    frames_per_sec: int = 60

    option_width: int = 320

    n_boids: int = 50
    alignment_force: float = 0.2
    cohesion_force: float = 0.4
    separation_force: float = 0.5
    edges: bool = False
    same_speed: bool = True

    frame_rate: pygame.time.Clock = pygame.time.Clock()
    screen = pygame.display.set_mode((window_width + option_width,window_height), pygame.SCALED)
    pygame.display.set_caption("Boids")
    all_boids: pygame.sprite.Group = pygame.sprite.Group()

    boid_area = pygame.Surface((window_width, window_height))
    option_area = pygame.Surface((option_width, window_height))

    if n_boids > 0:
        for _ in range(n_boids):
            x_location = window_width * random.random()
            y_location = window_height * random.random()
            all_boids.add(Boid(x_location, y_location, window_width, window_height,
                               alignment_force=alignment_force, cohesion_force=cohesion_force, separation_force=separation_force))

    font = pygame.font.Font('freesansbold.ttf',20)
    alignment_text = Text('Alignment', option_area, pygame.Rect((50,100,200,32)), font)
    alignment_input = InputBox(str(alignment_force), option_area, pygame.Rect((50,150,200,32)),font)
    cohesion_text = Text('Cohesion', option_area, pygame.Rect((50,200,200,32)), font)
    cohesion_input = InputBox(str(cohesion_force), option_area, pygame.Rect((50,250,200,32)),font)
    separation_text = Text('Separation', option_area, pygame.Rect((50,300,200,32)), font)
    separation_input = InputBox(str(separation_force), option_area, pygame.Rect((50,350,200,32)),font)

    edges_text = Text('Avoid Edge of Screen', option_area, pygame.Rect(50,400,200,32), font)
    edges_radio_button = RadioButton(edges, option_area, pygame.Rect(50,450,32,32))

    reset_button = Button('Reset', option_area, pygame.Rect(50,500,200,32), font,
                          'black', 'red')
    quit_button = Button('Quit', option_area, pygame.Rect(50,550,200,32), font,
                         'black', 'red')

    game_loop = True
    while game_loop:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()

            new_alignment_force = alignment_input.handle_event(event, (boid_area.get_width(),0))
            if new_alignment_force is not None:
                alignment_force = convert_to_float(new_alignment_force)
                alignment_input.text = str(alignment_force)

            new_cohesion_force = cohesion_input.handle_event(event, (boid_area.get_width(),0))
            if new_cohesion_force is not None:
                cohesion_force = convert_to_float(new_cohesion_force)
                cohesion_input.text = str(cohesion_force)

            new_separation_force = separation_input.handle_event(event, (boid_area.get_width(),0))
            if new_separation_force is not None: 
                separation_force = convert_to_float(new_separation_force)
                separation_input.text = str(separation_force)

            edge_radio_result = edges_radio_button.handle_event(event, (boid_area.get_width(),0))
            if edge_radio_result is not None:
                edges = edge_radio_result

            reset_result = reset_button.handle_event(event, (boid_area.get_width(),0))
            if reset_result:
                main()

            quit_result = quit_button.handle_event(event, (boid_area.get_width(),0))
            if quit_result:
                pygame.quit()

            for element in all_boids:
                element.cohesion_force_multiplier = cohesion_force
                element.alignment_force_multiplier = alignment_force
                element.separation_force_multiplier = separation_force
                    

        screen.fill('white')
        boid_area.fill('white')
        option_area.fill('white')
                
        for element in all_boids:
            element.calculate_velocity(all_boids, edges=edges)
        
        for element in all_boids:
            element.move(same_speed)
            element.draw(boid_area)
        
        alignment_text.draw()
        alignment_input.draw()

        cohesion_text.draw()
        cohesion_input.draw()

        separation_text.draw()
        separation_input.draw()

        edges_text.draw()
        edges_radio_button.draw()

        reset_button.draw()
        quit_button.draw()

        screen.blit(boid_area, (0,0))
        screen.blit(option_area, (boid_area.get_width(), 0))
        pygame.display.flip()
        frame_rate.tick(frames_per_sec)


def convert_to_float(string: str) -> float:
    string = string
    number = [character for i, character in enumerate(string) if character in '1234567890.' and (character != '.' or '.' not in string[:i])]
    number = ''.join(number)
    
    if number == '':
        return 0.0

    number = float(number)
    return number


if __name__ == "__main__":
    main()
