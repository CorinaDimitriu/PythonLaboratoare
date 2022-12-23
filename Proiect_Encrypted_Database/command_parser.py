"""
This module validates commands and separates them into request and request parameters
starting from the user keyboard input.
"""


def parse(command: str) -> (bool, int, list[str]):
    """
    It is designed to classify commands by assigning a request code and extract the necessary parameters from
    them. Some pre-established syntax rules are checked during the execution of this function, such as the number
    of parameters issued by the user and the existence of the mandatory ones within them.

    :param command: the command issued by the user
    :type command: str
    :return: a tuple made up of 3 elements, from which the first one indicates the success/failure
        of the parsing operation which was attempted, the second one represents the request code and the third one is
        a list of the actual parameters of the request. The request code has 4 possible values, which correspond
        to the 4 basic operations which the user can execute: upload, read, delete file and exit.
    :rtype: (bool, int, list[str])
    """
    error_combo = (False, -1, [])
    command = command.strip()
    components = command.split()
    if components[0] not in {'upload', 'read', 'delete', 'exit'}:
        return error_combo
    params = components[1:]
    request_code = ['upload', 'read', 'delete', 'exit'].index(components[0])
    validation = validate_command(request_code, params)
    if not validation[0]:
        return error_combo
    return True, request_code, validation[1]


def validate_command(request_code: int, params: list[str]) -> (bool, list[str]):
    """
    Splits validation into particular cases depending on the command type/request code the user issued.
    Significance of codes: 0 ~ upload; 1 ~ read; 2 ~ delete; 3 ~ exit.

    :param request_code: the request code deduced according to the above signification
    :type request_code: int
    :param params: the raw parameter string issued by the user; includes specifications such as
        ``-n`` or ``-p`` which are meant to be eliminated after parsing
    :type params: list[str]
    :return: the validation tuple made up of the OK code and the actual parameters' list
    :rtype: (bool, list[str])
    """
    if request_code == 0:
        return upload_validate(params)
    elif request_code in {1, 2}:
        return delete_retrieve_validate(params)
    else:
        return exit_validate(params)


def upload_validate(params: list[str]) -> (bool, list[str]):
    """
    Validates the upload parameters issued by user in the second part of his query.

    :param params: the raw parameter string issued by the user
    :type params: list[str]
    :return: the validation tuple made up of the OK code and the actual parameters' list
    :rtype: (bool, list[str])
    """
    if len(params) == 2:
        return True, params
    else:
        return False, []


def delete_retrieve_validate(params: list[str]) -> (bool, list[str]):
    """
    Validates the read/delete parameters issued by user in the second part of his query.
    At least one of name and path must be specified.
    The user can specify both but in this case only name will be taken into account.

    :param params: the raw parameter string issued by the user
    :type params: list[str]
    :return: the validation tuple made up of the OK code and the actual parameters' list
    :rtype: (bool, list[str])
    """
    if len(params) == 4:
        if params[0] == '-n' and params[2] == '-p':
            real_params = [params[1], params[3]]
            return True, real_params
        elif params[0] == '-p' and params[0] == '-n':
            real_params = [params[3], params[1]]
            return True, real_params
    if len(params) == 2:
        if params[0] == '-n':
            real_params = [params[1], '']
            return True, real_params
        elif params[0] == '-p':
            real_params = ['', params[1]]
            return True, real_params
    return False, []


def exit_validate(params: list[str]) -> (bool, list[str]):
    """
    Validates the exit command which should consist of a single word and no parameters.

    :param params: the raw parameter string issued by the user
    :type params: list[str]
    :return: the validation tuple made up of the OK code and the actual parameters' list
    :rtype: (bool, list[str])
    """
    if len(params) == 0:
        return True, []
    else:
        return False, []
