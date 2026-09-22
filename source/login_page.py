import customtkinter as ctk

class LoginFrame(ctk.CTkFrame):
    def __init__(self, master, on_login_success, **kwargs):
        super().__init__(master, **kwargs)
        self.on_login_success = on_login_success
        
        self.lbl = ctk.CTkLabel(self, text="Authentication",  fg_color="transparent", font=("Arial", 30,"bold"))
        self.lbl.pack(padx=20, pady=20)
        
        self.etr_username = ctk.CTkEntry(self, placeholder_text="Username", width=250, height=35)
        self.etr_username.pack(padx=20, pady=5)
        self.etr_password = ctk.CTkEntry(self, placeholder_text="Password", width=250, height=35)
        self.etr_password.pack(padx=20, pady=5)
        
        self.btn_login = ctk.CTkButton(self, text="Login", font=("Arial", 15, "bold"), command=self.login)
        self.btn_login.pack(padx=25, pady=5)
        
        self.btn_sign_up = ctk.CTkButton(self, text="Sign up", font=("Arial", 15, "bold"), command=self.sign_Up)
        self.btn_sign_up.pack(padx=25)
        
    def login(self):
        self.on_login_success()
        
    def sign_Up(self):
        pass