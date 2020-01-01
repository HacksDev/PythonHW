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



        

router = Router()
router.connectDevice("ETH1", "192.168.5.14/24")
router.addRoute("172.16.0.0/16", "192.168.5.1")
router.addRoute("172.24.0.0/16", "172.16.8.1")
router.showInterfaces()
router.showRoutes()
router.deleteRoute(0)
router.showRoutes()