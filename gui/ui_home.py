import tkinter as tk
import tkinter.font as font


class HomePage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        header_font = font.Font(family='Times New Roman', size=16, weight='bold')
        other_font = font.Font(family='Times New Roman', size=12, weight='bold')

        label_title = tk.Label(self, text="TEXT ENCRYPTION AND DECRYPTION APPLICATION\n"
                                          "USING ELLIPTIC CURVE CRYPTOGRAPHY\n"
                                          "AND PAILLIER CRYPTOSYSTEM")
        label_title['font'] = header_font
        label_title.pack(pady=70)
        label_title.configure(bg="LightSkyBlue2")

        author_label = tk.Label(self, text="Dibuat Oleh\n"
                                           "Slamet Sumasto\n"
                                           "1901510125")
        author_label['font'] = other_font
        author_label.pack(pady=15)
        author_label.configure(bg="LightSkyBlue2")

        author_label_cont = tk.Label(self, text="BINUS University\n"
                                                "2020")
        author_label_cont['font'] = other_font
        author_label_cont.pack(pady=45)
        author_label_cont.configure(bg="LightSkyBlue2")
