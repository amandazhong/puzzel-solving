"""
Puzzle solving
"""
import itertools
from collections import Counter
from fractions import Fraction
from typing import List

DICE_SIDES = [1, 2, 3, 4]

def roll_dice(number_of_dice: int):
    """
    Given one or more dice, return a list of all the possible
    combinations of the final results after all dice are rolled.
    """
    return [tuple(sorted(p)) for p in itertools.product(DICE_SIDES, repeat=number_of_dice)]


def combination_probabilities(combination_list):
    """Given a list of all the possible combinations,
    calculate the probability of each combination"""

    combination_counts =  len(combination_list)
    probabilities = {}

    for combination in combination_list:
        if combination in probabilities.keys():
            probabilities[combination] += Fraction(1, combination_counts)
        else:
            probabilities[combination] = Fraction(1, combination_counts)

    return probabilities


def probability_matrix():
    matrix = {}
    for i in range(2, 5):
        combinations = roll_dice(i)
        matrix[i] = combination_probabilities(combinations)
    return matrix


class Game:
    def __init__(self, unique: List[int], duplicate: List[int], probability: int, matrix: dict):
        self._total_dice = 4
        self._unique = unique
        self._duplicate = duplicate
        self.probability = probability
        self._matrix = matrix

    def won(self):
        return len(self._unique) == self._total_dice and len(self._duplicate) == 0

    def lost(self):
        return len(self._unique) == 0 and len(self._duplicate) == self._total_dice

    def over(self):
        return len(self._unique) == self._total_dice or len(self._duplicate) == self._total_dice

    def roll(self):
        if len(self._unique) == 0 and len(self._duplicate) == 0:
            return self._matrix[self._total_dice]
        else:
            return self._matrix[len(self._duplicate)]

    def update(self, combination, probability):
        if self.over():
            return None
        all_dice = self._unique + list(combination)
        occurances = Counter(all_dice)

        new_unique = [k for k, v in occurances.items() if v == 1]
        new_duplicate = [x for x in all_dice if x not in new_unique]
        return Game(new_unique, new_duplicate, self.probability * probability, self._matrix)


# 0.33674 when depth=7
# 0.36506 when depth=8
# 0.38629 when depth=9
def play(game: Game, winning_probabilities=[0], depth=0):
    depth += 1
    print(f"depth: {depth}")
    if not game or depth >= 9:
        return winning_probabilities

    if game.over():
        if game.won():
            winning_probabilities.append(game.probability)
        game.update(None, None)
    else:
        results = game.roll()
        for combination, probability in results.items():
            new_game = game.update(combination, probability)
            play(new_game, winning_probabilities, depth)

    return winning_probabilities



if __name__ == "__main__":
    import sys
    print(f"Current system recursion limit: {sys.getrecursionlimit()}")
    sys.setrecursionlimit(20000)
    print(f"Increased system recursion limit: {sys.getrecursionlimit()}")
    matrix = probability_matrix()
    game = Game([], [], 1, matrix)
    winning_probabilities = play(game)
    winning_probability = sum(winning_probabilities)
    print(winning_probability.numerator/winning_probability.denominator)




