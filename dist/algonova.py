import pygame as game
import random
import math as mathematic
import numpy as matrix


class GameSprite(game.sprite.Sprite):
    def __init__(self, sprite_image, sprite_x, sprite_y, size_x, size_y, sprite_speed):
        super().__init__()
        self.image = game.transform.scale(game.image.load(sprite_image), (size_x, size_y))
        self.speed = sprite_speed
        self.position = self.image.get_rect()
        self.position.x = sprite_x
        self.position.y = sprite_y
        self.side = "left"
        self.frames = []
        self.current_frame = 0
        self.animation_speed = 0.1
        self.status = None
        self.angle = 0

    def reset(self, window):
        window.window.blit(self.image, (self.position.x, self.position.y))

    def move(self, direction="up"):
        if direction == "up":
            self.position.y -= self.speed
        elif direction == "down":
            self.position.y += self.speed
        elif direction == "left":
            self.position.x -= self.speed
        elif direction == "right":
            self.position.x += self.speed

    def limit_movement(self, win_size=(0, 0)):
        win_width, win_height = win_size
        if self.position.x < 10:
            self.position.x = 10
        if self.position.x > win_width - self.image.get_width():
            self.position.x = win_width - self.image.get_width()
        if self.position.y < 10:
            self.position.y = 10
        if self.position.y > win_height - self.image.get_height():
            self.position.y = win_height - self.image.get_height()

    def collideWith(self, sprite):
        return self.position.colliderect(sprite.position)

    def left_right_behaviour(self, left_limit, right_limit):
        if self.position.x <= left_limit:
            if self.side != "right":  # Periksa apakah arah berubah
                self.flip(horizontal=True, vertical=False)
            self.side = "right"
        if self.position.x >= right_limit:
            if self.side != "left":  # Periksa apakah arah berubah
                self.flip(horizontal=True, vertical=False)
            self.side = "left"
        if self.side == "left":
            self.position.x -= self.speed
        else:
            self.position.x += self.speed

    def fall_down_behaviour(self, window_size=(0, 0)):
        win_width, win_height = window_size
        self.position.y += self.speed
        if self.position.y > win_height:
            self.position.x = random.randint(80, win_width - 80)
            self.position.y = 0
    
    def zig_zag_behaviour(self, window_size=(0, 0), zigzag_width=50):
        win_width, win_height = window_size
        self.position.y += self.speed
        self.position.x += (self.speed if (self.position.y // zigzag_width) % 2 == 0 else -self.speed)

        if self.position.y > win_height:
            self.position.x = random.randint(80, win_width - 80)
            self.position.y = 0

    def bouncing_behaviour(self, window_size=(0, 0)):
        win_width, win_height = window_size
        if self.position.x <= 0 or self.position.x + self.image.get_width() >= win_width:
            self.speed = -self.speed  # Balik arah horizontal
        self.position.x += self.speed

    def hovering_behaviour(self, hover_range=10):
        self.position.y += self.speed
        if abs(self.position.y % (2 * hover_range) - hover_range) < hover_range // 2:
            self.speed = -self.speed

    def random_teleport_behaviour(self, window_size=(0, 0), teleport_interval=120):
        win_width, win_height = window_size
        if random.randint(0, teleport_interval) == 0:
            self.position.x = random.randint(10, win_width - self.image.get_width() - 10)
            self.position.y = random.randint(10, win_height - self.image.get_height() - 10)

    def circular_behaviour(self, center, radius, angle_speed):
        self.angle += angle_speed
        self.position.x = center[0] + int(radius * mathematic.cos(self.angle))
        self.position.y = center[1] + int(radius * mathematic.sin(self.angle))

    def accelerating_behaviour(self, max_speed=10):
        if self.speed < max_speed:
            self.speed += 0.1  # Tingkatkan kecepatan secara bertahap
        self.position.y += self.speed

    def rotate(self, angle):
        self.image = game.transform.rotate(self.image, angle)
        self.position = self.image.get_rect(center=self.position.center)

    def flip(self, horizontal=True, vertical=False):
        self.image = game.transform.flip(self.image, horizontal, vertical)
        self.position = self.image.get_rect(center=self.position.center)

    def update_animation(self):
        if self.frames:
            self.current_frame += self.animation_speed
            if self.current_frame >= len(self.frames):
                self.current_frame = 0
            self.image = self.frames[int(self.current_frame)]

    def load_animation(self, frame_paths, size):
        self.frames = [game.transform.scale(game.image.load(frame), size) for frame in frame_paths]
        if self.frames:
            self.image = self.frames[0]

    def set_status(self, status):
        self.status = status

class Music():
    def __init__(self, music_file):
        game.mixer.init()
        self.music = game.mixer.music.load(music_file)
    def play(self):
        game.mixer.music.play()
    def stop(self):
        game.mixer.music.stop()

class Sound():
    def __init__(self, sound_file):
        game.mixer.init()
        self.sound = game.mixer.Sound(sound_file)
    def play(self):
        self.sound.play()

class Screen():
    def __init__(self, caption, background, window_size=(0, 0)):
        self.window = game.display.set_mode(window_size)
        game.display.set_caption(caption)
        self.window_size = window_size
        try:
            self.background = game.transform.scale(game.image.load(background), window_size)
        except:
            self.background = background
    
    def set_background(self, background):
        try:
            self.background = game.transform.scale(game.image.load(background), self.window_size)
        except:
            self.background = background

    def update(self):
        try:
            self.window.blit(self.background, (0, 0))
        except:
            self.window.fill(self.background)
    
    def toggle_fullscreen(self):
        game.display.toggle_fullscreen()

class Text():
    def __init__(self, caption, size, color, font=None):
        game.font.init()
        self.font = game.font.Font(font, size)
        self.text = self.font.render(caption, True, color)
        self.position = self.text.get_rect()
        self.position.x, self.position.y = 0, 0
        self.color = color
    def set_position(self, x, y):
        self.position.x = x
        self.position.y = y
    def change_text(self, text):
        self.text = self.font.render(text, True, self.color)
    def set_align(self, window_size, pos="center"):
        if pos == "center" or pos=="centre":
            self.position.x = (window_size[0] - self.text.get_width()) // 2
            self.position.y = (window_size[1] - self.text.get_height()) // 2
        elif pos == "left":
            self.position.x = 50
            self.position.y = (window_size[1] - self.text.get_height()) // 2
        elif pos == "right":
            self.position.x = window_size[0] - self.text.get_width() - 50
            self.position.y = (window_size[1] - self.text.get_height()) // 2
        elif pos == "top":
            self.position.x = (window_size[0] - self.text.get_width()) // 2
            self.position.y = 50
        elif pos == "bottom":
            self.position.x = (window_size[0] - self.text.get_width()) // 2
            self.position.y = window_size[1] - self.text.get_height() - 50
        elif pos == "left top":
            self.position.x = 50
            self.position.y = 50
        elif pos == "right top":
            self.position.x = window_size[0] - self.text.get_width() - 50
            self.position.y = 50
        elif pos == "left bottom":
            self.position.x = 50
            self.position.y = window_size[1] - self.text.get_height() - 50
        elif pos == "right bottom":
            self.position.x = window_size[0] - self.text.get_width() - 50
            self.position.y = window_size[1] - self.text.get_height() - 50
        else:
            text = 'Invalid position, you can use:\n1. top\n2. left\n3. right\n4. bottom\n5. center\nor combination between 1 until 4 like "left top" etc'
            raise ValueError(text)
    def set_multiline_text(self, caption, max_width):
        self.lines = []
        words = caption.split(' ')
        current_line = words[0]
        for word in words[1:]:
            if self.font.size(current_line + ' ' + word)[0] <= max_width:
                current_line += ' ' + word
            else:
                self.lines.append(current_line)
                current_line = word
        self.lines.append(current_line)

    def show_multiline_text(self, window, line_spacing=10):
        for i, line in enumerate(self.lines):
            text_surface = self.font.render(line, True, self.color)
            line_position = self.position.copy()
            line_position.y += i * (self.text.get_height() + line_spacing)
            window.window.blit(text_surface, line_position)
    def fade_in(self, window, steps=10, delay=50):
        for alpha in range(0, 256, steps):
            temp_surface = self.text.copy()
            temp_surface.set_alpha(alpha)
            window.window.blit(temp_surface, self.position)
            game.display.flip()
            game.time.delay(delay)

    def fade_out(self, window, steps=10, delay=50):
        for alpha in range(255, -1, -steps):
            temp_surface = self.text.copy()
            temp_surface.set_alpha(alpha)
            window.window.blit(temp_surface, self.position)
            game.display.flip()
            game.time.delay(delay)
    def change_color(self, new_color):
        self.color = new_color
        self.text = self.font.render(self.text.get_text(), True, self.color)
    def rotate_text(self, angle):
        self.text = game.transform.rotate(self.text, angle)
        self.position = self.text.get_rect(center=self.position.center)
    def set_shadow(self, shadow_color=(0, 0, 0), offset=(2, 2)):
        self.shadow_color = shadow_color
        self.shadow_offset = offset

    def show_text_with_shadow(self, window):
        # Gambar bayangan terlebih dahulu
        if hasattr(self, 'shadow_color') and hasattr(self, 'shadow_offset'):
            shadow_text = self.font.render(self.text.get_text(), True, self.shadow_color)
            shadow_position = self.position.copy()
            shadow_position.x += self.shadow_offset[0]
            shadow_position.y += self.shadow_offset[1]
            window.window.blit(shadow_text, shadow_position)
        # Gambar teks utama
        window.window.blit(self.text, self.position)

    def show_text(self, window):
        window.window.blit(self.text, self.position)

class Button:
    def __init__(self, width=90, height=50, color=(0, 0, 0), border_radius=10):
        self.position = game.Rect(0, 0, width, height)
        self.color = color
        self.width = width
        self.height = height
        self.border_radius = border_radius
        self.text = "Button"
        self.font = "verdana"
        self.font_size = int(height / 3)
        self.text_color = (255, 255, 255)
        self.bold = True
        self.italic = False
        self.disabled = False
        self.disabled_color = (100, 100, 100)
        self.hover_color = color
        self.hover_text_color = self.text_color

    def set_position(self, x, y):
        self.position.x = x
        self.position.y = y

    def set_align(self, window_size, pos="center"):
        if pos == "center" or pos == "centre":
            self.position.x = (window_size[0] - self.width) // 2
            self.position.y = (window_size[1] - self.height) // 2
        elif pos == "left":
            self.position.x = 50
            self.position.y = (window_size[1] - self.height) // 2
        elif pos == "right":
            self.position.x = window_size[0] - self.width - 50
            self.position.y = (window_size[1] - self.height) // 2
        elif pos == "top":
            self.position.x = (window_size[0] - self.width) // 2
            self.position.y = 50
        elif pos == "bottom":
            self.position.x = (window_size[0] - self.width) // 2
            self.position.y = window_size[1] - self.height - 50
        elif pos == "left top":
            self.position.x = 50
            self.position.y = 50
        elif pos == "right top":
            self.position.x = window_size[0] - self.width - 50
            self.position.y = 50
        elif pos == "left bottom":
            self.position.x = 50
            self.position.y = window_size[1] - self.height - 50
        elif pos == "right bottom":
            self.position.x = window_size[0] - self.width - 50
            self.position.y = window_size[1] - self.height - 50
        else:
            text = "Invalid position, you can use:\n1. top\n2. left\n3. right\n4. bottom\n5. center\nor combination like 'left top'"
            raise ValueError(text)

    def show_button(self, window, border=None):
        current_color = self.disabled_color if self.disabled else self.color
        current_text_color = (150, 150, 150) if self.disabled else self.text_color

        # Hover effect
        mouse_pos = game.mouse.get_pos()
        if not self.disabled and self.position.collidepoint(mouse_pos):
            current_color = self.hover_color
            current_text_color = self.hover_text_color

        text = game.font.SysFont(self.font, self.font_size, self.bold, self.italic).render(self.text, True, current_text_color)
        game.draw.rect(window.window, current_color, self.position, border_radius=self.border_radius)
        positionx = self.position.x + ((self.width - text.get_width()) // 2)
        positiony = self.position.y + ((self.height - text.get_height()) // 2)
        window.window.blit(text, (positionx, positiony))

        if border:
            try:
                frame_color, thickness = border
                game.draw.rect(window, frame_color, self.position, thickness)
            except:
                raise ValueError("The border must be a tuple. ex: ((0, 0, 0), 2)")

    def button_configure(self, text, font=None, font_size=None, text_color=None, bold=True, italic=False):
        self.text = text
        if font:
            self.font = font
        if font_size:
            self.font_size = font_size
        if text_color:
            self.text_color = text_color
        self.bold = bold
        self.italic = italic

    def set_hover_effect(self, hover_color=None, hover_text_color=None):
        self.hover_color = hover_color if hover_color else self.color
        self.hover_text_color = hover_text_color if hover_text_color else self.text_color

    def clicked(self):
        if self.disabled:
            return False
        mouse_pos = game.mouse.get_pos()
        if self.position.collidepoint(mouse_pos) and game.mouse.get_pressed()[0]:
            return True
        return False

    def on_click(self, callback, *args, **kwargs):
        if self.clicked():
            callback(*args, **kwargs)

    def animate_click(self, window, scale_factor=1.1):
        if self.disabled:
            return
        original_rect = self.position.copy()
        scaled_width = int(self.width * scale_factor)
        scaled_height = int(self.height * scale_factor)
        scaled_x = self.position.x - (scaled_width - self.width) // 2
        scaled_y = self.position.y - (scaled_height - self.height) // 2
        scaled_rect = game.Rect(scaled_x, scaled_y, scaled_width, scaled_height)

        game.draw.rect(window.window, self.color, scaled_rect)
        game.display.flip()
        game.time.delay(100)
        self.show_button(window)

    def set_disabled(self, disabled=True, disabled_color=(100, 100, 100)):
        self.disabled = disabled
        self.disabled_color = disabled_color

class Event():
    w = "w"
    s = "s"
    a = "a"
    d = "d"
    space = "space"
    esc = "esc"
    ctrl = "ctrl"
    shift = "shift"
    tab = "tab"
    q = "q"
    e = "e"
    r = "r"
    t = "t"
    y = "y"
    u = "u"
    i = "i"
    o = "o"
    p = "p"
    l = "l"
    j = "j"
    k = "k"
    h = "h"
    g = "g"
    f = "f"
    v = "v"
    b = "b"
    n = "n"
    m = "m"
    enter = "enter"
    backspace = "backspace"
    c = "c"
    x = "x"
    z = "z"
    k1 = "1"
    k2 = "2"
    k3 = "3"
    k4 = "4"
    k5 = "5"
    k6 = "6"
    k7 = "7"
    k8 = "8"
    k9 = "9"
    k0 = "0"
    f1 = "f1"
    f2 = "f2"
    f3 = "f3"
    f4 = "f4"
    f5 = "f5"
    f6 = "f6"
    f7 = "f7"
    f8 = "f8"
    f9 = "f9"
    f10 = "f10"
    arrow_up = "up"
    arrow_down = "down"
    arrow_left = "left"
    arrow_right = "right"
    def __init__(self):
        self.key_map = {
            "w": game.K_w, "s": game.K_s, "a": game.K_a, "d": game.K_d,
            "space": game.K_SPACE, "esc": game.K_ESCAPE, "ctrl": (game.K_LCTRL, game.K_RCTRL),
            "shift": (game.K_LSHIFT, game.K_RSHIFT), "tab": game.K_TAB, "enter": game.K_RETURN,
            "backspace": game.K_BACKSPACE, "q": game.K_q, "e": game.K_e, "r": game.K_r,
            "t": game.K_t, "y": game.K_y, "u": game.K_u, "i": game.K_i, "o": game.K_o,
            "p": game.K_p, "j": game.K_j, "k": game.K_k, "l": game.K_l, "z": game.K_z,
            "x": game.K_x, "c": game.K_c, "v": game.K_v, "b": game.K_b, "n": game.K_n,
            "m": game.K_m, "1": game.K_1, "2": game.K_2, "3": game.K_3, "4": game.K_4,
            "5": game.K_5, "6": game.K_6, "7": game.K_7, "8": game.K_8, "9": game.K_9,
            "0": game.K_0, "f": game.K_f, "g": game.K_g, "h": game.K_h,
            "arrow_up": game.K_UP, "arrow_down": game.K_DOWN,
            "arrow_left": game.K_LEFT, "arrow_right": game.K_RIGHT,
            "f1": game.K_F1, "f2": game.K_F2, "f3": game.K_F3, "f4": game.K_F4,
            "f5": game.K_F5, "f6": game.K_F6, "f7": game.K_F7, "f8": game.K_F8,
            "f9": game.K_F9, "f10": game.K_F10, "f11": game.K_F11, "f12": game.K_F12
        }

    def onKey(self, key):
        if key in self.key_map:
            mapped_key = self.key_map[key]
            if isinstance(mapped_key, tuple):
                # Handle cases with multiple possible keys (e.g., left and right ctrl)
                return any(game.key.get_pressed()[k] for k in mapped_key)
            return game.key.get_pressed()[mapped_key]
        raise ValueError(f"Key '{key}' is not mapped!")

    def onCombination(self, *keys):
        return all(self.onKey(key) for key in keys)

class System():
    def __init__(self, fps):
        game.init()
        self.time = game.time.Clock()
        self.fps = fps
        self.stop = False
    def run(self):
        for event in game.event.get():
            if event.type == game.QUIT:
                game.quit()
                quit()
        game.display.update()
        self.time.tick(self.fps)
    def start(self,setup, loop):
        setup()
        while not self.stop:
            loop()
            self.run()

    def update_screen(self):
        game.display.update()

class SpriteGroup:
    def __init__(self):
        self.sprite_group = []

    def add(self, sprite):
        self.sprite_group.append(sprite)

    def remove(self, sprite):
        if sprite in self.sprite_group:
            self.sprite_group.remove(sprite)

    def clear(self):
        self.sprite_group = []

    def show(self, window):
        for sprite in self.sprite_group:
            sprite.reset(window)

    def collideSingleSpriteWith(self, sprite, sprite1_kill=False, sprite2_kill=False):
        for i in range(len(self.sprite_group)):
            if self.sprite_group[i].collideWith(sprite):
                if sprite1_kill:
                    self.sprite_group[i].kill()
                    self.remove(self.sprite_group[i])
                if sprite2_kill:
                    sprite.kill()
                return (True, i)
        return (False,None)
    def collidegroup(self, sprite, sprite1_kill=False, sprite2_kill=False):
        try:
            for i in range(len(self.sprite_group)):
                for a in range(len(sprite)):
                    if self.sprite_group[i].collideWith(sprite.sprite_group[a]):
                        if sprite1_kill:
                            self.sprite_group[i].kill()
                            self.remove(self.sprite_group[i])
                        if sprite2_kill:
                            sprite.sprite_group[a].kill()
                            sprite.remove(sprite.sprite_group[a])
                        return True
            return False
        except:
            ValueError("Sprite must be list")
    
    def filter(self, condition):
        return [sprite for sprite in self.sprite_group if condition(sprite)]
    def __iter__(self):
        return iter(self.sprite_group)

def color(color):
    return game.Color(color)

def group():
    return game.sprite.Group()

