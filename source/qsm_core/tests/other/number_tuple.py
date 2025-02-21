# coding:utf-8
def find_ranges(nums):
    if not nums:
        return []

    nums = sorted(nums)
    result = []
    start = nums[0]
    end = nums[0]

    for i in range(1, len(nums)):
        if nums[i] == end + 1:
            end = nums[i]
        else:
            if start == end:
                result.append(start)
            else:
                result.append((start, end))
            start = nums[i]
            end = nums[i]

    if start == end:
        result.append(start)
    else:
        result.append((start, end))

    return result


if __name__ == '__main__':
    print find_ranges([0, 1, 3, 4, 5, 7, 9, 10, 11, 100])