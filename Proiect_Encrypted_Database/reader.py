# This module serves for reading texts.
# Advanced elements such as images, charts, passwords may cause unusual behaviour to the program.

import os
import docx
from PyPDF2 import PdfReader


def read_data(file_path):  # output is in base16
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
    content = file.read()
    return content.hex()


def docx_reader(file_path):
    doc = docx.Document(file_path)
    fullText = []
    for para in doc.paragraphs:
        fullText.append(para.text)
    data = '\n'.join(fullText)
    return data.encode('utf-8').hex()


def pdf_reader(file_path):
    reader = PdfReader(file_path)
    fullText = []
    all_pages = reader.pages
    for page in all_pages:
        fullText.append(page.extract_text())
    data = '\n'.join(fullText)
    return data.encode('utf-8').hex()


def get_format(path):
    ext = os.path.splitext(path)[1].removeprefix(".")
    if ext == 'txt':
        return 'ascii'
    elif ext in {'docx', 'pdf'}:
        return 'utf-8'
    else:
        return 'ascii'
