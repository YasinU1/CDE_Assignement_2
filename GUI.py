import json
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.textinput import TextInput
from kivy.uix.togglebutton import ToggleButton
from kivy.properties import StringProperty
from kivy.uix.togglebutton import ToggleButtonBehavior
from kivy.graphics import Color, Rectangle
import prettytable
import socket
import json 
import re

# ------------------------------------------------------------------------------------
# USER OPTION 1 - SER WELCOME MENU
# ------------------------------------------------------------------------------------
class MainScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Create the root widget with a vertical box layout
        root = BoxLayout(orientation='vertical')

        with root.canvas.before:
            Color(1, 1, 1, 1)  # White background color
            self.rect = Rectangle(size=root.size, pos=root.pos)
            root.bind(size=self._update_rect, pos=self._update_rect)

        # Title
        anchor_title = AnchorLayout(anchor_x='center', anchor_y='center')
        title_box = BoxLayout(orientation='vertical', spacing=10, size_hint=(1, 0.3))
        title_label = Label(text='', color=(0, 0, 0, 1), font_size=42)
        subtitle_label = Label(text='You have connected to the Server', color=(0, 0, 0, 1), font_size=30)

        # Logo 
        anchor_image = AnchorLayout(anchor_x='center', anchor_y='center')
        logo = Image(source='recordImage.png', size_hint=(1, 0.5))

        # Anchor (adds center buttons container)
        anchor_layout = AnchorLayout(anchor_x='center', anchor_y='center')
        # Buttons container
        buttons_container = BoxLayout(orientation='vertical', size_hint=(0.5, 0.5), spacing=5)

        # Option 1 - READ
        button1 = Button(text='View Employee Records', disabled=True)
        button1.bind(on_press=self.read_screen)
        # Option 2 - WRITE
        button2 = Button(text='Add Employee Records', disabled=True)
        button2.bind(on_press=self.write_screen)
        # Option 3 - EXIT
        button3 = Button(text='Exit')
        button3.bind(on_release=self.exit_app)

        # Anchor -> Buttons Container -> Buttons
        title_box.add_widget(title_label)
        title_box.add_widget(subtitle_label)
        anchor_title.add_widget(title_box)
        anchor_image.add_widget(logo)
        buttons_container.add_widget(button1)
        buttons_container.add_widget(button2)
        buttons_container.add_widget(button3)
        anchor_layout.add_widget(buttons_container)
        
        # Add to SCREEN widget
        root.add_widget(anchor_title)
        root.add_widget(anchor_image)
        root.add_widget(anchor_layout)
        self.add_widget(root)

        # Same host, port, and socket code as the server to create the connection
        host = '127.0.0.1'
        port = 8989
        s = socket.socket()
        # Connection to server
        try:
            s.connect((host, port))
            print("\n---------------------- Connected to the server successfully! ----------------------")
            title_label.text = 'Welcome to Employee Records!!!'
            button1.disabled = False
            button2.disabled = False
        # If the server is not connected, it shows an error message
        except socket.error as ERROR:
            title_label.text = 'Error: Not connected to the server'
            print("Error occurred while connecting to the server: ", ERROR)

    # Sends user to Read screen
    def read_screen(self, *args):
        self.manager.current = 'read_screen'

    # Sends user to Write screen
    def write_screen(self, *args):
        self.manager.current = 'write_screen'

    # Exits user from app
    def exit_app(self, instance):
        App.get_running_app().stop()  # Stop the Kivy application
    
    def _update_rect(self, instance, value):
        # Update the size and position of the rectangle
        self.rect.size = instance.size
        self.rect.pos = instance.pos

