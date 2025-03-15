import os
import time
import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox
from threading import Thread
import customtkinter as ctk
from tkinter import ttk
import subprocess

# Cấu hình giao diện mặc định của CustomTkinter
ctk.set_appearance_mode("dark") # Chế độ giao diện: "light", "dark", "system"
ctk.set_default_color_theme("blue") # Chủ đề màu: "blue", "green", "dark-blue"

# Lớp CustomScrolledText kế thừa từ ctk.CTkFrame để tạo vùng văn bản có thanh cuộn tùy chỉnh
class CustomScrolledText(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master)
        self.grid_columnconfigure(0, weight=1) # Cấu hình cột 0 để mở rộng theo chiều ngang
        self.grid_rowconfigure(0, weight=1)    # Cấu hình hàng 0 để mở rộng theo chiều dọc
        self.text = ctk.CTkTextbox(self, **kwargs) # Tạo đối tượng ctk.CTkTextbox
        self.text.grid(row=0, column=0, sticky="nsew") # Đặt textbox vào lưới và mở rộng theo mọi hướng

# Hàm định dạng đầu ra để hiển thị trên giao diện Tkinter
def format_output_for_tkinter(message, execution_time=None, num_files=0, num_folders=0, errors=None, skipped_files=None, skipped_folders=None, output_format="txt"):
    output_text = ""
    if execution_time is not None:
        if output_format == "txt":
            output_text += f"✨ Hoàn tất ({execution_time:.2f}s) ✨\n" # Thông báo hoàn thành (định dạng văn bản)
        elif output_format == "markdown":
             output_text += f"## ✨ Hoàn tất ({execution_time:.2f}s) ✨\n" # Thông báo hoàn thành (định dạng markdown)
    else:
        if output_format == "txt":
            output_text += "[Xử lý file]\n" # Thông báo đang xử lý (định dạng văn bản)
        elif output_format == "markdown":
            output_text += "### [Xử lý file]\n" # Thông báo đang xử lý (định dạng markdown)

    if message:
        if output_format == "txt":
            output_text += f"✅ {message}\n" # Thông báo thành công (định dạng văn bản)
        elif output_format == "markdown":
            output_text += f"✅ {message}\n\n" # Thông báo thành công (định dạng markdown)

    if num_files > 0 or num_folders > 0:
        if output_format == "txt":
            output_text += f"   📁 Thư mục đã quét: {num_folders}\n" # Số thư mục đã quét (định dạng văn bản)
            output_text += f"   📄 Tệp đã quét: {num_files}\n" # Số tệp đã quét (định dạng văn bản)
        elif output_format == "markdown":
            output_text += f"- 📁 Thư mục đã quét: {num_folders}\n" # Số thư mục đã quét (định dạng markdown)
            output_text += f"- 📄 Tệp đã quét: {num_files}\n" # Số tệp đã quét (định dạng markdown)

    if skipped_folders:
        if output_format == "txt":
            output_text += "   📂 Thư mục bỏ qua:\n" # Danh sách thư mục bị bỏ qua (định dạng văn bản)
        elif output_format == "markdown":
            output_text += "- 📂 Thư mục bỏ qua:\n" # Danh sách thư mục bị bỏ qua (định dạng markdown)
        for folder in skipped_folders:
            if output_format == "txt":
                output_text += f"      - {folder}\n" # Tên thư mục bị bỏ qua (định dạng văn bản)
            elif output_format == "markdown":
                output_text += f"    - {folder}\n" # Tên thư mục bị bỏ qua (định dạng markdown)

    if skipped_files:
        if output_format == "txt":
            output_text += "   📄 Tệp bỏ qua:\n" # Danh sách tệp bị bỏ qua (định dạng văn bản)
        elif output_format == "markdown":
            output_text += "- 📄 Tệp bỏ qua:\n" # Danh sách tệp bị bỏ qua (định dạng markdown)
        for file in skipped_files:
            if output_format == "txt":
                output_text += f"      - {file}\n" # Tên tệp bị bỏ qua (định dạng văn bản)
            elif output_format == "markdown":
                output_text += f"    - {file}\n" # Tên tệp bị bỏ qua (định dạng markdown)

    if errors:
        if output_format == "txt":
            output_text += "❌ Lỗi:\n" # Thông báo lỗi (định dạng văn bản)
        elif output_format == "markdown":
            output_text += "- ❌ Lỗi:\n" # Thông báo lỗi (định dạng markdown)
        for error_item, error_msg in errors.items():
            if "No such file or directory" in error_msg:
                output_text += f"    - {error_item}: Không tìm thấy tệp/thư mục\n" # Lỗi không tìm thấy (định dạng văn bản)
            elif "Permission denied" in error_msg:
                output_text += f"    - {error_item}: Lỗi truy cập (Permission denied)\n" # Lỗi quyền truy cập (định dạng văn bản)
            else:
                output_text += f"    - {error_item}: {error_msg}\n" # Lỗi khác (định dạng văn bản)
    return output_text

