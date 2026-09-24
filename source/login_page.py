import json
from pathlib import Path

import customtkinter as ctk


class LoginFrame(ctk.CTkFrame):
    def __init__(self, master, on_login_success, **kwargs):
        super().__init__(master, **kwargs)
        self.on_login_success = on_login_success
        self.data = {}

        self.lbl = ctk.CTkLabel(
            self,
            text="Authentication",
            font=("Arial", 60, "bold"),
        )
        self.lbl.pack(padx=30, pady=(50, 40))

        self.etr_username = ctk.CTkEntry(
            self,
            placeholder_text="Username",
            font=("Arial", 15, "bold"),
            width=350,
            height=40,
        )
        self.etr_username.pack(padx=80, pady=5, anchor="w")
        self.etr_password = ctk.CTkEntry(
            self,
            placeholder_text="Password",
            show="*",
            font=("Arial", 15, "bold"),
            width=350,
            height=40,
        )
        self.etr_password.pack(padx=80, pady=5, anchor="w")

        self.checkbox_show_password = ctk.CTkCheckBox(
            self,
            text="Show password",
            font=("Arial", 15, "bold"),
            command=self.show_hide_password,
        )
        self.checkbox_show_password.pack(padx=80, pady=(10, 10), anchor="w")

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

        self.lbl_error = ctk.CTkLabel(
            self,
            text="",
            text_color="red",
            font=("Arial", 20, "bold"),
        )
        self.lbl_error.pack(padx=25, pady=5)

    def get_login_data(self):
        try:
            with open("source/data/login.json", "r", encoding="utf-8") as fichier:
                self.data = json.load(fichier)
        except FileNotFoundError:
            print("Erreur : Le fichier login.json est introuvable au chemin indiqué.")

    def save_login_data(self):
        try:
            Path("source/data").mkdir(exist_ok=True)

            with open("source/data/login.json", "w", encoding="utf-8") as fichier:
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
                self.lbl_error.configure(text="error : Incorrect password !")
        else:
            self.lbl_error.configure(text="error : Unknown user !")

    def sign_up(self):
        username = self.etr_username.get()
        password = self.etr_password.get()

        if username in self.data:
            self.lbl_error.configure(text="error : Existing user !")
        else:
            self.data[username] = password

            self.save_login_data()
            self.on_login_success()
