import sys
from socket import *
import time;
import os
import threading;
pcSockets=[]
recvSize=4096
threads=[]
chunkcount = 0;
sem = threading.Semaphore()
def makeTcpIpSocket():
    return socket(AF_INET,SOCK_STREAM)

def makeTcpIpSockets(connections,serverHost,serverPort):
    for i in range(connections):
        #Create Socket TCP
        s = makeTcpIpSocket();
        makeTcpConnect(s,serverHost,serverPort)
        pcSockets.append(s)
    return pcSockets;

def makeTcpConnect(socket,serverIp,serverPort):
    socket.connect((serverIp,int(serverPort)));

def closeTcpSockets(pcSockets):
    for s in pcSockets:
        s.close();

    
def getHeaderData(serverHost, serverFile, serverPort, down_file_dir):
    socket = makeTcpIpSocket()
    socket.connect((serverHost,int(serverPort)))
    socket.send(bytes("GET "+down_file_dir+" HTTP/1.1\r\nHost: "+serverHost+"\r\n\r\n",'utf-8'))
    headers = socket.recv(300)
    data = ""
    size=0
    headers = headers.decode("ASCII").split("\r\n\r\n")[0];
    for row in headers.split("\r\n"):
        if (row.split(":")[0]=="Content-Length"):
            size=int(row.split(":")[1])
    socket.close()
    return (size)

def makeTcpRequest(socket,down_file_dir,host,startRange,endRange):
    socket.send(bytes("GET "+down_file_dir+" HTTP/1.1\r\nHost: "+host+"\r\nRange: bytes="+str(startRange)+"-"+str(endRange)+"\r\n\r\n",'utf-8'))

def downloadTcpFile(fileChunksList,thread_id,socket,down_file,down_file_dir,host):
    print(thread_id)
    global chunkcount
    print(fileChunksList)
    #Create new directory for each file to store the chunks
    try:
        # Create target Directory
        os.mkdir(down_file.split(".")[0])
        print("Directory " , dirName ,  " Created ") 
    except FileExistsError:
        print("")
    for i in range(len(fileChunksList)):
        sem.acquire()
        #If Chunk is not downloaded
        if not fileChunksList[i][0] and not fileChunksList[i][3]:
            print("doing")
            makeTcpRequest(socket,down_file_dir,host,fileChunksList[i][1],fileChunksList[i][2])
            fileChunksList[i][3]=True; #Packet In Use
            #Making a folder in the location of .py file to get the chunks of the downloaded file
            with open(os.path.join(down_file.split(".")[0], str(i)+".txt"),'wb') as f:
                resp = socket.recv(recvSize*2)  #Size is double so as to recieve the partial requests fully
                time.sleep(0.02)
                #Removing extra partial content header from the files.
                if (len(resp.decode("ASCII").split("\r\n\r\n"))>1):
                    data = bytes(resp.decode("ASCII").split("\r\n\r\n")[1],'utf-8');
                else:
                    data = resp;
                print(data)
                time.sleep(0.02)
                f.write(data);
                time.sleep(0.02)

            fileChunksList[i][0]=True;
            f.close()
        sem.release()

