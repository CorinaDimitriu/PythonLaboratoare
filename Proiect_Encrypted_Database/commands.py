# Encryption, decryption, deletion -- preceded by connecting to database

import pyodbc
import os
import bitstring

import aes128
import messages
import reader
import rsa_oaep
import sha256


def connect_to_database() -> pyodbc.Connection:
    """
    This function facilitates connecting the application module to the database in
    order to perform insertions, retrievals and deletions.

    :return: the connection being opened
    :rtype: pyodbc.Connection
    """
    conn = pyodbc.connect(Trusted_Connection='yes',
                          Driver='{ODBC Driver 17 for SQL Server}',
                          Server=r'(localdb)\mssqllocaldb',
                          Database='EncryptedDatabase')
    return conn


def create_files_table() -> None:
    """
    This function (re)creates the FILES table in order to keep metadata
    and cryptographic information about the target files.
    """
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


def get_metadata(file_path: str) -> (str, str, int, bool, bool, int, int, str, bool):
    """
    This function gathers metadata about the file located at *file_path*.

    :param file_path: the path of the target file
    :type file_path: str
    :return: the essential metadata of the target file
    :rtype: (str, str, int, bool, bool, int, int, str, bool)
    """
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


def insert_encrypted_file(file_path: str, name: str) -> str:
    """
    This is where the upload command is being executed. The file located at *file_path*,
    along with its metadata, is inserted into the database and will be further identified under *name*.
    Multiple file formats have been treated (.txt, .docx, .pdf).

    :param file_path: the path to the target file
    :type file_path: str
    :param name: the file identifier
    :type name: str
    :return: success or error message, depending on the use-cases encountered
    :rtype: str
    """
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


def insert_all_data(name: str, file_path: str, encrypted_key: str,
                    metadata: (str, str, int, bool, bool, int, int, str, bool)) -> None:
    """
    This is where the database operations regarding the upload command are performed.

    :param name: the unique identifier wished by the user
    :type name: str
    :param file_path: the path to the target file
    :type file_path: str
    :param encrypted_key: the RSA-encrypted symmetric key used for file encryption
    :type encrypted_key: str
    :param metadata: metadata about the target file; includes:
        absolute path,
        base file name,
        size,
        if read operations are permitted,
        if write operations are permitted,
        owner id,
        group id,
        hash digest of the file,
        if the file has been deleted from disk (but the encryption is kept),
    :type metadata: (str, str, int, bool, bool, int, int, str, bool)
    """
    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO FILES(Name, Path, File_Path, Filename, Size_in_bytes, ReadPerm, WritePerm,"
                   "OwnerId, GroupId, Hash, Encrypted_Key, Method, Deleted) "
                   "VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                   name, file_path, metadata[0], metadata[1], metadata[2], metadata[3], metadata[4], metadata[5],
                   metadata[6], metadata[7], encrypted_key, "RSAES128-OAEP-SHA256", metadata[8])
    cursor.commit()
    conn.close()


def retrieve_decrypted_file(private_key: (int, int, int), name: str = '', path: str = '') -> str:
    """
    This is where the read command is being executed. The content of the target file is
    displayed to the user. The content of the file is decrypted using the asymmetric key stored
    within the database. Multiple file formats have been treated (.txt, .docx, .pdf).

    :param private_key: the private RSA key for decrypting the asymmetric key
        stored within the FILES table
    :type private_key: (int, int, int)
    :param name: the unique identifier of the target file (optional)
    :type name: str
    :param path: the path to the target file (optional)
    :type path: str
    :return: the content of the target file (as plaintext) or an error message if
        exceptions have occurred at the retrieval operation
    :rtype: str
    :raises AttributeError: if none of the 2 possible identifiers
        of the file has been specified by the user
    """
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


def retrieve_from_database(name: str, path: str) -> (str, str, int):
    """
    This is where the database operations regarding the read command are performed.

    :param name: the name of the target file
    :type name: str
    :param path: the path where the target file is located
    :type path: str
    :return: the name, path (updated if not specified from the very beginning)
        and the encrypted symmetric key which was used at file encryption
    :rtype: (str, str, int)
    :raises AttributeError: if targeted file does not exist within the database
        (and neither do its identifiers)
    """
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


def delete_file(name: str = '', path: str = '') -> str:  # if both parameters specified, only name is taken into account
    """
    This is where the delete command is being executed.

    :param name: the name of the target file
    :type name: str
    :param path: the path where the target file is located
    :type path: str
    :return: success or error message, depending on the use-cases encountered
    :rtype: str
    :raises AttributeError: if none of the 2 possible identifiers
        of the file has been specified by the user or if targeted file
        does not exist within the database (and neither do its identifiers)
    """
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


def solve_command(request_code: int, params: list[str], private_key: (int, int, int)) -> str:  # includes treating exceptions
    """
    This function implements command solving as far as user's inputs are concerned. After passing
    through a pre-processing step and acquiring the green flag for validation, the command is split into
    a request code and its actual parameters (tags for identifying parameters such as **-n** or **-p** are
    eliminated during pre-processing the input). The request code corresponds to one of the following operations:
    0 ~ upload; 1 ~ read; 2 ~ delete; 3 ~ exit.

    :param request_code: an integer (from [0-3]) identifying the requested operation
    :type request_code: int
    :param params: the actual parameters of the request, regarding the file (name and path)
    :type params: list[str]
    :param private_key: the private RSA key serving for decryption of the symmetric key
        used in AES-128
    :type private_key: (int, int, int)
    :return: the result of the operation (file content or specific messages)
    :rtype: str
    """
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
