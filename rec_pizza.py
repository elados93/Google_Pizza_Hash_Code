from pizza_problem import PizzaQuestion


def read_pizza_from_file(filename):
    with open(filename, 'r') as file:
        first_line = file.readline().strip()
        rows, cols, l, h = [int(x) for x in first_line.split()]
        matrix = []

        for line in file:
            matrix.append(list(line.strip()))

        return PizzaQuestion(rows, cols, matrix, l, h)


def main():
    file_name = 'c_medium.in'
    problem = read_pizza_from_file(file_name)
    print(problem)
    solution = problem.solve()
    print(solution)
    solution.print_on_question(problem)


if __name__ == '__main__':
    main()