# Hàm chính tạo tài liệu dự án
def tao_tai_lieu_du_an(duong_dan_thu_muc, thu_muc_con_loai_tru=None, tep_loai_tru=None, ten_tep_co_so="tai_lieu_du_an", thu_muc_dau_ra=".", verbose=False, output_format="txt"):
    """
    Tạo tài liệu dự án từ một hoặc nhiều thư mục nguồn.

    Args:
        duong_dan_thu_muc (list hoặc tuple): Danh sách hoặc tuple các đường dẫn thư mục dự án.
        thu_muc_con_loai_tru (list, tùy chọn): Danh sách các tên thư mục con cần loại trừ. Mặc định là None.
        tep_loai_tru (list, tùy chọn): Danh sách các phần mở rộng tệp hoặc tên tệp cần loại trừ. Mặc định là None.
        ten_tep_co_so (str, tùy chọn): Tên cơ sở cho tệp tài liệu đầu ra. Mặc định là "tai_lieu_du_an".
        thu_muc_dau_ra (str, tùy chọn): Đường dẫn thư mục đầu ra để lưu tài liệu. Mặc định là thư mục hiện tại ".".
        verbose (bool, tùy chọn): Cờ verbose để hiển thị thông tin chi tiết hơn. Mặc định là False.
        output_format (str, tùy chọn): Định dạng đầu ra, có thể là "txt" hoặc "markdown". Mặc định là "txt".

    Returns:
        tuple: Một tuple chứa thông báo, thời gian thực thi, số tệp đã xử lý, số thư mục đã xử lý,
               lỗi, tệp bị bỏ qua, thư mục bị bỏ qua và đường dẫn tệp đầu ra.

    Raises:
        TypeError: Nếu duong_dan_thu_muc không phải là list hoặc tuple.
        ValueError: Nếu duong_dan_thu_muc rỗng hoặc output_format không hợp lệ.
    """

    # Kiểm tra đầu vào
    if not isinstance(duong_dan_thu_muc, (list, tuple)):
        raise TypeError("duong_dan_thu_muc phải là list hoặc tuple") # Báo lỗi nếu đầu vào không đúng kiểu
    if not duong_dan_thu_muc:
        raise ValueError("duong_dan_thu_muc không được rỗng") # Báo lỗi nếu danh sách đường dẫn thư mục rỗng
    if output_format not in ("txt", "markdown"):
        raise ValueError("output_format phải là 'txt' hoặc 'markdown'") # Báo lỗi nếu định dạng đầu ra không hợp lệ

    start_time = time.time() # Ghi lại thời gian bắt đầu

    if thu_muc_con_loai_tru is None:
        thu_muc_con_loai_tru = [] # Khởi tạo danh sách thư mục con loại trừ nếu chưa được cung cấp
    if tep_loai_tru is None:
        tep_loai_tru = [] # Khởi tạo danh sách tệp loại trừ nếu chưa được cung cấp

    # Tạo set chứa các tệp và thư mục loại trừ để tìm kiếm nhanh hơn
    tep_loai_tru_set = set(tep_loai_tru) # Chuyển danh sách tệp loại trừ thành set để tìm kiếm nhanh
    thu_muc_con_loai_tru_set = set(thu_muc_con_loai_tru) # Chuyển danh sách thư mục con loại trừ thành set để tìm kiếm nhanh

    os.makedirs(thu_muc_dau_ra, exist_ok=True) # Tạo thư mục đầu ra nếu chưa tồn tại

    total_files_processed = 0 # Biến đếm tổng số tệp đã xử lý
    total_folders_processed = 0 # Biến đếm tổng số thư mục đã xử lý
    all_errors = {} # Từ điển lưu trữ tất cả lỗi
    all_skipped_files = [] # Danh sách lưu trữ tất cả tệp bị bỏ qua
    all_skipped_folders = [] # Danh sách lưu trữ tất cả thư mục bị bỏ qua
    all_output_paths = []  # Danh sách lưu trữ đường dẫn của tất cả các tệp đầu ra

    for duong_dan in duong_dan_thu_muc: # Lặp qua từng đường dẫn thư mục đầu vào
        if not os.path.isdir(duong_dan):
            all_errors[duong_dan] = "Thư mục không tồn tại" # Ghi lỗi nếu thư mục không tồn tại
            continue # Chuyển sang thư mục tiếp theo nếu thư mục hiện tại không tồn tại

        ten_thu_muc_du_an = os.path.basename(duong_dan) # Lấy tên thư mục dự án từ đường dẫn
        thu_muc_dau_ra_du_an = os.path.join(thu_muc_dau_ra, ten_thu_muc_du_an) # Tạo đường dẫn thư mục đầu ra cho dự án
        os.makedirs(thu_muc_dau_ra_du_an, exist_ok=True) # Tạo thư mục đầu ra dự án nếu chưa tồn tại

        file_extension = ".txt" if output_format == "txt" else ".md" # Xác định phần mở rộng tệp dựa trên định dạng đầu ra
        ten_file = os.path.join(thu_muc_dau_ra_du_an, f"{ten_tep_co_so}{file_extension}") # Tạo đường dẫn đầy đủ cho tệp đầu ra

        count = 1
        while os.path.exists(ten_file):
            ten_file = os.path.join(thu_muc_dau_ra_du_an, f"{ten_tep_co_so} {count}{file_extension}") # Thêm số đếm vào tên tệp nếu tệp đã tồn tại
            count += 1

        all_output_paths.append(os.path.abspath(ten_file))  # Thêm đường dẫn tuyệt đối của tệp đầu ra vào danh sách

        num_files_processed = 0 # Đặt lại bộ đếm tệp đã xử lý cho mỗi thư mục dự án
        num_folders_processed = 0 # Đặt lại bộ đếm thư mục đã xử lý cho mỗi thư mục dự án
        errors = {} # Đặt lại từ điển lỗi cho mỗi thư mục dự án
        skipped_files_list = [] # Đặt lại danh sách tệp bị bỏ qua cho mỗi thư mục dự án
        skipped_folders_list = [] # Đặt lại danh sách thư mục bị bỏ qua cho mỗi thư mục dự án

        with open(ten_file, "w", encoding="utf-8") as outfile: # Mở tệp đầu ra để ghi, mã hóa UTF-8
            if output_format == "markdown":
                outfile.write(f"# Dự án: {ten_thu_muc_du_an} - ...\n\n") # Viết tiêu đề dự án (markdown)
            else:
                outfile.write(f"Dự án: {ten_thu_muc_du_an} - ...\n\n") # Viết tiêu đề dự án (văn bản)

            def viet_cau_truc_thu_muc(thu_muc_goc, indent_level=0):
                """
                Đệ quy viết cấu trúc thư mục vào tệp đầu ra.

                Args:
                    thu_muc_goc (str): Đường dẫn thư mục gốc hiện tại.
                    indent_level (int): Mức thụt lề hiện tại.
                """
                nonlocal num_folders_processed # Cho phép sửa đổi biến bên ngoài hàm
                if output_format == "txt":
                    thut_le = "│   " * indent_level + "├── " # Thụt lề cho định dạng văn bản
                elif output_format == "markdown":
                    thut_le = "    " * indent_level + "- " # Thụt lề cho định dạng markdown

                try:
                    with os.scandir(thu_muc_goc) as entries: # Sử dụng os.scandir để duyệt thư mục hiệu quả hơn
                        for entry in entries: # Lặp qua các mục trong thư mục
                            if entry.is_dir(follow_symlinks=False): # Kiểm tra nếu mục là thư mục (không theo liên kết tượng trưng)
                                if entry.name in thu_muc_con_loai_tru_set: # Kiểm tra nếu thư mục bị loại trừ
                                    if output_format == "txt":
                                        outfile.write(thut_le + f"{entry.name}/ (Ko liệt kê)\n") # Ghi thư mục bị loại trừ (văn bản)
                                    elif output_format == "markdown":
                                        outfile.write(thut_le + f"{entry.name}/ (Không liệt kê)\n") # Ghi thư mục bị loại trừ (markdown)
                                    skipped_folders_list.append(os.path.relpath(entry.path, duong_dan)) # Thêm thư mục bị bỏ qua vào danh sách
                                    continue # Chuyển sang mục tiếp theo
                                if output_format == "txt":
                                    outfile.write(thut_le + f"{entry.name}/\n") # Ghi tên thư mục (văn bản)
                                elif output_format == "markdown":
                                    outfile.write(thut_le + f"{entry.name}/\n") # Ghi tên thư mục (markdown)

                                num_folders_processed += 1 # Tăng bộ đếm thư mục đã xử lý
                                viet_cau_truc_thu_muc(entry.path, indent_level + 1) # Đệ quy gọi hàm cho thư mục con
                            elif entry.is_file(follow_symlinks=False): # Kiểm tra nếu mục là tệp (không theo liên kết tượng trưng)
                                if entry.name.endswith(tuple(tep_loai_tru)) or entry.name in tep_loai_tru_set: # Kiểm tra nếu tệp bị loại trừ
                                    skipped_files_list.append(os.path.relpath(entry.path, duong_dan)) # Thêm tệp bị bỏ qua vào danh sách
                                    continue # Chuyển sang mục tiếp theo
                                outfile.write(thut_le + f"{entry.name}\n") # Ghi tên tệp

                except FileNotFoundError: # Bắt lỗi FileNotFoundError
                    outfile.write(thut_le + f"{os.path.basename(thu_muc_goc)}/ (Không tìm thấy thư mục)\n") # Ghi lỗi không tìm thấy thư mục
                    errors[os.path.basename(thu_muc_goc)] = "Không tìm thấy thư mục" # Lưu lỗi vào từ điển
                except PermissionError: # Bắt lỗi PermissionError
                    outfile.write(thut_le + f"{os.path.basename(thu_muc_goc)}/ (Không có quyền truy cập)\n") # Ghi lỗi quyền truy cập
                    errors[os.path.basename(thu_muc_goc)] = "Không có quyền truy cập" # Lưu lỗi vào từ điển
                except OSError as e: # Bắt lỗi OSError chung
                    outfile.write(thut_le + f"{os.path.basename(thu_muc_goc)}/ (Lỗi hệ thống: {e})\n") # Ghi lỗi hệ thống
                    errors[os.path.basename(thu_muc_goc)] = f"Lỗi hệ thống: {e}" # Lưu lỗi vào từ điển


            def viet_noi_dung_tep(thu_muc_goc):
                """
                Đệ quy viết nội dung của các tệp mã nguồn được hỗ trợ vào tệp đầu ra.

                Args:
                    thu_muc_goc (str): Đường dẫn thư mục gốc hiện tại.
                """
                nonlocal num_files_processed # Cho phép sửa đổi biến bên ngoài hàm

                try:
                    with os.scandir(thu_muc_goc) as entries: # Sử dụng os.scandir để duyệt thư mục hiệu quả hơn
                        for entry in entries: # Lặp qua các mục trong thư mục
                            if entry.is_dir(follow_symlinks=False): # Kiểm tra nếu mục là thư mục (không theo liên kết tượng trưng)
                                if entry.name in thu_muc_con_loai_tru_set: # Kiểm tra nếu thư mục bị loại trừ
                                    continue # Chuyển sang mục tiếp theo
                                viet_noi_dung_tep(entry.path) # Đệ quy gọi hàm cho thư mục con
                            elif entry.is_file(follow_symlinks=False): # Kiểm tra nếu mục là tệp (không theo liên kết tượng trưng)
                                if entry.name.endswith(tuple(tep_loai_tru)) or entry.name in tep_loai_tru_set: # Kiểm tra nếu tệp bị loại trừ
                                    skipped_files_list.append(os.path.relpath(entry.path, duong_dan)) # Thêm tệp bị bỏ qua vào danh sách
                                    continue # Chuyển sang mục tiếp theo
                                if entry.name.endswith(('.py', '.js', '.java', '.cpp', '.html', '.css', '.bat', '.sh', '.txt', '.env')): # Kiểm tra phần mở rộng tệp được hỗ trợ
                                    if output_format == "markdown":
                                      outfile.write(f"**{os.path.relpath(entry.path, thu_muc_goc)}**\n\n") # Ghi tên tệp (markdown, in đậm)
                                      outfile.write("```") # Bắt đầu khối mã (markdown)
                                    else:
                                      outfile.write(f"**{os.path.relpath(entry.path, thu_muc_goc)}**\n") # Ghi tên tệp (văn bản, in đậm)
                                      outfile.write("```") # Bắt đầu khối mã (văn bản)

                                    if entry.name.endswith('.bat'):
                                        outfile.write("\n") # Không thêm ngôn ngữ cho .bat
                                    elif entry.name.endswith('.py'):
                                         outfile.write("python\n") # Thêm ngôn ngữ python cho .py
                                    else:
                                        outfile.write("\n") # Thêm dòng mới sau ngôn ngữ

                                    try:
                                        with open(entry.path, "r", encoding="utf-8") as infile: # Mở tệp để đọc, mã hóa UTF-8
                                            outfile.write(infile.read()) # Đọc và ghi nội dung tệp
                                        num_files_processed += 1 # Tăng bộ đếm tệp đã xử lý
                                    except UnicodeDecodeError: # Bắt lỗi UnicodeDecodeError
                                        try:
                                            with open(entry.path, "r", encoding="latin-1") as infile: # Thử đọc lại với mã hóa latin-1
                                                outfile.write(infile.read()) # Đọc và ghi nội dung tệp
                                            num_files_processed += 1 # Tăng bộ đếm tệp đã xử lý
                                            if output_format == "txt":
                                                outfile.write("\n\n(Lưu ý: Tệp này có thể không được mã hóa bằng UTF-8, nội dung có thể khác)\n") # Chú thích mã hóa (văn bản)
                                            elif output_format == "markdown":
                                                outfile.write("\n\n_(Lưu ý: Tệp này có thể không được mã hóa bằng UTF-8, nội dung có thể khác)_\n") # Chú thích mã hóa (markdown)
                                        except Exception as e: # Bắt lỗi chung nếu vẫn không đọc được
                                            outfile.write(f"Không thể đọc tệp {entry.path}...\n") # Thông báo lỗi đọc tệp
                                            errors[entry.path] = str(e) # Lưu lỗi vào từ điển
                                    except FileNotFoundError: # Bắt lỗi FileNotFoundError
                                        outfile.write(f"Không tìm thấy tệp {entry.path}...\n") # Thông báo lỗi không tìm thấy tệp
                                        errors[entry.path] = "Không tìm thấy tệp" # Lưu lỗi vào từ điển
                                    except PermissionError: # Bắt lỗi PermissionError
                                        outfile.write(f"Không có quyền truy cập tệp {entry.path}...\n") # Thông báo lỗi quyền truy cập
                                        errors[entry.path] = "Không có quyền truy cập" # Lưu lỗi vào từ điển
                                    except OSError as e: # Bắt lỗi OSError chung
                                        outfile.write(f"Lỗi khi đọc tệp {entry.path}: {e}\n") # Thông báo lỗi hệ thống khi đọc tệp
                                        errors[entry.path] = f"Lỗi hệ thống: {e}" # Lưu lỗi vào từ điển
                                    outfile.write("\n```\n\n") # Kết thúc khối mã

                except FileNotFoundError: # Bắt lỗi FileNotFoundError
                      errors[thu_muc_goc] = "Không tìm thấy thư mục" # Lưu lỗi vào từ điển
                except PermissionError: # Bắt lỗi PermissionError
                    errors[thu_muc_goc] = "Không có quyền truy cập" # Lưu lỗi vào từ điển
                except OSError as e: # Bắt lỗi OSError chung
                    errors[thu_muc_goc] = f"Lỗi hệ thống: {e}" # Lưu lỗi vào từ điển


            outfile.write(f"{os.path.basename(duong_dan)}/\n") # Ghi tên thư mục gốc
            viet_cau_truc_thu_muc(duong_dan) # Gọi hàm viết cấu trúc thư mục
            outfile.write("\n") # Thêm dòng mới
            viet_noi_dung_tep(duong_dan) # Gọi hàm viết nội dung tệp
            outfile.write("\n\n") # Thêm hai dòng mới

        total_files_processed += num_files_processed # Cộng dồn số tệp đã xử lý
        total_folders_processed += num_folders_processed # Cộng dồn số thư mục đã xử lý
        all_errors.update(errors) # Cập nhật từ điển lỗi tổng hợp
        all_skipped_files.extend(skipped_files_list) # Mở rộng danh sách tệp bị bỏ qua tổng hợp
        all_skipped_folders.extend(skipped_folders_list) # Mở rộng danh sách thư mục bị bỏ qua tổng hợp

    end_time = time.time() # Ghi lại thời gian kết thúc
    execution_time = end_time - start_time # Tính thời gian thực thi
    message = f"Tài liệu dự án đã được tạo trong {thu_muc_dau_ra}" # Thông báo thành công
    if verbose:
        message += f"\nĐã xử lý {total_files_processed} tệp và {total_folders_processed} thư mục." # Thêm thông tin chi tiết nếu verbose

    output_paths_str = ", ".join(all_output_paths) # Tạo chuỗi đường dẫn tệp đầu ra
    return (message, execution_time, total_files_processed, total_folders_processed,
            all_errors, all_skipped_files, all_skipped_folders, output_paths_str) # Trả về kết quả

