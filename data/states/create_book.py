import pygame as pg

from .. import tools, prepare

from ..components.labels import Textbox
from ..components.book import Flipbook


class CreateBook(tools._State):
    def __init__(self):
        super(CreateBook, self).__init__()

    def startup(self, persistent):
        self.persist = persistent
        self.textbox = Textbox({"center": prepare.SCREEN_RECT.center},
                                        call=self.make_book,
                                        type_sound=prepare.SFX["key1"],
                                        final_sound=prepare.SFX["typewriter-bell"])

    def make_book(self, book_name):
        self.persist["flipbook"] = Flipbook(book_name, prepare.SCREEN_SIZE)
        self.done = True
        self.next = "GAMEPLAY"

    def get_event(self,event):
        if event.type == pg.QUIT:
            self.quit = True
        elif event.type == pg.KEYUP:
            if event.key == pg.K_ESCAPE:
                self.quit = True
            elif event.key == pg.K_SPACE:
                self.done = True
                self.next = "VIEW_BOOK"
                self.persist["flipbook"] = self.flipbook
        self.textbox.get_event(event)

    def update(self, dt):
        self.textbox.update(dt)

    def draw(self, surface):
        self.textbox.draw(surface)
