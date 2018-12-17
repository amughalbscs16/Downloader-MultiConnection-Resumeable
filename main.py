import sys
from socket import *
import time;
filesize=0;
def makeTcpIpSocket():
    return socket(AF_INET,SOCK_STREAM)

def makeTcpConnect(socket,ip,port):
    socket.connect((ip,int(port)));

def makeTcpRequest(socket,down_file_dir,host):
    socket.send(bytes("GET "+down_file_dir+" HTTP/1.0\r\nHost: "+host+"\r\nRange: bytes=10-\r\n\r\n",'utf-8'))

def downloadTcpFile(socket,down_file):
    count = 0;
    headers = "";
    with open(down_file, 'wb') as f:
        resp = socket.recv(1024)
        print(resp)
        data = ""
        headers = resp.decode("ASCII").split("\r\n\r\n")[0];
        filesize=int(headers.split("\r\n")[6].split(":")[1])
        print(filesize)
        return 0;
    """    while True:
                    if resp.decode("ASCII") == "":
                        break
                        f.close();
                    if count == 0:
                        count+=1
                        
                        data = resp.decode("ASCII").split("\r\n\r\n")[1]
                        data = bytes(data,'utf-8')
                    print(data)
                    f.write(data);
        """
        # Close the connection when completed

if __name__ == "__main__":
    #step 1: Read command line arguments
    print(sys.argv)
    resume=False;
    connections=0
    tInterval=0;
    cType=""
    filelocweb = "";
    filewebname = "";
    filelocpc = "";
    filepcname = "";
    for i in range(0,len(sys.argv)):
        #Parse each of the flag and store the data corresponding to that.
        if sys.argv[i]=="-r":
            resume=True;
        if sys.argv[i]=="-n":
            connections=int(sys.argv[i+1])
        if sys.argv[i]=="-i":
            tInterval=float(sys.argv[i+1])
        if sys.argv[i]=="-c":
            cType = sys.argv[i+1]
        if sys.argv[i]=="-f":
            filelocweb = sys.argv[i+1];
            filewebname = filelocweb.split('/')[-1]
        if sys.argv[i]=="-o":
            filelocpc = sys.argv[i+1]
            filepcname = filelocpc.split('/')[-1]
    print(resume,connections,tInterval,cType,filelocpc,filelocweb);
    #Step 2: Using them to proper fixes
    pcIp = "10.7.60.225"
    serverHost=filelocweb.split("://")[1].split("/")[0];
    serverPort = "80"
    pcSockets = []
    port=15000;
    #First Extract Header informaton


    #Making Multiple Connections
    if (cType.lower() == "tcp"):    
        print("TCP")
        for i in range(connections):
            #Create Socket TCP
            s = makeTcpIpSocket();

            makeTcpConnect(s,serverHost,serverPort)
            pcSockets.append(s)
            #Make TCP Connection
            port+=1;
        #Assign Each Connection to a Thread for downloading

        #Generate a Request for file download
        for s in pcSockets:
            s.close();
        
    """        
    elif (tcpudp == "u"):
        s = makeUdpIpSocket();
        makeUdpRequest(my_ip,s,down_file_dir,ip)
        s.bind(("localhost",81))
        downloadUdpFile(s,down_file)
    """
    s.close()
    print ("\ndone")
    

