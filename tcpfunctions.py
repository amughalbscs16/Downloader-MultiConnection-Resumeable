import sys
from socket import *
import time;
import os
import threading;
pcSockets=[]
recvSize=1024
threads=[]
dataDownList=[]
threadChunks=[]
sem = threading.Semaphore()
startTime = time.time();
prevTime = time.time();
presentTime = time.time();
resumeStoreCount=0
chunksDone=[[],[],[],[],[]]

def makeTcpIpSocket():
    """
    input: Nothing
    return: Create a TCP IP Socket
    """
    return socket(AF_INET,SOCK_STREAM)

def makeTcpIpSockets(connections,serverHost,serverPort):
    for i in range(connections):
        #Create Socket TCP
        s = makeTcpIpSocket();
        makeTcpConnect(s,serverHost,serverPort)
        pcSockets.append(s)
    return pcSockets;
#Connect each socket to Ip/Port of Server
def makeTcpConnect(socket,serverIp,serverPort):
    socket.connect((serverIp,int(serverPort)));
#Close the socket connections
def closeTcpSockets(pcSockets):
    for s in pcSockets:
        s.close();
#Get Header data i.e. specifically the Size of File
def getHeaderData(serverHost, serverFile, serverPort, down_file_dir):
    socket = makeTcpIpSocket()
    socket.connect((serverHost,int(serverPort)))
    socket.send(bytes("GET "+down_file_dir+" HTTP/1.1\r\nHost: "+serverHost+"\r\n\r\n",'utf-8'))
    headers = socket.recv(2048)
    data = ""
    size=0
    #print(headers)
    headers = headers.decode("ASCII").split("\r\n\r\n")[0];
    for row in headers.split("\r\n"):
        if (row.split(":")[0]=="Content-Length"):
            size=int(row.split(":")[1])
    socket.close()
    return (size)

#Makes TCP Request for each connection
def makeTcpRequest(socket,down_file_dir,host,startRange,endRange):
    socket.send(bytes("GET "+down_file_dir+" HTTP/1.1\r\nHost: "+host+"\r\nRange: bytes="+str(startRange)+"-"+str(endRange)+"\r\n\r\n",'utf-8'))
#Downloads the chunks of File from Start-End Chunks as Assigned In the Start
def downloadTcpFile(fileChunksList,thread_id,socket,down_file,down_file_dir,host,startChunkNo,endChunkNo,dataDownList,fileLocPc,connections):
    global resumeStoreCount
    #Create new directory for each file to store the chunks
    try:
        # Create target Directory
        os.mkdir(down_file.split(".")[0])
    #If File Exists Do not create new file simply pass to next Code
    except FileExistsError:
        pass
    #If the chunk is not assigned to this thread
    if (startChunkNo>=len(fileChunksList)):
        return;
    #If the chunk is not assigned to this thread
    if (endChunkNo>=len(fileChunksList)):
        endChunkNo=len(fileChunksList)-1;
    #Make Tcp Download Request from Start of First Chunk - End of Final Assigned Chunk
    makeTcpRequest(socket,down_file_dir,host,fileChunksList[startChunkNo][1],fileChunksList[endChunkNo][2])
    for i in range(startChunkNo,endChunkNo+1):
        if not fileChunksList[i][0] and not fileChunksList[i][3]:
            fileChunksList[i][3]=True; #Packet In Use
            #Making a folder in the location of .py file to get the chunks of the downloaded file
            with open(os.path.join(down_file.split(".")[0], str(i)+".txt"),'wb') as f:
                resp = socket.recv(recvSize)  #Size is double so as to recieve the partial requests fully
                #Removing extra partial content header from the files.
                if (len(resp.decode("ASCII").split("\r\n\r\n"))>1):
                    data = bytes(resp.decode("ASCII").split("\r\n\r\n")[1],'utf-8');
                else:
                    data = resp;
                #print(data)
                f.write(data);
                dataDownList[thread_id]+=len(data);
            fileChunksList[i][0]=True;
            resumeStoreCount+=1
            #Makes a Resume file after each 100 chunks recieved.
            #Implement Resume Part
            if (resumeStoreCount==100):
                #Store the whole into a file
                #Connections No
                #Into the File Directory
                #named _resume.txt
                with open(os.path.join(down_file.split(".")[0],"_resume.txt"),'wb') as resumeFile:
                    resumeFile.write(bytes(str(connections)+"\n",'utf-8')) #No Of Connections for resume
                    resumeFile.write(bytes(str(len(fileChunksList))+"\n",'utf-8')) #Length of Chunks List to read again so No Chunk is Missed
                    resumeFile.write(bytes(str(fileChunksList[-1][2])+"\n",'utf-8'))     #The FileSize/Content Length
                    for chunk in fileChunksList:
                        resumeFile.write(bytes(str(chunk[0])+","+str(chunk[1])+","+str(chunk[2])+","+str(chunk[3])+"\n",'utf-8'))
                    resumeFile.close()

                resumeStoreCount=0;
            f.close()
        #print("Thread id"+str(thread_id))

