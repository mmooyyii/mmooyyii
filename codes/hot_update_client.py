import socket

tcpClientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverAddr = ('127.0.0.1', 15000)
tcpClientSocket.connect(serverAddr)

while True:
    a = input("Integer or Update:   ")
    tcpClientSocket.send(a.encode())
    recvData = tcpClientSocket.recv(1024)
    print(recvData)
