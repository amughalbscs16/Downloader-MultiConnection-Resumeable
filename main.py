import sys
from socket import *
import time
def makeTcpIpSocket():
    return socket(AF_INET,SOCK_STREAM)

def makeUdpIpSocket():
    return socket(AF_INET, SOCK_DGRAM)

def makeTcpConnect(socket,ip,port):
    socket.connect((ip,int(port)));
    
def downloadsingletcp(socket1,down_file_dir,location_to_save):
    return;

def makeTcpRequest(socket,down_file_dir,host):
    socket.send(bytes("GET "+down_file_dir+" HTTP/1.0\r\nHost: "+host+"\r\n\r\n",'utf-8'))

def makeUdpRequest(my_ip,socket,down_file_dir,host):
    socket.bind(("",19995))
    
def downloadTcpFile(socket,down_file):
    count = 0;
    headers = "";
    with open(down_file, 'wb') as f:
    
                while True:
                    data = ""
                    resp = socket.recv(1024)
                    if resp.decode("ASCII") == "":
                        break
                        f.close();
                    if count == 0:
                        count+=1
                        headers = resp.decode("ASCII").split("\r\n\r\n")[0];
                        data = resp.decode("ASCII").split("\r\n\r\n")[1]
                        print(data)
                    f.write(bytes(data,'utf-8'));
        # Close the connection when completed
        
def downloadUdpFile(socket,down_file):
    count = 0;
    headers=""
    with open(down_file, 'wb') as f:
        while True:
            msg, (addr, port) = socket.recvfrom( 100 )
            if resp.decode("ASCII") == "":
                break
            print(msg)
            time.sleep(0.2)
        f.close();
               
if __name__ == "__main__":
    my_ip = "10.7.60.225";
    tcpudp = "u"
    ip="localhost"
    port = "80"
    down_file_dir = "/CNAssignment/filetodownload.txt";
    down_file = down_file_dir.split('/')[-1]
    if (tcpudp == "t"):    
        # print('Number of arguments:', len(sys.argv), 'arguments.')
        # print('Argument List:', str(sys.argv[0]))
        
        #Create Socket TCP
        s = makeTcpIpSocket();
        #Make TCP Connection
        makeTcpConnect(s,ip,port)
        # Generate a Request for file download
        makeTcpRequest(s,down_file_dir,"localhost")
        downloadTcpFile(s,down_file)
        
        
    elif (tcpudp == "u"):
        s = makeUdpIpSocket();
        makeUdpRequest(my_ip,s,down_file_dir,"localhost")
        downloadUdpFile(s,down_file)
                
    s.close()
    print ("\ndone")
    

