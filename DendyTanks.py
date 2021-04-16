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
    playerTank = GameObject("res/playerTank.png")
    playerTank.coords = Vector2(320, 240)
    self.allObjects.append(playerTank)

  def mainloop(self):
    while 1:
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          sys.exit()
      self.update()
      self.render()

  def update(self):
    prevTime = self.time
    self.time = time()
    dt = self.time - prevTime
    for obj in self.allObjects:
      obj.update(dt)

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

  def update(self, dt):
    self.coords += dt * self.speed
    self.rect.update(self.coords, self.rect.size)

  def render(self, screen):
    screen.blit(self.image, self.rect)


def main():
  """Main application call"""
  DendyTanks().mainloop()


if __name__ == "__main__":
  main()
