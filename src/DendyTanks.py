"""todo: write some text here."""

import sys
import os
import pygame
from pygame.math import Vector2
from time import time
from GameObject import PlayerTank
from pygame import freetype
import gettext

# todo: move it outside from here, because now localization not work when run not from
# project root folder. maybe create separate file with only localization messages
gettext.install("all", "localization")


class DendyTanks:
  """Main class for DendyTanks game."""
  def __init__(self):
    pygame.init()
    self.screenWidth = 640
    self.screenHeight = 480
    self.screen = pygame.display.set_mode((640, 480))
    self.time = time()
    self.allObjects = []
    self.allObjects.append(PlayerTank(Vector2(320, 240)))
    self.control = Control()

    myfont = freetype.SysFont("Liberation Sans", 30)
    text = _("Use arrows (←, ↑, →, ↓) to move your tank.")
    self.tutorialMsg, rect = myfont.render(text, (255, 255, 255))

  def mainloop(self):
    while 1:
      self.control.handleEvents()
      self.update()
      self.render()

  def update(self):
    prevTime = self.time
    self.time = time()
    dt = self.time - prevTime
    for obj in self.allObjects:
      obj.update(dt, self.control)

  def render(self):
    backGroundColor = (20, 20, 100)
    self.screen.fill(backGroundColor)
    for obj in self.allObjects:
      obj.render(self.screen)
    self.screen.blit(self.tutorialMsg, (0, 0))
    pygame.display.flip()


class Control():
  """Contain input from user."""

  def __init__(self):
    self.pressedKeys = set()

  def handleEvents(self):
    for event in pygame.event.get():
      # print(event)
      if event.type == pygame.QUIT:
        sys.exit()
      elif event.type == pygame.KEYDOWN:
        self.pressedKeys.add(event.key)
      elif event.type == pygame.KEYUP:
        self.pressedKeys.discard(event.key)


def main():
  """Change working directory to project folder and call mainloop."""
  srcDir = os.path.dirname(__file__)
  projectDir = os.path.join(srcDir, "..")
  os.chdir(projectDir)
  DendyTanks().mainloop()


if __name__ == "__main__":
  main()
