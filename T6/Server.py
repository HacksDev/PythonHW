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
