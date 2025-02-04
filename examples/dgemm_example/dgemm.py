# UNCOMMENT THESE LINES TO EXECUTE 
from prometeo.linalg import *
from prometeo.auxl import *

class p_class:
    attr_1: int = 1
    attr_2: float = 3.0

    def method_2(self, A: pmat, B: pmat, C: pmat) -> None:
        C = A * B
        pmat_print(C)
        return

def function1(A: pmat, B: pmat, C: pmat) -> None:
    C = A * B
    pmat_print(C)
    return

def main() -> None:

    n_list: List[int] = prmt_list(int, 10) 
    n_list[0] = 1

    test_class: p_class = p_class()
    test_class.attr_1 = 2

    j: int = 0
    for i in range(10):
        j = j + 1

    while j > 0:
        j = j - 1

    n: int = 10
    A: pmat = pmat(n, n)
    A[0][2] = 2.0

    for i in range(2):
        A[0][i] = A[0][i]

    # pmat_fill(A, 1.0)

    B: pmat = pmat(n, n)
    for i in range(2):
        B[0][i] = A[0][i]
    # pmat_fill(B, 2.0)

    C: pmat = pmat(n, n)

    test_class.method_2(A, B, C)

    pmat_list: List[pmat] = prmt_list(pmat, 10)
    pmat_list[0] = A

    C = A * B
    pmat_print(C)
    C = A + B
    pmat_print(C)
    C = A - B
    pmat_print(C)

    function1(A, B, C)
    function1(pmat_list[0], B, C)

    pmat_fill(A, 0.0)
    for i in range(10):
        A[i][i] = 1.0

    pmat_print(A)

    a : pvec = pvec(10)
    a[1] = 3.0
    b : pvec = pvec(3)
    b[0] = a[1]
    b[1] = A[0][2]
    # need to fix these
    # el : double
    # el = a[1]
    # el = A[1][1]
    pvec_print(a)
    pvec_print(b)

    c : pvec = pvec(10)
    c = A * a
    pvec_print(c)

    # still to be implemented in code-generator
    # prmt_lus(A, B, C)
    # pmat_print(C)
    # D: pmat = pmat(n, n)
    # D = A*C
    # pmat_print(D)

# UNCOMMENT THESE LINES TO EXECUTE 
if __name__ == "__main__":
    # execute only if run as a script
    main()
