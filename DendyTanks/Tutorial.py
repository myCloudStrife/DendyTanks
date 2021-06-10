"""Tutorial game mode."""

from .GameMode import GameMode
from . import Game
from . import MainMenu
from .Scene import Scene
from . import Localization
import pygame
import pygame_gui
from pygame import Rect
from .GameObject import PlayerTank
from .Enemy import EnemyTank
from .Spawner import Spawner
from pygame.math import Vector2


class Tutorial(GameMode):
  """Special game mode."""

  def __init__(self) -> None:
    """Load special scene."""
    super().__init__()
    Game.stats_required = False
    Game.current_scene = Scene("res/levels/tutorial.txt")
    self.curTime = 0.0
    self.moveHint = False
    self.shootHint = False
    self.killHint = False
    self.prevEnemies = 0
    self.killed = 0
    Game.ui_manager.preload_fonts([{'name': 'fira_code', 'point_size': 18, 'style': 'regular'}])

  def update(self, dt):
    """Show tutorial messages when it necessary."""
    self.curTime += dt

    screenSize = Game.ui_manager.window_resolution
    hintRect = Rect(10, 10, screenSize[1] - 10, 100)
    if not self.moveHint and self.curTime > 1:
      self.hintText = pygame_gui.elements.UITextBox(
        "<font size=\"5\">" + Localization.TUTORIAL_MOVEMENT + "</font>",
        hintRect, Game.ui_manager)
      # seems TEXT_EFFECT_FADE_IN/TEXT_EFFECT_FADE_OUT don't work :(
      self.hintText.set_active_effect(pygame_gui.TEXT_EFFECT_TYPING_APPEAR)
      self.playerTank = None
      for obj in Game.all_objects:
        if isinstance(obj, PlayerTank):
          self.playerTank = obj
      assert self.playerTank is not None
      self.startPos = Vector2(self.playerTank.pos)
      self.moveHint = True

    if (not self.shootHint and self.curTime > 3 and
        self.startPos.distance_to(self.playerTank.pos) > Game.current_scene.cellSize):
      self.hintText.kill()
      self.hintText = pygame_gui.elements.UITextBox(
        "<font size=\"5\">" + Localization.TUTORIAL_SHOOTING + "</font>",
        hintRect, Game.ui_manager)
      self.hintText.set_active_effect(pygame_gui.TEXT_EFFECT_TYPING_APPEAR)
      self.numShoots = 0
      self.shootHint = True

    numEnemies = 0
    for obj in Game.all_objects:
      if isinstance(obj, EnemyTank):
        numEnemies += 1

    if not self.killHint and self.shootHint and self.numShoots > 3:
      self.hintText.kill()
      self.hintText = pygame_gui.elements.UITextBox(
        "<font size=\"5\">" + Localization.TUTORIAL_KILL + f" (0/{numEnemies})" + "</font>",
        hintRect, Game.ui_manager)
      self.hintText.set_active_effect(pygame_gui.TEXT_EFFECT_TYPING_APPEAR)
      self.killHint = True
      for obj in Game.all_objects:
        if isinstance(obj, Spawner):
          obj.spawnsLeft = 0

    if self.killHint and numEnemies != self.prevEnemies:
      self.killed += self.prevEnemies - numEnemies
      self.hintText.kill()
      self.hintText = pygame_gui.elements.UITextBox(
        "<font size=\"5\">" + Localization.TUTORIAL_KILL +
        f" ({self.killed}/{self.killed+numEnemies})" + "</font>",
        hintRect, Game.ui_manager)

    if self.killHint and numEnemies == 0:
      Game.stats_required = True
      MainMenu.MainMenu()  # todo: show some message

    self.prevEnemies = numEnemies

  def handleEvent(self, event):
    """Count number of shoots for shooting hint."""
    if self.shootHint and event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
      self.numShoots += 1
