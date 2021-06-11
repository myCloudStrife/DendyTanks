"""Test."""

import unittest
import pygame
from pygame.math import Vector2
from DendyTanks.Application import Application
from DendyTanks.GameObject import PlayerTank
import os


class Test(unittest.TestCase):
    """Test."""

    def setUp(self):
        """Start application."""
        srcDir = os.path.dirname(__file__)
        os.chdir(srcDir)
        self.app = Application()

    def test_init_application(self):
        """Check some global hardcoded params."""
        self.assertEqual(self.app.screenWidth, 640, 'test_init_application_w')
        self.assertEqual(self.app.screenHeight, 480, 'test_init_application_h')
        self.assertEqual(self.app.game_over_screen, False, 'test_init_application_game_over_flag')

    def player_tank_init(self):
        """Check player tank creation."""
        event = pygame.event.Event(pygame.USEREVENT, user_type='MAINMENU',
                                   ui_element=self.app.menu.playButton)
        pygame.event.post(event)
        tmp = PlayerTank(pos=Vector2(5, 5), size=10)
        tmp.update(dt=0.5)
        self.assertEqual(tmp.pos, Vector2(5, 5), 'test_update_player_tank_init_pos')
        self.assertEqual(tmp.size, 10, 'test_update_player_tank_init_size')
        self.assertEqual(tmp.vel, Vector2(0, 0), 'test_update_player_tank_init_velocity')

    def player_tank_move(self):
        """Check player tank movement."""
        event = pygame.event.Event(pygame.USEREVENT, user_type='MAINMENU',
                                   ui_element=self.app.menu.playButton)
        pygame.event.post(event)
        tmp = PlayerTank(pos=Vector2(5, 5), size=10)
        tmp.update(dt=0.5)

        event = pygame.event.Event(type=pygame.KEYDOWN, key=pygame.K_UP)
        tmp.handleEvent(event)
        self.assertEqual(tmp.direction, Vector2(0, -1), 'test_update_player_tank_dir_up')

        event = pygame.event.Event(type=pygame.KEYDOWN, key=pygame.K_DOWN)
        tmp.handleEvent(event)
        self.assertEqual(tmp.direction, Vector2(0, 1), 'test_update_player_tank_dir_down')

        event = pygame.event.Event(type=pygame.KEYDOWN, key=pygame.K_LEFT)
        tmp.handleEvent(event)
        self.assertEqual(tmp.direction, Vector2(-1, 0), 'test_update_player_tank_dir_left')

        event = pygame.event.Event(type=pygame.KEYDOWN, key=pygame.K_RIGHT)
        tmp.handleEvent(event)
        self.assertEqual(tmp.direction, Vector2(1, 0), 'test_update_player_tank_dir_right')

    def tearDown(self):
        """Close app."""
        event = pygame.event.Event(pygame.USEREVENT, user_type=pygame.QUIT)
        pygame.event.post(event)


if __name__ == '__main__':
    unittest.main()
