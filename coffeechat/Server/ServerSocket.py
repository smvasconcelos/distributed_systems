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

    def sum_result(self, result):
        data = 0
        print(f"Somando resultado: {result}")
        Path(f"Result").mkdir(parents=True, exist_ok=True)
        my_file = Path("Result/result.txt")
        if my_file.is_file():
            print("Somando resultado com arquivo ...")
            with open("Result/result.txt", "r+") as f:
                data = f.read()

        with open("Result/result.txt", "w+") as f:
            print("Gravando resultado em um arquivo ...")
            f.write(str(result + int(data)))


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
                    self.result = {
                        "file" : self.info[0],
                        "status": self.info[1],
                        "result": self.info[2]
                    }
                    self.sum_result(int(self.info[2]))
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
