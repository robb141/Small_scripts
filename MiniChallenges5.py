# 1. task
'''
valid_parentheses("()") # True
valid_parentheses(")(()))") # False
valid_parentheses("(") # False
valid_parentheses("(())((()())())") # True
valid_parentheses('))((') # False
valid_parentheses('())(') # False
valid_parentheses('()()()()())()(') # False
'''
def valid_parentheses(text):
    count_start = 0
    for s in text:
        if s == '(':
            count_start += 1
        elif s == ')':
            count_start -= 1
        if count_start < 0:
            return False
    return count_start == 0


# 2. task
'''
reverse_vowels("Hello!") # "Holle!" 
reverse_vowels("Tomatoes") # "Temotaos" 
reverse_vowels("Reverse Vowels In A String") # "RivArsI Vewols en e Streng"
reverse_vowels("aeiou") # "uoiea"
reverse_vowels("why try, shy fly?") # "why try, shy fly?"
'''
def reverse_vowels(string):
    vowels = 'aeiou'
    s = list(string)
    i, j = 0, len(s) - 1
    while i < j:
        if s[i].lower() not in vowels:
            i += 1
        elif s[j].lower() not in vowels:
            j -= 1
        else:
            s[i], s[j] = s[j], s[i]
            i += 1
            j -= 1
    return "".join(s)


# 3. task
'''
three_odd_numbers([1,2,3,4,5]) # True
three_odd_numbers([0,-2,4,1,9,12,4,1,0]) # True
three_odd_numbers([5,2,1]) # False
three_odd_numbers([1,2,3,3,2]) # False
'''
def three_odd_numbers(nums):
    if len(nums) < 3:
        return False
    for i in range(len(nums)):
        if i + 3 > len(nums):
            return False
        elif sum(nums[i:i+3]) % 2 != 0:
            return True


# 4. task
'''
mode([2,4,1,2,3,3,4,4,5,4,4,6,4,6,7,4]) # 4
'''
def mode(nums):
    d = {v: nums.count(v) for v in nums}
    return max(d, key=d.get)


# 5.task
'''
rAvg = running_average()
rAvg(10) # 10.0
rAvg(11) # 10.5
rAvg(12) # 11

rAvg2 = running_average()
rAvg2(1) # 1
rAvg2(3) # 2
'''
def running_average():
    num = []

    def r_avg(digit):
        nonlocal num
        num.append(digit)
        return sum(num) / len(num)
    return r_avg
