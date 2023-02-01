# This program is used for managing the tasks assigned to a team. Once the user has logged in with valid credentials they are
# given a menu which allows them to: register a new user, assign a task, view all tasks or view their own tasks.
# The admin user can also select an option to generate reports or display statistics.  


# The function reg_user allows the user to register a new user. It takes the current dictionary of login details and returns an updated one. 
# The function updates the user.txt file with the new user. 
def reg_user(login_dict):
    
    print(f"\n{BOLD}Register a new user{WHITE}") 
        
    # Use a while loop to repeatedly ask for a username until a new one is entered. 
    new_username_check = False
           
    while new_username_check == False:
        new_username = input(f"\nPlease enter a new username: ")
        new_username_check = True

        # Check whether the username entered is already in use. 
        if new_username.strip() in login_dict:                    
            new_username_check = False
            print("The username is already in use. Please try again.")

    # Use a while loop to ask for the new password until two matching passwords are entered.
    new_password_check = False

    while new_password_check == False:

        new_password = input("\nPlease enter a new password: ")
        new_password_confirm = input("\nPlease re-enter the password: ")

        if new_password == new_password_confirm:
            new_password_check = True

            # Add the new username and password to the dictionary.
            login_dict[new_username] = new_password

            # Add the new username and password to the file user.txt
            user_file = open('user.txt', 'a', encoding='utf-8')
            user_file.write(f"\n{new_username}, {new_password}")
            user_file.close()

            print(f"\nNew user {new_username} has been created.\n")
        
        else:
            print("\nPasswords do not match. Please try again.")

    return(login_dict)


# The function add_task updates the file tasks.txt with a new task input by the user. 
def add_task(login_dict):

    print(f"\n{BOLD}Add a task{WHITE}") 
        
    # Use a while loop to make sure that the user the task will be assigned to is registered. 
    user_task_check = False

    while user_task_check == False:
        
        user_task = input(f"\nPlease enter the name of the user that the task is assigned to: ")

        # Check through the saved usernames for the user.
        if user_task.strip() in login_dict:
            user_task_check = True
            
        if user_task_check == False:
            print("Username not found. Please try again.")              

    # Request the task information from the user. 
    task_title = input("\nPlease enter the title of the task: ")   
    task_description = input("\nPlease enter a description of the task: ")
    
    while True:
        due_date = get_due_date()
        current_date = get_current_date()

        if overdue(current_date, due_date) == False:
            break
        else:
            print("\nInput error: due date is before current date. Please try again.")


    # Add the task details to the tasks.txt file. 
    task_file = open('tasks.txt', 'a', encoding='utf-8')
    task_file.write(f"\n{user_task}, {task_title}, {task_description}, {current_date}, {due_date}, No")
    task_file.close()

    print(f"\nConfirmation: {task_title} has been added for {user_task}.\n")


# The functional view_all takes the file name and displays all of the tasks in the file. 
def view_all(tasks_file_name):
    
    print(f"\n{BOLD}All tasks: {WHITE}") 

    task_file = open(tasks_file_name, 'r', encoding='utf-8')
        
    # Use a for loop to read each line in the task file and split into the individual details. 
    for line in task_file:
        task_split = line.split(', ')
        task_split[5] = task_split[5].strip('\n')

        print(f'''
Task:               {task_split[1]}
Assigned to:        {task_split[0]}
Date assigned:      {task_split[3]}
Due date:           {task_split[4]}
Task complete?      {task_split[5]}   
Task description:    
    {task_split[2]}
            ''')  

    task_file.close()


