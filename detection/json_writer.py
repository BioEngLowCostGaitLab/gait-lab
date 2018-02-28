import json
from functions import marker_sequence, generate_full_json_string
import numpy as np


s1c1 = marker_sequence('blue', 5, 0)
s1c1.set_coordinates((1, 1), 0)
s1c1.set_coordinates((2, 2), 1)
s1c1.set_coordinates((3, 3), 2)
s1c1.set_coordinates((4, 4), 3)
s1c1.set_coordinates((5, 5), 4)

s2c1 = marker_sequence('yellow', 5, 1)
s2c1.set_coordinates((10, 10), 1)
s2c1.set_coordinates((10, 10), 2)
s2c1.set_coordinates((10, 10), 3)
s2c1.set_coordinates((10, 10), 4)

s1c2 = marker_sequence('blue', 5, 0)
s1c2.set_coordinates((11, 11), 0)
s1c2.set_coordinates((21, 21), 1)
s1c2.set_coordinates((31, 31), 2)
s1c2.set_coordinates((41, 41), 3)
s1c2.set_coordinates((51, 51), 4)

s2c2 = marker_sequence('yellow', 5, 1)
s2c2.set_coordinates((101, 101), 1)
s2c2.set_coordinates((101, 101), 2)
s2c2.set_coordinates((101, 101), 3)
s2c2.set_coordinates((101, 101), 4)

s1c1._interpolate()
s2c1._interpolate()
s1c2._interpolate()
s2c2._interpolate()

cam_1_sequences = [s1c1, s2c1]
cam_2_sequences = [s1c2, s2c2]

all_sequences = [cam_1_sequences, cam_2_sequences]


full_string = generate_full_json_string(all_sequences, 2)

with open('test.json', 'w') as f:
    json.dump(full_string, f, indent=1)
