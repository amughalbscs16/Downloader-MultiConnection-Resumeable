from tcpfunctions import *
from dataextract import *

def printStats(dataDownList,tInterval,presentTime,prevTime,startTime):
	presentTime = time.time()
	totalTimeTaken = (presentTime-startTime);
	if (presentTime - prevTime >= tInterval):
		for i in range(len(dataDownList)):
			print("Download Speed Connection:"+str(i)+" "+str(dataDownList[i]/totalTimeTaken)+" Bytes/s" );
		prevTime=presentTime;
