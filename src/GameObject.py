"""Module with GameObject class."""
import pygame
import pygame_gui
from pygame import Rect
from pygame.math import Vector2
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
        if self.image:
            if size == 0:
                size = self.image.width
            self.image = pygame.transform.scale(self.image, (size, size))
        self.rect = Rect(pos, Vector2(size, size))
        self.is_active = False

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

    def shoot(self, pos, size, vel, color):
        bullet = Bullet(self, pos=pos, size=size, color=color)
        bullet.vel = vel
        Game.all_objects.append(bullet)


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
        self.direction = Vector2(0, -1)
        self.is_active = True
        self.hp = 100
        self.kills = 0
        stats = Stats(self, color=(255, 1, 1))
        Game.all_objects.append(stats)


    def handleEvent(self, event):
        """Handle movements keys and shoot key."""
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT):
                self.pressedKeys.append(event.key)

        elif event.type == pygame.KEYUP:
            if event.key in self.pressedKeys:
                self.pressedKeys.remove(event.key)

        self.updateVelocity()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            halfCellSize = self.rect.w / 2
            bulletSize = halfCellSize // 2
            bulletCenter = self.rect.center + self.direction * (halfCellSize + bulletSize / 2)
            bulletPos = bulletCenter - Vector2(bulletSize / 2, bulletSize / 2)
            bulletVel = self.direction * 4 * self.rect.w
            bulletColor = (255, 255, 255)
            self.shoot(bulletPos, bulletSize, bulletVel, bulletColor)

    def updateVelocity(self):
        """Update tank's velocity based on pressed keys."""
        speed = 2 * self.rect.width
        halfCellSize = self.rect.w / 2
        prevPos = self.pos.xy
        if len(self.pressedKeys) > 0:
            if self.pressedKeys[-1] == pygame.K_UP:
                self.direction = Vector2(0, -1)
                self.image = pygame.transform.rotate(self.baseImage, 0)
                self.pos.x = round(self.pos.x / halfCellSize) * halfCellSize
            elif self.pressedKeys[-1] == pygame.K_DOWN:
                self.direction = Vector2(0, 1)
                self.image = pygame.transform.rotate(self.baseImage, 180)
                self.pos.x = round(self.pos.x / halfCellSize) * halfCellSize
            elif self.pressedKeys[-1] == pygame.K_LEFT:
                self.direction = Vector2(-1, 0)
                self.image = pygame.transform.rotate(self.baseImage, 90)
                self.pos.y = round(self.pos.y / halfCellSize) * halfCellSize
            elif self.pressedKeys[-1] == pygame.K_RIGHT:
                self.direction = Vector2(1, 0)
                self.image = pygame.transform.rotate(self.baseImage, 270)
                self.pos.y = round(self.pos.y / halfCellSize) * halfCellSize
            self.vel = self.direction * speed
            self.rect.topleft = self.pos
            if Game.current_scene.testCollision(self.rect):
                self.pos = prevPos - (self.pos - prevPos)
        else:
            self.vel = Vector2(0, 0)


class Bullet(GameObject):
    """Bullet object."""

    def __init__(self, parent, color, **kwargs):
        """Construct bullet.

    :param GameObject parent: reference for tank who shooted
    """
        super().__init__(None, **kwargs)
        self.parent = parent
        self.color = color

    def update(self, dt):
        """Destroy scene bricks when hit them."""
        hit = False
        if Game.current_scene.testCollision(self.rect):
            Game.current_scene.damage(self.rect, Vector2.normalize(self.vel))
            hit = True
        for obj in Game.all_objects:
            if (hasattr(obj, "testCollision") and self != obj and
                    self.parent != obj and type(self.parent) != type(obj) and
                    obj.testCollision(self.rect) and obj.is_active is True):
                Game.all_objects.remove(obj)
                hit = True
        if hit:
            Game.all_objects.remove(self)
        super().update(dt)

    def render(self, screen):
        """Render bullet to the screen."""
        pygame.gfxdraw.filled_circle(screen, self.rect.centerx, self.rect.centery,
                                     self.rect.w // 2, self.color)


class Stats(GameObject):
  """Player stats object."""
  """"HP; kills; """

  def __init__(self, parent, color, **kwargs):
    """Construct users'stats.
    :param GameObject parent: reference for user's tank
    """
    super().__init__(None, **kwargs)
    self.parent = parent
    self.color = color
    self.max_hp = 100
    self.hp = self.parent.hp
    self.kills = self.parent.kills
    self.text = None
    self.text_height = 100
    Game.ui_manager.preload_fonts([{'name': 'fira_code', 'point_size': 18, 'style': 'regular'}])

  def update(self, dt):
    """Update user stats."""
    self.hp = self.parent.hp
    self.kills = self.parent.kills
    hp_string = "HP: " + str(self.hp) + "/" + str(self.max_hp)
    kills_string = "Kills: " + str(self.kills)

    screenSize = Game.ui_manager.window_resolution
    hintRect = Rect(0, 0, screenSize[1], self.text_height)
    if self.text is not None:
        self.text.kill()
    self.text = pygame_gui.elements.UITextBox(
      "<font size=\"5\">" + f"{hp_string}" + "<br />" + f"{kills_string}" + "</font>", hintRect, Game.ui_manager)
