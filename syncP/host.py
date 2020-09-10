import time
import socket
import argparse
import threading
from syncP.player import player
import sys

# node struct for linked list, param: connection
class node:
    def __init__(self, conn):
        self.next = None
        self.conn =  conn

# linked list implementation and routines, maintaining end and head
class list:
    def __init__(self):
        self.head = None
        self.end = None

    # Append method to add node to the end of the list
    def append(self, node):
        if self.end == None and self.head == None:
            self.head = node
            self.end = self.head
        else:
            self.end.next = node
            self.end = node

    # Remove method to search the connectiont to remove and remove from the list
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




# socket class to instantiate socket connection and start accepting new connections to the socker
class sock:

    # Specifying port to use for binding the socket
    def __init__(self, port):
        self.port = port

    # Get socket binds socket to a port and return the socket
    def get_socket(self):
        try:
            s = socket.socket()
            s.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            print("\nSocket created")
            s.bind(('', self.port))
            s.listen(10)
            print("Socket binded\n")
            return s

        except Exception as e:
            print(e)

    # Start starts a new connection and returns the connections object
    def start(self, s, p):
        try:
            print("\nSocket listening on port "+str(self.port))
            print("\nWaiting for connection")
            c, addr = s.accept()
            # print('Got connection from', addr, c.type, c.proto, c.family)
            c.send(("sync: "+str(p.player.time_pos)).encode())
            return c
        except Exception as e:
            print(e)


# Now playing accepts connection and the connections list, spawned for every connection and listens for messages 
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
        elif data=="" or data=="quit":
            try:
                conns_list.remove(conn)
                print("Cliend Disconnected")
            except Exception as e:
                print(e)
            p.pause()
            cur = conns_list.head
            while cur:
                if cur.conn != conn:
                    cur.conn.send("pause".encode())
                cur = cur.next
            break


# Get Connection runs in a separate thread and listens for new connection until the limit of connection is over
# Params: sock class object, socket binded to the port by the sock class, limit (default: 5) of connection, player object
def get_connections(s, socket, conns, limit, p):
    print("Limit of connections set to ", str(limit))
    for _ in range(limit):
        conn = s.start(socket, p)
        p.pause()
        cur = conns.head
        while cur:
            cur.conn.send("pause".encode())
            cur = cur.next
        temp = node(conn)
        conns.append(temp)
        print("\nNew client joined\n")
        try:
            threading.Thread(target=now_playing, args=(p, conn, conns)).start()
        except Exception as e:
            print(e)

# Run is the parent method called in the very beginning to orchestrate everything
# Params: Port specified on cli, limit specified on cli or defaults 3456 and 5
def run(port, limit):
    try:
        conns_list = list()
        p = player()
        s = sock(port)
        socket = s.get_socket()
        collect_connections_thread = threading.Thread(target=get_connections, args=(s, socket,conns_list, limit, p,))
        try:
            collect_connections_thread.start()
        except Exception as e:
            print(e)
        p.start(conns_list)
        curr = conns_list.head
        while curr:
            curr.conn.close()
            curr = curr.next
        socket.close()
        sys.exit()
        print("App Closed!")
    except Exception as e:
        print(e)



# Entry if script called separately
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Start host script")
    parser.add_argument("--port", help="Specifying port, default 3456", type=int)
    parser.add_argument("--limit", help="Specifying limit of clients, dafault 5", type=int)
    args = parser.parse_args()

    port = args.port if args.port else 3456
    limit = args.limit if args.limit else 5

    run(port, limit)













