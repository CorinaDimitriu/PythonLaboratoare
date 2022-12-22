# This module validates and separates commands into request and request parameters

def parse(command):
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


def validate_command(request_code, params):
    if request_code == 0:
        return upload_validate(params)
    elif request_code == 1:
        return retrieve_validate(params)
    elif request_code == 2:
        return delete_validate(params)
    else:
        return exit_validate(params)


def upload_validate(params):
    if len(params) == 2:
        return True, params
    else:
        return False, []


def retrieve_validate(params):
    if len(params) == 5:
        if params[0] == '-n' and params[2] == '-p':
            real_params = [params[1], params[3], params[4]]
            return True, real_params
        elif params[0] == '-p' and params[0] == '-n':
            real_params = [params[3], params[1], params[4]]
            return True, real_params
    if len(params) == 3:
        if params[0] == '-n':
            real_params = [params[1], '', params[2]]
            return True, real_params
        elif params[0] == '-p':
            real_params = ['', params[1], params[2]]
            return True, real_params
    return False, []


def delete_validate(params):
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


def exit_validate(params):
    if len(params) == 0:
        return True, []
    else:
        return False, []
