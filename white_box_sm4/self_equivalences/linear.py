from sage.all import matrix
from sage.all import vector

from . import CoefficientsSelfEquivalenceProvider


class LinearSelfEquivalenceProvider(CoefficientsSelfEquivalenceProvider):


    def __init__(self, word_size):

        super().__init__(word_size, 2 * word_size)

    def _self_equivalence_implicit(self, ring, coefficients):

        ws = self.word_size

        zero = matrix(ring, ws)
        one = matrix.identity(ring, ws)

        C0 = matrix.identity(ring, ws)
        for i in range(ws - 1):
            C0[ws - 1, i] = coefficients.pop()

        C1 = matrix.identity(ring, ws)
        for i in range(ws - 1):
            C1[ws - 1, i] = coefficients.pop()

        D0 = matrix(ring, ws)
        D0[ws - 1, 0] = coefficients.pop()
        for i in range(1, ws - 1):
            D0[ws - 1, i] = C0[ws - 1, i]

        D1 = matrix(ring, ws)
        D1[ws - 1, 0] = coefficients.pop()
        for i in range(1, ws - 1):
            D1[ws - 1, i] = C0[ws - 1, i] + C1[ws - 1, i]

        assert len(coefficients) == 0

        A = matrix.block(ring, [
            [C0, D0, D0, zero],
            [D1, C1, C0 + C1, D0],
            [D0, zero, C0, D0],
            [C0 + C1, D0, D1, C1]
        ])
        A.set_immutable()

        L = matrix.block(ring, [
            [zero, one, one, zero],
            [one, one, one, zero],
            [zero, zero, one, zero],
            [one, zero, one, one]
        ])
        L.set_immutable()
        return A, L

    def self_equivalence(self, ring, coefficients):

        A, L = self._self_equivalence_implicit(ring, coefficients)
        M = L * A * L.inverse()
        A = M.submatrix(row=0, col=0, nrows=2 * self.word_size, ncols=2 * self.word_size)
        A.set_immutable()
        a = vector(ring, 2 * self.word_size)
        a.set_immutable()
        B = M.submatrix(row=2 * self.word_size, col=2 * self.word_size).inverse()
        B.set_immutable()
        b = vector(ring, 2 * self.word_size)
        b.set_immutable()
        return A, a, B, b
