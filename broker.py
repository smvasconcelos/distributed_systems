"""Inicialização do broker"""
import argparse
import json
import os

from system.Broker import Broker

if __name__ == "__main__":

    # Array de conexões
    connections = json.load(open("connections.json", "r"))
    broker = Broker(connections)
    # Inicia a rotina
    broker.start()
