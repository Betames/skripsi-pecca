import tkinter as tk
import tkinter.font as font
from tkinter import scrolledtext
from algorithm.utilities import utilities


class HelpPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        help_font = font.Font(family='Times New Roman', size=16, weight='bold')
        explanation_font = font.Font(family='Times New Roman', size=12)

        self.help_label = tk.Label(self, text="How to Use this Application")
        self.help_label["font"] = help_font
        self.help_label.pack(padx=10, pady=5)
        self.help_label.configure(bg="LightSkyBlue2")

        self.helpTextArea = scrolledtext.ScrolledText(self, height=20, width=90, padx=10, pady=10)
        self.help_file = open(utilities.resource_path("assets/Help.txt"), 'r')
        self.help_text = self.help_file.read()
        self.helpTextArea.insert(tk.END, self.help_text)
        self.helpTextArea.configure(font=explanation_font)
        self.helpTextArea.pack(pady=10)
        self.help_file.close()
