import argparse, os

parser = argparse.ArgumentParser()
parser.add_argument('engwords')
parser.add_argument('input')
parser.add_argument('output')
args = parser.parse_args()

punct_list = [".",",","!",'"',"'","?","-",":",";","[","]","(",")","{","}","/","@","~","#","+"]

def oneLineCheck(words):
	with open(args.engwords,'r') as checkfile:
		checkers = checkfile.read()
	checkers = checkers.splitlines()
	punct_removed = num_removed = case_changed = correct_words = incorrect_words = 0
	words = words.split(" ")
	words_in_file = len(words)
	for word in words:
		formatted = word.translate({ord(c):None for c in punct_list})
		punct_removed += len(word) - len(formatted)
		num_formatted = formatted.translate({ord(c):None for c in "1234567890"})
		num_removed += len(formatted) - len(num_formatted)
		for c in num_formatted:
			char_formatted = c.lower()
			if char_formatted != c:
				case_changed += 1
		if num_formatted == "":
			words_in_file -= 1
			continue
		if num_formatted.lower() in checkers:
			correct_words += 1
		else:
			incorrect_words += 1

	return [case_changed, punct_removed, num_removed, words_in_file, correct_words, incorrect_words]

def multiLineCheck(words):
	with open(args.engwords,'r') as checkfile:
		checkers = checkfile.read()
	checkers.splitlines()
	punct_removed = num_removed = case_changed = correct_words = incorrect_words = words_in_file = 0
	for i in words:
		i = i.split(" ")
		words_in_file += len(i)
		for word in i:
			formatted = word.translate({ord(c):None for c in punct_list})
			punct_removed += len(word) - len(formatted)
			num_formatted = formatted.translate({ord(c):None for c in "1234567890"})
			num_removed += len(formatted) - len(num_formatted)
			for c in num_formatted:
				char_formatted = c.lower()
				if char_formatted != c:
					case_changed += 1
			if num_formatted.lower() in checkers:
				correct_words += 1
			else:
				incorrect_words += 1
	return [case_changed, punct_removed, num_removed, words_in_file, correct_words, incorrect_words]			

def writeFormat(format_display, file):
	try:
		out_file = open(path_end + file[:len(file)-4] + "_e35918rs.txt", 'w')
	except:
		os.mkdir(args.output)
		out_file = open(path_end + file[:len(file)-4] + "_e35918rs.txt", 'w')
	out_file.writelines(["e35918rs","\nFormatting ###################",
							"\nNumber of upper case words changed: " + str(format_display[0]),
							"\nNumber of punctuations removed: " + str(format_display[1]),
							"\nNumber of numbers removed: " + str(format_display[2]),
							"\nSpellchecking ###################",
							"\nNumber of words: " + str(format_display[3]),
							"\nNumber of correct words: " + str(format_display[4]),
							"\nNumber of incorrect_words: " + str(format_display[5])])
	out_file.close()


files = os.listdir(args.input)
if args.input[-1] == "/":
	path_start = args.input
else:
	path_start = args.input + "/"
if args.output[-1] == "/":
	path_end = args.output
else:
	path_end = args.output + "/"
for i in files:
	with open(path_start + i, 'r') as file:
		words = file.read()

	words = words.split('\n')
	if len(words) == 1:
		format_display = oneLineCheck(words[0])
	else:
		format_display = multiLineCheck(words)
	writeFormat(format_display, i)




