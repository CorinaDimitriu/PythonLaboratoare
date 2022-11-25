import os
import re
from itertools import permutations


# Exercitiul 1
def extract_words(text):
    if type(text) is not str:
        raise ValueError("Parameter should be text given as string value")
    # return re.split(r"\W+", text)
    return list(filter(None, re.split(r"\W+", text)))


try:
    print(extract_words("This Python Course, I had it yesterday, makes sense..."))
    print(extract_words("T"))
    print(extract_words(""))
    print(extract_words(",,,abc??'lala"))
except ValueError as exc:
    print(exc)


# Exercitiul 2
def check_match(pattern, sequence, x):
    if type(pattern) != str or type(sequence) != str or type(x) != int:
        raise ValueError("Wrong parameter types")
    return [sequence[i:i + x] for i in range(len(sequence) - x + 1)
            if re.match(pattern + r"$", sequence[i:i + x])]


try:
    print(check_match("07[0-9]{8}", "0740123456", 10))
    print(check_match("0*", "0000000000", 8))
except ValueError as exc:
    print(exc)


# # Exercitiul 3 - text version
# def match_regex(text, regex_list):
#     if type(text) != str or type(regex_list) != list \
#             or len([expr for expr in regex_list if type(expr) != str]) > 0:
#         return ValueError("Wrong parameter types")
#     if len(regex_list) == 0:
#         return ValueError("No regular expression given for filtering")
#     return [text[i:j] for i in range(len(text)) for j in range(i + 1, len(text) + 1)
#             if any([re.match(expr + r"$", text[i:j]) for expr in regex_list])]
#     # expr_combined = "|".join("(" + expr + "$)" for expr in regex_list)
#     # return [text[i:j] for i in range(len(text)) for j in range(i + 1, len(text) + 1)
#     #         if re.match(expr_combined, text[i:j])]


# Exercitiul 3 - list of strings version
def match_regex(list_of_strings, regex_list):
    if type(list_of_strings) != list or type(regex_list) != list or \
            len([expr for expr in regex_list if type(expr) != str]) > 0 or \
            len([string for string in list_of_strings if type(string) != str]) > 0:
        return ValueError("Wrong parameter types")
    if len(regex_list) == 0:
        return ValueError("No regular expression given for filtering")
    return [string for string in list_of_strings
            if any([re.match(expr + r"$", string) for expr in regex_list])]


try:
    # print(match_regex("0740123456", [r"07.", r"0."]))
    print(match_regex(["078", "044", "02"], [r"07.", r"0."]))
except ValueError as exc:
    print(exc)


# Exercitiul 4
def contained_by_xml(path_to_xml, attrs):
    content = open(path_to_xml, 'r', encoding='utf-8').read()
    if type(attrs) is not dict:
        raise ValueError("Wrong parameter type")
    regex = r"<([a-z]|[A-Z]|_)([a-z]|[A-Z]|_|[0-9]|\.|-)+\s+("
    perm = permutations(attrs)
    for combo in list(perm):
        regex_variant = "("
        for key in combo:
            regex_variant += "(" + str(key) + "=\"" + str(attrs[key] + "\"")
            regex_variant += r")\s+"
        regex += regex_variant[:-1] + r"*)|"
    regex = regex[:-1] + r")(>|(\/>))"
    occurrences = []
    while re.search(regex, content):
        occurrence = re.search(regex, content).group()
        occurrences.append(occurrence.split(" ")[0][1:])
        content = content[content.find(occurrence) + len(occurrence):]
    return occurrences


try:
    print(contained_by_xml("./test.xml", dict({"class": "url", "name": "url-form", "data-id": "item"})))
except (FileNotFoundError, ValueError) as err:
    print(err)


