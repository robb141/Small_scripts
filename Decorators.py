from functools import wraps
from time import sleep

'''
@show_args
def do_nothing(*args, **kwargs):
    pass

do_nothing(1, 2, 3,a="hi",b="bye")

# Should print (on two lines):
# Here are the args: (1, 2, 3)
# Here are the kwargs: {"a": "hi", "b": "bye"}
'''


def show_args(fn):
    def wrapper(*args, **kwargs):
        print('Here are the args: {}'.format(args))
        print('Here are the kwargs: {}'.format(kwargs))
        fn(args, kwargs)
    return wrapper


@show_args
def do_nothing(*args, **kwargs):
    pass

# do_nothing(1, 2, 3,a="hi",b="bye")


# another task
'''
@double_return 
def add(x, y):
    return x + y

add(1, 2) # [3, 3]

@double_return
def greet(name):
    return "Hi, I'm " + name

greet("Rob") # ["Hi, I'm Rob", "Hi, I'm Rob"]
'''


def double_return(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        val = fn(*args, **kwargs)
        return [val, val]
    return wrapper



@double_return
def add(x, y):
    return x + y

# print(add(1, 2)) # [3, 3]

@double_return
def greet(name):
    return "Hi, I'm " + name

# print(greet("Rob")) # ["Hi, I'm Rob", "Hi, I'm Rob"]

# another task
'''
@ensure_fewer_than_three_args
def add_all(*nums):
    return sum(nums)

add_all() # 0
add_all(1) # 1
add_all(1,2) # 3
add_all(1,2,3) # "Too many arguments!"
add_all(1,2,3,4,5,6) # "Too many arguments!"
'''


def ensure_fewer_than_three_args(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if len(args) >= 3:
            return 'Too many arguments!'
        return fn(*args, **kwargs)
    return wrapper

# another task
'''
@only_ints 
def add(x, y):
    return x + y

add(1, 2) # 3
add("1", "2") # "Please only invoke with integers."
'''


def only_ints(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if all(type(arg) == int for arg in args):
            return fn(*args, **kwargs)
        return "Please only invoke with integers."
    return wrapper


@only_ints
def add(x, y):
    return x + y

# print(add(1, 2)) # 3
# print(add("1", "2")) # "Please only invoke with integers."

# another task
'''
@ensure_authorized
def show_secrets(*args, **kwargs):
    return "Shh! Don't tell anybody!"

show_secrets(role="admin") # "Shh! Don't tell anybody!"
show_secrets(role="nobody") # "Unauthorized"
show_secrets(a="b") # "Unauthorized"
'''


def ensure_authorized(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if 'role' in kwargs and kwargs['role'] == 'admin':
            return fn(*args, **kwargs)
        return "Unauthorized"
    return wrapper

@ensure_authorized
def show_secrets(*args, **kwargs):
    return "Shh! Don't tell anybody!"

# print(show_secrets(role="admin")) # "Shh! Don't tell anybody!"
# print(show_secrets(role="nobody"))  # "Unauthorized"
# print(show_secrets(a="b"))  # "Unauthorized"


# another task
'''
@delay(3)
def say_hi():
    return "hi"

say_hi()
# should print the message "Waiting 3s before running say_hi" to the console
# should then wait 3 seconds
# finally, should invoke say_hi and return "hi"
'''


def delay(value):
    def inner(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            print("Waiting {}s before running {}".format(value, fn.__name__))
            sleep(value)
            return fn(*args, **kwargs)
        return wrapper
    return inner


@delay(3)
def say_hi():
    return "hi"

# print(say_hi())
