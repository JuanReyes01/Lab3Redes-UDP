from socket import *

serverName = '192.168.32.138'
serverPort = 50000

clientSocket = socket(AF_INET, SOCK_DGRAM)
paquete = open("prueba.jpg",'r+b')
clientSocket.sendall(paquete.encode(), (serverName, serverPort))

msg, serverAddress = clientSocket.recvfrom(2048)
# Print the modified message decoded
print (msg.decode())
# Close the connection
clientSocket.close()
