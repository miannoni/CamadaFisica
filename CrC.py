

# def get_bin(x, n=0):
#     """
#     Get the binary representation of x.

#     Parameters
#     ----------
#     x : int
#     n : int
#         Minimum number of digits. If x needs less digits in binary, the rest
#         is filled with zeros.

#     Returns
#     -------
#     str
#     """
#     return format(x, 'b').zfill(n)

# CRC = get_bin(11)

# def CRCbananinha(byte1, byte2):
# 	byte_final = get_bin(byte1,16) + get_bin(byte2, 3)
# 	print("byte final inicial: " + byte_final)

# 	for i in range(len(byte_final) - len(CRC)):

# 		byte_temporario = byte_final[i:i + len(CRC)]
# 		print("byte temporario {}: {}".format(i, byte_temporario))

# 		if (int(byte_final, 2) > 0):# and (len(byte_temporario) > 0):

# 			if int(byte_temporario, 2) >= int(CRC, 2):
# 				print("MAIOR")
# 				print("byte_final: " + byte_final)
# 				print("byte_temporario: " + byte_temporario)
# 				print("CRC: " + CRC)
# 				byte_temporario = get_bin(int(byte_temporario, 2) - int(CRC, 2))

# 				byte_final = byte_final[:i] + byte_temporario + byte_final[i + len(CRC):]
# 				# print("byte final: " + byte_final)
# 				print("byte final: " + byte_final)

# 				print("-"*50+"\n"*2)

# 			else:
# 				print("MENOR")
# 				print("byte_final: " + byte_final)
# 				print("byte_temporario: " + byte_temporario)
# 				print("CRC: " + CRC)
# 				byte_temporario_2 = ""

# 				for x in range(len(CRC)):
# 					if byte_temporario[x] != "0":
# 						byte_temporario_2 += "1"
# 					else:
# 						byte_temporario_2 += "0"

# 				byte_temporario = byte_temporario_2

# 				byte_final = byte_final[:i] + byte_temporario + byte_final[i + len(CRC):]
# 				# print("byte final: " + byte_final)
# 				print("byte final: " + byte_final)

# 				print("-"*50+"\n"*2)
# 				# print("CRC: " + CRC)

# 			# 	newbyte = ""

# 			# 	for x in range(len(byte_temporario)):
# 			# 		if byte_temporario[x] != "0"*len(CRC):
# 			# 			newbyte += ""

# 			# 	byte_final = byte_temporario + byte_final[i + len(CRC):]

# 	if byte_final != 0:
# 		return False
# 	else:
# 		return True


import crc16
crc = crc16.crc16xmodem(b'1234') # bin(11)
crc = crc16.crc16xmodem(b'56789', crc)
print(crc)



# byte1 = 33
# byte2 = 0
# print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
# print(CRCbananinha(byte1,byte2))

b = 2
a = 60
Crc = 11

def to_bin(integer):
	return bin(integer)[2:]

def CrC(payload, resto):
	binario = to_bin(payload) + to_bin(resto)

	print("Binario: ".format(binario))

	counter = 0
	
	while int(binario, 2) > 0:
		print("Contador: {}".format(counter))
		compare_binary = binario[counter:counter + len(to_bin(Crc))]

		if int(compare_binary, 2) > Crc:
			compare_binary = to_bin(int(compare_binary, 2) ^ Crc)

		while len(compare_binary) < 4:
			compare_binary = compare_binary >> 1


# print(to_bin(60))
# print(to_bin(240))

compare_binary = 1

while len(to_bin(compare_binary)) < 4:
	compare_binary = compare_binary >> 1

print(compare_binary)