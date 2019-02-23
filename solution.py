class Solution:

    def __init__(self):
        self.__slices = set()  # save a set of tuples with 2 tuples for coordinates
        self.__score = 0

    def add_slice(self, upper_left_point, lower_right_point):
        self.__slices.add((upper_left_point, lower_right_point))
        rows, cols = lower_right_point[0] - upper_left_point[0] + 1, lower_right_point[1] - upper_left_point[1] + 1
        self.__score += rows * cols
        return self

    def print_on_question(self, question):
        r, c = question.rows, question.cols
        cover_rate = self.__score / (r * c) * 100.0
        marked_mat = [[0 for _ in range(c)] for _ in range(r)]
        color = 0

        # mark all the slices
        for current_slice in self.__slices:
            upper, lower = current_slice[0], current_slice[1]
            color += 1

            for i in range(upper[0], lower[0] + 1):
                for j in range(upper[1], lower[1] + 1):
                    marked_mat[i][j] = color

        # print board
        print('Cover rate: {}%'.format(cover_rate))
        for line in marked_mat:
            print(line)

    def __add__(self, other):
        res = Solution()
        both_sets = self.__slices.union(other.__slices)
        for current_slice in both_sets:
            res.add_slice(*current_slice)
        return res

    def __gt__(self, other):
        return self.__score > other.__score

    def __repr__(self):
        return 'slices: %d ; score: %d' % (len(self.__slices), self.__score)
