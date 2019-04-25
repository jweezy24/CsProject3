import threading
import csv
import socket
import json

class reciever(threading.Thread):

  def __init__(self, get_sock):
      threading.Thread.__init__(self)
      self.get_sock = get_sock

  def run(self):
      print( "Value send " + str(self.h))


class sender(threading.Thread):

  def __init__(self, sender):
      threading.Thread.__init__(self)
      self.sender = sender

  def run(self):
      print( "Value send " + str(self.h))


class multi_cast_sock(threading.Thread):

    def __init__(self, multi):
        threading.Thread.__init__(self)
        self.multi = multi

    def run(self):
        print( "Value send " + str(self.h))

class main_menu_thread(threading.Thread):

    def __init__(self, getter, sender, multi):
        #I tried to call super instead, but that didn't work
        threading.Thread.__init__(self)
        self.getter = getter
        self.sender = sender
        self.multi = multi
        self.packet = b''
        self.username = self.read_csv()
        self.daemon = True
        self.is_found = False
        self.local_server = ("<broadcast>", 7999)
        if self.username == 'NOT_FOUND':
            raise "USER NOT FOUND"

    def run(self):
        while not self.is_found:
            self.listen()


    def read_csv(self):
        file = open('./config.csv')
        reader = csv.reader(file)
        username = 'NOT_FOUND'
        val_found = False
        for row in reader:
            for item in row:
                if item == 'username':
                    val_found = True
                    continue
                if val_found:
                    username = item
                    val_found = False
        file.close()
        return username

    def send_info(self):
        username = self.read_csv()
        dict = {'op': 'searching', 'username': username, "port":self.getter.getsockname()[1]}
        json_message = json.dumps(dict)
        self.sender.sendto(str(json_message).encode(), self.local_server)

    def __del__(self):
        print("thread deleted")

    def listen(self):
        while True:
            self.send_info()
            message, address = self.multi.recvfrom(1024)
            print(str(message) + "HERE")
            self.packet = message
            if b'match made' in message:
                self.is_found = True

if __name__ == "__main__":
    #init networking stuff
    sock2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock2.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock2.bind(("0.0.0.0",0))
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    MCAST_GRP = '224.0.0.251'
    MCAST_PORT = 5007
    sock3 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    try:
        sock3.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    except AttributeError:
        pass
    sock3.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 32)
    sock3.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_LOOP, 1)

    sock3.bind((MCAST_GRP, MCAST_PORT))
    host = socket.gethostbyname(socket.gethostname())
    sock3.setsockopt(socket.SOL_IP, socket.IP_MULTICAST_IF, socket.inet_aton(host))
    sock3.setsockopt(socket.SOL_IP, socket.IP_ADD_MEMBERSHIP,
                   socket.inet_aton(MCAST_GRP) + socket.inet_aton(host))

    thread1 = main_menu_thread(sock2, sock, sock3)
    thread1.start()
    while not thread1.is_found:
        print(thread1.packet)
    del thread1
