"""Solution to the Square Game puzzle.

Usage: update the ITERATION and run `python squares_v2.py`,
the INIT_SHADE can be modified to have a different start point as well.

Note: This implementation is faster than v1 because it only calculate the laterials for newly shaded squares.
But it can be better.

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
        self.laterals = self._get_laterals(self.shade)

    def _shaded(self, square) -> bool:
        return square in self.shade

    def _get_laterals(self, shade_list) -> Set[Square]:
        """Given a list of shaded squares, find out their neighbours that are unshaded."""
        laterals = []
        for square in shade_list:
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

    def _new_shade(self):
        """Find from the laterals that satisfy the criteria and can be shaded."""
        return [square for square in self.laterals if self._satisfy(square)]

    def _update_grid(self):
        """Update the shaded square list and the laterals after new squares being shaded."""
        new_shade = self._new_shade()
        self.shade = self.shade + new_shade

        new_laterals = self._get_laterals(new_shade)
        self.laterals = self.laterals.difference(new_shade).union(new_laterals)

    def play(self, iteration):
        """Play the game for as many iterations as specified."""
        for i in range(1, iteration + 1):
            self._update_grid()
            print(f"Iteration {i} total shaded squares are: {len(self.shade)}")


INIT_SHADE = [Square(0, 0),
              Square(0, 1),
              Square(0, -1),
              Square(-1, 0),
              Square(1, 0)
              ]
ITERATION = 100

if __name__ == "__main__":
    grid = Grid(INIT_SHADE)
    grid.play(ITERATION)
