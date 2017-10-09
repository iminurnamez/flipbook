import os
import shutil

import pygame as pg

from .. import prepare
from ..components.labels import Label


class FlipbookPage(object):
    def __init__(self, num, size, bg_color, layers=None):
        self.bg_color = bg_color
        if layers is not None:
            self.layers = layers
        else:
            layer = pg.Surface(size)
            layer.fill(bg_color)
            self.layers = [layer]

    def add_layer(self):
        self.layers.append(self.layers[-1].copy())

    def remove_layer(self):
        if len(self.layers) > 1:
            self.layers = self.layers[:-1]
        else:
            self.layers[-1].fill(self.bg_color)

    def copy_layers(self):
        return [layer.copy() for layer in self.layers]


class Flipbook(object):
    def __init__(self, book_name, size, pages=None):
        self.name = book_name
        self.size = size
        self.bg_color = pg.Color("white")
        self.color = pg.Color("black")
        self.line_weight = 4
        self.drawing = False
        if pages is not None:
            self.pages = pages
        else:    
            self.pages = [FlipbookPage(0, self.size, self.bg_color)]
        self.last_pos = None
        self.current_page_num = len(self.pages) - 1
        self.current_page = self.pages[self.current_page_num]
        self.current_line = []
        self.page_label = Label("{}".format(self.current_page_num),
                                        {"topright": (prepare.SCREEN_RECT.right - 5, 0)},
                                        text_color="gray20", font_size=32)               
        
    def get_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.pen_down()
        elif event.type == pg.MOUSEBUTTONUP:
            if event.button == 1:
                self.pen_up()
        elif event.type == pg.KEYUP:
            if event.key == pg.K_LEFT:
                self.previous_page()
            elif event.key == pg.K_RIGHT:
                self.next_page()
            elif pg.key.get_pressed()[pg.K_LCTRL] and not self.drawing:
                if event.key == pg.K_c:
                    self.copy()
                elif event.key == pg.K_z:
                    self.undo()
                elif event.key == pg.K_d:
                    self.delete_page()
                elif event.key == pg.K_s:
                    self.save()

    def copy(self):
        last_page = self.pages[self.current_page_num - 1]
        self.current_page.layers = last_page.copy_layers()

    def make_saving_screen(self):
        surf = pg.Surface(prepare.SCREEN_SIZE)
        surf.fill(pg.Color("dodgerblue"))
        text = "Saving {}".format(self.name)
        label = Label(text, {"center": prepare.SCREEN_RECT.center}, font_size=32)
        label.draw(surf)
        pg.display.get_surface().blit(surf, (0, 0))
        pg.display.update()
        
    def save(self):
        self.make_saving_screen()
        base_path = os.path.join("resources", "saved", self.name)
        try:
            os.mkdir(base_path)
        except:
            shutil.rmtree(base_path)
            os.mkdir(base_path)
        for page_num, page in enumerate(self.pages):
            path = os.path.join(base_path, "{}".format(page_num))
            os.mkdir(path)
            for i, layer in enumerate(self.pages[page_num].layers):
                pg.image.save(layer, os.path.join(path, "{}.png".format(i)))

    def delete_page(self):
        left = self.pages[:self.current_page_num]
        right = self.pages[self.current_page_num + 1:]
        self.pages = left + right
        if self.current_page_num > 0:
            self.current_page_num -= 1
        self.current_page = self.pages[self.current_page_num]
        
    def next_page(self):
        self.current_page_num += 1
        if self.current_page_num > len(self.pages) - 1:
            self.add_page()
        self.current_page = self.pages[self.current_page_num]

    def previous_page(self):
        if self.current_page_num > 0:
            self.current_page_num -= 1
            self.current_page = self.pages[self.current_page_num]

    def add_page(self):
        self.pages.append(
                FlipbookPage(self.current_page_num,
                                   self.size, self.bg_color))

    def pen_down(self):
        self.drawing = True

    def pen_up(self):
        self.drawing = False
        self.current_page.add_layer()
        layer = self.current_page.layers[-1]
        self.draw_lines(layer, self.color, self.current_line)
        self.current_line = []

    def draw_lines(self, surface, color, points):
        if len(points) > 1:
            pg.draw.lines(surface, color, False, points, self.line_weight)
        for p in points:
            pg.draw.circle(surface, color, p, self.line_weight // 2)

    def undo(self):
        self.current_page.remove_layer()

    def update(self, dt):
        mouse_pos = pg.mouse.get_pos()
        if self.drawing and mouse_pos != self.last_pos:
            self.current_line.append(mouse_pos)
        self.last_pos = mouse_pos
        self.page_label.set_text("{}".format(self.current_page_num))

    def draw(self, surface):
        if self.current_page.layers:
            surface.blit(self.current_page.layers[-1], (0, 0))
        if len(self.current_line) > 1:
            self.draw_lines(surface, self.color, self.current_line)
        if self.current_page_num:
            surf = self.pages[self.current_page_num - 1].layers[-1].copy()
            surf.set_colorkey(self.bg_color)
            surf.set_alpha(128)
            surface.blit(surf, (0, 0))     
        self.page_label.draw(surface)            