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
class TX(object):
    """ This class implements methods to handle the transmission
        data over the p2p fox protocol
    """

    def __init__(self, fisica):
        """ Initializes the TX class
        """
        self.fisica      = fisica
        self.buffer      = bytes(bytearray())
        self.transLen    = 0
        self.empty       = True
        self.threadMutex = False
        self.threadStop  = False


    def thread(self):
        """ TX thread, to send data in parallel with the code
        """
        flag = False
        while not self.threadStop:
            if(self.threadMutex):
                n = time.clock()
                self.transLen    = self.fisica.write(self.buffer)
                realtime = time.clock() - n
                self.threadMutex = False
                if flag == False:
                    if self.transLen > 0:
                        print("Tempo real envio: {}".format(realtime))
                        print("Tamanho da mensagem: {}".format(self.transLen))
                        print("Throughput envio: {}".format(self.transLen/(time.clock() - n)))
                        flag = True

    def threadStart(self):
        """ Starts TX thread (generate and run)
        """
        self.thread = threading.Thread(target=self.thread, args=())
        self.thread.start()

    def threadKill(self):
        """ Kill TX thread
        """
        self.threadStop = True

    def threadPause(self):
        """ Stops the TX thread to run

        This must be used when manipulating the tx buffer
        """
        self.threadMutex = False

    def threadResume(self):
        """ Resume the TX thread (after suspended)
        """
        self.threadMutex = True

    def sendBuffer(self, data):
        """ Write a new data to the transmission buffer.
            This function is non blocked.

        This function must be called only after the end
        of transmission, this erase all content of the buffer
        in order to save the new value.
        """
        self.transLen   = 0
        self.buffer = data
        self.threadMutex  = True

    def getBufferLen(self):
        """ Return the total size of bytes in the TX buffer
        """
        return(len(self.buffer))

    def getStatus(self):
        """ Return the last transmission size
        """
        #print("O tamanho transmitido. Impressao fora do thread {}" .format(self.transLen))
        return(self.transLen)
        

    def getIsBussy(self):
        """ Return true if a transmission is ongoing
        """
        return(self.threadMutex)

