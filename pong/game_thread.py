import threading

class reciever(threading.Thread):

  def __init__(self, get_sock):
      threading.Thread.__init__(self)
      self.get_sock = get_sock

  def run(self):
      print( "Value send " + str(self.h))


class sender(threading.Thread):

  def __init__(self, get_sock):
      threading.Thread.__init__(self)
      self.get_sock = get_sock

  def run(self):
      print( "Value send " + str(self.h))


class multi_cast_sock(Threading.thread):
    
    def __init__(self, get_sock):
        threading.Thread.__init__(self)
        self.get_sock = get_sock

    def run(self):
        print( "Value send " + str(self.h))


if __name__ == "__main__":
    thread1 = reciever(1)
    thread1.start()
