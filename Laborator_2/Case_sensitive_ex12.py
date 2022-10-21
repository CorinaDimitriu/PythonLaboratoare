# Exercise 12
def group_by_rhyme(list_of_words):
    visited_words = []
    result = []
    for word in list_of_words:
        if word.lower() not in visited_words:
            list_by_rhyme = list(filter(lambda element: element[-2:].lower() == word[-2:].lower(), list_of_words))
            visited_words += [word.lower() for word in list_by_rhyme]
            result.append(list_by_rhyme)
    return result


print(group_by_rhyme(['ana', 'banana', 'carte', 'arme', 'parte', "IguANa"]))
print(group_by_rhyme(['ana', 'banana', 'carte', 'ana', 'arme', 'parte']))