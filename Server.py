#04.04.2023
#Employment Status - Server 
#Yasin Usman & Olivia McAndrew


#Modules 
import socket #Imported for creating the socket for client-server functionality
import threading  #Imported for multi-threading

#Code
def send_messages_from_server(c):
    #Loop that runs so messages can be sent from the server
    while True:
        #Pulls data from the client
        response_data = c.recv(1024).decode('utf-8')
        # If no response is given the connection ends.
        if not response_data: 
            break       
        #If the response the server gets is "Data added to JSON" then a respective message gets sent
        if response_data == "Data added to JSON":
            print("Data has been added to the JSON file!")
        else:
            print("The connected user says: " + response_data)
            data = response_data.upper()  # Converts the data to uppercase
            print("Sending back in upper case!: " + response_data)
            c.send(response_data.encode('utf-8'))#sends the exact response to the client
    #Closes the connection to the client
    c.close()

def main():
    host = '127.0.0.1' #IP address that is custom created
    port = 8989 #Port number for server to connect to

    s = socket.socket() #Creates a new socket object
    s.bind((host,port)) #Binds the socket to a specific address and port that we mentioned above

    s.listen(1) #listens and accepts the connection
    #prints confirmation response to show the server is running
    print("Employment Status server is running...")
    print("Machine can connect on port 8989")

    while True:
        # Waits for a client to connect and then accepts the connection
        c, addr = s.accept()
        print("Connection from: " + str(addr))

        # Starts a new thread pulling the function send_messages_from_server to handle the client data and responses. A way to encompass Multi-threaded client/server functionality 
        create_client_thread = threading.Thread(target=send_messages_from_server, args=(c,))
        create_client_thread.start()


#Executes main function
if __name__ == '__main__':
    main()
