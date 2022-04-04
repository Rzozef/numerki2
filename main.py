import numpy as np
import itertools
import json


def is_good_enough(x_previous, x_current, epsilon):
    return abs(x_current - x_previous) < epsilon


def load_from_file(path):
    with open(path, "r") as file:
        return json.load(file)


def save_to_file(matrix, path):
    with open(path, "w") as file:
        json.dump(matrix, file)


def is_diagonally_dominant(matrix):
    abs_matrix = np.abs(matrix)
    # mnożymy przez 2, ponieważ w sumie bierzemy pod uwagę element w diagonali
    return np.all(2 * np.diag(abs_matrix) >= np.sum(abs_matrix, axis=1))


def variant_b(a, b, x, epsilon):
    """Macierz A, Macierz X, epsilon"""
    diff = 0
    for h in range(0, len(a)):
        equation = a[h]
        sum = 0
        for w in range(0, len(equation)):
            sum += equation[w] * x[w]
        diff += abs(sum - b[h])
    return diff < epsilon


def gauss_seidel_method(matrix, *, epsilon=None, iterations=None):
    if epsilon is not None and iterations is not None:
        raise RuntimeError("Warunkami stopu dla funkcji nie może być jednocześnie ilość iteracji i epsilon!")

    permutations = list(itertools.permutations(matrix))
    for matrix in permutations:

        # pierwszym przybliżeniem są same zera
        x = [0] * len(matrix)
        # macierz z obciętą ostatnią kolumną
        a = np.delete(matrix, -1, axis=1)

        matrix = np.array(matrix)
        b = matrix[:, -1]

        if not is_diagonally_dominant(a):
            continue

        L = np.tril(a, k=-1).tolist()
        D = np.diag(np.diag(a)).tolist()
        U = np.triu(a, k=1).tolist()

        inv_D = D.copy()
        for i in range(0, len(inv_D)):
            inv_D[i][i] = 1 / inv_D[i][i]

        b_alter = b.copy()
        for i in range(0, len(b)):
            b_alter[i] *= inv_D[i][i]
        for i in range(0, len(L)):
            for j in range(0, len(L[i])):
                L[i][j] *= inv_D[i][i]
        for i in range(0, len(U)):
            for j in range(0, len(U[i])):
                U[i][j] *= inv_D[i][i]
        n = len(x)

        if iterations is not None:
            for k in range(0, iterations):
                for i in range(0, n):
                    x[i] = b_alter[i]
                    for j in range(0, i):
                        x[i] -= L[i][j] * x[j]
                    for j in range(i + 1, n):
                        x[i] -= U[i][j] * x[j]
        else:  # Warunkiem stopu jest epsilon
            k = 0
            while not variant_b(a, b, x, epsilon):
                for i in range(0, n):
                    x[i] = b_alter[i]
                    for j in range(0, i):
                        x[i] -= L[i][j] * x[j]
                    for j in range(i + 1, n):
                        x[i] -= U[i][j] * x[j]
                k += 1
        return x
    raise RuntimeError("Podana macierz nie jest macierzą diagonalnie dominującą")

def main():
    choice_first = None
    while choice_first is None:
        print("W jaki sposób uzupełnić współczynniki?")
        print("\t1. Ręcznie")
        print("\t2. Wczytaj z pliku")
        choice_first = input("\t\t>>> ")
        if int(choice_first) < 1 or int(choice_first) > 2:
            print("Nie ma takiej opcji w menu")
            choice_first = None
    if int(choice_first) == 1:
        how_much = 0
        while int(how_much) <= 0:
            print("Ile równań chcesz wprowadzić?")
            how_much = input("\t\t>>> ")
        m = []
        matrix = []
        for i in range(int(how_much)):
            for j in range(int(how_much)):
                print("Wprowadz " + str(j + 1) + " wspolczynnik rownania nr " + str(i + 1))
                m.append(float(input("\t\t>>> ")))
            print("Wprowadz wynik rownania nr " + str(i + 1))
            m.append(float(input("\t\t>>> ")))
            matrix.append(m.copy())
            m.clear()
    else:
        print("Podaj sciezke do pliku")
        path = input("\t\t>>> ")
        matrix = load_from_file(path)
    for i in range(len(matrix)):
        if len(matrix) != (len(matrix[i]) - 1):
            raise RuntimeError("Ilość równań nie jest zgodna z ilością niewiadomych")
    stop_term = None
    while stop_term is None:
        print("Wybierz warunek stopu:")
        print("\t1. Spełnienie warunku założonego przez dokładność")
        print("\t2. Osiągnięcie zadanej liczby iteracji")
        stop_term = input("\t\t>>> ")
        if int(stop_term) < 1 or int(stop_term) > 2:
            print("Nie ma takiej opcji w menu")
            stop_term = None
    result, epsilon, iterations = None, None, 0
    if stop_term == "1":
        while epsilon is None:
            epsilon = input("Podaj epsilon: ")
        result = gauss_seidel_method(matrix, epsilon=float(epsilon))
    else:
        while iterations == 0:
            iterations = input("Podaj liczbę iteracji: ")
        result = gauss_seidel_method(matrix, iterations=int(iterations))
    print(result)


if __name__ == "__main__":
    main()
