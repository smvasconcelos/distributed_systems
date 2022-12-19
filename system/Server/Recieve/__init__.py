"""Configuração da classe resposável por receber mensagens do servidor"""
import os
import pickle
import threading
import zipfile
from pathlib import Path

from system.Server.Routine import Routine
from system.utils import *

class Recieve(threading.Thread):
    """
    A thread de recebimento escuta as mensagens recebidas do servidor.

    Attributes:

            sock (socket.socket): Objeto socket conectado.

            name (str): Nome de usuário fornecido pelo usuário.
    """

    def __init__(self, sock, name):
        super().__init__()
        self.sock = sock
        self.name = name
        self.file = None
        self.info = {}
        self.file_path = "RecievedFiles"
        self.file_name = ""
        self.data = b""
        self.program_info = {}

    def run(self):
        """
        Recebe os dados do Broker e os unzipa para executar
        Após iniciar executar, ouve para o termino do processo e enviar o resultado
        já calculado para o broker somar com o total.
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
                print("Loading json ...")
                self.info = pickle.loads(self.data)
                print(self.info["file"]["status"])
                # Se não tiver dado erro
                if self.info:
                    Path(f"RecievedFiles").mkdir(parents=True, exist_ok=True)
                    # E o estado ainda for de escrita
                    # Salva os bytes do arquivo zip
                    if self.info["file"]["status"] == "write":
                        self.file_name = self.info["file"]["name"]
                        self.program_info = self.info["program"]
                        with open(
                            "RecievedFiles/{}".format(self.info["file"]["name"]),
                            "wb+",
                        ) as f:
                            f.write(self.info["file"]["content"])

                        # Logo após já foi enviado e podemos unzipa-lo e iniciar o processo de execução
                        # Iniciamos a Rotina para chamar o programa enviado
                        # Assim que o processo termina e é confirmado que o resultado foi salvo em um arquivo
                        # Retornamos e tentamos abrir o arquivo
                        # Caso esteja tudo okay, envia o resultado com status done
                        # Caso não, 0 com o estado de error
                        self.data = b""
                        unzip_file(self.file_name)
                        print("Inicia a execução do programa depois de extrair o zip ...")
                        self.file_path = "RecievedFiles/{}/Files".format(self.file_name.replace(".zip", ""))
                        self.process = Routine(self.file_path, self.program_info)
                        self.process.start()
                        self.process.join()
                        print("Finalizado execução do programa enviado ...")
                        input_file_name = self.program_info["input"]
                        try:
                          file_zip = "OutputFiles/{}".format(input_file_name.replace("input", "output"))
                          zip_files([file_zip], file_zip.replace(".txt", ""))
                          with open(file_zip.replace("txt", "zip"), 'rb') as f:
                              while True:
                                  data = f.read()
                                  if not data:
                                      break
                                  self.info['file']['name'] = input_file_name.replace("input", "output")
                                  self.info['file']['content'] = data
                                  self.info["file"]["status"] = 'write'
                                  self.sock.send(pickle.dumps(self.info))
                        except:
                            print("Ocorreu um erro executando a rotina ...")
                            self.info['file']['content'] = 'data'
                            self.info["file"]["status"] = 'error'
                            self.sock.send(pickle.dumps(self.info))


            else:
                # Server has closed the socket, exit the program
                print("\nOh não, perdemos conexão com o server.")
                print("\nSaindo...")
                self.sock.close()
                os._exit(0)
