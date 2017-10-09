import pygame as pg

from .. import tools, prepare

from ..components.book import Flipbook


class ViewBook(tools._State):
    def __init__(self):
        super(ViewBook, self).__init__()
        self.view_rate = 250

    def startup(self, persistent):
        self.persist = persistent
        self.flipbook = self.persist["flipbook"]
        self.paused = False
        self.timer = 0
        self.page_num = 0
        self.page = self.flipbook.pages[self.page_num]
        self.flipped_page = None

    def get_event(self,event):
        if event.type == pg.QUIT:
            self.quit = True
        elif event.type == pg.KEYUP:
            if event.key == pg.K_ESCAPE:
                self.quit = True
            elif event.key == pg.K_p:
                self.paused = not self.paused
            elif event.key == pg.K_UP:
                if self.view_rate > 10:
                    self.view_rate -= 10
            elif event.key == pg.K_DOWN:
                self.view_rate += 10
            elif event.key == pg.K_SPACE:
                self.done = True
                self.next = "GAMEPLAY"

    def update(self, dt):
        self.flipbook.update(dt)
        if self.flipped_page is not None:
            self.flipped_page.update(dt)
        if not self.paused:
            self.timer += dt
            while self.timer >= self.view_rate:
                self.timer -= self.view_rate
                self.flip_page()

    def flip_page(self):
        self.page_num += 1
        if self.page_num > len(self.flipbook.pages) - 1:
            self.page_num = 0
        self.page = self.flipbook.pages[self.page_num]

    def draw(self, surface):
        surface.blit(self.page.layers[-1], (0, 0))
