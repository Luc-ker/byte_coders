import tkinter as tk
from tkinter import filedialog
import get_receipt
import ocr
import code_send
from random import randint
import sqlMethod
import csv

class App():
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Auto Shopping List")
        self.root.geometry("512x512")
        self.root.resizable(False, False)
        
        self.menu_bar = tk.Menu(self.root)
        options_menu = tk.Menu(self.menu_bar, tearoff=0)
        options_menu.add_command(label="Upload Reciept", command=self.upload_reciept)
        options_menu.add_command(label="Show Groups", command=self.show_group_frame)
        options_menu.add_command(label="Create New Group", command=self.show_group_create_frame)
        options_menu.add_command(label="Generate Shopping List", command=self.show_shop_frame)
        options_menu.add_command(label="Logout", command=self.show_login_frame)

        self.menu_bar.add_cascade(label="Options", menu=options_menu)

        # self.uname = "a"
        # self.show_menu_bar()
        # self.current_frame = GroupCreatorFrame(self)
        self.current_frame = LoginFrame(self)
        self.clear_user()

        self.root.mainloop()

    def upload_reciept(self):
        if type(self.current_frame) == MainFrame:
            return
        else:
            self.current_frame.destroy()
            self.current_frame = MainFrame(self)

    def show_group_frame(self):
        if type(self.current_frame) == GroupFrame:
            return
        else:
            self.current_frame.destroy()
            self.current_frame = GroupFrame(self)

    def show_group_create_frame(self):
        if type(self.current_frame) == GroupCreatorFrame:
            return
        else:
            self.current_frame.destroy()
            self.current_frame = GroupCreatorFrame(self)
            
    def show_shop_frame(self):
        if type(self.current_frame) == ShoppingListFrame:
            return
        else:
            self.current_frame.destroy()
            self.current_frame = ShoppingListFrame(self)

    def show_login_frame(self):
        if type(self.current_frame) == LoginFrame:
            return
        else:
            self.hide_menu_bar()
            self.clear_user()
            self.current_frame.destroy()
            self.current_frame = LoginFrame(self)

    def create_acc_frame(self):
        if type(self.current_frame) == CreateAccFrame:
            return
        else:
            self.current_frame.destroy()
            self.current_frame = CreateAccFrame(self)

    def show_pword_frame(self, uname, email):
        if type(self.current_frame) == PasswordResetFrame:
            return
        else:
            self.current_frame.destroy()
            self.current_frame = PasswordResetFrame(self, uname, email)

    def show_menu_bar(self):
        self.root.config(menu=self.menu_bar)

    def hide_menu_bar(self):
        self.root.config(menu="")

    def init_user(self, uname, fname, lname):
        self.uname = uname
        self.fname = fname
        self.lname = lname

    def clear_user(self):
        self.fname = ""
        self.lname = ""


class SwitchableFrame():
    def __init__(self, app, color):
        if type(app) != App:
            raise TypeError("app isn't an app type!")
        self.app = app
        self.frame = tk.Frame(app.root, bg=color, width=512, height=512)
        self.items = []

    def destroy(self):
        self.frame.destroy()

    def pack(self):
        self.frame.pack(fill="both", expand=True)
        if type(self.items) == list and len(self.items) > 0:
            for item in self.items:
                item.pack()


