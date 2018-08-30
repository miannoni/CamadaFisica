from tkinter import *
import appsender
import appreciever

class Application:
    def __init__(self, master=None):
        self.widget1 = Frame(master)
        self.widget1.pack()

        def callback_and_hide(button):
            callback()
            button.grid_forget()

        self.enviar = Button(self.widget1)
        self.enviar["text"] = "Enviar"
        self.enviar["font"] = ("Calibri", "9")
        self.enviar["width"] = 10
        self.enviar.bind("<Button-1>", self.enviado)
        self.enviar.pack(side=LEFT)

        self.receber = Button(self.widget1)
        self.receber["text"] = "Receber"
        self.receber["font"] = ("Calibri", "9")
        self.receber["width"] = 10
        self.receber.bind("<Button-1>", self.recebido)
        self.receber.pack(side=LEFT)

        self.msg = Label(self.widget1, text="")
        self.msg["font"] = ("Calibri", "9", "italic")
  
    # def enviado(self, event):
    #     self.msg.grid_forget()
    #     self.msg['text']="Enviando..."
    #     self.msg.pack ()

    #     appsender.main()

    def enviado(self, event):
        self.msg.grid_forget()
        self.msg['text']="Enviando..."
        self.msg.pack ()

        appsender.main()

    def recebido(self, event):
        self.msg['text']="Recebendo..."
        self.msg.pack()

        appreciever.main()
  
root = Tk()
root.geometry("400x300")
Application(root)
root.mainloop()