import math
from inspect import signature, getfullargspec


# Exercitiul 1
# a
# import utils
# b
# import app


# Exercitiul 2
def sum_keyword(*no_keyword, **keyword):
    return sum([keyword[letter] for letter in keyword])


anonymous = lambda *no_keyword, **keyword: sum([keyword[letter] for letter in keyword])

print(sum_keyword(1, 2, c=3, d=4))
print(anonymous(1, 2, c=3, d=4))
print(sum_keyword(c=3, d=4))
print(anonymous(c=3, d=4))
print(sum_keyword(3))
print(anonymous(3))


# Exercitiul 3
def generate_vowels_list_comprehension(phrase):
    return [letter for letter in phrase if letter.lower() in {'a', 'e', 'i', 'o', 'u'}]


def generate_vowels_filter_lambda(phrase):
    return list(filter(lambda letter: letter.lower() in {'a', 'e', 'i', 'o', 'u'}, phrase))


generate_vowels_lambda = lambda phrase: [letter for letter in phrase if letter.lower() in {'a', 'e', 'i', 'o', 'u'}]

print(generate_vowels_list_comprehension("Programming In Phyton is FuUn"))
print(generate_vowels_filter_lambda("Programming In Phyton is FuUn"))
print(generate_vowels_lambda("Programming In Phyton is FuUn"))


# Exercitiul 4
def my_function(*no_keyword, **keyword):
    result = [argument for argument in no_keyword if type(argument) is dict and len(argument.keys()) >= 2 and
              len([key for key in argument.keys() if type(key) is str and len(key) >= 3]) > 0]
    second_result = [keyword[argument] for argument in keyword if type(keyword[argument]) is dict and
                     len(keyword[argument].keys()) >= 2 and
                     len([key for key in keyword[argument].keys() if type(key) is str and len(key) >= 3]) > 0]
    result.append(*second_result)
    return result


print(my_function({1: 2, 3: 4, 5: 6}, {'a': 5, 'b': 7, 'c': 'e'}, {2: 3}, [1, 2, 3], {'abc': 4, 'def': 5},
                  3764, dictionar={'ab': 4, 'ac': 'abcde', 'fg': 'abc'}, test={1: 1, 'test': True}))


# Exercitiul 5
def my_function(list_of_things):
    return [thing for thing in list_of_things if type(thing) in {int, float, complex}]


print(my_function(my_function([1, "2", {"3": "a"}, {4, 5}, 5, 6, 3.0, complex(8, 1)])))


# Exercitiul 6
def my_function(list_of_numbers):
    try:
        for thing in list_of_numbers:
            if type(thing) is not int:
                raise ValueError("Not all list elements are of integer type")
    except ValueError as err:
        return str(err)
    else:
        even = [number for number in list_of_numbers if number % 2 == 0]
        odd = [number for number in list_of_numbers if number % 2 != 0]
        maximum = max(len(even), len(odd))
        even.extend([None for x in range(0, maximum - len(even))])
        odd.extend([None for x in range(0, maximum - len(odd))])
        return list(zip(even, odd))


print(my_function([1, 3, 5, 2, 8, 7, 4, 10, 9, 2]))
print(my_function([1, 3, 5, 2, 8, 7, 4, 10, 9, 2, 1]))
print(my_function([1, 3, 5, 2, 8, 7, 4, 10, 9, 2, 8]))
print(my_function([1, 3, 5, 2, 8, 7.5, 'blabla', 10, 9, 2, 8]))


# Exercitiul 7
def sum_digits(x):
    return sum(map(int, str(x)))


def fibonacci():
    result = [0, 1]
    for index in range(2, 1000):
        result.append(result[index - 2] + result[index - 1])
    return result


def process(**keyword):
    fibo = fibonacci()
    if "filters" in keyword:
        if type(keyword["filters"]) is not list:
            raise ValueError("Argument must be a list of filters")
        for each_filter in keyword["filters"]:
            if each_filter(fibo[0]) is not (True or False):
                raise ValueError("Function must return boolean")
        fibo = [elem for elem in fibo if all(each_filter(elem) for each_filter in keyword["filters"])]
    if "offset" in keyword:
        if keyword["offset"] > len(fibo):
            raise ValueError("Parameter offset exceeds the length of the (filtered) Fibo list")
        else:
            fibo = fibo[keyword["offset"]:]
    if "limit" in keyword:
        if keyword["limit"] > len(fibo):
            raise ValueError("Parameter limit exceeds the length of the (filtered, starting from offset) Fibo list")
        else:
            fibo = fibo[:keyword["limit"]]
    return fibo


