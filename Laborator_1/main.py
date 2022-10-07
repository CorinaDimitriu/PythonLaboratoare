# # Exercise 1:
# def gcd(list_of_numbers): # where list_of_numbers is a string given by the user following specific rules
#     list_of_numbers = list_of_numbers.split(" ")
#     if len(list_of_numbers) == 0:
#         return "There are no arguments passed to the computing gcd function."
#     if not list_of_numbers[0].isdigit():
#         return "Argument is not of integer type."
#     _gcd = int(list_of_numbers[0])
#     for number in list_of_numbers:  # list_of_numbers[0]
#         if not number.isdigit():
#             return "Argument is not of type integer."
#         number = int(number)
#         while number:
#             remainder = _gcd % number
#             _gcd = number
#             number = remainder
#     return _gcd
#
#
# def gcd_from_keyboard_input():
#     print("Give me some numbers to calculate the GCD for (each one separated by one blank space from the others): ")
#     list_of_numbers = input()
#     return gcd(list_of_numbers)
#
#
# print(gcd_from_keyboard_input())

# # Exercise 2
# example_string = "abracadabra trick is the most interesting in your show"
# number_of_vowels = 0
# for letter in "aeiou":
#     number_of_vowels += example_string.lower().count(letter)
# print("Number of vowels in %8s: %d" % (f"{example_string!r}", number_of_vowels))
#
# # Exercise 3
# print("Give me the first string: ")
# string_first = input()
# print("Give me the second string: ")
# string_second = input()
# count = string_first.count(string_second)
# print("Number of occurrences of %8s in %8s: %d" % (f"{string_first!r}", f"{string_second!r}", count))

# # Exercise 4
# example_string = "ThisStringIsNotWrittenInUpperCamelCaseAnymore"
# converted_string = ""
# for letter in example_string:
#     if letter.isupper():
#         if example_string.index(letter) != 0:
#             converted_string += '_'
#         converted_string += letter.lower()
#     else:
#         converted_string += letter
# print(converted_string)
#
# # Exercise 4 - alternative, keeping the same string
# example_string = "ThisStringIsNotWrittenInUpperCamelCaseAnymore"
# converted_string = ""
# for letter in example_string:
#     index = example_string.index(letter)
#     if letter.isupper():
#         if index != 0:
#             example_string = example_string[:index] + '_' + letter.lower() + example_string[index + 1:]
#         else:
#             example_string = example_string[:index] + letter.lower() + example_string[index + 1:]
# print(example_string)

# Exercise 5
import sys

print("Give me the number of rows and cols for your square matrix: ")
rows_cols = input()
if not rows_cols.isdigit():
    print("Number of rows/columns is not of integer type")
else:
    rows_cols = int(rows_cols)
    letter_matrix = [['' for _ in range(rows_cols)] for _ in range(rows_cols)]
    print("Now give me the matrix: ")
    for i in range(0, rows_cols):
        for j in range(0, rows_cols):
            letter_matrix[i][j] = sys.stdin.read(1)
        sys.stdin.read(1)
    left_up_row = 0
    right_down_row = rows_cols
    while left_up_row < right_down_row:
        for j in range(left_up_row, right_down_row):
            print(letter_matrix[left_up_row][j], end='')
        for i in range(left_up_row + 1, right_down_row):
            print(letter_matrix[i][right_down_row - 1], end='')
        for j in range(right_down_row - 2, left_up_row - 1, -1):
            print(letter_matrix[right_down_row - 1][j], end='')
        for i in range(right_down_row - 2, left_up_row, -1):
            print(letter_matrix[i][left_up_row], end='')
        left_up_row = left_up_row + 1
        right_down_row = right_down_row - 1

# # Exercise 6
# def is_palindrome(number):
#     if type(number) is not int:
#         return "Argument is not of integer type"
#     inverse_number = int(str(number)[::-1])
#     if inverse_number == number:
#         return "%d is palindrome" % number
#     else:
#         return "%d is not palindrome" % number

# # Exercise 6 - alternative
# def is_palindrome(number):
#     if type(number) is not int:
#         return "Argument is not of integer type"
#     initial_number = number
#     inverse_number = 0
#     while number != 0:
#         inverse_number = number % 10 + inverse_number * 10
#         number = number // 10
#     else:
#         if inverse_number == initial_number:
#             return "%d is palindrome" % initial_number
#         else:
#             return "%d is not palindrome" % initial_number


# print(is_palindrome(154456))
# print(is_palindrome(15456))
# print(is_palindrome(1325775231))
# print(is_palindrome(132575231))
# print(is_palindrome(132575231.5))
# print(is_palindrome("132575231"))

# # Exercise 7
# def number_extraction(text):
#     all_digits = "0123456789"
#     for symbol in text:
#         if symbol in all_digits:
#             number = symbol
#             for index in range(text.index(symbol) + 1, len(text)):
#                 if text[index] in all_digits:
#                     number += text[index]
#                 else:
#                     break
#             return number
#     else:
#         return "No numbers found..."
#
#
# print(number_extraction("An apple is 123 USD"))
# print(number_extraction("An apple is 12377171829201 88192"))
# print(number_extraction("abc123abc"))
# print(number_extraction(" 11123"))
# print(number_extraction("11123far from here"))
# print(number_extraction("far from here..."))


# # Exercise 8
# def count_in_binary(number):
#     count = 0
#     while number != 0:
#         if number % 2 == 1:
#             count = count + 1
#         number //= 2
#     return count
#
#
# print(count_in_binary(24))
# print(count_in_binary(1))
# print(count_in_binary(0))
# print(count_in_binary(874832652))

# # Exercise 9
# def most_common_letter(text):
#     all_letters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
#     max_count = 0
#     max_letter = "The text contains no letters"
#     for letter in all_letters:
#         count = text.count(letter)
#         if count > max_count:
#             max_count = count
#             max_letter = letter
#     return max_letter
#
#
# print(most_common_letter("  an apple is not A tomato 99%"))


# # Exercise 10
# def count_words(text):
#     if len(text) == 0:
#         return 0
#     return len(text.strip().split(" "))
#
#
# print(count_words("I have Python exam"))
# print(count_words(""))
# print(count_words("  I have Python exam "))
