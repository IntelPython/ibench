/*
 * Copyright (C) 2019 Intel Corporation
 *
 * SPDX-License-Identifier: MIT
 */

#include "bench.h"

class qr_C : public Bench {
 public:
  qr_C();
  ~qr_C();
  void make_args(int size);
  void compute();

 private:
  double *x_mat, *r_mat, *tau_vec;
  int n,lda;
};


qr_C::qr_C() {
  x_mat = r_mat = tau_vec = 0;
}

void
qr_C::make_args(int size) {
  n = lda = size;

  int mat_size = n*n;

  /* input matrix */
  x_mat = make_random_mat(mat_size);

  /* upper triangular output matrix */
  r_mat = make_mat(mat_size);
  memset(r_mat, 0, mat_size * sizeof(*r_mat));

  /* tau */
  tau_vec = make_mat(n);
}

void qr_C::compute() {
  /* compute qr decomposition */
  int info = LAPACKE_dgeqrf(LAPACK_COL_MAJOR, n, n, x_mat, lda, tau_vec);
  assert(info == 0);

  /* numpy computes upper triangular part of A even when mode='raw' */
  for (int i = 0; i < n; i++) {
    memcpy(&r_mat[i*n], &x_mat[i*n], (i+1) * sizeof(*r_mat));
  }

}

qr_C::~qr_C() {
  if (x_mat) mkl_free(x_mat);
  if (r_mat) mkl_free(r_mat);
  if (tau_vec) mkl_free(tau_vec);
}
