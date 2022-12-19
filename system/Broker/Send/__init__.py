"""Configuração da rotina do servidor"""
import pickle
import platform
import threading
from system.Broker.utils import *

class Send(threading.Thread):
    """
        Zipa todos os arquivos e os envia para o cliente executar a rotina
    """
    def __init__(self, id,connection):
        super().__init__()
        self.connection = connection
        self.id = id
        self.message = {
            "file":{
                "status": "write",
                "name": f"file_{id}.zip",
                "content": "",
            },
            "program": {
                "input": f"input_{id}.txt",
                "exe": "program.exe" if platform.system() == "Windows" else "program.bin"
            }
        }

    def run(self):
        try:
            with open(f"Files/{self.message['file']['name']}", 'rb') as f:
                print("Enviando arquivo {}...".format(self.message["program"]["input"]))
                while True:
                    data = f.read()
                    if not data:
                        break
                    self.message['file']['content'] = data
                    self.connection.send(pickle.dumps(self.message))

            self.message['file']['content'] = ""
            self.message['file']['status'] = "done"
            self.connection.send(pickle.dumps(self.message))
            print("Arquivo enviado {}...".format(self.message["program"]["input"]))
        except:
            print("Ocorreu um erro enviando ...")

