import argparse
import json

if __name__ == "__main__":

	parser = argparse.ArgumentParser(description='Program Routine Params')
	parser.add_argument('input_file', help='Arquivo padrão de input')
	parser.add_argument('output_file', help='Arquivo padrão de output')

	args = parser.parse_args()

	result = 0
	with open(args.input_file, 'r') as file:
		result = sum(json.loads(file.read()))

	with open(args.output_file, 'w+') as file:
		file.write(str(result))
