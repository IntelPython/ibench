#include "bench.h"

class dot_C : public Bench {
 public:
  dot_C() {
    a_mat = 0;
    b_mat = 0;
    r_mat = 0;
  }

  ~dot_C() {
    if (a_mat)
      mkl_free(a_mat);
    if (b_mat)
      mkl_free(b_mat);
    if (r_mat)
      mkl_free(r_mat);
  }

  void make_args(int size) {
    m = n = k = size;
    
    a_mat = make_random_mat(m*k);
    b_mat = make_random_mat(k*n);
    r_mat = make_random_mat(m*n);
  }

  void compute() {
    double alpha = 1.0; 
    double beta = 0.0;

    cblas_dgemm(CblasRowMajor, CblasNoTrans, CblasNoTrans, 
                n, n, k, alpha, a_mat, k, b_mat, n, beta, r_mat, n);
  }

 private:
  double *a_mat, *b_mat, *r_mat;
  int m,n,k;
};
