import math


# Exercise 1
def fibonacci(n):
    result = []
    fibo1 = 1
    fibo2 = 1
    if type(n) != int or n < 1:
        return "This is not a valid parameter."
    if n >= 1:
        result.append(fibo1)
    if n >= 2:
        result.append(fibo2)
    for i in range(3, n + 1):
        fibo3 = fibo1 + fibo2
        result.append(fibo3)
        fibo1 = fibo2
        fibo2 = fibo3
    return result


print(fibonacci("-2"))
print(fibonacci(1))
print(fibonacci(2))
print(fibonacci(20))
print(fibonacci(0))


# Exercise 2
def select_primes(list_of_numbers):
    list_of_primes = []
    for number in list_of_numbers:
        if type(number) != int:
            return "List element is not of integer type."
        if number in (2, -2):
            list_of_primes.append(number)
        if number > 4 or number < -4:
            list_of_proper_divs = [d for d in range(2, int(math.sqrt(abs(number))) + 1) if number % d == 0]
            if len(list_of_proper_divs) == 0:
                list_of_primes.append(number)
    return list_of_primes


print(select_primes([12, "abc", 23, 0, 1, 2, 3, -4, -8, 18, 31, -(-41)]))
print(select_primes([12, 23, 0, 1, 2, 3, -4, -8, -31, 18, 31, -(-41), 37]))


# Exercise 3
# def set_operations(a, b):
#     return list(set(a).union(set(b))), list(set(a).intersection(set(b))), \
#            list(set(a).difference(set(b))), list(set(b).difference(set(a)))

def set_operations(a, b):  # allowing duplicates
    union = a + b
    intersection = []
    for element in set(a):
        count_element_a = len(list(elem for elem in a if elem == element))
        count_element_b = len(list(elem for elem in b if elem == element))
        intersection += [element] * min(count_element_a, count_element_b)
    difference_a = list(elem for elem in a if len([instance for instance in b if instance == elem]) == 0)
    difference_b = list(elem for elem in b if len([instance for instance in a if instance == elem]) == 0)
    rez_tuple = (union, intersection, difference_a, difference_b)
    return rez_tuple


print(set_operations([2, 2, 4, 4, 5, 6], [4, 6, 7, 8]))
print(set_operations([2, "four", 5, 6], []))


# Exercise 4
# def compose(notes, moves, start):
#     if len(notes) > start >= 0:
#         song = [notes[start]]
#     else:
#         return "Invalid start position for the musical composition. This note does not exist."
#     current_pos = start
#     for move in moves:
#         if type(move) != int:
#             return "Invalid movement given as parameter"
#         current_pos += move
#         if len(notes) > current_pos >= 0:
#             song.append(notes[current_pos])
#         else:
#             return "Wrong sequence of moves. At least one move is impossible to make."
#     return song

def compose(notes, moves, start):  # modulo version
    if len(notes) == 0:
        return "No partiture provided."
    if len(notes) > start >= 0:
        song = [notes[start]]
    else:
        return "Invalid start position for the musical composition. This note does not exist."
    current_pos = start
    for move in moves:
        if type(move) != int:
            return "Invalid movement given as parameter"
        current_pos += move
        if len(notes) == 1:
            current_pos = 0
        else:
            if current_pos > len(notes):
                current_pos = current_pos % len(notes)
            if current_pos < 0 and len(notes) > 1:
                current_pos = len(notes) - ((-1) * current_pos) % len(notes)
        song.append(notes[current_pos])
    return song


print(compose(["do", "re", "mi", "fa", "sol"], [1, -3, 4, 2], 2))
print(compose(["do", "re", "mi", "fa", "sol"], [1, -3, 4, -3], 2))
print(compose(["do", "re", "mi", "fa", "sol"], [1, -3, 4, -5], 2))
print(compose(["do", "re", "mi", "fa", "sol"], [1, -3, 4, -5], 5))
print(compose(["do", "re", "mi", "fa", "sol"], [1, -3, 4.5, -5], 3))
print(compose(["do", "re", "mi", "fa", "sol"], [22, -22], 4))
print(compose([], [22, -22], 4))
print(compose(["do"], [22, -22], 0))
print(compose(["do", "re", "mi", "fa", "sol", "la", "si", "do"], [21, -22, -5, 8], 4))


# Exercise 5
def under_main_diagonal(matrix):
    if not all(isinstance(row, list) for row in matrix):
        return "Given argument is not a matrix made up of lists"
    for row in matrix:
        if len(row) != len(matrix):
            return "Given matrix is not a square matrix"
    no_rows_cols = len(matrix)
    for i in range(0, no_rows_cols):
        for j in range(0, i):
            matrix[i][j] = 0
    return matrix


print(under_main_diagonal([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16]]))
print(under_main_diagonal([[16]]))
print(under_main_diagonal([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15]]))
print(under_main_diagonal([[1, 2, 3, 4], "0000", [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15]]))


# Exercise 6
def count_frequency(x, *list_of_lists):
    if type(x) is not int:
        return "x can't be a measure of frequency"
    elem_frequency = dict()
    for each_list in list_of_lists:
        for element in each_list:
            if element in elem_frequency:
                elem_frequency[element] += 1
            else:
                elem_frequency[element] = 1
    x_frequency = []  # the result list
    for element in elem_frequency:
        if elem_frequency[element] == x:
            x_frequency.append(element)
    return x_frequency


