import json
from pathlib import Path

import customtkinter as ctk
from PIL import Image


class LoginFrame(ctk.CTkFrame):
    def __init__(self, master, on_login_success, **kwargs):
        super().__init__(master, **kwargs)
        self.on_login_success = on_login_success
        self.data = {}
        self.last_user = ""

        self.lbl_title = ctk.CTkLabel(
            self,
            text="Authentication",
            font=("Arial", 60, "bold"),
        )
        self.lbl_title.pack(padx=30, pady=(50, 40))

        self.etr_username = ctk.CTkEntry(
            self,
            placeholder_text="Username",
            font=("Arial", 15, "bold"),
            width=350,
            height=40,
        )
        self.etr_username.pack(padx=80, pady=5)
        self.etr_password = ctk.CTkEntry(
            self,
            placeholder_text="Password",
            show="*",
            font=("Arial", 15, "bold"),
            width=350,
            height=40,
        )
        self.etr_password.pack(padx=80, pady=5)

        self.checkbox_show_password = ctk.CTkCheckBox(
            self,
            text="Show password",
            font=("Arial", 15, "bold"),
            command=self.show_hide_password,
        )
        self.checkbox_show_password.pack(padx=80, pady=(10, 10))

        self.btn_login = ctk.CTkButton(
            self,
            text="Login",
            font=("Arial", 20, "bold"),
            command=self.login,
            width=200,
            height=40,
        )
        self.btn_login.pack(padx=25, pady=(20, 5))

        self.btn_sign_up = ctk.CTkButton(
            self,
            text="Sign up",
            font=("Arial", 20, "bold"),
            command=self.sign_up,
            width=200,
            height=40,
        )
        self.btn_sign_up.pack(padx=25, pady=5)

    def find_last_user(self):
        try:
            with open("source/data/last_user.txt", "r", encoding="utf-8") as fichier:
                self.last_user = fichier.read()
        except FileNotFoundError:
            print("Erreur : Le fichier last_user.txt est introuvable.")

    def welcome_back_last_user(self):
        self.find_last_user()
        if self.last_user != "":
            self.lbl_title.configure(text=f"Welcome back\n{self.last_user} !")
            self.etr_username.insert(0, self.last_user)
        else:
            self.lbl_title.configure(text="Authentication")

    def save_last_user(self, new_user):
        try:
            with open("source/data/last_user.txt", "w", encoding="utf-8") as fichier:
                fichier.write(new_user)
        except Exception as e:  # noqa: BLE001
            print("Erreur lors de l'enregistrement du dernier utilisateur :", e)

    def check_username_lenght(self, username):
        return not len(username) > 25

    def get_login_data(self):
        try:
            with open("source/data/users.json", "r", encoding="utf-8") as fichier:
                self.data = json.load(fichier)
        except FileNotFoundError:
            print("Erreur : Le fichier users.json est introuvable au chemin indiqué.")

    def save_login_data(self):
        try:
            Path("source/data").mkdir(exist_ok=True)

            with open("source/data/users.json", "w", encoding="utf-8") as fichier:
                json.dump(self.data, fichier, indent=4)
        except Exception as e:  # noqa: BLE001
            print("Erreur lors de l'enregistrement des tâches :", e)

    def show_hide_password(self):
        if self.checkbox_show_password.get() == 1:
            self.etr_password.configure(show="")
            self.checkbox_show_password.configure(text="Hide password")
        else:
            self.etr_password.configure(show="*")
            self.checkbox_show_password.configure(text="Show password")

    def login(self):
        username = self.etr_username.get()
        password = self.etr_password.get()

        self.get_login_data()

        if self.data != None and username in self.data:
            if self.data[username] == password:
                print("Connection validé ! ")
                self.on_login_success()
            else:
                self.show_error_popup("ERROR : Incorrect password !")
        else:
            self.show_error_popup("ERROR : Unknown user !")

    def sign_up(self):
        username = self.etr_username.get()
        password = self.etr_password.get()

        if username in self.data:
            self.show_error_popup("ERROR : Existing user !")
        else:
            if self.check_username_lenght(username):
                self.data[username] = password
                self.save_last_user(username)

                self.save_login_data()
                self.on_login_success()
            else:
                self.show_error_popup("ERROR : Username longer than 25 characters !")

    def show_error_popup(self, error_text):
        popup = ctk.CTkToplevel(self)
        popup.title("ERROR")

        largeur = 325
        hauteur = 150
        pos_x = int((popup.winfo_screenwidth() / 2) - (largeur / 2))
        pos_y = int((popup.winfo_screenheight() / 2) - (hauteur / 2))
        popup.geometry(f"{largeur}x{hauteur}+{pos_x}+{pos_y}")
        popup.grab_set()

        icone_img = ctk.CTkImage(
            light_image=Image.open("source/public/error_icon.png"), size=(20, 20)
        )

        label = ctk.CTkLabel(
            popup, text=f"  {error_text}", image=icone_img, compound="left"
        )
        label.pack(pady=30)

        bouton = ctk.CTkButton(popup, text="OK", command=popup.destroy)
        bouton.pack()
