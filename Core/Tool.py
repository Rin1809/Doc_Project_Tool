import os
import time
import tkinter as tk
from tkinter import filedialog, messagebox
from threading import Thread
import customtkinter as ctk
import markdown 
import codecs 


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class ProjectDocApp:
    def __init__(self, root):
        self.root = root
        root.title("Tạo Tài Liệu Dự Án")
        root.geometry("900x750") # Kích thước cửa sổ nhỏ lại một chút

        self.font_family = "Segoe UI"
        self.font_size = 12
        self.my_font = ctk.CTkFont(family=self.font_family, size=self.font_size)

        self.project_dirs = []
        self.excluded_subdirs = ["__pycache__", "moitruongao", "venv", ".git", ".vscode", ".bieutuong", "memory", "node_modules", "uploads", "chats"]
        self.excluded_files = [".pyc", "desktop.ini", ".json", ".txt", ".rar", "requirements.txt", "ex.json", ".jpg", ".mp3", ".png"]
        self.output_dir = "."
        self.base_filename = "tai_lieu_du_an"
        self.verbose = tk.BooleanVar(value=False)
        self.output_format = tk.StringVar(value="Plain Text")  

        self.create_widgets()
    


    def create_widgets(self):
        main_frame = ctk.CTkFrame(self.root, fg_color="#242424")
        main_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

     
        self.project_dir_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        self.project_dir_frame.grid(row=0, column=0, sticky="ew", padx=0, pady=(0, 10))
        main_frame.columnconfigure(0, weight=1)


        self.project_dir_list = tk.Listbox(self.project_dir_frame, width=50, height=5,  selectbackground="#4A4D5A", font=(self.font_family, self.font_size), bg="#2b2b2b", fg="#f2f2f2", borderwidth=0, highlightthickness=0)
        self.project_dir_list.grid(row=0, column=0, rowspan=2, sticky="nsew", padx=(5, 0), pady=5)
        self.project_dir_frame.columnconfigure(0, weight=1)
        self.project_dir_frame.rowconfigure(0, weight=1)


        self.add_project_dir_button = ctk.CTkButton(self.project_dir_frame, text="Thêm", command=self.add_project_directory, width=80, font=self.my_font, corner_radius=8, fg_color="#0078d7", hover_color="#005a9e")
        self.add_project_dir_button.grid(row=0, column=1, sticky="ew", padx=5, pady=5)

        self.remove_project_dir_button = ctk.CTkButton(self.project_dir_frame, text="Xóa", command=self.remove_project_directory, width=80, font=self.my_font, corner_radius=8, fg_color="#0078d7", hover_color="#005a9e")
        self.remove_project_dir_button.grid(row=1, column=1, sticky="ew", padx=5, pady=5)

   
        self.exclusion_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        self.exclusion_frame.grid(row=1, column=0, sticky="ew", pady=(0, 10))
        self.exclusion_frame.rowconfigure(0, weight=1)

        self.excluded_subdirs_frame = ctk.CTkFrame(self.exclusion_frame, corner_radius=8, fg_color="transparent")
        self.excluded_subdirs_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        self.exclusion_frame.columnconfigure(0, weight=1)

        self.excluded_subdirs_label = ctk.CTkLabel(self.excluded_subdirs_frame, text="Thư mục con loại trừ:", font=self.my_font, text_color="#f2f2f2")
        self.excluded_subdirs_label.pack(padx=5, pady=(5, 0), anchor="w")
        self.excluded_subdirs_text = ctk.CTkTextbox(self.excluded_subdirs_frame, width=40, font=(self.font_family, self.font_size), fg_color="#2b2b2b", text_color="#f2f2f2", border_width=0)
        self.excluded_subdirs_text.insert(tk.END, "\n".join(self.excluded_subdirs))
        self.excluded_subdirs_text.pack(padx=5, pady=(0, 5), fill=tk.BOTH, expand=True)

        self.excluded_files_frame = ctk.CTkFrame(self.exclusion_frame, corner_radius=8, fg_color="transparent")
        self.excluded_files_frame.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
        self.exclusion_frame.columnconfigure(1, weight=1)

        self.excluded_files_label = ctk.CTkLabel(self.excluded_files_frame, text="Tệp loại trừ:", font=self.my_font, text_color="#f2f2f2")
        self.excluded_files_label.pack(padx=5, pady=(5, 0), anchor="w")
        self.excluded_files_text = ctk.CTkTextbox(self.excluded_files_frame, width=40, font=(self.font_family, self.font_size), fg_color="#2b2b2b", text_color="#f2f2f2", border_width=0)
        self.excluded_files_text.insert(tk.END, "\n".join(self.excluded_files))
        self.excluded_files_text.pack(padx=5, pady=(0, 5), fill=tk.BOTH, expand=True)

        self.add_defaults_button = ctk.CTkButton(self.exclusion_frame, text="Thêm mặc định", command=self.add_default_exclusions, font=self.my_font, corner_radius=8, fg_color="#0078d7", hover_color="#005a9e")
        self.add_defaults_button.grid(row=1, column=0, columnspan=2, sticky="ew", pady=5)

        self.output_settings_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        self.output_settings_frame.grid(row=2, column=0, sticky="ew", pady=(0, 10))

        self.output_dir_frame = ctk.CTkFrame(self.output_settings_frame, corner_radius=8, fg_color="transparent")
        self.output_dir_frame.grid(row=0, column=0, sticky="ew", padx=(0, 10))
        self.output_settings_frame.columnconfigure(0, weight=1)

        self.output_dir_label = ctk.CTkLabel(self.output_dir_frame, text="Thư mục đầu ra:", font=self.my_font, text_color="#f2f2f2")
        self.output_dir_label.pack(side=tk.LEFT, padx=5, pady=5)
        self.output_dir_entry = ctk.CTkEntry(self.output_dir_frame, width=30, font=(self.font_family, self.font_size), corner_radius=8,  text_color="#f2f2f2", placeholder_text_color="#aaaaaa", border_color="#555555")
        self.output_dir_entry.insert(0, self.output_dir)
        self.output_dir_entry.pack(side=tk.LEFT, padx=5, pady=5, fill=tk.X, expand=True)

        self.browse_output_dir_button = ctk.CTkButton(self.output_dir_frame, text="Chọn...", command=self.browse_output_directory, font=self.my_font, corner_radius=8, width=80, fg_color="#0078d7", hover_color="#005a9e")
        self.browse_output_dir_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.base_filename_frame = ctk.CTkFrame(self.output_settings_frame, corner_radius=8, fg_color="transparent")
        self.base_filename_frame.grid(row=0, column=1, sticky="ew", padx=(10, 0))
        self.output_settings_frame.columnconfigure(1, weight=1)

        self.base_filename_label = ctk.CTkLabel(self.base_filename_frame, text="Tên tệp:", font=self.my_font, text_color="#f2f2f2")
        self.base_filename_label.pack(side=tk.LEFT, padx=5, pady=5)
        self.base_filename_entry = ctk.CTkEntry(self.base_filename_frame, width=20, font=(self.font_family, self.font_size), corner_radius=8,  text_color="#f2f2f2", placeholder_text_color="#aaaaaa", border_color="#555555")
        self.base_filename_entry.insert(0, self.base_filename)
        self.base_filename_entry.pack(padx=5, pady=5, fill=tk.X, expand=True)

        # --- Output Format ---
        self.output_format_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        self.output_format_frame.grid(row=3, column=0, sticky="ew", pady=(10, 0))

        output_format_label = ctk.CTkLabel(self.output_format_frame, text="Định dạng đầu ra:", font=self.my_font, text_color="#f2f2f2")
        output_format_label.pack(side=tk.LEFT, padx=5, pady=5)

        output_formats = ["Plain Text", "Markdown", "HTML"]
        for format_text in output_formats:
            radio_button = ctk.CTkRadioButton(self.output_format_frame, text=format_text, variable=self.output_format, value=format_text, font=self.my_font, text_color="#f2f2f2", fg_color="#0078d7", border_color="#555555", hover_color="#005a9e")
            radio_button.pack(side=tk.LEFT, padx=10, pady=5)


        # --- Verbose & Run ---
        self.options_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        self.options_frame.grid(row=4, column=0, sticky="ew")

        self.verbose_checkbutton = ctk.CTkCheckBox(self.options_frame, text="Verbose", variable=self.verbose, font=self.my_font, text_color="#f2f2f2", fg_color="#0078d7", border_color="#555555", hover_color="#005a9e")
        self.verbose_checkbutton.pack(side=tk.LEFT, padx=5, pady=5)

        self.run_button = ctk.CTkButton(self.options_frame, text="Tạo Tài Liệu", command=self.run_documentation, font=self.my_font, corner_radius=8, fg_color="#0078d7", hover_color="#005a9e")
        self.run_button.pack(side=tk.RIGHT, padx=5, pady=5)

        # --- Output Display ---
        self.output_text = ctk.CTkTextbox(main_frame, width=80, height=15, font=(self.font_family, self.font_size), fg_color="#2b2b2b", text_color="#f2f2f2", border_width=0)
        self.output_text.grid(row=5, column=0, sticky="nsew", pady=(10, 0))
        main_frame.rowconfigure(5, weight=1)



    def add_default_exclusions(self):
        default_subdirs = "__pycache__\nvenv\n.git\n.vscode\nnode_modules\nuploads\nchats"
        default_files = ".pyc\ndesktop.ini\n.json\n.txt\n.rar\nrequirements.txt"

        self.excluded_subdirs_text.delete("1.0", tk.END)
        self.excluded_subdirs_text.insert(tk.END, default_subdirs)

        self.excluded_files_text.delete("1.0", tk.END)
        self.excluded_files_text.insert(tk.END, default_files)

    def add_project_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            if directory not in self.project_dirs:
                self.project_dirs.append(directory)
                self.project_dir_list.insert(tk.END, directory) 

    def remove_project_directory(self):
        selected_indices = self.project_dir_list.curselection()
        for i in reversed(selected_indices):
            self.project_dirs.pop(i)
            self.project_dir_list.delete(i)

    def browse_output_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.output_dir = directory
            self.output_dir_entry.delete(0, tk.END)
            self.output_dir_entry.insert(0, directory)

    def run_documentation(self):
        self.project_dirs = [d.strip() for d in self.project_dir_list.get(0, tk.END) if d.strip()] # Lấy từ Listbox
        self.excluded_subdirs = [item.strip() for item in self.excluded_subdirs_text.get("1.0", tk.END).split("\n") if item.strip()]
        self.excluded_files = [item.strip() for item in self.excluded_files_text.get("1.0", tk.END).split("\n") if item.strip()]
        self.output_dir = self.output_dir_entry.get().strip()
        self.base_filename = self.base_filename_entry.get().strip()
        verbose = self.verbose.get()
        output_format = self.output_format.get() 

        if not self.project_dirs:
            messagebox.showerror("Lỗi", "Vui lòng chọn ít nhất một thư mục dự án.")
            return
        if not self.output_dir:
            messagebox.showerror("Lỗi", "Vui lòng chọn thư mục đầu ra.")
            return
        if not self.base_filename:
            messagebox.showerror("Lỗi", "Vui lòng nhập tên tập tin cơ sở.")
            return

        self.output_text.delete('1.0', tk.END)

        def run_in_thread():
            try:
                results = tao_tai_lieu_du_an(
                    self.project_dirs,
                    self.excluded_subdirs,
                    self.excluded_files,
                    self.base_filename,
                    self.output_dir,
                    verbose,
                    output_format  
                )
                self.root.after(0, self.update_output, results)
            except Exception as e:
                self.root.after(0, self.show_error, str(e))

        thread = Thread(target=run_in_thread)
        thread.start()

    def update_output(self, results):
        message, execution_time, num_files, num_folders, errors, skipped_files, skipped_folders = results
        formatted_output = format_output_for_tkinter(message, execution_time, num_files, num_folders, errors, skipped_files, skipped_folders)
        self.output_text.insert(tk.END, formatted_output)
        self.output_text.see(tk.END)
        messagebox.showinfo("Hoàn thành", "Tạo tài liệu dự án hoàn tất!")

    def show_error(self, error_message):
        self.output_text.insert(tk.END, f"LỖI: {error_message}\n")
        self.output_text.see(tk.END)


