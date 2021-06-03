"""Enemy tank."""

from GameObject import CollidableGameObject
from pygame.math import Vector2


class EnemyTank(CollidableGameObject):
  """Enemy tank class."""

  def __init__(self, **kwargs):
    """Construct EnemyTank."""
    super().__init__("res/enemyTank.png", **kwargs)
    self.baseImage = self.image.copy()
    self.direction = Vector2(0, -1)
