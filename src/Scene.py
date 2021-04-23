"""Scene object that store all level's obstacles."""

from pygame.math import Vector2
from pygame.rect import Rect
from pygame import gfxdraw


class Scene():
  """Scene.

  :var Rect bbox: scene bounding box
  :var List[Rect] bricks: list with brick blocks
  """

  def __init__(self, sceneName):
    """Scene constructor."""
    w = -1
    h = 0
    self.bricks = []
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
    self.bbox = Rect(Vector2(0, 0), Vector2(w, h))

  def _processCell(self, cell, pos):
    """Add cell to scene.

    :param char cell: type of cell
    :param Vector2 pos: cell position in scene
    """
    if cell == 'b':
      self.bricks.append(Rect(pos, Vector2(1, 1)))
    elif cell == '.':
      pass  # empty cell
    else:
      assert False, f"Unknown cell type \"{cell}\""

  def render(self, screen):
    """Draw scene.

    :param Surface screen: surface where you want to draw scene
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
