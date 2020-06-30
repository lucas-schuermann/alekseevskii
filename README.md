# alekseevskii
Exhaustive numerical admissibility analysis of spatial blocks towards a resolution of the Alekseevkii Conjecture

Updated for modern python/opencl

## Notes

- `blocking` contains an implementation of a numerical search algorithm in python and cython
  - 
  - for a few related ideas, please see [Arroyo and Lafuente](https://arxiv.org/abs/1503.07079), [Jablonski and Petersen](https://arxiv.org/abs/1403.5037), or [Prof. Jablonski's research statement](http://www2.math.ou.edu/~mjablonski/math/#research)
- `tests` include a simple benchmark of computing spatial array index
- `opencl_helper.py` provides a nice wrapper around `pyopencl` for loading simple kernels and running sequences over sets of numpy arrays

## License
[MIT](https://lucasschuermann.com/license.txt)
