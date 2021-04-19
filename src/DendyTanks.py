"""todo: write some text here."""

import sys
import pygame
from pygame.math import Vector2
from time import time
from GameObject import PlayerTank


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
  """Main application call"""
  DendyTanks().mainloop()


if __name__ == "__main__":
  main()
