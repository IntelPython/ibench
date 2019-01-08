/*
 * Copyright (C) 2019 Intel Corporation
 *
 * SPDX-License-Identifier: MIT
 */

#include "bench.h"

class cholesky_C : public Bench {
 public:
  cholesky_C();
  ~cholesky_C();
  void make_args(int size);
  void compute();

 private:
  double *x_mat, *r_mat;
  int n,lda;
};


cholesky_C::cholesky_C() {
  x_mat = r_mat = 0;
}

void
cholesky_C::make_args(int size) {
  n = lda = size;

  int mat_size = n*n;
  int r_size = mat_size;

  /* input matrix */
  x_mat = make_random_mat(mat_size);

  /* matrix for result */
  r_mat = make_mat(r_size);
  memset(r_mat, 0, r_size * sizeof(*r_mat));
  // Set r_mat to identity matrix as in python bench
  for (int i = 0; i < n; i++) r_mat[i*n+i] = 1;
  cblas_dsyrk(CblasColMajor, CblasUpper, CblasNoTrans, n, n, 1.0, x_mat, lda, n, r_mat, lda);

  // we now have r_mat = x_mat * x_mat' + n * np.eye(n)
  // copy back into x_mat
  mkl_domatcopy('R', 'N', n, n, 1.0, r_mat, n, x_mat, n);
}

void cholesky_C::compute() {
  /* compute cholesky decomposition */
  int info = LAPACKE_dpotrf(LAPACK_COL_MAJOR, 'U', n, r_mat, lda);
  assert(info == 0);

}

cholesky_C::~cholesky_C() {
  if (r_mat) mkl_free(r_mat);
  if (x_mat) mkl_free(x_mat);
}
