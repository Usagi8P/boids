import pygame
from typing import Union, Optional

class InputBox:
    def __init__(self, text:str, surface: pygame.Surface, rect: pygame.Rect,
                 font:pygame.font, text_color:Union[str,tuple[int,int,int]]='black'):
        self.surface = surface
        self.rect = rect
        self.font = font
        self.text_color = text_color
        self.text = text
        self.active = False
        self.color = 'black'

    def handle_event(self, event, offset:tuple[int,int]) -> Optional[str]:
        collision_area = self.rect.move(offset[0], offset[1])

        if event.type == pygame.MOUSEBUTTONDOWN:
            if collision_area.collidepoint(event.pos):
                self.active = not self.active
                self.previous_text = self.text
                self.text = ''
                self.color = 'blue'

            elif self.active and not collision_area.collidepoint(event.pos):
                self.active = False
                self.color = 'black'
                if self.text == '':
                    self.text = self.previous_text
                return self.text

            else:
                self.active = False
                self.color = 'black'

        elif event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    self.active = False
                    self.color = 'black'
                    return self.text

                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode

    def draw(self):
        pygame.draw.rect(self.surface, self.color, self.rect, 2)
        text_surface = self.font.render(self.text, True, self.text_color)
        width = max(self.rect.width, text_surface.get_width() + 10)
        self.rect.width = width
        self.surface.blit(text_surface, (self.rect.x + 5, self.rect.y + 5))


class RadioButton:
    def __init__(self, value: bool, surface: pygame.Surface, rect: pygame.Rect):
        self.value = value
        self.surface = surface
        self.rect = rect
        self.color = 'black'
        self.interior = self.rect.scale_by(0.9)
        self.on_button = self.interior.scale_by(0.9)

    def handle_event(self, event, offset:tuple[int,int]) -> Optional[bool]:
        collision_area = self.rect.move(offset[0], offset[1])

        if event.type == pygame.MOUSEBUTTONDOWN:
            if collision_area.collidepoint(event.pos):
                self.value = not self.value
                return self.value        

    def draw(self):
        if self.value:
            pygame.draw.rect(self.surface, self.color, self.rect)
            pygame.draw.rect(self.surface, 'white', self.interior)
            pygame.draw.rect(self.surface, self.color, self.on_button)
        if not self.value:
            pygame.draw.rect(self.surface, self.color, self.rect)
            pygame.draw.rect(self.surface, 'white', self.interior)


class Button:
    def __init__(self, text: str, surface: pygame.surface, rect: pygame.Rect, font: pygame.font,
                 text_color: Union[str,tuple[int,int,int]], background_color: Union[str,tuple[int,int,int]]):
        self.text = text
        self.rect = rect
        self.surface = surface
        self.font = font
        self.text_color = text_color
        self.color = background_color

    def handle_event(self, event, offset:tuple[int,int]):
        collision_area = self.rect.move(offset[0], offset[1])

        if event.type == pygame.MOUSEBUTTONDOWN:
            if collision_area.collidepoint(event.pos):
                return True

    def draw(self):
        pygame.draw.rect(self.surface, self.color, self.rect)
        text_surface = self.font.render(self.text, True, self.text_color)
        width = max(self.rect.width, text_surface.get_width() + 10)
        self.rect.width = width
        self.surface.blit(text_surface, (self.rect.x + 5, self.rect.y + 5))


class Text:
    def __init__(self, text: str, surface: pygame.surface, rect: pygame.Rect, font: pygame.font):
        self.text = text
        self.rect = rect
        self.surface = surface
        self.font = font
        self.text_color = 'black'
        self.color = 'white'
    
    def draw(self):
        pygame.draw.rect(self.surface, self.color, self.rect, 2)
        text_surface = self.font.render(self.text, True, self.text_color)
        width = max(self.rect.width, text_surface.get_width() + 10)
        self.rect.width = width
        self.surface.blit(text_surface, (self.rect.x + 5, self.rect.y + 5))
