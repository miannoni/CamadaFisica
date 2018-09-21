#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#####################################################
# Camada Física da Computação
#Carareto
#17/02/2018
#  Camada de Enlace
####################################################

# Importa pacote de tempo
import time

# Threads
import threading

# Class
class RX(object):
    """ This class implements methods to handle the reception
        data over the p2p fox protocol
    """
    
    def __init__(self, fisica):
        """ Initializes the TX class
        """
        self.fisica      = fisica
        self.buffer      = bytes(bytearray())
        self.threadStop  = False
        self.threadMutex = True
        self.READLEN     = 1024

    def thread(self): 
        """ RX thread, to send data in parallel with the code
        essa é a funcao executada quando o thread é chamado. 
        """
        timinho = 0
        while not self.threadStop:
            if(self.threadMutex == True):
                # n = time.clock()
                rxTemp, nRx = self.fisica.read(self.READLEN)
                # realtime = time.clock() - n
                # if realtime > timinho:
                #     timinho = realtime
                if (nRx > 0):
                    self.buffer += rxTemp
                # time.sleep(0.01)
        # print("Tempo real recebimento: {}".format(timinho))
        # print("Tamanho da mensagem recebida: {}".format(len(self.buffer)))
        # print("Throughput recebimento: {}".format(len(self.buffer)/(time.clock() - n)))

    def threadStart(self):
        """ Starts RX thread (generate and run)
        """
        self.thread = threading.Thread(target=self.thread, args=())
        self.thread.start()

    def threadKill(self):
        """ Kill RX thread
        """
        self.threadStop = True

    def threadPause(self):
        """ Stops the RX thread to run

        This must be used when manipulating the Rx buffer
        """
        self.threadMutex = False

    def threadResume(self):
        """ Resume the RX thread (after suspended)
        """
        self.threadMutex = True

    def getIsEmpty(self):
        """ Return if the reception buffer is empty
        """
        if(self.getBufferLen() == 0):
            return(True)
        else:
            return(False)

    def getBufferLen(self):
        """ Return the total number of bytes in the reception buffer
        """
        return(len(self.buffer))

    def getAllBuffer(self):
        """ Read ALL reception buffer and clears it
        """
        self.threadPause()
        b = self.buffer[:]
        self.clearBuffer()
        self.threadResume()
        return(b)

    def getBuffer(self, nData):
        """ Remove n data from buffer
        """
        self.threadPause()
        b           = self.buffer[0:nData]
        self.buffer = self.buffer[nData:]
        self.threadResume()
        return(b)

    def getAllData(self):
        """ Read N bytes of data from the reception buffer

        This function blocks until the number of bytes is received
        """
#        temPraLer = self.getBufferLen()
#        print('leu %s ' + str(temPraLer) )
        
        #if self.getBufferLen() < size:
            #print("ERROS!!! TERIA DE LER %s E LEU APENAS %s", (size,temPraLer))
        x = self.getBufferLen()
        dx = 0
        flag = False
        counter = 0

        while (self.getBufferLen() < size) and (counter < 10000):
            time.sleep(0.05)
            counter += 1
#                 
        return(self.getBuffer(size))

    def getunknownData(self):#, size):

        flag = False
        buffer_len_now = self.getBufferLen()

        n = time.clock()
        while (flag == False):
            if (5 < time.clock() - n):
                print("Erro: Time-out!")
                return b""
            if buffer_len_now > 5:
                time.sleep(0.1)  
                if buffer_len_now == self.getBufferLen():
                    flag = True
                buffer_len_now = self.getBufferLen()
            else:
                time.sleep(0.1)
                if buffer_len_now == self.getBufferLen():
                    self.clearBuffer()
                buffer_len_now = self.getBufferLen()

#                 
        return (self.getAllBuffer())



        # x = self.getBufferLen()
        # time.sleep(1)
        
        # while((self.getBufferLen() == 0) or (self.getBufferLen() != x)):
        #     time.sleep(1)
        #     x = self.getBufferLen()
        #     time.sleep(1)

        # print("lenbuffer fora:   ",x)
        # return(self.getBuffer(x))

    def getNData(self, size):
        """ Read N bytes of data from the reception buffer

        This function blocks until the number of bytes is received
        """
#        temPraLer = self.getBufferLen()
#        print('leu %s ' + str(temPraLer) )
        
        #if self.getBufferLen() < size:
            #print("ERROS!!! TERIA DE LER %s E LEU APENAS %s", (size,temPraLer))

        while (self.getBufferLen() < size):
            time.sleep(0.05)
#                 
        return (self.getBuffer(size))

    def getTimedNData(self, size):
        """ Read N bytes of data from the reception buffer

        This function blocks until the number of bytes is received
        """
#        temPraLer = self.getBufferLen()
#        print('leu %s ' + str(temPraLer) )
        
        #if self.getBufferLen() < size:
            #print("ERROS!!! TERIA DE LER %s E LEU APENAS %s", (size,temPraLer))

        counter = 0

        while(self.getBufferLen() < size):
            time.sleep(0.05)
            counter += 1

            if counter >= 20:
                return -1
#                 
        return(self.getBuffer(size))


    def clearBuffer(self):
        """ Clear the reception buffer
        """
        self.buffer = b""
