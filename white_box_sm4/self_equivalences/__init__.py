from abc import ABC
from abc import abstractmethod
from random import randint

from sage.all import GF


class SelfEquivalenceProvider(ABC):


    @abstractmethod
    def __init__(self, word_size):

        self.word_size = word_size

    @abstractmethod
    def random_self_equivalence(self, ring):

        pass


class CoefficientsSelfEquivalenceProvider(SelfEquivalenceProvider):

    @abstractmethod
    def __init__(self, word_size, coefficients_size):
        self.word_size = word_size
        self.coefficients_size = coefficients_size

    def _check_constraints(self, coefficients):
        return len(coefficients) == self.coefficients_size

    @abstractmethod
    def self_equivalence(self, ring, coefficients):
        pass

    def random_self_equivalence(self, ring):
        assert ring == GF(2)

        while True:
            coefficients = [randint(0, 1) for _ in range(self.coefficients_size)]
            if self._check_constraints(coefficients):
                return self.self_equivalence(ring, coefficients)
