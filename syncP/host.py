import time
import socket
import threading
from syncP.player import player
import sys

class sock:
    def __init__(self, port):
        self.port = port

    def start(self):
        try:
            s = socket.socket()
            s.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            print("socket created")
            s.bind(('', self.port))
            print("socket binded")
            s.listen(2)
            print("socket listening on port "+str(self.port))
            print("Waiting for connection")
            c, addr = s.accept()
            print('Got connection from', addr)
            c.send("Connected".encode())
            return (s, c)
        except Exception as e:
            print(e)

def keepAlive(conn):
    while 1:
        try:
            conn.send("check".encode())
            time.sleep(60)
        except Exception as e:
            print(e)
            return


def playing(p, conn):
    print("thread created successfullyy")
    while 1:
        data = conn.recv(1024).decode()
        if data=="toggle":
            p.toggle()
        elif data=="":
            p.quit()
            break

    print("thread completed")

def run(port=3456):
    try:
        p = player()
        s = sock(port)
        s, conn = s.start()
        ka = threading.Thread(target=keepAlive, args=(conn,))
        t = threading.Thread(target=playing, args=(p, conn,))
        ka.start()
        try:
            t.start()
            p.start(conn)
        except Exception as e:
            print(e)
        conn.close()
        s.close()
        print("App Closed!")
    except Exception as e:
        raise e



if __name__ == "__main__":
    args = sys.argv
    port = 3456
    if(args[2]=="--port"):
        if int(args[3]) in range(1000,10000):
            port = int(args[3])
    run(port)