# ------------------------------------------------------------------------------------
# USER OPTION 1 - USER CAN DISPLAY AND SEARCH WITHIN JSON DATA
# ------------------------------------------------------------------------------------
class ReadScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Create the root widget with a vertical box layout
        root = BoxLayout(orientation='vertical')

        with root.canvas.before:
            Color(1, 1, 1, 1)  # White background color
            self.rect = Rectangle(size=root.size, pos=root.pos)
            root.bind(size=self._update_rect, pos=self._update_rect)

        # Title
        title = Label(text='See Employees Records', color=(0, 0, 0, 1), size_hint=(1, 0.3), font_size=42)

        # User inputs
        self.inputs = {}  # Dictionary to store references to the TextInput widgets

        # Search Bar
        anchor_search = AnchorLayout(anchor_x='center', anchor_y='top', size_hint=(1, 0.3))
        search_container = BoxLayout(orientation='horizontal', spacing=20, size_hint=(0.5, None), height=70)
        search_label = Label(text='Search:', color=(0, 0, 0, 1), size_hint=(0.2, None), height=30)
        search_input = TextInput(size_hint=(0.5, None), height=30)
        self.inputs['search'] = search_input
        search_button = Button(text='GO!', size_hint=(0.2, None), height=32)
        search_button.bind(on_press=lambda x: self.search_records(search_input.text))
        clear_button = Button(text='Clear', size_hint=(0.2, None), height=32)
        clear_button.bind(on_press=lambda x: self.search_records(" "))

        # Display JSON file
        anchor_json = AnchorLayout(anchor_x='center', anchor_y='center', size_hint=(1, 0.4))
        try:
            # Making the path to the file OS agnostic
            with open('EmploymentRecords.json', 'r') as f:
                self.records = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            # Sends error message if no records or JSON are found
            print(f"Error occurred while trying to read records: {str(e)}")
            print("No records found.")

        self.json_layout = GridLayout(cols=4)
        headers = ['First Name', 'Last Name', 'Age', 'Employee Status']
        for header in headers:
            self.json_layout.add_widget(Label(text=header, bold=True, color=(0, 0, 0, 1)))  # Add header labels to the layout
        
        self.display_records()  # Display all records initially

        # Exit buttons
        anchor_layout_exit = AnchorLayout(anchor_x='center', anchor_y='center', size_hint_y=None, height=120)
        buttons_container = BoxLayout(orientation='vertical', size_hint=(0.3, 0.3))
        exitBut = Button(text='Go back to home!')
        exitBut.bind(on_press=self.main_screen)

        # Add to widget containers
        search_container.add_widget(search_label)
        search_container.add_widget(search_input)
        search_container.add_widget(search_button)
        search_container.add_widget(clear_button)
        anchor_search.add_widget(search_container)

        anchor_json.add_widget(self.json_layout)

        buttons_container.add_widget(exitBut)
        anchor_layout_exit.add_widget(buttons_container)

        # Add to root widget
        root.add_widget(title)
        root.add_widget(anchor_search)
        root.add_widget(anchor_json)
        root.add_widget(anchor_layout_exit)
        
        self.add_widget(root)

    # Sends user to Write screen
    def main_screen(self, *args):
        self.manager.current = 'main_screen'
    
    # Update the size and position of the rectangle
    def _update_rect(self, instance, value):
        self.rect.size = instance.size
        self.rect.pos = instance.pos

    # Display all records
    def display_records(self):
        self.json_layout.clear_widgets()  # Clear the current widgets

        headers = ['First Name', 'Last Name', 'Age', 'Employment Status']
        for header in headers:
            self.json_layout.add_widget(Label(text=header, bold=True, color=(0, 0, 0, 1)))  # Add header labels to the layout

        for record in self.records:
            first_name = record['First Name']
            last_name = record['Last Name']
            age = str(record['Age'])
            employment_status = record['Employment Status']

            self.json_layout.add_widget(Label(text=first_name, color=(0, 0, 0, 1)))
            self.json_layout.add_widget(Label(text=last_name, color=(0, 0, 0, 1)))
            self.json_layout.add_widget(Label(text=age, color=(0, 0, 0, 1)))
            self.json_layout.add_widget(Label(text=employment_status, color=(0, 0, 0, 1)))

    # Search and display records based on search value
    def search_records(self, search_value):
        if search_value.strip():  # If search_value is not empty or contains only spaces
            search_results = []
            for record in self.records:
                first_name = record['First Name']
                last_name = record['Last Name']
                age = str(record['Age'])
                employment_status = record['Employment Status']

                # Check if any field matches the search value
                if search_value.lower() in first_name.lower() or \
                        search_value.lower() in last_name.lower() or \
                        search_value.lower() in age.lower() or \
                        search_value.lower() in employment_status.lower():
                    search_results.append(record)

            # Update the display with search results
            self.json_layout.clear_widgets()  # Clear the current widgets

            headers = ['First Name', 'Last Name', 'Age', 'Employment Status']
            for header in headers:
                self.json_layout.add_widget(Label(text=header, bold=True, color=(0, 0, 0, 1)))  # Add header labels to the layout

            for record in search_results:
                first_name = record['First Name']
                last_name = record['Last Name']
                age = str(record['Age'])
                employment_status = record['Employment Status']

                self.json_layout.add_widget(Label(text=first_name, color=(0, 0, 0, 1)))
                self.json_layout.add_widget(Label(text=last_name, color=(0, 0, 0, 1)))
                self.json_layout.add_widget(Label(text=age, color=(0, 0, 0, 1)))
                self.json_layout.add_widget(Label(text=employment_status, color=(0, 0, 0, 1)))
        else:
            self.display_records()  # Display all records when search_value is empty or contains only spaces
            # Clear the input values
            self.inputs['search'].text = ''

