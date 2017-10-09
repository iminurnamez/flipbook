import os

import pygame as pg

from .. import tools, prepare
from ..components.labels import Label, Button, ButtonGroup
from ..components.book import Flipbook, FlipbookPage


class TitleScreen(tools._State):
    def __init__(self):
        super(TitleScreen, self).__init__()
        self.title = Label("Flipbook", {"midtop": prepare.SCREEN_RECT.midtop},
                                font_size=32)
        self.make_book_buttons()
        Button({"midtop": (prepare.SCREEN_RECT.centerx, 80)}, self.buttons,
                  text="Create New Book", fill_color="gray50",
                  button_size=(240, 40), call=self.new_book)

    def make_book_buttons(self):
        books = []
        p = os.path.join("resources", "saved")
        book_names = sorted(os.listdir(p))
        left, top = 120, 200
        self.buttons = ButtonGroup()
        for book_name in book_names:
            book_path = os.path.join(p, book_name)
            Button({"topleft": (left, top)}, self.buttons, button_size=(240, 40),
                      fill_color="gray50", text=book_name, call=self.load_book,
                      args=book_path)
            left += 300
            if left > prepare.SCREEN_RECT.right - 300:
                top += 100
                left = 120

    def new_book(self, *args):
        self.done = True
        self.next = "CREATE_BOOK"

    def make_loading_screen(self, book_name):
        surf = pg.Surface(prepare.SCREEN_SIZE)
        surf.fill(pg.Color("dodgerblue"))
        text = "Loading {}".format(book_name)
        label = Label(text, {"center": prepare.SCREEN_RECT.center}, font_size=32)
        label.draw(surf)
        pg.display.get_surface().blit(surf, (0, 0))
        pg.display.update()

    def load_book(self, book_path):
        book_name = os.path.split(book_path)[1]
        self.make_loading_screen(book_name)
        page_names = sorted(os.listdir(book_path),
                                       key=lambda x: int(os.path.splitext(x)[0]))
        pages = []
        for page_name in page_names:
            page_path = os.path.join(book_path, page_name)
            layer_names = sorted(os.listdir(page_path),
                                          key=lambda x: int(os.path.splitext(x)[0]))
            layers = []
            for layer_name in layer_names:
                img = pg.image.load(os.path.join(page_path, layer_name))
                layers.append(img)
            pages.append(layers)
        size = img.get_size()
        pages = [FlipbookPage(i, size, layers[0].get_at((0, 0)), layers)
                    for i, layers in enumerate(pages)]
        self.persist["flipbook"] = Flipbook(book_name, size, pages)
        self.done = True
        self.next = "GAMEPLAY"

    def startup(self, persistent):
        self.persist = persistent

    def get_event(self,event):
        if event.type == pg.QUIT:
            self.quit = True
        elif event.type == pg.KEYUP:
            if event.key == pg.K_ESCAPE:
                self.quit = True
        self.buttons.get_event(event)

    def update(self, dt):
        mouse_pos = pg.mouse.get_pos()
        self.buttons.update(mouse_pos)

    def draw(self, surface):
        surface.fill(pg.Color("dodgerblue"))
        self.title.draw(surface)
        self.buttons.draw(surface)
