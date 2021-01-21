import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as messagebox
from tkinter import filedialog
from tkinter import scrolledtext
import tkinter.font as font
from algorithm.paillier_algorithm import paillier_class, paillier_priv_key, paillier_pub_key, paillier_r
# from algorithm.testing_paillier import *
from algorithm.utilities import utilities
import time


class PaillierPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        header_font = font.Font(family='Times New Roman', size=16, weight='bold')
        text_font = font.Font(family='Times New Roman', size=12)

        self.paillier_label = tk.Label(self, text="Paillier Cryptosystem")
        self.paillier_label["font"] = header_font
        self.paillier_label.pack(padx=10, pady=5)
        self.paillier_label.configure(bg="LightSkyBlue2")

        paillier_tabs = ttk.Notebook(self)

        # Paillier ENCRYPTION TAB
        self.paillier_enc_tab = tk.Frame(paillier_tabs)
        self.paillier_enc_tab.configure(bg="LightSkyBlue2")

        self.input_text_button_enc = tk.Button(self.paillier_enc_tab, text='Input Text',
                                               command=lambda: self.input_text(
                                                   paillier_tabs.tab(paillier_tabs.select(), "text")))
        self.input_text_button_enc.grid(sticky="NSEW", row=0, column=0, columnspan=2, padx=20, pady=5)

        self.save_text_button_enc = tk.Button(self.paillier_enc_tab, text='Save Text',
                                              command=lambda: self.save_text(
                                                  paillier_tabs.tab(paillier_tabs.select(), "text")))
        self.save_text_button_enc.grid(sticky="NSEW", row=0, column=3, columnspan=2, padx=20, pady=5)

        self.paillier_enc_plaintextArea = scrolledtext.ScrolledText(self.paillier_enc_tab)
        self.paillier_enc_plaintextArea.configure(font=text_font, width=40, height=15, padx=10)
        self.paillier_enc_plaintextArea.grid(row=1, column=0, rowspan=5, padx=20, pady=5)

        self.paillier_enc_ciphertextArea = scrolledtext.ScrolledText(self.paillier_enc_tab)
        self.paillier_enc_ciphertextArea.configure(font=text_font, width=40, height=15, padx=10)
        self.paillier_enc_ciphertextArea.grid(row=1, column=3, rowspan=5, padx=20, pady=5)

        self.paillier_encrypt_button = tk.Button(self.paillier_enc_tab, text='Encrypt',
                                                 command=lambda: self.paillier_encrypt(
                                                     str('' + self.paillier_enc_plaintextArea.get("1.0",
                                                                                                  tk.END)).rstrip(""),
                                                     paillier_pub_key, paillier_r))
        # self.paillier_encrypt_button = tk.Button(self.paillier_enc_tab, text='Encrypt',
        #                                          command=lambda: self.paillier_encrypt(
        #                                              str('' + self.paillier_enc_plaintextArea.get("1.0",
        #                                                                                           tk.END)).rstrip(""),
        #                                              pub, r))
        self.paillier_encrypt_button.grid(row=8, column=0, padx=5, pady=5)
        self.paillier_encrypt_button["state"] = "disabled"

        # PAILLIER DECRYPTION TAB
        self.paillier_dec_tab = tk.Frame(paillier_tabs)
        self.paillier_dec_tab.configure(bg="LightSkyBlue2")

        self.input_text_button_dec = tk.Button(self.paillier_dec_tab, text='Input Text',
                                               command=lambda: self.input_text(
                                                   paillier_tabs.tab(paillier_tabs.select(), "text")))
        self.input_text_button_dec.grid(sticky="NSEW", row=0, column=0, columnspan=2, padx=20, pady=5)

        self.save_text_button_dec = tk.Button(self.paillier_dec_tab, text='Save Text',
                                              command=lambda: self.save_text(
                                                  paillier_tabs.tab(paillier_tabs.select(), "text")))
        self.save_text_button_dec.grid(sticky="NSEW", row=0, column=3, columnspan=2, padx=20, pady=5)

        self.paillier_dec_plaintextArea = scrolledtext.ScrolledText(self.paillier_dec_tab)
        self.paillier_dec_plaintextArea.configure(font=text_font, width=40, height=15, padx=10)
        self.paillier_dec_plaintextArea.grid(row=1, column=0, rowspan=5, padx=20, pady=5)

        self.paillier_dec_deciphertextArea = scrolledtext.ScrolledText(self.paillier_dec_tab)
        self.paillier_dec_deciphertextArea.configure(font=text_font, width=40, height=15, padx=10)
        self.paillier_dec_deciphertextArea.grid(row=1, column=3, rowspan=5, padx=20, pady=5)

        self.paillier_decrypt_button = tk.Button(self.paillier_dec_tab, text='Decrypt',
                                                 command=lambda: self.paillier_decrypt(
                                                     str('' + self.paillier_dec_plaintextArea.get("1.0",
                                                                                                  tk.END)).rstrip(""),
                                                     paillier_priv_key))
        # self.paillier_decrypt_button = tk.Button(self.paillier_dec_tab, text='Decrypt',
        #                                          command=lambda: self.paillier_decrypt(
        #                                              str('' + self.paillier_dec_plaintextArea.get("1.0",
        #                                                                                           tk.END)).rstrip(""),
        #                                              priv))
        self.paillier_decrypt_button.grid(row=8, column=0, padx=5, pady=5)
        self.paillier_decrypt_button["state"] = "disabled"

        paillier_tabs.add(self.paillier_enc_tab, text='Encryption')
        paillier_tabs.add(self.paillier_dec_tab, text='Decryption')

        paillier_tabs.pack(anchor=tk.S, pady=10)

    def input_text(self, tab_index_text):
        self.reset_all(tab_index_text)
        if tab_index_text == "Encryption":
            filename = filedialog.askopenfilename(
                initialdir="C:/Users/Slamet S D K/PycharmProjects/skripsi_final/input_text_files",
                title="Select a File",
                filetypes=(("Text files", "*.txt*"),))
            try:
                if filename:
                    self.paillier_encrypt_button["state"] = "normal"
                    chosenFile = open(filename, 'r', encoding='utf-8')
                    text = chosenFile.read().replace("\n", "")
                    text = text.rstrip("")
                    # print(text)
                    self.paillier_enc_plaintextArea.insert(tk.END, text)
                    chosenFile.close()
                    print('Selected:', filename)
                    messagebox.showinfo("Success", "Successfully loaded!")
                elif filename == '':
                    messagebox.showinfo("Cancel", "Cancel choose file")
            except IOError:
                messagebox.showerror("Error", "Could not open file!")
        else:
            filename = filedialog.askopenfilename(
                initialdir="C:/Users/Slamet S D K/PycharmProjects/skripsi_final/cipher_text_files/cipher_paillier",
                title="Select a File",
                filetypes=(("Text files", "*.txt*"),))
            try:
                if filename:
                    self.paillier_decrypt_button["state"] = "normal"
                    chosenFile = open(filename, 'r', encoding='utf-8')
                    text = chosenFile.read().replace("\n", "")
                    text = text.rstrip("")
                    # print(text)
                    self.paillier_dec_plaintextArea.insert(tk.END, text)
                    chosenFile.close()
                    print('Selected:', filename)
                    messagebox.showinfo("Success", "Successfully loaded!")
                elif filename == '':
                    messagebox.showinfo("Cancel", "Cancel choose file")
            except IOError:
                messagebox.showerror("Error", "Could not open file!")

    def reset_all(self, tab_index_text):
        if tab_index_text == "Encryption":
            self.paillier_enc_plaintextArea.delete("1.0", tk.END)
            self.paillier_enc_ciphertextArea.delete("1.0", tk.END)

        elif tab_index_text == "Decryption":
            self.paillier_dec_plaintextArea.delete("1.0", tk.END)
            self.paillier_dec_deciphertextArea.delete("1.0", tk.END)

    def save_text(self, tab_index_text):
        if tab_index_text == "Encryption":
            if str(self.paillier_enc_ciphertextArea.get('1.0', tk.END)).strip() == "":
                messagebox.showerror("Error", "There is no text to save")
            else:
                file_to_save = tk.filedialog.asksaveasfilename(
                    initialdir="C:/Users/Slamet S D K/PycharmProjects/skripsi_final/cipher_text_files/cipher_paillier",
                    defaultextension=".txt",
                    filetypes=(("Text files", "*.txt*"),))
                if not file_to_save:
                    messagebox.showinfo('Cancel', 'Cancel save file')
                else:
                    text = str(self.paillier_enc_ciphertextArea.get('1.0', tk.END))
                    f = open(file_to_save, 'w', encoding='utf-8')
                    f.write(text)
                    f.close()
                    messagebox.showinfo('Success', 'Encrypted Text File Saved')
        elif tab_index_text == "Decryption":
            if str(self.paillier_dec_deciphertextArea.get('1.0', tk.END)).strip() == "":
                messagebox.showerror("Error", "There is no text to save")
            else:
                file_to_save = tk.filedialog.asksaveasfilename(
                    initialdir="C:/Users/Slamet S D K/PycharmProjects/skripsi_final/decipher_text_files"
                               "/decipher_paillier",
                    defaultextension=".txt",
                    filetypes=(("Text files", "*.txt*"),))
                if not file_to_save:
                    messagebox.showinfo('Cancel', 'Cancel save file')
                elif not file_to_save:
                    messagebox.showinfo("Cancel", "")
                else:
                    text = str(self.paillier_dec_deciphertextArea.get('1.0', tk.END))
                    f = open(file_to_save, 'w', encoding='utf-8')
                    f.write(text)
                    f.close()
                    messagebox.showinfo('Success', 'Decrypted Text File Saved')

    def paillier_encrypt(self, plain, pub, r):
        start_time = time.time()
        self.paillier_enc_ciphertextArea.delete('1.0', tk.END)
        cipher = paillier_class.encryptTextPaillier(plain, pub, r)
        # cipher = encryptTextPaillier(plain, pub, r)
        self.paillier_enc_ciphertextArea.insert(tk.END, cipher)
        endTime = time.time()
        encrypt_time = utilities.calculateTime(start_time, endTime)
        messagebox.showinfo("Encryption Succeed", "Encrypt time is " + str(encrypt_time) + " second(s)")

    def paillier_decrypt(self, cipher, priv):
        start_time = time.time()
        self.paillier_dec_deciphertextArea.delete('1.0', tk.END)
        decipher = paillier_class.decryptTextPaillier(cipher, priv)
        # decipher = decryptTextPaillier(cipher, priv)
        self.paillier_dec_deciphertextArea.insert(tk.END, decipher)
        endTime = time.time()
        decrypt_time = utilities.calculateTime(start_time, endTime)
        messagebox.showinfo("Decryption Succeed", "Decrypt time is " + str(decrypt_time) + " second(s)")