# ------------------------------------------------------------------------------------
# USER OPTION 2 - USER INPUTS DATA
# ------------------------------------------------------------------------------------
class WriteScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        root = BoxLayout(orientation='vertical')

        with root.canvas.before:
            Color(1, 1, 1, 1)
            self.rect = Rectangle(size=root.size, pos=root.pos)
            root.bind(size=self._update_rect, pos=self._update_rect)

        title = Label(text='Add an Employee Records', color=(0, 0, 0, 1), size_hint=(1, 0.1), font_size=42)

        # Add an error message label to your layout
        self.error_message = Label(text='', color=(1, 0, 0, 1), size_hint=(1, 0.05))

        # User inputs
        self.inputs = {}  # Dictionary to store references to the TextInput widgets
        anchor_firstName = AnchorLayout(anchor_x='center', anchor_y='center', size_hint_y=None, height=40)
        firstName_container = BoxLayout(orientation='horizontal', size_hint=(0.5, None), height=70)
        firstName_label = Label(text='First Name:', color=(0, 0, 0, 1), size_hint=(0.5, None), height=30)
        firstName_input = TextInput(size_hint=(0.5, None), height=30)
        self.inputs['firstName'] = firstName_input  # Store the reference

        anchor_lastName = AnchorLayout(anchor_x='center', anchor_y='center', size_hint_y=None, height=40)
        lastName_container = BoxLayout(orientation='horizontal', size_hint=(0.5, None), height=70)
        lastName_label = Label(text='Last Name:', color=(0, 0, 0, 1), size_hint=(0.5, None), height=30)
        lastName_input = TextInput(size_hint=(0.5, None), height=30)
        self.inputs['lastName'] = lastName_input  # Store the reference

        anchor_age = AnchorLayout(anchor_x='center', anchor_y='center', size_hint_y=None, height=40)
        age_container = BoxLayout(orientation='horizontal', size_hint=(0.5, None), height=70)
        age_label = Label(text='Age:', color=(0, 0, 0, 1), size_hint=(0.5, None), height=30)
        age_input = TextInput(size_hint=(0.5, None), height=30)
        self.inputs['age'] = age_input  # Store the reference

        anchor_status = AnchorLayout(anchor_x='center', anchor_y='center', size_hint_y=None, height=40)
        status_container = BoxLayout(orientation='horizontal', size_hint=(0.4, None), height=70)
        status_label = Label(text='Employee Status:', color=(0, 0, 0, 1), size_hint=(0.55, None), height=30)

        # Create a custom ToggleButton class with radio button behavior
        class RadioButton(ToggleButton):
            group = StringProperty('')

        no_option = RadioButton(state='down', group='my_group', size_hint=(None, None), height=30, width=30)
        no_label = Label(text='NO', size_hint=(0.30, None), height=30,  color=(0, 0, 0, 1), font_size=12)

        yes_option = RadioButton(group='my_group', size_hint=(None, None), height=30, width=30)
        yes_label = Label(text='YES', size_hint=(0.30, None), height=30, color=(0, 0, 0, 1), font_size=12)

        # Store the reference to the 'status' input field
        self.inputs['status'] = yes_option

        # Submit buttons
        anchor_layout_submit = AnchorLayout(anchor_x='center', anchor_y='center', size_hint_y=None, height=140)
        buttonSub_container = BoxLayout(orientation='vertical', size_hint=(0.5, 0.2))
        subBut = Button(text='Submit')
        subBut.bind(on_press=self.display_screen)

        # Exit buttons
        anchor_layout_exit = AnchorLayout(anchor_x='center', anchor_y='center', size_hint_y=None, height=120)
        buttons_container = BoxLayout(orientation='vertical', size_hint=(0.3, 0.3), spacing=5)
        exitBut = Button(text='Go back to home!')
        exitBut.bind(on_press=self.main_screen)

        # Add to widget containers
        firstName_container.add_widget(firstName_label)
        firstName_container.add_widget(firstName_input)
        anchor_firstName.add_widget(firstName_container)

        lastName_container.add_widget(lastName_label)
        lastName_container.add_widget(lastName_input)
        anchor_lastName.add_widget(lastName_container)

        age_container.add_widget(age_label)
        age_container.add_widget(age_input)
        anchor_age.add_widget(age_container)

        status_container.add_widget(status_label)
        status_container.add_widget(no_label)
        status_container.add_widget(no_option)
        status_container.add_widget(yes_label)
        status_container.add_widget(yes_option)
        anchor_status.add_widget(status_container)

        buttonSub_container.add_widget(subBut)
        anchor_layout_submit.add_widget(buttonSub_container)

        buttons_container.add_widget(exitBut)
        anchor_layout_exit.add_widget(buttons_container)

        # Add to root widget
        root.add_widget(title)
        root.add_widget(self.error_message)
        root.add_widget(anchor_firstName)
        root.add_widget(anchor_lastName)
        root.add_widget(anchor_age)
        root.add_widget(anchor_status)
        root.add_widget(anchor_layout_submit)
        root.add_widget(anchor_layout_exit)

        self.add_widget(root)


    # Sends user to Display screen
    def display_screen(self, *args):
        first_name = self.inputs['firstName'].text
        last_name = self.inputs['lastName'].text
        age = self.inputs['age'].text
        status = "YES" if self.inputs['status'].state == "down" else "NO"

        if not re.match("^[A-Za-z]*$", first_name) or not first_name:
            self.error_message.text = "Invalid first name. Please enter a valid first name."
            return
        if not re.match("^[A-Za-z]*$", last_name) or not last_name:
            self.error_message.text = "Invalid last name. Please enter a valid last name."
            return
        if not re.match("^(0?[1-9]|[1-9][0-9]|1[01][0-9]|120)$", age) or not age:
            self.error_message.text = "Invalid age. Please enter a valid age between 1 to 120."
            return

        self.error_message.text = ''

        self.inputs['firstName'].text = ''
        self.inputs['lastName'].text = ''
        self.inputs['age'].text = ''
        self.inputs['status'].state = 'normal'

        display_screen = self.manager.get_screen('display_screen')
        display_screen.set_data(first_name, last_name, age, status)
        self.manager.current = 'display_screen'

    def main_screen(self, *args):
        self.manager.current = 'main_screen'

    def _update_rect(self, instance, value):
        self.rect.size = instance.size
        self.rect.pos = instance.pos

