// TODO: represent double90[n] as double[90*n]
// position = current_batch[index[i] * i]
// index(i) = 0 ... 90

__kernel void find_next_batch(__global double* current_batch, __global double* output_batch, __constant double side_length)
{
    unsigned int i = get_global_id(0);

    double position[90] = current_batch[i];
    double delta[90] = {0};

    if(i < 90)
        delta[i] = side_length;
    else
        delta[i - 90] = -side_length;

    output_batch[i] = position + delta;
}

// this could be done more efficiently by sorting the arrays and performing operations on non-redundant keys
__kernel void remove_redundancies(__global double* next_batch, __global unsigned int next_batch_size,
                                  __global double* old_batch, __global unsigned int old_batch_size, __global double* output_batch)
{
    unsigned int i = get_global_id(0);

    if(i < next_batch_size)
        double90 p0 = next_batch[i];
    else
        // TODO: handle out of bounds exception
    if(i < old_batch_size)
        double90 p1 = old_batch[i];
    else;

    // if (p0[index[i] * i] != p1[index[i] * i]
    //     add to output_batch
    // else
    //     skip - flag as none for later compacting of the array?
}