# 1. task
'''
counter = letter_counter('Amazing')
counter('a') # 2
counter('m') # 1

counter2 = letter_counter('This Is Really Fun!')
counter2('i') # 2
counter2('t') # 1
'''


def letter_counter(string):
    def count_it(x):
        return string.lower().count(x)
    return count_it


# 2. Task
'''
def add(a,b):
    return a+b

oneAddition = once(add)

oneAddition(2,2) # 4
oneAddition(2,2) # None
oneAddition(12,200) # None
'''
def once(f):
    n = 1

    def wrapper(a, b):
        nonlocal n
        if n > 1:
            return None
        n += 1
        return f(a, b)
    return wrapper


@once
def add(a,b):
    return a+b


# 3.task
'''
primes = next_prime()
[next(primes) for i in range(25)]
# [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]
'''
def next_prime():
    i = 2
    while True:
        flag = False
        for j in range(2, (i//2)+1):
            if i % j == 0:
                flag = True
                break
        if not flag:
            yield i
        i += 1


# primes = next_prime()
# print([next(primes) for i in range(25)])

