import socket
import threading
from player import player

class sock:
    def __init__(self, port):
        self.port = port

    def start(self):
        try:
            s = socket.socket()
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
        sock, conn = s.start()
        t = threading.Thread(target=playing, args=(p, conn,))
        try:
            t.start()
            p.start(conn)
        except Exception as e:
            print(e)
        conn.close()
        sock.close()
        print("App Closed!")
    except Exception as e:
        print(e)











