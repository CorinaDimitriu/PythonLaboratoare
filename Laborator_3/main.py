from itertools import product


# Exercitiul 1


def set_operations(a, b):
    return [set(a).union(set(b)), set(a).intersection(set(b)),
            set(a).difference(set(b)), set(b).difference(set(a))]


print(set_operations([2, 2, 4, 4, 5, 6], [4, 6, 7, 8]))
print(set_operations([2, "four", 5, 6], []))


# Exercitiul 2
def count_occurrences(text):
    if type(text) is not str:
        return "Given parameter is not a sequence of characters"
    occurrence_dict = dict()
    for character in text:
        if character not in occurrence_dict:
            occurrence_dict[character] = text.count(character)
    return occurrence_dict


print(count_occurrences("Ana has apples."))
print(count_occurrences('a'))
print(count_occurrences(87))


# Exercitiul 3
def compare_collections(a, b):
    if type(a) != type(b):
        return False
    if type(a) in {int, float, complex, str, bool, bytearray, bytes, None}:
        return compare_basic_types(a, b)
    elif type(a) in {set, frozenset}:
        return compare_sets(a, b)
    elif type(a) in {list, tuple, range}:
        return compare_lists_or_tuples(a, b)
    elif type(a) is dict:
        return compare_dictionaries(a, b)
    else:
        return "There are variables of types which are not supported by this implementation."


def compare_basic_types(a, b):
    return a == b


def compare_lists_or_tuples(a, b):  # set is a particular case of list regarding the number of occurrences
    if len(a) != len(b):
        return False
    for index in range(0, len(a)):
        if not compare_collections(a[index], b[index]):
            return False
    return True


def compare_sets(a, b):
    if len(a) != len(b):
        return False
    a = list(a)
    b = list(b)
    for index in range(0, len(a)):
        if not compare_collections(a[index], b[index]):
            return False
    return True


def compare_dictionaries(a, b):
    if len(a.keys()) != len(b.keys()):
        return False
    for key in a.keys():
        if key not in b:
            return False
        else:
            return compare_collections(a[key], b[key])


def initialise_dictionaries_comparison(a, b):
    if type(a) == type(b) and type(a) is dict:
        return compare_collections(a, b)


print(initialise_dictionaries_comparison(dict({"abc": [{2, 3, "opt"}, ["89", 5]], "aaa": 2}),
                                         dict({"abc": [1, None], "aaa": 2})))
print(initialise_dictionaries_comparison(dict({"abc": [{2, 5, 3}, ["89", 5], range(1, 6)], "aaa": 2}),
                                         dict({"abc": [{2, 3, 5}, ["89", 5], range(1, 6, 1)], "aaa": 2})))
print(initialise_dictionaries_comparison(dict({"abc": [{"aa": 2}, 5], "aaa": 2}),
                                         dict({"abc": [{"aa": 2}, 5], "aaa": 2})))


# Exercitiul 4
def build_xml_element(tag, content, **key_value_params):
    attributes = " ".join(["%s" % key + "=\\\"%s\\\"" % key_value_params[key] for key in key_value_params])
    xml_construction = "<%s " % tag + attributes + ">%s</%s>" % (content, tag)
    return xml_construction


print(build_xml_element("a", "Hello there", href=" http://python.org ", _class=" my-link ", id=" someid "))


# Exercitiul 5
def validate_dict(dictionary, validation_rules):
    if type(dictionary) != dict or type(validation_rules) != set:
        return "Dictionary required as first parameter and set required as second parameter."
    for key in dictionary.keys():
        if type(key) != str or type(dictionary[key]) != str:
            return "String pair-value elements required in dictionary given as parameter."
    for rule in validation_rules:
        if type(rule) is not tuple or len(rule) != 4 or \
                len([rule_comp for rule_comp in rule if type(rule_comp) != str]) > 0:
            return "4 string elements required in every rule given as parameter."
    if len([rule for rule in validation_rules if rule[0] in dictionary.keys()]) < len(dictionary.keys()):
        return False
    for rule in validation_rules:
        if rule[0] in dictionary.keys():
            if not check_rule(dictionary[rule[0]], rule[1], rule[2], rule[3]):
                return False
    return True


