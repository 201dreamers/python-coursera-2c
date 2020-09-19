import math
import random
import logging
from typing import Tuple, List, Union
from dataclasses import dataclass

import pygame


logging.basicConfig(
    format='%(levelname)s//%(funcName)s//%(lineno)d: %(message)s',
    level=logging.INFO
)


@dataclass
class Speed2d:
    x: Union[int, float]
    y: Union[int, float]


class Vec2d:
    """
    Represents 2D vector
    The vector is defined by x coordinate, y coordinate - the end
    point of vector.  The start point of vector always coincides
    with center of coordinates (0, 0)
    """

    def __init__(self, x: Union[int, float], y: Union[int, float]):
        self.x = x
        self.y = y

    def __add__(self, other_vector: 'Vec2d') -> 'Vec2d':
        """Returns the sum of two vectors"""
        return Vec2d(self.x + other_vector.x, self.y + other_vector.y)

    def __sub__(self, other_vector: 'Vec2d') -> 'Vec2d':
        """Returns the substitution of two vectors"""
        return Vec2d(self.x - other_vector.x, self.y - other_vector.y)

    def __mul__(self, scalar: Union[int, float]) -> 'Vec2d':
        """Returns the multiplication of the vector by scalar"""
        return Vec2d(self.x * scalar, self.y * scalar)

    def __len__(self) -> int:
        """Returns the length of the vector"""
        return int(math.sqrt(self.x ** 2 + self.y ** 2))

    def __eq__(self, other_vector: 'Vec2d'):
        return self.x == other_vector.x and self.y == other_vector.y

    def __lt__(self, other_vector: 'Vec2d'):
        return self.x < other_vector.x and self.y < other_vector.y

    def __gt__(self, other_vector: 'Vec2d'):
        return self.x > other_vector.x and self.y > other_vector.y

    def int_pair(self):
        return self.x, self.y


class Polyline:

    def __init__(self, surface: pygame.Surface):
        self.surface = surface
        self.anchor_points: List[Vec2d] = []
        self.speed_of_points: List[Speed2d] = []

    def add_anchor_point(self, position: Tuple[Union[int, float], Union[int, float]]):
        self.anchor_points.append(Vec2d(position[0], position[1]))
        self.speed_of_points.append(Speed2d(random.uniform(0.001, 1.1), random.uniform(0.001, 1.1)))

    def delete_anchor_point(self, position: Tuple[Union[int, float], Union[int, float]]):
        point = Vec2d(position[0], position[1])
        try:
            self.anchor_points.remove(point)
        except ValueError:
            epsylon = Vec2d(0.5, 0.5)
            logging.info(f'No {position} point exists. Will try close points')
            for index in range(len(self.anchor_points)):
                if point > self.anchor_points[index] - epsylon or\
                        point < self.anchor_points[index] + epsylon:
                    self.anchor_points.pop(index)
                    break

    def set_points(self):
        """Function for recalculating coordinates of anchor points"""
        screen_width, screen_height = self.surface.get_size()
        for index, point in enumerate(self.anchor_points):
            self.anchor_points[index].x += self.speed_of_points[index].x
            self.anchor_points[index].y += self.speed_of_points[index].y

            if ((point.x < 0 and self.speed_of_points[index].x < 0) or
                    (point.x > screen_width and self.speed_of_points[index].x > 0)):
                self.speed_of_points[index].x = -self.speed_of_points[index].x

            if ((point.y < 0 and self.speed_of_points[index].y < 0) or
                    (point.y >= screen_height and self.speed_of_points[index].y > 0)):
                self.speed_of_points[index].y = -self.speed_of_points[index].y

    def draw_anchor_points(self, radius=3, color=(255, 255, 255)):
        for point in self.anchor_points:
            pygame.draw.circle(
                surface=self.surface,
                color=color,
                center=(point.x, point.y),
                radius=radius
            )

    def draw_figure(self, width=3, color=(255, 255, 255)):
        for index, point in enumerate(self.anchor_points):
            pygame.draw.line(
                surface=self.surface,
                color=color,
                start_pos=(self.anchor_points[index - 1].x, self.anchor_points[index - 1].y),
                end_pos=(point.x, point.y),
                width=width
            )


