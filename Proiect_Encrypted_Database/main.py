# This is considered the application interface with the user
from commands import solve_command, create_files_table
import rsa_oaep
from command_parser import parse


def create_workspace():
    create_files_table()


def display_menu():
    menu = " \u001b[36m \n********************\nInsert into database: upload <path> <name>\n" \
           "Retrieve from database: read <[-n name] [-p path]>\n" \
           "Delete from database: delete <[-n name] [-p path]>\n" \
           "Exit: exit\n********************\n"
    print(menu)
    print("\u001b[33m Give me the command you wish to execute: ")


def crypto(private_key):
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
            print("\u001b[35m" + solve_command(request, params, private_key))


def extract_keys():
    # create_keys()
    private_file = open("./Keys/PrivateKey.txt", "rt")
    private_key = []
    for line in private_file.readlines():
        private_key.append(int(line.strip(), 16))
    private_file.close()
    public_file = open("./Keys/PublicKey.txt", "rt")
    public_key = []
    for line in public_file.readlines():
        public_key.append(int(line.strip(), 16))
    public_file.close()
    rsa_oaep.public_key = tuple(public_key)
    return tuple(private_key)


def create_keys():
    public_key, private_key = rsa_oaep.compute_parameters()
    private_file = open("./Keys/PrivateKey.txt", "wt")
    private_file.write(hex(private_key[0])[2:] + '\n' +
                       hex(private_key[1])[2:] + '\n' + hex(private_key[2])[2:] + '\n')
    private_file.close()
    public_file = open("./Keys/PublicKey.txt", "wt")
    public_file.write(hex(public_key[0])[2:] + '\n' + hex(public_key[1])[2:] + '\n')
    public_file.close()


if __name__ == "__main__":
    secret_key = extract_keys()
    # create_workspace()
    crypto(secret_key)