def check_rule(item, prefix, middle, suffix):
    if not (len(item) >= len(prefix) and item[:len(prefix)] == prefix):
        return False
    if not (len(item) >= len(suffix) and item[-len(suffix):] == suffix):
        return False
    if not (len(item) >= len(middle) + 2 and middle in item
            and item[:len(middle)] != middle and item[-len(middle):] != middle):
        return False
    return True


print(validate_dict({"key1": "come inside, it's too cold out", "key3": "this is not valid"},
                    {("key1", "", "inside", ""), ("key2", "start", "middle", "winter")}))
print(validate_dict({"key1": "come inside, it's too cold out", "key3": "this is not valid"},
                    {("key1", "come", "inside", "out"), ("key3", "t", " ", "d")}))
print(validate_dict({"key1": "come inside, it's too cold out", "key3": "this is not valid"},
                    {("key1", "come", "inside", "out"), ("key3", "t", "th", "vd")}))


# Exercitiul 6
def unique_or_duplicate(elements):
    a = len([element for element in set(elements) if len([elem for elem in elements if elem == element]) == 1])
    b = len([element for element in set(elements) if len([elem for elem in elements if elem == element]) > 1])
    return a, b


print(unique_or_duplicate([1, 2, 3, 4, 5, 5, 55, 4, 3, 2, 8, 2, 2, 2]))
print(unique_or_duplicate([2, 2]))


# Exercitiul 7
def create_dict(*sets):
    for given_set in sets:
        if type(given_set) != set:
            return "Not all given parameters are sets."
    combinations = [list(zip(sets, element)) for element in product(sets, repeat=len(sets))]  # combinations step
    combinations = [element for nestedlist in combinations for element in nestedlist]  # merge step
    reunion = dict(zip(["%s | %s" % (str(set_r[0]), str(set_r[1])) for set_r in combinations if set_r[0] != set_r[1]
                        and list(sets).index(set_r[0]) < list(sets).index(set_r[1])],
                       [set_r[0].union(set_r[1]) for set_r in combinations if set_r[0] != set_r[1]
                        and list(sets).index(set_r[0]) < list(sets).index(set_r[1])]))
    intersection = dict(
        zip(["%s & %s" % (str(set_r[0]), str(set_r[1])) for set_r in combinations if set_r[0] != set_r[1]
             and list(sets).index(set_r[0]) < list(sets).index(set_r[1])],
            [set_r[0].intersection(set_r[1]) for set_r in combinations if set_r[0] != set_r[1]
             and list(sets).index(set_r[0]) < list(sets).index(set_r[1])]))
    difference_01 = dict(
        zip(["%s - %s" % (str(set_r[0]), str(set_r[1])) for set_r in combinations if set_r[0] != set_r[1]
             and list(sets).index(set_r[0]) < list(sets).index(set_r[1])],
            [set_r[0].difference(set_r[1]) for set_r in combinations if set_r[0] != set_r[1]
             and list(sets).index(set_r[0]) < list(sets).index(set_r[1])]))
    difference_10 = dict(
        zip(["%s - %s" % (str(set_r[1]), str(set_r[0])) for set_r in combinations if set_r[0] != set_r[1]],
            [set_r[1].difference(set_r[0]) for set_r in combinations if set_r[0] != set_r[1]]))
    return reunion | intersection | difference_01 | difference_10


print(create_dict({1, 2}, {2, 3}))
print(create_dict({1, 2}, {2, 3}, {3, 4}))


# Exercitiul 8
def loop(mapping):
    if (type(mapping) is not dict) or ('start' not in mapping.keys()):
        return "Dictionary containing 'start' key required as parameter."
    result = []
    key = "start"
    while key in mapping.keys() and mapping[key] not in result:
        result.append(mapping[key])
        key = mapping[key]
    return result


print(loop({'start': 'a', 'b': 'a', 'a': '6', '6': 'z', 'x': '2', 'z': '2', '2': '2', 'y': 'start'}))
print(loop({'start': 'start'}))


# Exercitiul 9
def count_positional_in_keywords(*positional, **keywords):
    return len([positional_elem for positional_elem in positional
                if len(set(keywords[position] for position in keywords if keywords[position] == positional_elem)) > 0])


print(count_positional_in_keywords(1, 2, 3, 4, x=1, y=2, z=3, w=5))
