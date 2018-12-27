
from clearingstuff import *

if __name__ == "__main__":
    #step 1: Read command line arguments
    serverHost,resume,connections,tInterval,cType,fileLocWeb,fileWebName,serverDownDirectory,fileLocPc = getCommandLineArguments(sys.argv)
    serverPort = "80"
    
    #First Extract Header informaton
    fileSize = getHeaderData(serverHost,fileWebName,serverPort,serverDownDirectory)
    
    #Sockets Equal Number of Connections i.e. number of threads
    #Making Multiple Connections  
    pcSockets = makeTcpIpSockets(connections,serverHost,serverPort)

    #Assign Each Connection to a Thread for downloading
    resumePossible=True
    resumePossible=os.path.exists(os.path.join(fileWebName.split(".")[0],"_resume.txt"))

    #Generate a Request for file download
    if not resume or not resumePossible:
        print("Starting Download from Start")
        fileChunksList = getChunksList(fileSize,recvSize)
    else:
        print("Starting the Resume File")
        connections,fileChunksList = resumeFile(os.path.join(fileWebName.split(".")[0],"_resume.txt"))
    
    #Assigning Chunks to Each Thread for Downloading
    threadChunks=assignThreadChunks(fileChunksList,connections)

    #Making the number of bytes downloaded by each connection
    dataDownList = [0 for i in range(connections)]
    
    for i in range(connections):    
        thread = threading.Thread(target=downloadTcpFile,args=(fileChunksList,i,pcSockets[i],fileWebName,fileLocWeb,serverHost,threadChunks[i][0],threadChunks[i][1],dataDownList,fileLocPc,connections))
        threads.append(thread)
    thread = threading.Timer(tInterval,printStats,args=[dataDownList,tInterval,presentTime,prevTime,startTime,fileChunksList])
    threads.append(thread)
    
    #Time Thread
    for i in range(len(threads)):
        threads[i].start()

    for i in range(len(threads)):
        threads[i].join()

        
    if (checkAllChunksDownloaded(fileChunksList)):
        joinAllChunks(fileWebName,fileChunksList,fileLocPc);

    #Cleaning all the temporary chunks stored
    removeTmpFiles(fileWebName.split(".")[0])
    print ("\ndone")
    

