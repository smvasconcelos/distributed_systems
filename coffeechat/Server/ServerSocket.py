"""Configuração do socket do servidor"""
import os
import pickle
import threading
from pathlib import Path


class ServerSocket(threading.Thread):
    """
    Suporta comunicações com um cliente conectado.

    Attributes:
            sc (socket.socket): Socket conectado.
            sockname (tuple): Endereço do socket do client.
            server (Server): Thread pai.
    """

    def __init__(self, sc, sockname, server):
        super().__init__()
        self.sc = sc
        self.sockname = sockname
        self.server = server
        self.info = []
        self.result = {}

    def run(self):
        """
        Recebe dados do cliente conectado e transmite a mensagem para todos os outros clientes.
        Se o cliente saiu da conexão, fecha o socket conectado e remove a si mesmo da lista
        de threads ServerSocket no thread de servidor pai.
        """
        while True:
            message = self.sc.recv(1024).decode("ascii")
            if message:
                self.info = message.split(",")
                try:
                    self.server.sum_result(int(self.info[2]))
                except:
                    print(f"{self.sockname} diz {message}")
                    self.server.broadcast(message, self.sockname)
            else:
                print(f"{self.sockname} fechou a conexao.")
                self.sc.close()
                self.server.remove_connection(self)
                return

    def send(self, message):
        """
        Envia uma mensagem ao servidor conectado

        Args:
            message (str): Mensagem a ser enviada.
        """
        if type(message) == str:
            self.sc.sendall(message.encode("ascii"))
        else:
            self.sc.sendall(message)
