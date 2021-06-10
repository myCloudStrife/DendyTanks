"""Spawner that can spawn tanks (player and enemies)."""

from GameObject import GameObject
import Game
from pygame import gfxdraw
import random
from Enemy import EnemyTank


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
    self.cooldown -= dt
    if self.spawnedObject is None:
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
    if 0 < self.cooldown < 1 and self.spawnsLeft:
      x, y = self.rect.center
      r = self.rect.w * (1.0 - self.cooldown) * 0.5
      endAngle = self.startAngle + (1.0 - self.cooldown) * 360
      gfxdraw.pie(screen, x, y, int(r), self.startAngle, int(endAngle), (255, 255, 255))
    else:
      if type(self.spawnedObject) == EnemyTank and self.cooldown <= -0.5:
        self.spawnedObject.is_active = True
