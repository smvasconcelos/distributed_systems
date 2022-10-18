"""Configuração da classe resposável por receber mensagens do servidor"""
import threading


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
        self.file_path = "RecievedFiles"
        self.file_name = ""
        self.broker = broker
        self.program_info = {}

    def run(self):
        """
        Recebe dados do servidor e os exibe na GUI.
        Sempre escuta os dados de entrada até que uma das extremidades feche o socket.
        """
        while True:
            """
                message : "file_name", int result,  "status",
            """
            message = self.sock.recv(1024).decode("asciii")
            if message:
                file_name , result, status, = message.split(",")
                if status == "done":
                    self.broker.sum_result(result)
                else:
                    print(f"Ocorreu um erro executando o processo com o arquivo de nome: {file_name}")
