from enum import Enum
import random
import socket
import binascii


class DNSData:
    class OpcodeType(Enum):
        DEFAULT = 0
        INVERSE = 1
        STATUS = 2

    class RCODEType(Enum):
        SUCCESS = 0
        WRONG_FORMAT = 1
        DNS_ERROR = 2
        NAME_NOT_EXIST = 3
        REQ_NOT_SUPPORT = 4
        SECURITY_RULES = 5

    class QueryType(Enum):
        TEST = 0
        A = 1
        AAAA = 28
        CNAME = 5
        DNAME = 39
        MX = 15
        NS = 2
        PTR = 12

    class QCLASSType(Enum):
        INTERNET = 1

    OPCODE_TYPE = OpcodeType
    RCODE_TYPE = RCODEType
    QUERY_TYPE = QueryType
    QCLASS_TYPE = QCLASSType

    ID = None
    QR = None  # 0 for request, 1 for response
    Opcode = None
    AA = None  # 0 for not authoritative, 1 for authoritative
    TC = None  # 1 if message more than 512b
    RD = None  # 1 - get an answer recursively without any steps, just an answer
    RA = None  # Recursion Available
    Z = None  # Must be 0. Flag for future :)
    RCODE = None

    QDCOUNT = None  # Amount of requests.
    ANCOUNT = None  # Amount of answers.
    NSCOUNT = None  # Amount of records in the Authority Section
    ARCOUNT = None  # Amount of records in the Additional Record Section

    # #############################################3
    QNAME = None
    QTYPE = None
    QCLASS = None

    def generate_id(self):
        return self.n2xs(random.randint(1, 65535), pos=4)

    def set_request_head(self, numQuestion):
        self.ID = self.generate_id()
        self.QR = "0"
        self.Opcode = self.n2xs(self.OPCODE_TYPE.DEFAULT.value, 4)
        self.AA = "0"
        self.TC = "0"
        self.RD = "1"
        self.RA = "0"
        self.Z = self.n2xs(0, 3)
        self.RCODE = self.n2xs(self.RCODE_TYPE.SUCCESS.value, 4)

        flagseq = self.QR + self.Opcode + self.AA + self.TC + self.RD + self.RA + self.Z + self.RCODE
        flags = str(int(flagseq[0:4])) + str(int(flagseq[4:8])) + \
                str(int(flagseq[8:12])) + str(int(flagseq[12:16]))

        self.QDCOUNT = self.n2xs(numQuestion, 4)
        self.ANCOUNT = "0000"
        self.NSCOUNT = "0000"
        self.ARCOUNT = "0000"
        return self.ID + flags + self.QDCOUNT + self.ANCOUNT + self.NSCOUNT + self.ARCOUNT

    def set_request_body(self, questions):
        self.QNAME = ""
        for qname in questions:
            for word in qname.split('.'):
                length = self.n2xs(len(word))
                self.QNAME += length
                self.QNAME += "".join([self.c2xs(c) for c in word])
        self.QNAME += "00"  # 00 - END QNAME

        self.QTYPE = self.n2xs(self.QUERY_TYPE.A.value, 4)
        self.QCLASS = self.n2xs(self.QCLASS_TYPE.INTERNET.value, 4)
        return self.QNAME + self.QTYPE + self.QCLASS

    def set_response_head(self):
        pass

    def assemble_request(self, question):
        return (self.set_request_head(len(question)) +
                self.set_request_body(question))

    def assemble_response(self):
        pass

    def parse_request_data(self, string):
        pass

    def read_names(self, string, position):
        hostname = ""
        while True:
            if (string[position: position + 2] == "c0" or
                    string[position: position + 2] == "C0"):
                nextStep = int(int(string[position + 2: position + 4], 16) * 2)
                hostname += self.read_names(string, nextStep)[0]
                position += 4
                break

            if string[position: position + 2] == "":
                break

            buff = int(string[position: position + 2], 16)
            if buff != 0:
                tempName = string[position + 2: position + 2 + buff * 2]
                hostname += "".join([chr(int(tempName[ch:ch + 2], 16)) for ch in range(0, len(tempName), 2)])
                hostname += "."
                position = position + 2 + buff * 2
            else:
                break
        return [hostname, position]

    @staticmethod
    def parse_response_data(answer):
        data = DNSData()
        data.ID = answer[0:4]
        flags = bin(int(answer[4:8], 16))[2:]
        data.QR = flags[0]
        data.Opcode = data.OPCODE_TYPE(int(flags[1:5], 2))
        data.AA = data.bs2i2s(flags[5], 2)
        data.TC = data.bs2i2s(flags[6], 2)
        data.RD = data.bs2i2s(flags[7], 2)
        data.RA = data.bs2i2s(flags[8], 2)
        data.Z = str(flags[9:12])
        data.RCODE = data.RCODE_TYPE(int(flags[12:16], 2))

        data.QDCOUNT = answer[8:12]
        data.ANCOUNT = answer[12:16]
        data.NSCOUNT = answer[16:20]
        data.ARCOUNT = answer[20:24]

        # ########### Black magic
        hostname = ""
        counter = 24
        for r in range(int(data.QDCOUNT)):
            hostname, counter = data.read_names(answer, counter)
            counter += 2

        data.QTYPE = data.QUERY_TYPE(int(answer[counter: counter + 4], 2))
        counter += 4
        data.QCLASS = data.QCLASS_TYPE(int(answer[counter: counter + 4], 2))
        counter += 4

        hosts = []
        for r in range(int(data.ANCOUNT)):
            hostname, counter = data.read_names(answer, counter)
            QTYPE = data.QUERY_TYPE(int(answer[counter: counter + 4], 2))
            counter += 4
            QCLASS = data.QCLASS_TYPE(int(answer[counter: counter + 4], 2))
            counter += 4
            TTL = int(answer[counter: counter + 8], 16)
            counter += 8

            if (QTYPE == data.QTYPE.A):
                dataLength = int(answer[counter: counter + 4], 16)
                counter += 4
                tempName = answer[counter: counter + 2 * dataLength]
                counter += 2 * dataLength
                IP = ".".join([ str(int(tempName[ch:ch + 2], 16)) for ch in range(0, len(tempName), 2)])
                hosts.append({"hostname": hostname, "QTYPE": QTYPE, "QCLASS": QCLASS, "TTL": TTL, "IP": IP})


        print(hosts)

        return data

    # Number to heX String
    def n2xs(self, num, pos=2):
        return ("{:0" + str(pos) + "x}").format(num)

    # Char TO heX String
    def c2xs(self, ch):
        return hex(ord(ch))[-2:]

    # Binary String to String thru Integer
    def bs2i2s(self, enter, base):
        return str(int(enter, base))


class DNSServer:
    PORT = 53
    DNS_SERVERS = ['8.8.8.8', '8.8.4.4']
    ADDRESS_SPACE = socket.AF_INET
    PROTO = socket.SOCK_DGRAM
    socket = None

    def __init__(self):
        self.socket = socket.socket(self.ADDRESS_SPACE, self.PROTO)

    def send_data_to(self, query):
        try:
            self.socket.sendto(binascii.unhexlify(query), ("8.8.8.8", 53))
            data, _ = self.socket.recvfrom(4096)
        finally:
            self.socket.close()
        return binascii.hexlify(data).decode("utf-8")

    def send_request(self):
        dnsData = DNSData()
        query = dnsData.assemble_request(['google.com'])
        responseDnsData = DNSData().parse_response_data(self.send_data_to(query))


serv = DNSServer()
serv.send_request()