# The function view_mine takes the user and the name of the tasks file and displays the user's tasks with the option to edit the tasks.
def view_mine(user, tasks_file_name):   
    
    print(f"\n{BOLD}Your tasks:") 
        
    task_file = open(tasks_file_name, 'r', encoding='utf-8')   

    # Create a dictionary to store the task details by user.  
    user_tasks = {}
        
    # For each line in the task file, split the data into the individual details.
    for line in task_file:
        task_split = line.split(', ')                  
        task_split[5] = task_split[5].strip('\n')    

        # Set up the user_tasks dictionary so that the users are the keys and the values are all lists that can be added to.                                         
        if task_split[0] not in user_tasks:
            user_tasks[task_split[0]] = []
        
        user_tasks[task_split[0]].append(", ".join(task_split))

        # If the assigned user for the task matches the user who is logged in then print the task details. 
        if user == task_split[0]: 

            print(f'''{WHITE} 
            Task {len(user_tasks[user])}

Task:               {task_split[1]}
Assigned to:        {task_split[0]}
Date assigned:      {task_split[3]}
Due date:           {task_split[4]}
Task complete?      {task_split[5]}   
Task description:    
    {task_split[2]}           
                ''')  


    task_file.close()

    # Use a while loop to repeatedly ask the user to select a task to make changes to or enter -1 to return to the main menu. 
    task_selection_check = False
    
    while task_selection_check == False:

        task_selection_check = True
        
        try:
            task_selection = int(input("\nEnter a task number to make changes to a task or enter -1 to return to the main menu: "))

            if task_selection < -1 or task_selection > len(user_tasks[user]):    
                print("Error: selection not made. Please try again.")
                task_selection_check = False

            elif task_selection == -1:
                return  

            else:

                # Use a while loop to get the user's choice whether to edit or complete the selected task.
                while True:

                    try:
                        user_choice = int(input("Enter 1 to edit the task or enter 2 to mark the task as complete: "))

                        if user_choice == 1 or user_choice == 2:
                            break

                        else:
                            print("Input error. Please try again.")
                    
                    except ValueError:
                        print("Input error. Please try again.")

                # If the user selects to edit the task, first check if the task is complete. 
                if user_choice == 1:

                    user_edit = user_tasks[user][task_selection - 1].split(', ')

                    if user_edit[5] == "Yes":
                        print(f"\nTask {task_selection} is already complete. Changes cannot be made to this task.")

                    else:
                        
                        # Use a while loop to ask the user whether they want to change the user the task is assigned to or change the due date of the task. 
                        while True:

                            try:
                                user_edit_choice = int(input("Enter 1 to change the user that the task is assigned to or enter 2 to change the due date of the task: "))

                                if user_edit_choice == 1 or user_edit_choice == 2:
                                    break

                                else:
                                    print("Input error. Please try again.")

                            except ValueError:
                                print("Input error. Please try again.")

                        # If the user selects to change the user the task is assigned to, ask for the new user and check the user exists.
                        if user_edit_choice == 1:

                            while True:
                                user_change = input("Please enter the user you would like to assign the task to: ")

                                if user_change in login_details:
                                    break

                                else:
                                    print("User not found, please try again.")
                    
                            # Update the user.
                            user_edit[0] = user_change
                            print(f"\nConfirmation: task {task_selection} assigned to {user_change}.")

                        # If the user selects to edit the due date, request the new due date. 
                        if user_edit_choice == 2:
                            user_edit[4] = get_due_date()

                        # Update the user_tasks dictionary with any changes.
                        user_tasks[user][task_selection - 1] = ", ".join(user_edit)

                # If the user selects to mark the task as complete, change No to Yes in the task details in user_tasks.
                if user_choice == 2:
                
                    user_edit = user_tasks[user][task_selection - 1].split(', ')
                    user_edit[5] = "Yes"  
                    user_tasks[user][task_selection - 1] = ", ". join(user_edit)

                    print(f"\nConfirmation: task {task_selection} is complete.")
            
                # Write the updated dictionary of tasks to the task file. 
                task_file = open(tasks_file_name, 'w', encoding='utf-8') 
            
                line_count = 0

                for users in user_tasks:

                    for j in range(0, len(user_tasks[users])):   
                    
                        line_count += 1

                        # After the first line of the file, start a new line for each task.
                        if line_count == 1:
                            task_file.write(user_tasks[users][j])
                        else:
                            task_file.write(f"\n{user_tasks[users][j]}") 

                task_file.close()

            # Mark task_selection_check as False to give the user the option to make other changes to their tasks if required. 
            task_selection_check = False

        except ValueError:
            print("Error: selection not made. Please try again.")
            task_selection_check = False        


