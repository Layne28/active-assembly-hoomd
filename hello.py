import argparse

parser = argparse.ArgumentParser()

parser.add_argument("-1", "--input1", dest="input1", default="")
parser.add_argument("-2", "--input2", dest="input2", default="")

args = parser.parse_args()

print('hi, testing:', args.input1, args.input2)
