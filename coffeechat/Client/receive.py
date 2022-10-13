"""Configuração da classe resposável por receber mensagens do servidor"""
import json
import os
import pickle
import socket
import threading
import tkinter as tk
import zipfile
from datetime import datetime
from pathlib import Path

from coffeechat.Client.Routine import Routine


def unzip_file(file_name):

    with zipfile.ZipFile(f"RecievedFiles/{file_name}", 'r') as zip_ref:
        zip_ref.extractall("RecievedFiles/{}".format(file_name.replace(".zip", "")))

class Receive(threading.Thread):
    """
    A thread de recebimento escuta as mensagens recebidas do servidor.

    Attributes:
            sock (socket.socket): Objeto socket conectado.
            name (str): Nome de usuário fornecido pelo usuário.
            messages (tk.Listbox): Objeto tk.Listbox que contém todas as mensagens exibidas na GUI.
    """

    def __init__(self, sock, name):
        super().__init__()
        self.sock = sock
        self.name = name
        self.file = None
        self.info = {}
        self.file_path = "RecievedFiles"
        self.file_name = ""
        self.program_info = {}

    def run(self):
        """
        Recebe dados do servidor e os exibe na GUI.
        Sempre escuta os dados de entrada até que uma das extremidades feche o socket.
        """
        while True:
            """
            message: {
                host: ip:port
                file:{
                    status: "write" | "done"
                    name: string
                    content: "binary content"
                }
                program: {
                    input: "input.txt" | string,
                    exe: program.exe
                }
            }
            """
            data = b""
            while True:
                message = self.sock.recv(1024)
                if not message:
                    break
                data += message
                try:
                    pickle.loads(data)
                    break
                except:
                    pass

            if data:
                print("Loading json ...")
                self.info = pickle.loads(data)
                Path(f"RecievedFiles").mkdir(parents=True, exist_ok=True)
                try:
                    if self.info:
                        if self.info["file"]["status"] == "write":
                            self.file_name = self.info["file"]["name"]
                            self.program_info = self.info["program"]
                            with open(
                                "RecievedFiles/{}".format(self.info["file"]["name"]),
                                "wb+",
                            ) as f:
                                f.write(self.info["file"]["content"])
                    else:
                        print("Ocorreu um erro durante o parsign do json...")
                except:
                    unzip_file(self.file_name)
                    print("Inicia a execução do programa depois de extrair o zip ...")
                    self.file_path = "RecievedFiles/{}/Files".format(self.file_name.replace(".zip", ""))
                    self.process = Routine(self.file_path, self.program_info)
                    self.process.start()
                    self.process.join()
                    input_file_name = self.program_info["input"]
                    with open("OutputFiles/{}".format(input_file_name.replace("input", "output")), 'r') as f:
                        result = f.read()
                    self.sock.send(f"{self.file_name},done,{result}".encode("ascii"))


            else:
                # Server has closed the socket, exit the program
                print("\nOh não, perdemos conexão com o server.")
                print("\nSaindo...")
                self.sock.close()
                os._exit(0)
