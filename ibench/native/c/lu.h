#include "bench.h"

class lu_C : public Bench {
 public:
  lu_C();
  ~lu_C();
  void make_args(int size);
  void compute();

 private:
  int *ipiv;
  double *x_mat, *r_mat, *l_mat, *u_mat, *p_mat;
  int m,n,lda,mn_min;
  int l_size, u_size, p_size;
};


lu_C::lu_C() {
  x_mat = r_mat = l_mat = u_mat = p_mat = 0;
}

void
lu_C::make_args(int size) {
  m = n = lda = size;

  int mat_size = m*n;
  int r_size = mat_size, 

  mn_min = min(m, n);
  l_size = m*mn_min;
  u_size = mn_min*n;
  p_size = m*m;

  /* input matrix */
  x_mat = make_random_mat(mat_size);

  /* list of pivots */
  ipiv = (int *) mkl_malloc(mn_min * sizeof(int), 64);
  assert(ipiv);

  /* matrix for result */
  r_mat = make_random_mat(r_size);

  /* lower-triangular matrix */
  l_mat = make_random_mat(l_size);

  /* upper triangular matrix */
  u_mat = make_random_mat(u_size);

  /* permutation matrix */
  p_mat = make_random_mat(p_size);

  mkl_domatcopy('R', 'T', m, n, 1.0, x_mat, n, r_mat, m);
  lda = m + n - lda;
}

void lu_C::compute() {
  /* compute pivoted lu decomposition */
  int info = LAPACKE_dgetrf(LAPACK_COL_MAJOR, m, n, r_mat, lda, ipiv);
  assert(info == 0);

  int ld_l = m;
  int ld_u = mn_min;
  int ld_p = m;
  memset(l_mat, 0, l_size * sizeof(double));
  memset(u_mat, 0, u_size * sizeof(double));

  /* extract L and U matrix elements from r_mat */
  #pragma ivdep
  for(int i = 0; i < m; i++) {
    #pragma ivdep
    for(int j = 0; j < n; j++){
      if (j < mn_min) {
        if(i == j) {
          l_mat[j * ld_l + i] = 1.0;
        } else if (i > j) {
          l_mat[j * ld_l + i] = r_mat[j * lda + i];
        } 
      }
      if (i < mn_min) {
        if(i <= j) 
          u_mat[j * ld_u + i] = r_mat[j * lda + i];
      }
    }
  }

  /* make a diagonal matrix (m,m) */
  memset(p_mat, 0, p_size * sizeof(double)); 
  for(int i = 0; i < m; i++) p_mat[i*(m + 1)] = 1.0;    

  info = LAPACKE_dlaswp(LAPACK_COL_MAJOR, m, p_mat, m, 1, mn_min, ipiv, -1);
  assert(info == 0);
}

lu_C::~lu_C() {
  if (l_mat) mkl_free(l_mat);
  if (u_mat) mkl_free(u_mat);
  if (r_mat) mkl_free(r_mat);
  if (p_mat) mkl_free(p_mat);

  if (ipiv) mkl_free(ipiv);
  if (x_mat) mkl_free(x_mat);
}
