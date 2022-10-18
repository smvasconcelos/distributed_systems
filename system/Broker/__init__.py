"""Configuração do broker"""
import json
import os
import socket
import tkinter as tk
import zipfile
from datetime import datetime
from pathlib import Path

from dotenv import find_dotenv, load_dotenv
from system.Broker.Recieve import Recieve
from system.Broker.Send import Send

load_dotenv(find_dotenv())

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
    with zipfile.ZipFile(f"Files/{output_name}.zip", "w") as zipF:
        for file in list_files_path:
            zipF.write(file, compress_type=zipfile.ZIP_DEFLATED)

class Broker:
    """
    Oferece suporte ao gerenciamento de conexões cliente-servidor e integração com a GUI.

    Attributes:
            host (str): Endereço IP do socket de escuta do servidor.
            port (int): Número da porta do socket de escuta do servidor.
            sock (socket.socket): Objeto socket conectado.
            name (str): Nome de usuário do cliente.
            messages (tk.Listbox): Objeto tk.Listbox que contém todas as mensagens exibidas na GUI.
    """

    def __init__(self, hosts):
        self.hosts = hosts
        self.name = None
        self.messages = None
        self.max_conn = int(os.getenv('MAX_CONN'))
        self.values = [x for x in range(int(os.getenv('START_VAL')),  int(os.getenv('END_VAL')) + 1)]
        self.count = 0
        self.total = 0
        self.connections = []
        self.recieves = []
        self.routines = []

    def sum_result(self, result):
        self.total += result
        self.count += 1
        print(f"Somando total ... {self.total}")
        if self.count == self.max_conn:
            Path(f"Result").mkdir(parents=True, exist_ok=True)
            with open("Result/result.txt", "w+") as f:
                print("Gravando resultado em Result/result.txt ...")
                f.write(str(self.total))

    def start(self):
        """
        Estabelece a conexão cliente-servidor. Reúne a entrada do usuário para o nome de usuário,
        cria e inicia as threads de envio e recebimento e notifica outros clientes conectados.

        Returns:
                Um objeto Receive que representa o segmento de recebimento.
        """
        for conn in self.hosts["connections"]:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.connections.append(sock)
            sock.connect((conn['host'], int(conn['port'])))
            recieve = Recieve(sock, self)
            recieve.start()
            self.recieves.append(recieve)

        self.prepare_routine()

    def prepare_routine(self):
        """
        Prepara Os dados para executar a rotina

        Divide o array de valores pela quantidade de conexões e gera os arquivos de input para cada uma delas
        """

        print("Preparando rotina ...")
        self.values = split(self.values, len(self.connections))
        Path(f"Files").mkdir(parents=True, exist_ok=True)
        for conn_id in range(0, self.max_conn):
            with open(f"Files/input_{conn_id}.txt", "w+") as f:
                f.write(json.dumps(self.values[conn_id]))
            zip_files(
                [f"Files/input_{conn_id}.txt", "Files/program.py"], f"file_{conn_id}"
            )
            print(f"Zipped [input_{conn_id}.txt, program.py] => file_{conn_id}.zip ...")
        self.start_routine()

    def start_routine(self):
        """
            Organiza todos os arquivos relacionado a uma rotina e envia para ser executada pelo cliente
        """
        print("Iniciando rotina ...")
        self.routine = True
        for id, connection in enumerate(self.connections):
            print(f"Iniciando rontina {id} ...")
            process = Send(id, connection)
            self.routines.append(process)
            process.start()

        # Espera mandar os arquivos pra todas as conexões
        print("Rotinas em execução...")
        for process in self.routines:
            process.join()

        print("Rotinas Finalizadas...")
        print("Aguardando retorno ...")
