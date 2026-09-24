import customtkinter as ctk
from login_page import LoginFrame


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("LockBox")
        self.geometry("1200x800")

        self.after(0, lambda: self.state("zoomed"))

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure((0, 1), weight=1)

        self.login_frame = LoginFrame(
            master=self,
            on_login_success=self.open_app,
            border_width=2,
        )
        self.login_frame.place(relx=0.5, rely=0.5, anchor="center")

    def open_app(self):
        self.login_frame.place_forget()


if __name__ == "__main__":
    app = App()
    app.mainloop()
