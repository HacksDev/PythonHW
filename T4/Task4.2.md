# Task4.2

## Task description

Написать класс router.
Должен иметь методы добавить/удалить/вывести список ip address.
Должен иметь методы добавить/удалить/вывести список ip routes.

Есть маршруты к непосредственно-подключенным сетям:
если у устройства есть ip-adress ```192.168.5.14/24``` на интерфейсе eth1,
значит у него должен быть маршрут:
к сети ```192.168.5.0/24``` через eth1 или через ```192.168.5.14```.

Если мы хотим добавить маршрут к какой-нибудь удаленной сети,
то надо проверять доступен ли gateway.

Например мы можем добавить маршрут к 172.16.0.0/16 через gateway
```192.168.5.132```, только если у нас уже есть маршрут до ```192.168.5.132```.

Если же мы попытаемся добавить маршрут до какой-либо сети через gateway,
до которого у нас пока еще нет маршрута, то должен вылетать exception.

Например:
Добавляем ip-address ```192.168.5.14/24 eth1```.
Добавляем маршрут до ```172.16.0.0/16``` через ```192.168.5.1``` - ok.
Добавляем маршрут до ```172.24.0.0/16``` через ```192.168.8.1``` - exception.
Добавляем маршрут до ```172.24.0.0/16``` через ```172.16.8.1``` - ok.

Итого - 1 интерфейс и 3 маршрута в таблице.


## Report

[File 4.2](Task4.2.py)   

```python
self.interfaceTable # Таблица интерфейсов
self.rountingTable # Таблица маршрутов
```

```python
def isValidAddress(self, address): # Максимально упрощенная валидация корректности IPv4 адреса в десятичном виде 
def getNetwork(self, address): # Получить IPv4 адрес сети по IPv4 узла и маске
def __init__(self, rountingTable = list(), interfaceTable = dict()): # Конструктор
def showInterfaces(self): # Вывести таблицу интерфейсов
def showRoutes(self): # Вывести таблицу маршрутов
def connectDevice(self, interface, address): # Подключить узел к порту (интерфейсу)
def deleteDevice(self, interface): # Отключить узел от порта
def addRoute(self, tar, to, check = True): # Добавить маршрут
def deleteRoute(self, num): # Удалить маршру
```

```python
router = Router()
router.connectDevice("ETH1", "192.168.5.14/24")
router.addRoute("172.16.0.0/16", "192.168.5.1")
router.addRoute("172.24.0.0/16", "172.16.8.1")
# router.addRoute("172.24.0.0/16", "192.168.8.1") -> Exception("Gateway not found!")
router.showInterfaces()
router.showRoutes()

>>> ======================Interfaces Table=======================
>>> Port ETH1     -> IP Address 192.168.5.14/24
>>> Port ETH2     -> IP Address
>>> Port ETH3     -> IP Address
>>> Port ETH4     -> IP Address
>>> 
>>> =============================================================
>>> ------------------------ROUTING TABLE------------------------
>>> =============================================================
>>> #0   Target: 192.168.5.14/24    -> To: ETH1
>>> #1   Target: 172.16.0.0/16      -> To: 192.168.5.1/24
>>> #2   Target: 172.24.0.0/16      -> To: 172.16.8.1/16
```


```python
class Router:
    """Router emulation class"""

    def isValidAddress(self, address):
        return True if (len(address.split(".")) == 4) else False

    def getNetwork(self, address):
        if (len(address.split("/")) > 1):
            mask = int(address.split('/')[1])
            ip = address.split('/')[0]
            return ".".join([ \
                str(int(a)&m) \
                for a, m in list( \
                    zip(ip.split("."),
                    [int((("1"*mask).ljust(32, "0"))[8*x:(8*(x+1))],2) for x in range(4)]))]
                ) + "/" + str(mask)
        return 0
            

    def __init__(self, rountingTable = list(), interfaceTable = dict()):
        self.routingTable = rountingTable
        self.interfaceTable = interfaceTable
        self.interfaceTable["ETH1"] = ""
        self.interfaceTable["ETH2"] = ""
        self.interfaceTable["ETH3"] = ""
        self.interfaceTable["ETH4"] = ""

    def showInterfaces(self):
        print("======================Interfaces Table=======================")
        for interface, device in self.interfaceTable.items():
            print("Port {:<8} -> IP Address {}".format(interface, device))

    def showRoutes(self):
        print("=============================================================")
        print("------------------------ROUTING TABLE------------------------")
        print("=============================================================")
        i = 0
        for elem in self.routingTable:
            print("#{:<3} Target: {:<18} -> To: {}".format(i, elem["target"], elem["to"]))
            i += 1

    def connectDevice(self, interface, address):
        if (self.interfaceTable.get(interface, -1) != -1):
            self.interfaceTable[interface] = address
            self.addRoute(address, interface, False)
        else: 
            print("Interface not found!")

    def deleteDevice(self, interface):
        self.connectDevice(interface, "")

    def addRoute(self, tar, to, check = True):
        mask = ""
        if (check):
            exist = False
            for elem in self.routingTable:
                mask = elem["target"][-3::]
                if (self.isValidAddress(elem["target"]) and \
                    self.getNetwork(elem["target"]) == \
                    self.getNetwork(to + mask)
                    ):
                    exist = True
                    break
                mask = elem["to"][-3::]
                if (self.isValidAddress(elem["to"]) and \
                    self.getNetwork(elem["to"]) == \
                    self.getNetwork(to + mask)
                    ):
                    exist = True
                    break
            if (not exist): raise Exception("Gateway not found!")
        route = dict()
        route["target"] = tar
        route["to"] = to + mask
        self.routingTable.append(route)
       

    def deleteRoute(self, num):
        self.routingTable.pop(num)
```
