"""Application class."""

import sys
import pygame
from time import time
from . import Game
import pygame_gui
from .MainMenu import MainMenu
from .Enemy import EnemyTank
from .GameObject import GameOver


class Application:
  """Main entry point for DendyTanks game."""

  def __init__(self):
    """Init app window and some other similar stuff, then run main menu."""
    pygame.init()
    self.screenWidth = 640
    self.screenHeight = 480
    screenSize = (self.screenWidth, self.screenHeight)
    self.screen = pygame.display.set_mode(screenSize)
    Game.ui_manager = pygame_gui.UIManager(screenSize)
    self.time = time()
    self.game_over_screen = False
    self.menu = MainMenu()

  def mainloop(self):
    """App mainloop, iteratively call `handleEvents`, `update` and `render`."""
    while 1:
      self.handleEvents()
      self.update()
      self.render()

  def update(self):
    """Calculete delta time, then update all objects and UI."""
    prevTime = self.time
    self.time = time()
    dt = self.time - prevTime
    for obj in Game.all_objects:
      obj.update(dt)
    Game.ui_manager.update(dt)
    Game.current_mode.update(dt)

  def render(self):
    """Draw scene, all objects, UI and then display backbuffer."""
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
    """Forward all events from pygame to game objects and UI."""
    for event in pygame.event.get():
      if event.type == pygame.USEREVENT and event.user_type == "MAINMENU":
        Game.all_objects.append(GameOver())
        self.game_over_screen = True
        pygame.event.clear()
      if event.type == pygame.QUIT:
        sys.exit()
      if self.game_over_screen and event.type == pygame.KEYDOWN:
        Game.all_objects[:] = []
        self.game_over_screen = False
        self.menu = MainMenu()
      for obj in Game.all_objects:
        if type(obj) != EnemyTank:
          obj.handleEvent(event)
      Game.ui_manager.process_events(event)
      Game.current_mode.handleEvent(event)
    for obj in Game.all_objects:
      if type(obj) == EnemyTank:
        obj.handleEvent(None)
