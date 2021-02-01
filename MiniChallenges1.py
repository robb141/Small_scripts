# 1. task
'''
reverse_string('awesome') # 'emosewa'
reverse_string('Colt') # 'tloC'
reverse_string('Elie') # 'eilE'
'''
# add whatever parameters you deem necessary - good luck!
def reverse_string(s):
    # implement your function here
    return s[::-1]

# 2. task
'''
list_check([[],[1],[2,3], (1,2)]) # False
list_check([1, True, [],[1],[2,3]]) # False
list_check([[],[1],[2,3]]) # True
'''
def list_check(*args):
    return all(type(a) == list for a in args[0])


# 3. task
'''
remove_every_other([1,2,3,4,5]) # [1,3,5] 
remove_every_other([5,1,2,4,1]) # [5,2,1]
remove_every_other([1]) # [1] 
'''
def remove_every_other(nums):
    return [nums[i] for i in range(len(nums)) if i % 2 == 0]


# 4. task
'''
sum_pairs([4,2,10,5,1], 6) # [4,2]
sum_pairs([11,20,4,2,1,5], 100) # []
'''
def sum_pairs(nums, x):
    for i in range(len(nums) - 1):
        if nums[i] + nums[i+1] == x:
            return [nums[i], nums[i+1]]
    return []


# 5. task
'''
vowel_count('awesome') # {'a': 1, 'e': 2, 'o': 1}
vowel_count('Elie') # {'e': 2, 'i': 1}
vowel_count('Colt') # {'o': 1}
'''

def vowel_count(string):
    return {x: string.lower().count(x) for x in 'aeiou' if string.count(x)}
