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
            font=("Arial", 30, "bold"),
        )
        self.lbl.pack(padx=20, pady=20)

        self.etr_username = ctk.CTkEntry(
            self, placeholder_text="Username", width=250, height=35
        )
        self.etr_username.pack(padx=20, pady=5)
        self.etr_password = ctk.CTkEntry(
            self, placeholder_text="Password", width=250, height=35
        )
        self.etr_password.pack(padx=20, pady=5)

        self.btn_login = ctk.CTkButton(
            self, text="Login", font=("Arial", 15, "bold"), command=self.login
        )
        self.btn_login.pack(padx=25, pady=5)

        self.btn_sign_up = ctk.CTkButton(
            self, text="Sign up", font=("Arial", 15, "bold"), command=self.sign_up
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
        except json.JSONDecodeError:
            print("Erreur : Le fichier login.json mal formaté.")

    def save_login_data(self):
        try:
            Path("source/data").mkdir(exist_ok=True)

            with open("source/data/login.json", "w", encoding="utf-8") as fichier:
                json.dump(self.data, fichier, indent=4)
        except Exception as e:  # noqa: BLE001
            print("Erreur lors de l'enregistrement des tâches :", e)

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
                print("Mot de passe éroné")
                print(self.data)
        else:
            self.lbl_error.configure(text="error : Unknown user !")
            print("Nom d'utilisateur éroné")
            print(self.data)

    def sign_up(self):
        username = self.etr_username.get()
        password = self.etr_password.get()

        self.data[username] = password

        self.save_login_data()
        self.on_login_success()
