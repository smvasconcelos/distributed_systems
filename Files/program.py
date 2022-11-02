import argparse
import json

if __name__ == "__main__":

	parser = argparse.ArgumentParser(description="Subprocess Routine Params")
	parser.add_argument("input_file", help="Input file to process")
	parser.add_argument("output_file",  help="Output file path to store the results")
	args = parser.parse_args()

	with open(args.input_file, 'r') as f:
		char = f.readline().replace('\n', '')
		string = f.readline()

	with open(args.output_file, 'w+') as f:
			f.write(str(string.count(char)))
