/*
 * Copyright (C) 2016 Intel Corporation
 *
 * SPDX-License-Identifier: MIT
 */

#include <algorithm>

using namespace std;
  

#include "assert.h"
#include "stdlib.h"

#if defined(__INTEL_COMPILER)

#include "mkl.h"

class Random{
 private:
  enum {SEED = 77777};
  static double const d_zero = 0.0, d_one = 1.0;
  VSLStreamStatePtr stream;

 public:
  Random() {
    int err = vslNewStream(&stream, VSL_BRNG_MT19937, SEED);
    assert(err == VSL_STATUS_OK);
  }
  ~Random() {
    int err = vslDeleteStream(&stream);
    assert(err == VSL_STATUS_OK);
  }
  void init_mat(double* mat, int size) {
    int err = vdRngGaussian(VSL_RNG_METHOD_GAUSSIAN_ICDF, stream, size, mat, d_zero, d_one);
    assert(err == VSL_STATUS_OK);
  }
};

#else

#include "lapacke.h"
#include "cblas.h"

class Random {
 public:
  void init_mat(double* mat, int size) {
  }
};

static void* mkl_malloc(int size, int align) {
   return malloc(size);
}

static void mkl_free(void*p) {
    free(p);
}
#endif


class Bench {
 private:
  Random random;
 public:

  double* make_random_mat(int size) {
    double* mat = make_mat(size);
    random.init_mat(mat,size);
    return mat;
  }

  double* make_mat(int mat_size) {
    double *mat = (double *) mkl_malloc(mat_size * sizeof(double), 64);
    assert(mat);
    return mat;
  }

  virtual void compute()=0;
};