# --------------------------------------------------------------------------------------------------
# USER OPTION 2 - DISPLAY USER WITH ENTERED INFORMATION BEFORE SUBMITTING
# --------------------------------------------------------------------------------------------------
class DisplayScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Create the root widget with a vertical box layout
        root = BoxLayout(orientation='vertical')

        with root.canvas.before:
            Color(1, 1, 1, 1)  # White background color
            self.rect = Rectangle(size=root.size, pos=root.pos)
            root.bind(size=self._update_rect, pos=self._update_rect)

        # Title
        title = Label(text='Employee Records', color=(0, 0, 0, 1), size_hint=(1, None), height=150, font_size=42)

        # Displayed data
        anchor_data_layout = AnchorLayout(anchor_x='center', anchor_y='center', size_hint_y=None, height=250)
        self.data_label = Label(text='', color=(0, 0, 0, 1), size_hint=(1, 1), font_size=18)
        
        # Question
        anchor_question_layout = AnchorLayout(anchor_x='center', anchor_y='center', size_hint_y=None, height=50)
        question_container = BoxLayout(orientation='vertical', size_hint=(0.5, None), height=10)
        question_label = Label(text='Is your information correct?', color=(0, 0, 0, 1), font_size=20)

        # User options
        anchor_button_layout = AnchorLayout(anchor_x='center', anchor_y='top')
        buttons_container = BoxLayout(orientation='horizontal', size_hint=(0.5, None), height=50, spacing=25)
        # Option 1 - YES
        yes_button = Button(text='YES')
        yes_button.bind(on_press=self.Add_To_Json)
        # Option 2 - NO
        no_button = Button(text='NO')
        no_button.bind(on_press=self.write_screen)

        # Add to widget containers
        anchor_data_layout.add_widget(self.data_label)
        buttons_container.add_widget(yes_button)
        buttons_container.add_widget(no_button)
        anchor_button_layout.add_widget(buttons_container)
        question_container.add_widget(question_label)
        anchor_question_layout.add_widget(question_container)

        # Add to root widget
        root.add_widget(title)
        root.add_widget(anchor_data_layout)
        root.add_widget(anchor_question_layout)
        root.add_widget(anchor_button_layout)
        self.add_widget(root)

    # Set the displayed data
    def set_data(self, first_name, last_name, age, status):
        data = f"First Name: {first_name}\nLast Name: {last_name}\nAge: {age}\nStatus: {status}"
        self.data_label.text = data

    # Sends user to Write screen
    def write_screen(self, *args):
        self.manager.current = 'write_screen'

    # Sends user to Write screen
    def Add_To_Json(self, *args):
        # Get the data from the data box
        displayed_data = self.data_label.text

        # Extract the data
        first_name = ''
        last_name = ''
        age = ''
        status = ''
        data_lines = displayed_data.split('\n')
        for line in data_lines:
            if line.startswith('First Name:'):
                first_name = line.split(': ')[1]
            elif line.startswith('Last Name:'):
                last_name = line.split(': ')[1]
            elif line.startswith('Age:'):
                age = line.split(': ')[1]
            elif line.startswith('Status:'):
                status = line.split(': ')[1]

        # Create a dictionary for the person's information
        person = {
            "First Name": first_name,
            "Last Name": last_name,
            "Age": age,
            "Employment Status": status
        }

        # Load the existing records from the JSON file
        try:
            with open('EmploymentRecords.json', 'r') as f:
                people = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            # If no records are found, start with an empty list
            people = []

        # Add the new person's information to the list of records
        people.append(person)

        # Write the updated records back to the JSON file
        try:
            with open('EmploymentRecords.json', 'w') as f:
                json.dump(people, f)
                print("Data added to JSON")
        except Exception as e:
            print(f"Error occurred while trying to write to file: {str(e)}")
        
        self.manager.current = 'write_screen'

    def _update_rect(self, instance, value):
        # Update the size and position of the rectangle
        self.rect.size = instance.size
        self.rect.pos = instance.pos

# Main Screen
class EmployeeRecordsApp(App):
    def build(self):  
        
        # Create the screen manager
        screen_manager = ScreenManager()

        main_screen = MainScreen(name='main_screen')
        screen_manager.add_widget(main_screen)

        write_screen = WriteScreen(name='write_screen')
        screen_manager.add_widget(write_screen)

        read_screen = ReadScreen(name='read_screen')
        screen_manager.add_widget(read_screen)

        display_screen = DisplayScreen(name='display_screen')
        screen_manager.add_widget(display_screen)

        return screen_manager
    

if __name__ == '__main__':
    EmployeeRecordsApp().run()