try:
    print(process(filters=[lambda item: item % 2 == 0, lambda item: item == 2 or 4 <= sum_digits(item) <= 20],
                  limit=2, offset=2))
    print(process(filters=[lambda item: item % 2 == 0, lambda item: item == 2 or 4 <= sum_digits(item) <= 20],
                  limit=0, offset=8))
    print(process(filters=[lambda item: item % 2 == 0, lambda item: item == 2 or 4 <= sum_digits(item) <= 20],
                  limit=1, offset=8))
except (ValueError, TypeError) as err:
    print(str(err))

try:
    print(process(filters=[lambda item: item % 2 == 0, lambda digit, item: item == 2 or 4 <= sum_digits(item) <= 20],
                  limit=2, offset=2))
except (ValueError, TypeError) as err:
    print(str(err))

try:
    print(process(filters=[lambda item: item % 2 == 0, sum_digits],
                  limit=2, offset=2))
except (ValueError, TypeError) as err:
    print(str(err))

try:
    print(process(filters=[lambda item: item % 2 == 0, lambda item: item + 'aaa'],
                  limit=2, offset=2))
except (ValueError, TypeError) as err:
    print(str(err))


# Exercitiul 8
def print_arguments(function):
    args = getfullargspec(function)
    definition = "global new_function\ndef new_function" + str(signature(function)) + ":\n\t" +\
        "print(\"Arguments are: (\""
    if args[0] is not None:
        for arg in args[0]:
            definition += " + str(" + arg + ")" + " + \",\""
    definition += " + \"), {\""
    if args[2] is not None:
        kwargs = args[2]
        if type(args[2]) != list:
            kwargs = [args[2]]
        for arg in kwargs:
            definition += " + str(" + arg + ")" + " + \",\""
    definition += " + \"}\")\n\t" +\
        "return " + str(function.__name__) + str(signature(function))
    exec(definition)
    return new_function


def multiply_by_two(x, **kargs):
    return x * 2


def add_numbers(a, b):
    return a + b


augmented_multiply_by_two = print_arguments(multiply_by_two)
trial = augmented_multiply_by_two(10, a=10, b=20)

augmented_add_numbers = print_arguments(add_numbers)
trial1 = augmented_add_numbers(3, 4)


def multiply_by_three(x):
    return x * 3


def multiply_output(function):
    definition = "global new_function_b\nnew_function_b = lambda " + str(signature(function))[1:-1] + \
                 ": 2 * " + str(function.__name__) + str(signature(function))
    exec(definition)
    return new_function_b


augmented_multiply_by_three = multiply_output(multiply_by_three)
trial2 = augmented_multiply_by_three(10)  # this will return 2 * (10 * 3)
print(trial2)


def augment_function(function, decorators):
    definition = "global new_function_c\ndef new_function_c" + str(signature(function)) + ":\n\t"
    definition += "last_function = " + str(function.__name__) + "\n\t"
    for decorator in decorators:
        definition += "last_function = " + decorator.__name__ + "(last_function)\n\t"
    definition += "return last_function" + str(signature(function))
    exec(definition)
    return new_function_c


decorated_function = augment_function(add_numbers, [print_arguments, multiply_output])
trial3 = decorated_function(3, 4)
print(trial3)


# Exercitiul 9
def f9(pairs):
    result = []
    try:
        if type(pairs) != list:
            raise ValueError("Argument is not a list")
        for pair in pairs:
            if type(pair) != tuple:
                raise ValueError("List element is not a tuple")
            if len(pair) != 2 or type(pair[0]) != int or type(pair[1]) != int:
                raise ValueError("Tuple is not formed of two integers")
    except ValueError as err:
        return str(err)
    else:
        for pair in pairs:
            pair_dict = dict()
            pair_dict["sum"] = sum(pair)
            pair_dict["prod"] = math.prod(pair)
            pair_dict["pow"] = int(math.pow(*pair))
            result.append(pair_dict)
        return result


print(f9(pairs=[(5, 2), (19, 1), (30, 6), (2, 2)]))
