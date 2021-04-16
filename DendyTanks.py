'''
todo: write some text here.
'''

import sys
import pygame
from pygame.math import Vector2
from time import time


class DendyTanks:
  """Main class for DendyTanks game"""
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


class GameObject():
  """Class that represents every object in game, such as tank or bullet."""
  def __init__(self, resourceName):
    self.coords = Vector2(0, 0)
    self.speed = Vector2(0, 0)
    self.image = pygame.image.load(resourceName) if resourceName else None
    self.rect = self.image.get_rect()

  def update(self, dt, control=None):
    self.coords += dt * self.speed
    self.rect.update(self.coords, self.rect.size)

  def render(self, screen):
    screen.blit(self.image, self.rect)


class PlayerTank(GameObject):
  def __init__(self, pos):
    super().__init__("res/playerTank.png")
    self.coords = pos

  def update(self, dt, control):
    direction = Vector2(0, 0)
    if pygame.K_UP in control.pressedKeys:
      direction = Vector2(0, -1)
    elif pygame.K_DOWN in control.pressedKeys:
      direction = Vector2(0, 1)
    elif pygame.K_LEFT in control.pressedKeys:
      direction = Vector2(-1, 0)
    elif pygame.K_RIGHT in control.pressedKeys:
      direction = Vector2(1, 0)
    self.speed = direction * 120
    super().update(dt, control)


class Control():
  """Contain input from user"""
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
