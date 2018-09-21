
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#####################################################
# Camada Física da Computação
#Carareto
#17/02/2018
#  Aplicação
####################################################

# print("comecou")

from enlace import *
from formathandler import *

import time
import serial.tools.list_ports
from os import system
from transmissionhandlers import *

# voce deverá descomentar e configurar a porta com através da qual ira fazer a
# comunicaçao
# Serial Com Port
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports
# se estiver usando windows, o gerenciador de dispositivos informa a porta

# serialName = "/dev/cu.usbmodem146241"           # Ubuntu (variacao de)
# serialName = "/dev/cu.usbmodem144241" # Mac    (variacao de)

def main():

    # serialName = str(serial.tools.list_ports.comports()[1])
    # mensagem = formater()

    # if (len(serialName) > 3):

        # serialName = serialName[0:5]

        # Inicializa enlace ... variavel com possui todos os metodos e propriedades do enlace, que funciona em threading
        # com = enlace(serialName)
        # message = message()

        transmit = transmitter(1)

        print("Abrindo porta COM")

        # Ativa comunicacao
        # com.enable()

        #verificar que a comunicação foi aberta
        print("Abrindo comunicação")

        #########################################################################################

        transmit.recieve1()

        transmit.send2recieve3()

        data = transmit.recieveData()

        transmit.send5recieve7()

        transmit.send7()

        with open("Saved_File.png", "wb+") as image:
            f = image.write(data)

        transmit.endComunication()


    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
# if __name__ == "__main__":
#     main()
