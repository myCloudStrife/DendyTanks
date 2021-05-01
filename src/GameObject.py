"""Module with GameObject class."""
import pygame
from pygame.math import Vector2
from pygame import Rect
import Game


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

  def handleEvent(self, event):
    """Handle event by object.

    :param pygame.event.EventType event: event to be handled
    """
    pass

  def update(self, dt):
    """Update object."""
    self.pos += dt * self.vel
    self.rect.topleft = self.pos

  def render(self, screen):
    """Render object to the screen."""
    if self.image:
      screen.blit(self.image, self.rect)


class CollidableGameObject(GameObject):
  """GameObject with collision."""

  def testCollision(self, rect):
    """Test if object collides with rect."""
    return self.rect.colliderect(rect)

  def update(self, dt):
    """Update object with collision."""
    oldPos = self.pos.xy
    super().update(dt)

    collide = Game.current_scene.testCollision(self.rect)
    for obj in Game.all_objects:
      if hasattr(obj, "testCollision") and self != obj:
        collide |= obj.testCollision(self.rect)
    if collide:
      self.pos = oldPos
      self.rect.topleft = self.pos


class PlayerTank(CollidableGameObject):
  """
  Player's tank class.

  It has own texture and control support.
  """

  def __init__(self, **kwargs):
    """Construct PlayerTank."""
    super().__init__("res/playerTank.png", **kwargs)
    self.pressedKeys = []
    self.baseImage = self.image.copy()

  def handleEvent(self, event):
    """Handle movements keys and shoot key."""
    if event.type == pygame.KEYDOWN:
      if event.key in (pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT):
        self.pressedKeys.append(event.key)

    elif event.type == pygame.KEYUP:
      if event.key in (pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT):
        self.pressedKeys.remove(event.key)

  def update(self, dt):
    """Update tank's speed based on pressed keys and call GameObject's update."""
    speed = 2 * self.rect.width
    halfCellSize = Game.current_scene.cellSize / 2
    if len(self.pressedKeys) > 0:
      if self.pressedKeys[-1] == pygame.K_UP:
        self.vel = Vector2(0, -speed)
        self.image = pygame.transform.rotate(self.baseImage, 0)
        self.pos.x = round(self.pos.x / halfCellSize) * halfCellSize
      elif self.pressedKeys[-1] == pygame.K_DOWN:
        self.vel = Vector2(0, speed)
        self.image = pygame.transform.rotate(self.baseImage, 180)
        self.pos.x = round(self.pos.x / halfCellSize) * halfCellSize
      elif self.pressedKeys[-1] == pygame.K_LEFT:
        self.vel = Vector2(-speed, 0)
        self.image = pygame.transform.rotate(self.baseImage, 90)
        self.pos.y = round(self.pos.y / halfCellSize) * halfCellSize
      elif self.pressedKeys[-1] == pygame.K_RIGHT:
        self.vel = Vector2(speed, 0)
        self.image = pygame.transform.rotate(self.baseImage, 270)
        self.pos.y = round(self.pos.y / halfCellSize) * halfCellSize
    else:
      self.vel = Vector2(0, 0)
    super().update(dt)
