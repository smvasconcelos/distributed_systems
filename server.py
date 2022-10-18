"""Inicialização do servidor e suas rotinas"""
import argparse
import threading

import system.utils as utils
from system.Server import Server

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="CoffeChat Server")
    parser.add_argument("host", nargs='?', default="localhost", help="Interface the server listens at")
    parser.add_argument(
        "-p", metavar="PORT", type=int, default=1060, help="TCP port (default 1060)"
    )
    args = parser.parse_args()
    server = Server(args.host, args.p)
    server.start()

    exit = threading.Thread(target=utils.exit, args=(server,))
    exit.start()
