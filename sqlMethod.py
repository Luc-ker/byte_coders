import sqlite3, csv
conn = sqlite3.connect('example.db')
cursor = conn.cursor()
#Creates whole database
#All primary keys are planned to simply be integers incremented by 1 as the number of items in a table grows.
def setup():
    #Groups - Stores name of group & ID
    cursor.execute('''CREATE TABLE `groups` (
    `GroupID` int(11) PRIMARY KEY,
    `Name` varchar(30) DEFAULT NULL
    );''')
    #GroupUsers - Links users to groups
    cursor.execute('''
    CREATE TABLE `groupsusers` (
    `UserID` int(11) DEFAULT NULL,
    `GroupID` int(11) DEFAULT NULL,
    `guID` int(11) PRIMARY KEY,
    FOREIGN KEY (UserID) REFERENCES users(UserID),
    FOREIGN KEY (GroupID) REFERENCES groups(GroupID)
    );''')
    #Item - Stores information on each item
    cursor.execute('''
    CREATE TABLE `item` (
    `ItemID` int(11) PRIMARY KEY,
    `Name` varchar(40) DEFAULT NULL,
    `Price` decimal(4,2) DEFAULT NULL,
    `Store` VARCHAR(20) DEFAULT NULL
    );''')
    #ShoppingList - Links groups to lists of items
    cursor.execute('''
    CREATE TABLE `shoppinglist` (
    `ListID` int(11) PRIMARY KEY,
    `GroupID` int(11) DEFAULT NULL,
    FOREIGN KEY (GroupID) REFERENCES groups(GroupID)
    );''')
    #ShoppingListItem - Links items to the list of items.
    cursor.execute('''
    CREATE TABLE `shoppinglistitem` (
    `ItemID` int(11) DEFAULT NULL,
    `ListID` int(11) DEFAULT NULL,
    `DaysRemaining` int(11) DEFAULT NULL,
    `siID` int(11) PRIMARY KEY,
    FOREIGN KEY(ItemID) REFERENCES item(ItemID),
    FOREIGN KEY(ListID) REFERENCES shoppinglist(ListID)
    );''')
    #Users - Stores information on each user
    cursor.execute('''
    CREATE TABLE `users` (
    `Firstname` varchar(30) DEFAULT NULL,
    `Lastname` varchar(30) DEFAULT NULL,
    `UserID` int(11) PRIMARY KEY,
    `Username` varchar(30) DEFAULT NULL,
    `Password` varchar(30) DEFAULT NULL
    );''')
    #cursor.execute('''INSERT INTO users VALUES('Brandon', 'Ryan-Izzard', '1', 'Brizzard', 'no')''')
    #cursor.execute('''SELECT * FROM users;''')
    #print(cursor.fetchall())
#setup()

#Creates new user
def newUser(fn, ln, id, un, pw):
    cursor.execute('''INSERT INTO users VALUES(?, ?, ?, ?, ?)''', (fn, ln, id, un, pw))
#Adds a new user to the group
def appendGroup(user, group, gID):
    cursor.execute('''INSERT INTO groupsusers VALUES(?, ?, ?)''', (user, group, gID))
#Creates a new group, then adds a user to the group
def newGroup(g, gname, user, gID):
    cursor.execute('''INSERT INTO groups VALUES(?, ?)''', (g, gname))
    appendGroup(user, g, gID)
#Adds a new item to a list
def appendList(iID, lID, days ,siID):
    cursor.execute('''INSERT INTO shoppingListItem VALUES(?, ?, ?, ?)''', (iID, lID, days, siID))
#Creates a new list, then adds an item to the list
def newList(lID, gID, iID, days, siID):
    cursor.execute('''INSERT INTO shoppingList VALUES(?, ?)''', (lID, gID))
    appendList(iID, lID, days, siID)
#Creates a new item
def newItem(iID, name, price, store):
    cursor.execute('''INSERT INTO item VALUES(?, ?, ?, ?)''', (iID, name, price, store))
#Adds the csv contents into the Items table
#NOTE: Currently only works for format StoreName, ID, Name, Price
def toDB():
    with open('bills_output\\bill_items.csv', 'r') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            cursor.execute('''INSERT INTO item(Store, ItemID, Name, Price) VALUES (?, ?, ?, ?)''', row)

#setup()
#toDB()
#cursor.execute('''SELECT * FROM item;''')
#print(cursor.fetchall())
#setup()
#newUser('Brandon', 'Ryan-Izzard', 1, 'Brizzard', 'no')
#newItem(1, "Milk", 2.05, 500)
#cursor.execute('''SELECT * FROM users;''')
#print(cursor.fetchall())
#cursor.execute('''SELECT * FROM item;''')
#print(cursor.fetchall())
