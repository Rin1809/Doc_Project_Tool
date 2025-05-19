import os
import tkinter as tk
from tkinter import filedialog, messagebox
from threading import Thread
import customtkinter as ctk
import subprocess
import json
from datetime import datetime
import webbrowser # Them wb

from .constants import (
    TITLE_FONT_SIZE, HEADER_FONT_SIZE, NORMAL_FONT_SIZE, SMALL_FONT_SIZE,
    PRIMARY_COLOR, ACCENT_COLOR, HOVER_COLOR, SUCCESS_COLOR, WARNING_COLOR, ERROR_COLOR,
    DEFAULT_EXCLUDED_SUBDIRS, DEFAULT_EXCLUDED_FILES, DEFAULT_OUTPUT_DIR, DEFAULT_BASE_FILENAME,
    HISTORY_FILE, MAX_HISTORY_ITEMS
)
from .gui_components import CustomScrolledText
from .gui_utils import format_output_for_tkinter
from .app_logic import tao_tai_lieu_du_an

# Lop chinh GUI
class ProjectDocApp:
    def __init__(self, root):
        self.root = root # Cua so goc
        root.title("Tao Tai Lieu Du An")
        root.geometry("1000x800")
        root.minsize(800, 700)

        self.font_family = "Segoe UI" if os.name == "nt" else "Helvetica" # Chon font
        self.title_font = ctk.CTkFont(family=self.font_family, size=TITLE_FONT_SIZE, weight="bold")
        self.header_font = ctk.CTkFont(family=self.font_family, size=HEADER_FONT_SIZE, weight="bold")
        self.normal_font = ctk.CTkFont(family=self.font_family, size=NORMAL_FONT_SIZE)
        self.small_font = ctk.CTkFont(family=self.font_family, size=SMALL_FONT_SIZE)

        # Colors
        self.primary_color = PRIMARY_COLOR
        self.accent_color = ACCENT_COLOR
        self.hover_color = HOVER_COLOR
        self.success_color = SUCCESS_COLOR
        self.warning_color = WARNING_COLOR
        self.error_color = ERROR_COLOR

        # Variables
        self.project_dirs = [] # DS TM DA
        self.excluded_subdirs = list(DEFAULT_EXCLUDED_SUBDIRS) # TM con loai tru
        self.excluded_files = list(DEFAULT_EXCLUDED_FILES) # Tep loai tru
        self.output_dir = DEFAULT_OUTPUT_DIR # TM out MD
        self.base_filename = DEFAULT_BASE_FILENAME # Ten tep co so MD
        self.verbose = tk.BooleanVar(value=False)
        self.output_format = tk.StringVar(value="txt")
        self.progress_var = tk.DoubleVar(value=0)
        self.status_var = tk.StringVar(value="San sang")
        
        self.last_main_output_file = None # Luu path file TLDA moi nhat

        # LS vars
        self.history_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), HISTORY_FILE) # Path file LS
        self.history_data = [] # DS luu cac muc LS

        self.create_ui() # Tao UI
        self.load_history_from_file() # Tai LS khi start

    def create_ui(self): # Tao UI chinh
        self.main_container = ctk.CTkFrame(self.root)
        self.main_container.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

        self.create_header()
        self.create_tabs()
        self.create_status_bar()

    def create_header(self): # Tao header
        header_frame = ctk.CTkFrame(self.main_container, corner_radius=10, fg_color="transparent")
        header_frame.pack(fill=tk.X, padx=10, pady=(0, 15))

        icon_label = ctk.CTkLabel(header_frame, text="📁", font=ctk.CTkFont(size=32))
        icon_label.pack(side=tk.LEFT, padx=(5, 10))

        title_label = ctk.CTkLabel(header_frame, text="Tao Tai Lieu Du An", font=self.title_font)
        title_label.pack(side=tk.LEFT)

        version_label = ctk.CTkLabel(header_frame, text="v2.2.2", font=self.small_font, text_color="gray") # VD: version
        version_label.pack(side=tk.RIGHT, padx=10)

    def create_tabs(self): # Tao tabview
        self.tabview = ctk.CTkTabview(self.main_container, corner_radius=10)
        self.tabview.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.tab_config = self.tabview.add("Cau hinh")
        self.tab_advanced = self.tabview.add("Nang cao")
        self.tab_history = self.tabview.add("Lich su") # Tab LS
        self.tab_output = self.tabview.add("Ket qua")

        for tab in [self.tab_config, self.tab_advanced, self.tab_history, self.tab_output]: # Cfg tab
            tab.grid_columnconfigure(0, weight=1)
            tab.grid_rowconfigure(0, weight=1) # Cho phep ND tab mo rong

        self.create_config_tab()
        self.create_advanced_tab()
        self.create_history_tab() # Tao ND tab LS
        self.create_output_tab()

    def create_config_tab(self): # ND tab "Cau hinh"
        config_scroll = ctk.CTkScrollableFrame(self.tab_config)
        config_scroll.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        config_scroll.columnconfigure(0, weight=1)

        # Phan TM DA
        dir_section = ctk.CTkFrame(config_scroll, corner_radius=10)
        dir_section.pack(fill=tk.X, padx=10, pady=10)

        section_label = ctk.CTkLabel(dir_section, text="Thu muc du an", font=self.header_font, anchor="w")
        section_label.pack(fill=tk.X, padx=15, pady=(15, 5))
        desc_label = ctk.CTkLabel(dir_section, text="Chon mot hoac nhieu thu muc du an de tao tai lieu.", font=self.normal_font, anchor="w", justify="left")
        desc_label.pack(fill=tk.X, padx=15, pady=(0, 10))

        self.dir_list_frame = ctk.CTkFrame(dir_section, fg_color="transparent")
        self.dir_list_frame.pack(fill=tk.X, padx=15, pady=(5, 15))

        self.project_dir_list = tk.Listbox(
            self.dir_list_frame, height=6, selectbackground=self.accent_color,
            font=(self.font_family, 12), bg="#2b2b2b", fg="#f2f2f2",
            borderwidth=1, highlightthickness=0, relief="flat", selectmode=tk.EXTENDED
        )
        self.project_dir_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ctk.CTkScrollbar(self.dir_list_frame, command=self.project_dir_list.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.project_dir_list.config(yscrollcommand=scrollbar.set)

        dir_buttons_frame = ctk.CTkFrame(dir_section, fg_color="transparent")
        dir_buttons_frame.pack(fill=tk.X, padx=15, pady=(0, 15))

        self.add_dir_btn = ctk.CTkButton(
            dir_buttons_frame, text="Them thu muc", command=self.add_project_directory,
            font=self.normal_font, fg_color=self.primary_color, hover_color=self.hover_color,
            corner_radius=8, height=35
        )
        self.add_dir_btn.pack(side=tk.LEFT, padx=(0, 10))

        self.remove_dir_btn = ctk.CTkButton(
            dir_buttons_frame, text="Xoa thu muc", command=self.remove_project_directory,
            font=self.normal_font, fg_color="#555555", hover_color="#444444",
            corner_radius=8, height=35
        )
        self.remove_dir_btn.pack(side=tk.LEFT)

        # Phan TM out
        output_section = ctk.CTkFrame(config_scroll, corner_radius=10)
        output_section.pack(fill=tk.X, padx=10, pady=10)

        output_label = ctk.CTkLabel(output_section, text="Thu muc dau ra", font=self.header_font, anchor="w")
        output_label.pack(fill=tk.X, padx=15, pady=(15, 5))
        output_desc = ctk.CTkLabel(output_section, text="Chon thu muc de luu tai lieu du an duoc tao ra.", font=self.normal_font, anchor="w", justify="left")
        output_desc.pack(fill=tk.X, padx=15, pady=(0, 10))

        output_dir_frame = ctk.CTkFrame(output_section, fg_color="transparent")
        output_dir_frame.pack(fill=tk.X, padx=15, pady=(5, 15))

        self.output_dir_entry = ctk.CTkEntry(
            output_dir_frame, font=self.normal_font, corner_radius=8,
            height=35, placeholder_text="Duong dan thu muc dau ra"
        )
        self.output_dir_entry.insert(0, self.output_dir)
        self.output_dir_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))

        self.browse_btn = ctk.CTkButton(
            output_dir_frame, text="Duyet...", command=self.browse_output_directory,
            font=self.normal_font, fg_color=self.primary_color, hover_color=self.hover_color,
            corner_radius=8, width=100, height=35
        )
        self.browse_btn.pack(side=tk.RIGHT)

        filename_frame = ctk.CTkFrame(output_section, fg_color="transparent")
        filename_frame.pack(fill=tk.X, padx=15, pady=(0, 15))
        filename_label = ctk.CTkLabel(filename_frame, text="Ten tep co so:", font=self.normal_font, width=120, anchor="w")
        filename_label.pack(side=tk.LEFT, padx=(0, 10))
        self.base_filename_entry = ctk.CTkEntry(filename_frame, font=self.normal_font, corner_radius=8, height=35)
        self.base_filename_entry.insert(0, self.base_filename)
        self.base_filename_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

        # Dinh dang
        format_section = ctk.CTkFrame(config_scroll, corner_radius=10)
        format_section.pack(fill=tk.X, padx=10, pady=10)
        format_label = ctk.CTkLabel(format_section, text="Dinh dang dau ra", font=self.header_font, anchor="w")
        format_label.pack(fill=tk.X, padx=15, pady=(15, 5))

        format_options = ctk.CTkFrame(format_section, fg_color="transparent")
        format_options.pack(fill=tk.X, padx=15, pady=(5, 15))

        self.txt_radio = ctk.CTkRadioButton(
            format_options, text="Van ban (.txt)", variable=self.output_format, value="txt",
            font=self.normal_font, fg_color=self.accent_color
        )
        self.txt_radio.pack(side=tk.LEFT, padx=(0, 20))
        self.md_radio = ctk.CTkRadioButton(
            format_options, text="Markdown (.md)", variable=self.output_format, value="markdown",
            font=self.normal_font, fg_color=self.accent_color
        )
        self.md_radio.pack(side=tk.LEFT)

        self.verbose_check = ctk.CTkCheckBox(
            format_options, text="Chi tiet", variable=self.verbose,
            font=self.normal_font, fg_color=self.accent_color, checkbox_width=20, checkbox_height=20
        )
        self.verbose_check.pack(side=tk.RIGHT)

        # Nut chay
        run_frame = ctk.CTkFrame(config_scroll, fg_color="transparent")
        run_frame.pack(fill=tk.X, padx=10, pady=(10, 20))
        self.run_button = ctk.CTkButton(
            run_frame, text="Tao Tai Lieu", command=self.run_documentation,
            font=ctk.CTkFont(family=self.font_family, size=15, weight="bold"),
            fg_color=self.success_color, hover_color="#218838",
            corner_radius=8, height=40
        )
        self.run_button.pack(fill=tk.X, padx=15)

    def create_advanced_tab(self): # ND tab "Nang cao"
        advanced_scroll = ctk.CTkScrollableFrame(self.tab_advanced)
        advanced_scroll.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        advanced_scroll.columnconfigure(0, weight=1)

        excluded_dirs_section = ctk.CTkFrame(advanced_scroll, corner_radius=10)
        excluded_dirs_section.pack(fill=tk.X, padx=10, pady=10)
        excl_dirs_label = ctk.CTkLabel(excluded_dirs_section, text="Thu muc con loai tru", font=self.header_font, anchor="w")
        excl_dirs_label.pack(fill=tk.X, padx=15, pady=(15, 5))
        excl_dirs_desc = ctk.CTkLabel(excluded_dirs_section, text="Nhap TM con (cach nhau boi dau phay) de loai tru.", font=self.normal_font, anchor="w", justify="left")
        excl_dirs_desc.pack(fill=tk.X, padx=15, pady=(0, 10))
        self.excluded_subdirs_entry = ctk.CTkEntry(excluded_dirs_section, font=self.normal_font, corner_radius=8, height=35)
        self.excluded_subdirs_entry.insert(0, ", ".join(self.excluded_subdirs))
        self.excluded_subdirs_entry.pack(fill=tk.X, padx=15, pady=(5, 15))

        excluded_files_section = ctk.CTkFrame(advanced_scroll, corner_radius=10)
        excluded_files_section.pack(fill=tk.X, padx=10, pady=(0, 10)) 
        excl_files_label = ctk.CTkLabel(excluded_files_section, text="Tep loai tru", font=self.header_font, anchor="w")
        excl_files_label.pack(fill=tk.X, padx=15, pady=(15, 5))
        excl_files_desc = ctk.CTkLabel(excluded_files_section, text="Nhap duoi tep/ten tep (cach nhau boi dau phay) de loai tru.", font=self.normal_font, anchor="w", justify="left")
        excl_files_desc.pack(fill=tk.X, padx=15, pady=(0, 10))
        self.excluded_files_entry = ctk.CTkEntry(excluded_files_section, font=self.normal_font, corner_radius=8, height=35)
        self.excluded_files_entry.insert(0, ", ".join(self.excluded_files))
        self.excluded_files_entry.pack(fill=tk.X, padx=15, pady=(5, 15))

        save_button = ctk.CTkButton(
            advanced_scroll, text="Luu Cai Dat", command=self.save_advanced_settings,
            font=self.normal_font, fg_color="#6C757D", hover_color="#5A6268",
            corner_radius=8, height=35
        )
        save_button.pack(fill=tk.X, padx=15, pady=(15, 20))

    def create_history_tab(self): # ND tab "Lich su"
        history_frame = ctk.CTkFrame(self.tab_history, fg_color="transparent")
        history_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        history_frame.grid_columnconfigure(0, weight=1)
        history_frame.grid_rowconfigure(1, weight=1) 

        title_label = ctk.CTkLabel(history_frame, text="Lich su cau hinh da chay", font=self.header_font)
        title_label.grid(row=0, column=0, sticky="w", padx=5, pady=(5,10), columnspan=2) 

        self.history_listbox = tk.Listbox(
            history_frame, height=15, font=(self.font_family, 12),
            bg="#2b2b2b", fg="#f2f2f2", borderwidth=1, highlightthickness=0,
            relief="flat", selectbackground=self.accent_color
        )
        self.history_listbox.grid(row=1, column=0, sticky="nsew", padx=(5,0), pady=5) 

        history_scrollbar = ctk.CTkScrollbar(history_frame, command=self.history_listbox.yview)
        history_scrollbar.grid(row=1, column=1, sticky="ns", padx=(0,5), pady=5) 
        self.history_listbox.config(yscrollcommand=history_scrollbar.set)

        buttons_frame = ctk.CTkFrame(history_frame, fg_color="transparent")
        buttons_frame.grid(row=2, column=0, columnspan=2, sticky="ew", padx=5, pady=(10,5))

        load_btn = ctk.CTkButton(
            buttons_frame, text="Tai Cau Hinh", command=self.load_selected_history_item,
            font=self.normal_font, fg_color=self.primary_color, hover_color=self.hover_color,
            height=35, corner_radius=8
        )
        load_btn.pack(side=tk.LEFT, padx=(0,10))

        delete_btn = ctk.CTkButton(
            buttons_frame, text="Xoa Muc", command=self.delete_selected_history_item,
            font=self.normal_font, fg_color=self.error_color, hover_color="#C82333", 
            height=35, corner_radius=8
        )
        delete_btn.pack(side=tk.LEFT)
        
        delete_all_btn = ctk.CTkButton(
            buttons_frame, text="Xoa Tat Ca", command=self.delete_all_history,
            font=self.normal_font, fg_color=self.warning_color, hover_color="#E0A800", 
            height=35, corner_radius=8
        )
        delete_all_btn.pack(side=tk.RIGHT, padx=(10,0))


    def create_output_tab(self): # ND tab "Ket qua"
        self.output_text = CustomScrolledText(self.tab_output, wrap=tk.WORD, font=self.normal_font)
        self.output_text.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        buttons_frame = ctk.CTkFrame(self.tab_output, fg_color="transparent")
        buttons_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=(0, 10))

        self.copy_button = ctk.CTkButton(
            buttons_frame, text="Sao chep", command=self.copy_to_clipboard,
            font=self.normal_font, fg_color="#4CAF50", hover_color="#388E3C",
            corner_radius=8, width=120, height=30
        )
        self.copy_button.pack(side=tk.LEFT, padx=(0, 10))

        self.clear_button = ctk.CTkButton(
            buttons_frame, text="Xoa", command=self.clear_output,
            font=self.normal_font, fg_color="#F44336", hover_color="#D32F2F",
            corner_radius=8, width=120, height=30
        )
        self.clear_button.pack(side=tk.LEFT, padx=(0, 10))

        self.ai_studio_button = ctk.CTkButton(
            buttons_frame, text="🚀 AI Studio", command=self.open_ai_studio_and_copy_path,
            font=self.normal_font, fg_color="#7E57C2", hover_color="#5E35B1", 
            corner_radius=8, height=30, state="disabled"
        )
        self.ai_studio_button.pack(side=tk.LEFT, padx=(0,10))

        self.open_folder_button = ctk.CTkButton(
            buttons_frame, text="Mo Thu Muc Dau Ra", command=self.open_output_folder,
            font=self.normal_font, fg_color=self.primary_color, hover_color=self.hover_color,
            corner_radius=8, height=30
        )
        self.open_folder_button.pack(side=tk.RIGHT, padx=(10, 0)) 
        self.open_folder_button.configure(state="disabled")


    def create_status_bar(self): # Tao status bar
        status_bar = ctk.CTkFrame(self.root, height=30, fg_color="transparent")
        status_bar.pack(fill=tk.X, side=tk.BOTTOM, padx=15, pady=(5, 10))

        self.status_label = ctk.CTkLabel(status_bar, textvariable=self.status_var, font=self.small_font)
        self.status_label.pack(side=tk.LEFT)
        self.progress_bar = ctk.CTkProgressBar(status_bar, variable=self.progress_var, height=10, corner_radius=5)
        self.progress_bar.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=(10, 0))

    def add_project_directory(self): # Them TM DA
        directory = filedialog.askdirectory(title="Chon Thu Muc Du An")
        if directory:
            directory = os.path.abspath(directory)
            if directory not in self.project_dirs:
                self.project_dirs.append(directory)
                self.project_dir_list.insert(tk.END, directory)
            else:
                messagebox.showinfo("Thong bao", "Thu muc ban chon da co trong danh sach.")

    def remove_project_directory(self): # Xoa TM DA
        selected_indices = self.project_dir_list.curselection()
        if selected_indices:
            for i in reversed(selected_indices):
                self.project_dir_list.delete(i)
                self.project_dirs.pop(i)
        else:
            messagebox.showinfo("Thong bao", "Vui long chon it nhat mot thu muc de xoa.")

    def browse_output_directory(self): # Chon TM out
        directory = filedialog.askdirectory(title="Chon Thu Muc Dau Ra")
        if directory:
            self.output_dir = os.path.abspath(directory)
            self.output_dir_entry.delete(0, tk.END)
            self.output_dir_entry.insert(0, self.output_dir)

    def save_advanced_settings(self): # Luu cai dat nang cao
        self.excluded_subdirs = [s.strip() for s in self.excluded_subdirs_entry.get().split(",") if s.strip()]
        self.excluded_files = [f.strip() for f in self.excluded_files_entry.get().split(",") if f.strip()]
        messagebox.showinfo("Da Luu", "Cai dat nang cao da duoc cap nhat.")

    # --- Ham xu ly LS ---
    def populate_history_listbox(self): # Dien LS vao listbox
        self.history_listbox.delete(0, tk.END)
        for item in self.history_data:
            first_proj_dir = os.path.basename(item["project_dirs"][0]) if item.get("project_dirs") else "Khong TM"
            if len(item.get("project_dirs", [])) > 1:
                first_proj_dir += " (+...)"
            
            try:
                dt_obj = datetime.fromisoformat(item["timestamp"])
                timestamp_str = dt_obj.strftime("%d/%m/%y %H:%M")
            except:
                timestamp_str = "N/A"
            
            display_name = item.get("name", first_proj_dir)
            if not display_name or display_name == "Khong TM": display_name = first_proj_dir

            display_text = f"{display_name} [{timestamp_str}]"
            self.history_listbox.insert(tk.END, display_text)

    def load_history_from_file(self): # Tai LS tu file
        try:
            if os.path.exists(self.history_file):
                with open(self.history_file, "r", encoding="utf-8") as f:
                    self.history_data = json.load(f)
                self.history_data.sort(key=lambda x: x.get("timestamp", ""), reverse=True) 
            else:
                self.history_data = []
        except json.JSONDecodeError:
            self.history_data = [] 
        except Exception as e:
            messagebox.showerror("Loi", f"Khong the tai lich su: {e}")
            self.history_data = []
        self.populate_history_listbox()

    def save_history_to_file(self): # Luu LS vao file
        try:
            with open(self.history_file, "w", encoding="utf-8") as f:
                json.dump(self.history_data, f, indent=4, ensure_ascii=False)
        except Exception as e:
            messagebox.showerror("Loi", f"Khong the luu lich su: {e}")

    def add_to_history(self, current_config): # Them muc vao LS
        new_config_key_parts = sorted(current_config["project_dirs"]) + \
                               [current_config["output_dir"], current_config["base_filename"]]
        new_config_key = "|".join(new_config_key_parts)

        filtered_history = []
        for item in self.history_data:
            item_key_parts = sorted(item["project_dirs"]) + \
                             [item["output_dir"], item["base_filename"]]
            item_key = "|".join(item_key_parts)
            if item_key != new_config_key:
                filtered_history.append(item)
        self.history_data = filtered_history

        self.history_data.insert(0, current_config) 

        if len(self.history_data) > MAX_HISTORY_ITEMS:
            self.history_data = self.history_data[:MAX_HISTORY_ITEMS]

        self.save_history_to_file()
        self.populate_history_listbox()

    def load_selected_history_item(self): # Tai muc LS da chon
        selected_indices = self.history_listbox.curselection()
        if not selected_indices:
            messagebox.showinfo("Thong Bao", "Vui long chon mot muc tu lich su.")
            return
        
        try:
            selected_index = selected_indices[0]
            config_data = self.history_data[selected_index]

            self.project_dirs = list(config_data.get("project_dirs", [])) 
            self.project_dir_list.delete(0, tk.END)
            for p_dir in self.project_dirs:
                self.project_dir_list.insert(tk.END, p_dir)

            self.output_dir_entry.delete(0, tk.END)
            self.output_dir_entry.insert(0, config_data.get("output_dir", DEFAULT_OUTPUT_DIR))
            self.output_dir = config_data.get("output_dir", DEFAULT_OUTPUT_DIR) 

            self.base_filename_entry.delete(0, tk.END)
            self.base_filename_entry.insert(0, config_data.get("base_filename", DEFAULT_BASE_FILENAME))

            self.output_format.set(config_data.get("output_format", "txt"))
            self.verbose.set(config_data.get("verbose", False))

            self.excluded_subdirs = list(config_data.get("excluded_subdirs", DEFAULT_EXCLUDED_SUBDIRS))
            self.excluded_subdirs_entry.delete(0, tk.END)
            self.excluded_subdirs_entry.insert(0, ", ".join(self.excluded_subdirs))
            
            self.excluded_files = list(config_data.get("excluded_files", DEFAULT_EXCLUDED_FILES))
            self.excluded_files_entry.delete(0, tk.END)
            self.excluded_files_entry.insert(0, ", ".join(self.excluded_files))

            self.tabview.set("Cau hinh") 
            # messagebox.showinfo("Da Tai", "Cau hinh da duoc tai. Vui long kiem tra va chay.") # Bo TB
        except IndexError:
            messagebox.showerror("Loi", "Khong tim thay muc lich su tuong ung.")
        except Exception as e:
            messagebox.showerror("Loi", f"Loi khi tai lich su: {str(e)}")


    def delete_selected_history_item(self): # Xoa muc LS da chon
        selected_indices = self.history_listbox.curselection()
        if not selected_indices:
            messagebox.showinfo("Thong Bao", "Vui long chon mot muc de xoa.")
            return

        confirm = messagebox.askyesno("Xac Nhan Xoa", "Ban co chac chan muon xoa muc lich su nay?")
        if confirm:
            try:
                selected_index = selected_indices[0]
                del self.history_data[selected_index]
                self.save_history_to_file()
                self.populate_history_listbox()
                messagebox.showinfo("Da Xoa", "Muc lich su da duoc xoa.")
            except IndexError:
                 messagebox.showerror("Loi", "Khong tim thay muc lich su de xoa.")


    def delete_all_history(self): # Xoa toan bo LS
        if not self.history_data:
            messagebox.showinfo("Thong Bao", "Lich su trong.")
            return
        confirm = messagebox.askyesno("Xac Nhan Xoa Tat Ca", "Ban co chac chan muon xoa TOAN BO lich su chay?")
        if confirm:
            self.history_data = []
            self.save_history_to_file()
            self.populate_history_listbox()
            messagebox.showinfo("Da Xoa", "Toan bo lich su da duoc xoa.")
    # --- Het ham LS ---

    def run_documentation(self): # Bat dau tao doc
        if not self.project_dirs:
            messagebox.showerror("Loi", "Vui long chon it nhat mot thu muc du an.")
            return

        self.progress_var.set(0)
        self.status_var.set("Dang xu ly...")
        self.output_text.text.delete("1.0", tk.END)
        self.open_folder_button.configure(state="disabled")
        self.ai_studio_button.configure(state="disabled") 
        self.last_main_output_file = None 

        self.run_button.configure(state="disabled")
        self.add_dir_btn.configure(state="disabled")
        self.remove_dir_btn.configure(state="disabled")
        self.browse_btn.configure(state="disabled")

        output_dir_val = self.output_dir_entry.get()
        base_filename_val = self.base_filename_entry.get()
        output_format_val = self.output_format.get()
        verbose_val = self.verbose.get()
        
        current_excluded_subdirs = [s.strip() for s in self.excluded_subdirs_entry.get().split(",") if s.strip()]
        current_excluded_files = [f.strip() for f in self.excluded_files_entry.get().split(",") if f.strip()]


        def run_doc_thread():
            self.root.after(0, lambda: self.tabview.set("Ket qua")) # Chuyen tab KQ
            try:
                (message, execution_time, num_files, num_folders,
                errors, skipped_files, skipped_folders, output_paths_str) = tao_tai_lieu_du_an(
                    self.project_dirs, current_excluded_subdirs, current_excluded_files, 
                    base_filename_val, output_dir_val, verbose_val, output_format_val
                )
                formatted_output = format_output_for_tkinter(
                    message, execution_time, num_files, num_folders,
                    errors, skipped_files, skipped_folders, output_format_val
                )
                self.root.after(0, self.update_output, formatted_output)
                self.root.after(0, self.update_status, f"Hoan tat! Tai lieu tai: {output_paths_str}")
                self.root.after(0, self.progress_var.set, 100) 
                self.root.after(0, lambda: self.open_folder_button.configure(state="normal"))

                all_output_files = [p.strip() for p in output_paths_str.split(",") if p.strip()]
                if all_output_files:
                    self.last_main_output_file = all_output_files[0] 
                    self.root.after(0, lambda: self.ai_studio_button.configure(state="normal"))
                else:
                    self.last_main_output_file = None
                    self.root.after(0, lambda: self.ai_studio_button.configure(state="disabled"))


                is_successful_run = not errors or all("khong ton tai" in str(v).lower() or "not found" in str(v).lower() for v in errors.values())

                if is_successful_run and self.project_dirs: 
                    first_proj_dir_name = os.path.basename(self.project_dirs[0])
                    history_item_name = f"{first_proj_dir_name} ({datetime.now().strftime('%d/%m %H:%M')})"
                    if len(self.project_dirs) > 1:
                        history_item_name = f"{first_proj_dir_name},... ({datetime.now().strftime('%d/%m %H:%M')})"

                    current_config = {
                        "name": history_item_name, 
                        "project_dirs": list(self.project_dirs), 
                        "output_dir": output_dir_val,
                        "base_filename": base_filename_val,
                        "excluded_subdirs": current_excluded_subdirs,
                        "excluded_files": current_excluded_files,
                        "output_format": output_format_val,
                        "verbose": verbose_val,
                        "timestamp": datetime.now().isoformat()
                    }
                    self.root.after(0, self.add_to_history, current_config)

            except Exception as e:
                self.root.after(0, self.update_output, f"Da xay ra loi: {str(e)}")
                self.root.after(0, self.update_status, "Loi")
                self.root.after(0, self.progress_var.set, 0)
                self.root.after(0, lambda: self.ai_studio_button.configure(state="disabled")) 
            finally:
                self.root.after(0, lambda: self.run_button.configure(state="normal"))
                self.root.after(0, lambda: self.add_dir_btn.configure(state="normal"))
                self.root.after(0, lambda: self.remove_dir_btn.configure(state="normal"))
                self.root.after(0, lambda: self.browse_btn.configure(state="normal"))

        Thread(target=run_doc_thread, daemon=True).start() 

    def update_output(self, text): # Cap nhat output
        self.output_text.text.insert(tk.END, text + "\n")
        self.output_text.text.see(tk.END)

    def update_status(self, message): # Cap nhat status
         self.status_var.set(message)

    def copy_to_clipboard(self): # Sao chep ND
        try:
            self.root.clipboard_clear()
            self.root.clipboard_append(self.output_text.text.get("1.0", tk.END))
            messagebox.showinfo("Da sao chep", "Noi dung da duoc sao chep vao clipboard.")
        except Exception as e:
            messagebox.showerror("Loi", f"Khong the sao chep noi dung: {str(e)}")

    def clear_output(self): # Xoa ND output
        self.output_text.text.delete("1.0", tk.END)
        self.open_folder_button.configure(state="disabled") 
        self.ai_studio_button.configure(state="disabled") 
        self.last_main_output_file = None 

    def open_output_folder(self): # Mo TM out
       output_path_to_open = self.output_dir_entry.get() 
       if output_path_to_open and os.path.isdir(output_path_to_open):
           try:
               if os.name == 'nt':
                   subprocess.Popen(['explorer', os.path.normpath(output_path_to_open)])
               elif os.name == 'posix':
                   subprocess.Popen(['open', os.path.normpath(output_path_to_open)])
               else:
                   messagebox.showwarning("Khong ho tro", "HDH cua ban khong duoc ho tro de mo thu muc.")
           except Exception as e:
              messagebox.showerror("Loi", f"Khong the mo thu muc: {str(e)}")
       else:
         messagebox.showerror("Loi", "Duong dan thu muc dau ra khong hop le hoac khong ton tai.")

    def open_ai_studio_and_copy_path(self): # Mo AI Studio va copy path
        ai_studio_url = "https://aistudio.google.com/prompts/new_chat"
        if self.last_main_output_file and os.path.exists(self.last_main_output_file):
            try:
                webbrowser.open_new_tab(ai_studio_url)
                self.root.clipboard_clear()
                self.root.clipboard_append(self.last_main_output_file)
                
            except Exception as e:
                messagebox.showerror("Loi", f"Khong the mo AI Studio hoac sao chep duong dan: {str(e)}")
        else:
            messagebox.showwarning("Thong Bao", "Khong tim thay tep tai lieu de sao chep duong dan.")