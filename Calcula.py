from binascii import crc_hqx

numero = 11

def CalculaCrC(data):
	# return data % numero
    crc = crc_hqx(data,0xB)

    return crc

a = bytes([11])

print(CalculaCrC(b""))