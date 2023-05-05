#04.04.2023
#Employment Status - Client 
#Olivia McAndrew & Yasin Usman

#Modules 
import socket

#Variables&Constants 

#Code
def Main():
    host = '127.0.0.1'
    port = 8989
    s = socket.socket()

    print("Welcome to Employment record centre!!!")

    menu = int(input(""" 
    Please select an Option:
    1 = Display employment records
    2 = Add data to employment records
    3 = Exit
    """))

    #USER IS DISPLAYED WITH DATA
    if menu == 1:
        print("NOT ready sorry")
    
    # ****************************************************************

    #USER INPUTS DATA
    if menu == 2:
        personCount = 0 
        s = socket.socket()
        try:
            s.connect((host,port))     #connects to server 
            print("  ")
            print("You have conntect to the server.")

        except socket.error as ERROR:
            print(ERROR, "Occured")   
        while True:
            class Person:                   

                def __init__(self):         #class for inputted user.
                    self.fname = input("Your first name: ")
                    self.sname = input("Your last name: ")
                    self.eRecord = input("Your employment status: ")
                
                def displayPerson(self):    #display user inputs.
                    print("First name:", self.fname, "Last name:", self.sname, "Employment Status", self.eRecord) #needs to be prettier



            print("To enter your employment records please enter the information")  
            person = Person()
            person.displayPerson()

            #Needs to be done 
            #Add function to add data to a JSON file
            #Send data to SERVER
            #Add Age
            #Fix server error
            #Input Validation

            continue_ = input("Would you like to add another status") #This can be made a lot pretty
            if continue_.upper() == "N":
                break


    # ****************************************************************  

   
    #USER EXITS PAGE
    if menu ==  3: 
        print("NOT ready sorry")

    # ****************************************************************


    '''
    s = socket.socket()
    s.connect((host,port))   #creates socket with server details

    
    message = input("You are connected to the server. Enter Your Name:")
    while message != 'q':
        s.send(message.encode('utf-8'))

        data = s.recv(1024).decode('utf-8')
        print("Message recevied from server: " + str(data))
        message = input("-->")
    s.close() 
    '''
    

if __name__ == '__main__':
    Main()

