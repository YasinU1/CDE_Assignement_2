#04.04.2023
#Employment Status - Client 
#Olivia McAndrew & Yasin Usman

#Modules 
import socket #Imported for creating the socket for client-server functionality
import json #Module to make handling JSON easy.
import re  #REGEX module for input validation to create parameters
from prettytable import PrettyTable #table module to nicely present our JSON data

#Classes and Functions
class Person:                   
    def __init__(self):         # Class for inputted user.
        # Input validation for first name using REGEX: allows only letters and it should not be empty or have any spaces.
        while True:
            self.first_name = input("Your first name: ")
            if re.match("^[A-Za-z]*$", self.first_name) and self.first_name:
                break
            else:
                print("Invalid input. Please enter a valid first name.")

        # Input validation for last name using REGEX: allows only letters and it should not be empty or have any spaces.
        while True:
            self.surname = input("Your last name: ")
            if re.match("^[A-Za-z]*$", self.surname) and self.surname:
                break
            else:
                print("Invalid input. Please enter a valid last name.")

        # Input validation for age using REGEX: allows only numbers and age should be between 1 to 120.
        while True:
            self.age = input("Your Age: ")
            if re.match("^[1-9][0-9]?$|^100$", self.age):
                break
            else:
                print("Invalid input. Please enter a valid age between 1 to 100.")

        # Input validation for employment status using REGEX: allows only 'y' or 'n'.
        while True:
            self.employment_record = input("Your employment status, y or n: ")
            if re.match("^[ynYN]$", self.employment_record):
                break
            else:
                print("Invalid input. Please enter 'y' for yes or 'n' for no.")

    # Display user inputs.
    def displayPerson(self):
        print("\nFirst name:", self.first_name, "\nLast name:", self.surname, "\nAge:", self.age, "\nEmployment Status", self.employment_record)

    # Return dictionary representation of person similar to JSON
    def to_dict(self):   
        return {
            'First name': self.first_name,
            'Last name': self.surname,
            'Age': self.age,
            'Employment Status': self.employment_record
        }

# Function used in menu option 1 to search person within records
def search_person_within_records(records):
    while True:
        # Prompts the user to search using the exact first name of the person
        search_term = input("Enter the first name of the person to search for or 'exit' to return to display all records: ")
        #Checks if user has entered exit to break the loop, however if first name begins with exit it breaks.
        if search_term.lower() == "exit":
            break
        #For loop and if statment to search for first name, 
        found_records = []
        for record in records:
            if record['First name'].lower() == search_term.lower():
                found_records.append(record)
        # Checks if any of the same records of first name are found, if yes, displays pretty table of matching results, similar to main display table.
        if found_records:
            #Creates table using the inputs as column titles.
            table = PrettyTable(['First Name', 'Last Name', 'Age', 'Employment Status'])
            #For loop to add each found result in a table from the JSON file
            for record in found_records:
                table.add_row([record['First name'], record['Last name'], record['Age'], record['Employment Status']])
            print(table)
        else:
            #If no result is found prints this message
            print("No person found with the given first name.")
            continue

# ****************************************************************  

        #MAIN CLIENT FUNCTION CODE

# ****************************************************************  
def Main():
    #Same host port and socket code as server to create that connection
    host = '127.0.0.1'
    port = 8989
    s = socket.socket()
    
    # Conenction to server
    try: 
        s.connect((host,port))
        print("\nConnected to the server successfully.")
    # If the server is not connected, it shows an error message and ends the program
    except socket.error as ERROR:  
        print("Error occurred while connecting to the server: ", ERROR)
        return

# ****************************************************************  

        # USER WELCOME MENU

# ****************************************************************  
 
    while True:
        print("\nWelcome to Employment record centre!!!")
        while True:
            menu = input(""" 
            Please select an Option:
            1 = Display employment records
            2 = Add data to employment records
            3 = Exit
            """)
            # Input validation for the main menu so it only allows 1, 2 or 3 as an input, specifed using REGEX
            if re.match("^[123]$", menu):
                menu = int(menu)  # Convert the validated input to integer
                break
            else:
                print("Invalid input. Please enter 1, 2 or 3.")

