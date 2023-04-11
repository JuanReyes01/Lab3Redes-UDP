from socket import *
import threading
import os
import time

serverPort = 50000
file_path = "250MB.bin"
pktSize = 28897  #bytes

def main(t):
    serverSocket = createSocket()
    print("Servidor iniciado. Esperando mensajes...")
    while True:
        message, clientAddress = serverSocket.recvfrom(pktSize)
        print("Mensaje recibido de {}: {}".format(clientAddress, message.decode()))
        threading.Thread(target=sendFile, args=(serverSocket, clientAddress,t,)).start()
        t=t+1

def createSocket():
    serverSocket = socket(AF_INET, SOCK_DGRAM)
    serverSocket.bind(('', serverPort))
    return serverSocket

def sendFile(serverSocket, clientAddress,t):
    file = open(file_path, "r+b")
    st = time.time()
    data = file.read(pktSize)
    serverSocket.sendto((file_path+": "+str(str(os.stat(file_path).st_size))+" Bytes").encode(), clientAddress)
    while data:
        serverSocket.sendto(data, clientAddress)
        data = file.read(pktSize)        
    serverSocket.sendto(b'', clientAddress)
    et = time.time()
    file.close()
    modifyLog(et-st,t)
    

def modifyLog(tiempo,t):
    print(t)
    a = time.strftime("%Y-%m-%d-%H-%M-%S")
    log = open("logs/"+str(a)+"C"+str(t)+".txt", "w")
    info = str(str(os.stat(file_path).st_size))+" Bytes"
    info = info + "\n"+str(tiempo)+" ms"
    log.write(info)
    log.close()

if __name__ == '__main__':
    if not os.path.isdir("logs"):
        os.mkdir("logs")
    
    t = 0
    main(t)
    
    
    
    
