import customtkinter as ctk
from .main_app import ProjectDocApp
from .constants import APPEARANCE_MODE, DEFAULT_COLOR_THEME

def main():
    # Cấu hình giao diện mặc định của CustomTkinter
    ctk.set_appearance_mode(APPEARANCE_MODE)
    ctk.set_default_color_theme(DEFAULT_COLOR_THEME)

    root = ctk.CTk() # Tạo cửa sổ gốc
    app = ProjectDocApp(root) # Tạo đối tượng App
    root.mainloop() # Bắt đầu vòng lặp GUI

if __name__ == "__main__":
    main()