# This function takes the date today and the due date of the task in the format 1 Jan 2023. 
# The function returns True if the task is overdue and False if not. 
def overdue(date_today, date_due):

    date_today_list = (date_today.lower()).split()
    date_due_list = (date_due.lower()).split()

    # Define a list of months to use to check dates and find out if a task is overdue. 
    months = ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"]

    # If the due date year is before today's date then the task is overdue. 
    if int(date_due_list[2]) < int(date_today_list[2]):
        return True

    # If the years are the same, check whether the months are the same. 
    elif int(date_due_list[2]) == int(date_today_list[2]):

        # If the months are the same, check whether the day of the due date has passed.
        if date_due_list[1] == date_today_list[1]:

            # If the day is before today then the task is overdue. 
            if int(date_due_list[0]) < int(date_today_list[0]):   
                return True
            else:
                return False                              

        # Else, check whether the due date month has already passed.
        else:

            for month in months:
                # If the due date month appears in months before the current month then the task is overdue. 
                if month == date_due_list[1]:
                    return True

                if month == date_today_list[1]:
                    return False
    else:
        return False


# This function generates the report files task_overview.txt and user_overview.txt.
def generate_reports():   

    task_file = open('tasks.txt', 'r', encoding='utf-8')

    # Set up variables to count the tasks.    
    task_count = 0
    completed_tasks_count = 0
    uncompleted_tasks_count = 0
    overdue_tasks_count = 0

    # Call the get_current_date function to get today's date.     
    today_date = get_current_date()

    # Go through each line in the task file and count the number of tasks, completed tasks, uncompleted tasks and overdue tasks. 
    for line in task_file:
        task_count += 1
        task_split = line.split(', ')

        if task_split[5] == "Yes":
            completed_tasks_count += 1
        else:
            uncompleted_tasks_count += 1
            
            # Check if the uncompleted tasks are overdue. 
            if overdue(today_date, task_split[4]) == True:
                overdue_tasks_count += 1

    task_file.close()

    # Calculate the required percentages. 
    if task_count > 0:
        incomplete_percentage = round((uncompleted_tasks_count/task_count)*100, 2)
        overdue_percentage = round((overdue_tasks_count/task_count)*100, 2)
    else:
        incomplete_percentage = 0.00
        overdue_percentage = 0.00

    # Print the reports to the files. 
    task_overview = open('task_overview.txt', 'w', encoding='utf-8')
    task_overview.write(f'''            Task Overview
        
Total number of tasks:                              {task_count}
Number of completed tasks:                          {completed_tasks_count}
Number of uncompleted tasks:                        {uncompleted_tasks_count}
Number of overdue uncompleted tasks:                {overdue_tasks_count}
Percentage of tasks that are incomplete:            {incomplete_percentage}%
Percentage of tasks that are overdue:               {overdue_percentage}%             ''')
    task_overview.close()


    user_overview = open('user_overview.txt', 'w', encoding='utf-8')
    user_overview.write(f'''            User Overview 
        
Total number of users:          {len(login_details)}                  
Total number of tasks:          {task_count}  \n''')
    user_overview.close()
        

    user_overview = open('user_overview.txt', 'a', encoding='utf-8')

    for users in login_details:
        
        # Set up variables to count each users tasks, completed tasks, uncompleted tasks and overdue tasks. 
        user_task_count = 0
        user_completed_count = 0
        user_uncompleted_count = 0
        user_overdue_count = 0

        task_file = open('tasks.txt', 'r', encoding='utf-8')

        for tasks in task_file:

            tasks_list = tasks.split(', ')

            # Count the users tasks, completed tasks and uncompleted tasks. 
            if users == tasks_list[0]:
                user_task_count += 1

                if tasks_list[5] == "Yes":
                    user_completed_count += 1
                else:
                    user_uncompleted_count += 1

                    # Count how many of each users uncompleted tasks are overdue. 
                    if overdue(today_date, tasks_list[4]) == True:
                        user_overdue_count += 1
            
        task_file.close()
                       
        # Calculate the required percentages for the user. 
        if task_count > 0:
            percentage_assigned = round((user_task_count/task_count)*100, 2)
        else:
            percentage_assigned = 0

        if user_task_count > 0:
            percentage_completed = round((user_completed_count/user_task_count)*100, 2)
            percentage_uncompleted = round((user_uncompleted_count/user_task_count)*100, 2)
            percentage_overdue = round((user_overdue_count/user_task_count)*100, 2)
        else:
            percentage_completed = 0.00
            percentage_uncompleted = 0.00
            percentage_overdue = 0.00

        # Print the users statistics to the user_overview file.
        user_overview.write(f'''\n          {users}

Total number of tasks assigned:                          {user_task_count}
Percentage of tasks assigned (out of all users):         {percentage_assigned}%      
Percentage of assigned tasks completed:                  {percentage_completed}%
Percentage of assigned tasks to be completed:            {percentage_uncompleted}%
Percentage of overdue assigned tasks:                    {percentage_overdue}%

''')

    user_overview.close()
    
    return


