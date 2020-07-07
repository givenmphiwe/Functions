import datetime
# Functions 
def reg_user(user_names):
    registered = False
    new_user = open("user.txt","a")
    user_exists = None
    new_username = input("New Username: ")
    
    # Checks if user exists
    if new_username in user_names:
        user_exists = True
    
    while user_exists == True:
        if new_username in user_names:
            print("\nA user with that name already exists")
            new_username = input("New Username: ")
        else:
            user_exists = False
    # Registers new user
    while registered == False:
        new_password = input("New Password: ")
        new_password_confirm = input("Please confirm the new password: ")
        if new_password == new_password_confirm:
            new_user.write("\n{}, {}".format(new_username,new_password))
            registered = True
            print("\nUser Registered Successfully")
            new_user.close()
        else:
            print("\nThose passwords don't match")


# Displays stats
def show_stats():
    # Creates reports 
    generate_report()
    # Opens report files 
    with open("task_overview.txt","r") as file:
        task_report = file.readlines()
    
    with open("user_overview.txt","r") as file:
        user_report = file.readlines()
    # Outputting report files 
    print("\nTask Statistics\n")
    
    for line in task_report:
        print(line,end = "")
    
    print("\n\nUser Statistics\n")
    
    for line in user_report:
        print(line,end = "")


# Adds Task 
def add_task(user_names):
    task_entered = False
    while task_entered == False:
        task_user = input("\nWhich user is the task for: ")
        if task_user not in user_names:
            print("\nThat user does not exist")
        else:
            task_title = input("Title of the task: ")
            task_descrip = input("Description of task: ")
            task_due_date = input("Task due date: ")
            task_date = datetime.datetime.now().strftime("%d %b %Y")
            task_complete = "No"
            new_task = open("tasks.txt","a")
            new_task.write("\n{}, {}, {}, {}, {}, {}".format(task_user,task_title,
                        task_descrip,task_date,task_due_date,task_complete))
            task_entered = True
            print("\nNew Task successfully entered")
            new_task.close()


# Displays all tasks 
def view_all():
    all_tasks = open("tasks.txt","r")
    num = 1
    for line in all_tasks:
        temp = line.strip()
        temp = temp.split(", ")
        print("")
        print("{}   Task User              :{}".format(num,temp[0]))
        print("    Task Name              :{}".format(temp[1]))
        print("    Task Description       :{}".format(temp[2]))
        print("    Task Entry Date        :{}".format(temp[3]))
        print("    Task Due Date          :{}".format(temp[4]))
        print("    Task Completion Status :{}".format(temp[5]))
        num += 1
    all_tasks.close()


# Displays users tasks
def view_mine(username,user_names):
    with open("tasks.txt","r") as file:
        all_tasks = file.readlines()

    # Users task output
    num = 1
    count = 1
    all_tasks_copy = all_tasks.copy()
    user_tasks = []
    for line in all_tasks:
        temp = line.strip()
        temp = temp.split(", ")
        if username in line:
            print("")
            print("{}   Task User              :{}".format(num,temp[0]))
            print("    Task Name              :{}".format(temp[1]))
            print("    Task Description       :{}".format(temp[2]))
            print("    Task Entry Date        :{}".format(temp[3]))
            print("    Task Due Date          :{}".format(temp[4]))
            print("    Task Completion Status :{}".format(temp[5]))
            user_tasks.append(all_tasks_copy.pop(count - num))
            num += 1
        count += 1
    
    all_tasks = all_tasks_copy.copy()
    
    # Handles selecting task options =================
    print("\n* - Select a task using it's number")
    print("b - Back to main menu")
    choice = input(": ")
    
    # Handles choice of option =======================
    if choice == "b":
        return
    else:
        choice = int(choice) - 1
        if choice > len(user_tasks) - 1:
            print("\nThere is no task with that number")
        else:
            if "Yes" in user_tasks[choice]:
                print("\nThis task is already completed and can not be edited")
            else:
                print("\nm - Mark task as complete")
                print("e - Edit the task")
                choice_2 = input(": ")

                if choice_2 == "m":
                    mark_complete(all_tasks,choice,user_tasks)
                elif choice_2 == "e":
                    edit_task(all_tasks,choice,user_names,user_tasks)


