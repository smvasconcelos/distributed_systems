"""Configuração da rotina do server"""
import os
import platform
import subprocess
import threading
from pathlib import Path


class Routine(threading.Thread):
    """
        Executa a rotina enviada pelo broker
    """

    def __init__(self, files_folder, program_info):
        super().__init__()
        self.folder = files_folder
        self.info = program_info
        self.output_path = ""
        self.done = False
        Path(f"OutputFiles").mkdir(parents=True, exist_ok=True)

    def run(self):
        """
            Executa o arquivo enviado com o input recebido
        """
        print("Executando arquivo recebido...")
        program = "{}/{}".format(self.folder, self.info["exe"])
        input_file = "{}/{}".format(self.folder, self.info["input"])
        output_file = "OutputFiles/{}".format(self.info["input"].replace("input", "output"))
        try:
            if platform.system()  != "Windows":
                os.system(f"chmod +x {program}")
            subprocess.run([program, input_file, output_file])
            while True:
                output_file = Path(output_file)
                try:
                    if output_file.is_file():
                        open(output_file, 'rb')
                        break
                except:
                    pass
        except:
            print("Ocorreu um erro executando o programa enviado...")
