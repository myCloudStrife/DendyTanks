"""Module with GameObject class."""
import pygame
from pygame.math import Vector2


class GameObject():
  """Class that represents every object in game, such as tank or bullet."""

  def __init__(self, resourceName):
    """Construct GameObject."""
    self.coords = Vector2(0, 0)
    self.speed = Vector2(0, 0)
    self.image = pygame.image.load(resourceName) if resourceName else None
    self.rect = self.image.get_rect()

  def update(self, dt, control=None):
    """Update object."""
    self.coords += dt * self.speed
    self.rect.update(self.coords, self.rect.size)

  def render(self, screen):
    """Render object to the screen."""
    screen.blit(self.image, self.rect)


class PlayerTank(GameObject):
  """
  Player's tank class.

  It has own texture and control support.
  """

  def __init__(self, pos: Vector2):
    """
    Construct ``GameObject`` with special texture and place it to ``pos``.

    :param pos: coordinates where to place player tank.
    """
    super().__init__("res/playerTank.png")
    self.coords = pos

  def update(self, dt, control):
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
    self.speed = direction * 120
    super().update(dt, control)
