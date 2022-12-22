# Encryption, decryption, deletion -- preceded by connecting to database

import pyodbc
import os
import bitstring

import aes128
import messages
import reader
import rsa_oaep
import sha256


def connect_to_database():
    conn = pyodbc.connect(Trusted_Connection='yes',
                          Driver='{ODBC Driver 17 for SQL Server}',
                          Server=r'(localdb)\mssqllocaldb',
                          Database='EncryptedDatabase')
    return conn


def create_files_table():
    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS FILES")
    cursor.execute("CREATE TABLE FILES"
                   "(Id int IDENTITY(1,1) PRIMARY KEY,"
                   " Name VARCHAR(20) unique not null,"
                   " Path VARCHAR(100) unique not null,"
                   " File_Path VARCHAR(200),"
                   " Filename VARCHAR(100),"
                   " Size_in_bytes BIGINT,"
                   " ReadPerm BIT,"
                   " WritePerm BIT,"
                   " OwnerId int,"
                   " GroupId int,"
                   " Hash VARCHAR(70),"
                   " Encrypted_Key VARCHAR(270),"
                   " Method VARCHAR(20),"
                   " Deleted BIT)")
    cursor.commit()
    conn.close()


def get_metadata(file_path):
    can_read = os.access(file_path, os.R_OK)
    can_write = os.access(file_path, os.W_OK)
    size = os.path.getsize(file_path)
    full_path = os.path.abspath(file_path)
    filename = os.path.basename(file_path)
    additional_info = os.stat(file_path, follow_symlinks=False)
    owner = additional_info.st_uid
    group = additional_info.st_gid
    file = open(file_path, "rb")
    content = file.read()
    content = bitstring.BitArray(content).bin[2:]
    hash_digest = sha256.execute_sha256(content)
    hash_digest = str(hex(int(hash_digest, 2)))[2:]
    deleted = False
    file.close()
    return full_path, filename, size, can_read, \
           can_write, owner, group, hash_digest, deleted


def insert_encrypted_file(file_path, name):
    metadata = get_metadata(file_path)
    content = reader.read_data(file_path)
    key, counter, ciphertext = aes128.encrypt_aes128(content)
    full_name = r"D:\Facultate\Anul_3\Python\Proiect_Encrypted_Database\EncryptedDatabase\\" \
                + name + ".txt"
    key = int(key, 16)
    encrypted_key = hex(rsa_oaep.encrypt_rsa_oaep(key))[2:]
    insert_all_data(name, file_path, encrypted_key, metadata)
    file_db = open(full_name, "wt")
    file_db.write(counter + ciphertext)
    file_db.close()
    return messages.Success


def insert_all_data(name, file_path, encrypted_key, metadata):
    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO FILES(Name, Path, File_Path, Filename, Size_in_bytes, ReadPerm, WritePerm,"
                   "OwnerId, GroupId, Hash, Encrypted_Key, Method, Deleted) "
                   "VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                   name, file_path, metadata[0], metadata[1], metadata[2], metadata[3], metadata[4], metadata[5],
                   metadata[6], metadata[7], encrypted_key, "RSAES128-OAEP-SHA256", metadata[8])
    cursor.commit()
    conn.close()


def retrieve_decrypted_file(private_key, name='', path=''):
    if name == '' and path == '':
        raise AttributeError(messages.ParameterSpecification +
                             "At least one in {name, path} should contain valid value")
    name, path, encrypted_key = retrieve_from_database(name, path)
    decrypted_key = hex(rsa_oaep.decrypt_rsa_oaep(encrypted_key, private_key, 128))[2:]
    crypto_path = r"D:\Facultate\Anul_3\Python\Proiect_Encrypted_Database\EncryptedDatabase\\" \
                  + name + ".txt"
    file_db = open(crypto_path, "rt")
    content = file_db.read()
    file_db.close()
    counter = content[:32]
    ciphertext = content[32:]
    hexadecimal = aes128.decrypt_aes128(counter, ciphertext, decrypted_key)
    return bytes.fromhex(hexadecimal).decode(reader.get_format(path))


def retrieve_from_database(name, path):
    conn = connect_to_database()
    cursor = conn.cursor()
    if name == '':
        cursor.execute("SELECT Name FROM FILES WHERE Path=?", path)
        result = cursor.fetchone()
        if result is None:
            raise AttributeError(messages.NotExistingAnymore)
        name = result[0]
    cursor.execute("SELECT Encrypted_Key, Path FROM FILES WHERE Name=?", name)
    result = cursor.fetchone()
    if result is None:
        raise AttributeError(messages.NotExistingAnymore)
    encrypted_key = int(result[0], 16)
    path = result[1]
    if not os.path.exists(path):
        cursor.execute("UPDATE FILES SET Deleted=? WHERE Name=?", True, name)
    cursor.commit()
    conn.close()
    return name, path, encrypted_key


def delete_file(name='', path=''):  # if both parameters specified, only name is taken into account
    if name == '' and path == '':
        raise AttributeError(messages.ParameterSpecification +
                             "At least one in {name, path} should contain valid value")
    conn = connect_to_database()
    cursor = conn.cursor()
    if name == '':
        cursor.execute("SELECT Name FROM FILES WHERE Path=?", path)
        result = cursor.fetchone()
        if result is None:
            raise AttributeError(messages.NotExistingAnymore)
        name = result[0]
    cursor.execute("SELECT Name FROM FILES WHERE Name=?", name)
    result = cursor.fetchone()
    if result is None:
        raise AttributeError(messages.NotExistingAnymore)
    cursor.execute("DELETE FROM FILES WHERE Name=?", name)
    cursor.commit()
    conn.close()
    os.remove(r"D:\Facultate\Anul_3\Python\Proiect_Encrypted_Database\EncryptedDatabase\\" \
              + name + ".txt")
    return messages.Success


def solve_command(request_code, params, private_key):  # includes treating exceptions
    try:
        if request_code == 0:  # code for insertion
            return insert_encrypted_file(params[0], params[1])
        elif request_code == 1:  # code for retrieval
            return retrieve_decrypted_file(private_key, params[0], params[1])
        else:  # code for deletion
            return delete_file(params[0], params[1])
    except (FileNotFoundError, PermissionError) as exc:
        return messages.FileNotFound + str(exc)
    except (UnicodeDecodeError, UnicodeEncodeError) as exc:
        return messages.FileFormat + str(exc)
    except IOError as exc:
        return messages.IOInvalid + str(exc)
    except AttributeError as exc:
        return str(exc)
    except pyodbc.DatabaseError as exc:
        return messages.DatabaseManipulation + str(exc)
    except (ValueError, TypeError, ArithmeticError) as exc:
        return messages.CryptographicError + str(exc)
    except Exception as exc:
        return messages.Unknown + str(exc)
