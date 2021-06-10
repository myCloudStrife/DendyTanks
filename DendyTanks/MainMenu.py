"""Main menu module."""

from . import Game
import pygame_gui
import pygame
from .GameMode import GameMode, DefaultGameMode
from pygame import Rect
from . import Localization
import importlib
import os
from . import Tutorial


class MainMenu(GameMode):
  """Main menu."""

  def __init__(self):
    """Draw menu layout."""
    super().__init__()
    screenSize = Game.ui_manager.window_resolution

    Game.ui_manager = pygame_gui.UIManager(screenSize, "res/themes/main_menu.json")
    x, y, w, h = 0.2, 0.2, 0.6, 0.2
    rect = Rect(x * screenSize[0], y * screenSize[1], w * screenSize[0], h * screenSize[1])
    Game.ui_manager.preload_fonts([{'name': 'fira_code', 'point_size': 48, 'style': 'bold'}])
    pygame_gui.elements.UITextBox(
      "<font size=\"7\"><b>DendyTanks</b></font>",  # todo: better to replace with image
      rect, Game.ui_manager)

    x, y, w, h = 0.35, 0.45, 0.3, 0.1
    rect = Rect(x * screenSize[0], y * screenSize[1], w * screenSize[0], h * screenSize[1])
    self.tutorialButton = pygame_gui.elements.UIButton(
      rect, Localization.MAIN_MENU_TUTORIAL, Game.ui_manager)

    x, y, w, h = 0.35, 0.6, 0.3, 0.1
    rect = Rect(x * screenSize[0], y * screenSize[1], w * screenSize[0], h * screenSize[1])
    self.playButton = pygame_gui.elements.UIButton(
      rect, Localization.MAIN_MENU_PLAY, Game.ui_manager)

    x, y, w, h = 0.35, 0.75, 0.3, 0.1
    rect = Rect(x * screenSize[0], y * screenSize[1], w * screenSize[0], h * screenSize[1])
    self.langButton = pygame_gui.elements.UIButton(
      rect, Localization.MAIN_MENU_LANGUAGE, Game.ui_manager)

    self.applyButton = None

  def handleEvent(self, event):
    """Check if any button is pressed."""
    if event.type == pygame.USEREVENT and event.user_type == pygame_gui.UI_BUTTON_PRESSED:
      if event.ui_element == self.tutorialButton:
        Tutorial.Tutorial()
      elif event.ui_element == self.playButton:
        DefaultGameMode()
      elif event.ui_element == self.langButton:
        screenSize = Game.ui_manager.window_resolution
        x, y, w, h = 0.3, 0.3, 0.4, 0.4
        rect = Rect(x * screenSize[0], y * screenSize[1], w * screenSize[0], h * screenSize[1])
        self.langWin = pygame_gui.elements.UIWindow(rect, Game.ui_manager)
        winSize = self.langWin.get_container().get_size()
        x, y, w, h = 0, 0, 1, 0.8
        rect = Rect(x * winSize[0], y * winSize[1], w * winSize[0], h * winSize[1])
        self.langList = pygame_gui.elements.UISelectionList(
            rect, Localization.SUPPORTED_LANGUAGES.keys(), Game.ui_manager,
            container=self.langWin, parent_element=self.langWin)
        x, y, w, h = 0, 0.8, 1, 0.2
        rect = Rect(x * winSize[0], y * winSize[1], w * winSize[0], h * winSize[1])
        self.applyButton = pygame_gui.elements.UIButton(
          rect, Localization.MAIN_MENU_APPLY, Game.ui_manager,
          container=self.langWin)
      elif event.ui_element == self.applyButton:
        selected = self.langList.get_single_selection()
        if selected in Localization.SUPPORTED_LANGUAGES:
          os.environ["LC_ALL"] = Localization.SUPPORTED_LANGUAGES[selected]
          importlib.reload(Localization)
          MainMenu()
        self.langWin.kill()
