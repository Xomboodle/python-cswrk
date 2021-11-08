import argparse

parser = argparse.ArgumentParser()
parser.add_argument('input')
parser.add_argument('output')
args = parser.parse_args()

# Functions #


def decryptHex(code):
	code = code.split(' ')
	decrypted = ""
	for i in code:
		x = int(i,16)
		decrypted += chr(x)
	return decrypted

def decryptCaesar(code):
	alphabet = list("abcdefghijklmnopqrstuvwxyz")
	print(alphabet)
	decrypted = ""
	for i in range(len(code)):
		if code[i] not in alphabet:
			decrypted += code[i]
			continue
		decrypted += alphabet[(alphabet.index(code[i])) - 3]
	return decrypted

def decryptMorse(code):
	morse_dict = {".-":"a","-...":"b","-.-.":"c","-..":"d",".":"e","..-.":"f",
					"--.":"g","....":"h","..":"i",".---":"j","-.-":"k",".-..":"l",
					"--":"m","-.":"n","---":"o",".--.":"p","--.-":"q",".-.":"r",
					"...":"s","-":"t","..-":"u","...-":"v",".--":"w","-..-":"x",
					"-.--":"y","--..":"z",".-.-.-":".","--..--":",","..--..":"?",
					"-..-.":"/","...-.-":"@",".----":"1","..---":"2","...--":"3",
					"....-":"4",".....":"5","-....":"6","--...":"7","---..":"8",
					"----.":"9","-----":"0"}

	code = code.split(" ")
	decrypted = ""
	for i in code:
		if i == "/":
			decrypted += " "
			continue
		decrypted += morse_dict.get(i)
	return decrypted


with open(args.input,'r') as file:
	encrypted = file.read()
encryption = encrypted.split(':')[0]
to_encrypt = encrypted.split(':')[1]
if encryption == "Hex":
	decrypted = decryptHex(to_encrypt).lower()
elif encryption == "Caesar Cipher(+3)":
	decrypted = decryptCaesar(to_encrypt).lower()
elif encryption == "Morse Code":
	decrypted = decryptMorse(to_encrypt).lower()

with open(args.output,'w') as file:
	file.write(decrypted)