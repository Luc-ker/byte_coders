import sqlite3
import datetime as dt

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
    `StoreID` VARCHAR(20) DEFAULT NULL,
    FOREIGN KEY (StoreID) REFERENCES stores(StoreID)
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
    #Stores - Stores name of store & ID
    cursor.execute('''CREATE TABLE `stores` (
    `StoreID` int(11) PRIMARY KEY,
    `Name` varchar(30) DEFAULT NULL
    );''')
    #Users - Stores information on each user
    cursor.execute('''
    CREATE TABLE `users` (
    `Firstname` varchar(30) DEFAULT NULL,
    `Lastname` varchar(30) DEFAULT NULL,
    `UserID` int(11) PRIMARY KEY,
    `Username` varchar(30) DEFAULT NULL,
    `Password` varchar(30) DEFAULT NULL,
    `Email` varchar(50) DEFAULT NULL
    );''')
    conn.commit()
    #cursor.execute('''INSERT INTO users VALUES('Brandon', 'Ryan-Izzard', '1', 'Brizzard', 'no')''')
    #cursor.execute('''SELECT * FROM users;''')
    #print(cursor.fetchall())
#setup()

#Creates new user
def newUser(fn, ln, un, pw, email):
    cursor.execute('''INSERT INTO users VALUES(?, ?, NULL, ?, ?, ?)''', (fn, ln, un, pw, email))
    id = cursor.lastrowid
    cursor.execute('''UPDATE users SET UserID = ?
                   WHERE Username = ? AND Password = ?''', [id, un, pw])
    conn.commit()

# function assumes that the user exists!
def userReged(un):
    cursor.execute(f'''SELECT Username FROM users WHERE Username = "{un}"''')
    res = cursor.fetchall()
    return len(res) > 0

def getUserEmail(un):
    cursor.execute(f'''SELECT Email FROM users WHERE Username = "{un}"''')
    return cursor.fetchall()[0][0]

def getUserDetails(un, pw):
    cursor.execute(f'''SELECT Username, Firstname, Lastname FROM users WHERE Username = "{un}" AND Password = "{pw}"''')
    res = cursor.fetchall()
    if len(res) > 0:
        return res[0]
    else:
        return res

def getOtherUserDetails(un):
    cursor.execute(f'''SELECT Username, Firstname, Lastname FROM users WHERE Username != "{un}"''')
    res = cursor.fetchall()
    return res

def getUserID(fname, lname):
    cursor.execute('''SELECT UserID FROM users WHERE Firstname = ?
                   AND Lastname = ?''', (fname, lname))
    return cursor.fetchall()[0][0]

def getUserPassword(un):
    cursor.execute(f'''SELECT Password FROM users WHERE Username = "{un}"''')
    return cursor.fetchall()[0][0]

def updatePassword(un, pw):
    cursor.execute('''UPDATE users SET Password = ? WHERE Username = ?''', (pw, un))
    conn.commit()


#Adds a new user to the group
def appendToGroup(userID, groupID):
    cursor.execute('''INSERT INTO groupsusers VALUES(?, ?, ?)''', (userID, groupID, None))
    id = cursor.lastrowid
    cursor.execute('''UPDATE groupsusers SET guID = ?
        WHERE UserID = ? AND GroupID = ?''', [id, userID, groupID])
    conn.commit()
    
#Creates a new group, then adds users to the group
def newGroup(gname, users):
    cursor.execute('''INSERT INTO groups VALUES(?, ?)''', (None, gname))
    groupID = cursor.lastrowid
    cursor.execute('''UPDATE groups SET GroupID = ?
        WHERE Name = ?''', [groupID, gname])
    conn.commit()
    for user in users:
        appendToGroup(getUserID(user[0], user[1]), groupID)

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

def getItemID(itemName, storeID):
    cursor.execute('''SELECT ItemID FROM item WHERE Name = ? AND StoreID = ?''', (itemName, storeID))
    res = cursor.fetchall()
    if len(res) > 0:
        return res[0][0]
    else:
        return res    

def itemExists(itemID, name, storeID):
    if itemID is not None:
        cursor.execute('''SELECT rowID FROM item WHERE ItemID = ?''', itemID)
    else:
        cursor.execute('''SELECT rowID FROM item WHERE Name = ?
                       AND StoreID = ?''', [name, storeID])
    res = cursor.fetchall()
    return len(res) > 0    
    
#Adds the csv contents into the Items table
#NOTE: Currently only works for format StoreID, ItemID, Name, Price
def insertBillItems(rows):
    for row in rows:
        cursor.execute('''SELECT StoreID FROM stores WHERE Name = ?''', [row[0]])
        row[0] = cursor.fetchall()[0][0]
        if row[0] != "aldi":
            row[1] = None
        row[-2] = dt.datetime.now().date()
        row[-1] = row[-2] + dt.timedelta(days=row[-1])
        if itemExists(row[1], row[2], row[0]):
            cursor.execute(f'''UPDATE item SET Price = ?, Last_Update = ?,
                           Expiry_Date = ?''', row[3:])
            conn.commit()
        else:
            cursor.execute(f'''INSERT INTO item (StoreID, ItemID,
                            Name, Price, Last_Update, Expiry_Date)
                            VALUES (?, ?, ?, ?, ?, ?)''', row)
            if row[0] != "aldi":
                id = cursor.lastrowid
                cursor.execute('''UPDATE item SET ItemID = ?
                    WHERE StoreID = ? AND Name = ?''', [id, row[0], row[2]])
                conn.commit()

def urgentItems():
    today = dt.datetime.now().date() + dt.timedelta(days=1)
    latest = today + dt.timedelta(days=3)
    cursor.execute('''SELECT Name, Expiry_Date, Price FROM item
                   WHERE Expiry_Date BETWEEN ? AND ?''',
                   (today, latest))
    return cursor.fetchall()

def getGroupData(un):
    cursor.execute('''
        SELECT groups.GroupID
        FROM groups
        INNER JOIN groupsusers ON groups.GroupID = groupsusers.GroupID
        INNER JOIN users ON users.UserID = groupsusers.UserID
        WHERE users.Username = ?''', (un))
    results = cursor.fetchall()
    if len(results) > 0:
        groups = []
        for res in results:
            cursor.execute('''
                SELECT users.Firstname, users.Lastname, groups.Name
                FROM users
                INNER JOIN groupsusers ON users.UserID = groupsusers.UserID
                INNER JOIN groups ON groupsusers.GroupID = groups.GroupID
                WHERE groups.GroupID = ?''', (res[0],))
            groups.append(cursor.fetchall())
        return groups
    else:
        return results

if __name__ == "__main__":
    # setup()
    # newUser("zebra", "giraffe", "test3", "test3", "lucker4889@gmail.com")
    print(getUserDetails("jlee4889", "test"))
    print(getUserDetails("a", "be"))

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
