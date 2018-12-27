from tcpfunctions import *
from dataextract import *
from printthreads import *
import shutil
#Join All the chunks of file downloaded into the given directory.
def joinAllChunks(fileWebName,fileChunksList,fileLocPc):
    """
    param fileWebName: The name of file to download - string
    param fileChunksList: The chunks list for each file - 2d list
    param fileLocPc: The location of file to be store on PC - string
    """
    with open(fileLocPc,'wb') as ffinal:
        for chunkcount in range(len(fileChunksList)):
            with open(os.path.join(fileWebName.split(".")[0], str(chunkcount)+".txt"),'rb') as f:
                ffinal.write(f.read())
                f.close()
        ffinal.close()
    return;
    
#Check if all the chunks have been downloaded
def checkAllChunksDownloaded(fileChunksList):
    for chunk in fileChunksList:
        if (not chunk[0]):
            return False;
    return True;
#Assign Chunks sequence to each connection/Thread
def assignThreadChunks(fileChunksList,connections):
    threadChunkList = [[(int(len(fileChunksList)/connections)+1)*i,(int(len(fileChunksList)/connections)+1)*(i+1)-1] for i in range(connections)]
    threadChunkList[-1][1] = len(fileChunksList)
    #print(threadChunkList)
    return threadChunkList;
#Remove the temporary created files after Download Completes
def removeTmpFiles(fileDirectoryPc):
    shutil.rmtree(fileDirectoryPc)
#Resume the file download
def resumeFile(fileDirectoryPc):
    fileChunksList = []
    connections=0
    #Reading the resume file
    with open(fileDirectoryPc,'rb') as resumeFile:
        fileData = bytes("",'utf-8');
        for row in resumeFile:
            fileData+=row;
        fileArray = fileData.decode("ASCII").split("\n")
        connections = int(fileArray[0])
        noChunks = int(fileArray[1])
        fileSize = int(fileArray[2])
        #print(connections)
        #print(noChunks)
        #print(fileSize)
        #Read Whole File and put into a string and then split into fileChunksList,connections,noChunks
        for i in range(3,len(fileArray)):
            if (not fileArray[i] == ""):
                tmpChunk = fileArray[i].split(",")
                fileChunksList.append([tmpChunk[0]=='True',int(tmpChunk[1]),int(tmpChunk[2]),tmpChunk[3]=='True'])
                #print(tmpChunk[0]=='True')
        resumeFile.close()
    return (connections,fileChunksList);