import time
import json
import os
from P0_User import User
import fileinput

global run
global curruser
global user_list
run = True
curruser = "Guest"


def main():
    global user_list
    read_data()
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
        for i in range(len(commands)):
            if command == commands[i]:
                print()
                currcommand = commands[i]
                run_command(currcommand)
                break
            elif command != commands[i] and i == len(commands) - 1:
                print(
                    "I'm sorry, that doesn't seem to be a valid command. Did you make sure to not type any spaces?"
                )


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


def get_curr_user(username):
    for i in range(len(user_list)):
        if username == user_list[i].username:
            return user_list[i]


def check_existing_user(username):
    global user_list
    users = user_list
    for i in range(len(user_list)):
        if username == users[i].username:
            return True
    return False


def change_data(user):
    file = open("data.csv", "r")
    lines = file.readlines()
    file.close()
    file = open("data.csv", "w")
    for line in lines:
        data = line.split(",")
        if user.username != data[0]:
            file.write(line)
    file.close()
    file = open("data.csv", "a")
    file.write(f"{user.username}, {user.wallet}, {user.balance}\n")
    file.close()


def check_login():
    global curruser
    if curruser == "Guest":
        return False
    else:
        return True


def contains_comma(word):
    for i in range(len(word)):
        if word[i] == ",":
            return True
    return False


def run_command(command):
    global curruser
    global user_list
    try:

        if command == "/help":
            print("/help - Displays the various commands available to use.")
            print("/balance - Check the current user's balance")
            print("/wallet - Check the current user's wallet")
            print(
                "/pay - Transfers money from your account to another registered user's"
            )
            print(
                "/withdraw - Withdraws money from the bank account and puts it into the current user"
            )
            print(
                "/deposit - Transfers money from the wallet to the current account's bank balance"
            )
            print("/login - Logs in to a created user")
            print("/display - Displays information of current user")
            print("/displayall - Displays the information of all users")
            print("/logout - Logs out of current user")
            print("/register - Creates a new user with a specified name")
            print("/work - Work a specified amount of hours for money.")
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

        elif command == "/pay":
            if check_login() == True:
                target = input("Enter the username whom you wish to send money to: >>>")
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
                amount = int(input("Enter the amount you wish to withdraw: >>>"))
                user = get_curr_user(curruser)
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
                amount = int(input("Enter the amount you wish to deposit: >>>"))
                user = get_curr_user(curruser)
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

                username = input("Please enter desired username: >>>")
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
                else:
                    print(
                        "User already exists or name is unavailable. Please try another username"
                    )

        elif command == "/work":
            if check_login() == False:
                print("You're not logged in!")
            else:
                user = get_curr_user(curruser)
                hours = int(input("How many hours would you like to work? >>>"))
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

    except AttributeError:
        print(
            "OOPS! Something went wrong. Maybe try logging out and logging back in? \nReturning to main page..."
        )
    except ValueError:
        print(
            "ERROR: Make sure you type int in int field and string in string field!\n Returning to main page..."
        )


main()
