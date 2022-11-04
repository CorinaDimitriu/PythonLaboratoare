import os
import sys
import numpy as np


# Exercitiul 1
def sort_extensions(directory):
    try:
        if not os.path.isdir(directory):
            raise FileNotFoundError('No directory exists at specified path')
        extensions = {os.path.splitext(file)[1].removeprefix(".")
                      for file in os.listdir(directory) if os.path.isfile(os.path.join(directory, file))}
        return sorted(list(extensions))
    except FileNotFoundError as exc:
        return str(exc)


print(sort_extensions("D:\\Facultate\\Anul_2\\Semestrul_1\\CDC"))
print(sort_extensions("D:\\Facultate\\Anul_2\\Semestrul_1\\CDC_not_here"))
print(sort_extensions("D:\\Facultate\\Anul_2\\Semestrul_1\\CDC\\Exemplu.txt"))


# Exercitiul 2
def insert_folder_in_file(folder, fisier):
    try:
        if not os.path.isdir(folder):
            raise FileNotFoundError("There is no directory at specified path")
        fis = open(fisier, "wt")
        if not os.path.isfile(fisier):
            raise FileNotFoundError("There is no file at specified path")
        files_starting_A = [os.path.abspath(os.path.join(folder, file)) for file in os.listdir(folder) if
                            os.path.basename(file).startswith('A')]  # if os.path.isfile(os.path.join(folder, file))
        print(*files_starting_A, sep='\n', file=fis, flush=True)
        fis.close()
    except FileNotFoundError as exc:
        print(str(exc))


insert_folder_in_file("D:\\Facultate\\Anul_2\\Semestrul_1\\CDC", "./ex2.txt")
insert_folder_in_file("D:\\Facultate\\Anul_2\\Semestrul_2\\Criptografie", "./ex2.txt")
insert_folder_in_file("D:\\Facultate\\Anul_2\\Semestrul_2\\Criptografie_not_here", "./ex2_new.txt")
insert_folder_in_file("D:\\Facultate\\Anul_2\\Semestrul_2\\Criptografie", "./ex2_new.txt")


# Exercitiul 3
def count_extensions_characters(my_path):
    try:
        if os.path.isfile(my_path):
            content = open(my_path, "rt", encoding='utf-8').read().strip()
            if len(content) < 20:
                raise ValueError("This file is too short to extract the last 20 characters")
            return content[-20:]
        elif os.path.isdir(my_path):
            file_extensions = []
            for (root, directories, files) in os.walk(my_path):
                for file_name in files:
                    file_extensions.append(os.path.splitext(os.path.join(root, file_name))[1].removeprefix("."))
            my_extensions = [(file_ext, file_extensions.count(file_ext)) for file_ext in set(file_extensions)]
            return sorted(my_extensions, key=lambda ext: ext[1], reverse=True)
        elif os.path.exists(my_path):
            raise ValueError("Unknown file type: neither directory nor file")
        else:
            raise FileNotFoundError("File not found")
    except UnicodeDecodeError as exc:
        raise Exception("File can't be converted into utf-8 encoding while reading") from exc


try:
    print(count_extensions_characters("D:\\Facultate\\Anul_2\\Semestrul_1\\CDC"))
except Exception as e:
    print("Wrong parameter -> " + str(e))
try:
    print(count_extensions_characters("D:\\Facultate\\Anul_2\\Semestrul_1\\BlaBlaBla"))
except Exception as e:
    print("Wrong parameter -> " + str(e))
try:
    print(count_extensions_characters("./ex2.txt"))
except Exception as e:
    print("Wrong parameter -> " + str(e))
try:
    print(count_extensions_characters("ex7"))
except Exception as e:
    print("Wrong parameter -> " + str(e))
try:
    print(count_extensions_characters("D:\Facultate\Anul_1\Semestrul_1\IP\Laborator_9\P3\program.bin"))
except Exception as e:
    print("Wrong parameter -> " + str(e))

# Exercitiul 4
print(sort_extensions(sys.argv[1]))


# Exercitiul 5
def list_searched_files(target, to_search):
    list_files = []
    try:
        if type(to_search) is not str:
            raise ValueError("Text to be searched has to be a string")
        if os.path.isfile(target):
            try:
                if to_search in open(target, "rt", encoding="utf-8").read():
                    list_files.append(target)
                else:
                    raise ValueError("Only one file not containing target text given as parameter")
            except ValueError:
                raise
        elif os.path.isdir(target):
            for (root, directories, files) in os.walk(target):
                for file_name in files:
                    if to_search in open(os.path.join(root, file_name), "rt", encoding="utf-8").read():
                        list_files.append(file_name)
        else:
            raise ValueError("Unknown file type: neither directory nor file")
    except (ValueError, FileNotFoundError, UnicodeDecodeError) as exc:
        print(str(exc))
    finally:
        return list_files


