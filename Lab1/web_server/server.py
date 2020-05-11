# 多线程
from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread
PORT = 800
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', PORT))  # 将TCP欢迎套接字绑定到指定端口
serverSocket.listen(1)  # 最大连接数为1



class Reader(Thread):
    def __init__(self, connection):
        Thread.__init__(self)
        self.connection = connection
    def run(self):
        while True:
            try:
                message = self.connection.recv(1024)  # 获取客户发送的报文
                filename = message.split()[1]
                print(message, filename)
                #print(filename)
                if filename == '/':
                    raise IOError
                f = open(filename[1:])
                outputdata = f.read()
                # Send one HTTP header line into socket
                header = ' HTTP/1.1 200 OK\nConnection: close\nContent-Type: text/html\nContent-Length: %d\n\n' % (
                    len(outputdata))
                self.connection.send(header.encode())
                self.connection.send(outputdata.encode())
                self.connection.close()
            except IOError:
                # Send response message for file not found
                header = ' HTTP/1.1 404 Not Found'
                self.connection.send(header.encode())
                self.connection.close()
                

class Listener(Thread):
    def __init__(self, port):
        Thread.__init__(self)
        self.port = port 
        self.serverSocket = socket(AF_INET, SOCK_STREAM)
        self.serverSocket.bind(('', self.port))
        self.serverSocket.listen(1)
    def run(self):
        while True:
            connectionSocket, addr = self.serverSocket.accept()
            Reader(connectionSocket).start()

server = Listener(808)
server.start()



# 单线程

'''
from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread
PORT = 800
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', PORT))  # 将TCP欢迎套接字绑定到指定端口
serverSocket.listen(1)  # 最大连接数为1
while True:
    print('Ready to serve...')
    connectionSocket, addr = serverSocket.accept()  # 接收到客户连接请求后，建立新的TCP连接套接字
    print(connectionSocket, addr)
    try:
        message = connectionSocket.recv(1024)  # 获取客户发送的报文
        filename = message.split()[1]
        print(message, filename)
        #print(filename)
        if filename == '/':
            raise IOError
        f = open(filename[1:])
        outputdata = f.read()
        # Send one HTTP header line into socket
        header = ' HTTP/1.1 200 OK\nConnection: close\nContent-Type: text/html\nContent-Length: %d\n\n' % (
            len(outputdata))
        connectionSocket.send(header.encode())
        connectionSocket.send(outputdata.encode())
        connectionSocket.close()
    except IOError:
        # Send response message for file not found
        header = ' HTTP/1.1 404 Not Found'
        connectionSocket.send(header.encode())
        connectionSocket.close()
serverSocket.close()
'''