class MainFrame(SwitchableFrame):
    def __init__(self, app):
        super(MainFrame, self).__init__(app, "red")
        msg = "Press Space to take an image and Esc to cancel."
        self.info_label = tk.Label(self.frame, text=msg)
        self.img_take = tk.Button(self.frame, text="Take image", command=self.take_image)
        self.img_upload = tk.Button(self.frame, text="Upload image", command=self.upload_image)
        self.output = tk.Label(self.frame, text="Your shopping list will show up below")
        self.items = [self.info_label, self.img_take, self.img_upload, self.output]
        self.create_labels()

        self.output_items = []
        self.pack()
        # self.process_image("bills_image/bill_1.JPG") # for testing purposes only

    def create_labels(self):
        self.item_label = tk.Label(self.frame, text="Item")
        self.days_label = tk.Label(self.frame, text="Days expected to last:")
        self.output_items = [self.item_label, self.days_label]

    def take_image(self):
        img_path = get_receipt.get_image()
        if img_path == "":
            return
        self.process_image(img_path)

    def upload_image(self):
        img_path = filedialog.askopenfilename()
        if img_path == "":
            return
        elif img_path[-4:].lower() == ".png" or img_path[-4:].lower() == ".jpg":
            print("valid image file")
            self.process_image(img_path)
        else:
            print("not an image file")
            return

    def process_image(self, img_path):
        for item in self.output_items:
            item.destroy()
        if ocr.process_image_for_ocr(img_path):
            self.create_labels()
            with open('bills_output/bill_items.csv', 'r') as file:
                reader = csv.reader(file)
                next(reader)
                self.rows = []
                # to do: add check to see if item is already in db
                # to insert proper default value for expiry date
                for i, row in enumerate(reader):
                    self.output_items.append(tk.Button(self.frame, text=f"{row[2]}",
                                                       command=lambda i=i: self.edit_item(i)))
                    entry = tk.Entry(self.frame)
                    entry.insert(0, "0")
                    self.output_items.append(entry)
                    self.rows.append(row + ["", 0])
            self.output_items.append(tk.Button(self.frame, text="Save List",
                                                command=self.save_list))
            for i, item in enumerate(self.output_items):
                item.grid(row=len(self.items)+i//2, column=i%2)

    def edit_item(self, idx):
        btn = self.output_items[idx]
        item = tk.simpledialog.askstring(title="Change item name",
            prompt="What should this item be called?", initialvalue=btn.cget("text"))
        btn.configure(text=item)
        self.rows[idx][2] = item

    def save_list(self):
        day_counts = [x.get() for x in self.output_items[3::2]]
        if True in [x=="" for x in day_counts]:
            tk.messagebox.showinfo(title="Missing Details",
                message="Please fill out all the expected dates!")
        elif False in [x.isdigit() for x in day_counts]:
            tk.messagebox.showinfo(title="Invalid Number of Days",
                message="Days must be numbers greater than 0.")
        else:
            for i, days in enumerate(day_counts):
                self.rows[i][-1] = int(days)
            sqlMethod.insertBillItems(self.rows)
            self.app.show_group_frame()

    def pack(self):
        self.frame.pack(fill="both", expand=True)
        for item in self.items:
            item.grid(columnspan=2, padx=5, pady=2)


class UserFrame(SwitchableFrame):
    def __init__(self, app, color):
        super(UserFrame, self).__init__(app, color)
        self.uname_label = tk.Label(self.frame, text="Username: ")
        self.uname_box = tk.Entry(self.frame)
        self.pword_label = tk.Label(self.frame, text="Password: ")
        self.pword_box = tk.Entry(self.frame)
        self.items = [self.uname_label, self.uname_box, 
                      self.pword_label, self.pword_box]

    def pack(self):
        self.frame.pack(fill="both", expand=True)
        for i, item in enumerate(self.items):
            item.grid(row=i//2, column=i%2)


class LoginFrame(UserFrame):
    def __init__(self, app):
        super(LoginFrame, self).__init__(app, "yellow")
        self.create_btn = tk.Button(self.frame, text="Create Account", command=self.create_acc_frame)
        self.login_btn = tk.Button(self.frame, text="Login", command=self.check_details)
        self.items = self.items + [self.create_btn, self.login_btn]
        self.frame.columnconfigure(2, weight = 1)
        self.frame.rowconfigure(2, weight = 1)
        self.pack()

    def check_details(self):
        uname = self.uname_box.get()
        pword = self.pword_box.get()
        if uname == "" or pword == "":
            tk.messagebox.showinfo(title="Invalid credentials",
                message="Please enter your details!")
            return
        elif not sqlMethod.userReged(uname):
            if tk.messagebox.askyesno("Invalid credentials",
                    "You aren't registered. Register?"):
                self.create_acc_frame()
            return
        res = sqlMethod.getUserDetails(uname, pword)
        if len(res) == 0:
            tk.messagebox.showinfo(title="Invalid credentials",
                message="Invalid username or password!")
            return
        uname, fname, lname = res
        self.login(uname, fname, lname)

    def login(self, uname, fname, lname):
        self.app.init_user(uname, fname, lname)
        self.app.show_menu_bar()
        self.app.upload_reciept()

    def create_acc_frame(self):
        self.app.create_acc_frame()


class CreateAccFrame(UserFrame):
    def __init__(self, app):
        super(CreateAccFrame, self).__init__(app, "yellow")
        self.fname_label = tk.Label(self.frame, text="First name: ")
        self.fname_box = tk.Entry(self.frame)
        self.lname_label = tk.Label(self.frame, text="Last name: ")
        self.lname_box = tk.Entry(self.frame)
        self.email_label = tk.Label(self.frame, text="Email: ")
        self.email_box = tk.Entry(self.frame)
        self.login_btn = tk.Button(self.frame, text="Go to Login", command=self.show_login_frame)
        self.create_btn = tk.Button(self.frame, text="Create Account", command=self.check_details)
        self.items = [self.fname_label, self.fname_box,
                      self.lname_label, self.lname_box, self.email_label,
                      self.email_box] + self.items + [self.login_btn, self.create_btn]
        self.pack()

    def check_details(self):
        fields = [x.get() for x in self.items[1:10:2]]
        if True in [x == "" for x in fields]:
            tk.messagebox.showinfo(title="Incomplete Details",
                message="Please enter all the boxes.")
        elif max([len(x) for x in fields[0:2] + fields[3:]]) > 30:
            tk.messagebox.showinfo(title="Details too long",
                message="The length of your name/credentials are too long!")
        elif len(fields[2]) > 50 or not code_send.valid_email(fields[2]):
            tk.messagebox.showinfo(title="Invalid Email",
                message="Please enter a valid email.")
        else:
            self.check_uname()

    def check_uname(self):
        uname = self.uname_box.get()
        if sqlMethod.userReged(uname):
            if tk.messagebox.askyesno("Registered User",
                    '''There is already an account with this username.
                    Would you like to login?'''):
                self.show_login_frame()
            else:
                if tk.messagebox.askyesno("Reset password?",
                        "Would you like to reset your password?"):
                    self.show_pword_frame(uname, sqlMethod.getUserEmail(uname))
        else:
            self.create_acc(uname)

    def create_acc(self, uname):
        pword = self.pword_box.get()
        fname = self.fname_box.get()
        lname = self.lname_box.get()
        email = self.email_box.get()
        sqlMethod.newUser(fname, lname, uname, pword, email)
        tk.messagebox.showinfo(title="Account Created",
            message="You have successfully created an account!")
        self.show_login_frame()

    def show_login_frame(self):
        self.app.show_login_frame()

    def show_pword_frame(self, uname, email):
        self.app.show_pword_frame(uname, email)


class PasswordResetFrame(SwitchableFrame):
    def __init__(self, app, uname, email):
        if type(app) != App:
            raise TypeError("app isn't an app type!")
        self.app = app
        self.frame = tk.Frame(app.root)
        self.uname = uname
        self.code = str(randint(100000, 999999))
        code_send.main(email, self.code)

        self.code_label = tk.Label(self.frame, text="Code: ")
        self.code_box = tk.Entry(self.frame)
        self.pword_label = tk.Label(self.frame, text="New Password: ")
        self.pword_box = tk.Entry(self.frame)
        self.validate_btn = tk.Button(self.frame, text="Reset Password", command=self.validate)
        self.items = [self.code_label, self.code_box, self.pword_label, self.pword_box, self.validate_btn]
        self.pack()

    def validate(self):
        pword = self.pword_box.get()
        if self.code_box.get() != self.code:
            tk.messagebox.showinfo(title="Incorrect code",
                message="Incorrect code. Please try again.")
        elif pword == sqlMethod.getUserPassword(self.uname):
            tk.messagebox.showinfo(title="Invalid Password",
                message="That's your current password!")
        else:
            self.update_password(pword)

    def update_password(self, pword):
        sqlMethod.updatePassword(self.uname, pword)
        tk.messagebox.showinfo(title="Password Reset",
            message="Your password was successfully reset.")
        self.app.show_login_frame()


class GroupFrame(SwitchableFrame):
    def __init__(self, app):
        super(GroupFrame, self).__init__(app, "blue")
        self.label = tk.Label(self.frame, text="Groups that you're a part of:")
        self.items = [self.label]
        results = sqlMethod.getGroupData(self.app.uname)
        for row in results:
            self.items.append(tk.Label(self.frame, text=f"Group {row[0][2]}"))
            for user in row:
                self.items.append(tk.Label(self.frame, text=f"{user[0]} {user[1]}"))
        self.pack()
    

class GroupCreatorFrame(SwitchableFrame):
    def __init__(self, app):
        super(GroupCreatorFrame, self).__init__(app, "red")
        msg = "Select people to create a new group with."
        self.info_label = tk.Label(self.frame, text=msg)
        self.grp_name_label = tk.Label(self.frame, text="Group Name: ")
        self.grp_name_box = tk.Entry(self.frame)
        self.user_search_label = tk.Label(self.frame, text="Search for User: ")
        self.search = tk.StringVar(self.frame)
        self.user_search_box = tk.Entry(self.frame, textvariable=self.search)
        self.user_search_box.bind("<Key>", self.get_users)
        self.get_users()
        self.create_grp_btn = tk.Button(self.frame, text="Create Group", command=self.create_group)
        self.items = [self.info_label, self.grp_name_label, self.grp_name_box,
                      self.user_search_label, self.user_search_box] + self.users + [self.create_grp_btn]
        self.pack()
        
    def show_group_frame(self):
        self.app.show_group_frame()

    def get_users(self, event=None):
        if event is not None:
            for user in self.users:
                user.destroy()
            filter = self.user_search_box.get()
            if event.char == "\x08":
                filter = filter[:-1]
            else:
                filter += event.char
        else:
            filter = ""
        self.users = self.get_users_from_db(filter)
        if event is not None:
            self.pack(event)
            
    def get_users_from_db(self, filter=""):
        return [tk.Button(self.frame, text=f"{x[1]} {x[2]}", bg="white",
            command=lambda i=i: self.select_user(i)) for i,
            x in enumerate(sqlMethod.getOtherUserDetails(self.app.uname))
            if filter in f"{x[1]} {x[2]}"]   

    def select_user(self, idx):
        btn = self.users[idx]
        col = btn.cget("bg")
        if col == "green":
            btn.config(bg="white")
        else:
            btn.config(bg="green")

    def create_group(self):
        users = [[self.app.fname, self.app.lname]] + [x.cget("text").split(" ") for x in self.users
                 if x.cget("bg") == "green"]
        name = self.grp_name_box.get()
        if name.rstrip() == "":
            tk.messagebox.showinfo(title="Missing Group Name",
                message="You haven't made a group name...")
        elif len(users) == 0:
            tk.messagebox.showinfo(title="Invalid Group",
                message="That's not enough to form a group!")
        else:
            sqlMethod.newGroup(name, users)
            tk.messagebox.showinfo(title="Success",
                message="New group created!")
            self.show_group_frame()

    def pack(self, event=None):
        if event is not None:
            for i, item in enumerate(self.users):
                item.grid(row=(i+6)//2, column=i%2, padx=5, pady=2)
        else:
            self.frame.pack(fill="both", expand=True)
            self.items[0].grid(row=0, column=0, columnspan=2)
            for i, item in enumerate(self.items[1:]):
                item.grid(row=(i+2)//2, column=i%2, padx=5, pady=2)


class ShoppingListFrame(SwitchableFrame):
    def __init__(self, app):
        super(ShoppingListFrame, self).__init__(app, "red")
        self.item_label = tk.Label(self.frame, text="Item")
        self.date_label = tk.Label(self.frame, text="Expiry Date")
        self.price_label = tk.Label(self.frame, text="Price")
        self.items = [self.item_label, self.date_label, self.price_label]
        self.parse_data()
        self.pack()

    def parse_data(self):
        items = sqlMethod.urgentItems()
        total_price = 0
        for item in items:
            for i, attr in enumerate(item):
                if i == 2:
                    total_price += attr
                self.items.append(tk.Label(self.frame, text=f"{attr}"))
        self.items.append(tk.Label(self.frame, text="Total"))
        self.items.append(tk.Label(self.frame, text=f"{round(total_price, 2)}"))

    def pack(self):
        self.frame.pack(fill="both", expand=True)
        for i, item in enumerate(self.items):
            if item == self.items[-2]:
                item.grid(row=i//3, column=i%3, columnspan=2)
            elif item == self.items[-1]:
                item.grid(row=i//3, column=2)
            else:
                item.grid(row=i//3, column=i%3)        


class TestFrame(SwitchableFrame):
    def __init__(self, app):
        super(TestFrame, self).__init__(app, "blue")
        self.test_button = tk.Button(self.frame, text="Press me!")
        self.test_label = tk.Label(self.frame, text="Press me!")
        self.items = [self.test_button, self.test_label]
        self.pack()



if __name__ == "__main__":
    app = App()