# Mark task complete
def mark_complete(all_tasks,choice,user_tasks):
    user_tasks[choice] = user_tasks[choice].replace("No","Yes")
    
    # Adding users array with main array
    all_tasks.extend(user_tasks)
    
    # Splitting lines into list
    all_tasks_sorted = []
    for line in all_tasks:
        line = line.split(", ")
        all_tasks_sorted.append(line)
    
    # Sorts tasks output
    all_tasks_output = []
    all_tasks = sorted(all_tasks_sorted, key = lambda x: datetime.datetime.strptime(x[3],"%d %b %Y"))
    for array in all_tasks:
        array = ", ".join(array)
        all_tasks_output.append(array)

    # Output to tasks.txt 
    with open("tasks.txt","w") as file:
        file.writelines(all_tasks_output)
    
    print("\nTask marked as complete")


# Edit task
def edit_task(all_tasks,choice,user_names,user_tasks):
    # Input edit user choice
    edit_user_choice = input("\nWould you like to edit this tasks assigned user?\ny or n: ")
    
    # Handles edit user
    if edit_user_choice == "y":
        edited_user = input("New assigned user: ")
        if edited_user not in user_names:
            print("That user does not exist")
        else:
            edit_user(all_tasks,choice,user_names,user_tasks,edited_user)
    
    # Input edit date choice 
    edit_date_choice = input("\nWould you like to edit this tasks due date?\ny or n: ")

    if edit_date_choice == "y":
        edit_date(all_tasks,choice,user_names,user_tasks)


# Edit user 
def edit_user(all_tasks,choice,user_names,user_tasks,edited_user):
    user_tasks[choice] = user_tasks[choice].split(", ")
    user_tasks[choice][0] = edited_user
    user_tasks[choice] = ", ".join(user_tasks[choice])
        
    # Adding users array with main array 
    all_tasks_user = []
    all_tasks_user.extend(all_tasks)
    all_tasks_user.extend(user_tasks)

    # Splitting lines into list
    all_tasks_sorted = []
    for line in all_tasks_user:
        line = line.split(", ")
        all_tasks_sorted.append(line)

    # Sorts tasks output
    all_tasks_output = sorted(all_tasks_sorted,
    key = lambda x: datetime.datetime.strptime(x[3],"%d %b %Y"))
    all_tasks_output_user = []
    for array in all_tasks_output:
        array = ", ".join(array)
        all_tasks_output_user.append(array)
    
    with open("tasks.txt","w") as file:
        file.writelines(all_tasks_output_user)
    print("User assigned to task changed")


# Edit date
def edit_date(all_tasks,choice,user_names,user_tasks):
    # Handles edit date 
    edited_date = input("New due date: ")
    user_tasks[choice] = user_tasks[choice].split(", ")
    user_tasks[choice][4] = edited_date
    user_tasks[choice] = ", ".join(user_tasks[choice])
    
    # Adding users array with main array 
    all_tasks_date = []
    all_tasks_date.extend(all_tasks)
    all_tasks_date.extend(user_tasks)
    # Splitting lines into list
    all_tasks_sorted = []
    for line in all_tasks_date:
        line = line.split(", ")
        all_tasks_sorted.append(line)

    # Sorts tasks output 
    all_tasks_output = sorted(all_tasks_sorted,
    key = lambda x: datetime.datetime.strptime(x[3],"%d %b %Y"))
    all_tasks_output_date = []
    for array in all_tasks_output:
        array = ", ".join(array)
        all_tasks_output_date.append(array)
    with open("tasks.txt","w") as file:
        file.writelines(all_tasks_output_date)

