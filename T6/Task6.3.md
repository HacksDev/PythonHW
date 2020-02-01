# Task6.3 (hwx) [IN PROCESS]

## Task description

TCP чат.
Написать сервер и клиент для простого чата-мессенджера.
1. Возможность посмотреть список участников.
2. Возможность написать конкретному участнику.
3. Выйти из чата.
4. Отправить сообщение всем участникам.

Задание творческое. Примените свою фантазию для ответа на вопрос, как это должно выглядеть.


## Report


[File 6.3 Client](Client.py)  

```python
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

```


[File 6.3 Server](Server.py)  

```python
import select
import socket

class Server:
    SERVER_ADDR = ("localhost", 7596)
    MAX_DESC = 3
    socket = None

    inStream = list()
    outStream = list()

    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setblocking(False)
        self.socket.bind(self.SERVER_ADDR)
        self.socket.listen(self.MAX_DESC)

    def run(self):
        self.inStream.append(self.socket)
        print("[INFO] Server is running, use Ctrl+C to stop")
        try:
            while self.inStream:
                readables, writables, exceptional = select.select(self.inStream, self.outStream, self.inStream)
                self.on_event(readables)
        except KeyboardInterrupt:
            self.free_res(self.socket)
            print("[INFO] Server stopped!")

    def free_res(self, resource):
        if resource in self.outStream:
            self.outStream.remove(resource)
        if resource in self.inStream:
            self.inStream.remove(resource)
        resource.close()
        print('closing connection ' + str(resource))

    def on_event(self, readables):
        for resource in readables:
            if resource is self.socket:
                connection, client_address = resource.accept()
                connection.setblocking(0)
                self.inStream.append(connection)
                print("new connection from {address}".format(address=client_address))
            else:
                data = ""
                try:
                    data = resource.recv(1024)
                except ConnectionResetError:
                    pass
                if data:
                    print("getting data: {}".format(str(data)))
                    if resource not in self.outStream:
                        self.outStream.append(resource)
                    self.send_all(str(data, encoding="UTF-8"))
                else:
                    self.free_res(resource)

    def send_all(self, message):
        for resource in self.outStream:
            try:
                resource.send(bytes(message, encoding='UTF-8'))
            except OSError:
                self.free_res(resource)

if __name__ == '__main__':
    server = Server()
    server.run()

```
