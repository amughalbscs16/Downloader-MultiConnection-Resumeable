from tcpfunctions import *
from dataextract import *
      
def joinAllChunks(fileWebName,fileChunksList,fileLocPc):
    with open(fileLocPc,'wb') as ffinal:
        for chunkcount in range(len(fileChunksList)):
            with open(os.path.join(fileWebName.split(".")[0], str(chunkcount)),'rb') as f:
                ffinal.write(f.read())
    return;
     
if __name__ == "__main__":
    #step 1: Read command line arguments
    serverHost,resume,connections,tInterval,cType,fileLocWeb,fileWebName,serverDownDirectory,fileLocPc = getCommandLineArguments(sys.argv)
    serverPort = "80"
    #Sockets Equal Number of Connections i.e. number of threads
    #First Extract Header informaton
    fileSize = getHeaderData(serverHost,fileWebName,serverPort,serverDownDirectory)
    print(fileSize)
    #Making Multiple Connections  
    pcSockets = makeTcpIpSockets(connections,serverHost,serverPort)
    #Assign Each Connection to a Thread for downloading
    print(pcSockets)
    #Generate a Request for file download
    fileChunksList = getChunksList(fileSize,recvSize)
    for i in range(connections):
        thread = threading.Thread(target=downloadTcpFile,args=(fileChunksList,i,pcSockets[i],fileWebName,fileLocWeb,serverHost))
        threads.append(thread)
    for i in range(connections):
        threads[i].start()
        threads[i].join()

    print(threads)
    print(fileChunksList)
    print(fileLocPc)
    joinAllChunks(fileWebName,fileChunksList,fileLocPc);



    print ("\ndone")
    

