"""Module with GameObject class."""
import pygame
from pygame.math import Vector2
from pygame import Rect


class GameObject():
  """Class that represents every object in game, such as tank or bullet."""

  def __init__(self, resourceName, pos=Vector2(0, 0), size=0):
    """Construct GameObject.

    :param str resourceName: path to texture
    :param pygame.math.Vector2 pos: object's initial position
    :param int size: size for object's Rect
    """
    self.pos = pos
    self.vel = Vector2(0, 0)
    self.image = pygame.image.load(resourceName) if resourceName else None
    if self.image and size == 0:
      size = self.image.width
    self.image = pygame.transform.scale(self.image, (size, size))
    self.rect = Rect(pos, Vector2(size, size))

  def update(self, dt, control=None, collision=None):
    """Update object."""
    oldPos = self.pos.xy
    self.pos += dt * self.vel
    self.rect.topleft = self.pos
    if collision and collision(self.rect):
      self.pos = oldPos
      self.rect.topleft = self.pos

  def render(self, screen):
    """Render object to the screen."""
    if self.image:
      screen.blit(self.image, self.rect)


class PlayerTank(GameObject):
  """
  Player's tank class.

  It has own texture and control support.
  """

  def __init__(self, **kwargs):
    """Construct PlayerTank."""
    super().__init__("res/playerTank.png", **kwargs)

  def update(self, dt, control, collision):
    """Update tank's speed based on pressed keys and call GameObject's update."""
    direction = Vector2(0, 0)
    if pygame.K_UP in control.pressedKeys:
      direction = Vector2(0, -1)
    elif pygame.K_DOWN in control.pressedKeys:
      direction = Vector2(0, 1)
    elif pygame.K_LEFT in control.pressedKeys:
      direction = Vector2(-1, 0)
    elif pygame.K_RIGHT in control.pressedKeys:
      direction = Vector2(1, 0)
    self.vel = direction * 2 * self.rect.width
    super().update(dt, control, collision)
