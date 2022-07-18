class User:
    def __init__(self, username, wallet, balance):
        self.username = username
        self.wallet = int(wallet)
        self.balance = int(balance)

    def pay(self, amount, target_user):
        self.balance -= amount
        target_user.balance += amount

    def deposit(self, amount):
        self.balance += amount
        self.wallet -= amount

    def withdraw(self, amount):
        self.balance -= amount
        self.wallet += amount

    def work(self, time):
        self.balance += time * 8

    def str(self):
        return (
            f"User: {self.username}  Wallet: ${self.wallet}  Balance: ${self.balance}"
        )
