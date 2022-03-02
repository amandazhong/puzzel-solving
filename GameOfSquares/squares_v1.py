"""Solution to the Square Game puzzle.

Ref: https://dat.jeppesen.com/confluence/pages/viewpage.action?pageId=115212982

Usage: update the ITERATION and run `python squares_v1.py`,
the INIT_SHADE can be modified to have a different start point as well.

Note: This implementation is slow as the iteration goes bigger 
because it calculates the lateral for the grid for each iteration.

"""

from typing import List, Set


class Square:
    """Object that represents a square by given the cooridnates of the left bottom corner,
    the eight neighbous are identified by shifting the cooridnates one unit to each direction."""

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def neighbours(self):
        return [Square(self.x, self.y + 1),
                Square(self.x, self.y - 1),
                Square(self.x + 1, self.y),
                Square(self.x - 1, self.y),
                Square(self.x + 1, self.y + 1),
                Square(self.x + 1, self.y - 1),
                Square(self.x - 1, self.y + 1),
                Square(self.x - 1, self.y - 1),
                ]

    def __eq__(self, other):
        if isinstance(other, Square):
            return self.x == other.x and self.y == other.y
        return false

    def __hash__(self):
        return hash((self.x, self.y))

    def __str__(self):
        return f"({x},{y})"


class Grid:
    """Object representing a grid, within which there are shaded and unshaded squares."""
    def __init__(self, shade: List[Square]):
        self.shade = shade

    def _shaded(self, square) -> bool:
        return square in self.shade

    def _laterals(self) -> Set[Square]:
        """Set of unshaded squares that are adjacent to at least one shaded square on the grid."""
        laterals = []
        for square in self.shade:
            for neighbour in square.neighbours():
                if not self._shaded(neighbour):
                    laterals.append(neighbour)
        return set(laterals)

    def _satisfy(self, square: Square) -> bool:
        """For a square to be shaded next, it must have at least three neighours that are shaded."""
        intersect = [neighbour for neighbour in square.neighbours() if self._shaded(neighbour)]
        if len(intersect) >= 3:
            return True
        else:
            return False

    def next(self):
        """Return a grid that is with the additional shaded squares. """
        next = [square for square in self._laterals() if self._satisfy(square)]
        return Grid(next + self.shade)

    def __len__(self):
        return len(self.shade)


INIT_SHADE = [Square(0, 0),
              Square(0, 1),
              Square(0, -1),
              Square(-1, 0),
              Square(1, 0)
              ]

ITERATION = 100


def play(iteration):
    current = Grid(INIT_SHADE)
    for i in range(1, iteration + 1):
        next = current.next()
        print(f"Iteration {i} total shaded squares are: {len(next)}")
        current = next


if __name__ == "__main__":
    play(ITERATION)
