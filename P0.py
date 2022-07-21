import time
from P0_User import User
from P0_helper_methods import (
    count_spaces,
    command_base,
    separate_args,
    remove_space,
    change_data,
    contains_comma,
)

global run
global curruser
global user_list
run = True
curruser = "Guest"


def main():
    global user_list
    try:
        read_data()
    except ValueError:
        print(
            "Oops! It looks like the file is corrupted. Delete the file and rerun the program to continue."
        )
    commands = [
        "/help",
        "/balance",
        "/wallet",
        "/pay",
        "/withdraw",
        "/deposit",
        "/login",
        "/display",
        "/displayall",
        "/logout",
        "/register",
        "/work",
        "/exit",
    ]
    print(
        "Welcome to the not very secure banking app. For a list of commands, please type /help."
    )
    while run:
        time.sleep(0.1)
        command = ""
        command = input(f"\nWhat would you like to do, {curruser}? >>> ")
        print()
        if (
            command_base(command) == "/login"
            or command_base(command) == "/withdraw"
            or command_base(command) == "/deposit"
            or command_base(command) == "/register"
            or command_base(command) == "/work"
        ) and len(separate_args(command)) == 2:
            currcommand = separate_args(command)[0]
            arg1 = separate_args(command)[1]
            run_command(currcommand, arg1, 0)
        elif command[0:4] == "/pay" and len(separate_args(command)) == 3:
            currcommand = separate_args(command)[0]
            arg1 = separate_args(command)[1]
            arg2 = int(separate_args(command)[2])
            run_command(currcommand, arg1, arg2)
        else:
            currcommand = remove_space(command)
            run_command(currcommand, 0, 0)


# Function to see if the user is logged in. By default, the username is Guest, so when name = Guest, user is not logged in.
def check_login():
    global curruser
    if curruser == "Guest":
        return False
    else:
        return True


# Function to convert all the data in the data.csv file into User objects that we can interact with.
def read_data():
    global user_list
    user_list = []
    # We have to make sure a file called data.csv exists, so a simple open and close would do the trick.
    file = open("data.csv", "a")
    file.close()
    file = open("data.csv", "r")
    for line in file:
        if not line.isspace():
            str_list = line.split(",")
            username = str_list[0]
            wallet = str_list[1]
            balance = str_list[2]
            user = User(username, wallet, balance)
            user_list.append(user)
    file.close()


# Function to convert the current logged in user STRING into an object in the csv with the same username.
def get_curr_user(username):
    for i in range(len(user_list)):
        if username == user_list[i].username:
            return user_list[i]


# Function for registering that checks if the name inputted is unique.
def check_existing_user(username):
    global user_list
    users = user_list
    for i in range(len(user_list)):
        if username == users[i].username:
            return True
    return False