class Knot(Polyline):

    def __init__(self, surface: pygame.Surface, smoothing_step: int = 15):
        super().__init__(surface)
        self.points_of_knot: List[Vec2d] = []
        self.smoothing_step: int = smoothing_step

    def get_point(self, points, alpha, deg=None) -> Vec2d:
        if deg is None:
            deg = len(points) - 1
        if deg == 0:
            return points[0]

        return (points[deg] * alpha) + (self.get_point(points, alpha, deg - 1) * (1 - alpha))

    def get_smoothing_points(self, base_points: Union[Tuple[Vec2d, Vec2d, Vec2d], List[Vec2d]]):
        alpha = 1 / self.smoothing_step

        for index in range(self.smoothing_step):
            self.points_of_knot.append(self.get_point(base_points, index * alpha))

    def get_knot(self):
        self.points_of_knot = []
        if len(self.anchor_points) < 3:
            return

        for index, anchor_point in enumerate(self.anchor_points):
            self.get_smoothing_points((
                (self.anchor_points[index - 2] + self.anchor_points[index - 1]) * 0.5,
                self.anchor_points[index - 1],
                (self.anchor_points[index - 1] + anchor_point) * 0.5
            ))

    def set_points(self):
        super().set_points()
        self.get_knot()

    def draw_figure(self, width=3, color=(255, 255, 255)):
        for index, point in enumerate(self.points_of_knot):
            pygame.draw.line(
                surface=self.surface,
                color=color,
                start_pos=(self.points_of_knot[index - 1].x, self.points_of_knot[index - 1].y),
                end_pos=(point.x, point.y),
                width=width
            )

        
class Screensaver:

    def __init__(self, screen_width: int, screen_height: int):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.__is_working = False
        self.__is_pause = True
        self.__show_help = False
        self.__hue = 0
        self.__color = pygame.Color(0, 0, 0)
        self.__help_commands = [
            ('F1', 'Show Help'),
            ('R', 'Restart'),
            ('P', 'Pause/Play'),
            ('N', 'New Figure'),
            ('Num+', 'More points'),
            ('Num-', 'Less points'),
            ('Left Mouse Button', 'Create point'),
            ('Right Mouse Button', 'Delete point'),
        ]

        pygame.init()
        self.surface = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption("MyScreenSaver")

        self.figures = [Knot(self.surface),]

    def start(self):
        self.__is_pause = False
        self.__is_working = True
        for figure in self.figures:
            figure.anchor_points = []
        while self.__is_working:
            for event in pygame.event.get():
                self.handle_event(event)

            self.surface.fill((0, 0, 0))
            self.__hue = (self.__hue + 1) % 360
            self.__color.hsla = (self.__hue, 100, 50, 100)

            for figure in self.figures:
                figure.draw_anchor_points()
                figure.draw_figure(color=self.__color)

                if not self.__is_pause:
                    figure.set_points()

            if self.__show_help:
                self.draw_help()

            pygame.display.flip()

        pygame.display.quit()
        pygame.quit()
        exit(0)

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            self.__is_working = False
            return

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.__is_working = False
                return

            if event.key == pygame.K_r:
                self.start()
            if event.key == pygame.K_p:
                self.__is_pause = not self.__is_pause
            if event.key == pygame.K_F1:
                self.__show_help = not self.__show_help
            if event.key == pygame.K_n:
                self.figures.append(Knot(self.surface))
            if event.key == pygame.K_KP_PLUS:
                for figure in self.figures:
                    figure.smoothing_step += 1
            if event.key == pygame.K_KP_MINUS:
                for figure in self.figures:
                    figure.smoothing_step -= 1 if figure.smoothing_step > 1 else 0

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.figures[-1].add_anchor_point(event.pos)
            else:
                for figure in self.figures:
                    figure.delete_anchor_point(event.pos)

    def draw_help(self):
        self.surface.fill((50, 50, 50))
        font1 = pygame.font.SysFont('courier', 24)
        font2 = pygame.font.SysFont('serif', 24)
        frame_coordinates = [
            (0, 0),
            (self.screen_width, 0),
            (self.screen_width, self.screen_height),
            (0, self.screen_height)
        ]

        pygame.draw.lines(
            surface=self.surface,
            color=(255, 50, 50, 255),
            closed=True,
            points=frame_coordinates,
            width=5
        )

        for index, text in enumerate(self.__help_commands):
            self.surface.blit(
                source=font1.render(text[0], True, (128, 128, 255)),
                dest=(100, 100 + 30 * index)
            )

            self.surface.blit(
                source=font2.render(text[1], True, (128, 128, 255)),
                dest=(500, 100 + 30 * index)
            )


if __name__ == '__main__':
    screensaver = Screensaver(800, 600)
    screensaver.start()
