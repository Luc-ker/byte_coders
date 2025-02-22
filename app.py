import tkinter as tk
from tkinter import filedialog
import get_receipt
import subprocess

class App():
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Auto Shopping List")
        self.root.geometry("512x512")
        
        menu_bar = tk.Menu(self.root)
        options_menu = tk.Menu(menu_bar, tearoff=0)
        options_menu.add_command(label="Upload Reciept", command=self.upload_reciept)
        options_menu.add_command(label="Show test frame", command=self.show_test_frame)

        menu_bar.add_cascade(label="Options", menu=options_menu)
        self.root.config(menu=menu_bar)

        self.current_frame = MainFrame(self.root)

        # self.frame.pack()


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

class MainFrame():
    def __init__(self, root):
        self.frame = tk.Frame(root, bg="red")
        msg = "Press Space to take an image and Esc to cancel."
        self.info_label = tk.Label(self.frame, text=msg)
        self.img_take = tk.Button(self.frame, text="Take image", command=self.take_image)
        self.img_upload = tk.Button(self.frame, text="Upload image", command=self.upload_image)
        self.items = [self.info_label, self.img_take, self.img_upload]
        self.pack()

    def take_image(self):
        get_receipt.get_image()

    def upload_image(self):
        file_path = filedialog.askopenfilename()
        if file_path[-4:] != ".png":
            print("not an image file")
            return true
        else:
            print("valid image file")
            return false

    def destroy(self):
        self.frame.destroy()

    def pack(self):
        self.frame.pack()
        for item in self.items:
            item.pack()


class TestFrame():
    def __init__(self, root):
        self.canvas = tk.Canvas(root, bg="blue")
        self.test_button = tk.Button(self.canvas, text="Press me!")
        self.test_label = tk.Label(self.canvas, text="Press me!")
        self.items = [self.test_button, self.test_label]
        self.pack()

    def destroy(self):
        self.canvas.destroy()

    def pack(self):
        self.canvas.pack()
        for item in self.items:
            item.pack()



if __name__ == "__main__":
    app = App()