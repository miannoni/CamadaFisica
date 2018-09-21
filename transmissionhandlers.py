import time
from enlace import *
from formathandler import *
from os import system
import serial.tools.list_ports

class transmitter:

	def __init__(self, usb_port):
		self.com = enlace(str(serial.tools.list_ports.comports()[usb_port])[0:5])
		self.mensagem = formater()
		self.comunicating = True
		self.com.enable()

	def print(self, string, sleep_bool):
		# system("cls")
		print(string)
		if sleep_bool == True:
			time.sleep(0.25)

	def recieve1(self):
		messagetype = -1

		while (messagetype != 1) and (messagetype != 7):
			self.print("Esperando handshake 1...", False)

			rxBuffer, nRx = self.com.getunknownData()
			if nRx != 0:
				payload, messagetype, unit, total_units = self.mensagem.parsemessage(rxBuffer)

			if messagetype == 7:
				self.endComunication()
				self.comunicating = False

	def send1recieve2(self):
		if self.comunicating == True:
			messagetype = -1

			n = time.clock()

			while (messagetype != 2) and (messagetype != 7):
				if messagetype == -1:
					self.print("Enviando handshake 1...", False)
					type1 = self.mensagem.setupmessage(bytearray(), 1)
					self.com.sendData(type1)
					messagetype = -2

				elif messagetype == -2:
					self.print("Re-enviando handshake 1...", False)
					type1 = self.mensagem.setupmessage(bytearray(), 1)
					self.com.sendData(type1)

				print("Esperando handshake 2...")
				rxBuffer, nRx = self.com.getunknownData()
				if nRx > 0:
					payload, messagetype, unit, total_units = self.mensagem.parsemessage(rxBuffer)

				if messagetype == 7:
					self.endComunication()
					self.comunicating = False

	def send2recieve3(self):
		if self.comunicating == True:
			messagetype = -1

			while (messagetype != 3) and (messagetype != 7):
				if messagetype == -1:
					self.print("Enviando handshake 2...", False)
					type4 = self.mensagem.setupmessage(bytearray(),  2)
					self.com.sendData(type4)
				if (messagetype == -2):
					self.print("Re-enviando handshake 2...", False)
					# print("Re-enviando um salve de volta...")
					type4 = self.mensagem.setupmessage(bytearray(),  2)
					self.com.sendData(type4)

				messagetype = -2

				print("Esperando handshake 3...")
				rxBuffer, nRx = self.com.getunknownData()
				if nRx != 0:
					payload, messagetype, unit, total_units = self.mensagem.parsemessage(rxBuffer)
				if messagetype == 7:
					self.endComunication()
					self.comunicating = False

	def send3(self):
		if self.comunicating == True:
			print("Enviando handshake 3...")
			type3 = self.mensagem.setupmessage(bytearray(), 3)
			self.com.sendData(type3)

	def sendData(self, Bytearray):
		if self.comunicating == True:
			messagetype = -1

			print("Tempo teorico de envio: {}".format(round((2*len(Bytearray)*10/115200), 3)))

			package_counter = 0
			lista_pacotes = self.mensagem.setupmessage(Bytearray,  4)
			false_message = True
			# pacotes_confirmados = []

			while (messagetype != 7) and (package_counter < len(lista_pacotes)):
				if messagetype == -1:
					print("Enviando dados...")

					if package_counter == 5 and false_message == True:
						package_counter = 10
						false_message = False

					# for x in lista_pacotes:
					if True:
						print("Pacote {} de {}...".format(package_counter + 1, len(lista_pacotes)))
						print("Tamanho do pacote: {}".format(len(lista_pacotes[package_counter])))
						self.com.sendData(lista_pacotes[package_counter])
					messagetype = -2

				elif (messagetype == -2):
					# print("ERRO: Ack ou Nack não recebido")
					print("Re-enviando dados...")

					# for x in lista_pacotes:
					if True:
						print("Pacote {} de {}...".format(package_counter + 1,len(lista_pacotes)))
						self.com.sendData(lista_pacotes[package_counter])

				print("Esperando confirmação de envio...")
				rxBuffer, nRx = self.com.getunknownData()
				if nRx > 0:
					payload, messagetype, unit, total_units = self.mensagem.parsemessage(rxBuffer)
					if messagetype == 5:
						# pacotes_confirmados.append(package_counter)
						print("Recebimento do pacote {} confirmado!".format(package_counter + 1))
						package_counter += 1
						# if package_counter > len(lista_pacotes):
						# 	break
						messagetype = -1
					elif messagetype == 6:
						print("Nack recebido para o pacote {}, pacote {} foi pedido.".format(package_counter, payload))
						package_counter = payload
						messagetype = -2
					else:
						print("Tipo da mensagem {} não é valido nesse momento...".format(messagetype))
						messagetype = -2

	def recieveData(self):
		if self.comunicating == True:
			messagetype = -1
			size = 0
			mensagem_final = b""
			esperando_pacote_ = 0
			unit = 0

			while ((messagetype != 7) and ((esperando_pacote_ < size) or (size == 0))):
				if messagetype == -1:
					print("Esperando pacote {}...".format(esperando_pacote_ + 1))
					messagetype = -2

				elif messagetype == -2:
					print("Esperando pacote {} novamente...".format(esperando_pacote_ + 1))

				elif (messagetype == -3):
					print("Houve um erro no recebimento do pacote {}".format(esperando_pacote_ + 1))
					type6 = self.mensagem.setupmessage(str(esperando_pacote_).encode(), 6)
					print("Pedindo pacote {} novamente...".format(esperando_pacote_ + 1))
					self.com.sendData(type6)

				elif (unit != esperando_pacote_):
					print("Erro: pacote {} recebido, esperando pacote {}".format(unit + 1, esperando_pacote_ + 1))
					type6 = self.mensagem.setupmessage(str(esperando_pacote_).encode(), 6)
					print("Pedindo pacote {} novamente...".format(esperando_pacote_ + 1))
					self.com.sendData(type6)

				rxBuffer, nRx = self.com.getunknownData()

				if nRx != 0:
					rxBuffer_forReal, messagetype, unit, size_ = self.mensagem.parsemessage(rxBuffer)
				
					if messagetype == 4:
						# if unit not in pacotes_recebidos:
						if (unit == esperando_pacote_):
							if (size == 0):
								size = size_
							# pacotes_recebidos.append(unit)
							# mensagem_lista.append(rxBuffer_forReal)
							print("Pacote {} de {} recebido com sucesso!".format(esperando_pacote_ + 1, size))
							print("Enviando confirmacao do pacote {}...".format(esperando_pacote_ + 1))
							type5 = self.mensagem.setupmessage(bytearray(), 5)
							self.com.sendData(type5)
							mensagem_final += rxBuffer_forReal
							print("Tamanho do payload reagrupado: {}".format(len(mensagem_final)))
							esperando_pacote_ += 1
							unit += 1
				# else:
				# 	if messagetype == 4:
				# 		# if unit not in pacotes_recebidos:
				# 		if (unit == esperando_pacote_):
				# 			if (size == 0):
				# 				size = size_
				# 			print("Re-enviando confirmacao do pacote {}...".format(esperando_pacote_ + 1))
				# 			type5 = self.mensagem.setupmessage(bytearray(), 5)
				# 			self.com.sendData(type5)

			# mensagem_final = b""
			# package_counter = 0

			# while len(mensagem_lista) != (counter + 1):
			# 	#mensagem_final += mensagem_lista[i]
			# 	for i in pacotes_recebidos:
			# 		if pacotes_recebidos[i] == counter:
			# 			mensagem_final += mensagem_lista[i]
			# 			# del mensagem_lista[i]
			# 			# del pacotes_recebidos[i]
			# 			package_counter += 1

			if messagetype == 7:
				self.endComunication()
				self.comunicating = False

			# return rxBuffer_forReal
			return mensagem_final

	def send5recieve7(self):
		if self.comunicating == True:
			messagetype = -1

			while (messagetype != 7):
				if messagetype == -1:
					self.print("Enviando confirmacao de recebimento...", False)
					type5 = self.mensagem.setupmessage(bytearray(),  5)
					self.com.sendData(type5)
				if (messagetype == -2):
					self.print("Re-enviando confirmacao de recebimento...", False)
					type5 = self.mensagem.setupmessage(bytearray(),  5)
					self.com.sendData(type5)

				messagetype = -2

				rxBuffer, nRx = self.com.getunknownData()
				if nRx != 0:
					payload, messagetype, unit, total_units = self.mensagem.parsemessage(rxBuffer)
				if messagetype == 7:
					self.endComunication()
					self.comunicating = False

	def send7(self):
		if self.comunicating == True:
			self.print("Enviando encerramento", True)
			type7 = self.mensagem.setupmessage(bytearray(),  7)
			self.com.sendData(type7)
			self.endComunication()
			self.comunicating = False

	def send7recieve7(self):
		if self.comunicating == True:
			messagetype = -1
			while (messagetype != 7):
				if messagetype == -1:
					self.print("Enviando encerramento de comunicação...", False)
					type4 = self.mensagem.setupmessage(bytearray(),  7)
					self.com.sendData(type4)
					messagetype = -2

				elif (messagetype == -2):
					self.print("Re-enviando encerramento de comunicação...", False)
					type4 = self.mensagem.setupmessage(bytearray(),  7)
					self.com.sendData(type4)

				print("Esperando encerramento de comunicação...")
				rxBuffer, nRx = self.com.getunknownData()
				if nRx > 0:
					payload, messagetype, unit, total_units = self.mensagem.parsemessage(rxBuffer)

	def endComunication(self):
		if self.comunicating == True:
			print("-------------------------")
			print("Comunicação encerrada")
			print("-------------------------")
			self.com.disable()