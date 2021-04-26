"""Scene object that store all level's obstacles."""

from pygame.math import Vector2
from pygame.rect import Rect
from pygame import gfxdraw


class Scene():
  """Scene.

  :var pygame.Rect bbox: scene bounding box
  :var int cellSize: size of single cell, for both X and Y axis
  :var list[pygame.Rect] bricks: list with brick blocks
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

  def _processCell(self, cell, pos):
    """Add cell to scene.

    :param str cell: type of cell
    :param pygame.math.Vector2 pos: cell position in scene
    """
    if cell == 'b':
      self.bricks.append(Rect(pos * self.cellSize, Vector2(1, 1) * self.cellSize))
    elif cell == '.':
      pass  # empty cell
    else:
      assert False, f"Unknown cell type \"{cell}\""

  def testCollision(self, rect):
    """Test collision between rect and scene.

    :param pygame.Rect rect: rectangle to be tested
    """
    fittedRect = rect.clamp(self.bbox)
    return fittedRect.topleft != rect.topleft or rect.collidelist(self.bricks) != -1

  def render(self, screen):
    """Draw scene.

    :param pygame.Surface screen: surface where you want to draw scene
    """
    backgroundColor = (0, 0, 0)
    screen.fill(backgroundColor)
    screenSize = screen.get_size()
    sceneToScreenScale = [s1 / s2 for s1, s2 in zip(screenSize, self.bbox.size)]

    def sceneToScreen(sceneRect):
      return Rect([coord * scale for coord, scale in zip(sceneRect.topleft, sceneToScreenScale)],
                  [size * scale for size, scale in zip(sceneRect.size, sceneToScreenScale)])

    for brick in self.bricks:
      r = sceneToScreen(brick)
      gfxdraw.box(screen, r, (255, 0, 0))
