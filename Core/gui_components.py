import customtkinter as ctk

# Lớp CustomScrolledText kế thừa từ ctk.CTkFrame
class CustomScrolledText(ctk.CTkFrame): # Vùng txt có scroll tùy chỉnh
    def __init__(self, master, **kwargs):
        super().__init__(master)
        self.grid_columnconfigure(0, weight=1) # Cfg cột 0 mở rộng ngang
        self.grid_rowconfigure(0, weight=1)    # Cfg hàng 0 mở rộng dọc
        self.text = ctk.CTkTextbox(self, **kwargs) # Tạo ctk.CTkTextbox
        self.text.grid(row=0, column=0, sticky="nsew") # Đặt textbox, mở rộng mọi hướng