#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class formater:

    def __init__(self):
        self.EOP = "!#*)-+".encode()
        self.escape_byte = "&%$".encode()#ou bytes(["111"])
        self.headsize = 3
        self.headtype = 1
        self.headunit = 4
        self.headunittotal = 4
        self.headcrc = 4
        self.CrC = 11

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
        if type(Bytearray) == type(self.EOP):
            # print(Bytearray)
            return Bytearray + self.EOP, len(Bytearray + self.EOP)

        Bytearray = Bytearray[0]
        # print(Bytearray + self.EOP)
        return Bytearray + self.EOP, len(Bytearray + self.EOP)
        # Bytearray = bytearray(Bytearray)
        # print(Bytearray)
        

    def addNumber(self, Bytearray, number, number_type):

        temporary_thing = str(number)

        while len(temporary_thing) < number_type:
            temporary_thing = "0" + temporary_thing

        thing = temporary_thing.encode()

        return (thing + Bytearray)


    def HeadSetup(self, Bytearray, Type, Unit, TotalUnits):

        calcCRC(Bytearray)
        addNumber(Bytearray, calcCRC, self.headcrc)
        Bytearray = self.addNumber(Bytearray, len(Bytearray), self.headsize)
        Bytearray = self.addNumber(Bytearray, TotalUnits, self.headunittotal)
        Bytearray = self.addNumber(Bytearray, Unit, self.headunit)
        Bytearray = self.addNumber(Bytearray, Type, self.headtype)

        length = self.headsize + self.headtype + self.headunit + self.headunittotal

        return Bytearray, length

    def setupmessage(self, Bytearray, Type):
            # Bytearray = Bytearray.encode()
            lista_pacotes = []

            payload, payload_size = self.escape(Bytearray)

            i = 0

            while i*128 <= len(payload):
                if (i + 1)*128 < len(payload):
                    lista_pacotes.append(payload[i*128:(i + 1)*128])
                else:
                    lista_pacotes.append(payload[i*128:])
                i += 1

            lista_pacotes_2 = []

            for i in range(0, len(lista_pacotes)):

                pacote_tratado = self.HeadSetup(lista_pacotes[i], Type, i, len(lista_pacotes))
                pacote_tratado_comeop, tamanho_da_mensagem = self.addEOP(pacote_tratado)

                lista_pacotes_2.append(pacote_tratado_comeop)

            if Type == 4:
                return lista_pacotes_2
            else:
                return lista_pacotes_2[0]


    def extract_head_raw(self, Bytearray):

        lista_coisas_head = [self.headtype, self.headunit, self.headunittotal, self.headsize, self.headcrc]

        payload_and_strings = []

        payload_and_strings.append(Bytearray[sum(lista_coisas_head) :])

        try:
            for i in range(len(lista_coisas_head)):
                if i == 0:
                    payload_and_strings.append(Bytearray[0:lista_coisas_head[i]].decode())
                else:
                    payload_and_strings.append(Bytearray[sum(lista_coisas_head[:i]):sum(lista_coisas_head[:i]) + lista_coisas_head[i]].decode())

            return payload_and_strings

        except UnicodeDecodeError:
            return [b"", "Erro"]

    def to_numeric_if_so(self, string):
        if len(string) == 0:
            return False, -1

        for x in string:
            if x not in "0123456789":
                return False, -1

        return True, int(string)

    def takeHead(self, Bytearray):

        head_strings_and_payload = self.extract_head_raw(Bytearray)

        for string in range(1,len(head_strings_and_payload)):
            boolean, converted = self.to_numeric_if_so(head_strings_and_payload[string])
            if boolean == False:
                return [b"", 0, 6, 0, 0]
            else:
                head_strings_and_payload[string] = converted

        return head_strings_and_payload

    def parsemessage(self, Bytearray):

        payload_eop, message_type, unit, TotalUnits, payload_size = self.takeHead(Bytearray)
        temporary_array = b""

        # step = 5000

        if (message_type == 4) or (message_type == 6):
            print("Parsing {} bytes de mensagem...".format(payload_size))
            for i in range(len(payload_eop)):
                if i < len(payload_eop) - len(self.EOP) + 1:
                    if payload_eop[i:i + len(self.EOP)] == self.EOP:
                        if temporary_array[-3:] == self.escape_byte:
                            print("Stuffing encontrado no index: {}".format(i))
                            temporary_array += bytes([payload_eop[i]])#bytearray(payload_eop[i])
                            temporary_array = temporary_array[:-4]
                        else:
                            if payload_size != i:
                                print("ERRO: tamanho esperado foi de {}, mas o recebido foi de {}".format(payload_size, i + 1))
                                return (b"", -3, unit, TotalUnits)


                            if (message_type == 4):
                                print("Byte de EOP: {}".format(i + 1))
                                return (temporary_array, 4,unit, TotalUnits)


                            else:
                                # print("SUCESSO! byte de EOP: {}".format(i + 1))
                                return (int(temporary_array.decode()), 6, unit, TotalUnits)


                    temporary_array += bytes([payload_eop[i]])#bytearray(payload_eop[i])
                else:
                    if payload_size != i:
                        print("ERRO: tamanho esperado foi de {}, mas o recebido foi de {}".format(payload_size, i + 1))
                        return (b"", -3, unit, TotalUnits)

                        
                    print("ERRO: NAO FOI ENCONTRADO O EOP")
                    return (b"", -3, unit, TotalUnits)
        else:
            return (b"", message_type, unit, TotalUnits)