print(count_frequency(2, [1, 2, 3], [2, 3, 4], [4, 5, 6], [4, 1, "test"]))
print(count_frequency("twoORNone", [1, 2, 3], [2, 3, 4], [4, 5, 6], [4, 1, "test"]))


# Exercise 7
def palindrome_or_not(list_of_numbers):
    max_palindrome = 0
    count_palindrome = 0
    for number in list_of_numbers:
        if type(number) != int:
            return "Wrong argument type inside list."
        if number < 0:
            number_string = str(number)[1:]
        else:
            number_string = str(number)
        if number_string[::-1] == number_string:
            count_palindrome += 1
            max_palindrome = max(max_palindrome, number)
    return count_palindrome, max_palindrome


print(palindrome_or_not([154456, 15456, 1325775231, 132575231, 132575231.5, 132575231]))
print(palindrome_or_not([154456, 15456, 1325775231, 132575231, 132575231]))
print(palindrome_or_not([154456, 15456, -1325775231, 132575231, 132575231]))


# Exercise 8
def ascii_divisible(list_of_strings, x=1, flag=True):
    list_for_all_strings = []
    for each_string in list_of_strings:
        list_for_character = list(character for character in each_string if
                                  (flag is True and ord(character) % x == 0 or
                                   flag is False and ord(character) % x != 0))
        if len(list_for_character) > 0:
            list_for_all_strings.append(list_for_character)
    return list_for_all_strings


print(ascii_divisible(["test", "hello", "lab002"], 2, False))
print(ascii_divisible(x=2, list_of_strings=["test", "hello", "lab002"]))
print(ascii_divisible(list_of_strings=["test", "hello", "lab002", ""]))


# Exercise 9
def taller_and_visibility(seats):
    no_rows = len(seats)
    no_columns = len(seats[1])
    for row in range(1, no_rows):
        no_columns_current = len(seats[row])
        if no_columns != no_columns_current:
            return "The stadium is not uniform, it does not contain the same number of columns for each row."
    no_visibility = []
    for column in range(0, no_columns):
        max_height = seats[0][column]
        for row in range(1, no_rows):
            if seats[row][column] <= max_height:
                no_visibility.append((row, column))
            else:
                max_height = seats[row][column]
    return no_visibility


print(taller_and_visibility([[1, 2, 3, 2, 1, 1], [2, 4, 4, 3, 7, 2], [5, 5, 2, 5, 6, 4], [6, 6, 7, 6, 7, 5]]))
print(taller_and_visibility([[1, 2, 3, 2, 1, 1], [2, 4, 4, 3, 7, 2], [5, 5, 2, 5, 6, 4], [6, 6, 7, 6, 7, 5, 9]]))
print(taller_and_visibility([[1, 2, 6, 2, 1, 1], [2, 4, 4, 3, 7, 2], [5, 5, 2, 5, 6, 4], [6, 6, 7, 6, 7, 5]]))


# Exercise 10
# def order_by_index(*many_lists):
#     list_of_tuples = []
#     max_len = max(len(one_list) for one_list in many_lists)
#     if len(many_lists) > 0:
#         if len(many_lists[0]) < max_len:
#             many_lists[0] += [None] * (max_len - len(many_lists[0]))
#         list_of_tuples = many_lists[0]
#     for index, each_list in enumerate(many_lists):
#         if index > 0:
#             if len(each_list) < max_len:
#                 each_list += [None] * (max_len - len(each_list))
#             list_of_tuples = list(zip(list_of_tuples, each_list))
#     return list_of_tuples

def order_by_index(*many_lists):  # varianta fara 'tuple in tuple'
    list_of_tuples = []
    max_len = max(len(one_list) for one_list in many_lists)
    for each_list in many_lists:
        if len(each_list) < max_len:
            each_list += [None] * (max_len - len(each_list))
    for index in range(0, max_len):
        index_tuple = tuple(each_list[index] for each_list in many_lists)
        list_of_tuples.append(index_tuple)
    return list_of_tuples


print(order_by_index([1, 2, 3, 'zb'], [5, 6, 7, 8.8], ["a", "b", "c"]))
print(order_by_index([], []))
print(order_by_index([1, 2, 3], [1], []))


# Exercise 11
def order_by_3rd_character_of_2nd_element(list_of_tuples):
    if len(list(filter(lambda element: len(element) < 2 or len(element[1]) < 3, list_of_tuples))) > 0:
        return "Incorrect entry data"
    return sorted(list_of_tuples, key=lambda element: element[1][2])


print(order_by_3rd_character_of_2nd_element([('abc', 'bcd'), ('abc', 'zza')]))
print(order_by_3rd_character_of_2nd_element([('abc', 'bcd'), ('abc', 'zz')]))
print(order_by_3rd_character_of_2nd_element([('abcd', 'bcdp', 'abad'), ('abc', 'liam', 'bobo'),
                                             ('abc', 'bibi', 'bobo')]))


# Exercise 12
def group_by_rhyme(list_of_words):
    visited_words = []
    result = []
    for word in list_of_words:
        if word not in visited_words:
            list_by_rhyme = list(filter(lambda element: element[-2:] == word[-2:], list_of_words))
            visited_words += list_by_rhyme
            result.append(list_by_rhyme)
    return result


print(group_by_rhyme(['ana', 'banana', 'carte', 'arme', 'parte']))
print(group_by_rhyme(['ana', 'banana', 'carte', 'ana', 'arme', 'parte']))