# This function requests the current date from the user, validates the input and returns the current date. 
def get_current_date():

    input_check = False

    while input_check == False:

        date = input("\nPlease enter the date today in the format 1 Jan 2023: ")

        # Split the input into a list to use to validate the input.
        split_date = date.split()

        # Define a list of months to check the input.
        abbr_months = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']

        # Define a list of months that have 30 days.
        months_30 = ['sep', 'apr', 'jun', 'nov']

        # The user should have entered the date in 3 parts.
        if len(split_date) != 3:
            print("\nInput error. Please try again.")

        else:

            try:
                # The day should be between 1 and 31 inclusive and the year should be after 2022.
                if int(split_date[0]) > 0 and int(split_date[0]) <= 31 and int(split_date[2]) > 2022:
                    
                    # If the user enters 31 as the day and a month with only 30 days the date will be incorrect.
                    if int(split_date[0]) == 31 and split_date[1].lower() in months_30:
                        print("\nIncorrect date entered. Please try again.")

                    # If the user enters 30th or 31st feb then the date is incorrect.
                    elif int(split_date[0]) > 29 and split_date[1].lower() == 'feb':
                        print("\nIncorrect date entered. Please try again.")

                    # If the user enters 29 feb in a year that is not a leap year then the date is incorrect.
                    elif int(split_date[0]) == 29 and split_date[1].lower() == 'feb' and int(split_date[2]) % 4 != 0:
                        print("\nIncorrect date entered. Please try again.")
                    
                    # Check that the month entered is in abbr_months
                    elif split_date[1].lower() in abbr_months:
                        input_check = True

                    else:
                        print("\nInput error. Please try again.")
                
                else:
                    print("\nInput error. Please try again.")

            except ValueError:
                print("\nInput error. Please try again.")

    return date


# This function requests the due date of a task from the user, validates the input and returns the due date. 
def get_due_date():

    input_check = False

    # Use a while loop to request the due date from the user until a valid date is entered. 
    while input_check == False:

        date = input("\nPlease enter the due date of the task in the format 1 Jan 2023: ")

        # Split the input into a list.
        split_date = date.split()

        # Define a list of abbreviations for the months of the year.
        abbr_months = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']

        # Create a list of months which only have 30 days.
        months_30 = ['sep', 'apr', 'jun', 'nov']

        # The user input should have 3 parts if it has been entered in the correct format.
        if len(split_date) != 3:
            print("\nInput error. Please try again.")

        else:

            try:
                # The day should be between 1 and 31 inclusive and the year should be after 2022.
                if int(split_date[0]) > 0 and int(split_date[0]) <= 31 and int(split_date[2]) > 2022:
                    
                    # If the day entered is 31, the month should have 31 days.
                    if int(split_date[0]) == 31 and split_date[1].lower() in months_30:
                        print("\nIncorrect date entered. Please try again.")

                    # If the month entered is feb the day should not be 30 or 31.
                    elif int(split_date[0]) > 29 and split_date[1].lower() == 'feb':
                        print("\nIncorrect date entered. Please try again.")

                    # If the user enters 29 feb and the year is not a leap year then the date is incorrect.
                    elif int(split_date[0]) == 29 and split_date[1].lower() == 'feb' and int(split_date[2]) % 4 != 0:
                        print("\nIncorrect date entered. Please try again.")
                    
                    # Check that the month entered is in abbr_months
                    elif split_date[1].lower() in abbr_months:
                        input_check = True

                    else:
                        print("\nInput error. Please try again.")
                
                else:
                    print("\nInput error. Please try again.")

            except ValueError:
                print("\nInput error. Please try again.")

    return date


