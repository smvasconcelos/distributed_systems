"""Configuração do broker"""
import json
import os
import socket
import threading
from datetime import datetime
from pathlib import Path

from dotenv import find_dotenv, load_dotenv
from system.Broker.Recieve import Recieve
from system.Broker.Send import Send
from system.Broker.utils import *

load_dotenv(find_dotenv())


class Broker(threading.Thread):
    """
    Oferece suporte ao gerenciamento de conexões broker-servidor e suas rotinas.

    Attributes:

        hosts ([{host: localhost, port: 1060]): Array de possiveis conexões a serem tentadas.

        port (int): Número da porta do socket de escuta do servidor.

        sock (socket.socket): Objeto socket conectado.

        count (int): Quantos processos já foram encerrados

        total (int): O resultado da soma total

        connections: (list(socket)) Lista de conexões de socket

        recieves: (list(Recieve)) Lista de threads com a rotirna de recebimento

        routines: (list(Send)) Lista de threads com a rotirna de envio
    """

    def __init__(self, hosts):
        super().__init__()
        self.hosts = hosts
        self.max_conn = len(hosts)
        self.values = [
            x for x in range(int(os.getenv("START_VAL")), int(os.getenv("END_VAL")) + 1)
        ]
        self.count = 0
        self.total = 0
        self.connections = []
        self.recieves = []
        self.routines = []

    def sum_result(self, result):
        """
        Soma result ao resultado total o grava no arquivo caso seja a ultima conexão
        """
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
        Estabelece a conexão cliente-servidor.Cria e inicia as threads de recebimento.
        """
        for conn in self.hosts["connections"]:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.connections.append(sock)
            sock.connect((conn["host"], int(conn["port"])))
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
        for conn_id in range(0, self.max_conn + 1):
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
