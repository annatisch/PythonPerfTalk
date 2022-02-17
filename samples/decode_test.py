import os
from decode_v1 import decode_frame as decode1
from decode_vlatest import decode_frame as decode2

frame_bytes = b'\x00S\x11\xc0\x15\x08@Cp\x00\x01\x00\x00p\x00\x01\x00\x00p\xff\xff\xff\xff@@@'


### timeit comparison

import timeit

t = timeit.timeit(lambda: decode1(frame_bytes), number=15000)
print(f"Time to decode 15k frames v1: {t}")
t = timeit.timeit(lambda: decode2(memoryview(frame_bytes)), number=15000)
print(f"Time to decode 15k frames v2: {t}")



### running the profiler in code

import cProfile

def decode_lots_of_frames1(n):
    for _ in range(n):
        decode1(frame_bytes)

def decode_lots_of_frames2(n):
    memview_bytes = memoryview(frame_bytes)
    for _ in range(n):
        decode2(memview_bytes)

if __name__ == '__main__':
    for index, decoder in enumerate([decode_lots_of_frames1, decode_lots_of_frames2]):
        profile = cProfile.Profile()
        try:
            profile.enable()
            decoder(150000)
        finally:
            profile.disable()
        profile_name = "{}/decode{}_results".format(os.getcwd(), index)
        profile.dump_stats(profile_name)
