"""todo: write some text here."""

import sys
import os
import pygame
from pygame.math import Vector2
from time import time
from GameObject import PlayerTank
from Scene import Scene
from pygame import freetype
import Game
import gettext

# todo: move it outside from here, because now localization not work when run not from
# project root folder. maybe create separate file with only localization messages
gettext.install("all", "localization")


class DendyTanks:
  """Main class for DendyTanks game."""

  def __init__(self):
    pygame.init()
    self.screenWidth = 640
    self.screenHeight = 480
    self.screen = pygame.display.set_mode((640, 480))
    self.time = time()
    Game.current_scene = Scene("res/level0.txt")
    self.sceneSurface = pygame.Surface(Game.current_scene.bbox.size)
    print("Use {}x{} texture for intermediate rendering".format(
      self.sceneSurface.get_width(), self.sceneSurface.get_height()))

    Game.all_objects.append(PlayerTank(pos=Vector2(320, 240), size=Game.current_scene.cellSize))

    myfont = freetype.SysFont("Liberation Sans", 30)
    text = _("Use arrows (←, ↑, →, ↓) to move your tank.")
    self.tutorialMsg, rect = myfont.render(text, (255, 255, 255))

  def mainloop(self):
    while 1:
      self.handleEvents()
      self.update()
      self.render()

  def update(self):
    prevTime = self.time
    self.time = time()
    dt = self.time - prevTime
    for obj in Game.all_objects:
      obj.update(dt)

  def render(self):
    backGroundColor = (20, 20, 100)
    self.screen.fill(backGroundColor)
    Game.current_scene.render(self.sceneSurface)
    for obj in Game.all_objects:
      obj.render(self.sceneSurface)
    sceneSubsurface = self.screen.subsurface(0, 0, self.screenHeight, self.screenHeight)
    pygame.transform.smoothscale(self.sceneSurface, (self.screenHeight, self.screenHeight),
                                 sceneSubsurface)
    self.screen.blit(self.tutorialMsg, (0, 0))
    pygame.display.flip()

  def handleEvents(self):
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        sys.exit()
      for obj in Game.all_objects:
        obj.handleEvent(event)


def main():
  """Change working directory to project folder and call mainloop."""
  srcDir = os.path.dirname(__file__)
  projectDir = os.path.join(srcDir, "..")
  os.chdir(projectDir)
  DendyTanks().mainloop()


if __name__ == "__main__":
  main()
