from socket import *
import sys, datetime, time
# import requests
def urlFilter(url):
    with open('UrlsFilter.txt','r',encoding='utf-8') as f:
        lines = f.readlines()
        for url in lines:
            return True
        else:
            return False
if len(sys.argv) <= 1:
    print ('Usage : "python ProxyServer.py server_ip"\n[server_ip : It is the IP Address Of Proxy Server')
    sys.exit(2) 
ServerIp=sys.argv[1]
# Create a server socket, bind it to a port and start listening
tcpSerSock =socket(AF_INET, SOCK_STREAM)
# Fill in start.
tcpSerSock.bind((ServerIp, 80)) # Connect to the webserver on port 80
tcpSerSock.listen(10) #can queue requests up to 5 requests
while True:
    # accept connections from outside (server socket)
    # Fill in end.
    # Start receiving data from the client
    print ('\n\nReady to serve...')
    tcpCliSock, addr = tcpSerSock.accept()
    print ('Received a connection from:', addr)
    message = tcpCliSock.recv(1024)
    """summary
    """    
    # Fill in end.
    print (message)
    # Extract the filename from the given message
    print (message.split()[1])
    if(not urlFilter(message.split()[1]) and message !=""):
        filename = message.split()[1].decode("utf-8").rpartition("/")[2]
        print (filename)
        fileExist = "false"
        filetouse = "/" + filename
        print (filetouse)
        try:
            # Check wether the file exist in the cache
            f = open(filetouse[1:], "rb")#read binary 
            outputdata = f.readlines()
            fileExist = "true"
        # ProxyServer finds a cache hit and generates a response message
        
            tcpCliSock.send(b'HTTP/1.0 200 OK\r\n')
            tcpCliSock.send(b'Content-Type:text/html\r\n')
        # Fill in start.
        # Send the content of the requested file to the client
            for i in range(0, len(outputdata)):
                tcpCliSock.send(outputdata[i])
            f.close()
        # Fill in end.
            print ('Read from cache')
        # Error handling for file not found in cache
        except IOError:
            if fileExist == "false":
            # Create a socket on the proxyserver
                c = socket(AF_INET, SOCK_STREAM)
                # Fill in end.
                hostn = message.split()[4].decode("utf-8")
                print (hostn)
                try:
                    # Connect to the socket to port 80
                    # Fill in start.
                    #srv = getaddrinfo(hostn, 80)
                    c.connect((hostn,80))
                    print("Connected to port 80")
                    # Fill in end.
                    # Create a temporary file on this socket and ask port 80 for the file requested by the client
                    fileobj = c.makefile('w', None)
                    fileobj.write("GET " + message.split()[1].decode("utf-8") + " HTTP/1.0\n\n")
                    fileobj.close()
                    fileobj=c.makefile('rb',None)
                    # Read the response into buffer
                    # Fill in start.
                    buffer=fileobj.readlines()
                    fileobj.close()
                    # Fill in end.
                    # Create a new file in the cache for the requested file.
                    # Also send the response in the buffer to client socket and the corresponding file in the cache
                    tmpFile = open("./cachefile/" + filename,"wb+")#read and write
                    # Fill in start.\
                    for i in range(0, len(buffer)):
                        tmpFile.write(buffer[i])
                        tcpCliSock.send(buffer[i])
                        
                    tmpFile.close()
                    c.close()
                    # Fill in end.
                except:
                    tcpCliSock.send(b'HTTP/1.0 404 sendError\r\n')
                    tcpCliSock.send(b'Content-Type:text/html\r\n')
                    print ("Illegal request")
            else:
                # Close the client and the server sockets
                tcpCliSock.close()
    else :
        # HTTP response message for file not found
        tcpCliSock.send(b'HTTP/1.0 404 sendError\r\n')
        tcpCliSock.send(b'Content-Type:text/html\r\n')
        
        # Close the client and the server sockets
        tcpCliSock.close()