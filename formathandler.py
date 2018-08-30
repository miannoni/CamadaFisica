#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class formater:

    def __init__(self):
        self.EOP = "!#*)-+".encode()
        self.escape_byte = "&%$".encode()#ou bytes(["111"])
        self.headsize = 8
        self.headtype = 1

    def tobyte(self,anything):
        return bytes([anything])

    def escape(self, Bytearray):
        temporary_array = b""#bytearray()
        # print(self.escape_byte)

        for i in range(len(Bytearray) - len(self.EOP)):
            # print(temporary_array)
            if Bytearray[i:i + len(self.EOP)] == self.EOP:
                print("add escape byte no index: {}".format(i))
                temporary_array += self.escape_byte
                temporary_array += bytes([Bytearray[i]])
            else:
                # print("add no escape byte")
                # print(Bytearray[i])
                temporary_array += bytes([Bytearray[i]])#bytearray(Bytearray[i])

        temporary_array += Bytearray[- (len(self.EOP)  ):]
        # print(temporary_array)
        return temporary_array, len(temporary_array)

    def addEOP(self, Bytearray):
        # Bytearray = bytearray(Bytearray)
        return Bytearray + self.EOP, len(Bytearray + self.EOP)

    def addNumber(self, Bytearray, number, number_type):

        temporary_thing = str(number)

        while len(temporary_thing) < number_type:
            temporary_thing = "0" + temporary_thing

        thing = temporary_thing.encode()

        return (thing + Bytearray)



    def HeadSetup(self, Bytearray, Type):

        Bytearray = self.addNumber(Bytearray, len(Bytearray), self.headsize)
        Bytearray = self.addNumber(Bytearray, Type, self.headtype)
        length = self.headsize + self.headtype

        return Bytearray, length

    def setupmessage(self, Bytearray, Type):
        # Bytearray = Bytearray.encode()
        payload, payload_size = self.escape(Bytearray)

        head_payload, head_payload_size = self.HeadSetup(payload, Type)

        head_payload_eop, head_payload_eop_size = self.addEOP(head_payload)

        print("payload size: {}".format(payload_size))
        print("head + payload size: {}".format(head_payload_size))
        print("head + payload + eop size: {}".format(head_payload_eop_size))

        print("Overhead: " + str(round((payload_size/head_payload_eop_size)*100, 2)) + "%")
        return head_payload_eop

    def takeHead(self, Bytearray):

        # Array com o tipo da mensagem tornado em string
        mt_bytearray = Bytearray[0:self.headtype].decode()

        # Check para ver se algum caracter nao é numerico
        for x in mt_bytearray:
            if x not in "0123456789":
                return b"", 0, 6

        # Tornando em int a string com o tipo da mensagem
        message_type = int(mt_bytearray)

        # Se forem dados, continue parseando
        if message_type == 4:

            # Array com o tamanho do payload da mensagem tornado em string
            hs_bytearray = Bytearray[self.headtype:self.headsize + self.headtype].decode()

            # Check para ver se algum caracter nao é numerico
            for x in mt_bytearray:
                if x not in "0123456789":
                    return b"", 0, 6

            # Tornando em int a string com o tipo da mensagem
            head_size = int(hs_bytearray)

            # Extraindo o payload e EOP de acordo com informações no head e type
            new_array = Bytearray[self.headsize + self.headtype:]

        else:
            return b"", 0, message_type

        return new_array, head_size, message_type

    def parsemessage(self, Bytearray):

        payload_eop, payload_size, message_type = self.takeHead(Bytearray)
        temporary_array = b""

        # step = 5000

        if message_type == 4:
            print("Parsing {} bytes de mensagem...".format(payload_size))
            for i in range(len(payload_eop)):
                if i < len(payload_eop) - len(self.EOP) + 1:
                    # if i%step == 0:
                    #     if i + step >= payload_size:
                    #         print('lendo bytes {} a {}'.format(i ,payload_size))
                    #     else:
                    #         print('lendo bytes {} a {}'.format(i ,i+500))
                    if payload_eop[i:i + len(self.EOP)] == self.EOP:
                        if temporary_array[-3:] == self.escape_byte:
                            print("Stuffing encontrado no index: {}".format(i))
                            temporary_array += bytes([payload_eop[i]])#bytearray(payload_eop[i])
                            temporary_array = temporary_array[:-4]
                        else:
                            if payload_size != i:
                                print("ERRO: tamanho esperado foi de {}, mas o recebido foi de {}".format(payload_size, i + 1))
                                return (b"", -3)
                            print("SUCESSO! byte de EOP: {}".format(i + 1))
                            return (temporary_array, 4)
                    temporary_array += bytes([payload_eop[i]])#bytearray(payload_eop[i])
                else:
                    if payload_size != i:
                        print("ERRO: tamanho esperado foi de {}, mas o recebido foi de {}".format(payload_size, i + 1))
                        return (b"", -3)
                    print("ERRO: NAO FOI ENCONTRADO O EOP")
                    return (b"", -3)
        else:
            return (b"", message_type)