# These are included so that titles can be formatted in bold. 
BOLD = '\033[1m'        
WHITE = '\033[0m'


#====Login Section====

login_details = {}

user_file = open('user.txt', 'r', encoding='utf-8')

for line in user_file:

    # Split each line of the file into list items to store the username and password separately. 
    line_split = line.split()
    login_details[(line_split[0].strip(','))] = line_split[1]

user_file.close()

# Use a while loop to repeatedly ask the user to enter their username and password until a correct combination is entered. 
login = False

while login == False:

    username = input("\nPlease enter your username: ").strip()
    password = input("Please enter your password: ").strip()

    # If the username is not found print an error message.
    if username not in login_details:
        print("\nUsername not found. Please try again.")

    else:
        for i in range(0, len(login_details)):

            # If the usernames and passwords match then the user can log in. 
            if login_details[username] == password:
                login = True 

    # If the username is saved but the password is entered incorrectly, print an incorrect password error message.
    if username in login_details and login == False:
        print("\nIncorrect password entered. Please try again.")  


print("\n")


while True:
    # Present the appropriate menu to the user and 
    # make sure that the user input is converted to lower case.

    if username == "admin":
         menu = input('''Select one of the following Options below:
r - Register a user
a - Add a task
va - View all tasks
vm - View my tasks
gr - Generate reports
ds  - Display statistics
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

    # If the admin user selects r, call the reg_user function. 
    if menu == 'r':    

        if username == "admin":
            login_details = reg_user(login_details)

        # Display an error message if any other user apart from 'admin' tries to register a new user. 
        else:
            print(f"\n{WHITE}You do not have permission to register new users. Please select a different option from the menu.\n")


    # If the user selects a, call the add_task function. 
    elif menu == 'a':   
        add_task(login_details)

    # If the user selects va, call the view_all function.
    elif menu == 'va':
        view_all('tasks.txt')  

    # If the user selects vm, call the view_mine function.
    elif menu == 'vm':
        view_mine(username, 'tasks.txt')

    # If the admin user selects gr, call the generate_reports function. 
    elif menu == 'gr' and username == "admin":

        generate_reports()             

    # This section of code displays statistics for the admin user. 
    elif menu == 'ds' and username == "admin":

        print(f"\n{BOLD}Display Statistics{WHITE}") 

        # Check if the task_overview file already exists and if not call the generate_reports function. 
        try:
            task_overview = open('task_overview.txt', 'r', encoding='utf-8')

        except FileNotFoundError:
            generate_reports()
            task_overview = open('task_overview.txt', 'r', encoding='utf-8')

        print('\n')

        # Print each line in task_overview.txt to the screen.
        for line in task_overview:
            print(line.strip('\n'))      

        task_overview.close()

        # Print each line in user_overview.txt to the screen.
        user_overview = open('user_overview.txt', 'r', encoding='utf-8')

        print('\n')

        for line in user_overview:
            print(line.strip('\n'))

        user_overview.close()

    elif menu == 'e':
        print('Goodbye!!!')
        exit()

    else:
        print("You have made a wrong choice, Please Try again")  