# # Exercitiul 4 - other attributes included version
# def contained_by_xml(path_to_xml, attrs):
#     content = open(path_to_xml, 'r', encoding='utf-8').read()
#     if type(attrs) is not dict:
#         raise ValueError("Wrong parameter type")
#     regex = r"<([a-z]|[A-Z]|_)([a-z]|[A-Z]|_|[0-9]|\.|-)+\s+("
#     perm = permutations(attrs)
#     for combo in list(perm):
#         regex_variant = "("
#         for key in combo:
#             regex_variant += "(" + r"(([a-z]|[A-Z]|_)(\w|\.|-)+=\".*\"\s+)*" + \
#                              str(key) + "=\"" + str(attrs[key] + "\"")
#             regex_variant += r")\s+"
#         regex += regex_variant[:-3] + r"(([a-z]|[A-Z]|_)(\w|\.|-)+=\".*\"\s+)*" + r"\s*)|"
#     regex = regex[:-1] + r")(>|(\/>))"
#     occurrences = []
#     while re.search(regex, content):
#         occurrence = re.search(regex, content).group()
#         occurrences.append(occurrence.split(" ")[0][1:])
#         content = content[content.find(occurrence) + len(occurrence):]
#     return occurrences
#
#
# try:
#     print(contained_by_xml("./test.xml", dict({"class": "url", "name": "url-form", "data-id": "item"})))
# except (FileNotFoundError, ValueError) as err:
#     print(err)


# Exercitiul 5
def contained_single_by_xml(path_to_xml, attrs):
    content = open(path_to_xml, 'r', encoding='utf-8').read()
    if type(attrs) is not dict:
        raise ValueError("Wrong parameter type")
    regex = r"<([a-z]|[A-Z]|_)(\w|\.|-)+\s+(([a-z]|[A-Z]|_)(\w|\.|-)+=\".*\"\s+)*("
    for key in attrs.keys():
        regex += "(" + str(key) + "=\"" + str(attrs[key] + "\"")
        regex += r")|"
    regex = regex[:-1] + r")(([a-z]|[A-Z]|_)(\w|\.|-)+=\".*\"\s+)*(>|(\/>))"
    occurrences = []
    while re.search(regex, content):
        occurrence = re.search(regex, content).group()
        occurrences.append(occurrence.split(" ")[0][1:])
        content = content[content.find(occurrence) + len(occurrence):]
    return occurrences


try:
    print(contained_single_by_xml("./test.xml", dict({"class": "url", "name": "url-form", "data-id": "item"})))
except (FileNotFoundError, ValueError) as err:
    print(err)


# Exercitiul 6
def censor_words(text):
    if type(text) != str:
        raise ValueError("Parameter should be of string type")
    text_split = re.split(r"(\W)", text)
    new_text = ""
    for word in text_split:
        if re.match(r"([aeiou]$|[aeiou]\w*[aeiou]$)", word.lower()):
            word = list(word)
            for index, letter in enumerate(word):
                if index % 2 == 0:
                    word[index] = '*'
        new_text += "".join(word)
    return new_text


try:
    print(censor_words("aaajajsksliiou"))
    print(censor_words("I iike ,,, . . Python pr /// ogramme"))
    print(censor_words("aaajajsksl"))
    print(censor_words("wwajajsksl"))
    print(censor_words("wwajajskslo"))
    print(censor_words(""))
except ValueError as err:
    print(err)


# Exercitiul 7
def validate_CNP(cnp):
    regex = r"^[1-8]((\d{2}(((0[1-9]|1[0-2])(0[1-9]|1[0-9]|2[0-8]))|((0[13578]|1[02])(29|30|31))|((0[469]|11)(29|30))))|(([13579][26]|[02468][048])0229))(0[1-9]|[1-3][0-9]|4[0-6]|5[1-2])\d{4}$"
    if re.match(regex, cnp):
        return "Valid"
    else:
        return "Invalid"


print(validate_CNP("6011213226700"))
print(validate_CNP("60112132267000"))
print(validate_CNP("6200229226700"))
print(validate_CNP("6210229226700"))
print(validate_CNP("6201231226700"))
print(validate_CNP("6201131226700"))


# Exercitiul 8
def scroll_directory(regex, path):
    if type(regex) is not str or type(path) is not str:
        raise ValueError("Wrong parameter types")
    for (root, directories, files) in os.walk(path):
        for fileName in files:
            if re.match(regex, fileName):
                print(">>" + fileName)
            elif re.search(regex, fileName):
                print(fileName)


try:
    scroll_directory(r"^C.*", "D:\\Facultate\\Anul_2\\Semestrul_1\\CDC")
    scroll_directory(r"C.*", "D:\\Facultate\\Anul_2\\Semestrul_1\\CDC")
except ValueError as err:
    print(err)
except FileNotFoundError as err:
    print("File given as parameter not found on this pc")
