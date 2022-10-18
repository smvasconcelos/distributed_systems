"""Configuração do servidor"""
import json
import os
import pickle
import socket
import threading
import zipfile
from gettext import find
from pathlib import Path

from dotenv import find_dotenv, load_dotenv
from system.Server import *
from system.Server.Routine import Routine
from system.Server.ServerSocket import ServerSocket

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


class Server(threading.Thread):
    """
    Suporta gerenciamento de conexões de servidor.

    Attributes:
            connections (list): Lista de objetos ServerSocket que representam as conexões ativas.
            host (str): Endereço IP do socket de escuta.
            port (int): Número da porta do socket de escuta.
            routine (bool) : Indica se uma rotina está em execução
            routines (Array<Threading.Thread>): Array com threads de cada rotina
            max_conn (int): Define quantas conexões são necessárias para iniciar a rotina
            values (Array<int>): Define os valroes a serem somados pelas rotinas
            data (str) : Utilizado para concatenar respostas que são longas
            count (int) : Conta quantas rotinas terminaram até agora
            total (int) : Armazena o total da soma de cada rotina
    """

    def __init__(self, host, port):
        super().__init__()
        # list of server sockets objects representing active client connections
        self.connections = []
        self.host = host
        self.port = port
        self.routine = False
        self.routines = []
        self.max_conn = int(os.getenv('MAX_CONN'))
        self.values = [x for x in range(int(os.getenv('START_VAL')),  int(os.getenv('END_VAL')) + 1)]
        self.data = b""
        self.count = 0
        self.total = 0

    def sum_result(self, result):
        self.total += result
        self.count += 1
        print(f"Somando total ... {self.total}")
        if self.count == self.max_conn:
            Path(f"Result").mkdir(parents=True, exist_ok=True)
            with open("Result/result.txt", "w+") as f:
                print("Gravando resultado em Result/result.txt ...")
                f.write(str(self.total))

    def run(self):
        """
        Cria o socket de escuta. O socket de escuta usará a opção SO_REUSEADDR para
        permitir a ligação a um endereço de socket usado anteriormente. Este é um aplicativo de pequena escala que
        suporta apenas uma conexão em espera por vez.
        Para cada nova conexão, um thread ServerSocket é iniciado para facilitar a comunicação com
        aquele cliente específico. Todos os objetos ServerSocket são armazenados no atributo connections.
        """
        # AF_INET: address family, for IP networking
        # SOCK_STREAM: socket type, for reliable flow-controlled data stream
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((self.host, self.port))

        sock.listen(1)
        print(f"Ouvindo em {sock.getsockname()}")

        # listen for new client connections
        while True:
            # new connection
            if len(self.connections) < self.max_conn:
                sc, sockname = sock.accept()
                print(f"Nova conexao de {sc.getpeername()} para {sc.getsockname()}")

                # new thread
                server_socket = ServerSocket(sc, sockname)
                # start thread
                server_socket.start()

                # add thread to active connections
                self.connections.append(server_socket)
                # print(f"Pronto para receber mensagens de {sc.getpeername()}")
                # ! Forma antiga
                # ! if len(self.connections) == self.max_conn:
                # !     self.prepare_routine()

    def broadcast(self, message, source):
        """
        Envia uma mensagem para todos os clientes conectados,
        exceto a origem da mensagem.

        Args:
                message (str): Mensagem a ser transmitida.
                source (tuple): Endereço de socket do cliente de origem.
        """

        for connection in self.connections:
            if connection.sockname != source:
                connection.send(message)

    def remove_connection(self, connection):
        """
        Remove uma thread ServerSocket do atributo connections.

        Args:
                connection (ServerSocket): Thread ServerSocket a ser removida.
        """
        self.connections.remove(connection)

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
            process = Routine(id, connection)
            self.routines.append(process)
            process.start()

        # Espera mandar os arquivos pra todas as conexões
        print("Rotinas em execução...")
        for process in self.routines:
            process.join()

        print("Rotinas Finalizadas...")
        print("Aguardando retorno ...")