# Lớp chính của ứng dụng giao diện người dùng
class ProjectDocApp:
    def __init__(self, root):
        self.root = root # Lưu cửa sổ gốc
        root.title("Tạo Tài Liệu Dự Án") # Đặt tiêu đề cửa sổ
        root.geometry("1000x800") # Đặt kích thước cửa sổ ban đầu
        root.minsize(800, 700) # Đặt kích thước tối thiểu của cửa sổ
        try:
            pass # Đoạn mã dự phòng có thể được thêm vào đây
        except:
            pass

        self.font_family = "Segoe UI" if os.name == "nt" else "Helvetica" # Chọn font chữ tùy thuộc vào hệ điều hành
        self.title_font = ctk.CTkFont(family=self.font_family, size=20, weight="bold") # Font chữ cho tiêu đề lớn
        self.header_font = ctk.CTkFont(family=self.font_family, size=16, weight="bold") # Font chữ cho tiêu đề phần
        self.normal_font = ctk.CTkFont(family=self.font_family, size=13) # Font chữ thường
        self.small_font = ctk.CTkFont(family=self.font_family, size=12) # Font chữ nhỏ

        # Colors - Màu sắc chủ đề
        self.primary_color = "#1E90FF"  # Dodger Blue - Xanh Dodger
        self.accent_color = "#0078D7"  # Windows blue - Xanh Windows
        self.hover_color = "#005A9E"  # Darker blue for hover - Xanh đậm hơn khi hover
        self.success_color = "#28A745"  # Green - Xanh lá cây (thành công)
        self.warning_color = "#FFC107"  # Yellow - Vàng (cảnh báo)
        self.error_color = "#DC3545"  # Red - Đỏ (lỗi)

        # Variables - Biến
        self.project_dirs = [] # Danh sách thư mục dự án
        self.excluded_subdirs = ["__pycache__", "moitruongao", "venv", ".git", ".vscode", "bieutuong", "memory", "node_modules", "uploads", "chats"] # Thư mục con loại trừ mặc định
        self.excluded_files = [".pyc", "desktop.ini", ".rar", "ex.json", ".jpg", ".mp3"] # Tệp loại trừ mặc định
        self.output_dir = "." # Thư mục đầu ra mặc định (thư mục hiện tại)
        self.base_filename = "tai_lieu_du_an" # Tên tệp cơ sở mặc định
        self.verbose = tk.BooleanVar(value=False) # Biến BooleanVar cho tùy chọn verbose, mặc định False
        self.output_format = tk.StringVar(value="txt") # Biến StringVar cho định dạng đầu ra, mặc định "txt"
        self.progress_var = tk.DoubleVar(value=0) # Biến DoubleVar cho thanh tiến trình, mặc định 0
        self.status_var = tk.StringVar(value="Sẵn sàng") # Biến StringVar cho trạng thái ứng dụng, mặc định "Sẵn sàng"

        self.create_ui() # Gọi hàm tạo giao diện người dùng

    def create_ui(self):
        """Tạo giao diện người dùng chính."""
        self.main_container = ctk.CTkFrame(self.root) # Tạo frame chính chứa tất cả các thành phần
        self.main_container.pack(fill=tk.BOTH, expand=True, padx=15, pady=15) # Đặt frame chính vào cửa sổ, mở rộng và có padding

        self.create_header() # Tạo header
        self.create_tabs() # Tạo tabview
        self.create_status_bar() # Tạo status bar

    def create_header(self):
        """Tạo header của ứng dụng."""
        header_frame = ctk.CTkFrame(self.main_container, corner_radius=10, fg_color="transparent") # Tạo frame cho header
        header_frame.pack(fill=tk.X, padx=10, pady=(0, 15)) # Đặt frame header vào container chính, mở rộng theo chiều ngang và có padding

        icon_label = ctk.CTkLabel(header_frame, text="📁", font=ctk.CTkFont(size=32)) # Tạo label icon thư mục
        icon_label.pack(side=tk.LEFT, padx=(5, 10)) # Đặt icon label bên trái, có padding

        title_label = ctk.CTkLabel(
            header_frame,
            text="Tạo Tài Liệu Dự Án",
            font=self.title_font # Sử dụng font chữ tiêu đề
        )
        title_label.pack(side=tk.LEFT) # Đặt title label bên trái

        # Version info - Thông tin phiên bản
        version_label = ctk.CTkLabel(
            header_frame,
            text="v2.0",
            font=self.small_font, # Sử dụng font chữ nhỏ
            text_color="gray" # Màu xám
        )
        version_label.pack(side=tk.RIGHT, padx=10) # Đặt version label bên phải, có padding

    def create_tabs(self):
        """Tạo tabview và các tab."""
        # Create tabview - Tạo tabview
        self.tabview = ctk.CTkTabview(self.main_container, corner_radius=10) # Tạo đối tượng tabview
        self.tabview.pack(fill=tk.BOTH, expand=True, padx=10, pady=10) # Đặt tabview vào container chính, mở rộng và có padding

        # Create tabs - Tạo các tab
        self.tab_config = self.tabview.add("Cấu hình") # Thêm tab "Cấu hình"
        self.tab_advanced = self.tabview.add("Nâng cao") # Thêm tab "Nâng cao"
        self.tab_output = self.tabview.add("Kết quả") # Thêm tab "Kết quả"

        for tab in [self.tab_config, self.tab_advanced, self.tab_output]: # Cấu hình cho từng tab
            tab.grid_columnconfigure(0, weight=1) # Cấu hình cột 0 mở rộng theo chiều ngang
            tab.grid_rowconfigure(0, weight=1) # Cấu hình hàng 0 mở rộng theo chiều dọc

        self.create_config_tab() # Tạo nội dung tab "Cấu hình"
        self.create_advanced_tab() # Tạo nội dung tab "Nâng cao"
        self.create_output_tab() # Tạo nội dung tab "Kết quả"

    def create_config_tab(self):
        """Tạo nội dung cho tab "Cấu hình"."""

        config_scroll = ctk.CTkScrollableFrame(self.tab_config) # Tạo scrollable frame cho tab cấu hình
        config_scroll.grid(row=0, column=0, sticky="nsew", padx=5, pady=5) # Đặt scrollable frame vào tab, mở rộng và có padding
        config_scroll.columnconfigure(0, weight=1) # Cấu hình cột 0 mở rộng theo chiều ngang

        # Project directories section - Phần thư mục dự án
        dir_section = ctk.CTkFrame(config_scroll, corner_radius=10) # Tạo frame cho phần thư mục dự án
        dir_section.pack(fill=tk.X, padx=10, pady=10) # Đặt frame phần thư mục dự án vào scrollable frame, mở rộng và có padding

        section_label = ctk.CTkLabel(
            dir_section,
            text="Thư mục dự án",
            font=self.header_font, # Sử dụng font chữ header
            anchor="w" # Căn chỉnh văn bản sang trái
        )
        section_label.pack(fill=tk.X, padx=15, pady=(15, 5)) # Đặt section label vào frame phần thư mục dự án, mở rộng và có padding

        # Description - Mô tả
        desc_label = ctk.CTkLabel(
            dir_section,
            text="Chọn một hoặc nhiều thư mục dự án để tạo tài liệu.",
            font=self.normal_font, # Sử dụng font chữ thường
            anchor="w", # Căn chỉnh văn bản sang trái
            justify="left" # Căn chỉnh văn bản sang trái (đa dòng)
        )
        desc_label.pack(fill=tk.X, padx=15, pady=(0, 10)) # Đặt desc label vào frame phần thư mục dự án, mở rộng và có padding

        # Directory list frame - Frame danh sách thư mục
        dir_list_frame = ctk.CTkFrame(dir_section) # Tạo frame chứa danh sách thư mục
        dir_list_frame.pack(fill=tk.X, padx=15, pady=10) # Đặt dir_list_frame vào frame phần thư mục dự án, mở rộng và có padding

        # Directory listbox with custom styling - Listbox thư mục với kiểu dáng tùy chỉnh
        self.dir_list_frame = ctk.CTkFrame(dir_section, fg_color="transparent") # Tạo frame trong suốt chứa listbox
        self.dir_list_frame.pack(fill=tk.X, padx=15, pady=(5, 15)) # Đặt dir_list_frame vào frame phần thư mục dự án, mở rộng và có padding

        self.project_dir_list = tk.Listbox(
            self.dir_list_frame,
            height=6, # Chiều cao listbox
            selectbackground=self.accent_color, # Màu nền khi chọn
            font=(self.font_family, 12), # Font chữ listbox
            bg="#2b2b2b", # Màu nền listbox
            fg="#f2f2f2", # Màu chữ listbox
            borderwidth=1, # Độ rộng viền
            highlightthickness=0, # Độ dày highlight khi focus
            relief="flat", # Kiểu viền
            selectmode=tk.EXTENDED # Chế độ chọn (đa lựa chọn)
        )
        self.project_dir_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True) # Đặt listbox vào dir_list_frame, mở rộng theo mọi hướng

        # Add scrollbar for list - Thêm thanh cuộn cho list
        scrollbar = ctk.CTkScrollbar(self.dir_list_frame, command=self.project_dir_list.yview) # Tạo thanh cuộn dọc
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y) # Đặt thanh cuộn bên phải, mở rộng theo chiều dọc
        self.project_dir_list.config(yscrollcommand=scrollbar.set) # Liên kết thanh cuộn với listbox

        # Buttons frame - Frame nút bấm
        dir_buttons_frame = ctk.CTkFrame(dir_section, fg_color="transparent") # Tạo frame trong suốt chứa các nút
        dir_buttons_frame.pack(fill=tk.X, padx=15, pady=(0, 15)) # Đặt dir_buttons_frame vào frame phần thư mục dự án, mở rộng và có padding

        # Add directory button - Nút thêm thư mục
        self.add_dir_btn = ctk.CTkButton(
            dir_buttons_frame,
            text="Thêm thư mục",
            command=self.add_project_directory, # Liên kết với hàm add_project_directory
            font=self.normal_font, # Sử dụng font chữ thường
            fg_color=self.primary_color, # Màu nền nút
            hover_color=self.hover_color, # Màu nền khi hover
            corner_radius=8, # Độ cong góc
            height=35, # Chiều cao nút
            image=self.create_plus_icon() if hasattr(self, 'create_plus_icon') else None, # Thêm icon nếu có hàm create_plus_icon
            compound="left" # Đặt icon bên trái chữ
        )
        self.add_dir_btn.pack(side=tk.LEFT, padx=(0, 10)) # Đặt nút thêm thư mục bên trái, có padding bên phải

        # Remove directory button - Nút xóa thư mục
        self.remove_dir_btn = ctk.CTkButton(
            dir_buttons_frame,
            text="Xóa thư mục",
            command=self.remove_project_directory, # Liên kết với hàm remove_project_directory
            font=self.normal_font, # Sử dụng font chữ thường
            fg_color="#555555", # Màu nền nút (xám)
            hover_color="#444444", # Màu nền khi hover (xám đậm hơn)
            corner_radius=8, # Độ cong góc
            height=35 # Chiều cao nút
        )
        self.remove_dir_btn.pack(side=tk.LEFT) # Đặt nút xóa thư mục bên trái

        # Output directory section - Phần thư mục đầu ra
        output_section = ctk.CTkFrame(config_scroll, corner_radius=10) # Tạo frame cho phần thư mục đầu ra
        output_section.pack(fill=tk.X, padx=10, pady=10) # Đặt frame phần thư mục đầu ra vào scrollable frame, mở rộng và có padding

        # Section title - Tiêu đề phần
        output_label = ctk.CTkLabel(
            output_section,
            text="Thư mục đầu ra",
            font=self.header_font, # Sử dụng font chữ header
            anchor="w" # Căn chỉnh văn bản sang trái
        )
        output_label.pack(fill=tk.X, padx=15, pady=(15, 5)) # Đặt output label vào frame phần thư mục đầu ra, mở rộng và có padding

        # Description - Mô tả
        output_desc = ctk.CTkLabel(
            output_section,
            text="Chọn thư mục để lưu tài liệu dự án được tạo ra.",
            font=self.normal_font, # Sử dụng font chữ thường
            anchor="w", # Căn chỉnh văn bản sang trái
            justify="left" # Căn chỉnh văn bản sang trái (đa dòng)
        )
        output_desc.pack(fill=tk.X, padx=15, pady=(0, 10)) # Đặt output desc vào frame phần thư mục đầu ra, mở rộng và có padding

        # Output directory selection frame - Frame chọn thư mục đầu ra
        output_dir_frame = ctk.CTkFrame(output_section, fg_color="transparent") # Tạo frame trong suốt chứa các thành phần chọn thư mục đầu ra
        output_dir_frame.pack(fill=tk.X, padx=15, pady=(5, 15)) # Đặt output_dir_frame vào frame phần thư mục đầu ra, mở rộng và có padding

        # Output directory entry and button - Entry và nút chọn thư mục đầu ra
        self.output_dir_entry = ctk.CTkEntry(
            output_dir_frame,
            font=self.normal_font, # Sử dụng font chữ thường
            corner_radius=8, # Độ cong góc
            height=35, # Chiều cao entry
            placeholder_text="Đường dẫn thư mục đầu ra" # Văn bản gợi ý
        )
        self.output_dir_entry.insert(0, self.output_dir) # Điền đường dẫn thư mục đầu ra mặc định vào entry
        self.output_dir_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10)) # Đặt output_dir_entry bên trái, mở rộng theo chiều ngang và có padding bên phải

        # Browse button - Nút duyệt thư mục
        self.browse_btn = ctk.CTkButton(
            output_dir_frame,
            text="Duyệt...",
            command=self.browse_output_directory, # Liên kết với hàm browse_output_directory
            font=self.normal_font, # Sử dụng font chữ thường
            fg_color=self.primary_color, # Màu nền nút
            hover_color=self.hover_color, # Màu nền khi hover
            corner_radius=8, # Độ cong góc
            width=100, # Chiều rộng nút
            height=35 # Chiều cao nút
        )
        self.browse_btn.pack(side=tk.RIGHT) # Đặt nút duyệt thư mục bên phải

        # Base filename frame - Frame tên tệp cơ sở
        filename_frame = ctk.CTkFrame(output_section, fg_color="transparent") # Tạo frame trong suốt chứa các thành phần tên tệp cơ sở
        filename_frame.pack(fill=tk.X, padx=15, pady=(0, 15)) # Đặt filename_frame vào frame phần thư mục đầu ra, mở rộng và có padding

        # Base filename label - Label tên tệp cơ sở
        filename_label = ctk.CTkLabel(
            filename_frame,
            text="Tên tệp cơ sở:",
            font=self.normal_font, # Sử dụng font chữ thường
            width=120, # Chiều rộng label
            anchor="w" # Căn chỉnh văn bản sang trái
        )
        filename_label.pack(side=tk.LEFT, padx=(0, 10)) # Đặt filename_label bên trái, có padding bên phải

        # Base filename entry - Entry tên tệp cơ sở
        self.base_filename_entry = ctk.CTkEntry(
            filename_frame,
            font=self.normal_font, # Sử dụng font chữ thường
            corner_radius=8, # Độ cong góc
            height=35 # Chiều cao entry
        )
        self.base_filename_entry.insert(0, self.base_filename) # Điền tên tệp cơ sở mặc định vào entry
        self.base_filename_entry.pack(side=tk.LEFT, fill=tk.X, expand=True) # Đặt base_filename_entry bên trái, mở rộng theo chiều ngang

        # Format options frame - Frame tùy chọn định dạng
        format_section = ctk.CTkFrame(config_scroll, corner_radius=10) # Tạo frame cho phần tùy chọn định dạng
        format_section.pack(fill=tk.X, padx=10, pady=10) # Đặt format_section vào scrollable frame, mở rộng và có padding

        # Section title - Tiêu đề phần
        format_label = ctk.CTkLabel(
            format_section,
            text="Định dạng đầu ra",
            font=self.header_font, # Sử dụng font chữ header
            anchor="w" # Căn chỉnh văn bản sang trái
        )
        format_label.pack(fill=tk.X, padx=15, pady=(15, 5)) # Đặt format_label vào frame phần tùy chọn định dạng, mở rộng và có padding

        # Format options - Tùy chọn định dạng
        format_options = ctk.CTkFrame(format_section, fg_color="transparent") # Tạo frame trong suốt chứa các tùy chọn định dạng
        format_options.pack(fill=tk.X, padx=15, pady=(5, 15)) # Đặt format_options vào frame phần tùy chọn định dạng, mở rộng và có padding

        # Format radio buttons - Nút radio định dạng
        self.txt_radio = ctk.CTkRadioButton(
            format_options,
            text="Văn bản (.txt)",
            variable=self.output_format, # Liên kết với biến output_format
            value="txt", # Giá trị khi chọn
            font=self.normal_font, # Sử dụng font chữ thường
            fg_color=self.accent_color # Màu nền khi chọn
        )
        self.txt_radio.pack(side=tk.LEFT, padx=(0, 20)) # Đặt nút radio txt bên trái, có padding bên phải

        self.md_radio = ctk.CTkRadioButton(
            format_options,
            text="Markdown (.md)",
            variable=self.output_format, # Liên kết với biến output_format
            value="markdown", # Giá trị khi chọn
            font=self.normal_font, # Sử dụng font chữ thường
            fg_color=self.accent_color # Màu nền khi chọn
        )
        self.md_radio.pack(side=tk.LEFT) # Đặt nút radio markdown bên trái

        # Verbose option - Tùy chọn verbose
        self.verbose_check = ctk.CTkCheckBox(
            format_options,
            text="Chi tiết (bao gồm thông tin thêm)",
            variable=self.verbose, # Liên kết với biến verbose
            font=self.normal_font, # Sử dụng font chữ thường
            fg_color=self.accent_color, # Màu nền khi chọn
            checkbox_width=20, # Chiều rộng checkbox
            checkbox_height=20 # Chiều cao checkbox
        )
        self.verbose_check.pack(side=tk.RIGHT) # Đặt checkbox verbose bên phải

        # Run button section - Phần nút chạy
        run_frame = ctk.CTkFrame(config_scroll, fg_color="transparent") # Tạo frame trong suốt cho nút chạy
        run_frame.pack(fill=tk.X, padx=10, pady=(10, 20)) # Đặt run_frame vào scrollable frame, mở rộng và có padding

        self.run_button = ctk.CTkButton(
            run_frame,
            text="Tạo Tài Liệu",
            command=self.run_documentation, # Liên kết với hàm run_documentation
            font=ctk.CTkFont(family=self.font_family, size=15, weight="bold"), # Sử dụng font chữ đậm
            fg_color=self.success_color, # Màu nền nút (xanh lá cây)
            hover_color="#218838",  # Darker green - Xanh lá cây đậm hơn khi hover
            corner_radius=8, # Độ cong góc
            height=40 # Chiều cao nút
        )
        self.run_button.pack(fill=tk.X, padx=15) # Đặt nút chạy vào run_frame, mở rộng và có padding

    def create_advanced_tab(self):
        """Tạo nội dung cho tab "Nâng cao"."""
        # Create a scrollable frame for advanced settings - Tạo scrollable frame cho cài đặt nâng cao
        advanced_scroll = ctk.CTkScrollableFrame(self.tab_advanced) # Tạo scrollable frame cho tab nâng cao
        advanced_scroll.grid(row=0, column=0, sticky="nsew", padx=5, pady=5) # Đặt scrollable frame vào tab, mở rộng và có padding
        advanced_scroll.columnconfigure(0, weight=1) # Cấu hình cột 0 mở rộng theo chiều ngang

        # Excluded subdirectories - Thư mục con loại trừ
        excluded_dirs_section = ctk.CTkFrame(advanced_scroll, corner_radius=10) # Tạo frame cho phần thư mục con loại trừ
        excluded_dirs_section.pack(fill=tk.X, padx=10, pady=10) # Đặt frame phần thư mục con loại trừ vào scrollable frame, mở rộng và có padding

        # Section title - Tiêu đề phần
        excl_dirs_label = ctk.CTkLabel(
            excluded_dirs_section,
            text="Thư mục con loại trừ",
            font=self.header_font, # Sử dụng font chữ header
            anchor="w" # Căn chỉnh văn bản sang trái
        )
        excl_dirs_label.pack(fill=tk.X, padx=15, pady=(15, 5)) # Đặt excl_dirs_label vào frame phần thư mục con loại trừ, mở rộng và có padding

        # Description - Mô tả
        excl_dirs_desc = ctk.CTkLabel(
            excluded_dirs_section,
            text="Nhập các thư mục con (cách nhau bởi dấu phẩy) để loại trừ khỏi tài liệu.",
            font=self.normal_font, # Sử dụng font chữ thường
            anchor="w", # Căn chỉnh văn bản sang trái
            justify="left" # Căn chỉnh văn bản sang trái (đa dòng)
        )
        excl_dirs_desc.pack(fill=tk.X, padx=15, pady=(0, 10)) # Đặt excl_dirs_desc vào frame phần thư mục con loại trừ, mở rộng và có padding

        # Entry for excluded subdirectories - Entry cho thư mục con loại trừ
        self.excluded_subdirs_entry = ctk.CTkEntry(
            excluded_dirs_section,
            font=self.normal_font, # Sử dụng font chữ thường
            corner_radius=8, # Độ cong góc
            height=35 # Chiều cao entry
        )
        self.excluded_subdirs_entry.insert(0, ", ".join(self.excluded_subdirs)) # Điền thư mục con loại trừ mặc định vào entry
        self.excluded_subdirs_entry.pack(fill=tk.X, padx=15, pady=(5, 15)) # Đặt excluded_subdirs_entry vào frame phần thư mục con loại trừ, mở rộng và có padding

        # Excluded files - Tệp loại trừ
        excluded_files_section = ctk.CTkFrame(advanced_scroll, corner_radius=10) # Tạo frame cho phần tệp loại trừ
        excluded_files_section.pack(fill=tk.X, padx=10, pady=(0, 10)) # Đặt frame phần tệp loại trừ vào scrollable frame, mở rộng và có padding

        # Section title - Tiêu đề phần
        excl_files_label = ctk.CTkLabel(
            excluded_files_section,
            text="Tệp loại trừ",
            font=self.header_font, # Sử dụng font chữ header
            anchor="w" # Căn chỉnh văn bản sang trái
        )
        excl_files_label.pack(fill=tk.X, padx=15, pady=(15, 5)) # Đặt excl_files_label vào frame phần tệp loại trừ, mở rộng và có padding

        # Description - Mô tả
        excl_files_desc = ctk.CTkLabel(
            excluded_files_section,
            text="Nhập các phần mở rộng tệp hoặc tên tệp (cách nhau bởi dấu phẩy) để loại trừ.",
            font=self.normal_font, # Sử dụng font chữ thường
            anchor="w", # Căn chỉnh văn bản sang trái
            justify="left" # Căn chỉnh văn bản sang trái (đa dòng)
        )
        excl_files_desc.pack(fill=tk.X, padx=15, pady=(0, 10)) # Đặt excl_files_desc vào frame phần tệp loại trừ, mở rộng và có padding

        # Entry for excluded files - Entry cho tệp loại trừ
        self.excluded_files_entry = ctk.CTkEntry(
            excluded_files_section,
            font=self.normal_font, # Sử dụng font chữ thường
            corner_radius=8, # Độ cong góc
            height=35 # Chiều cao entry
        )
        self.excluded_files_entry.insert(0, ", ".join(self.excluded_files)) # Điền tệp loại trừ mặc định vào entry
        self.excluded_files_entry.pack(fill=tk.X, padx=15, pady=(5, 15)) # Đặt excluded_files_entry vào frame phần tệp loại trừ, mở rộng và có padding

        # Save settings button - Nút lưu cài đặt
        save_button = ctk.CTkButton(
            advanced_scroll,
            text="Lưu Cài Đặt",
            command=self.save_advanced_settings, # Liên kết với hàm save_advanced_settings
            font=self.normal_font, # Sử dụng font chữ thường
            fg_color="#6C757D",  # Gray color - Màu xám
            hover_color="#5A6268", # Xám đậm hơn khi hover
            corner_radius=8, # Độ cong góc
            height=35 # Chiều cao nút
        )
        save_button.pack(fill=tk.X, padx=15, pady=(15, 20)) # Đặt nút lưu cài đặt vào scrollable frame, mở rộng và có padding

    def create_output_tab(self):
        """Tạo nội dung cho tab "Kết quả"."""
        # Use the custom scrolled text - Sử dụng custom scrolled text
        self.output_text = CustomScrolledText(self.tab_output, wrap=tk.WORD, font=self.normal_font) # Tạo đối tượng CustomScrolledText
        self.output_text.grid(row=0, column=0, sticky="nsew", padx=10, pady=10) # Đặt output_text vào tab, mở rộng và có padding

        # Copy and clear buttons frame - Frame nút sao chép và xóa
        buttons_frame = ctk.CTkFrame(self.tab_output, fg_color="transparent") # Tạo frame trong suốt chứa các nút
        buttons_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=(0, 10)) # Đặt buttons_frame vào tab, mở rộng theo chiều ngang và có padding

        # Copy to clipboard button - Nút sao chép vào clipboard
        self.copy_button = ctk.CTkButton(
            buttons_frame,
            text="Sao chép",
            command=self.copy_to_clipboard, # Liên kết với hàm copy_to_clipboard
            font=self.normal_font, # Sử dụng font chữ thường
            fg_color="#4CAF50",  # Green - Xanh lá cây
            hover_color="#388E3C", # Xanh lá cây đậm hơn khi hover
            corner_radius=8, # Độ cong góc
            width=120, # Chiều rộng nút
            height=30 # Chiều cao nút
        )
        self.copy_button.pack(side=tk.LEFT, padx=(0, 10)) # Đặt nút sao chép bên trái, có padding bên phải

        # Clear output button - Nút xóa đầu ra
        self.clear_button = ctk.CTkButton(
            buttons_frame,
            text="Xóa",
            command=self.clear_output, # Liên kết với hàm clear_output
            font=self.normal_font, # Sử dụng font chữ thường
            fg_color="#F44336",  # Red - Đỏ
            hover_color="#D32F2F", # Đỏ đậm hơn khi hover
            corner_radius=8, # Độ cong góc
            width=120, # Chiều rộng nút
            height=30 # Chiều cao nút
        )
        self.clear_button.pack(side=tk.LEFT) # Đặt nút xóa đầu ra bên trái

        # Open output folder button - Nút mở thư mục đầu ra
        self.open_folder_button = ctk.CTkButton(
            buttons_frame,
            text="Mở Thư Mục Đầu Ra",
            command=self.open_output_folder, # Liên kết với hàm open_output_folder
            font=self.normal_font, # Sử dụng font chữ thường
            fg_color=self.primary_color, # Màu nền nút
            hover_color=self.hover_color, # Màu nền khi hover
            corner_radius=8, # Độ cong góc
            height=30 # Chiều cao nút
        )
        self.open_folder_button.pack(side=tk.RIGHT, padx=(10, 0)) # Đặt nút mở thư mục đầu ra bên phải, có padding bên trái

    def create_status_bar(self):
        """Tạo status bar ở dưới cùng của ứng dụng."""
        status_bar = ctk.CTkFrame(self.root, height=30, fg_color="transparent") # Tạo frame trong suốt cho status bar
        status_bar.pack(fill=tk.X, side=tk.BOTTOM, padx=15, pady=(5, 10)) # Đặt status_bar vào cửa sổ gốc, mở rộng theo chiều ngang và có padding

        self.status_label = ctk.CTkLabel(
            status_bar,
            textvariable=self.status_var, # Liên kết với biến status_var
            font=self.small_font # Sử dụng font chữ nhỏ
        )
        self.status_label.pack(side=tk.LEFT) # Đặt status_label bên trái

        self.progress_bar = ctk.CTkProgressBar(
            status_bar,
            variable=self.progress_var, # Liên kết với biến progress_var
            height=10, # Chiều cao thanh tiến trình
            corner_radius=5 # Độ cong góc
        )
        self.progress_bar.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=(10, 0)) # Đặt progress_bar bên phải, mở rộng và có padding bên trái

    def add_project_directory(self):
        """Mở hộp thoại chọn thư mục và thêm thư mục dự án."""
        directory = filedialog.askdirectory(title="Chọn Thư Mục Dự Án") # Mở hộp thoại chọn thư mục
        if directory: # Kiểm tra nếu người dùng đã chọn thư mục
            directory = os.path.abspath(directory) # Lấy đường dẫn tuyệt đối
            if directory not in self.project_dirs: # Kiểm tra nếu thư mục chưa có trong danh sách
                self.project_dirs.append(directory) # Thêm thư mục vào danh sách
                self.project_dir_list.insert(tk.END, directory) # Thêm thư mục vào listbox
            else:
                messagebox.showinfo("Thư mục đã tồn tại", "Thư mục bạn chọn đã có trong danh sách.") # Hiển thị thông báo nếu thư mục đã tồn tại

    def remove_project_directory(self):
        """Xóa thư mục dự án đã chọn khỏi danh sách."""
        selected_indices = self.project_dir_list.curselection() # Lấy chỉ số của các mục đã chọn trong listbox
        if selected_indices: # Kiểm tra nếu có mục nào được chọn
            # Reverse to avoid index issues after deletion - Đảo ngược để tránh lỗi chỉ mục sau khi xóa
            for i in reversed(selected_indices): # Lặp qua các chỉ số đã chọn theo thứ tự ngược
                self.project_dir_list.delete(i) # Xóa mục khỏi listbox
                self.project_dirs.pop(i) # Xóa thư mục khỏi danh sách
        else:
            messagebox.showinfo("Không có thư mục nào được chọn", "Vui lòng chọn ít nhất một thư mục để xóa.") # Hiển thị thông báo nếu không có thư mục nào được chọn

    def browse_output_directory(self):
        """Mở hộp thoại chọn thư mục và đặt thư mục đầu ra."""
        directory = filedialog.askdirectory(title="Chọn Thư Mục Đầu Ra") # Mở hộp thoại chọn thư mục
        if directory: # Kiểm tra nếu người dùng đã chọn thư mục
            self.output_dir = os.path.abspath(directory) # Lấy đường dẫn tuyệt đối
            self.output_dir_entry.delete(0, tk.END) # Xóa nội dung hiện tại của entry thư mục đầu ra
            self.output_dir_entry.insert(0, self.output_dir) # Điền đường dẫn thư mục đầu ra mới vào entry

    def save_advanced_settings(self):
        """Lưu cài đặt nâng cao (thư mục và tệp loại trừ)."""
        self.excluded_subdirs = [s.strip() for s in self.excluded_subdirs_entry.get().split(",") if s.strip()] # Lấy và xử lý thư mục con loại trừ từ entry
        self.excluded_files = [f.strip() for f in self.excluded_files_entry.get().split(",") if f.strip()] # Lấy và xử lý tệp loại trừ từ entry
        messagebox.showinfo("Đã Lưu", "Cài đặt nâng cao đã được lưu.") # Hiển thị thông báo đã lưu

    def run_documentation(self):
        """Bắt đầu quá trình tạo tài liệu dự án."""
        if not self.project_dirs: # Kiểm tra nếu không có thư mục dự án nào được chọn
            messagebox.showerror("Lỗi", "Vui lòng chọn ít nhất một thư mục dự án.") # Hiển thị thông báo lỗi
            return

        self.progress_var.set(0) # Đặt thanh tiến trình về 0
        self.status_var.set("Đang xử lý...") # Đặt trạng thái thành "Đang xử lý..."
        self.output_text.text.delete("1.0", tk.END)  # Clear previous output - Xóa đầu ra trước đó

        # Disable buttons - Vô hiệu hóa các nút
        self.run_button.configure(state="disabled") # Vô hiệu hóa nút chạy
        self.add_dir_btn.configure(state="disabled") # Vô hiệu hóa nút thêm thư mục
        self.remove_dir_btn.configure(state="disabled") # Vô hiệu hóa nút xóa thư mục
        self.browse_btn.configure(state="disabled") # Vô hiệu hóa nút duyệt thư mục

        # Get options from GUI - Lấy tùy chọn từ GUI
        output_dir = self.output_dir_entry.get() # Lấy thư mục đầu ra từ entry
        base_filename = self.base_filename_entry.get() # Lấy tên tệp cơ sở từ entry
        output_format = self.output_format.get() # Lấy định dạng đầu ra từ radio button
        verbose = self.verbose.get() # Lấy giá trị verbose từ checkbox


        def run_doc_thread():
            """Hàm chạy tạo tài liệu trong một thread riêng biệt."""
            try:
                (message, execution_time, num_files, num_folders,
                errors, skipped_files, skipped_folders, output_paths) = tao_tai_lieu_du_an( # Gọi hàm tạo_tai_lieu_du_an
                    self.project_dirs,
                    self.excluded_subdirs,
                    self.excluded_files,
                    base_filename,
                    output_dir,
                    verbose,
                    output_format
                )

                formatted_output = format_output_for_tkinter( # Định dạng đầu ra cho Tkinter
                    message, execution_time, num_files, num_folders,
                    errors, skipped_files, skipped_folders, output_format
                )

                # Update GUI from the thread using after() - Cập nhật GUI từ thread sử dụng after()
                self.root.after(0, self.update_output, formatted_output) # Cập nhật output text
                self.root.after(0, self.update_status, f"Hoàn tất! Tài liệu đã được tạo tại: {output_paths}") # Cập nhật status label
                self.root.after(0, self.progress_var.set, 100)  # Set progress to 100% - Đặt tiến trình về 100%
                self.root.after(0, lambda: self.open_folder_button.configure(state="normal")) # Kích hoạt lại nút mở thư mục đầu ra

            except Exception as e: # Bắt lỗi nếu có lỗi xảy ra
                self.root.after(0, self.update_output, f"Đã xảy ra lỗi: {str(e)}") # Hiển thị thông báo lỗi
                self.root.after(0, self.update_status, "Lỗi") # Cập nhật status label thành "Lỗi"
                self.root.after(0, self.progress_var.set, 0) # Đặt tiến trình về 0
            finally: # Khối finally luôn được thực hiện, kể cả khi có lỗi hay không
                self.root.after(0, lambda: self.run_button.configure(state="normal")) # Kích hoạt lại nút chạy
                self.root.after(0, lambda: self.add_dir_btn.configure(state="normal")) # Kích hoạt lại nút thêm thư mục
                self.root.after(0, lambda: self.remove_dir_btn.configure(state="normal")) # Kích hoạt lại nút xóa thư mục
                self.root.after(0, lambda: self.browse_btn.configure(state="normal")) # Kích hoạt lại nút duyệt thư mục


        # Run the documentation generation in a separate thread - Chạy quá trình tạo tài liệu trong một thread riêng biệt
        Thread(target=run_doc_thread).start() # Khởi tạo và bắt đầu thread

    def update_output(self, text):
        """Cập nhật output text box với văn bản mới."""
        self.output_text.text.insert(tk.END, text + "\n") # Thêm văn bản vào cuối output text box
        self.output_text.text.see(tk.END)  # Scroll to the end - Cuộn xuống cuối để hiển thị văn bản mới nhất

    def update_status(self, message):
         """Cập nhật status label với thông báo mới."""
         self.status_var.set(message) # Đặt văn bản mới cho status label

    def copy_to_clipboard(self):
        """Sao chép nội dung output text box vào clipboard."""
        try:
            self.root.clipboard_clear() # Xóa clipboard hiện tại
            self.root.clipboard_append(self.output_text.text.get("1.0", tk.END)) # Thêm nội dung output text box vào clipboard
            messagebox.showinfo("Đã sao chép", "Nội dung đã được sao chép vào clipboard.") # Hiển thị thông báo đã sao chép
        except Exception as e: # Bắt lỗi nếu có lỗi xảy ra
            messagebox.showerror("Lỗi", f"Không thể sao chép nội dung: {str(e)}") # Hiển thị thông báo lỗi

    def clear_output(self):
        """Xóa nội dung output text box."""
        self.output_text.text.delete("1.0", tk.END) # Xóa toàn bộ nội dung output text box

    def open_output_folder(self):
       """Mở thư mục đầu ra bằng trình quản lý tệp của hệ điều hành."""
       output_path = self.output_dir_entry.get() # Lấy đường dẫn thư mục đầu ra từ entry

       if output_path and os.path.isdir(output_path): # Kiểm tra nếu đường dẫn hợp lệ và là thư mục
           try:
               if os.name == 'nt':  # Windows - Hệ điều hành Windows
                   subprocess.Popen(['explorer', output_path]) # Mở thư mục bằng Explorer trên Windows
               elif os.name == 'posix':  # macOS or Linux - macOS hoặc Linux
                   subprocess.Popen(['open', output_path])  # macOS - Mở thư mục bằng Open trên macOS (có thể hoạt động trên Linux)
               else:
                   messagebox.showwarning("Không được hỗ trợ", "Hệ điều hành của bạn không được hỗ trợ để mở thư mục.") # Hiển thị cảnh báo nếu hệ điều hành không được hỗ trợ
           except Exception as e: # Bắt lỗi nếu có lỗi xảy ra
              messagebox.showerror("Lỗi", f"Không thể mở thư mục: {str(e)}") # Hiển thị thông báo lỗi
       else:
         messagebox.showerror("Lỗi", "Đường dẫn thư mục đầu ra không hợp lệ.") # Hiển thị thông báo lỗi nếu đường dẫn không hợp lệ

if __name__ == "__main__":
    root = ctk.CTk() # Tạo cửa sổ gốc CustomTkinter
    app = ProjectDocApp(root) # Tạo đối tượng ứng dụng ProjectDocApp
    root.mainloop() # Bắt đầu vòng lặp chính của giao diện người dùng