# Big function to run the command user inputs.
def run_command(command, arg1, arg2):
    global curruser
    global user_list
    try:

        if command == "/help":
            print("/help - Displays the various commands available to use.")
            print("/balance - Check the current user's balance")
            print("/wallet - Check the current user's wallet")
            print(
                "/pay or /pay [user] [amount] - Transfers money from your account to another registered user's"
            )
            print(
                "/withdraw or /withdraw [amount] - Withdraws money from the bank account and puts it into the current user"
            )
            print(
                "/deposit or /deposit [amount] - Transfers money from the wallet to the current account's bank balance"
            )
            print("/login or /login [username] - Logs in to a created user")
            print("/display - Displays information of current user")
            print("/displayall - Displays the information of all users")
            print("/logout - Logs out of current user")
            print(
                "/register or /register [name] - Creates a new user with a specified name"
            )
            print(
                "/work or /work [hours] - Work a specified amount of hours for money."
            )
            print("/exit - Closes the program")

        elif command == "/balance":
            if check_login() == True:
                user = get_curr_user(curruser)
                print(f"Bank balance: ${user.balance}")
            else:
                print("Not logged in!")

        elif command == "/wallet":
            if check_login() == True:
                user = get_curr_user(curruser)
                print(f"Wallet: ${user.wallet}")
            else:
                print("Not logged in!")

        elif command[0:4] == "/pay":
            if check_login() == True:
                if arg1 != 0 and arg2 != 0:
                    user = get_curr_user(curruser)
                    if check_existing_user(arg1) == False:
                        print("That user does not exist!")
                    else:
                        if arg2 <= user.balance:
                            target_user = get_curr_user(arg1)
                            user.pay(arg2, target_user)
                            print(f"Sucessfully paid ${arg2} to {arg1}")
                            change_data(user)
                            change_data(target_user)
                        else:
                            print("Amount exceeds balance")
                else:
                    target = input(
                        "Enter the username whom you wish to send money to: >>>"
                    )
                    if check_existing_user(target) == False:
                        print("That user does not exist!")
                    else:
                        amount = int(
                            input("Enter how much money you would like to send: >>>")
                        )
                        user = get_curr_user(curruser)
                        target_user = get_curr_user(target)
                        if amount <= user.balance:
                            user.pay(amount, target_user)
                            print(f"Successfully paid ${amount} to {target}")
                            change_data(user)
                            change_data(target_user)
                        else:
                            print("Amount exceeds balance.")
            else:
                print("You are not logged in!")

        elif command == "/withdraw":
            if check_login() == True:
                user = get_curr_user(curruser)
                if arg1 != 0:
                    amount = int(arg1)
                    if amount > user.balance:
                        print("Amount exceeds balance")
                    else:
                        user.withdraw(amount)
                        print(f"Sucessfully witthdrew ${amount}")
                        change_data(user)
                else:
                    amount = int(input("Enter the amount you wish to withdraw: >>>"))
                    if amount > user.balance:
                        print("Amount exceeds balance")
                    else:
                        user.withdraw(amount)
                        print(f"Sucessfully withdrew ${amount}")
                        change_data(user)
            else:
                print("Not logged in!")

        elif command == "/deposit":
            if check_login() == True:
                user = get_curr_user(curruser)
                if arg1 != 0:
                    amount = int(arg1)
                    if amount > user.wallet:
                        print("Amount exceeds wallet!")
                    else:
                        user.deposit(amount)
                        print(f"Sucessfully deposited ${amount}")
                        change_data(user)
                else:
                    amount = int(input("Enter the amount you wish to deposit: >>>"))
                    if amount > user.wallet:
                        print("Amount exceeds wallet!")
                    else:
                        user.deposit(amount)
                        print(f"Sucessfully deposited ${amount}")
                        change_data(user)
            else:
                print("Not logged in!")

        elif command == "/login":
            if check_login() == True:
                print("Already logged in!")
            else:
                if arg1 != 0:
                    if check_existing_user(arg1):
                        curruser = arg1
                        print("Logged in sucessfully!")
                    else:
                        print("This user does not exist. Did you mean /register?")
                else:
                    username = input("Enter the username: >>>")
                    if check_existing_user(username):
                        curruser = username
                        print("Logged in sucessfully!")
                    else:
                        print("This user does not exist. Did you mean /register? ")

        elif command == "/display":
            if check_login() == False:
                print("Not logged in!")
            else:
                user = get_curr_user(curruser)
                print(user.str())

        elif command == "/displayall":
            for elem in user_list:
                if elem.username != "Guest":
                    print(elem.str())

        elif command == "/logout":
            if check_login() == False:
                print("User not logged in")
            else:
                curruser = "Guest"
                print("Logged out successfully!")

        elif command == "/register":
            registering = True
            while registering:

                if arg1 == 0:
                    username = input("Please enter desired username: >>>")
                else:
                    username = arg1
                if (
                    check_existing_user(username) == False
                    and contains_comma(username) == False
                ):
                    user = User(username, 500, 0)
                    user_list.append(user)
                    with open("data.csv", "a") as file:
                        file.write(f"\n{username}, 500, 0")
                    print("User created sucessfully!")
                    curruser = user.username
                    registering = False
                elif (
                    check_existing_user(username) == True
                    or contains_comma(username) == True
                ) and arg1 == 0:
                    print(
                        "User already exists or name is unavailable. Please try another username"
                    )
                elif (
                    check_existing_user(username) == True
                    or contains_comma(username) == True
                ) and arg1 != 0:
                    print(
                        "User already exists or name is unavailable. Please try another username"
                    )
                    registering = False

        elif command == "/work":
            if check_login() == False:
                print("You're not logged in!")
            else:
                user = get_curr_user(curruser)
                if arg1 == 0:
                    hours = int(input("How many hours would you like to work? >>>"))
                else:
                    hours = int(arg1)
                if hours > 8:
                    print(
                        "You can't work that much! Your boss does not like to pay overtime!"
                    )
                elif hours < 0:
                    print("You can't work negative hours!")
                else:
                    for i in range(hours):
                        print("Working...")
                        time.sleep(2)
                    income = hours * 8
                    user.work(hours)
                    print(
                        f"*{user.username} worked for {hours} hours at $8 an hour and gained ${income}*"
                    )
                    change_data(user)

        elif command == "/exit":
            print("The program will now terminate")
            global run
            run = False

        else:
            print(
                "I'm sorry, that doesn't seem to be a valid command. Type /help for a list of commands along with proper usage."
            )

    except AttributeError:
        print(
            "OOPS! Something went wrong. Maybe try logging out and logging back in? \nReturning to main page..."
        )
    except ValueError:
        print(
            "ERROR: Make sure you type int in int field and string in string field!\n Returning to main page..."
        )


main()
