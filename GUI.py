from tkinter import *
from FinTrinity import FinTrinity
from time import sleep


class GUI:
    def __init__(self):
        self.fin = FinTrinity()
        self.fin.read_config()
        row = 0

        self.window = Tk()
        self.window.title("FinTrinity")
        self.window.minsize(400, 0)

        lbl_username = Label(self.window, text="{} ({})".format(self.fin.user.name, self.fin.user.id))
        lbl_username.grid(sticky=N, column=0, row=row, columnspan=2)
        row += 1
        lbl_info = Label(self.window, justify=LEFT, text="Select a game in the list:").grid(sticky=W, column=0, row=row,
                                                                                            columnspan=2)
        row += 1

        self.select_value = IntVar()
        self.game_images = []
        self.checkboxes = []
        for idx, game in enumerate(self.fin.user.games):
            cbox = Checkbutton(self.window, text="{} ({})".format(game.title, game.id), variable=self.select_value,
                               onvalue=idx + 1, offvalue=0, command=self.game_select)
            cbox.grid(sticky=W, column=1, row=row)
            self.checkboxes.append(cbox)
            self.game_images.append(PhotoImage(file=game.image))
            row += 1

        self.game_canvas = Canvas(self.window, width=144, height=80)
        self.game_image = None
        self.game_canvas.grid(sticky=E, column=0, row=2, columnspan=1, rowspan=row - 2)
        row += 1

        self.btn_confirm = Button(self.window, text="Confirm", state=DISABLED, command=self.click_confirm)
        self.btn_confirm.grid(column=0, row=row, columnspan=2)
        row += 1
        self.lbl_info = Label(self.window, text="")
        self.lbl_info.grid(column=0, row=row, columnspan=2)

        self.select_value.set(1)
        self.game_select()

        self.window.mainloop()

    def game_select(self):
        idx = self.select_value.get()
        if idx == 0:
            self.game_canvas.delete("all")
            self.game_image = None
            self.fin.game = None
        else:
            idx -= 1
            self.fin.game = self.fin.user.games[idx]
            if self.game_image is None:
                self.game_image = self.game_canvas.create_image(0, 0, anchor=NW, image=None)
            self.game_canvas.itemconfig(self.game_image, image=self.game_images[idx])
        if self.fin.game is None:
            self.btn_confirm.configure(state=DISABLED)
        else:
            self.btn_confirm.configure(state=NORMAL)
        self.window.update()

    def click_confirm(self):
        if self.fin.game is None:
            return
        for cbox in self.checkboxes:
            cbox.configure(state=DISABLED)
        self.btn_confirm.configure(text="Patching...")
        self.btn_confirm.configure(state=DISABLED)
        self.window.update()
        self.fin.setup_dirs()
        self.fin.backup_game()
        self.fin.download_dependencies()
        self.fin.hack()
        self.btn_confirm.configure(text="Finished!")
        self.btn_confirm.configure(state=DISABLED, command=self.window.destroy)
        self.lbl_info.config(text="Please refresh your QCMA database!")
        self.window.update()


gui = GUI()
