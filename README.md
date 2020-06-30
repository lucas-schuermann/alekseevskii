# alekseevskii
Numerical classification of unimodular Einstein Lie groups towards resolving the long-standing generalized Alekseevskii conjecture

Updated in 2020 for modern python/opencl

## Notes
- In the 1970s, it was conjectured by D. Alekseevskii that any (non-compact) homogeneous Einstein space of negative scalar curvature is diffeomorphic to R^n. In other words, the Classical Alekseevskii Conjecture states: Given a homogeneous Einstein space G/K with negative scalar curvature, K must be a maximal compact subgroup of G [[Jablonski](https://arxiv.org/abs/1403.5037)].
- `blocking` contains an implementation of a numerical search algorithm in python and cython
  - blocks are sampled from the unit cube of a specified dimension in R^n
  - each is checked for a number of necessary conditions given by the conjecture: sphere admissibility, jacobi condition, and possibility of Einstein metrics
  - for a few related ideas, please see [Arroyo and Lafuente](https://arxiv.org/abs/1503.07079), [Jablonski and Petersen](https://arxiv.org/abs/1403.5037), or [Prof. Jablonski's research statement](http://www2.math.ou.edu/~mjablonski/math/#research)
- `tests` include a simple benchmark of computing spatial array index
- `opencl_helper.py` provides a nice wrapper around `pyopencl` for loading simple kernels and running sequences over sets of numpy arrays

## License
[MIT](https://lucasschuermann.com/license.txt)

