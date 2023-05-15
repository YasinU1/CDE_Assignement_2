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

    s = socket.socket()  # Creates a new socket object
    s.bind((host,port))  # Binds the socket to a specific address and port

    s.listen(1)  # Configures the socket to accept connections
    print("Employment Status server is running...")
    print("Machine can connect on port 8989")
    c, addr = s.accept()     # Waits for a client to connect and then accepts the connection
    print("Connection from: " + str(addr))

    while True:
        data = c.recv(1024).decode('utf-8')     # Receives data from the client
        if not data: 
            break       # Ends the connection if no data is received
        
        # If the client sent a specific message, output a message accordingly.
        if data == "Data added to JSON":
            print("Data has been added to the JSON file!")
        else:
            print("The connected user says: " + data)
            data = data.upper()  # Converts the data to uppercase
            print("Sending back in upper case!: " + data)
            c.send(data.encode('utf-8'))    # Sends the uppercase data back to the client

    c.close()  # Closes the connection to the client

if __name__ == '__main__':
    Main()