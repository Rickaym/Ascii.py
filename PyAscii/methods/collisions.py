from ..globals import SCREENS
from ..rect import Rect
from ..utils import beautify

try:
    from typing import Any
except ImportError:
    pass
"""
Contains different definitions on checking collisions of a model
Different models can pick best fitting collisions checking methods circumstantially.
"""

#
#  Measures the true collisions based on the overlapping changes of two empty frames
#  after rendering.
#

single_print = True


def write_collision_state(screen, self_frame, other_frame):
    global single_print

    if single_print:
        with open("self_frame.txt", "w") as f:
            f.write(beautify(self_frame, screen))

        with open("model_frame.txt", "w") as f:
            f.write(beautify(other_frame, screen))
        single_print = False


def multi_collides_with(self, *models):
    # type: (Any, Any) -> bool
    self_frame = None
    other_frames = None
    screen_ = None
    states = [False] * len(models)

    # screen lookup is O(n) where n is the amount of screens
    # let the blit method have the time complexity of O(z)
    # Result: O(n+2z)
    for screen in SCREENS:
        if screen.all_models.get(self.rect) is not None:
            self_frame = self.blit(screen, empty=True)
            other_frames = [
                model.blit(screen, empty=True) for model in models if model != self
            ]
            screen_ = screen
            break

    # compared models are shallow and doesn't have a boundary
    if self_frame is None or len(other_frames) < 0:
        return False

    # collision lookup is O(m)
    # total time complexity in checking collisions is
    # O(n+2z+m) where m is the amount of characters in a screen
    for z, frame in enumerate(other_frames):
        for i, char in enumerate(self_frame):
            if char != " " and frame[i] != " ":
                write_collision_state(screen_, self_frame, frame)
                states[z] = True
                break
    return states if len(states) > 1 else states[0]


def collides_with(self, model):
    # type: (Any, Any) -> bool
    if model == self:
        return False

    self_frame = None
    other_frame = None
    screen_ = None

    # screen lookup is O(n) where n is the amount of screens
    # let the blit method have the time complexity of O(z)
    # Result: O(n+2z)
    for screen in SCREENS:
        if screen.all_models.get(self.rect) is not None:
            self_frame = self.blit(screen, empty=True)
            other_frame = model.blit(screen, empty=True)
            screen_ = screen
            break

    # compared models are shallow and doesn't have a boundary
    if self_frame is None or other_frame is None:
        return False

    # collision lookup is O(m)
    # total time complexity in checking collisions is
    # O(n+2z+m) where m is the amount of characters in a screen
    for i, char in enumerate(self_frame):
        if char != " " and other_frame[i] != " ":
            write_collision_state(screen_, self_frame, other_frame)
            return True
    return False


#
#  Measuring collisions based on quadilateral pixel overlapping
#


def get_occupancy(rect):
    occupancy = []
    for y_point in range(rect.y, rect.y + rect.dimension[1]):
        occupancy.extend(
            list(
                zip(
                    list(range(rect.x, rect.x + rect.dimension[0])),
                    [y_point] * rect.dimension[0],
                )
            )
        )
    return occupancy


def colliding_with(rect):
    # type: (Rect) -> bool
    """
    IMAGINE

    x = 0, 0   |   length = 20
    y = 0, 0   |   height = 20

    Objective: Gets all possible coordinates of the rectangle and checks for
        similarities.

    range of height = range(y, y+height)
    range of width = range(x, x+legth)
    """
    self_occupancy = get_occupancy()
    alien_occupancy = get_occupancy(rect)

    return any()