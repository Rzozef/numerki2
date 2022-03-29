import numpy as np


def is_good_enough(x_previous, x_current, epsilon):
    return abs(x_current - x_previous) < epsilon


def load_from_file(path):
    m = []
    count_rows = 0
    with open(path) as file:
        for line in file:
            m.append(line.split())
            count_rows += 1
    m2 = []
    for i in range(count_rows):
        for j in range(len(m[i])):
            m2.append(int(m[i][j].rstrip(',')))
    m3 = []
    matrix = []
    for i in range(count_rows):
        for j in range(len(m[i])):
            m3.append(m2[i * len(m[i]) + j])
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


def is_diagonally_dominant(matrix):  # mozliwe ze sie nie przyda
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
    # dorobic sprawdzanie warunkow koniecznych TODO
    b = return_b(matrix)
    a = return_a(matrix)
    x = [0, 0, 0]  # do poprawy zeby bylo dostosowane do kazdej ilosci rownan
    x = np.asmatrix(x)
    x.transpose()
    for k in range(a.shape[0]):
        b_k = b[k]
        for j in range(a.shape[1]):
            if j != k:
                b_k -= a[k][j] * x[j]  # zly wzor
        x[k] = b_k / a[k][k]
    return x


def main():
    print(load_from_file("r1.txt"))


if __name__ == "__main__":
    main()
