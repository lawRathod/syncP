import socket
from time import sleep
# print("Enter host: ")
# host = input()

# print("Enter Port:")
# port = int(input())

# host = socket.gethostbyname(host)

try:
    s=socket.socket()
    s.connect(('127.0.0.1', 3000))

    while 1:
        data = s.recv(1024).decode()
        print(data)
        if data=="close":
            break
    s.close()
except Exception as e:
    print(e)

