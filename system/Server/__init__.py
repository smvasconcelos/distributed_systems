"""Configuração do servidor"""
import socket
import threading

from system.Server import *
from system.Server.Recieve import Recieve


class Server(threading.Thread):
    """
    Suporta gerenciamento de conexões de servidor.

    Attributes:

            connections (list): Lista de objetos Recieve que representam as conexões ativas.

            host (str): Endereço IP do socket de escuta.

            port (int): Número da porta do socket de escuta.
    """

    def __init__(self, host, port):
        super().__init__()
        # list of server sockets objects representing active client connections
        self.connections = []
        self.host = host
        self.port = port

    def run(self):
        """
        Cria o socket de escuta. O socket de escuta usará a opção SO_REUSEADDR para
        permitir a ligação a um endereço de socket usado anteriormente. Este é um aplicativo de pequena escala que
        suporta apenas uma conexão em espera por vez.
        Para cada nova conexão, um thread Recieve é iniciado para facilitar a comunicação com
        aquele cliente específico. Todos os objetos Recieve são armazenados no atributo connections.
        """
        # AF_INET: address family, for IP networking
        # SOCK_STREAM: socket type, for reliable flow-controlled data stream
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((self.host, self.port))

        sock.listen(1)
        print(f"Ouvindo em {sock.getsockname()}")

        # Ouve novas conexões e as inicia
        while True:
            # new connection
            sc, sockname = sock.accept()
            print(f"Nova conexao de {sc.getpeername()} para {sc.getsockname()}")

            # new thread
            server_socket = Recieve(sc, sockname)
            # start thread
            server_socket.start()

            # add thread to active connections
            self.connections.append(server_socket)
            print(f"Pronto para receber arquivos de {sc.getpeername()}")
