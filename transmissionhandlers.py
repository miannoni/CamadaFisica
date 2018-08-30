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

	def prettyprint(self, string, sleep_bool):
		# system("cls")
		print(string)
		if sleep_bool == True:
			time.sleep(0.25)

	def recieve1(self):
		messagetype = -1

		while (messagetype != 1) and (messagetype != 7):
			self.prettyprint("Esperando handshake 1...", False)

			rxBuffer, nRx = self.com.getunknownData()
			if nRx != 0:
				payload, messagetype = self.mensagem.parsemessage(rxBuffer)

			if messagetype == 7:
				self.endComunication()
				self.comunicating = False

	def send1recieve2(self):
		if self.comunicating == True:
			messagetype = -1

			n = time.clock()

			while (messagetype != 2) and (messagetype != 7):
				if messagetype == -1:
					self.prettyprint("Enviando handshake 1...", False)
					type1 = self.mensagem.setupmessage(bytearray(), 1)
					self.com.sendData(type1)
					messagetype = -2

				elif messagetype == -2:
					self.prettyprint("Re-enviando handshake 1...", False)
					type1 = self.mensagem.setupmessage(bytearray(), 1)
					self.com.sendData(type1)

				print("Esperando handshake 2...")
				rxBuffer, nRx = self.com.getunknownData()
				if nRx > 0:
					payload, messagetype = self.mensagem.parsemessage(rxBuffer)

				if messagetype == 7:
					self.endComunication()
					self.comunicating = False

	def send2recieve3(self):
		if self.comunicating == True:
			messagetype = -1

			while (messagetype != 3) and (messagetype != 7):
				if messagetype == -1:
					self.prettyprint("Enviando handshake 2...", False)
					type4 = self.mensagem.setupmessage(bytearray(),  2)
					self.com.sendData(type4)
				if (messagetype == -2):
					self.prettyprint("Re-enviando handshake 2...", False)
					# print("Re-enviando um salve de volta...")
					type4 = self.mensagem.setupmessage(bytearray(),  2)
					self.com.sendData(type4)

				messagetype = -2

				print("Esperando handshake 3...")
				rxBuffer, nRx = self.com.getunknownData()
				if nRx != 0:
					payload, messagetype = self.mensagem.parsemessage(rxBuffer)
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

			while (messagetype != 5) and (messagetype != 7):
				if messagetype == -1:
					print("Enviando dados...")
					type4 = self.mensagem.setupmessage(Bytearray,  4)
					self.com.sendData(type4)
					messagetype = -2

				elif (messagetype == -2) or (messagetype == 6):
					print("ERRO: Ack e Nack não recebido")
					print("Re-enviando dados...")
					type4 = self.mensagem.setupmessage(Bytearray,  4)
					self.com.sendData(type4)

				print("Esperando confirmação de envio...")
				rxBuffer, nRx = self.com.getunknownData()
				if nRx > 0:
					payload, messagetype = self.mensagem.parsemessage(rxBuffer)

	def recieveData(self):
		if self.comunicating == True:
			messagetype = -1

			while (messagetype != 4) and (messagetype != 7):
				if messagetype == -1:
					self.prettyprint("Esperando mensagem...", False)

				if messagetype == -2:
					self.prettyprint("Esperando mensagem novamente...", False)

				if messagetype == -3:
					self.prettyprint("Houve um erro no recebimento", False)
					type6 = self.mensagem.setupmessage(bytearray(), 6)
					self.com.sendData(type6)
					self.print("Esperando mensagem novamente...")

				messagetype = -2

				rxBuffer, nRx = self.com.getunknownData()
				if nRx != 0:
					rxBuffer_forReal, messagetype = self.mensagem.parsemessage(rxBuffer)

				if messagetype == 7:
					self.endComunication()
					self.comunicating = False

			return rxBuffer_forReal

	def send5recieve7(self):
		if self.comunicating == True:
			messagetype = -1

			while (messagetype != 7):
				if messagetype == -1:
					self.prettyprint("Enviando confirmacao de recebimento...", False)
					type5 = self.mensagem.setupmessage(bytearray(),  5)
					self.com.sendData(type5)
				if (messagetype == -2):
					self.prettyprint("Re-enviando confirmacao de recebimento...", False)
					type5 = self.mensagem.setupmessage(bytearray(),  5)
					self.com.sendData(type5)

				messagetype = -2

				rxBuffer, nRx = self.com.getunknownData()
				if nRx != 0:
					payload, messagetype = self.mensagem.parsemessage(rxBuffer)
				if messagetype == 7:
					self.endComunication()
					self.comunicating = False

	def send7(self):
		if self.comunicating == True:
			self.prettyprint("Enviando encerramento", True)
			type7 = self.mensagem.setupmessage(bytearray(),  7)
			self.com.sendData(type7)
			self.endComunication()
			self.comunicating = False

	def send7recieve7(self):
		if self.comunicating == True:
			messagetype = -1
			while (messagetype != 7):
				if messagetype == -1:
					self.prettyprint("Enviando encerramento de comunicação...", False)
					type4 = self.mensagem.setupmessage(bytearray(),  7)
					self.com.sendData(type4)
					messagetype = -2

				elif (messagetype == -2):
					self.prettyprint("Re-enviando encerramento de comunicação...", False)
					type4 = self.mensagem.setupmessage(bytearray(),  7)
					self.com.sendData(type4)

				print("Esperando encerramento de comunicação...")
				rxBuffer, nRx = self.com.getunknownData()
				if nRx > 0:
					payload, messagetype = self.mensagem.parsemessage(rxBuffer)

	def endComunication(self):
		if self.comunicating == True:
			print("-------------------------")
			print("Comunicação encerrada")
			print("-------------------------")
			self.com.disable()