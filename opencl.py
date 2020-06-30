# OpenCL helper class based upon pyopencl
#
# For more information on usage see the example below but most of the methods are meant to be
# self-explanatory. Read on opencl usage and possibly pyopencl before using and/or extending to use
# more complex methods. For the needs at hand most OpenCL testing at least could be implemented
# using this library

import pyopencl as cl
import numpy
from collections import defaultdict


class CL:

    def __init__(self):
        platform = cl.get_platforms()
        my_gpu_devices = platform[0].get_devices(device_type=cl.device_type.GPU)
        self.ctx = cl.Context(devices=my_gpu_devices)
        print("Using CL Device:", self.ctx.devices[0].vendor,
              self.ctx.devices[0].name)
        self.queue = cl.CommandQueue(self.ctx)
        self.programs = {}
        self.buffers = defaultdict(dict)

    def add_program(self, name, filename):
        f = open(filename, 'r')
        fstr = "".join(f.readlines())
        self.programs[name] = cl.Program(self.ctx, fstr).build()
        print("Added program", "\"" + name + "\"")

    def build_program(self, name, fstr):
        self.programs[name] = cl.Program(self.ctx, fstr).build()
        print("Added program", "\"" + name + "\"")

    def add_read_buffer(self, program, name, data):
        mf = cl.mem_flags
        self.buffers[program][name] = cl.Buffer(self.ctx,
                                                mf.READ_ONLY | mf.COPY_HOST_PTR,
                                                hostbuf=data)
        print("Added read buffer", "\"" + name + "\"", "to program",
              "\"" + program + "\"")

    def add_intermediate_buffer(self, program, name, data):
        mf = cl.mem_flags
        self.buffers[program][name] = cl.Buffer(self.ctx,
                                                mf.READ_WRITE |
                                                mf.COPY_HOST_PTR,
                                                hostbuf=data)

    def add_write_buffer(self, program, name, nbytes):
        mf = cl.mem_flags
        self.buffers[program][name] = cl.Buffer(self.ctx, mf.WRITE_ONLY, nbytes)
        print("Added write buffer", "\"" + name + "\"", "to program", program)

    def read_buffer(self, program, name, size, dtype):
        result = numpy.array(list(range(size)), dtype=dtype)
        print("Enqueueing buffer copy for", "\"" + name + "\"", "of program", "\"" + program + "\"", \
              "with size", result.size, "and type", dtype)
        cl.enqueue_copy(self.queue, result, self.buffers[program][name]).wait()
        return result

    def execute_program_kernel(self, program, kernel, dim, *args):
        print("Enqueueing kernel", "\"" + kernel + "\"", "of program", "\"" + program + "\"", "with arguments", \
              list(args))
        args = [self.buffers[program][i] for i in args]
        self.programs[program].__getattr__(kernel)(self.queue, dim, None, *args)


if __name__ == "__main__":
    cltest = CL()
    cltest.build_program("Test", (
        "__kernel void test(__global float* a, __global float* b, __global float* c)\n"
        "{\n"
        "    unsigned int i = get_global_id(0);\n"
        "    c[i] = a[i] + b[i];\n"
        "}\n"))
    test_array = numpy.array(list(range(10)), dtype=numpy.float32)
    cltest.add_read_buffer("Test", "a", test_array)
    cltest.add_read_buffer("Test", "b", test_array)
    cltest.add_write_buffer("Test", "c", test_array.nbytes)
    cltest.execute_program_kernel("Test", "test", test_array.shape, "a", "b",
                                  "c")
    a = cltest.read_buffer("Test", "a", test_array.size, test_array.dtype)
    b = cltest.read_buffer("Test", "b", test_array.size, test_array.dtype)
    c = cltest.read_buffer("Test", "c", test_array.size, test_array.dtype)
    print("Array A:", list(a))
    print("Array B:", list(b))
    print("Result (A+B):", list(c))
