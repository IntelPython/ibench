#include "bench.h"

class inv_C : public Bench {
 public:
  inv_C() {
    x_mat = 0;
    r_mat = 0;
    ipiv = 0;
  }

  ~inv_C() {
    if (r_mat)
      mkl_free(r_mat);
    if (ipiv)
      mkl_free(ipiv);
    if (x_mat)
      mkl_free(x_mat);
  }

  void make_args(int size) {
    N = size;
    M = size;
    LDA = size;
    int mat_size = M*N, mn_min = min(M, N);

    assert(M == N);

    /* input matrix */
    x_mat = make_random_mat(mat_size);

    /* list of pivots */
    ipiv = (int *) mkl_malloc(mn_min * sizeof(int), 64);
    assert(ipiv);

    /* matrix for result */
    r_mat = make_random_mat(mat_size);
  }

  void compute() {
    /* compute pivoted lu decomposition */
    int info = LAPACKE_dgetrf(LAPACK_ROW_MAJOR, M, N, r_mat, LDA, ipiv);
    assert(info == 0);

    info = LAPACKE_dgetri(LAPACK_ROW_MAJOR, N, r_mat, LDA, ipiv);
    assert(info == 0);
  }

 private:
  double *x_mat, *r_mat;
  int *ipiv;
  int N,M,LDA;
};
