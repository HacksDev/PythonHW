# Task6.3 (hwx)

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
    clientsInfo = {}

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
            while True:
                readables, writables, exceptional = select.select(self.inStream, self.outStream, self.inStream)
                self.on_event(readables)
        except KeyboardInterrupt:
            self.free_res(self.socket)
            print("[INFO] Server was stopped!")

    def accept_new_client(self, resource):
        connection, client_address = resource.accept()
        connection.setblocking(0)
        self.inStream.append(connection)
        print("New client {address}".format(address=client_address))

    def receive_data(self, resource):
        data = ""
        try:
            data = resource.recv(1024)
        except ConnectionResetError:
            print("[WARNING] Connection was closed!")
            self.send_join_left_message(resource, isJoin=False)
        if data:
            data = str(data, encoding="UTF-8")
            print("[TEXT-LOG]: {}".format(data))

            if resource not in self.outStream:
                self.outStream.append(resource)
            if data.find("#[SERVICE]#") != -1:
                self.service_action(resource, data)
            else:
                self.send_broadcast(data, resource)
        else:
            self.free_res(resource)

    def on_event(self, readables):
        for resource in readables:
            if resource is self.socket:
                self.accept_new_client(resource)
            else:
                self.receive_data(resource)

    def get_resource_id(self, resource):
        if self.outStream.count(resource) > 0:
            return self.outStream.index(resource)
        return -1

    def service_action(self, resource, data):
        data = data[11:]
        raw = data.split(":")
        if raw[0] == "cmd":
            if raw[1] == "userlist":
                self.show_user_list(resource)
            if raw[1] == "whoami":
                self.show_whoami(resource)
            if raw[1] == "help":
                self.show_help(resource)
            if raw[1] == "p":
                self.send_private_message(raw, resource)
            if raw[1] == "cname":
                self.change_user_name(raw, resource)
        else:
            self.add_user_info(raw, resource)

    def add_user_info(self, raw, resource):
        unum = self.get_resource_id(resource)
        isGreeting = 0
        if unum not in self.clientsInfo.keys():
            isGreeting = -1
        info = {raw[0]: raw[1]}
        if unum != -1:
            self.clientsInfo[unum] = info
        if isGreeting == -1:
            self.send_join_left_message(resource, isJoin=True)

    def send_join_left_message(self, resource, isJoin=True):
        nickname = self.clientsInfo[self.get_resource_id(resource)]["NICK"]
        words = " join in" if isJoin else " left from"
        message = "User " + nickname + words + " our chat!"
        self.send_broadcast(message)

    def send_broadcast(self, message, innerres=None):
        for resource in self.outStream:
            try:
                if innerres is not None:
                    if innerres != resource:
                        id = self.outStream.index(innerres)
                        info = self.clientsInfo[id]
                        resource.send(bytes(info["NICK"] + ": " + message, encoding='UTF-8'))
                else:
                    resource.send(bytes(message, encoding='UTF-8'))
            except OSError:
                self.free_res(resource)

    def send_answer_to(self, toclient, message, fromclient=None):
        fromId = self.get_resource_id(fromclient)
        try:
            if fromclient is not None:
                infoFromClient = self.clientsInfo[fromId]
                message = infoFromClient["NICK"] + ": " + message
            if toclient in self.clientsInfo.keys():
                self.outStream[toclient].send(bytes(message, encoding='UTF-8'))
            else:
                self.send_answer_to(fromId, "[SERVER] Your message was not delivered")
        except OSError:
            self.free_res(self.outStream[toclient])

    def show_user_list(self, resource):
        unum = self.get_resource_id(resource)
        if unum != -1:
            result = "\nWho is online: \n"
            for k, v in self.clientsInfo.items():
                result += "#{} -> {}\n".format(k, v["NICK"])
            self.send_answer_to(unum, result)

    def show_help(self, resource):
        unum = self.get_resource_id(resource)
        if unum != -1:
            result = "=====================================\n" \
                     "/userlist - Show all users online\n" \
                     "/help - Get the command list\n" \
                     "/quit - Leave from the hell\n" \
                     "/whoami - Returns your nickname and ID\n" \
                     "/p:ID - Send a private message\n" \
                     "/cname:NEWNAME to change your nickname\n" \
                     "====================================="
            self.send_answer_to(unum, result)

    def show_whoami(self, resource):
        unum = self.get_resource_id(resource)
        try:
            name = self.clientsInfo[unum]["NICK"]
            self.outStream[unum].send(bytes("You are #{} -> {}".format(unum, name), encoding='UTF-8'))
        except OSError:
            self.free_res(self.outStream[unum])

    def send_private_message(self, raw, resource):
        if raw[2] != "" and raw[3] != "":
            self.send_answer_to(int(raw[2]), "(private) " + raw[3], resource)

    def free_res(self, resource):
        if resource in self.outStream:
            self.outStream.remove(resource)
        if resource in self.inStream:
            self.inStream.remove(resource)
        resource.close()
        print('[INFO] Closing connection ' + str(resource))

    def change_user_name(self, raw, resource):
        if raw[2] != "":
            self.add_user_info(["NICK", raw[2]], resource)


if __name__ == '__main__':
    server = Server()
    server.run()
```
