# coding:utf-8
import bisect


def _find_closest_frame(frames, target):
    pos = bisect.bisect_left(frames, target)
    if pos == 0:
        return frames[0]
    if pos == len(frames):
        return frames[-1]

    before = frames[pos-1]
    after = frames[pos]
    if after-target < target-before:
        return after
    return before


# print _find_closest_frame([1, 2, 3, 10], 7)


a = [(2, 3), (-1, 2)]

a.sort()

print a
