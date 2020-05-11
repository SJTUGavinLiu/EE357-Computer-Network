from socket import socket, AF_INET, SOCK_STREAM
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect(('192.168.50.246',800))
request = 'GET /HelloWorld.html'
clientSocket.send(request.encode())
rec = clientSocket.recv(1024)
response = b''
while rec:
    response += rec
    rec = clientSocket.recv(1024)
print(response.decode())