print(list_searched_files("D:\Facultate\Anul_2\Semestrul_2\Criptografie\Examples", "day"))
print(list_searched_files("./ex2.txt", "Alfabet"))
print(list_searched_files("./ex2.txt", 12))
print(list_searched_files("./ex2.txt", "blablabla"))


# Exercitiul 6
def list_searched_files_callback(target, to_search, error_handler):
    list_files = []
    try:
        if type(to_search) is not str:
            raise ValueError("Text to be searched has to be a string")
        if os.path.isfile(target):
            try:
                if to_search in open(target, "rt", encoding="utf-8").read():
                    list_files.append(target)
                else:
                    raise ValueError("Only one file not containing target text given as parameter")
            except ValueError:
                raise
        elif os.path.isdir(target):
            for (root, directories, files) in os.walk(target):
                for file_name in files:
                    if to_search in open(os.path.join(root, file_name), "rt", encoding="utf-8").read():
                        list_files.append(file_name)
        else:
            raise ValueError("Unknown file type: neither directory nor file")
    except Exception as exc:
        error_handler(exc)
    finally:
        return list_files


def error_handler(exception):
    if type(exception) is ValueError or UnicodeDecodeError:
        print("Wrong format files given -> ", end='')
    elif type(exception) is FileNotFoundError:
        print("Files aiming to be processed do not exist -> ", end='')
    else:
        print("Not specific exception -> ", end='')
    print(str(exception))


print(list_searched_files_callback("D:\Facultate\Anul_2\Semestrul_2\Criptografie\Examples", "day", error_handler))
print(list_searched_files_callback("./ex2.txt", "Alfabet", error_handler))
print(list_searched_files_callback("./ex2.txt", 12, error_handler))
print(list_searched_files_callback("./ex2.txt", "blablabla", error_handler))
print(list_searched_files_callback("D:\Facultate\Anul_2\Semestrul_2\Criptografie\inexistent", "day", error_handler))


# Exercitiul 7
def create_dict(path_to_file):
    characterisation = dict()
    try:
        if not os.path.isfile(path_to_file):
            raise FileNotFoundError("There is no file at specified path")
        characterisation['full_path'] = os.path.abspath(path_to_file)
        characterisation['file_size'] = os.path.getsize(path_to_file)
        characterisation['file_extension'] = os.path.splitext(path_to_file)[1].removeprefix(".")
        characterisation['can_read'] = os.access(path_to_file, os.R_OK)
        characterisation['can_write'] = os.access(path_to_file, os.W_OK)
    except FileNotFoundError as exc:
        return str(exc)
    except:
        return "Unexpected exception -> " + str(e)
    else:
        return characterisation


print(create_dict("./ex2.txt"))
print(create_dict("./ex7"))
print(create_dict("D:\Facultate\Anul_2\Semestrul_2\Criptografie\Examples"))
print(create_dict("D:\Facultate\Anul_2\Semestrul_2\Criptografie\inexistent"))


# Exercitiul 8
# def absolute_paths(dir_path):
#     try:
#         if not os.path.isdir(dir_path):
#             raise FileNotFoundError("Directory given as argument does not exist")
#         root = os.path.dirname(dir_path)
#         if root == dir_path:
#             raise FileNotFoundError("Root could not be identified")
#         return [os.path.abspath(file) for file in os.listdir(root) if os.path.isfile(os.path.join(root, file))]
#     except FileNotFoundError as exc:
#         return str(exc)


def absolute_paths(dir_path):  # recursive version
    try:
        if not os.path.isdir(dir_path):
            raise FileNotFoundError("Directory given as argument does not exist")
        root = os.path.dirname(dir_path)
        if root == dir_path:
            raise FileNotFoundError("Root could not be identified")
        return [os.path.abspath(file) for root_rec, dirs, files in os.walk(root) for file in files
                if os.path.isfile(os.path.join(root, file))]
    except FileNotFoundError as exc:
        return str(exc)


print(absolute_paths("D:\Facultate\Anul_2\Semestrul_2\Criptografie\Examples"))
print(absolute_paths("D:\\"))
