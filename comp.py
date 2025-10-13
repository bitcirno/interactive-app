"""
SID: 25098892g
NAME: LUO DONGPU

This script defines commonly used components
"""

from abc import abstractmethod
from pygame.rect import Rect
from pygame.surface import Surface
from pygame.event import Event
from context import Context


class GraphicComponent:
    def __init__(self, ctx: Context):
        self.ctx: Context = ctx
        self.rect: Rect = None
        self.sprite: Surface = None  # sprite to be rendered

    def handle_event(self, event: Event):
        """
        Handle the passed event
        """
        ...

    @abstractmethod
    def update(self):
        """
        Update logic
        """
        ...

    @abstractmethod
    def render(self):
        """
        Render graphics
        """
        ...


class Button(GraphicComponent):
    def __init__(self, ctx: Context, text: str):
        super().__init__(ctx)
        self.text: str = text
        self.is_hover = False  # is the pointer hovering the button?

    @abstractmethod
    def on_enter(self):
        """
        Invoked on pointer entering the rect
        :return:
        """
        ...

    @abstractmethod
    def on_exit(self):
        """
        Invoked on pointer exiting the rect
        """
        ...

    @abstractmethod
    def on_click(self):
        """
        Invoked on clicking in the rect
        """
        ...
