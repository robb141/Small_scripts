# 1. task
'''
Function that accepts an NxN list of lists and sums the two main diagonals.

EXAMPLES:


list1 = [
  [ 1, 2 ],
  [ 3, 4 ]
]

sum_up_diagonals(list1) # 10

list2 = [
  [ 1, 2, 3 ],
  [ 4, 5, 6 ],
  [ 7, 8, 9 ]
]

sum_up_diagonals(list2) # 30

list3 = [
  [ 4, 1, 0 ],
  [ -1, -1, 0],
  [ 0, 0, 9]
]

sum_up_diagonals(list3) # 11

list4 = [
  [ 1, 2, 3, 4 ],
  [ 5, 6, 7, 8 ],
  [ 9, 10, 11, 12 ],
  [ 13, 14, 15, 16 ]
]

sum_up_diagonals(list4) # 68
'''


def sum_up_diagonals(matrix):
    return sum(matrix[i][i] + matrix[i][len(matrix[i]) - 1 - i] for i in range(len(matrix)))


# 2. task
'''
min_max_key_in_dictionary({2:'a', 7:'b', 1:'c',10:'d',4:'e'}) # [1,10]
min_max_key_in_dictionary({1: "Elie", 4:"Matt", 2: "Tim"}) # [1,4]
'''

def min_max_key_in_dictionary(d):
    return [min(d.keys()), max(d.keys())]


# 3. task
'''
find_greater_numbers([1,2,3]) # 3 
find_greater_numbers([6,1,2,7]) # 4
find_greater_numbers([5,4,3,2,1]) # 0
find_greater_numbers([]) # 0
'''
def find_greater_numbers(nums):
    if len(nums) < 2:
        return 0
    result = 0
    for i in range(len(nums) - 1):
        for j in range(i + 1, len(nums)):
            if nums[i] < nums[j]:
                result += 1
    return result


# 4. task
'''
two_oldest_ages( [1, 2, 10, 8] ) # [8, 10]
two_oldest_ages( [6,1,9,10,4] ) # [9,10]
two_oldest_ages( [4,25,3,20,19,5] ) # [20,25]
'''
def two_oldest_ages(nums):
    if len(nums) < 2:
        return "Length of list is less than 2!"
    old1 = 0
    old2 = 0
    for i in range(len(nums)):
        curr = nums[i]
        if curr <= old2 <= old1:
            continue
        elif old2 <= curr <= old1:
            old2 = curr
        elif curr >= old1:
            old2 = old1
            old1 = curr
        else:
            raise ValueError(f"Something is not right, values of curr, old1 and old 2 are {curr}, {old1} and {old2}")
    return [old2, old1]


# 5. task
'''
is_odd_string('a') # True
is_odd_string('aaaa') # False
is_odd_string('amazing') # True
is_odd_string('veryfun') # True
is_odd_string('veryfunny') # False
'''
def is_odd_string(string):
    abc = 'abcdefghijklmnopqrstuvwxyz'
    suma = 0
    for i in string:
        suma += abc.index(i) + 1
    return suma % 2 != 0

