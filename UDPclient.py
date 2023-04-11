from socket import *
import threading
import os
import time

serverName = '192.168.32.147'
serverPort = 50000
cantConexiones = 10
ext = ".bin"
pktSize = 28897  #bytes

def main(t,a):
    clientSocket = createSocket(t)
    receivePacket(clientSocket,t,a)
    clientSocket.close()
    print("Cliente: "+str(t)+" desconectado")

def createSocket(t):

    clientSocket = socket(AF_INET, SOCK_DGRAM)
    clientSocket.connect((serverName, serverPort))
    clientSocket.sendto(str(t).encode(), (serverName, serverPort))
    print("Cliente "+str(t)+" conectado al servidor")
    return clientSocket    

def receivePacket(clientSocket,t,a):
    file = open("ArchivosRecibidos/prueba"+str(a)+"/Cliente"+str(t)+"-prueba-"+str(cantConexiones)+str(ext), "wb")
    logInfo, serverAddress = clientSocket.recvfrom(pktSize)
    tiempo = 0
    st = time.time()
    while True:
        clientSocket.settimeout(10)
        try:
            data, serverAddress = clientSocket.recvfrom(pktSize)
        except timeout:
            print("Tiempo de espera agotado para el cliente "+str(t))
            break
        if data == b'':
            break
        file.write(data)
    et = time.time()
    tiempo = (et-st)
    clientSocket.close()
    file.close()
    print("Archivo recibido y guardado como", "Cliente"+str(t)+"-prueba"+str(cantConexiones)+str(ext))
    modifyLog(tiempo,t,a,logInfo.decode())

def modifyLog(tiempo,t,a,info):
    print(t)
    d = time.strftime("%Y-%m-%d-%H-%M-%S")
    log = open("ArchivosRecibidos/prueba"+str(a)+"/logs/"+str(d)+"C"+str(t)+"-log.txt", "w")
    if isSuccess(a,t,info):
        info = info + "\n Transferencia realizada exitosamente"
    else:
        info = info + "\n Transferencia fallida"
    info = info + "\n"+str(tiempo)+" ms"
    log.write(info)
    log.close()


def isSuccess(a,t,data):
    data = data.split(":")[1]
    data = data.split("Bytes")[0]
    data = data.strip()
    data = int(data)
    if data == os.stat("ArchivosRecibidos/prueba"+str(a)+"/Cliente"+str(t)+"-prueba-"+str(cantConexiones)+str(ext)).st_size:
        return True
    else:
        return False

if __name__ == '__main__':
    if not os.path.isdir("ArchivosRecibidos"):
        os.mkdir("ArchivosRecibidos")
    num=open("tstnum.txt","r")
    a = int(num.read())
    num=open("tstnum.txt","w")
    num.write(str(a+1))
    os.mkdir("ArchivosRecibidos/prueba"+str(a))
    os.mkdir("ArchivosRecibidos/prueba"+str(a)+"/logs")
    t =[]
    for i in range(cantConexiones):
        thread = threading.Thread(target=main, args=(i,a,))
        thread.start()
        t.append(thread)
    

 
