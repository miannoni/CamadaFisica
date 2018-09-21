
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#####################################################
# Camada Física da Computação
#Carareto
#17/02/2018
#  Aplicação
####################################################

# print("comecou")

# from enlace import *
# from parser1 import *
# import time
# import subprocess
import os
from transmissionhandlers import *
# from formathandler import *
from tkinter import Tk
from tkinter.filedialog import askopenfilename
# import serial.tools.list_ports
# import sendsize
# import cv2


# voce deverá descomentar e configurar a porta com através da qual ira fazer a
# comunicaçao
# Serial Com Port
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports
# se estiver usando windows, o gerenciador de dispositivos informa a porta

# serialName = "/dev/cu.usbmodem146241"           # Ubuntu (variacao de)
# serialName = "/dev/cu.usbmodem144241" # Mac    (variacao de)

# serialName = str(serial.tools.list_ports.comports()[0])[0:5]# Windows(variacao de)
# mensagem = embucetamento('caralho')

# def prettyprint(string, sleep_bool):
#     system("cls")
#     print(string)
#     if sleep_bool == True:
#         time.sleep(0.25)

# def sendnondata(mensagem, com, tipo):
#     com.sendData(mensagem.setupmessage(b"",  tipo))

def main():

    transmit = transmitter(0)
    print("Porta COM aberta com sucesso")

    print("Comunicação aberta")

    ################################ GUI ###############################################

    Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
    local_path = os.path.dirname(os.path.abspath(__file__))
    file = askopenfilename(initialdir = local_path) # show an "Open" dialog box and return the path to the selected file
    filename = ""
    n = len(file)

    while not "/" in filename:
        n -= 1
        filename = str(file[n:])
    filename = filename[1:] #nome do arquivo em uma string
    
    with open(file, "rb") as arquivotemporario:
        txBuffer = bytearray(arquivotemporario.read()) # arquivo em byte array

    #################################### HANDSHAKE START  #################################### 

    # transmit.send7() # teste 1

    transmit.send1recieve2()

    # transmit.send7() # teste 2

    transmit.send3()

    # transmit.send7() # teste 3

    transmit.sendData(txBuffer)

    transmit.send7() # teste 4

    # transmit.send7recieve7()

    transmit.endComunication()

    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
# if __name__ == "__main__":
#     main()
