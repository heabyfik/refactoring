import json
import pygame


class Button:
    def __init__(self, x, y, w, h, text='Hello', is_off=False):
        self.x = int(x)
        self.y = int(y)
        self.w = int(w)
        self.h = int(h)

        self.text = text
        self.is_active = False
        self.is_off = is_off
        self.font = pygame.font.SysFont(None, 42)

        self._load_images()

    def draw(self, window, outline=None):
        if outline:
            pygame.draw.rect(window, outline, (self.x-2, self.y-2, self.w+4, self.h+4), 0)

        if self.is_off:
            window.blit(self.image_off, [int(self.x), int(self.y)])
        elif self.is_active:
            window.blit(self.image_active, [int(self.x), int(self.y)])
        else:
            window.blit(self.image, [int(self.x), int(self.y)])

        text = self.font.render(self.text, 1, (0, 0, 0))
        window.blit(text, (self.x+(self.w/2-text.get_width()/2), self.y+(self.h/2-text.get_height()/2)))

    def is_over(self, pos):
        if pos[0] > self.x and pos[0] < self.x + self.w:
            if pos[1] > self.y and pos[1] < self.y + self.h:
                self.is_active = True
                return True
        self.is_active = False
        return False

    def _load_images(self):
        self.image = pygame.image.load('../drawable/buttons/red_button.png')
        self.image_active = pygame.image.load('../drawable/buttons/red_button_light.png')
        self.image_off = pygame.image.load('../drawable/buttons/gray_button.png')

        self.image = pygame.transform.scale(self.image, (self.w, self.h))
        self.image_active = pygame.transform.scale(self.image_active, (self.w, self.h))
        self.image_off = pygame.transform.scale(self.image_off, (self.w, self.h))


class TextView:
    def __init__(self, font, color, x, y, text=""):
        self.font = font
        self.color = color
        self.x = int(x)
        self.y = int(y)
        self.text = text

        self.COLOR_ACTIVE = (255, 0, 0)
        self.COLOR_INACTIVE = (180, 0, 0)

        self.text_object = self.font.render(self.text, 1, self.color)
        self.rect = self.text_object.get_rect()
        self.rect.topleft = (self.x, self.y)

    def draw(self, window):
        self.text_object = self.font.render(self.text, 1, self.color)
        window.blit(self.text_object, self.rect)

    def draw_this(self, window, buffer):
        self.text_object = self.font.render(buffer, 1, self.color)
        window.blit(self.text_object, self.rect)

    def next_line(self, size):
        self.rect.move_ip(0, size+2)

    def is_over(self, pos): 
        if pos[0] > self.rect.left and pos[0] < self.rect.right:
            if pos[1] > self.rect.top and pos[1] < self.rect.bottom:
                self.color = self.COLOR_ACTIVE
                return True

        self.color = self.COLOR_INACTIVE
        return False


class Player:
    def __init__(self, player_name, score, levels, skins, current_skin):
        self.name = player_name
        self.score = score
        self.levels = levels
        self.skins = skins
        self.current_skin = current_skin

    def save_current_state(self):
        data = dict()
        data["name"] = self.name
        data["score"] = self.score
        data["levels"] = self.levels
        data["skins"] = self.skins
        data["current_skin"] = self.current_skin

        handler = open("../stats/players/" + self.name + ".json", 'w')
        json.dump(data, handler)
        handler.close()


class InputBox:
    def __init__(self, x, y, w, h, text=''):
        self.COLOR_INACTIVE = (180, 0, 0) 
        self.COLOR_ACTIVE = (255, 0, 0)
        self.rect = pygame.Rect(x, y, w, h)
        self.color = self.COLOR_INACTIVE
        self.font = pygame.font.Font(None, 32) 
        self.text = text
        self.txt_surface = self.font.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self._handle_mouse_click()
        if event.type == pygame.KEYDOWN:
            self._handle_key_press()

    def _handle_mouse_click(self):
        if self.rect.collidepoint(event.pos):
            self.active = not self.active
        else:
            self.active = False
        self.color = self.COLOR_ACTIVE if self.active else self.COLOR_INACTIVE

    def _handle_key_press(self):
        if self.active:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                if len(self.text) > 20:
                    return
                self.text += event.unicode
            self.txt_surface = self.font.render(self.text, True, self.color)

    def update(self):
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, window):
        window.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        pygame.draw.rect(window, self.color, self.rect, 2)


def load_player_by_path(path):
    handler = open(path, 'r')
    data = json.load(handler)
    player = Player(data['name'], data['score'], data['levels'], data['skins'], data["current_skin"])
    handler.close()
    
    return player


def create_empty_profile(nickname):
    handler = open("../stats/players/" + nickname + ".json", 'w')
    data = {"name": nickname, "score": 0, "levels": [1], "skins": [1], "current_skin" : 1}
    json.dump(data, handler)
    handler.close()
