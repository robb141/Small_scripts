# 1. task
'''
two_list_dictionary(['a', 'b', 'c', 'd'], [1, 2, 3]) # {'a': 1, 'b': 2, 'c': 3, 'd': None}
two_list_dictionary(['a', 'b', 'c']  , [1, 2, 3, 4]) # {'a': 1, 'b': 2, 'c': 3}
two_list_dictionary(['x', 'y', 'z']  , [1,2]) # {'x': 1, 'y': 2, 'z': None}
'''
def two_list_dictionary(d1, d2):
    k = len(d1)
    while k > len(d2):
        d2.append(None)
        k -= 1
    return dict(zip(d1, d2))


# 2.task
'''
range_in_list([1,2,3,4],0,2) #  6
range_in_list([1,2,3,4],0,3) # 10
range_in_list([1,2,3,4],1) #  9
range_in_list([1,2,3,4]) # 10
range_in_list([1,2,3,4],0,100) # 10
range_in_list([],0,1) # 0
'''
def range_in_list(nums, *args):
    if len(args) > 1:
        start, end = args[0], min(args[1] + 1, len(nums))
    elif len(args) == 1:
        start, end = args[0], len(nums)
    else:
        start, end = 0, len(nums)
    return sum(nums[x] for x in range(len(nums)) if start <= x < end)


# 3. task
'''
same_frequency(551122,221515) # True
same_frequency(321142,3212215) # False
same_frequency(1212, 2211) # True
'''
def same_frequency(d1, d2):
    s1 = str(d1)
    s2 = str(d2)
    return len(s1) == len(s2) and all(s1.count(x) == s2.count(x) for x in s1)


# 4. task
'''
nth(['a', 'b', 'c', 'd'], 1)  # 'b' 
nth(['a', 'b', 'c', 'd'], -2) #  'c'
nth(['a', 'b', 'c', 'd'], 0)  # 'a'
nth(['a', 'b', 'c', 'd'], -4) #  'a'
nth(['a', 'b', 'c', 'd'], -1) #  'd'
nth(['a', 'b', 'c', 'd'], 3)  # 'd'
'''
def nth(nums, i):
    return nums[i]


# 5. task
'''
find_the_duplicate([1,2,1,4,3,12]) # 1
find_the_duplicate([6,1,9,5,3,4,9]) # 9
find_the_duplicate([2,1,3,4]) # None
'''
def find_the_duplicate(nums):
    for i in range(len(nums)):
        if nums.count(nums[i]) > 1:
            return nums[i]
    return None

