import math
from typing import Tuple

def calculate_sm2_mutation(q: int, interval: int, ease_factor: float, repetitions: int) -> tuple[int, float, int]:
    """
    Execute precise SuperMemo-2 algorithms for structural memory retention tracking.
    Maps response scores [0..5] directly to calendar spacing intervals.
    """
    if not (0 <= q <= 5):
        raise ValueError("q must be between 0 and 5")

    if q <3:
        next_interval = 1
        next_repetitions = 0
        next_ease_factor = ease_factor

    else:
        if repetitions == 0:
            next_interval = 1
        elif repetitions == 1:
            next_interval = 6
        else:
            next_interval = int(math.ceil(interval * ease_factor))

        next_repetitions = repetitions + 1
        next_ease_factor = ease_factor +(.1 - (5-q) *(.08 + (5 - q) * .02))

    if next_ease_factor <1.3:
        next_ease_factor = 1.3

    return next_interval, round(next_ease_factor, 4), next_repetitions