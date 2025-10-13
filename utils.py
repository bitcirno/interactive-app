import random


def clamp_angle(angle):
    """
    clamp the input angle to [-360, 360]
    """
    while angle > 360:
        angle -= 360
    while angle <= -360:
        angle += 360
    return angle


def shortest_arc(a, b):
    a = clamp_angle(a)
    b = clamp_angle(b)
    diff = b - a

    if abs(diff) <= 180:
        return a, b

    if diff > 180:
        a_new = a + 360
        if -360 <= a_new <= 360:
            return a_new, b
        b_new = b - 360
        return a, b_new

    if diff < -180:
        a_new = a - 360
        if -360 <= a_new <= 360:
            return a_new, b
        b_new = b + 360
        return a, b_new

    return a, b


def get_random_float_between(a, b):
    return a + (b - a) * random.random()
