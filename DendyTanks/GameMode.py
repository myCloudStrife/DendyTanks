"""Game mode interface."""

from . import Game
from .Scene import Scene


class GameMode:
  """Game mode interface."""

  def __init__(self) -> None:
    """Clear current state."""
    Game.current_scene = None
    Game.all_objects.clear()
    Game.ui_manager.clear_and_reset()
    Game.current_mode = self

  def update(self, dt):
    """Call by mainloop update every frame."""
    pass

  def handleEvent(self, event):
    """Call by mainloop handleEvent every frame."""
    pass


class DefaultGameMode(GameMode):
  """Load scene on init."""

  def __init__(self) -> None:
    """Load scene."""
    super().__init__()
    Game.current_scene = Scene("res/levels/level0.txt")
