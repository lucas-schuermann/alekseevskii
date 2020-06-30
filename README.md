# alekseevskii
Exhaustive numerical admissibility analysis of spatial blocks towards a resolution of the Alekseevkii Conjecture

Updated for modern python/opencl

## Notes
- `blocking` contains an implementation of a numerical search algorithm in python and cython
  - blocks are sampled from the unit cube of a specified dimension in R^n
  - each is checked for a number of necessary conditions given by the conjecture: sphere admissibility, jacobi condition, and possibility of Einstein metrics
  - for a few related ideas, please see [Arroyo and Lafuente](https://arxiv.org/abs/1503.07079), [Jablonski and Petersen](https://arxiv.org/abs/1403.5037), or [Prof. Jablonski's research statement](http://www2.math.ou.edu/~mjablonski/math/#research)
- `tests` include a simple benchmark of computing spatial array index
- `opencl_helper.py` provides a nice wrapper around `pyopencl` for loading simple kernels and running sequences over sets of numpy arrays

## License
[MIT](https://lucasschuermann.com/license.txt)
