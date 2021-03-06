"""Scene object that store all level's obstacles."""

from pygame.math import Vector2
from pygame.rect import Rect
import pygame
from pygame import gfxdraw
from . import Game
from .GameObject import PlayerTank
from .Enemy import EnemyTank
from .Spawner import Spawner


class Scene():
  """Scene.

  :var pygame.Rect bbox: scene bounding box
  :var int cellSize: size of single cell, for both X and Y axis
  :var list[pygame.Rect] bricks: list with brick blocks
  :var pygame.Surface surface: texture for scene rendering
  """

  def __init__(self, sceneName):
    """Load scene from file.

    :param str sceneName: file name with scene
    """
    w = -1
    h = 0
    self.bricks = []
    self.cellSize = 64
    with open(sceneName) as sceneFile:
      for line in sceneFile:
        line = line.rstrip()
        if w == -1:
          w = len(line)
        else:
          assert(w == len(line))
        for i, cell in enumerate(line):
          self._processCell(cell, Vector2(i, h))
        h += 1
    self.bbox = Rect(Vector2(0, 0), Vector2(w, h) * self.cellSize)
    try:
      self.bricksImage = pygame.image.load("res/bricks.png")
    except FileNotFoundError:
      self.bricksImage = pygame.image.load("../res/bricks.png")
    halfSize = self.cellSize // 2
    self.bricksImage = pygame.transform.scale(self.bricksImage, (halfSize, halfSize))
    self.surface = pygame.Surface(self.bbox.size)
    print("Use {}x{} texture for intermediate rendering".format(
      self.surface.get_width(), self.surface.get_height()))

  def _processCell(self, cell, pos):
    """Add cell to scene.

    :param str cell: type of cell
    :param pygame.math.Vector2 pos: cell position in scene
    """
    if cell == 'b':
      self.bricks.append(Rect(pos * self.cellSize, Vector2(1, 1) * self.cellSize))
    elif cell == '.':
      pass  # empty cell
    elif cell == 'p':
      Game.all_objects.append(Spawner(PlayerTank, pos=(pos * self.cellSize), size=self.cellSize))
    elif cell == 'e':
      Game.all_objects.append(Spawner(EnemyTank, numSpawns=10,
                                      pos=(pos * self.cellSize), size=self.cellSize))
    else:
      assert False, f"Unknown cell type \"{cell}\""

  def testCollision(self, rect):
    """Test collision between rect and scene.

    :param pygame.Rect rect: rectangle to be tested
    """
    fittedRect = rect.clamp(self.bbox)
    return fittedRect.topleft != rect.topleft or rect.collidelist(self.bricks) != -1

  def render(self):
    """Draw scene into its texture."""
    backgroundColor = (0, 0, 0)
    self.surface.fill(backgroundColor)

    for brick in self.bricks:
      points = [brick.topleft, brick.topright, brick.bottomright, brick.bottomleft]
      gfxdraw.textured_polygon(self.surface, points, self.bricksImage, 2, -1)

  def damage(self, rect, direction):
    """Damage scene obstacles.

    :param pygame.Rect rect: rectangle that dealing damage
    :param pygame.math.Vector2 direction: rectangle's movement direction
    """
    hits = rect.collidelistall(self.bricks)
    halfSize = self.cellSize // 2
    forRemove = []
    for idx in hits:
      b = self.bricks[idx]
      if b.w == self.cellSize:
        forRemove.append(idx)
        self.bricks.append(Rect((b.x, b.y), (halfSize, halfSize)))
        self.bricks.append(Rect((b.x + halfSize, b.y), (halfSize, halfSize)))
        self.bricks.append(Rect((b.x, b.y + halfSize), (halfSize, halfSize)))
        self.bricks.append(Rect((b.x + halfSize, b.y + halfSize), (halfSize, halfSize)))
        for idx in rect.collidelistall(self.bricks[-4:]):
          idx = -4 + idx
          b = self.bricks[idx]
          self.bricks[idx] = b.clip(Rect(Vector2(b.topleft) + direction * halfSize // 2, b.size))
      else:
        self.bricks[idx] = b.clip(Rect(Vector2(b.topleft) + direction * halfSize // 2, b.size))
        if self.bricks[idx].size == (0, 0):
          forRemove.append(idx)
    for idx in forRemove[-1::-1]:
      self.bricks.pop(idx)
