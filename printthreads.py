from tcpfunctions import *
from dataextract import *
#Prints the statistics of each connection
def printStats(dataDownList,tInterval,presentTime,prevTime,startTime):
	"""
	param dataDownList: List containing downloaded data of each connection/thread
	oaram tInterval: Time after which the download statistics should print
	param presentTime: The present time
	oaran prevTime: The previous time of printing download statistics
	param startTime: The starting time of download.
	"""
	presentTime = time.time()
	#Total Time Taken
	totalTimeTaken = (presentTime-startTime);
	#Print the statistics if the tInterval seconds time has passed
	if (presentTime - prevTime >= tInterval):
		for i in range(len(dataDownList)):
			print("Download Speed Connection:"+str(i)+" "+str(dataDownList[i]/totalTimeTaken)+" Bytes/s" );
		prevTime=presentTime;
