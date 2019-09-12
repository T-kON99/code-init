import app.uhunt as uhunt
import sys
import argparse

parser = argparse.ArgumentParser(prog='uhunt-init', description='Init a source file with problem details from uhunt along with the pdf file')
parser.add_argument('--problem', '-p', dest='problem_no', required=True, type=int, help='Problem number', metavar='problem_no')
parser.add_argument('--lang', '-l', dest='lang', required=True, type=str, help='Source code language', metavar='code_lang')
parser.add_argument('-o', dest='overwrite', action='store_true', help="Overwrite file")
args = parser.parse_args()

try:
    uhunt.uhunt(args.problem_no, args.lang, args.overwrite)
except Exception as err:
    print(err)