# Generates reports 
def generate_report():
    # Generates task report
    with open("tasks.txt","r") as file:
        info = file.readlines()
    
    # Intialising counting variables
    num_of_tasks = 0
    num_of_complete_tasks = 0
    num_of_uncompleted_tasks = 0
    num_of_overdue_tasks = 0
    
    # Checking through tasks info
    for line in info:
        num_of_tasks += 1
        if "Yes" in line:
            num_of_complete_tasks += 1
        if "No" in line:
            num_of_uncompleted_tasks += 1
        line = line.split(", ")
        due_date = datetime.datetime.strptime(line[4],"%d %b %Y")
        date = datetime.datetime.now()
        line = ", ".join(line)
        if date > due_date:
            num_of_overdue_tasks += 1
    
    # Working out the percentages 
    percentage_incomplete = (num_of_uncompleted_tasks/num_of_tasks) * 100
    percentage_overdue = (num_of_overdue_tasks/num_of_tasks) * 100
    
    # Creating report output list
    tasks_report_output = ["Total tasks\t\t\t:" + str(num_of_tasks) + "\n",
                        "Completed tasks\t\t\t:" + str(num_of_complete_tasks) + "\n",
                        "Uncompleted tasks\t\t:" + str(num_of_uncompleted_tasks) + "\n",
                        "Tasks overdue\t\t\t:" + str(num_of_overdue_tasks) + "\n",
                        "Percentage of incomplete tasks\t:" +
                        str(round(percentage_incomplete,1)) + "%\n",
                        "Percentage of overdue tasks\t:" +
                        str(round(percentage_overdue,1)) + "%"]
    
    # Adding text to the report file
    with open("task_overview.txt","w") as file:
        file.writelines(tasks_report_output)
    
    # Generates user report
    # Open file and create user list
    with open("user.txt","r") as file:
        user_info = file.readlines()

    num_users = 0
    users = ""
    for line in user_info:
        num_users += 1
        temp = line.split(", ")
        users += temp[0] + " "
    
    # Initialising list variables
    users = users.split()
    num_task_user_total_list = []
    num_task_user_list = []
    num_task_user_complete_list = []
    num_task_user_incomplete_list = []
    num_task_user_over_list = []
    
    # Checking through each users info
    for user in users:
        num_task_user = 0
        num_task_user_complete = 0
        num_task_user_incomplete = 0
        num_task_user_over = 0
        for line in info:
            if user in line:
                num_task_user += 1
                if "Yes" in line:
                    num_task_user_complete += 1 
                if "No" in line:
                    num_task_user_incomplete += 1
                if "No" in line and date > due_date:
                    num_task_user_over += 1

        # Working out each users outputs
        if num_task_user > 0:
            percentage_user = (100/num_of_tasks) * num_task_user
            percentage_user_complete = (100/num_task_user) * num_task_user_complete
            percentage_user_incomplete = (100/num_task_user) * num_task_user_incomplete
            percentage_user_overdue = (100/num_task_user) * num_task_user_over
        else:
            percentage_user = 0
            percentage_user_complete = 0
            percentage_user_incomplete = 0
            percentage_user_overdue = 0
        
        # Creating lists of users outputs
        num_task_user_total_list.append(num_task_user)
        num_task_user_list.append(percentage_user)
        num_task_user_complete_list.append(percentage_user_complete)
        num_task_user_incomplete_list.append(percentage_user_incomplete)
        num_task_user_over_list.append(percentage_user_overdue)
    
    # Creating report output list 
    user_report_output = ["Total users\t\t\t:" + str(num_users) + "\n",
                        "Total tasks\t\t\t:" + str(num_of_tasks) + "\n",]

    # Creating each users report output list
    each_users_output = []
    count = 0
    for user in users:
        each_users_output.append("\n" + user +
                                "\nTasks assigned\t\t\t:" +
                                str(num_task_user_total_list[count]) +
                                "\nTasks assigned of total tasks\t:" +
                                str(round(num_task_user_list[count],1)) +
                                "%\nTasks assigned completed\t:" +
                                str(round(num_task_user_complete_list[count],1)) +
                                "%\nTasks assigned incomplete\t:" +
                                str(round(num_task_user_incomplete_list[count],1)) +
                                "%\nTasks assigned overdue\t\t:" +
                                str(round(num_task_user_over_list[count],1)) + "%\n"
                                )
        count += 1
    
    # Adding the text to the report file
    with open("user_overview.txt", "w") as file:
        file.writelines(user_report_output)
    
    with open("user_overview.txt","a") as file:
        file.writelines(each_users_output)
    
    # Terminal output
    print("\nReport Generated Successfully")
