"""Inicialização do servidor e suas rotinas"""
import threading

import system.utils as utils
from system.Server import Server

if __name__ == "__main__":

    host = input('Host (default localhost): ')
    host =  host if not host else 'localhost'
    port = input('Port (default 1060): ')
    port = 1060 if not port else int(port)
    server = Server(host, port)
    server.start()

    exit = threading.Thread(target=utils.exit, args=(server,))
    exit.start()
