import threading
import socket
from player import player
# print("Enter host: ")
# host = input()

# print("Enter Port:")
# port = int(input())

# host = socket.gethostbyname(host)

class sock:
    def __init__(self, port):
        self.port = port

    def start(self):
        try:
            s = socket.socket()
            print("socket created")
            s.connect(('127.0.0.1', self.port))
            print(s.recv(1024).decode())
            return s
        except Exception as e:
            print(e)

def playing(p, conn):
    print("thread created successfullyy")
    while 1:
        data = conn.recv(1024).decode()
        print(data)
        if data=="toggle":
            p.toggle()
        elif data=="quit":
            p.quit()
        elif data=="":
            break

    print("thread completed")


if __name__ == "__main__":
    try:
        p = player()
        s = sock(3000)
        conn = s.start()
        if conn==None:
            raise EOFError
        t = threading.Thread(target=playing, args=(p, conn,))
        try:
            t.start()
            p.start(conn)
        except Exception as e:
            print(e)
        conn.close()
        print("App Closed!")
    except Exception as e:
        print(e)

