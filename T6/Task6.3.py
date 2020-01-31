from tkinter import *
 
class Server:
    def __init__(self):
        root = Tk()
        root.title("Message Server")
        ConnectionWindow(root)
        windowHeight = 130
        windowWidth = 400
        w = root.winfo_screenwidth() # ширина экрана
        h = root.winfo_screenheight() # высота экрана
        w = w//2 # середина экрана
        h = h//2 
        w = w - windowWidth//2 # смещение от середины
        h = h - windowHeight//2
        root.geometry('{}x{}+{}+{}'.format(windowWidth, windowHeight, w, h))
        root.mainloop()


class ConnectionWindow:
    def __init__(self, master):
        self.label = Label(
            text="Server configuration:",
            font="Ubuntu 14"
        ).pack(side=TOP)

        self.inputContainer = Frame()
        self.inputContainer.pack(side=TOP)

        self.addressLabel = LabelFrame(self.inputContainer, text="Address", padx=5, pady=5)
        self.address = Entry(self.addressLabel, width=40)
        self.address.insert(0, "127.0.0.1")
        self.address.pack()
        self.addressLabel.pack(padx=10, pady=10, side=LEFT)

        self.portLabel = LabelFrame(self.inputContainer, text="Port", padx=5, pady=5)
        self.portLabel.pack(padx=10, pady=10, side=RIGHT)
        self.port = Entry(self.portLabel)
        self.port.insert(0, "8725")
        self.port.pack()

        self.runBtn = Button(text="Run server!")
        self.runBtn.pack()


if __name__ == "__main__":
    serv = Server()

