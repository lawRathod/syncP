import socket
import threading


port = 3000
try:
    s = socket.socket()
    print("socket created")
    s.bind(('', port))
    print("socket binded")
    s.listen(2)
    print("socket listening on port "+str(port))
    while 1:
        c, addr = s.accept()
        print('Got connection from', addr)
        c.send("Connected".encode())
        while True:
            p = input()
            if p==" ":
                c.send("water".encode())
            elif p=="close":
                c.send(p.encode())
                c.close()
                break

except Exception as e:
    print(e)
