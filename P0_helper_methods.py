from P0_User import User


def count_spaces(command):
    count = 0
    for elem in command:
        if elem == " ":
            count += 1
    return count


# Function to remove everything after the first word in command so something like /deposit 200 becomes just /deposit for sake of comparisons.
def command_base(command):
    try:
        index = command.index(" ")
    except ValueError:
        return command
    return command[:index]


# Function to separate arguments into separate parts as a list in case user inputs a command that supports more than one argument.
def separate_args(command):
    arg_list = []
    try:
        index = command.index(" ")
    except:
        return command
    arg_list.append(command[0:index])
    # index2 = command.index(" ", index + 1, len(command))
    if count_spaces(command) == 1:
        arg_list.append(command[index + 1 :])
    elif count_spaces(command) == 2:
        new_arg = command[index + 1 :]
        index2 = command.index(" ", index + 1, len(command))
        arg_list.append(command[index + 1 : index2])
        arg_list.append(command[index2 + 1 :])
    return arg_list


# Function for removing spaces in commands so /lo g i n would also work, etc.
def remove_space(command):
    return_word = ""
    for i in range(len(command)):
        if command[i] != " ":
            return_word += command[i]
    return return_word


# Function whenever data in the user changes, e.g when someone does /pay, it updates both the issuer and receiver.
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
    file = open("data.csv", "r")
    lines = file.readlines()
    file.close()
    file = open("data.csv", "a")
    file.write(f"{user.username}, {user.wallet}, {user.balance}\n")
    file.close()


# Function to check for comma's when registering. This is to prevent the csv to mess up with more commas than expected.
def contains_comma(word):
    for i in range(len(word)):
        if word[i] == ",":
            return True
    return False
