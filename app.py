import tkinter as tk
from tkinter import filedialog
import get_receipt
import ocr
import code_send
from random import randint
import sqlMethod

class App():
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Auto Shopping List")
        self.root.geometry("512x512")
        
        self.menu_bar = tk.Menu(self.root)
        options_menu = tk.Menu(self.menu_bar, tearoff=0)
        options_menu.add_command(label="Upload Reciept", command=self.upload_reciept)
        options_menu.add_command(label="Show groups", command=self.show_group_frame)
        options_menu.add_command(label="Show test frame", command=self.show_test_frame)
        options_menu.add_command(label="Logout", command=self.show_login_frame)

        self.menu_bar.add_cascade(label="Options", menu=options_menu)

        self.current_frame = LoginFrame(self)
        self.clear_user()

        self.root.mainloop()

    def upload_reciept(self):
        if type(self.current_frame) == MainFrame:
            return
        else:
            self.current_frame.destroy()
            self.current_frame = MainFrame(self.root)

    def show_test_frame(self):
        if type(self.current_frame) == TestFrame:
            return
        else:
            self.current_frame.destroy()
            self.current_frame = TestFrame(self.root)

    def show_group_frame(self):
        if type(self.current_frame) == GroupFrame:
            return
        else:
            self.current_frame.destroy()
            self.current_frame = GroupFrame(self.root)

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

    def init_user(self, fname, lname):
        self.fname = fname
        self.lname = lname

    def clear_user(self):
        self.fname = ""
        self.lname = ""


class SwitchableFrame():
    def __init__(self, root, color):
        self.frame = tk.Frame(root, bg=color)
        self.items = []

    def destroy(self):
        self.frame.destroy()

    def pack(self):
        self.frame.pack()
        if type(self.items) == list and len(self.items) > 0:
            for item in self.items:
                item.pack()


class MainFrame(SwitchableFrame):
    def __init__(self, root):
        super(MainFrame, self).__init__(root, "red")
        msg = "Press Space to take an image and Esc to cancel."
        self.info_label = tk.Label(self.frame, text=msg)
        self.img_take = tk.Button(self.frame, text="Take image", command=self.take_image)
        self.img_upload = tk.Button(self.frame, text="Upload image", command=self.upload_image)
        self.items = [self.info_label, self.img_take, self.img_upload]
        self.pack()

    def take_image(self):
        img_path = get_receipt.get_image()
        self.process_image(img_path)

    def upload_image(self):
        img_path = filedialog.askopenfilename()
        if img_path[-4:].lower() == ".png" or img_path[-4:].lower() == ".jpg":
            print("valid image file")
            self.process_image(img_path)
        else:
            print("not an image file")
            return

    def process_image(self, img_path):
        ocr.process_image_for_ocr(img_path)


class UserFrame(SwitchableFrame):
    def __init__(self, app, color):
        if type(app) != App:
            raise TypeError("app isn't an app type!")
        self.app = app
        self.frame = tk.Frame(app.root, bg=color)
        self.uname_label = tk.Label(self.frame, text="Username: ")
        self.uname_box = tk.Entry(self.frame)
        self.pword_label = tk.Label(self.frame, text="Password: ")
        self.pword_box = tk.Entry(self.frame)
        self.items = [self.uname_label, self.uname_box, 
                      self.pword_label, self.pword_box]

    def pack(self):
        self.frame.pack()
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
        fname, lname = res
        self.login(fname, lname)

    def login(self, fname, lname):
        self.app.init_user(fname, lname)
        self.app.show_menu_bar()
        self.app.show_group_frame()

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
    def __init__(self, root):
        super(GroupFrame, self).__init__(root, "blue")
        self.label = tk.Label(self.frame, text="Groups that you're a part of:")
        self.items = [self.label]
        self.pack()


class TestFrame(SwitchableFrame):
    def __init__(self, root):
        super(TestFrame, self).__init__(root, "blue")
        self.test_button = tk.Button(self.frame, text="Press me!")
        self.test_label = tk.Label(self.frame, text="Press me!")
        self.items = [self.test_button, self.test_label]
        self.pack()



if __name__ == "__main__":
    app = App()