def tao_tai_lieu_du_an(duong_dan_thu_muc, thu_muc_con_loai_tru=None, tep_loai_tru=None, ten_tep_co_so="tai_lieu_du_an", thu_muc_dau_ra=".", verbose=False, output_format="Plain Text"):
    """Hàm tạo tài liệu (giữ nguyên)"""
    if not isinstance(duong_dan_thu_muc, (list, tuple)):
        raise TypeError("duong_dan_thu_muc phải là list hoặc tuple")
    if not duong_dan_thu_muc:
        raise ValueError("duong_dan_thu_muc không được rỗng")

    start_time = time.time()

    if thu_muc_con_loai_tru is None:
        thu_muc_con_loai_tru = []
    if tep_loai_tru is None:
        tep_loai_tru = []

    tep_loai_tru_set = set(tep_loai_tru)
    thu_muc_con_loai_tru_set = set(thu_muc_con_loai_tru)

    os.makedirs(thu_muc_dau_ra, exist_ok=True)

    total_files_processed = 0
    total_folders_processed = 0
    all_errors = {}
    all_skipped_files = []
    all_skipped_folders = []

    for duong_dan in duong_dan_thu_muc:
        if not os.path.isdir(duong_dan):
            all_errors[duong_dan] = "Thư mục không tồn tại"
            continue

        ten_thu_muc_du_an = os.path.basename(duong_dan)
        thu_muc_dau_ra_du_an = os.path.join(thu_muc_dau_ra, ten_thu_muc_du_an)
        os.makedirs(thu_muc_dau_ra_du_an, exist_ok=True)

        # Xác định phần mở rộng dựa trên định dạng đầu ra
        if output_format == "Markdown":
            file_extension = ".md"
        elif output_format == "HTML":
            file_extension = ".html"
        else:
            file_extension = ".txt"

        ten_file = os.path.join(thu_muc_dau_ra_du_an, f"{ten_tep_co_so}{file_extension}")
        count = 1
        while os.path.exists(ten_file):
            ten_file = os.path.join(thu_muc_dau_ra_du_an, f"{ten_tep_co_so} {count}{file_extension}")
            count += 1

        num_files_processed = 0
        num_folders_processed = 0
        errors = {}
        skipped_files_list = []
        skipped_folders_list = []

        # Mở file với encoding utf-8 và xử lý lỗi
        try:
            outfile = codecs.open(ten_file, "w", "utf-8")
        except OSError as e:
            all_errors[ten_file] = str(e)
            return (f"Không thể mở tệp đầu ra: {ten_file}", 0, 0, 0, all_errors, [], [])

        with outfile:
            if output_format == "HTML":
                outfile.write("<!DOCTYPE html>\n<html>\n<head>\n<title>Tài liệu dự án</title>\n<meta charset='utf-8'>\n</head>\n<body>\n")
                outfile.write(f"<h1>Dự án: {ten_thu_muc_du_an}</h1>\n")
            else:
                 outfile.write(f"Dự án: {ten_thu_muc_du_an} - ...\n\n")

            def viet_cau_truc_thu_muc(thu_muc_goc, indent_level=0):
                nonlocal num_folders_processed
                if output_format == "Markdown":
                    thut_le = "    " * indent_level + "* "
                elif output_format == "HTML":
                    thut_le = "    " * indent_level + "• "  
                else: # Plain Text
                    thut_le = "│   " * indent_level + "├── "

                try:
                    with os.scandir(thu_muc_goc) as entries:
                        for entry in entries:
                            if entry.is_dir(follow_symlinks=False):
                                if entry.name in thu_muc_con_loai_tru_set:
                                    if output_format == "HTML":
                                         outfile.write(thut_le + f"<b>{entry.name}/</b> (Ko liệt kê)<br>\n")
                                    else:
                                        outfile.write(thut_le + f"{entry.name}/ (Ko liệt kê)\n")
                                    skipped_folders_list.append(os.path.relpath(entry.path, duong_dan))
                                    continue

                                if output_format == "HTML":
                                    outfile.write(thut_le + f"<b>{entry.name}/</b><br>\n")
                                elif output_format == "Markdown":
                                     outfile.write(thut_le + f"{entry.name}/\n")
                                else: #Plain Text
                                    outfile.write(thut_le + f"{entry.name}/\n")
                                num_folders_processed += 1
                                viet_cau_truc_thu_muc(entry.path, indent_level + 1)
                            elif entry.is_file(follow_symlinks=False):
                                if entry.name.endswith(tuple(tep_loai_tru)) or entry.name in tep_loai_tru_set:
                                    skipped_files_list.append(os.path.relpath(entry.path, duong_dan))
                                    continue

                                if output_format == "HTML":
                                    outfile.write(thut_le + f"<i>{entry.name}</i><br>\n")
                                elif output_format == "Markdown":
                                    outfile.write(thut_le + f"{entry.name}\n")
                                else: # Plain Text
                                     outfile.write(thut_le + f"{entry.name}\n")

                except FileNotFoundError:
                    error_msg = f"{os.path.basename(thu_muc_goc)}/ (Không tìm thấy thư mục)\n"
                    if output_format == "HTML":
                        outfile.write(thut_le + error_msg.replace("\n", "<br>") )
                    else:
                        outfile.write(thut_le + error_msg)
                    errors[os.path.basename(thu_muc_goc)] = "Không tìm thấy thư mục"
                except PermissionError:
                    error_msg = f"{os.path.basename(thu_muc_goc)}/ (Không có quyền truy cập)\n"
                    if output_format == "HTML":
                         outfile.write(thut_le + error_msg.replace("\n", "<br>"))
                    else:
                        outfile.write(thut_le + error_msg)

                    errors[os.path.basename(thu_muc_goc)] = "Không có quyền truy cập"
                except OSError as e:
                    error_msg = f"{os.path.basename(thu_muc_goc)}/ (Lỗi hệ thống: {e})\n"
                    if output_format == "HTML":
                        outfile.write(thut_le + error_msg.replace("\n", "<br>"))
                    else:
                        outfile.write(thut_le + error_msg)
                    errors[os.path.basename(thu_muc_goc)] = f"Lỗi hệ thống: {e}"

            def viet_noi_dung_tep(thu_muc_goc):
                nonlocal num_files_processed

                try:
                    with os.scandir(thu_muc_goc) as entries:
                        for entry in entries:
                            if entry.is_dir(follow_symlinks=False):
                                if entry.name in thu_muc_con_loai_tru_set:
                                    continue
                                viet_noi_dung_tep(entry.path)
                            elif entry.is_file(follow_symlinks=False):
                                if entry.name.endswith(tuple(tep_loai_tru)) or entry.name in tep_loai_tru_set:
                                    skipped_files_list.append(os.path.relpath(entry.path, duong_dan))
                                    continue
                                if entry.name.endswith(('.py', '.js', '.java', '.cpp', '.html', '.css', '.bat', '.sh', '.txt', '.env')):

                                    if output_format == "HTML":
                                        outfile.write(f"<p><b>{os.path.relpath(entry.path, thu_muc_goc)}</b></p>\n")
                                        outfile.write("<pre><code class='hljs'>")
                                    elif output_format == "Markdown":
                                        outfile.write(f"**{os.path.relpath(entry.path, thu_muc_goc)}**\n")
                                        outfile.write("```")
                                    else: # Plain Text
                                        outfile.write(f"**{os.path.relpath(entry.path, thu_muc_goc)}**\n")
                                        outfile.write("```")

                                    if entry.name.endswith('.bat'):
                                        if output_format == "Markdown" or output_format == "Plain Text":
                                            outfile.write("\n") 
                                    elif entry.name.endswith('.py'):
                                         if output_format == "Markdown" or output_format == "Plain Text":
                                            outfile.write("python\n")
                                    elif entry.name.endswith('.js'):
                                        if output_format == "Markdown" or output_format == "Plain Text":
                                            outfile.write("javascript\n")
                                    elif entry.name.endswith('.java'):
                                        if output_format == "Markdown" or output_format == "Plain Text":
                                            outfile.write("java\n")
                                    elif entry.name.endswith('.cpp'):
                                         if output_format == "Markdown" or output_format == "Plain Text":
                                            outfile.write("cpp\n")
                                    elif entry.name.endswith('.html'):
                                        if output_format == "Markdown" or output_format == "Plain Text":
                                            outfile.write("html\n")
                                    elif entry.name.endswith('.css'):
                                        if output_format == "Markdown" or output_format == "Plain Text":
                                            outfile.write("css\n")
                                    elif entry.name.endswith('.sh'):
                                         if output_format == "Markdown" or output_format == "Plain Text":
                                            outfile.write("bash\n") 
                                    elif entry.name.endswith('.env'):
                                        if output_format == "Markdown" or output_format == "Plain Text":
                                            outfile.write("\n")
                                    else:
                                        if output_format == "Markdown" or output_format == "Plain Text":
                                             outfile.write("\n")

                                    try:
                                        with open(entry.path, "r", encoding="utf-8") as infile:
                                            file_content = infile.read()
                                            if output_format == "HTML":
                                                file_content = file_content.replace("&", "&").replace("<", "<").replace(">", ">")
                                            outfile.write(file_content)
                                        num_files_processed += 1
                                    except UnicodeDecodeError:
                                        try:
                                            with open(entry.path, "r", encoding="latin-1") as infile:
                                                file_content = infile.read()
                                                if output_format == "HTML":
                                                    file_content = file_content.replace("&", "&").replace("<", "<").replace(">", ">")
                                                outfile.write(file_content)

                                            num_files_processed += 1
                                            error_msg = "\n\n(Lưu ý: Tệp này có thể không được mã hóa bằng UTF-8, nội dung có thể khác)\n"
                                            if output_format == "HTML":
                                                outfile.write(error_msg.replace("\n", "<br>"))
                                            else:
                                                outfile.write(error_msg)
                                        except Exception as e:
                                            error_msg = f"Không thể đọc tệp {entry.path}...\n"
                                            if output_format == "HTML":
                                                outfile.write(error_msg.replace("\n", "<br>"))
                                            else:
                                                outfile.write(error_msg)
                                            errors[entry.path] = str(e)
                                    except FileNotFoundError:
                                        error_msg = f"Không tìm thấy tệp {entry.path}...\n"
                                        if output_format == "HTML":
                                             outfile.write(error_msg.replace("\n", "<br>"))
                                        else:
                                             outfile.write(error_msg)

                                        errors[entry.path] = "Không tìm thấy tệp"
                                    except PermissionError:
                                        error_msg = f"Không có quyền truy cập tệp {entry.path}...\n"
                                        if output_format == "HTML":
                                            outfile.write(error_msg.replace("\n", "<br>"))
                                        else:
                                            outfile.write(error_msg)
                                        errors[entry.path] = "Không có quyền truy cập"
                                    except OSError as e:
                                        error_msg = f"Lỗi khi đọc tệp {entry.path}: {e}\n"
                                        if output_format == "HTML":
                                            outfile.write(error_msg.replace("\n", "<br>"))
                                        else:
                                            outfile.write(error_msg)
                                        errors[entry.path] = f"Lỗi hệ thống: {e}"

                                    if output_format == "HTML":
                                         outfile.write("</code></pre>\n")
                                    elif output_format == "Markdown":
                                        outfile.write("\n```\n\n")
                                    else: # Plain Text
                                        outfile.write("\n```\n\n")

                except FileNotFoundError:
                    errors[thu_muc_goc] = "Không tìm thấy thư mục"
                except PermissionError:
                    errors[thu_muc_goc] = "Không có quyền truy cập"
                except OSError as e:
                    errors[thu_muc_goc] = f"Lỗi hệ thống: {e}"


            if output_format == "HTML":
                outfile.write(f"<h2>{os.path.basename(duong_dan)}/</h2>\n")
            else:
                outfile.write(f"{os.path.basename(duong_dan)}/\n")

            viet_cau_truc_thu_muc(duong_dan)
            outfile.write("\n")
            viet_noi_dung_tep(duong_dan)
            if output_format == "HTML":
                outfile.write("\n</body>\n</html>") 
            else:
                outfile.write("\n\n")


        total_files_processed += num_files_processed
        total_folders_processed += num_folders_processed
        all_errors.update(errors)
        all_skipped_files.extend(skipped_files_list)
        all_skipped_folders.extend(skipped_folders_list)

    end_time = time.time()
    execution_time = end_time - start_time

    if output_format == "HTML" or output_format == "Markdown":
        message = f"Tài liệu dự án ({output_format}) đã được tạo trong {thu_muc_dau_ra}"
    else:
        message = f"Tài liệu dự án đã được tạo trong {thu_muc_dau_ra}"
    if verbose:
        message += f"\nĐã xử lý {total_files_processed} tệp và {total_folders_processed} thư mục."

    return (message, execution_time, total_files_processed, total_folders_processed,
            all_errors, all_skipped_files, all_skipped_folders)

if __name__ == "__main__":
    root = ctk.CTk() 
    app = ProjectDocApp(root)
    root.mainloop()