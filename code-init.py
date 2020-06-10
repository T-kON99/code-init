from app.Initiator import Initiator
import sys
import argparse

parser = argparse.ArgumentParser(prog='uhunt-init', description='Init a source file with problem details from uhunt along with the pdf file')
parser.add_argument('--no', '-n', dest='problem_no', required=True, type=int, help='Problem number', metavar='problem_no')
parser.add_argument('--lang', '-l', dest='lang', required=True, type=str, help='Source code language', metavar='code_lang')
parser.add_argument('--platform', '-p', dest='platform', required=True, type=str, help='Platform of the website (Example uhunt, projecteuler)', metavar='platform')
parser.add_argument('-o', dest='overwrite', action='store_true', help="Overwrite file")
args = parser.parse_args()

try:
    src_file = Initiator(args.platform).generate_code(args.problem_no, args.lang, args.overwrite)
    print(f'[INFO]: Generated code at {src_file}')
except Exception as err:
    print(err)

