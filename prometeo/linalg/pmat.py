from ctypes import *
from .pmat_blasfeo_wrapper import *
from .pvec import *
from .blasfeo_wrapper import *
from multipledispatch import dispatch
from abc import ABC

class pmat_(ABC):
    pass

class pmat(pmat_):

    blasfeo_dmat = None
    _i = None
    _j = None

    def __init__(self, m: int, n: int):
        self.blasfeo_dmat = c_prmt_create_blasfeo_dmat(m, n)  
    
    def __getitem__(self, index):
        if self._i is not None:
            self._j = index
            el = self.my_get_item()
            return el

        self._i = index
        return self

    def __setitem__(self, index, value):
        self._j = index
        self.my_set_item(value)
        return
   

    def my_set_item(self, value):
        pmat_set(self, value, self._i, self._j)
        self._i = None
        self._j = None
        return

    def my_get_item(self):
        el = pmat_get(self, self._i, self._j)
        self._i = None
        self._j = None
        return el 
    
    
    # TODO(andrea): ideally one would have three levels:
    # 1) high-level
    # 2) intermediate-level 
    # 3) low-level (BLASFEO wrapper)

    # high-level linear algebra
    @dispatch(pmat_)
    def __mul__(self, other):
        if self.blasfeo_dmat.n != other.blasfeo_dmat.m:
            raise Exception('__mul__: mismatching dimensions:' 
                ' ({}, {}) x ({}, {})'.format(self.blasfeo_dmat.m, \
                self.blasfeo_dmat.n, other.blasfeo_dmat.m, \
                other.blasfeo_dmat.n))

        res = pmat(self.blasfeo_dmat.m, other.blasfeo_dmat.n)
        pmat_fill(res, 0.0)
        zero_mat = pmat(self.blasfeo_dmat.m, other.blasfeo_dmat.n)
        pmat_fill(zero_mat, 0.0)
        prmt_gemm_nn(self, other, zero_mat, res)
        return res

    @dispatch(pvec_)
    def __mul__(self, other):
        if self.blasfeo_dmat.n != other.blasfeo_dvec.m:
            raise Exception('__mul__: mismatching dimensions:' 
                ' ({}, {}) x ({},)'.format(self.blasfeo_dmat.m, \
                self.blasfeo_dmat.n, other.blasfeo_dvec.m))

        res = pvec(self.blasfeo_dmat.m)
        res.fill(0.0)
        zero_vec = pvec(self.blasfeo_dmat.m)
        zero_vec.fill(0.0)
        prmt_gemv_n(self, other, zero_vec, res)
        return res

    @dispatch(pmat_)
    def __add__(self, other):
        if self.blasfeo_dmat.m != other.blasfeo_dmat.m \
                or self.blasfeo_dmat.n != other.blasfeo_dmat.n:
            raise Exception('__add__: mismatching dimensions:' 
                ' ({}, {}) + ({}, {})'.format(self.blasfeo_dmat.m, \
                self.blasfeo_dmat.n, other.blasfeo_dmat.m, \
                other.blasfeo_dmat.n))
        res = pmat(self.blasfeo_dmat.m, self.blasfeo_dmat.n)
        pmat_copy(other, res)
        prmt_gead(1.0, self, res)
        return res 

    def __sub__(self, other):
        if self.blasfeo_dmat.m != other.blasfeo_dmat.m \
                or self.blasfeo_dmat.n != other.blasfeo_dmat.n:
            raise Exception('__sub__: mismatching dimensions:' 
                ' ({}, {}) + ({}, {})'.format(self.blasfeo_dmat.m, \
                self.blasfeo_dmat.n, other.blasfeo_dmat.m, \
                other.blasfeo_dmat.n))
        res = pmat(self.blasfeo_dmat.m, self.blasfeo_dmat.n)
        pmat_copy(self, res)
        prmt_gead(-1.0, other, res)
        return res 

def pmat_fill(A: pmat, value):
    for i in range(A.blasfeo_dmat.m):
        for j in range(A.blasfeo_dmat.n):
            A[i][j] = value
    return

def pmat_copy(A: pmat, B: pmat):
    for i in range(A.blasfeo_dmat.m):
        for j in range(A.blasfeo_dmat.n):
            B[i][j] = A[i][j]
    return

def prmt_lus(A: pmat, B: pmat, opts):
    res  = pmat(A.blasfeo_dmat.m, B.blasfeo_dmat.n)
    fact = pmat(A.blasfeo_dmat.m, B.blasfeo_dmat.m)
    # create pmat for factor
    fact = pmat(A.blasfeo_dmat.m, A.blasfeo_dmat.n)
    pmat_copy(A, fact)
    # create permutation vector
    ipiv = cast(create_string_buffer(A.blasfeo_dmat.m*A.blasfeo_dmat.m), POINTER(c_int))
    # factorize
    prmt_getrf(fact, ipiv)
    # create permuted rhs
    pB = pmat(B.blasfeo_dmat.m, B.blasfeo_dmat.n)
    pmat_copy(B, pB)
    prmt_rowpe(B.blasfeo_dmat.m, ipiv, pB)
    # solve
    prmt_trsm_llnu(A, pB)
    prmt_trsm_lunn(A, pB)
    return pB

# intermediate-level linear algebra
def prmt_gemm_nn(A: pmat, B: pmat, C: pmat, D: pmat):
    c_prmt_dgemm_nn(A, B, C, D)
    return

def prmt_gemm_nt(A: pmat, B: pmat, C: pmat, D: pmat):
    c_prmt_dgemm_nt(A, B, C, D)
    return

def prmt_gemm_tn(A: pmat, B: pmat, C: pmat, D: pmat):
    c_prmt_dgemm_tn(A, B, C, D)
    return

def prmt_gemm_tt(A: pmat, B: pmat, C: pmat, D: pmat):
    c_prmt_dgemm_tt(A, B, C, D)
    return

def prmt_gead(alpha: float, A: pmat, B: pmat):
    c_prmt_dgead(alpha, A, B)
    return

def prmt_rowpe(m: int, ipiv: POINTER(c_int), A: pmat):
    c_prmt_drowpe(m, ipiv, A)
    return

def prmt_trsm_llnu(A: pmat, B: pmat):
    c_prmt_trsm_llnu(A, B)
    return 

def prmt_trsm_lunn(A: pmat, B: pmat):
    c_prmt_trsm_lunn(A, B)
    return

def prmt_getrf(fact: pmat, ipiv):
    c_prmt_getrf(fact, ipiv);
    return 

def prmt_gemv_n(A: pmat, b: pvec, c: pvec, d: pvec):
    c_prmt_dgemv_n(A, b, c, d)
    return

# auxiliary functions
def prmt_set_data(M: pmat, data: POINTER(c_double)):
    c_prmt_set_blasfeo_dmat(M.blasfeo_dmat, data)  
    return

def pmat_set(M: pmat, value, i, j):
    c_prmt_set_blasfeo_dmat_el(value, M.blasfeo_dmat, i, j)  
    return

def pmat_get(M: pmat, i, j):
    el = c_prmt_get_blasfeo_dmat_el(M.blasfeo_dmat, i, j)  
    return el 

def pmat_print(M: pmat):
    c_prmt_print_blasfeo_dmat(M)
    return  


