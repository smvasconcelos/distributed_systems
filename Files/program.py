import argparse
import json

if __name__ == "__main__":

	parser = argparse.ArgumentParser(description="Subprocess Routine Params")
	parser.add_argument("input_file", help="Input file to process")
	parser.add_argument("output_file",  help="Output file path to store the results")
	args = parser.parse_args()

	arr = []
	with open(args.input_file, 'rb') as f:
		arr = json.loads(f.read())

	with open(args.output_file, 'w+') as f:
			f.write(str(sum(arr)))
