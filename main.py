import numpy as np


def is_good_enough(x_previous, x_current, epsilon):
    return abs(x_current - x_previous) < epsilon


def load_from_file(path):
    m1 = []
    count_rows = 0
    with open(path) as file:
        for line in file:
            m1.append(line.split())
            count_rows += 1
    m2 = []
    for i in range(count_rows):
        for j in range(len(m1[i])):
            m2.append(m1[i][j].rstrip(','))  # typ string, mozna rzutowac w tym miejscu na inta, ale niektore
            # macierze maja floaty
    m3 = []
    matrix = []
    for i in range(count_rows):
        for j in range(len(m1[i])):
            m3.append(m2[i * len(m1[i]) + j])
        matrix.append(m3.copy())
        m3.clear()
    return np.asmatrix(matrix)


def return_b(matrix):
    b = []
    for i in range(matrix.shape[0]):
        b.append(matrix[i, matrix.shape[1] - 1])
    b_matrix = np.asmatrix(b)
    return b_matrix.transpose()


def return_a(matrix):
    a = []
    aa = []
    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1] - 1):
            a.append(matrix[i, j])
        aa.append(a.copy())
        a.clear()
    return np.asmatrix(aa)


def is_diagonally_dominant(matrix):
    diag = np.diag(np.abs(matrix))
    print(diag)
    off_diag = np.sum(np.abs(matrix), axis=1)
    for i in range(len(diag)):
        off_diag[i] -= diag[i]
    print(off_diag)
    if np.all(diag > off_diag):
        return True
    else:
        return False


def gauss_seidel_method(matrix):
    # TODO jakie byly warunki konieczne?
    b = return_b(matrix)
    a = return_a(matrix)
    x = []
    xmatrix = []
    for i in range(len(b)):
        x.append(0)
        xmatrix.append(x.copy())
        x.clear()
    xmatrix = np.asmatrix(xmatrix)
    xmatrix.transpose()
    print(xmatrix)
    for k in range(a.shape[0]):
        b_k = b[k]
        for j in range(a.shape[1]):
            if j != k:
                b_k -= a[k][j] * xmatrix[j]  # zly wzor
        xmatrix[k] = b_k / a[k][k]
    return xmatrix


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
        # todo wczytywanie wspolczynnikow z konsoli
    else:
        print("Podaj sciezke do pliku")
        path = input("\t\t>>> ")
        matrix = load_from_file(path)
    stop_term = None
    while stop_term is None:
        print("Wybierz warunek stopu:")
        print("\t1. Spełnienie warunku założonego przez dokładność")
        print("\t2. Osiągnięcie zadanej liczby iteracji")
        stop_term = input("\t\t>>> ")
        if int(stop_term) < 1 or int(stop_term) > 2:
            print("Nie ma takiej opcji w menu")
            stop_term = None

    epsilon, iterations = None, 0

    if stop_term == "1":
        while epsilon is None:
            epsilon = input("Podaj epsilon: ")
    else:
        while iterations == 0:
            iterations = input("Podaj maksymalną liczbę iteracji: ")
    gauss_seidel_method(matrix)


if __name__ == "__main__":
    main()
