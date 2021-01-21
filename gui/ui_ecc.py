import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as messagebox
from tkinter import filedialog
from tkinter import scrolledtext
import tkinter.font as font
from algorithm.ecc_algorithm import ecc_class
# from algorithm.testing_ecc import *
from algorithm.utilities import utilities
from gui.tooltip import CreateToolTip
import time


class EccPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        header_font = font.Font(family='Times New Roman', size=16, weight='bold')
        text_font = font.Font(family='Times New Roman', size=12)

        self.ecc_label = tk.Label(self, text="Elliptic Curve Cryptography")
        self.ecc_label["font"] = header_font
        self.ecc_label.pack(padx=10)
        self.ecc_label.configure(bg="LightSkyBlue2")

        self.curve_label = tk.Label(self, text="E: y^2 = x^3 - 8x + 31 mod 65629")
        self.curve_label.pack(pady=5)
        self.curve_label.configure(bg="LightSkyBlue2")

        ecc_tabs = ttk.Notebook(self)

        # ECC ENCRYPTION TAB
        self.ecc_enc_tab = tk.Frame(ecc_tabs)
        self.ecc_enc_tab.configure(bg="LightSkyBlue2")

        self.input_text_button_enc = tk.Button(self.ecc_enc_tab, text='Input Text',
                                               command=lambda: self.input_text(
                                                   ecc_tabs.tab(ecc_tabs.select(), "text")))
        self.input_text_button_enc.grid(sticky="NSEW", row=0, column=0, columnspan=4, padx=20, pady=5)

        self.save_text_button_enc = tk.Button(self.ecc_enc_tab, text='Save Text',
                                              command=lambda: self.save_text(
                                                  ecc_tabs.tab(ecc_tabs.select(), "text")))
        self.save_text_button_enc.grid(sticky="NSEW", row=0, column=4, columnspan=4, padx=20, pady=5)

        self.ecc_enc_plaintextArea = scrolledtext.ScrolledText(self.ecc_enc_tab)
        self.ecc_enc_plaintextArea.configure(font=text_font, width=40, height=15, padx=10)
        self.ecc_enc_plaintextArea.grid(row=1, column=0, rowspan=5, columnspan=4, padx=20, pady=5)

        self.ecc_enc_ciphertextArea = scrolledtext.ScrolledText(self.ecc_enc_tab)
        self.ecc_enc_ciphertextArea.configure(font=text_font, width=40, height=15, padx=10)
        self.ecc_enc_ciphertextArea.grid(row=1, column=4, rowspan=5, columnspan=4, padx=20, pady=5)

        self.ecc_enc_key_label = tk.Label(self.ecc_enc_tab, text="Key")
        self.ecc_enc_key_label.grid(sticky="E", row=7, column=0)
        self.ecc_enc_key_label.configure(bg="LightSkyBlue2")

        self.ecc_priv_key = tk.IntVar()
        self.ecc_priv_key_entry = tk.Entry(self.ecc_enc_tab, textvariable=self.ecc_priv_key, show="*", width=10)
        self.ecc_priv_key_entry.delete("0", tk.END)
        self.ecc_priv_key_entry.grid(sticky="NSEW", row=7, column=1, padx=5, pady=5)
        self.ecc_priv_key_entry["state"] = "disabled"

        self.ecc_enc_key_tooltip = tk.Label(self.ecc_enc_tab, text='?')
        self.ecc_enc_key_tooltip['font'] = text_font
        self.ecc_enc_key_tooltip.grid(sticky="W", row=7, column=2, padx=5, pady=5)
        self.ecc_enc_key_tooltip.configure(bg="LightSkyBlue2")
        self.label_enc_tooltip = CreateToolTip(self.ecc_enc_key_tooltip,
                                               "Key must filled with integer.\n"
                                               "Integer must be greater than 0\n"
                                               "and less than 65538.\n"
                                               "Encryption and Decryption\n"
                                               "use same key.")

        self.show_icon = tk.PhotoImage(file=utilities.resource_path("img/show.png"))
        self.hide_icon = tk.PhotoImage(file=utilities.resource_path("img/hide.png"))
        self.ecc_enc_key_button = tk.Button(self.ecc_enc_tab, image=self.show_icon,
                                            command=lambda: self.show_hide_key(
                                                ecc_tabs.tab(ecc_tabs.select(), "text")))
        self.ecc_enc_key_button.configure(width=20, height=20, background='gray90')
        self.ecc_enc_key_button.grid(sticky="W", row=7, column=3, padx=5, pady=5)
        self.ecc_enc_key_button["state"] = "disabled"

        self.ecc_encrypt_button = tk.Button(self.ecc_enc_tab, text='Encrypt',
                                            command=lambda: self.ecc_encrypt(
                                                self.ecc_enc_plaintextArea.get("1.0", tk.END),
                                                ecc_class.random_k, self.ecc_priv_key.get(),
                                                ecc_class.random_index))
        # self.ecc_encrypt_button = tk.Button(self.ecc_enc_tab, text='Encrypt',
        #                                     command=lambda: self.ecc_encrypt(
        #                                         self.ecc_enc_plaintextArea.get("1.0", tk.END),
        #                                         5443, self.ecc_priv_key.get(),
        #                                         37347))
        self.ecc_encrypt_button.grid(sticky="NSEW", row=8, column=1, padx=5, pady=5)
        self.ecc_encrypt_button["state"] = "disabled"

        # ECC DECRYPTION TAB
        self.ecc_dec_tab = tk.Frame(ecc_tabs)
        self.ecc_dec_tab.configure(bg="LightSkyBlue2")

        self.input_text_button_dec = tk.Button(self.ecc_dec_tab, text='Input Text',
                                               command=lambda: self.input_text(
                                                   ecc_tabs.tab(ecc_tabs.select(), "text")))
        self.input_text_button_dec.grid(sticky="NSEW", row=0, column=0, columnspan=4, padx=20, pady=5)

        self.save_text_button_dec = tk.Button(self.ecc_dec_tab, text='Save Text',
                                              command=lambda: self.save_text(
                                                  ecc_tabs.tab(ecc_tabs.select(), "text")))
        self.save_text_button_dec.grid(sticky="NSEW", row=0, column=4, columnspan=4, padx=20, pady=5)

        self.ecc_dec_plaintextArea = scrolledtext.ScrolledText(self.ecc_dec_tab)
        self.ecc_dec_plaintextArea.configure(font=text_font, width=40, height=15, padx=10)
        self.ecc_dec_plaintextArea.grid(row=1, column=0, rowspan=5, columnspan=4, padx=20, pady=5)

        self.ecc_dec_deciphertextArea = scrolledtext.ScrolledText(self.ecc_dec_tab)
        self.ecc_dec_deciphertextArea.configure(font=text_font, width=40, height=15, padx=10)
        self.ecc_dec_deciphertextArea.grid(row=1, column=4, rowspan=5, columnspan=4, padx=20, pady=5)

        self.ecc_dec_key_label = tk.Label(self.ecc_dec_tab, text="Key")
        self.ecc_dec_key_label.grid(sticky="E", row=7, column=0)
        self.ecc_dec_key_label.configure(bg="LightSkyBlue2")

        self.ecc_dec_priv_key = tk.IntVar()
        self.ecc_dec_priv_key_entry = tk.Entry(self.ecc_dec_tab, textvariable=self.ecc_dec_priv_key,
                                               show="*", width=10)
        self.ecc_dec_priv_key_entry.delete("0", tk.END)
        self.ecc_dec_priv_key_entry.grid(sticky="NSEW", row=7, column=1, padx=5, pady=5)
        self.ecc_dec_priv_key_entry["state"] = "disabled"

        self.ecc_dec_key_tooltip = tk.Label(self.ecc_dec_tab, text='?')
        self.ecc_dec_key_tooltip['font'] = text_font
        self.ecc_dec_key_tooltip.grid(sticky="W", row=7, column=2, padx=5, pady=5)
        self.ecc_dec_key_tooltip.configure(bg="LightSkyBlue2")
        self.label_dec_tooltip = CreateToolTip(self.ecc_dec_key_tooltip,
                                               "Key must filled with integer.\n"
                                               "Integer must be greater than 0\n"
                                               "and less than 65538.\n"
                                               "Encryption and Decryption\n"
                                               "use same key.")

        self.ecc_dec_key_button = tk.Button(self.ecc_dec_tab, image=self.show_icon,
                                            command= lambda: self.show_hide_key(
                                                ecc_tabs.tab(ecc_tabs.select(), "text")))
        self.ecc_dec_key_button.configure(width=20, height=20, background='gray90')
        self.ecc_dec_key_button.grid(sticky="W", row=7, column=3, padx=5, pady=5)
        self.ecc_dec_key_button["state"] = "disabled"

        self.ecc_decrypt_button = tk.Button(self.ecc_dec_tab, text='Decrypt',
                                            command=lambda: self.ecc_decrypt(
                                                self.ecc_dec_plaintextArea.get("1.0", tk.END),
                                                ecc_class.random_k, self.ecc_dec_priv_key.get(),
                                                ecc_class.random_index))
        # self.ecc_decrypt_button = tk.Button(self.ecc_dec_tab, text='Decrypt',
        #                                     command=lambda: self.ecc_decrypt(
        #                                         self.ecc_dec_plaintextArea.get("1.0", tk.END),
        #                                         5443, self.ecc_dec_priv_key.get(),
        #                                         37347))
        self.ecc_decrypt_button.grid(sticky="NSEW", row=8, column=1, padx=5, pady=5)
        self.ecc_decrypt_button["state"] = "disabled"

        ecc_tabs.add(self.ecc_enc_tab, text='Encryption')
        ecc_tabs.add(self.ecc_dec_tab, text='Decryption')

        ecc_tabs.pack(anchor=tk.S)

    def show_hide_key(self, tab_index_text):
        if tab_index_text == "Encryption":
            if self.ecc_priv_key_entry.cget('show') == "*":
                self.ecc_priv_key_entry.configure(show="")
                self.ecc_enc_key_button.configure(image=self.hide_icon)
            elif self.ecc_priv_key_entry.cget('show') == "":
                self.ecc_priv_key_entry.configure(show="*")
                self.ecc_enc_key_button.configure(image=self.show_icon)
        elif tab_index_text == "Decryption":
            if self.ecc_dec_priv_key_entry.cget('show') == "*":
                self.ecc_dec_priv_key_entry.configure(show="")
                self.ecc_dec_key_button.configure(image=self.hide_icon)
            elif self.ecc_dec_priv_key_entry.cget('show') == "":
                self.ecc_dec_priv_key_entry.configure(show="*")
                self.ecc_dec_key_button.configure(image=self.show_icon)

    def input_text(self, tab_index_text):
        self.reset_all(tab_index_text)
        if tab_index_text == "Encryption":
            filename = filedialog.askopenfilename(
                initialdir="C:/Users/Slamet S D K/PycharmProjects/skripsi_final/input_text_files",
                title="Select a File",
                filetypes=(("Text files", "*.txt*"),))
            try:
                if filename:
                    self.ecc_encrypt_button["state"] = "normal"
                    self.ecc_priv_key_entry["state"] = "normal"
                    self.ecc_enc_key_button["state"] = "normal"
                    chosenFile = open(filename, 'r', encoding='utf-8')
                    text = chosenFile.read().replace("\n", " ")
                    text = text.rstrip("")
                    print(text)
                    self.ecc_enc_plaintextArea.insert(tk.END, text)
                    chosenFile.close()
                    print('Selected:', filename)
                    messagebox.showinfo("Success", "Successfully loaded!")
                elif filename == '':
                    messagebox.showinfo("Cancel", "Cancel choose file")
            except IOError:
                messagebox.showinfo("Error", "Could not open file!")
        else:
            filename = filedialog.askopenfilename(
                initialdir="C:/Users/Slamet S D K/PycharmProjects/skripsi_final/cipher_text_files/cipher_ecc",
                title="Select a File",
                filetypes=(("Text files", "*.txt*"),))
            try:
                if filename:
                    self.ecc_decrypt_button["state"] = "normal"
                    self.ecc_dec_priv_key_entry["state"] = "normal"
                    self.ecc_dec_key_button["state"] = "normal"
                    chosenFile = open(filename, 'r', encoding='utf-8')
                    text = chosenFile.read().replace("\n", " ")
                    text = text.rstrip("")
                    print(text)
                    self.ecc_dec_plaintextArea.insert(tk.END, text)
                    chosenFile.close()
                    print('Selected:', filename)
                    messagebox.showinfo("Success", "Successfully loaded!")
                elif filename == '':
                    messagebox.showinfo("Cancel", "Cancel choose file")
            except IOError:
                messagebox.showinfo("Error", "Could not open file!")

    def reset_all(self, tab_index_text):
        if tab_index_text == "Encryption":
            self.ecc_enc_plaintextArea.delete("1.0", tk.END)
            self.ecc_enc_ciphertextArea.delete("1.0", tk.END)
            self.ecc_priv_key_entry.delete("0", tk.END)

        elif tab_index_text == "Decryption":
            self.ecc_dec_plaintextArea.delete("1.0", tk.END)
            self.ecc_dec_deciphertextArea.delete("1.0", tk.END)
            self.ecc_dec_priv_key_entry.delete("0", tk.END)

    def save_text(self, tab_index_text):
        if tab_index_text == "Encryption":
            if str(self.ecc_enc_ciphertextArea.get('1.0', tk.END)).strip() == "":
                messagebox.showerror("Error", "There is no text to save")
            else:
                file_to_save = tk.filedialog.asksaveasfilename(
                    initialdir="C:/Users/Slamet S D K/PycharmProjects/skripsi_final/cipher_text_files/cipher_ecc",
                    defaultextension=".txt",
                    filetypes=(("Text files", "*.txt*"),))
                if not file_to_save:
                    messagebox.showinfo('Cancel', 'Cancel save file')
                else:
                    text = str(self.ecc_enc_ciphertextArea.get('1.0', tk.END))
                    f = open(file_to_save, 'w', encoding='utf-8')
                    f.write(text)
                    f.close()
                    tk.messagebox.showinfo('Success', 'Encrypted Text File Saved')
        elif tab_index_text == "Decryption":
            if str(self.ecc_dec_deciphertextArea.get('1.0', tk.END)).strip() == "":
                messagebox.showerror("Error", "There is no text to save")
            else:
                file_to_save = tk.filedialog.asksaveasfilename(
                    initialdir="C:/Users/Slamet S D K/PycharmProjects/skripsi_final/decipher_text_files/decipher_ecc",
                    defaultextension=".txt",
                    filetypes=(("Text files", "*.txt*"),))
                if not file_to_save:
                    messagebox.showinfo('Cancel', 'Cancel save file')
                else:
                    text = str(self.ecc_dec_deciphertextArea.get('1.0', tk.END))
                    f = open(file_to_save, 'w', encoding='utf-8')
                    f.write(text)
                    f.close()
                    tk.messagebox.showinfo('Success', 'Decrypted Text File Saved')

    def ecc_encrypt(self, plain, k, priv_key, random_idx):
        try:
            if priv_key > 65538 or priv_key < 1:
                messagebox.showerror("Error", "Private key value must be greater than 0 and less than 65538")
            else:
                start_time = time.time()
                self.ecc_enc_ciphertextArea.delete('1.0', tk.END)
                cipher = ecc_class.encryptTextECC(plain[:-1], k, priv_key, random_idx)
                self.ecc_enc_ciphertextArea.insert(tk.END, cipher)
                endTime = time.time()
                encrypt_time = utilities.calculateTime(start_time, endTime)
                messagebox.showinfo("Encryption Succeed", "Encrypt time is " + str(encrypt_time) + " second(s)")
        except ValueError:
            messagebox.showerror("Error", "Private key must be a number")

    def ecc_decrypt(self, cipher, k, priv_key, random_idx):
        try:
            if priv_key > 65538 or priv_key < 1:
                messagebox.showwarning("Warning", "Private key value must be greater than 0 and less than 65538")
            else:
                start_time = time.time()
                self.ecc_dec_deciphertextArea.delete('1.0', tk.END)
                decipher = ecc_class.decryptTextECC(cipher[:-2], k, priv_key, random_idx)
                self.ecc_dec_deciphertextArea.insert(tk.END, decipher)
                endTime = time.time()
                decrypt_time = utilities.calculateTime(start_time, endTime)
                messagebox.showinfo("Decryption Succeed", "Decrypt time is " + str(decrypt_time) + " second(s)")
        except ValueError:
            messagebox.showerror("Error", "Private key must be a number")
