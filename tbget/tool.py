import argparse
import sys

from .convenience import extract_traceback

def parse_args(argv=sys.argv):
	parser = argparse.ArgumentParser(
		description="Extracts Python tracebacks from garbled text.")
	parser.add_argument("file", default="-", nargs="?",
						help="File to extract TB from (will default to "
						     "reading from standard input).")
	parser.add_argument("--run-tests", action="store_true",
						help="Runs the test suite.")

	return parser.parse_args()

def main(argv=sys.argv):
	args = parse_args()

	if args.run_tests:
		from .tests.run_tests import run_tests
		run_tests()
		return

	file_obj = sys.stdin if args.file == "-" else open(args.file, "rb")
	with file_obj:
		result = extract_traceback(file_obj)
		if result:
			print result
