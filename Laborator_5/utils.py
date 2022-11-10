import math


def process_item(x):
    y = x + 1
    while not isPrime(y):
        y = y + 1
    return y


def isPrime(y):
    return y != 0 and y != 1 and \
           len([d for d in range(2, int(math.sqrt(y) + 1)) if y % d == 0]) == 0


# if __name__ == "__main__":
#     number = input("Give me a number: ")
#     while not number.isdigit():
#         number = input("Give me a number: ")
#     print(process_item(int(number)))


number = input("Give me a number: ")
while not number.isdigit():
    number = input("Give me a number: ")
print(process_item(int(number)))
