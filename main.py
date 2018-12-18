from tcpfunctions import *
from dataextract import *
from printthreads import *

def joinAllChunks(fileWebName,fileChunksList,fileLocPc):
    with open(fileLocPc,'wb') as ffinal:
        for chunkcount in range(len(fileChunksList)):
            with open(os.path.join(fileWebName.split(".")[0], str(chunkcount)+".txt"),'rb') as f:
                ffinal.write(f.read())
    return;

def checkAllChunksDownloaded(fileChunksList):
    for chunk in fileChunksList:
        if (not chunk[0]):
            return False;
    return True;

def assignThreadChunks(fileChunksList,connections):
    threadChunkList = [[(int(len(fileChunksList)/connections)+1)*i,(int(len(fileChunksList)/connections)+1)*(i+1)-1] for i in range(connections)]
    threadChunkList[-1][1] = len(fileChunksList)
    #print(threadChunkList)
    return threadChunkList;

def resumeFile(fileDirectoryPc):
    return;

if __name__ == "__main__":
    #step 1: Read command line arguments
    serverHost,resume,connections,tInterval,cType,fileLocWeb,fileWebName,serverDownDirectory,fileLocPc = getCommandLineArguments(sys.argv)
    serverPort = "80"
    #Sockets Equal Number of Connections i.e. number of threads
    #First Extract Header informaton
    fileSize = getHeaderData(serverHost,fileWebName,serverPort,serverDownDirectory)
    #print(fileSize)
    #Making Multiple Connections  
    pcSockets = makeTcpIpSockets(connections,serverHost,serverPort)
    #Assign Each Connection to a Thread for downloading
    #print(pcSockets)
    #Generate a Request for file download
    fileChunksList = getChunksList(fileSize,recvSize)
    #Assigning Chunks to Each Thread for Downloading
    threadChunks=assignThreadChunks(fileChunksList,connections)
    #Making the number of bytes downloaded by each connection
    dataDownList = [0 for i in range(connections)]
    for i in range(connections):
        thread = threading.Thread(target=printStats,args=(dataDownList,tInterval,presentTime,prevTime,startTime))
        threads.append(thread)
        thread = threading.Thread(target=downloadTcpFile,args=(fileChunksList,i,pcSockets[i],fileWebName,fileLocWeb,serverHost,threadChunks[i][0],threadChunks[i][1],dataDownList,fileLocPc,connections))
        threads.append(thread)
    #Time Thread
    thread = threading.Thread(target=printStats,args=(dataDownList,tInterval,presentTime,prevTime,startTime))
    threads.append(thread)
    
    for i in range(2*connections+1):
        threads[i].start()
        threads[i].join()
        
    if (checkAllChunksDownloaded(fileChunksList)):
        joinAllChunks(fileWebName,fileChunksList,fileLocPc);

    print ("\ndone")
    

