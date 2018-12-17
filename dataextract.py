from tcpfunctions import *


def getCommandLineArguments(arguments):
    connections=0
    tInterval=0;
    cType=""
    fileLocWeb = "";
    fileWebName = "";
    fileLocPc = "";
    filePcName = "";
    serverHost="";
    serverDownDirectory="";
    for i in range(0,len(arguments)):
        #Parse each of the flag and store the data corresponding to that.
        if arguments[i]=="-r":
            resume=True;

        if arguments[i]=="-n":
            connections=int(arguments[i+1])

        if arguments[i]=="-i":
            tInterval=float(arguments[i+1])

        if arguments[i]=="-c":
            cType = arguments[i+1]

        if arguments[i]=="-f":
            fileLocWeb = arguments[i+1];
            fileWebName = fileLocWeb.split('/')[-1]
            for i in range(3,len(fileLocWeb.split("/"))):
                serverDownDirectory+="/"+fileLocWeb.split("/")[i];
            
        if arguments[i]=="-o":
            fileLocPc = arguments[i+1]
            filePcName = fileWebName
            if fileLocPc == ".":
                fileLocPc = sys.path[0]
                fileLocPc+="\\"+filePcName

    serverHost=fileLocWeb.split("://")[1].split("/")[0];
    return (serverHost,resume,connections,tInterval,cType,fileLocWeb,fileWebName,serverDownDirectory,fileLocPc)

def getChunksList(dataSize,recvSize):
    #Downloaded,start,end,InUse
    chunkList=[[False,j*recvSize,(j+1)*recvSize-1,False] for j in range((int(dataSize/recvSize))+1)]
    return chunkList;
