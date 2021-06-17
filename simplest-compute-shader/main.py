import moderngl
import numpy as np
import timeit

ARRAY_LENGTH = 4000

# create opengl context
ctx = moderngl.create_standalone_context(require=430)

# open shader source
with open("shader.comp") as f:
    gl_src = f.read()

# initialize arrays
array_a = np.random.randint(1, 100, ARRAY_LENGTH, dtype=np.int32)
array_b = np.random.randint(1, 100, ARRAY_LENGTH, dtype=np.int32)

# intitialize the compute shader
compute_shader = ctx.compute_shader(gl_src)

# initialize the buffers
# at this moment data from arrays is copied to VRAM
buffer_a = ctx.buffer(array_a)
buffer_b = ctx.buffer(array_b)

# bind them
# now data is interpreted as two SSBOs 
buffer_a.bind_to_storage_buffer(0)
buffer_b.bind_to_storage_buffer(1)

# run the shader
# at this moment will be created group_x * group_y * group_z work groups and every work group will run main function in the shader local_size_x * local_size_y * local_size_z times
# for our example there is len(array_a) work groups only in x dimension (so x coordinate of current work group is used as array index)
# and every work group is (1, 1, 1) so main function is invoked len(array_a) times with gl_WorkGroupID.x corresponding to array index
compute_shader.run(group_x=len(array_a))

# read from buffer
result = np.frombuffer(buffer_b.read(), dtype=np.int32)

# if you are trying to understand compute shaders now I hope you understand them better :)
# after this are tests and prints

print("- RESULT ACCURACY TEST -")

for a, b, c in zip(array_a, array_b, result):
    if a * b == c:
        print(f"PASSED: {a} * {b} = {c}")
    else:
        print(f"FAILED: {a} * {b} = {a * b} != {c}")

if np.array_equal(array_a * array_b, result):
    print(f"PASSED: array_a * array_b = result")
else:
    print(f"FAILED: array_a * array_b != result")

print("- TIME TEST -")

gpu_time = timeit.timeit("compute_shader.run(group_x=len(array_a))", globals=globals(), number=100)
cpu_time = timeit.timeit("array_a * array_b", globals=globals(), number=100)

print(f"CPU\t\t\tGPU")
print(f"{cpu_time * 1_000_000_000} ns\t{gpu_time * 1_000_000_000} ns")
