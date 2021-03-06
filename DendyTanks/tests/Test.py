"""Unit tests."""

import unittest
import pygame
from pygame.math import Vector2
from DendyTanks.Application import Application
from DendyTanks import Game
from DendyTanks.GameObject import PlayerTank
from DendyTanks.GameObject import Bullet
from DendyTanks.Scene import Scene
from DendyTanks.Enemy import EnemyTank
from pygame.rect import Rect
import os
os.environ["SDL_VIDEODRIVER"] = "dummy"


class Test(unittest.TestCase):
    """Unit test class."""

    def setUp(self):
        """Det up for test."""
        srcDir = os.path.dirname(__file__)
        os.chdir(srcDir)
        self.app = Application()

    def test_init_application(self):
        """Test init application."""
        self.assertEqual((self.app.screenWidth, self.app.screenHeight,
                          self.app.game_over_screen), (640, 480, False), 'test_init_application')

    def test_player_tank_init(self):
        """Test player tank init."""
        Game.current_scene = Scene("../res/levels/level0.txt")
        tmp = PlayerTank(pos=Vector2(5, 5), size=10)
        tmp.update(dt=0.5)
        result = (tmp.pos, tmp.vel)
        response = (Vector2(5, 5), Vector2(0, 0))
        self.assertEqual(result, response, 'player_tank_init')

    def test_player_tank_key_reaction(self):
        """Test player tank key reation."""
        Game.current_scene = Scene("../res/levels/level0.txt")
        event = pygame.event.Event(pygame.USEREVENT, user_type='MAINMENU',
                                   ui_element=self.app.menu.playButton)
        pygame.event.post(event)
        tmp = PlayerTank(pos=Vector2(5, 5), size=10)
        tmp.update(dt=0.5)

        speed = 2 * tmp.rect.width

        event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_UP)
        tmp.handleEvent(event)
        self.assertEqual(tmp.direction, Vector2(0, -1), 'test_update_player_tank_dir_up')
        self.assertEqual(tmp.vel, Vector2(0, -speed), 'test_update_player_tank_vel_up')

        event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_DOWN)
        tmp.handleEvent(event)
        self.assertEqual(tmp.direction, Vector2(0, 1), 'test_update_player_tank_dir_down')
        self.assertEqual(tmp.vel, Vector2(0, speed), 'test_update_player_tank_vel_down')

        event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_LEFT)
        tmp.handleEvent(event)
        self.assertEqual(tmp.direction, Vector2(-1, 0), 'test_update_player_tank_dir_left')
        self.assertEqual(tmp.vel, Vector2(-speed, 0), 'test_update_player_tank_vel_left')

        event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RIGHT)
        tmp.handleEvent(event)
        self.assertEqual(tmp.direction, Vector2(1, 0), 'test_update_player_tank_dir_right')
        self.assertEqual(tmp.vel, Vector2(speed, 0), 'test_update_player_tank_vel_right')

    def test_player_tank_move_up(self):
        """Test player tank move up."""
        Game.current_scene = Scene("../res/levels/level0.txt")
        Game.current_scene.bbox = Rect(Vector2(-100000, -100000),
                                       Vector2(100000, 100000) * Game.current_scene.cellSize)
        event = pygame.event.Event(pygame.USEREVENT, user_type='MAINMENU',
                                   ui_element=self.app.menu.playButton)
        pygame.event.post(event)
        tmp = PlayerTank(pos=Vector2(0, 0), size=10)
        tmp.update(dt=0.5)

        dt = 10.0
        speed = 2 * tmp.rect.width

        event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_UP)
        tmp.handleEvent(event)
        self.assertEqual(tmp.pos, Vector2(0, 0), 'test_update_player_tank_pos_up')
        self.assertEqual(tmp.direction, Vector2(0, -1), 'test_update_player_tank_dir_up')
        self.assertEqual(tmp.vel, Vector2(0, -speed), 'test_update_player_tank_vel_up')
        tmp.update(dt=dt)
        self.assertEqual(tmp.pos, Vector2(0, -speed) * dt + Vector2(0, 0),
                         'test_update_player_tank_pos_up_update')
        self.assertEqual(tmp.direction, Vector2(0, -1), 'test_update_player_tank_dir_up_update')
        self.assertEqual(tmp.vel, Vector2(0, -speed), 'test_update_player_tank_vel_up_update')

    def test_player_tank_move_down(self):
        """Test player tank move down."""
        Game.current_scene = Scene("../res/levels/level0.txt")
        Game.current_scene.bbox = Rect(Vector2(-100000, -100000),
                                       Vector2(100000, 100000) * Game.current_scene.cellSize)
        event = pygame.event.Event(pygame.USEREVENT, user_type='MAINMENU',
                                   ui_element=self.app.menu.playButton)
        pygame.event.post(event)
        tmp = PlayerTank(pos=Vector2(5, 5), size=10)
        tmp.update(dt=0.5)

        dt = 10.0
        speed = 2 * tmp.rect.width

        event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_UP)
        tmp.handleEvent(event)
        self.assertEqual(tmp.pos, Vector2(5, 5), 'test_update_player_tank_pos_down')
        self.assertEqual(tmp.direction, Vector2(0, -1), 'test_update_player_tank_dir_down')
        self.assertEqual(tmp.vel, Vector2(0, -speed), 'test_update_player_tank_vel_down')
        tmp.update(dt=dt)
        self.assertEqual(tmp.pos, Vector2(0, -speed) * dt + Vector2(5, 5),
                         'test_update_player_tank_pos_down_update')
        self.assertEqual(tmp.direction, Vector2(0, -1), 'test_update_player_tank_dir_down_update')
        self.assertEqual(tmp.vel, Vector2(0, -speed), 'test_update_player_tank_vel_down_update')

    def test_player_tank_move_left(self):
        """Test player tank move left."""
        Game.current_scene = Scene("../res/levels/level0.txt")
        Game.current_scene.bbox = Rect(Vector2(-100000, -100000),
                                       Vector2(100000, 100000) * Game.current_scene.cellSize)
        event = pygame.event.Event(pygame.USEREVENT, user_type='MAINMENU',
                                   ui_element=self.app.menu.playButton)
        pygame.event.post(event)
        tmp = PlayerTank(pos=Vector2(5, 5), size=10)
        tmp.update(dt=0.5)

        dt = 10.0
        speed = 2 * tmp.rect.width

        event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_LEFT)
        tmp.handleEvent(event)
        self.assertEqual(tmp.pos, Vector2(5, 5), 'test_update_player_tank_pos_left')
        self.assertEqual(tmp.direction, Vector2(-1, 0), 'test_update_player_tank_dir_left')
        self.assertEqual(tmp.vel, Vector2(-speed, 0), 'test_update_player_tank_vel_left')
        tmp.update(dt=dt)
        self.assertEqual(tmp.pos, Vector2(-speed, 0) * dt + Vector2(5, 5),
                         'test_update_player_tank_pos_left_update')
        self.assertEqual(tmp.direction, Vector2(-1, 0), 'test_update_player_tank_dir_left_update')
        self.assertEqual(tmp.vel, Vector2(-speed, 0), 'test_update_player_tank_vel_left_update')

    def test_player_tank_move_right(self):
        """Test player tank move right."""
        Game.current_scene = Scene("../res/levels/level0.txt")
        Game.current_scene.bbox = Rect(Vector2(-100000, -100000),
                                       Vector2(100000, 100000) * Game.current_scene.cellSize)
        event = pygame.event.Event(pygame.USEREVENT, user_type='MAINMENU',
                                   ui_element=self.app.menu.playButton)
        pygame.event.post(event)
        tmp = PlayerTank(pos=Vector2(5, 5), size=10)
        tmp.update(dt=0.5)

        dt = 10.0
        speed = 2 * tmp.rect.width

        event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RIGHT)
        tmp.handleEvent(event)
        self.assertEqual(tmp.pos, Vector2(5, 5), 'test_update_player_tank_pos_right')
        self.assertEqual(tmp.direction, Vector2(1, 0), 'test_update_player_tank_dir_right')
        self.assertEqual(tmp.vel, Vector2(speed, 0), 'test_update_player_tank_vel_right')
        tmp.update(dt=dt)
        self.assertEqual(tmp.pos, Vector2(speed, 0) * dt + Vector2(5, 5),
                         'test_update_player_tank_pos_right_update')
        self.assertEqual(tmp.direction, Vector2(1, 0), 'test_update_player_tank_dir_right_update')
        self.assertEqual(tmp.vel, Vector2(speed, 0), 'test_update_player_tank_vel_right_update')

    def test_bullet(self):
        """Test player tank move right."""
        Game.current_scene = Scene("../res/levels/level0.txt")
        Game.current_scene.bbox = Rect(Vector2(-100000, -100000),
                                       Vector2(100000, 100000) * Game.current_scene.cellSize)
        event = pygame.event.Event(pygame.USEREVENT, user_type='MAINMENU',
                                   ui_element=self.app.menu.playButton)
        pygame.event.post(event)
        enemy = EnemyTank(pos=Vector2(5, 2), size=10)
        Game.all_objects.append(enemy)
        player = PlayerTank(pos=Vector2(5, 5), size=10)
        Game.all_objects.append(player)

        self.assertEqual(player.hp, 100, 'test_bullet_player_hp_init')

        halfCellSize = enemy.rect.w / 2
        bulletSize = halfCellSize // 2
        bulletCenter = enemy.rect.center + enemy.direction * (halfCellSize + bulletSize / 2)
        bulletPos = bulletCenter - Vector2(bulletSize / 2, bulletSize / 2)
        bulletVel = enemy.direction * 4 * enemy.rect.w
        bulletColor = (255, 255, 255)
        enemy.shoot(bulletPos, bulletSize, bulletVel, bulletColor)

        dt = 0.01

        event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_UP)
        for obj in Game.all_objects:
            if type(obj) != Bullet:
                obj.handleEvent(event)
                obj.update(dt=dt)
                obj.pos = Vector2(9, 0)
                obj.handleEvent(event)
                obj.update(dt=dt)

        self.assertEqual(player.hp, 100, 'test_bullet_player_hp')

    def tearDown(self):
        """Tear down."""
        pass


if __name__ == '__main__':
    unittest.main()
