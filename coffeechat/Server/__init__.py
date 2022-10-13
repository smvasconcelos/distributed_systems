"""Configuração do servidor"""
import json
import os
import pickle
import socket
import threading
import zipfile
from pathlib import Path

from coffeechat.Server import *
from coffeechat.Server.Routine import Routine
from coffeechat.Server.ServerSocket import ServerSocket


def split(a, n):
    k, m = divmod(len(a), n)
    return list(a[i * k + min(i, m) : (i + 1) * k + min(i + 1, m)] for i in range(n))


def zip_files(list_files_path, output_name):
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
    """

    def __init__(self, host, port):
        super().__init__()
        # list of server sockets objects representing active client connections
        self.connections = []
        self.host = host
        self.port = port
        self.routine = False
        self.routines = []
        self.max_conn = 1
        self.values = [x for x in range(0, 100)]
        self.data = b""

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
                server_socket = ServerSocket(sc=sc, sockname=sockname, server=self)
                # start thread
                server_socket.start()

                # add thread to active connections
                self.connections.append(server_socket)
                print(f"Pronto para receber mensagens de {sc.getpeername()}")
                if len(self.connections) == self.max_conn:
                    self.prepare_routine()

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
        # Tem que fazer a lógica de divisão dos arquivos
        # Dai cria uma pasta pra cada conexão com os ID
        # Dps zipa elas pra enviar de vez tudo, junto com o algoritmo que vai somar tudo
        print("Preparando rotina ...")
        self.values = split(self.values, len(self.connections))
        Path(f"Files").mkdir(parents=True, exist_ok=True)
        for conn_id in range(0, self.max_conn):
            with open(f"Files/input_{conn_id}.txt", "w+") as f:
                f.write(json.dumps(self.values[conn_id]))
            zip_files(
                [f"Files/input_{conn_id}.txt", "Files/sample.exe"], f"file_{conn_id}"
            )
            print(f"Zipped [input_{conn_id}.txt, sample.exe] => file_{conn_id}.zip ...")
        self.start_routine()

    def start_routine(self):
        print("Iniciando rotina ...")
        self.routine = True
        for id, connection in enumerate(self.connections):
            process = Routine(id, connection)
            self.routines.append(process)
            process.start()

        # Espera mandar os arquivos pra todas as conexões
        print("Rotinas em execução...")
        for process in self.routines:
            process.join()

        print("Rotinas Finalizadas...")
        print("Aguardando retorno ...")
