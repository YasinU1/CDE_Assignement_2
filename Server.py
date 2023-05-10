#04.04.2023
#Employment Status - Server 
#Olivia McAndrew & Yasin Usman


#Modules 
import socket

#Variables&Constants 

#Code
def Main():
    host = '127.0.0.1'
    port = 8989

    s = socket.socket()
    s.bind((host,port))  #connects socket to port

    s.listen(1)
    print("Employment Status server is running...")
    print("Machine can connect on port 8989")
    c, addr = s.accept()     #accepts connection
    print("Connection from: " + str(addr))

    while True:
        data = c.recv(1024).decode('utf-8')     #accepts data from client 
        if not data: 
            break       #ends client connection
        print("the connected user says: " + data)
        data = data.upper()
        print("Sending back in upper case!: " + data)
        c.send(data.encode('utf-8'))    #sends data to the client
    c.close()

if __name__ == '__main__':
    Main()



