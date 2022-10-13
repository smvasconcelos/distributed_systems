"""Configuração do servidor"""
import json
import pickle
import threading
from pathlib import Path


class Routine(threading.Thread):

    def __init__(self, files_folder, program_info):
        super().__init__()
        self.folder = files_folder
        self.info = program_info
        self.output_path = ""
        Path(f"OutputFiles").mkdir(parents=True, exist_ok=True)

    def run(self):
        print("Summing file content ...")
        arr = []
        with open("{}/{}".format(self.folder, self.info["input"]), 'rb') as f:
            arr = json.loads(f.read())

        print(f"The sum is equal to {sum(arr)}")
        with open("OutputFiles/{}".format(self.info["input"].replace("input", "output")), 'w+') as f:
            f.write(str(sum(arr)))
