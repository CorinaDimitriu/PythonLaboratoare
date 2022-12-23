"""
This module is considered the application interface with the user.
"""

from commands import solve_command, create_files_table
import rsa_oaep
from command_parser import parse


def create_workspace() -> None:
    """
    This function (re)creates the application's table inside database.
    Using this function is recommended when targeting to clean the table's records
    and (re)create the FILES as an empty table.
    """
    create_files_table()


def display_menu() -> None:
    """
    This function displays the possible commands a user can issue and their corresponding formatting rules.
    The commands' menu is printed on screen every time the user has to input a new command. This way all the rules
    he has to follow are displayed right in front of him at the time he needs to compose his command.
    """
    menu = " \u001b[36m \n********************\nInsert into database: upload <path> <name>\n" \
           "Retrieve from database: read <[-n name] [-p path]>\n" \
           "Delete from database: delete <[-n name] [-p path]>\n" \
           "Exit: exit\n********************\n"
    print(menu)
    print("\u001b[33m Give me the command you wish to execute: ")


def crypto(private_key: int) -> str:
    """
    This function captures the interaction between the user and the application.
    This might be considered the top layer which encapsulates accessing the database, parsing the user's
    commands and responding to them and all the cryptographic operations performed in the layers below.

    :param private_key: the private (fixed) key derived from computing rsa parameters; keys can be changed
        from this module as well, so their 'time to leave' is decided by the user
    :type private_key: (int, int, int)
    """
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


def extract_keys() -> (int, int, int):
    """
    This function aims to extract the RSA keys from the local files where they are stored.
    The keys are stored in hexadecimal format. When extracted, they are also converted to big integers.
    If the user decides so, keys can be (re)generated, which causes the corresponding files to be overwritten.

    :return: the RSA private key
    :rtype: (int, int, int)
    """
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


def create_keys() -> None:
    """
    This function replaces the old RSA keys with new ones, for security or maintenance reasons.
    This function must be run when starting the application for the first time (no RSA parameters have been created
    before in this case) or if any external changes have occurred to the files which store them (the files
    being located in the Keys directory).
    """
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
