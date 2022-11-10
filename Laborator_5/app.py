from utils import process_item


# if __name__ == "__main__":
#     while True:
#         number = input("Give me a number: ")
#         while not number.isdigit():
#             if number == 'q':
#                 break
#             number = input("Give me a number: ")
#         if number == 'q':
#             break
#         print("The least prime greater than %s is %d" % (number, process_item(int(number))))


while True:
    number = input("Give me a number: ")
    while not number.isdigit():
        if number == 'q':
            break
        number = input("Give me a number: ")
    if number == 'q':
        break
    print("The least prime greater than %s is %d" % (number, process_item(int(number))))
