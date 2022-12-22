# This is considered the application interface
from commands import solve_command
import rsa_oaep
from command_parser import parse


def display_menu():
    menu = "\u001b[37m \n********************\nInsert into database: upload <path> <name>\n" \
           "Retrieve from database: read <[-n name] [-p path]> <key>\n" \
           "Delete from database: delete <[-n name] [-p path]>\n" \
           "Exit: exit\n********************\n"
    print(menu)
    print("\u001b[33m Give me the command you wish to execute: ")


def crypto():
    private_key = rsa_oaep.compute_parameters()[1]
    command = ''
    while command.lower() != 'exit':
        display_menu()
        command = input()
        ok, request, params = parse(command)
        if not ok:
            print("\u001b[33m Wrong command! Please use one of "
                  "the available commands/formats listed up here.")
            continue
        if request == 3:  # code for exit
            break
        else:
            print(solve_command(request, params, private_key))


if __name__ == "__main__":
    crypto()
