import argparse

parser = argparse.ArgumentParser()
parser.add_argument('input')
parser.add_argument('output')
args = parser.parse_args()

with open(args.input,'r') as file1:
	words = file1.read()

scores = [0,0]

for i in range(1,len(words), 3):
	if words[i+1] == 't': to_add = 5
	elif words[i+1] == 'c': to_add = 2
	elif words[i+1] == 'p': to_add = 3
	elif words[i+1] == 'd': to_add = 3

	if words[i] == '1':
		scores[0] += to_add
	else:
		scores[1] += to_add

out_file = open(args.output,'w')
out_file.write(str(scores[0])+":"+str(scores[1]))
out_file.close()