"""
This module serves for reading texts from different file formats.
Advanced elements such as images, charts, passwords may cause unusual behaviour to the program.
"""

import os
import docx
from PyPDF2 import PdfReader


def read_data(file_path):  # output is in base16
    """
    This function aims to read the content of the specified file, taking its extension
    into consideration as a hint for its formatting type (Windows OS).

    :param file_path: the absolute/relative path to the target file
    :type file_path: str
    :return: the content of the file, taking the format into account while
        encoding to serve the purposes of the application; the content is represented
        in base16
    :rtype: str
    """
    file = open(file_path, "rb")
    if not os.path.isfile(file_path):
        raise IOError("Parameter should be file and not directory")
    ext = os.path.splitext(file_path)[1].removeprefix(".")
    content = 'Sorry, we could not encode that file for you.'
    if ext == 'txt':
        content = txt_reader(file)
    elif ext == 'docx':
        content = docx_reader(file_path)
    elif ext == 'pdf':
        content = pdf_reader(file)
    file.close()
    return content


def txt_reader(file):
    """
    Reads content of txt files.

    :param file: the file descriptor
    :type: int
    :return: the content of the file encoded in hexadecimal format
    :rtype: str
    """
    content = file.read()
    return content.hex()


def docx_reader(file_path):
    """
    Reads content of docx files.

    :param file_path: the absolute/relative path to the target file
    :type file_path: str
    :return: the content of the file encoded in hexadecimal format
        (preliminary utf-8 encoding is worth being mentioned as well)
    :rtype: str
    """
    doc = docx.Document(file_path)
    fullText = []
    for para in doc.paragraphs:
        fullText.append(para.text)
    data = '\n'.join(fullText)
    return data.encode('utf-8').hex()


def pdf_reader(file_path):
    """
    Reads content of pdf files.

    :param file_path: the absolute/relative path to the target file
    :type file_path: str
    :return: the content of the file encoded in hexadecimal format
        (preliminary utf-8 encoding is worth being mentioned as well)
    :rtype: str
    """
    reader = PdfReader(file_path)
    fullText = []
    all_pages = reader.pages
    for page in all_pages:
        fullText.append(page.extract_text())
    data = '\n'.join(fullText)
    return data.encode('utf-8').hex()


def get_format(path):
    """
    This function aims to provide other services of the application with suitable
    decoding formats depending on the file type/extension on Windows OS.

    :param path: the absolute/relative path to the target file
    :type path: str
    :return: decoding character set suitable for the file
    :rtype: str
    """
    ext = os.path.splitext(path)[1].removeprefix(".")
    if ext == 'txt':
        return 'ascii'
    elif ext in {'docx', 'pdf'}:
        return 'utf-8'
    else:
        return 'ascii'
