# INPUT
dataset = """Bob Ross,bross,/home/workspace/bross
Bill Nye,bnye,/home/workspace/scienceguy
Adam Smith,asmith,/home/workspace/asmith
"""

# OUTPUT
# Please match the following output (They are in sorted order):
#
# Adam Smith
#   username: asmith
#   directory: /home/workspace/asmith
#
# Bill Nye
#   username: bnye
#   directory: /home/workspace/scienceguy
#
# Bob Ross
#   username: bross
#   directory: /home/workspace/bross

class UserManager:
    """
    Store and manipulate data about users
    """

    def __init__(self, name, username, directory):
        self.name = name
        self.username = username
        self.directory = directory

        self.myDict = {}

    def add_user(self, name, username, directory):
        self.myDict[name] = [username, directory]
        

    def print_users(self):
        sorted_dict = sorted(self.myDict.items())
        for key,value in sorted_dict:
            print(key)
            print("   username: ", value[0])
            print("   directory: ", value[1])
            print("\n")

employees = UserManager("", "", "")

for line in dataset.split('\n'):
    items = line.split(',')
    if len(items) == 3:
        employees.add_user(items[0], items[1], items[2])

employees.print_users()