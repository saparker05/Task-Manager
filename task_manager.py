# This program is used for managing the tasks assigned to a team. Once the user has logged in with valid credentials they are
# given a menu which allows them to: register a new user, assign a task, view all tasks or view their own tasks.
# The admin user can also select an option to display task statistics.  

# These are included so that titles can be formatted in bold. 
BOLD = '\033[1m'
WHITE = '\033[0m'

#====Login Section====
# Define lists to store the corresponding usernames and passwords from the user.txt file. Then read the data from the file. 
usernames = []
passwords = []

user_file = open('user.txt', 'r', encoding='utf-8')

for line in user_file:

    # Split each line of the file into list items to store the username and password separately. 
    line_split = line.split()
    usernames.append((line_split[0]).strip(','))
    passwords.append(line_split[1])

user_file.close()

# Use a while loop to repeatedly ask the user to enter their username and password until a correct combination is entered. 
login = False

while login == False:

    username_check = False

    username = input("\nPlease enter your username: ")
    password = input("Please enter your password: ")

    for i in range(0, len(usernames)):

        # If the usernames and passwords match then the user can log in. 
        if username == usernames[i] and password == passwords[i]:
            username_check = True
            login = True 

        # If the username is saved but the password is entered incorrectly, print an incorrect password error message.
        if username == usernames[i] and login == False:
            username_check = True
            print("\nIncorrect password entered. Please try again.")  

    # If the username is not recognised, print a username not found error message. 
    if username_check == False:
        print("\nUsername not found. Please try again. ")

print("\n")

while True:
    # Present the appropriate menu to the user and 
    # make sure that the user input is coneverted to lower case.

    if username == "admin":
         menu = input('''Select one of the following Options below:
r - Register a user
a - Add a task
va - View all tasks
vm - View my tasks
s  - Display statistics
e - Exit
: ''').lower()

    else:
        menu = input('''Select one of the following Options below:
r - Register a user
a - Add a task
va - View all tasks
vm - View my tasks
e - Exit
: ''').lower()

    # This section of the code allows the admin user to register a new user.
    if menu == 'r':    
        
        print(f"\n{BOLD}Register a new user") 

        if username == "admin":
            
            # Use a while loop to repeatedly ask for a user name until a new one is entered. 
            new_username_check = False
           
            while new_username_check == False:
                new_username = input(f"\n{WHITE}Please enter a new username: ")
                new_username_check = True

                # Use a for loop to check through the list of usernames to see if the one entered is already in use. 
                for i in range(0, len(usernames)):

                    if new_username == usernames[i]:
                        new_username_check = False
                        print("The username is already in use. Please try again.")  
                        break

            # Use a while loop to ask for the new password until two matching passwords are entered.
            new_password_check = False

            while new_password_check == False:

                new_password = input("\nPlease enter a new password: ")
                new_password_confirm = input("\nPlease re-enter the password: ")

                if new_password == new_password_confirm:
                    new_password_check = True

                    # Add the new username and password to the lists of usernames and passwords. 
                    usernames.append(new_username)
                    passwords.append(new_password)

                    # Add the new username and password to the file user.txt
                    user_file = open('user.txt', 'a', encoding='utf-8')
                    user_file.write(f"\n{new_username}, {new_password}")
                    user_file.close()

                    print(f"\nNew user {new_username} has been created.\n")
        
                else:
                    print("\nPasswords do not match. Please try again.")

        # Display an error message if any other user apart from 'admin' tries to register a new user. 
        else:
            print(f"\n{WHITE}You do not have permission to register new users. Please select a different option from the menu.\n")


    # This section of code allows the user to add a new task to the task file. 
    elif menu == 'a':   

        print(f"\n{BOLD}Add a task") 
        
        # Use a while loop to make sure that the user the task will be assigned to is registered. 
        user_task_check = False

        while user_task_check == False:
        
            user_task = input(f"\n{WHITE}Please enter the name of the user that the task is assigned to: ")

            # Check through the saved usernames for the user.
            for i in range(0, len(usernames)):
                if user_task.strip() == usernames[i]:
                    user_task_check = True
            
            if user_task_check == False:
                print("Username not found. Please try again.")              

        # Request the task information from the user. 
        task_title = input("\nPlease enter the title of the task: ")   
        task_description = input("\nPlease enter a description of the task: ")
        due_date = input("Please enter the due date for the task: ")
        current_date = input("Please enter today's date: ")

        # Add the task details to the tasks.txt file. 
        task_file = open('tasks.txt', 'a', encoding='utf-8')
        task_file.write(f"\n{user_task}, {task_title}, {task_description}, {current_date}, {due_date}, No")
        task_file.close()

        print(f"\nConfirmation: {task_title} has been added for {user_task}.\n")

    # This section of code displays all of the tasks from the task file. 
    elif menu == 'va':

        print(f"\n{BOLD}All tasks: ") 

        task_file = open('tasks.txt', 'r', encoding='utf-8')
        
        # Use a for loop to read each line in the task file and split into the individual details. 
        for line in task_file:
            task_split = line.split(', ')
            task_split[5] = task_split[5].strip('\n')

            print(f'''{WHITE}
Task:               {task_split[1]}
Assigned to:        {task_split[0]}
Date assigned:      {task_split[3]}
Due date:           {task_split[4]}
Task complete?      {task_split[5]}   
Task description:    
    {task_split[2]}
            ''')  

        task_file.close()

    # This section of code displays the tasks for the user who is currently logged in. 
    elif menu == 'vm':

        print(f"\n{BOLD}Your tasks:") 
        
        task_file = open('tasks.txt', 'r', encoding='utf-8')   
        
        # For each line in the task file, split the data into the individual details, check if the assigned user is the user who
        # is logged in and if so display the task details. 
        for line in task_file:
            task_split = line.split(', ')
            task_split[5] = task_split[5].strip('\n')

            if username == task_split[0]:     
                print(f'''{WHITE}
Task:               {task_split[1]}
Assigned to:        {task_split[0]}
Date assigned:      {task_split[3]}
Due date:           {task_split[4]}
Task complete?      {task_split[5]}   
Task description:    
    {task_split[2]}           
                ''')  

        task_file.close()

    # This section of code displays statistics for the admin user. 
    elif menu == 's' and username == "admin":

        print(f"\n{BOLD}Task Statistics") 

        # Count the number of tasks in the file tasks.txt.
        task_file = open('tasks.txt', 'r', encoding='utf-8')
        task_count = 0

        for line in task_file:
            task_count += 1

        task_file.close()

        # Display the total number of users registered and the total number of tasks. 
        print(f'''{WHITE}
Total number of users:           {len(usernames)}     
Total number of tasks assigned:  {task_count}      
        ''')

    elif menu == 'e':
        print('Goodbye!!!')
        exit()

    else:
        print("You have made a wrong choice, Please Try again")  