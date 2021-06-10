"""Enemy tank."""

import pygame
import Game
from GameObject import CollidableGameObject
from pygame.math import Vector2
import random


class EnemyTank(CollidableGameObject):
  """Enemy tank class."""

  def __init__(self, **kwargs):
    """Construct EnemyTank."""
    super().__init__("res/enemyTank.png", **kwargs)
    self.baseImage = self.image.copy()
    self.direction = Vector2(0, -1)
    self.p_upd_dir = 0.02
    self.p_move = 0.7
    self.p_shoot = 0.0033
    random.seed(random.randint(0, 30), version=2)

  def updateDirection(self):
    """Rotate tank (and do some movements?)."""
    move = random.randint(0, 10)
    if 0 <= move <= 3:
      prevPos = self.pos.xy
      direct = Vector2(0, 0)
      r = 0
      if move == 0:
        direct = Vector2(0, -1)
        r = 0
      elif move == 1:
        direct = Vector2(0, 1)
        r = 180
      elif move == 2:
        direct = Vector2(-1, 0)
        r = 90
      elif move == 3:
        direct = Vector2(1, 0)
        r = 270
      self.direction = direct
      self.image = pygame.transform.rotate(self.baseImage, r)
      halfCellSize = self.rect.w / 2
      self.pos.y = round(self.pos.y / halfCellSize) * halfCellSize

      if Game.current_scene.testCollision(self.rect):
        self.pos = prevPos - (self.pos - prevPos)

      self.rect.topleft = self.pos

  def handleEvent(self, event):
    """Enemy movement logic."""
    if self.is_active is True and random.uniform(0.0, 1.0) < self.p_upd_dir:
      self.updateDirection()

    if self.is_active is True and random.uniform(0.0, 1.0) < self.p_move:
      speed = 2 * self.rect.width
      self.vel = self.direction * speed
    else:
      self.vel = Vector2(0, 0)

    if self.is_active is True and random.uniform(0.0, 1.0) < self.p_shoot:
      halfCellSize = self.rect.w / 2
      bulletSize = halfCellSize // 2
      bulletCenter = self.rect.center + self.direction * (halfCellSize + bulletSize / 2)
      bulletPos = bulletCenter - Vector2(bulletSize / 2, bulletSize / 2)
      bulletVel = self.direction * 2.5 * self.rect.w
      bulletColor = (255, 0, 0)
      self.shoot(bulletPos, bulletSize, bulletVel, bulletColor)
