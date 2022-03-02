"""
Solution to the puzzle.
A tree will be built to represent each draw and its probability.
"""

import enum
from fractions import Fraction
from typing import Dict, List


class Chocolate(enum.Enum):
    """ Enum class representing types of chocolates"""
    MILK = "milk chocolate"
    DARK = "dark chocolate"


class Node:
    """
    Each node of the tree represents the state of each draw, which contains the chocolate just drawn,
    the accumulated probability of drawing this type of chocolate, as well as how many chocolates remain in the bag.
    A node can branch out two child nodes, with the left branch always drawing milk chocolate and the right
    branch dark, until the corresponding chocolate runs out.
    """

    def __init__(self, drawn: Chocolate, prob: Fraction, bag: Dict[Chocolate, int]):
        """drawn: chocolate drawn at this node
            bag: number of each type of chocolates remaining in the bag
            prob: accumulated probability of drawing this chocolate
        """
        self.drawn = drawn
        self.prob = prob
        self.bag = bag

    def draw(self, target: Chocolate):
        """
        Draw a target chocolate type from the bag, return a new Node.
        """

        if self.bag[target] == 0:
            return None

        count_target = self.bag[target]
        count_total = sum(list(self.bag.values()))

        new_bag = {**self.bag, target: count_target - 1}
        new_prob = self.prob * Fraction(count_target, count_total)

        new_node = Node(target, new_prob, new_bag)

        if self.drawn and target != self.drawn: # put the chocolate back to the bag if chocolate drawn is different than the previous draw
            new_node = Node(None, new_prob, self.bag)

        return new_node

    def left(self):
        """Draw a milk chocolate."""
        return self.draw(Chocolate.MILK)

    def right(self):
        """Draw a dark chocolate."""
        return self.draw(Chocolate.DARK)

    def _bag_empty(self):
        """Check if the bag is empty."""
        return self.bag[Chocolate.MILK] == 0 and self.bag[Chocolate.DARK] == 0

    def gotcha(self):
        """Check if the chocolate just drawn is milk chocolate and the bag is empty"""
        return self._bag_empty() and self.drawn == Chocolate.MILK


def tree(node: Node, all_prob: List[Fraction]):
    """Recursively build a probability tree.
       Returns a list of the probability of nodes that have drawn the last milk chocolate.
       (The sum of these probabilities should be the final probability)
    """
    if node:
        if node.gotcha():
            all_prob.append(node.prob)
        else:
            tree(node.left(), all_prob)
            tree(node.right(), all_prob)
    return all_prob


if __name__ == "__main__":
    bag = {Chocolate.MILK: 2, Chocolate.DARK: 8}
    node = Node(None, Fraction(1, 1), bag)
    all_prob = tree(node, [])
    final_prob = sum(all_prob)
    print(f"Total number of possible paths: {len(all_prob)}. Final probability is {final_prob}")
    print(all_prob)






