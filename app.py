import tkinter as tk
from tkinter import filedialog
import get_receipt
import ocr

class App():
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Auto Shopping List")
        self.root.geometry("512x512")
        
        menu_bar = tk.Menu(self.root)
        options_menu = tk.Menu(menu_bar, tearoff=0)
        options_menu.add_command(label="Upload Reciept", command=self.upload_reciept)
        options_menu.add_command(label="Show groups", command=self.show_group_frame)
        options_menu.add_command(label="Show test frame", command=self.show_test_frame)

        menu_bar.add_cascade(label="Options", menu=options_menu)
        self.root.config(menu=menu_bar)

        self.current_frame = MainFrame(self.root)

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
