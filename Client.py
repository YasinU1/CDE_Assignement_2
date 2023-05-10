#04.04.2023
#Employment Status - Client 
#Olivia McAndrew & Yasin Usman

#Modules 
import socket
import json


class Person:                   
    def __init__(self):         #class for inputted user.
        self.fname = input("Your first name: ")
        self.sname = input("Your last name: ")
        self.age = input("Your Age: ")
        self.eRecord = input("Your employment status, y or n: ")
    
    def displayPerson(self):    #display user inputs.
        print("First name:", self.fname, "Last name:", self.sname, "Age:", self.age, "Employment Status", self.eRecord)


    def to_dict(self):   #return dictionary representation of person
        return {
            'First name': self.fname,
            'Last name': self.sname,
            'Age': self.age,
            'Employment Status': self.eRecord
        }


#Variables&Constants 

#Code
def Main():
    host = '127.0.0.1'
    port = 8989
    s = socket.socket()

    while True:
        print("\nWelcome to Employment record centre!!!")

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
        elif menu == 2:
            s = socket.socket()
            try:
                s.connect((host,port))     #connects to server 
                print("  ")
                print("You have connected to the server.")

            except socket.error as ERROR:
                print(ERROR, "Occured")   
                continue
                
            while True:
                print("To enter your employment records please enter the information")  
                person = Person()
                person.displayPerson()
                
                # save data to json file
                try:
                    with open('EmploymentRecords.json', 'r') as f:
                        people = json.load(f)
                except (FileNotFoundError, json.JSONDecodeError):
                    people = []

                people.append(person.to_dict())

                with open('EmploymentRecords.json', 'w') as f:
                    json.dump(people, f)
                continue_ = input("Would you like to add another status: ") 
                if continue_.upper() == "N":
                    break

        # ****************************************************************  

        #USER EXITS PAGE
        elif menu ==  3: 
            print("NOT ready sorry")
            break

        else:
            print("Invalid option selected, please try again.")

    s.close() 

if __name__ == '__main__':
    Main()
    
    #Needs to be done 
    #Send data to SERVER
    #Add Age
    #Fix server error
    #Input Validation

    # '''
    # s = socket.socket()
    # s.connect((host,port))   #creates socket with server details

    
    # message = input("You are connected to the server. Enter Your Name:")
    # while message != 'q':
    #     s.send(message.encode('utf-8'))

    #     data = s.recv(1024).decode('utf-8')
    #     print("Message recevied from server: " + str(data))
    #     message = input("-->")
    # s.close() 
    # '''
    


