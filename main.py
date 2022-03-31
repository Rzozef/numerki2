import numpy as np
import json


# todo przed rozpoczeciem algorytmu kolumny badz wiersze
# maja byc tak poprzestawiane, zeby przekątna dominowała
# jak sie tego nie zrobi to tylko ostatni przyklad zadziala
# o ile w ogole zadziala, bo sie zajebac idzie z tymi indeksami
# pozdrawiam z rodzinką

def is_good_enough(x_previous, x_current, epsilon):
    return abs(x_current - x_previous) < epsilon


# Prościej już się tego nie da napisać xD
def load_from_file(path):
    with open(path, "r") as file:
        return json.load(file)


def save_to_file(matrix, path):
    with open(path, "w") as file:
        json.dump(matrix, file)


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
    off_diag = np.sum(np.abs(matrix), axis=1)
    for i in range(len(diag)):
        off_diag[i] -= diag[i]
    if np.all(diag > off_diag):
        return True
    else:
        return False


def szacher_macher(matrix):  # funkcja ma poszperać w macierzy zeby byla dominujaca na przekatnej
    if not is_diagonally_dominant(return_a(matrix)):
        array = []
        matrix_refactored = []  # ma przechowywac arraye
        for i in range((return_a(matrix)).shape[0]):
            maximum = max(return_a(matrix)[i])
            for j in range(return_a(matrix).shape[0]):
                if maximum == return_a(matrix)[i][j]:
                    row = i
                    column = j
            # todo przesuniecie w rzedzie o daną ilosc miejsc
            # to samo z kolumnami
        if not is_diagonally_dominant(return_a(matrix_refactored)):
            raise Exception("Macierz nie spełnia warunku zbieżności")
        else:
            return np.asmatrix(matrix_refactored)
    return matrix


def gauss_seidel_method(matrix, epsilon, iterations=None):
    #matrix = szacher_macher(matrix)
    #b = return_b(matrix)
    #a = return_a(matrix)
    #xmatrix = np.zeros_like(b)
    # todo implementacja wzoru
    #return xmatrix

    # pierwszym przybliżeniem są same zera
    x = [0] * len(matrix)
    # macierz z obciętą ostatinią kolumną
    a = np.delete(matrix, -1, axis=1)

    matrix = np.array(matrix) # TODO zmień wszystko na ndarray
    b = matrix[:,-1]

    L = np.tril(a, k=-1).tolist()
    D = np.diag(np.diag(a)).tolist() # Prościej się nie da, domyślnie np.diag(a) zwraca array
    U = np.triu(a, k=1).tolist()

    inv_D = []
    for arr in D:
        a = arr.copy()
        for i in range(0, len(a)):
            if a[i] != 0:
                a[i] = 1 / a[i]
        inv_D.append(a)
    for i in range(0, len(b)):
        b[i] *= inv_D[i][i]
    for i in range(0, len(L)):
        for j in range(0, len(L[i])):
            L[i][j] *= inv_D[i][i]
    for i in range(0, len(U)):
        for j in range(0, len(U[i])):
            U[i][j] *= inv_D[i][i]
    iter = 1000
    n = len(x)
    for k in range(0, iter):
        for i in range(0, n):
            x[i] = b[i]
            for j in range(0, i):
                x[i] -= L[i][j] * x[j]
            for j in range(i+1, n):
                x[i] -= U[i][j] * x[j]

    return x


def main():
    # TODO wczytywanie do poprawy
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
    print(gauss_seidel_method(matrix, 0)) # TODO wywołanie do popaawy (argumenty)
    print(matrix)


if __name__ == "__main__":
    main()
