import pygame as pg

from .. import tools, prepare

from ..components.book import Flipbook


class Gameplay(tools._State):
    def __init__(self):
        super(Gameplay, self).__init__()

    def startup(self, persistent):
        self.persist = persistent
        try:
            self.flipbook = self.persist["flipbook"]
        except KeyError:
            self.flipbook = Flipbook("test1", prepare.SCREEN_SIZE)

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
        self.flipbook.get_event(event)

    def update(self, dt):
        self.flipbook.update(dt)

    def draw(self, surface):
        self.flipbook.draw(surface)
