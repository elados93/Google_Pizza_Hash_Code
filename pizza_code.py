# BAS"D

from random import shuffle

default_value = -1
visited = -2


def read_pizza_from_file(filename):
    with open(filename, 'r') as file:
        first_line = file.readline().strip()
        rows, cols, l, h = [int(x) for x in first_line.split()]
        matrix = []

        for line in file:
            matrix.append(list(line.strip()))

        return rows, cols, l, h, matrix


def print_question(rows, cols, l, h, matrix):
    print("Rows: %d Cols: %d L: %d H: %d\n" % (rows, cols, l, h))
    for line in matrix:
        print(line)


def slice_legal(matrix, matrix_tm, upper_left, bottom_right, l, h):
    t_count = m_count = 0

    row, col = len(matrix_tm), len(matrix_tm[0])

    last_row = min(bottom_right[0] + 1, row)
    last_col = min(bottom_right[1] + 1, col)

    for i in range(upper_left[0], last_row):
        for j in range(upper_left[1], last_col):

            if matrix[i][j] != visited and matrix[i][j] != default_value:
                return False

            if matrix_tm[i][j] == 'T':
                t_count += 1
            else:
                m_count += 1

    if t_count < l or m_count < l:  # there isn't enough tomato's or mushrooms
        return False

    if m_count + t_count > h:  # there are more slices in the pizza than h
        return False

    return True


def enter_slice(matrix, all_slices, upper_left, bottom_right):
    slice_number = len(all_slices) + 1

    row, col = len(matrix), len(matrix[0])

    last_row = min(bottom_right[0] + 1, row)
    last_col = min(bottom_right[1] + 1, col)

    # mark the slice number in the matrix
    for i in range(upper_left[0], last_row):
        for j in range(upper_left[1], last_col):
            matrix[i][j] = slice_number

    all_slices.append([*upper_left, *bottom_right])


def choose_slice(matrix, matrix_tm, l, h, next_pos, slices):
    if not slices:
        return False
    for slice in slices:
        if slice_legal(matrix, matrix_tm, next_pos, slice, l, h):
            return slice
    return False  # didn't find any legal slice


def all_shapes(height, width, L, H, i, j):
    max_ex_right = min(width - j, H)
    max_ex_down = min(height - i, H)
    all_op = []
    for index in range(j, j + max_ex_right):
        for index2 in range(i, i + max_ex_down):
            if ((index - j + 1) * (index2 - i + 1) >= 2 * L) and ((index - j + 1) * (index2 - i + 1) <= H):
                all_op.append([index2, index])
    return all_op


def all_shapes_rand(width, height, L, H, i, j):
    max_ex_right = min(width - j, H)
    max_ex_down = min(height - i, H)
    all_op = []
    for index in range(j, j + max_ex_right):
        for index2 in range(i, i + max_ex_down):
            if ((index - j + 1) * (index2 - i + 1) >= 2 * L) and ((index - j + 1) * (index2 - i + 1) <= H):
                all_op.append([index2, index])
    shuffle(all_op)
    return all_op


def all_shapes_surface_area(width, height, L, H, i, j):
    max_ex_right = min(width - j, H)
    max_ex_down = min(height - i, H)
    min_squers = 2 * L
    all_op = []
    for index in range(j, j + max_ex_right):
        for index2 in range(i, i + max_ex_down):
            if ((index - j + 1) * (index2 - i + 1) >= 2 * L) and ((index - j + 1) * (index2 - i + 1) <= H):
                all_op.append([index2, index])
    for index, op in enumerate(all_op):
        all_op[index].append((op[0] - i) * 2 + (op[1] - j) * 2)
    all_op = sorted(all_op, key=lambda x: x[2])
    return [value[0:2] for value in all_op]


def next_corrd(matrix):
    row = len(matrix)
    column = len(matrix[0])
    for i in range(row):
        for j in range(column):
            if matrix[i][j] == default_value:
                matrix[i][j] = visited
                return [i, j]
    return False


def how_many_visited(matrix):
    visited_count = 0
    for row in matrix:
        for item in row:
            if item == visited:
                visited_count += 1
    return visited_count


def main():
    rows, cols, l, h, matrix_tm = read_pizza_from_file('b_small.in')

    min_score = float('inf')
    min_matrix = None

    for _ in range(1000):
        matrix = [[default_value for _ in range(cols)] for _ in range(rows)]
        all_slices = []

        while True:

            next_pos = next_corrd(matrix)

            if not next_pos:
                break

            all_options = all_shapes_rand(rows, cols, l, h, *next_pos)

            chosen_slice = choose_slice(matrix, matrix_tm, l, h, next_pos, all_options)

            if chosen_slice != False:
                enter_slice(matrix, all_slices, next_pos, chosen_slice)

        score = how_many_visited(matrix)

        if score < min_score:
            min_score = score
            min_matrix = matrix

            # print new matrix
            print('*' * 50)
            print("SCORE: %d FITNESS: %d" % (min_score, score + 1 / rows * cols))
            # print_question(rows, cols, l, h, matrix_tm)
            print_question(rows, cols, l, h, min_matrix)
            print('*' * 50)

    # upper_left = [1, 2]
    # bottom_right = [3, 3]
    #
    # print_question(rows, cols, l, h, matrix)
    #
    # enter_slice(matrix, all_slices, upper_left, bottom_right)
    #
    # print_question(rows, cols, l, h, matrix)


if __name__ == '__main__':
    main()
