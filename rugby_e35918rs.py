import argparse, os

parser = argparse.ArgumentParser()
parser.add_argument('input')
parser.add_argument('output')
args = parser.parse_args()


files = os.listdir(args.input + "/")
for i in files:
	with open(args.input + "/" + i,'r') as f:
		words = f.read()

	scores = [0,0]

	for j in range(1,len(words), 3):
		if words[j+1] == 't': to_add = 5
		elif words[j+1] == 'c': to_add = 2
		elif words[j+1] == 'p': to_add = 3
		elif words[j+1] == 'd': to_add = 3

		if words[j] == '1':
			scores[0] += to_add
		else:
			scores[1] += to_add
	try:
		out_file = open(args.output + "/" + i[:len(i)-4] + "_e35918rs.txt",'w')
		out_file.write(str(scores[0])+":"+str(scores[1]))
		out_file.close()
	except:
		os.mkdir(args.output)
		out_file = open(args.output + "/" + i[:len(i)-4] + "_e35918rs.txt",'w')
		out_file.write(str(scores[0])+":"+str(scores[1]))
		out_file.close()
	print("SUCCESS")