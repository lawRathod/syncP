import time
import socket
import argparse
import threading
from syncP.player import player
import sys

class node:
    def __init__(self, conn):
        self.next = None
        self.conn =  conn

class list:
    def __init__(self):
        self.head = None
        self.end = None

    def append(self, node):
        if self.end == None and self.head == None:
            self.head = node
            self.end = self.head
        else:
            self.end.next = node
            self.end = node

    def remove(self, conn):
        cur = self.head
        if conn == cur.conn:
            if self.head == self.end:
                self.head = None
                self.end = self.head
            else:
                self.head = cur.next
            return

        while cur and cur.next:
            if conn == cur.next.conn:
                break
            cur = cur.next

        temp = cur
        if self.end == cur.next:
            self.end = cur
            cur.next = None
        else:
            cur.next = cur.next.next

        del temp





class sock:
    def __init__(self, port):
        self.port = port

    def get_socket(self):
        try:
            s = socket.socket()
            s.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            print("socket created")
            s.bind(('', self.port))
            s.listen(10)
            print("socket binded")
            return s

        except Exception as e:
            raise e


    def start(self, s):
        try:
            print("socket listening on port "+str(self.port))
            print("Waiting for connection")
            c, addr = s.accept()
            print('Got connection from', addr, c.type, c.proto, c.family)
            c.send("Connected".encode())
            return c
        except Exception as e:
            raise e



def now_playing(p, conn, conns_list):
    print("thread created successfuly")
    while 1:
        data = conn.recv(1024).decode()
        if data=="toggle":
            cur = conns_list.head
            while cur:
                if cur.conn != conn:
                    cur.conn.send("toggle".encode())
                cur = cur.next
            p.toggle()
        elif data=="pause":
            cur = conns_list.head
            while cur:
                if cur.conn != conn:
                    cur.conn.send("pause".encode())
                cur = cur.next
            p.pause()
        elif data=="":
            try:
                conns_list.remove(conn)
                print("node removed")
            except Exception as e:
                print(e)
            p.pause()
            cur = conns_list.head
            while cur:
                if cur.conn != conn:
                    cur.conn.send("pause".encode())
                cur = cur.next
            break

    print("thread completed")

def get_connections(s, socket, conns, limit, p):
    for _ in range(limit):
        conn = s.start(socket)
        p.pause()
        cur = conns.head
        while cur:
            cur.conn.send("pause".encode())
            cur = cur.next
        temp = node(conn)
        conns.append(temp)
        try:
            threading.Thread(target=now_playing, args=(p, conn, conns)).start()
        except Exception as e:
            raise e

def run(port=3456):
    try:
        conns_list = list()
        p = player()
        s = sock(port)
        socket = s.get_socket()
        collect_connections_thread = threading.Thread(target=get_connections, args=(s, socket,conns_list,10, p,))
        try:
            collect_connections_thread.start()
        except Exception as e:
            raise e
        p.start(conns_list)
        curr = conns_list.head
        while curr:
            curr.conn.close()
            curr = curr.next
        socket.close()
        sys.exit()
        print("App Closed!")
    except Exception as e:
        raise e



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Start host script")
    port = 3456
    parser.add_argument("--port", help="Specifying port, default 3456", type=int)
    args = parser.parse_args()
    if(args.port):
        if args.port in range(1000,10000):
            port = args.port
    run(port)






