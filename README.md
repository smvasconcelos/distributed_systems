<!-- PROJECT LOGO -->
<br />
<p align="center">
  <a href="https://github.com/smvasconcelos/tictactoe">
	<h2 align="center">Sistemas Distribuidos - Projeto</h2>
  </a>
  <p align="center">
    Projeto final desenvolvido para a disciplina de Sistemas Distribuidos.
    <br />
  </p>
  <p align="center"><a href="https://smvasconcelos.github.io/distributed_systems/"> Link para documentação do projeto. <a/></p>
	<br />
</p>

<p align="center" >
	<img alt="python" src="https://badges.aleen42.com/src/python.svg">
	<img alt="python" src="https://img.shields.io/badge/3.9-python-blue">
 </p>


# Como utilizar

Inicialmente certifique-se que o python 3.9 ou superior está instalado na sua máquina, em seguida será necessário o git ou então que se faça o download do zip do projeto e prossiga com as instruções para rodar o projeto.

## Python

Para rodar o projeto abra a pasta do ambiente e clone o repositório em questão com :

```
$ git clone https://github.com/smvasconcelos/distributed_systems.git
$ cd distributed_systems
```


Preferencialmente inicie um ambiente virtual com :

```
$ pip install virtualenv
$ python -m venv .
```

E por último inicie o ambiente virtual e instale as dependências do python para iniciar o projeto :

```
$ cd Scripts
$ activate
$ cd ..
$ pip install -r requirements.txt
```

## Executando e testando

Para executar o servidor socket utilize:

```
$ python server.py
```

É aceito um endereço como parametro de execução e tem como default localhost
Além disso é possível passar a porta como uma flag indicando a porta a ser utilizada

```
$ python server.py 192.168.0.1
$ python server.py 192.168.0.1 -p 1060
```
Para o broker é necessário informar os endereços utilizados pelos servers no arquivo
connections.json que contém um array de objetos contendo cada host e suas portas
que serão utilizadas como parametro para iniciar o socket
```
$ python broker.py
```
É possível também alterar o intervalo em que os valores somados serão gerados indicas também no .env
```
  START_VAL = 0
  END_VAL = 100
```
Após a execução do código teremos x pastas resultantes, na seguinte estrutura:

	root
	├── Files
	│   ├── program.py -> Programa que vai ser executado nos clientes
	│   ├── input_0.txt -> Input do program.py para cada endereço n
	│   ├── file_0.zip -> O arquivo zipado do program.py com o input
	│   ├── input_n.zip
	│   └── file_n.zip
	│
	├── OutputFiles
	│   ├── output_0.txt -> Saída do programa 0
	│   └── output_n.txt
	│
	├── RecievedFiles
	│   ├── file_0.zip -> Arquivo enviado pelo servidor com o programa a ser executado com o seu respectivo input
	│   └─── file_0
	│          ├── Files
	│          ├── input_0.txt -> Input do programa x
	│          └── program.py -> Arquivo contendo a rotina pra ser executada no cliente
	└── .env


# Gerar documentação

```
$ pdoc server.py broker.py system -o docs
```
