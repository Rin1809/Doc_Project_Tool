# Tiện ích cho GUI

def format_output_for_tkinter(message, execution_time=None, num_files=0, num_folders=0, errors=None, skipped_files=None, skipped_folders=None, output_format="txt"):
    output_text = ""
    if execution_time is not None:
        if output_format == "txt":
            output_text += f"✨ Hoàn tất ({execution_time:.2f}s) ✨\n" 
        elif output_format == "markdown":
             output_text += f"## ✨ Hoàn tất ({execution_time:.2f}s) ✨\n" 
    else: # Khong can thiet nua vi se cap nhat status bar
        pass

    if message:
        if output_format == "txt":
            output_text += f"✅ {message}\n" 
        elif output_format == "markdown":
            output_text += f"✅ {message}\n\n"

    if num_files > 0 or num_folders > 0:
        if output_format == "txt":
            output_text += f"   📁 Thư mục đã quét: {num_folders}\n" 
            output_text += f"   📄 Tệp đã quét: {num_files}\n" 
        elif output_format == "markdown":
            output_text += f"- 📁 Thư mục đã quét: {num_folders}\n" 
            output_text += f"- 📄 Tệp đã quét: {num_files}\n" 

    if skipped_folders:
        if output_format == "txt":
            output_text += "   📂 Thư mục bỏ qua:\n" 
        elif output_format == "markdown":
            output_text += "- 📂 Thư mục bỏ qua:\n" 
        for folder in skipped_folders:
            if output_format == "txt":
                output_text += f"      - {folder}\n" 
            elif output_format == "markdown":
                output_text += f"    - {folder}\n" 

    if skipped_files:
        if output_format == "txt":
            output_text += "   📄 Tệp bỏ qua:\n" 
        elif output_format == "markdown":
            output_text += "- 📄 Tệp bỏ qua:\n"
        for file in skipped_files:
            if output_format == "txt":
                output_text += f"      - {file}\n" 
            elif output_format == "markdown":
                output_text += f"    - {file}\n"

    if errors:
        if output_format == "txt":
            output_text += "❌ Lỗi:\n" 
        elif output_format == "markdown":
            output_text += "- ❌ Lỗi:\n" 
        for error_item, error_msg in errors.items():
            if "No such file or directory" in error_msg or "không tồn tại" in error_msg:
                output_text += f"    - {error_item}: Không tìm thấy tệp/TM\n" 
            elif "Permission denied" in error_msg or "Lỗi truy cập" in error_msg:
                output_text += f"    - {error_item}: Lỗi truy cập\n" 
            else:
                output_text += f"    - {error_item}: {error_msg}\n" 
    return output_text