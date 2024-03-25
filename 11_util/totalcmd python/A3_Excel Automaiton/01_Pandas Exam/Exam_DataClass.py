from dataclasses import dataclass


@dataclass
class Returnvalue:
    y0: int
    y1: float
    y2: int


def total_cost(x):
    y0 = x + 1
    y1 = x * 3
    y2 = y1 ** y0
    return Returnvalue(y0, y1, y2)


aa = total_cost(2)
print(aa.y0, aa.y1, aa.y2)