# ****************************************************************************  

        # USER OPTION 1 - USER CAN DISPLAY AND SEARCH WITHIN JSON DATA

# ****************************************************************************    
        if menu == 1:
            #Displays employment records json data.
            try:
                #Making the path to the file OS agnostic
                with open('EmploymentRecords.json', 'r') as f:
                    records = json.load(f)
            except (FileNotFoundError, json.JSONDecodeError) as e:
                #Sends error message if no records or JSON are found
                print(f"Error occurred while trying to read records: {str(e)}")
                print("No records found.")
                continue

            #Displays JSON data in a prettytable format
            #Creates table using the inputs as column titles.
            table = PrettyTable(['First Name', 'Last Name', 'Age', 'Employment Status'])
            #For loop to add each found result in a table from the JSON file
            for record in records:
                table.add_row([record['First name'], record['Last name'], record['Age'], record['Employment Status']])
            print(table)

            #Search functionality to search name within Records, loop to keep search going until exit, which sends them back to the menu
            while True:
                #Shows a the pretty table of the JSON data
                table = PrettyTable(['First Name', 'Last Name', 'Age', 'Employment Status'])
                for record in records:
                    table.add_row([record['First name'], record['Last name'], record['Age'], record['Employment Status']])
                print(table)
                #Prompts the user to type search to begin using the search function or exit back to the menu
                search_choice = input("Type 'search' to search for a person, or type 'exit' to return to the menu: ")
                if search_choice.lower() == "search":
                    #Calls the function above, to search within the records
                    search_person_within_records(records)
                elif search_choice.lower() == "exit":
                    break
# ****************************************************************  

        # USER OPTION 2 - USER INPUTS DATA

# ****************************************************************  
        elif menu == 2:
            while True:
                #Uses the Person Class made above, to specify user input, and put it in a dict form similar to JSON
                print("To enter your employment records please enter the information")  
                person = Person()
                person_dict = person.to_dict()

                #Displays the new record in a pretty table for confirmation before adding to the JSON file
                table = PrettyTable(['First Name', 'Last Name', 'Age', 'Employment Status'])
                table.add_row([person_dict['First name'], person_dict['Last name'], person_dict['Age'], person_dict['Employment Status']])
                print("\nHere is your new record:")
                print(table)

                #Prompts user to check if the record is correct, if it is it adds to JSON file, if not, it is deleted and user is prompted to add it again, this starts the while loop again.
                confirm = input("Is this correct? (y/n): ")
                if confirm.lower() not in ['y', 'yes']:
                    print("Please add the record again.")
                    continue
                
                #Reads JSON data, and raises error if no records are found
                try:
                    with open('EmploymentRecords.json', 'r') as f:
                        people = json.load(f)
                except (FileNotFoundError, json.JSONDecodeError) as e:
                    print(f"Error occurred while trying to read records: {str(e)}")
                    people = []
                

                #Writes the newly inputted data into the JSON in dictonary format within the array.
                people.append(person.to_dict())
                try:
                    with open('EmploymentRecords.json', 'w') as f:
                        json.dump(people, f)
                        s.send("Data added to JSON".encode('utf-8')) # Notify the server about the addition
                except Exception as e:
                    print(f"Error occurred while trying to write to file: {str(e)}")

                #Prompts the user if they would like to add another emplloyee record, to the JSON.
                continue_ = input("Would you like to add another employee record: y or n ") 
                if continue_.upper() == "N":
                    break

# ****************************************************************  

        # USER OPTION 3 - EXITS PAGE

# ****************************************************************  
        elif menu ==  3: 
            print("NOT ready sorry")
            break
        else:
            print("Invalid option selected, please try again.")
    #Closes socket
    s.close() 

if __name__ == '__main__':
    Main()

#TO DO LIST
#Refactoring and Commenting Code
#Browser displayed content(dev)
#Heterogeneous systems architectures (i.e., different O/S) (dev) 
#GUI or an output of stats and data.
    


