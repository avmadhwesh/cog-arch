import sys
sys.path.append("build")
import py_random_points

# pipe the output of this file to a csv, and then analyze it


print("n,z_score,vacuumed_z_score")
for n in range(10, 101, 5):
    for _ in range(100000):
        stimulus = py_random_points.make_points(n)
        print(f"{n},{stimulus['z_score']},{stimulus['vacuumed_z_score']}")
