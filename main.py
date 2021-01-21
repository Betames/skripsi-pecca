import tkinter as tk
import tkinter.messagebox as messagebox
from gui import ui_home, ui_ecc, ui_paillier, ui_about, ui_help
from algorithm.utilities import utilities


class MyApp(tk.Tk):

    def __init__(self, *args, **kwargs, ):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        menu = tk.Menu(container)

        pages = tk.Menu(menu, tearoff=0)
        menu.add_cascade(menu=pages, label="Pages")

        # pages.add_command(label="Home",
        #                   command=lambda: self.show_frame(ui_home.HomePage))
        # pages.add_separator()
        pages.add_command(label="Elliptic Curve Cryptography Algorithm",
                          command=lambda: self.show_frame(ui_ecc.EccPage))
        pages.add_command(label="Paillier Cryptosystem Algorithm",
                          command=lambda: self.show_frame(ui_paillier.PaillierPage))
        pages.add_separator()
        pages.add_command(label="Exit",
                          command=lambda: self.exit())

        helper_menu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(menu=helper_menu, label="Others")

        helper_menu.add_command(label="About",
                                command=lambda: self.show_frame(ui_about.AboutPage))
        helper_menu.add_command(label="Help",
                                command=lambda: self.show_frame(ui_help.HelpPage))

        tk.Tk.config(self, menu=menu)

        for F in (ui_home.HomePage, ui_ecc.EccPage, ui_paillier.PaillierPage, ui_about.AboutPage, ui_help.HelpPage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
            # frame.configure(bg="LightSkyBlue2")

        self.show_frame(ui_home.HomePage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()
        frame.configure(bg="LightSkyBlue2")

    def exit(self):
        if messagebox.askyesno("Exit", "Are you sure want to exit?"):
            self.quit()


if __name__ == "__main__":
    app = MyApp()
    app.geometry("800x500")
    app.title("Text Encryption and Decryption Application")
    icon = tk.PhotoImage(file=utilities.resource_path("img/icon.png"))
    app.iconphoto(False, icon)
    app.mainloop()
