"""Configuração da classe resposável por receber mensagens do servidor"""
import pickle
import threading
from pathlib import Path


class Recieve(threading.Thread):
    """
    A thread de recebimento escuta as mensagens recebidas do servidor.

    Attributes:

        sock (socket.socket): Objeto socket conectado.

        name (str): Nome de usuário fornecido pelo usuário.

        messages (tk.Listbox): Objeto tk.Listbox que contém todas as mensagens exibidas na GUI.
    """

    def __init__(self, sock, broker):
        super().__init__()
        self.sock = sock
        self.file = None
        self.info = {}
        self.file_path = "ResultFiles"
        self.file_name = ""
        self.broker = broker
        self.program_info = {}
        self.data = b''
        Path(f"{self.file_path}").mkdir(parents=True, exist_ok=True)

    def run(self):
        """
        Recebe dados do servidor e os exibe na GUI.
        Sempre escuta os dados de entrada até que uma das extremidades feche o socket.
        """
        while True:
            """
                message : "file_name", "status", int result
            """
            while True:
                message = self.sock.recv(1024)
                if not message:
                    break
                self.data += message
                try:
                    pickle.loads(self.data)
                    break
                except:
                    pass

            if self.data:
                self.info = pickle.loads(self.data)
                if self.info["file"]["status"] != "error":
                    with open(f"{self.file_path}/{self.info['file']['name']}", "wb+") as f:
                        f.write(self.info["file"]["content"])

                    with open(f"{self.file_path}/{self.info['file']['name']}", "r") as f:
                        result = f.read()
                        self.broker.sum_result(int(result))
                else:
                    print(f"Ocorreu um erro executando o processo com o arquivo de nome: {self.file_name}")
