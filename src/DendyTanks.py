"""todo: write some text here."""

import sys
import os
import pygame
from time import time
import Game
import pygame_gui
from MainMenu import MainMenu
from Enemy import EnemyTank


class DendyTanks:
    """Main class for DendyTanks game."""

    def __init__(self):
        pygame.init()
        self.screenWidth = 640
        self.screenHeight = 480
        screenSize = (self.screenWidth, self.screenHeight)
        self.screen = pygame.display.set_mode(screenSize)
        Game.ui_manager = pygame_gui.UIManager(screenSize)
        self.time = time()
        MainMenu()

    def mainloop(self):
        while 1:
            self.handleEvents()
            self.update()
            self.render()

    def update(self):
        prevTime = self.time
        self.time = time()
        dt = self.time - prevTime
        for obj in Game.all_objects:
            obj.update(dt)
        Game.ui_manager.update(dt)
        Game.current_mode.update(dt)

    def render(self):
        backGroundColor = (20, 20, 100)
        self.screen.fill(backGroundColor)
        if Game.current_scene is not None:
            Game.current_scene.render()
            sceneSurface = Game.current_scene.surface
            for obj in Game.all_objects:
                obj.render(sceneSurface)
            screenSubsurface = self.screen.subsurface(0, 0, self.screenHeight, self.screenHeight)
            pygame.transform.smoothscale(sceneSurface, (self.screenHeight, self.screenHeight),
                                         screenSubsurface)
        Game.ui_manager.draw_ui(self.screen)
        pygame.display.flip()

    def handleEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            for obj in Game.all_objects:
                if type(obj) != EnemyTank:
                    obj.handleEvent(event)
            Game.ui_manager.process_events(event)
            Game.current_mode.handleEvent(event)
        for obj in Game.all_objects:
            if type(obj) == EnemyTank:
                obj.handleEvent(None)


def main():
    """Change working directory to project folder and call mainloop."""
    srcDir = os.path.dirname(__file__)
    projectDir = os.path.join(srcDir, "..")
    os.chdir(projectDir)
    DendyTanks().mainloop()


if __name__ == "__main__":
    main()
