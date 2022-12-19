
import os
import sys
import zipfile


def split(a, n):
    """
        Divide um array 'a' em 'n' partes 'iguais'.
    """
    k, m = divmod(len(a), n)
    return list(a[i * k + min(i, m) : (i + 1) * k + min(i + 1, m)] for i in range(n))

def zip_files(list_files_path, output_name):
    """
        Zipa uma lista de arquivos 'list_files_path' com um output de 'output_name'.
    """
    with zipfile.ZipFile(f"{resource_path('Files')}/{output_name}.zip", "w") as zipF:
        for file in list_files_path:
            zipF.write(file, compress_type=zipfile.ZIP_DEFLATED)

def unzip_file(file_name):
    """Unzipa um arquivo com o path file_name"""

    with zipfile.ZipFile(f"{file_name}", 'r') as zip_ref:
        zip_ref.extractall("{}".format(file_name.replace(".zip", "")))

def resource_path(path):
    """Recupera o caminho de um recurso da aplicação."""

    try:
        base_path = sys._MEIPASS
    except:
        base_path = os.path.relpath(".")

    return os.path.join(base_path, path)
