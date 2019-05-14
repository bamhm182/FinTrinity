from tkinter import *
from FinTrinity import FinTrinity
from time import sleep


class GUI:
    def __init__(self):
        self.fin = FinTrinity()
        self.fin.read_config()

        self.window = Tk()
        self.window.title("FinTrinity")
        self.window.minsize(250, 0)

        lbl_info = Label(self.window, text="I was able to find this game!\nPlease confirm it is correct.")
        lbl_info.pack(pady=10)

        lbl_username = Label(self.window, text=f"{self.fin.user.name} ({self.fin.user.id})")
        lbl_username.pack()

        lbl_game = Label(self.window, text=f"{self.fin.game.title} ({self.fin.game.id})")
        lbl_game.pack()
        
        canvas_game = Canvas(self.window, width=144, height=80)
        canvas_game.pack()
        img = PhotoImage(file=self.fin.game.image)
        canvas_game.create_image(0, 0, anchor=NW, image=img)

        self.txt_btn_confirm = StringVar()
        self.txt_btn_confirm.set("Confirm")

        btn_confirm = Button(self.window, textvariable=self.txt_btn_confirm, command=self.click_confirm)
        btn_confirm.pack(pady=10)

        self.window.mainloop()

    def click_confirm(self):
        if self.txt_btn_confirm.get() == "Confirm":
            self.txt_btn_confirm.set("Patching...")
            self.window.update()
            self.fin.setup_dirs()
            self.fin.backup_game()
            self.fin.download_dependencies()
            self.fin.hack()
            self.txt_btn_confirm.set("Finished!")
            lbl_refresh = Label(self.window, text="Please refresh your QCMA database!")
            lbl_refresh.pack(pady=10)


gui = GUI()
