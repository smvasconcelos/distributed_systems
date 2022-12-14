"""Configuração da rotina do cliente"""
import platform
import subprocess
import threading
from pathlib import Path


class Routine(threading.Thread):
    """
        Executa a rotina enviada pelo servidor
    """

    def __init__(self, files_folder, program_info):
        super().__init__()
        self.folder = files_folder
        self.info = program_info
        self.output_path = ""
        self.done = False
        Path(f"OutputFiles").mkdir(parents=True, exist_ok=True)

    def run(self):
        print("Summing file content ...")
        program = "{}/{}".format(self.folder, self.info["exe"])
        input_file = "{}/{}".format(self.folder, self.info["input"])
        output_file = "OutputFiles/{}".format(self.info["input"].replace("input", "output"))
        try:
            python = "python" if platform.system() == "Windows" else "python3"
            subprocess.check_call(
            [
                python,
                program,
                input_file,
                output_file
            ])
            while True:
                output_file = Path(output_file)
                try:
                    print(output_file.is_file())
                    if output_file.is_file():
                        open(output_file, 'rb')
                        break
                except:
                    pass
        except:
            print("Ocorreu um erro executando o programa enviado...")
