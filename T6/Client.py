import socket
import threading


class Client:
    SERVER_ADDR = ("localhost", 7596)
    socket = None
    threadRead = None
    threadWrite = None

    def terminate(self):
        print("[INFO] Connection was closed!")

    def recv_data(self):
        while True:
            try:
                data = self.socket.recv(4096)
            except:
                self.terminate()
                break
            if data:
                print("Received data: ", data)

    def send_data(self):
        request = input()
        while request != ".quit":
            self.socket.send(bytes(request, encoding="UTF-8"))
            request = input()
        self.socket.close()

    def __init__(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect(self.SERVER_ADDR)
        except Exception:
            print("[ERROR] Server is not available now!")
            exit(-1)
        print("[INFO] Welcome in our simple TCP chat.\n Type !'.quit'! if you want to leave!")
        try:
            self.threadRead = threading.Thread(target=self.recv_data)
            self.threadWrite = threading.Thread(target=self.send_data)
            self.threadRead.start()
            self.threadWrite.start()
        except Exception:
            self.socket.close()
            print("[INFO] Connection was closed!")


if __name__ == '__main__':
    client = Client()
