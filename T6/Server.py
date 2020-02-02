import select
import socket

class Server:
    SERVER_ADDR = ("localhost", 7596)
    MAX_DESC = 3
    socket = None

    inStream = list()
    outStream = list()
    clientsInfo = list()

    def __init__(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.setblocking(False)
            self.socket.bind(self.SERVER_ADDR)
            self.socket.listen(self.MAX_DESC)
        except Exception:
            print("[ERROR] Cannot to start. Probably you need to be root-user for launch the app!")

    def run(self):
        self.inStream.append(self.socket)
        print("[INFO] Server is running, use Ctrl+C to stop")
        try:
            while self.inStream:
                readables, writables, exceptional = select.select(self.inStream, self.outStream, self.inStream)
                self.on_event(readables)
        except KeyboardInterrupt:
            self.free_res(self.socket)
            print("[INFO] Server was stopped!")

    def free_res(self, resource):
        if resource in self.outStream:
            self.outStream.remove(resource)
        if resource in self.inStream:
            self.inStream.remove(resource)
        resource.close()
        print('[INFO] Closing connection ' + str(resource))

    def accept_new_client(self, resource):
        connection, client_address = resource.accept()
        connection.setblocking(0)
        self.inStream.append(connection)
        print("New client {address}".format(address=client_address))

    def service_action(self, resource, data):
        pass

    def receive_data(self, resource):
        data = ""
        try:
            data = resource.recv(1024)
        except ConnectionResetError:
            print("[WARNING] Connection was closed!")
        if data:
            data = str(data, encoding="UTF-8")
            print("[TEXT-LOG]: {}".format(data))
            if resource not in self.outStream:
                self.outStream.append(resource)
            if data.find("#[SERVICE]#") != -1:
                self.service_action(resource, data)
            else:
                self.send_answer(data)
        else:
            self.free_res(resource)

    def send_answer(self, message):
        for resource in self.outStream:
            try:
                resource.send(bytes(message, encoding='UTF-8'))
            except OSError:
                self.free_res(resource)

    def on_event(self, readables):
        for resource in readables:
            if resource is self.socket:
                self.accept_new_client(resource)
            else:
                self.receive_data(resource)

if __name__ == '__main__':
    server = Server()
    server.run()
