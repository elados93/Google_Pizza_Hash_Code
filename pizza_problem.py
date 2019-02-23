from enum import Enum

from solution import Solution

default_value = -1
visited = -2


class Result(Enum):
    LEGAL_SLICE = 1
    NOT_ENOUGH_INGREDIENTS = 2
    TOO_MUCH_PIZZA = 3


class PizzaQuestion:

    calc_answers = {}

    def __init__(self, rows, cols, mat, l, h):
        self._rows = rows
        self._cols = cols
        self._mat = mat
        self._l = l
        self._h = h

    def solve(self):
        return self.solve_rec(upper_left=(0, 0), bottom_right=(self._rows - 1, self._cols - 1))

    def solve_rec(self, upper_left, bottom_right):

        # if the solution calculated, return it
        if (upper_left, bottom_right) in PizzaQuestion.calc_answers:
            return PizzaQuestion.calc_answers[(upper_left, bottom_right)]

        current_slice_res = self.slice_legal(upper_left, bottom_right)

        # return no solution if there aren't enough ingredients
        if current_slice_res == Result.NOT_ENOUGH_INGREDIENTS:
            s = Solution()
            PizzaQuestion.calc_answers[(upper_left, bottom_right)] = s
            return s

        # return the whole pizza - greedy solution
        if current_slice_res == Result.LEGAL_SLICE:
            s = Solution().add_slice(upper_left, bottom_right)
            PizzaQuestion.calc_answers[(upper_left, bottom_right)] = s
            return s

        best_slices = Solution()

        for row in range(upper_left[0], bottom_right[0]):
            upper_solution = self.solve_rec(upper_left, (row, bottom_right[1]))
            down_solution = self.solve_rec((row + 1, upper_left[1]), bottom_right)

            best_slices = max(best_slices, upper_solution + down_solution)

        for col in range(upper_left[1], bottom_right[1]):
            left_solution = self.solve_rec(upper_left, (bottom_right[0], col))
            right_solution = self.solve_rec((upper_left[0], col + 1), bottom_right)

            best_slices = max(best_slices, left_solution + right_solution)

        PizzaQuestion.calc_answers[(upper_left, bottom_right)] = best_slices
        return best_slices

    def slice_legal(self, upper_left, bottom_right):
        t_count = m_count = 0

        last_row = min(bottom_right[0] + 1, self._rows)
        last_col = min(bottom_right[1] + 1, self._cols)

        for i in range(upper_left[0], last_row):
            for j in range(upper_left[1], last_col):

                if self._mat[i][j] == 'T':
                    t_count += 1
                else:
                    m_count += 1

        if t_count < self._l or m_count < self._l:
            # there isn't enough tomato's or mushrooms - don't need to search deeper
            return Result.NOT_ENOUGH_INGREDIENTS

        if m_count + t_count > self._h:
            # there are more slices in the pizza than h - need to search more
            return Result.TOO_MUCH_PIZZA

        return Result.LEGAL_SLICE

    def __str__(self):
        rep = "Rows: %d Cols: %d L: %d H: %d\n" % (self._rows, self._cols, self._l, self._h)
        for line in self._mat:
            rep += ''.join(line) + '\n'
        return rep

    @property
    def rows(self):
        return self._rows

    @property
    def cols(self):
        return self._cols
