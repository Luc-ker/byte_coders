import sqlite3
conn = sqlite3.connect('example.db')
cursor = conn.cursor()
def setup():
    cursor.execute('''CREATE TABLE `groups` (
    `GroupID` int(11) PRIMARY KEY,
    `Name` varchar(30) DEFAULT NULL
    );''')
    cursor.execute('''
    CREATE TABLE `groupsusers` (
    `UserID` int(11) DEFAULT NULL,
    `GroupID` int(11) DEFAULT NULL,
    `guID` int(11) PRIMARY KEY,
    FOREIGN KEY (UserID) REFERENCES users(UserID),
    FOREIGN KEY (GroupID) REFERENCES groups(GroupID)
    );''')
    cursor.execute('''
    CREATE TABLE `item` (
    `ItemID` int(11) PRIMARY KEY,
    `Name` varchar(40) DEFAULT NULL,
    `Price` decimal(4,2) DEFAULT NULL,
    `Quantity` int(11) DEFAULT NULL
    );''')
    cursor.execute('''
    CREATE TABLE `shoppinglist` (
    `ListID` int(11) PRIMARY KEY,
    `GroupID` int(11) DEFAULT NULL,
    FOREIGN KEY (GroupID) REFERENCES groups(GroupID)
    );''')
    cursor.execute('''
    CREATE TABLE `shoppinglistitem` (
    `ItemID` int(11) DEFAULT NULL,
    `ListID` int(11) DEFAULT NULL,
    `DaysRemaining` int(11) DEFAULT NULL,
    `siID` int(11) PRIMARY KEY,
    FOREIGN KEY(ItemID) REFERENCES item(ItemID),
    FOREIGN KEY(ListID) REFERENCES shoppinglist(ListID)
    );''')
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
def newUser(fn, ln, id, un, pw):
    cursor.execute('''INSERT INTO users VALUES(?, ?, ?, ?, ?);'''), (fn, ln, id, un, pw)
