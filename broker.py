"""Inicialização do brokere"""
import argparse
import json
import os

from system.Broker import Broker

if __name__ == "__main__":

	connections = json.load(open("connections.json", "r"))
	broker = Broker(connections)
	broker.start()

