#04.04.2023
#Employment Status - Client 
#Olivia McAndrew & Yasin Usman

#Modules 
import socket
import json
import re  # Regular Expression module for input validation
from prettytable import PrettyTable
import os  # Added for file handling in a cross-platform manner

class Person:                   
    def __init__(self):         # Class for inputted user.
        # Input validation for first name: allows only letters and it should not be empty.
        while True:
            self.fname = input("Your first name: ")
            if re.match("^[A-Za-z]*$", self.fname) and self.fname:
                break
            else:
                print("Invalid input. Please enter a valid first name.")

        # Input validation for last name: allows only letters and it should not be empty.
        while True:
            self.sname = input("Your last name: ")
            if re.match("^[A-Za-z]*$", self.sname) and self.sname:
                break
            else:
                print("Invalid input. Please enter a valid last name.")

        # Input validation for age: allows only numbers and age should be between 1 to 120.
        while True:
            self.age = input("Your Age: ")
            if re.match("^[1-9][0-9]?$|^120$", self.age):
                break
            else:
                print("Invalid input. Please enter a valid age between 1 to 120.")

        # Input validation for employment status: allows only 'y' or 'n'.
        while True:
            self.eRecord = input("Your employment status, y or n: ")
            if re.match("^[ynYN]$", self.eRecord):
                break
            else:
                print("Invalid input. Please enter 'y' for yes or 'n' for no.")

    def displayPerson(self):    # Display user inputs.
        print("\nFirst name:", self.fname, "\nLast name:", self.sname, "\nAge:", self.age, "\nEmployment Status", self.eRecord)

    def to_dict(self):   # Return dictionary representation of person
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
    


