#include "stdlib.h"
#include "pmat_blasfeo_wrapper.h"
#include "pvec_blasfeo_wrapper.h"
#include "prmt_heap.h"
#include "simple_example.h"



void *___c_prmt_8_heap; 
void *___c_prmt_64_heap; 
void main() {
    ___c_prmt_8_heap = malloc(1000); 
    char *mem_ptr = (char *)___c_prmt_8_heap; 
    align_char_to(8, &mem_ptr);
    ___c_prmt_8_heap = mem_ptr;
    ___c_prmt_64_heap = malloc(100000); 
    mem_ptr = (char *)___c_prmt_64_heap; 
    align_char_to(64, &mem_ptr);
    ___c_prmt_64_heap = mem_ptr;

    int n = 10;
    struct pmat * A = ___c_prmt___create_pmat(n, n);
    for(int i = 0; i < 10; i++) {
        for(int j = 0; j < 10; j++) {
            ___c_prmt___pmat_set_el(A, i, j, 1.0);
    }

    }

    struct pmat * B = ___c_prmt___create_pmat(n, n);
    for(int i = 0; i < 10; i++) {
        ___c_prmt___pmat_set_el(B, 0, i, 2.0);
    }

    struct pmat * C = ___c_prmt___create_pmat(n, n);
    ___c_prmt___pmat_fill(C, 0.0);
    ___c_prmt___dgemm(A, B, C, C);
    ___c_prmt___pmat_print(C);
}
