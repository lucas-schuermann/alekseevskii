__author__ = 'Lucas'

import numpy as np

from opencl import CL

# Testing the OpenCL API for use with the blocking vectors of 90 doubles (float64 datatype)


if __name__ == "__main__":
    cl = CL()

    # arbitrary constant
    side_length = 1

    prog = 0
    cl.add_program(prog, "kernels.cl")
    float90 = np.array(np.array([0.] * 90, dtype=np.float64), dtype=np.array(dtype=np.float64))
    cl.add_read_buffer(prog, "block_pos", float90)
    cl.add_write_buffer(prog, "out_pos", float90)
    cl.add_read_buffer(prog, "sidelen", side_length)

    # enqueue find_next_batch(vec90 in, vec90 out, double sidelen
    cl.execute_program_kernel(prog, "find_next_batch", "block_pos", "out_pos", "sidelen")
    positions = cl.read_buffer(prog, "out_pos", float90.size, float90.dtype)