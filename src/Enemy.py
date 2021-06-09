"""Enemy tank."""

import pygame
import Game
from GameObject import CollidableGameObject
from pygame.math import Vector2
import random
import time


class EnemyTank(CollidableGameObject):
  """Enemy tank class."""

  def __init__(self, **kwargs):
    """Construct EnemyTank."""
    super().__init__("res/enemyTank.png", **kwargs)
    self.baseImage = self.image.copy()
    self.direction = Vector2(0, -1)
    self.p_move = 0.05
    self.p_shoot = 0.01


  def handleEvent(self, event):
    """Enemy movement logic"""

    if random.uniform(0.0, 1.0) < self.p_move:
      speed = 2 * self.rect.width
      halfCellSize = self.rect.w / 2
      prevPos = self.pos.xy
      move = random.randint(0, 30)
      if move == 0:
        self.direction = Vector2(0, -1)
        self.image = pygame.transform.rotate(self.baseImage, 0)
        self.pos.x = round(self.pos.x / halfCellSize) * halfCellSize
      elif move == 1:
        self.direction = Vector2(0, 1)
        self.image = pygame.transform.rotate(self.baseImage, 180)
        self.pos.x = round(self.pos.x / halfCellSize) * halfCellSize
      elif move == 2:
        self.direction = Vector2(-1, 0)
        self.image = pygame.transform.rotate(self.baseImage, 90)
        self.pos.y = round(self.pos.y / halfCellSize) * halfCellSize
      elif move == 3:
        self.direction = Vector2(1, 0)
        self.image = pygame.transform.rotate(self.baseImage, 270)
        self.pos.y = round(self.pos.y / halfCellSize) * halfCellSize
      self.vel = self.direction * speed
      self.rect.topleft = self.pos
      if Game.current_scene.testCollision(self.rect):
        self.pos = prevPos - (self.pos - prevPos)

    if random.uniform(0.0, 1.0) < self.p_shoot:
      halfCellSize = self.rect.w / 2
      bulletSize = halfCellSize // 2
      bulletCenter = self.rect.center + self.direction * (halfCellSize + bulletSize / 2)
      bulletPos = bulletCenter - Vector2(bulletSize / 2, bulletSize / 2)
      bulletVel = self.direction * 2.5 * self.rect.w
      bulletColor = (255, 0, 0)
      self.shoot(bulletPos, bulletSize, bulletVel, bulletColor)
