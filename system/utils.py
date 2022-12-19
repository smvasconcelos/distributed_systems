import os
import sys
import zipfile

def exit(server):
	"""
	Permite que o administrador do servidor desligue o servidor.
	Digitar 'q' na linha de comando fechará todas as conexões ativas e sairá do aplicativo.

	Attributes:
		server (Server): Servidor que será desligado.
	"""
	while True:
		ipt = input('')
		if (ipt == 'q'):
			print('Fechando todas as conexoes...')
			for connection in server.connections:
				connection.sc.close()
			print('Desligando o servidor ...')
			os._exit(0)


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
    with zipfile.ZipFile(f"{output_name}.zip", "w") as zipF:
        for file in list_files_path:
            zipF.write(file, compress_type=zipfile.ZIP_DEFLATED)

def unzip_file(file_name):
    """Unzipa um arquivo com o path file_name"""

    with zipfile.ZipFile(f"RecievedFiles/{file_name}", 'r') as zip_ref:
        zip_ref.extractall("RecievedFiles/{}".format(file_name.replace(".zip", "")))
