"""Inicialização do broker"""
import argparse
import json
import os

from system.Broker import Broker

if __name__ == "__main__":

    chosen_text = ""
    chosen_string = input("Digite uma string para procurar no texto (default é gerado automaticamente): ")
    if chosen_string :
      chosen_text = input("Digite um texto para ser dividido e procurado pelo algoritmo (default é gerado automaticamente): ")

    # Array de conexões
    connections = json.load(open("connections.json", "r"))
    broker = Broker(connections, chosen_string, chosen_text)
    # Inicia a rotina
    broker.start()
