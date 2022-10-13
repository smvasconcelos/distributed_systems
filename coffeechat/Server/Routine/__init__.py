"""Configuração do servidor"""
import json
import pickle
import threading


class Routine(threading.Thread):

    def __init__(self, id,connection):
        super().__init__()
        self.connection = connection
        self.id = id
        self.message = {
            "file":{
                "status": "write",
                "name": f"file_{id}.zip",
                "content": "binary content",
            },
            "program": {
                "input": f"input_{id}.txt",
                "exe": "sure.exe"
            }
        }

    def run(self):
        try:
            with open(f"Files/{self.message['file']['name']}", 'rb') as f:
                while True:
                    data = f.read(1024)
                    if not data:
                        break
                    self.message['file']['content'] = data
                    self.connection.send(pickle.dumps(self.message))

            self.message['file']['content'] = ""
            self.message['file']['status'] = "done"
            self.connection.send(pickle.dumps(self.message))
        except:
            print("Ocorreu um erro em uma rotina ...")

