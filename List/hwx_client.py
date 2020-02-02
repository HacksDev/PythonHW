import socket
import threading


class Client:
    SERVER_ADDR = ("localhost", 7596)
    socket = None
    threadRead = None
    threadWrite = None
    threadRunningStatus = None
    nickname = None
    serviceFlag = "#[SERVICE]#"

    def terminate(self):
        self.threadRunningStatus = False
        self.socket.close()
        print("[INFO] Connection was closed! Goodbye!")
        exit(-1)

    def recv_data(self):
        while self.threadRunningStatus:
            while True:
                try:
                    data = self.socket.recv(4096)
                except:
                    break
                if data:
                    print(str(data, encoding="UTF-8"))
                else:
                    self.terminate()

    def send_data(self):
        while self.threadRunningStatus:
            try:
                try:
                    request = input()
                    if request == "/quit": self.terminate()
                    if request != "" and request[0] == "/":
                        self.send_service_data("cmd", request[1:].strip())
                    else:
                        self.socket.send(bytes(request, encoding="UTF-8"))
                except ConnectionResetError:
                    self.terminate()
            except OSError:
                pass

    def send_service_data(self, key, value):
        self.socket.send(bytes(self.serviceFlag + key + ":" + value, encoding="UTF-8"))

    def __init__(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect(self.SERVER_ADDR)
        except Exception:
            print("[ERROR] Server is not available now!")
            exit(-1)

        while self.nickname == None or self.nickname == "":
            self.nickname = input("[INFO] Please type your nickname: ")
        self.send_service_data("NICK", self.nickname)
        print("[INFO] Welcome in our simple TCP chat.\n"
              "[INFO] Type '/quit' if you want to leave!\n"
              "[INFO] Use '/help' for getting help.\n"
              "[INFO] Use '/p:ID:message' syntax to send a private message!\n"
              "[INFO] Use '/userlist' to see USERs and IDs list")
        try:
            self.threadRead = threading.Thread(target=self.recv_data)
            self.threadWrite = threading.Thread(target=self.send_data)
            self.threadRunningStatus = True
            self.threadRead.start()
            self.threadWrite.start()
        except Exception:
            self.socket.close()



if __name__ == '__main__':
    try:
        client = Client()
    except Exception:
        pass
