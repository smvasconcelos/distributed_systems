"""Configuração do cliente"""
import socket
import tkinter as tk
from datetime import datetime

from coffeechat.Client.receive import *
from coffeechat.Client.send import *


def get_name(entry, window, obj):
    """
    Captura o nome do usuário pela interface gráfica.

    Attributes:
            entry (tk.Entry): Campo de entrada para o nome do usuário.
            window (tk.Frame): Janela da interface gráfica onde é localizado o campo de entrada.
            obj (Client): Objeto do tipo Client.
    """
    obj.name = entry.get()
    window.destroy()


class Client:
    """
    Oferece suporte ao gerenciamento de conexões cliente-servidor e integração com a GUI.

    Attributes:
            host (str): Endereço IP do socket de escuta do servidor.
            port (int): Número da porta do socket de escuta do servidor.
            sock (socket.socket): Objeto socket conectado.
            name (str): Nome de usuário do cliente.
            messages (tk.Listbox): Objeto tk.Listbox que contém todas as mensagens exibidas na GUI.
    """

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.name = None
        self.messages = None

    def start(self):
        """
        Estabelece a conexão cliente-servidor. Reúne a entrada do usuário para o nome de usuário,
        cria e inicia as threads de envio e recebimento e notifica outros clientes conectados.

        Returns:
                Um objeto Receive que representa o segmento de recebimento.
        """
        print(f"Tentando se conecatar com {self.host}:{self.port}...")
        self.sock.connect((self.host, self.port))
        print(f"Conectado com sucesso a {self.host}:{self.port}\n")

        # create send and receive threads
        send = Send(self.sock, self.name)
        receive = Receive(self.sock, self.name)

        # start send and receive threads
        # send.start()
        receive.start()

        self.sock.sendall(
            "Server: {} acabou de se juntar a equipe, diga ola!".format(
                self.name
            ).encode("ascii")
        )

        return receive

    def send(self):
        """
        Envia dados text_input da GUI. Este método deve ser vinculado a text_input e
        quaisquer outros widgets que ativem uma função semelhante, por exemplo, botões.
        Digitar 'QUIT' fechará a conexão e sairá do aplicativo.

        Args: text_input(tk.Entry): Objeto tk.Entry destinado à entrada de texto do usuário.
        """

        self.sock.send("{}: {}".format(self.name, "message").encode("ascii"))
