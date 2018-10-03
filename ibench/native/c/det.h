#include "bench.h"

class det_C : public Bench {
 public:
  det_C();
  ~det_C();
  void make_args(int size);
  void compute();
 private:
  double *x_mat, *r_mat;
  int *ipiv;
  int n,m,lda;
  int mn_min;
  double result;
};

det_C::det_C() {
  r_mat = 0;
  ipiv = 0;
  x_mat = 0;
}

void
det_C::make_args(int size) {
  n = size;
  m = size;
  mn_min = min(m, n);
  lda = size;
  int mat_size = m*n;
  assert(m == n);

  /* input matrix */
  x_mat = make_random_mat(mat_size);

  /* list of pivots */
  ipiv = (int *) mkl_malloc(mn_min * sizeof(int), 64);
  assert(ipiv);

  /* matrix for result */
  r_mat = make_random_mat(mat_size);
}

void det_C::compute() {
  /* compute pivoted lu decomposition */
  int info = LAPACKE_dgetrf(LAPACK_ROW_MAJOR, m, n, r_mat, lda, ipiv);
  assert(info == 0);

  double t = 1.0;
  int i,j;
  for(i=0, j=0; i < mn_min; i++, j+= lda+1) {
    t *= (ipiv[i]==i) ? r_mat[j] : -r_mat[j];
  }
  result = t;
}

det_C::~det_C() {
  if (r_mat) mkl_free(r_mat);
  if (ipiv) mkl_free(ipiv);
  if (x_mat) mkl_free(x_mat);
}
