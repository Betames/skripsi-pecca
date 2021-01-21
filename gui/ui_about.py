import tkinter as tk
import tkinter.font as font
from tkinter import scrolledtext
from algorithm.utilities import utilities

class AboutPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        about_font = font.Font(family='Times New Roman', size=16, weight='bold')
        explanation_font = font.Font(family='Times New Roman', size=12)

        self.about_label = tk.Label(self, text="About Application")
        self.about_label['font'] = about_font
        self.about_label.pack(padx=10, pady=5)
        self.about_label.configure(bg="LightSkyBlue2")

        self.aboutTextArea = scrolledtext.ScrolledText(self, height=20, width=90, padx=10, pady=10)
        self.about_file = open(utilities.resource_path("assets/About.txt"), 'r')
        self.about_text = str(self.about_file.read())
        self.aboutTextArea.insert(tk.END, self.about_text)
        self.aboutTextArea.configure(font=explanation_font)
        self.aboutTextArea.pack(pady=10)
        self.about_file.close()
