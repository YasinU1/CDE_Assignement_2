#04.04.2023
#Employment Status - Client 
#Olivia McAndrew & Yasin Usman

#Modules 
import socket
import json
import re  # Regular Expression module for input validation
from prettytable import PrettyTable

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
    
    try:  # Try to connect to the server
        s.connect((host,port))
        print("\nConnected to the server successfully.")
    except socket.error as ERROR:  # If the server is not connected, it shows an error message and ends the program
        print("Error occurred while connecting to the server: ", ERROR)
        return

    while True:
        print("\nWelcome to Employment record centre!!!")
        # Input validation for the main menu: only allows 1, 2 or 3.
        while True:
            menu = input(""" 
            Please select an Option:
            1 = Display employment records
            2 = Add data to employment records
            3 = Exit
            """)
            # Here we use the regex pattern to check if the input is valid (1, 2, or 3)
            if re.match("^[123]$", menu):
                menu = int(menu)  # Convert the validated input to integer
                break
            else:
                print("Invalid input. Please enter 1, 2 or 3.")


        #USER IS DISPLAYED WITH DATA
        if menu == 1:
            # Display employment records
            try:
                # Making the path to the file OS agnostic
                with open('EmploymentRecords.json', 'r') as f:
                    records = json.load(f)
            except (FileNotFoundError, json.JSONDecodeError) as e:
                # Detailed error message here for no records
                print(f"Error occurred while trying to read records: {str(e)}")
                print("No records found.")
                continue

            # Display data in a table format
            table = PrettyTable(['First Name', 'Last Name', 'Age', 'Employment Status'])
            for record in records:
                table.add_row([record['First name'], record['Last name'], record['Age'], record['Employment Status']])
            print(table)

            # Add an option to search for a person after displaying records
            while True:
                display_records(records)
                choice = input("Type 'search' to search for a person, or type 'exit' to return to the menu: ")
                if choice.lower() == "search":
                    search_person(records)
                elif choice.lower() == "exit":
                    break
        # ****************************************************************

        #USER INPUTS DATA
        elif menu == 2:
            while True:
                print("To enter your employment records please enter the information")  
                person = Person()
                person_dict = person.to_dict()

                # Display the new record in a pretty table for confirmation
                table = PrettyTable(['First Name', 'Last Name', 'Age', 'Employment Status'])
                table.add_row([person_dict['First name'], person_dict['Last name'], person_dict['Age'], person_dict['Employment Status']])
                print("\nHere is your new record:")
                print(table)

                confirm = input("Is this correct? (y/n): ")
                if confirm.lower() not in ['y', 'yes']:
                    print("Please add the record again.")
                    continue
                
                # save data to json file
                try:
                    # Making the path to the file OS agnostic
                    with open('EmploymentRecords.json', 'r') as f:
                        people = json.load(f)
                except (FileNotFoundError, json.JSONDecodeError) as e:
                    print(f"Error occurred while trying to read records: {str(e)}")
                    people = []

                people.append(person.to_dict())

                # Try/except block for file write operation
                try:
                    with open('EmploymentRecords.json', 'w') as f:
                        json.dump(people, f)
                        s.send("Data added to JSON".encode('utf-8')) # Notify the server about the addition
                except Exception as e:
                    print(f"Error occurred while trying to write to file: {str(e)}")

                continue_ = input("Would you like to add another status: y or n ") 
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

def search_person(records):
    while True:
        search_term = input("Enter the first name of the person to search for or 'exit' to return to display all records: ")
        if search_term.lower() == "exit":
            break
        found_records = [record for record in records if record['First name'].lower() == search_term.lower()]
    
        if found_records:
            table = PrettyTable(['First Name', 'Last Name', 'Age', 'Employment Status'])
            for record in found_records:
                table.add_row([record['First name'], record['Last name'], record['Age'], record['Employment Status']])
            print(table)
        else:
            print("No person found with the given first name.")
            continue

def display_records(records):
    table = PrettyTable(['First Name', 'Last Name', 'Age', 'Employment Status'])
    for record in records:
        table.add_row([record['First name'], record['Last name'], record['Age'], record['Employment Status']])
    print(table)

if __name__ == '__main__':
    Main()


    #Needs to be done 
    #GUI

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
    


