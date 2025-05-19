# Tiện ích cho GUI

# Hàm định dạng đầu ra cho Tkinter
def format_output_for_tkinter(message, execution_time=None, num_files=0, num_folders=0, errors=None, skipped_files=None, skipped_folders=None, output_format="txt"):
    output_text = ""
    if execution_time is not None:
        if output_format == "txt":
            output_text += f"✨ Hoàn tất ({execution_time:.2f}s) ✨\n" # TB hoàn thành (txt)
        elif output_format == "markdown":
             output_text += f"## ✨ Hoàn tất ({execution_time:.2f}s) ✨\n" # TB hoàn thành (md)
    else:
        if output_format == "txt":
            output_text += "[Xử lý file]\n" # TB đang xử lý (txt)
        elif output_format == "markdown":
            output_text += "### [Xử lý file]\n" # TB đang xử lý (md)

    if message:
        if output_format == "txt":
            output_text += f"✅ {message}\n" # TB thành công (txt)
        elif output_format == "markdown":
            output_text += f"✅ {message}\n\n" # TB thành công (md)

    if num_files > 0 or num_folders > 0:
        if output_format == "txt":
            output_text += f"   📁 Thư mục đã quét: {num_folders}\n" # Số TM quét (txt)
            output_text += f"   📄 Tệp đã quét: {num_files}\n" # Số tệp quét (txt)
        elif output_format == "markdown":
            output_text += f"- 📁 Thư mục đã quét: {num_folders}\n" # Số TM quét (md)
            output_text += f"- 📄 Tệp đã quét: {num_files}\n" # Số tệp quét (md)

    if skipped_folders:
        if output_format == "txt":
            output_text += "   📂 Thư mục bỏ qua:\n" # DS TM bỏ qua (txt)
        elif output_format == "markdown":
            output_text += "- 📂 Thư mục bỏ qua:\n" # DS TM bỏ qua (md)
        for folder in skipped_folders:
            if output_format == "txt":
                output_text += f"      - {folder}\n" # Tên TM bỏ qua (txt)
            elif output_format == "markdown":
                output_text += f"    - {folder}\n" # Tên TM bỏ qua (md)

    if skipped_files:
        if output_format == "txt":
            output_text += "   📄 Tệp bỏ qua:\n" # DS tệp bỏ qua (txt)
        elif output_format == "markdown":
            output_text += "- 📄 Tệp bỏ qua:\n" # DS tệp bỏ qua (md)
        for file in skipped_files:
            if output_format == "txt":
                output_text += f"      - {file}\n" # Tên tệp bỏ qua (txt)
            elif output_format == "markdown":
                output_text += f"    - {file}\n" # Tên tệp bỏ qua (md)

    if errors:
        if output_format == "txt":
            output_text += "❌ Lỗi:\n" # TB lỗi (txt)
        elif output_format == "markdown":
            output_text += "- ❌ Lỗi:\n" # TB lỗi (md)
        for error_item, error_msg in errors.items():
            if "No such file or directory" in error_msg:
                output_text += f"    - {error_item}: Không tìm thấy tệp/TM\n" # Lỗi ko tìm thấy (txt)
            elif "Permission denied" in error_msg:
                output_text += f"    - {error_item}: Lỗi truy cập\n" # Lỗi quyền (txt)
            else:
                output_text += f"    - {error_item}: {error_msg}\n" # Lỗi khác (txt)
    return output_text