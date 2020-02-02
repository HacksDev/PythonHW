import socket
import threading


class Client:
    SERVER_ADDR = ("localhost", 7596)
    socket = None
    threadRead = None
    threadWrite = None
    threadRunningStatus = None
    nickname = None

    def terminate(self):
        self.threadRunningStatus = False
        self.socket.close()
        print("[INFO] Connection was closed! Goodbye!")

    def recv_data(self):
        while self.threadRunningStatus:
            while True:
                try:
                    data = self.socket.recv(4096)
                except:
                    break
                if data:
                    print("Received data: ", str(data, encoding="UTF-8"))
                else:
                    self.terminate()

    def send_data(self):
        while self.threadRunningStatus:
            try:
                request = input()
                while request != ".quit":
                    self.socket.send(bytes(request, encoding="UTF-8"))
                    request = input()
                self.terminate()
            except Exception:
                pass

    def __init__(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect(self.SERVER_ADDR)
        except Exception:
            print("[ERROR] Server is not available now!")
            exit(-1)
        while self.nickname == None or self.nickname == "":
            self.nickname = input("[INFO] Please type your nickname:")
        self.socket.send(bytes("NICK:"+self.nickname, encoding="UTF-8"))
        print("[INFO] Welcome in our simple TCP chat.\n Type '.quit' if you want to leave!")
        try:
            self.threadRead = threading.Thread(target=self.recv_data)
            self.threadWrite = threading.Thread(target=self.send_data)
            self.threadRunningStatus = True
            self.threadRead.start()
            self.threadWrite.start()
        except Exception:
            self.socket.close()



if __name__ == '__main__':
    client = Client()
