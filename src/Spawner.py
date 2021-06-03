"""Spawner that can spawn tanks (player and enemies)."""

from GameObject import GameObject
import Game
from pygame import gfxdraw
import random


class Spawner(GameObject):
  """Spawner."""

  def __init__(self, objType, numSpawns=1, **kwargs):
    """Construct spawner.

    :param type objType: type of object to be spawned
    :param int numSpawns: number of allowed spawns
    :param pygame.math.Vector2 pos: spawner position
    """
    super().__init__(None, **kwargs)
    self.objType = objType
    self.cooldown = 1.0
    self.spawnedObject = None
    self.startAngle = random.randint(0, 359)
    self.spawnsLeft = numSpawns

  def update(self, dt):
    """Spawner update.

    If none object object spawned then update cooldown and spawn tank when it ready.
    In other case check for object presence.
    """
    if self.spawnedObject is None:
      self.cooldown -= dt
      if (self.cooldown < 0 and self.spawnsLeft > 0):
        self.spawnedObject = self.objType(pos=self.pos, size=self.rect.w)
        Game.all_objects.append(self.spawnedObject)
        self.spawnsLeft -= 1
    elif not (self.spawnedObject in Game.all_objects):
      self.spawnedObject = None
      self.cooldown = 2.0 + random.random() * 3
      self.startAngle = random.randint(0, 359)

  def render(self, screen):
    """Draw some animation before spawn."""
    if self.cooldown > 0 and self.cooldown < 1:
      x, y = self.rect.center
      r = self.rect.w * (1.0 - self.cooldown) * 0.5
      endAngle = self.startAngle + (1.0 - self.cooldown) * 360
      gfxdraw.pie(screen, x, y, int(r), self.startAngle, int(endAngle), (255, 255, 255))
