import customtkinter as ctk
from login_page import LoginFrame


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("LockBox")
        self.geometry("400x300")
        
        self.mon_panneau = LoginFrame(master=self, on_login_success=self.open_app, border_width=2)
        self.mon_panneau.pack(padx=20, pady=20, fill="both", expand=True)
        
    def open_app(self):
        self.mon_panneau.pack_forget()
        
        
if __name__ == "__main__":
    app = App()
    app.mainloop()