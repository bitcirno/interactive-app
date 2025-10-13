"""
SID: 25098892g
NAME: LUO DONGPU

Find challenges!
Simply implement value interpolation functions
"""

from typing import Callable
from enum import Enum
import time
from pygame.math import lerp, clamp, Vector2, Vector3
from pygame.color import Color


class Ease(Enum):
    """
    Interpolation types
    """
    Linear = 0,
    InQuad = 1,
    OutQuad = 2,
    InOutQuad = 3,
    InCubic = 4,
    OutCubic = 5,
    InOutCubic = 6


class LerpType(Enum):
    Float = 0,
    Vec2 = 1,
    Vec3 = 2,
    Color = 3,


class Tween:

    @staticmethod
    def __ease_linear(t: float) -> float:
        return t

    @staticmethod
    def __ease_in_quad(t: float) -> float:
        return t*t

    @staticmethod
    def __ease_out_quad(t: float) -> float:
        return 1 - (t-1)*(t-1)

    @staticmethod
    def __ease_in_out_quad(t: float) -> float:
        if t < 0.5:
            return 2*t*t
        else:
            return -2*t*t + 4*t - 1

    @staticmethod
    def __ease_in_cubic(t: float) -> float:
        return t*t*t

    @staticmethod
    def __ease_out_cubic(t: float) -> float:
        return 1 + (t-1)*(t-1)*(t-1)

    @staticmethod
    def __ease_in_out_cubic(t: float) -> float:
        if t < 0.5:
            return 4 * t * t * t
        else:
            return 1 - (-2 * t + 2) ** 3 / 2

    interpolators = {
        Ease.Linear: __ease_linear,
        Ease.InQuad: __ease_in_quad,
        Ease.OutQuad: __ease_out_quad,
        Ease.InOutQuad: __ease_in_out_quad,
        Ease.InCubic: __ease_in_cubic,
        Ease.OutCubic: __ease_out_cubic,
        Ease.InOutCubic: __ease_in_out_cubic,
    }

    @staticmethod
    def update_active_tweens():
        tween_count = len(Tween.active_tweens)
        if tween_count == 0:
            return
        for i in range(tween_count-1, -1, -1):
            tween = Tween.active_tweens[i]
            if not tween.is_tweening:
                Tween.active_tweens.pop(i)
            else:
                tween.__step()

    active_tweens = []

    def __init__(self):
        self.is_tweening = False  # whether it is tweening and in active tween list
        self.onComplete: Callable = None
        # self.onUpdate: Callable = None
        self.setter: Callable = None
        self.start_time: float = 0
        self.end_time: float = 0
        self.duration: float = 0
        self.ease: Ease = Ease.OutQuad

        self.lerp_type: LerpType = LerpType.Float
        self.src_float: float = 0
        self.dst_float: float = 0
        self.src_vec2: Vector2 = Vector2()
        self.dst_vec2: Vector2 = Vector2()
        self.src_vec3: Vector3 = Vector3()
        self.dst_vec3: Vector3 = Vector3()
        self.src_color: Color = Color(255, 255, 255, 255)
        self.dst_color: Color = Color(255, 255, 255, 255)

    def kill(self):
        if not self.is_tweening:
            return
        self.is_tweening = False

    def to_float(self, source: float, target: float,
                 duration: float, setter: Callable,
                 onComplete: Callable = None, ease: Ease = Ease.OutQuad) -> None:
        self.lerp_type = LerpType.Float
        self.src_float = source
        self.dst_float = target
        self.__to(duration, setter, onComplete, ease)

    def to_vec2(self, source: Vector2, target: Vector2,
                duration: float, setter: Callable,
                onComplete: Callable = None, ease: Ease = Ease.OutQuad) -> None:
        self.lerp_type = LerpType.Vec2
        self.src_vec2 = source
        self.dst_vec2 = target
        self.__to(duration, setter, onComplete, ease)

    def to_vec3(self, source: Vector3, target: Vector3,
                duration: float, setter: Callable,
                onComplete: Callable = None, ease: Ease = Ease.OutQuad) -> None:
        self.lerp_type = LerpType.Vec3
        self.src_vec3 = source
        self.dst_vec3 = target
        self.__to(duration, setter, onComplete, ease)

    def to_color(self, source: Color, target: Color,
                 duration: float, setter: Callable,
                 onComplete: Callable = None, ease: Ease = Ease.OutQuad) -> None:
        self.lerp_type = LerpType.Color
        self.src_color = source
        self.dst_color = target
        self.__to(duration, setter, onComplete, ease)

    def __to(self, duration: float, setter: Callable, onComplete: Callable, ease: Ease) -> None:
        """
        Start tween from start_value to end_value with duration
        """
        if duration < 0:
            raise ValueError("Duration cannot be negative")

        is_already_active = self.is_tweening
        self.is_tweening = True

        self.duration = duration
        self.setter = setter
        self.onComplete = onComplete
        self.start_time = time.time()
        self.end_time = self.start_time + self.duration
        self.ease = ease

        if not is_already_active:
            Tween.active_tweens.append(self)  # add to active tweens list

        self.__step()  # step once

    def __step(self):
        """
        Update value interpolation by a step
        """
        if not self.is_tweening:
            return

        cur_time = time.time()
        per = (cur_time - self.start_time) / self.duration
        eased_per = self.interpolators[self.ease](per)
        eased_per = clamp(eased_per, 0, 1)

        is_complete = cur_time >= self.end_time
        if is_complete:
            eased_per = 1.0

        if self.lerp_type == LerpType.Float:
            value = lerp(self.src_float, self.dst_float, eased_per)
        elif self.lerp_type == LerpType.Vec2:
            value = self.src_vec2.lerp(self.dst_vec2, eased_per)
        elif self.lerp_type == LerpType.Vec3:
            value = self.src_vec3.lerp(self.dst_vec3, eased_per)
        else:  # lerp between two colors
            value = self.src_color.lerp(self.dst_color, eased_per)

        if self.setter:
            self.setter(value)
            # if self.onUpdate:
            #     self.onUpdate()

        if is_complete:
            self.is_tweening = False
            if self.onComplete:
                self.onComplete()
