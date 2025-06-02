
# Tiện ích cho GUI
from .translations import Translations 

def format_output_for_tkinter(message, execution_time=None, num_files=0, num_folders=0, errors=None, skipped_files=None, skipped_folders=None, output_format="txt"):
    output_text = ""
    if execution_time is not None:
        complete_msg = Translations.get("output_complete_status", time=execution_time)
        if output_format == "txt":
            output_text += f"{complete_msg}\n" 
        elif output_format == "markdown":
             output_text += f"## {complete_msg}\n" 
    else: 
        pass

    if message:
        msg_prefix = Translations.get("output_message_prefix", message=message)
        if output_format == "txt":
            output_text += f"{msg_prefix}\n" 
        elif output_format == "markdown":
            output_text += f"{msg_prefix}\n\n"

    if num_files > 0 or num_folders > 0:
        folders_scanned_msg = Translations.get("output_folders_scanned", num_folders=num_folders)
        files_scanned_msg = Translations.get("output_files_scanned", num_files=num_files)
        if output_format == "txt":
            output_text += f"   {folders_scanned_msg}\n" 
            output_text += f"   {files_scanned_msg}\n" 
        elif output_format == "markdown":
            output_text += f"- {folders_scanned_msg}\n" 
            output_text += f"- {files_scanned_msg}\n" 

    if skipped_folders:
        skipped_folders_header = Translations.get("output_skipped_folders_header")
        if output_format == "txt":
            output_text += f"   {skipped_folders_header}\n" 
        elif output_format == "markdown":
            output_text += f"- {skipped_folders_header}\n" 
        for folder in skipped_folders:
            if output_format == "txt":
                output_text += f"      - {folder}\n" 
            elif output_format == "markdown":
                output_text += f"    - {folder}\n" 

    if skipped_files:
        skipped_files_header = Translations.get("output_skipped_files_header")
        if output_format == "txt":
            output_text += f"   {skipped_files_header}\n" 
        elif output_format == "markdown":
            output_text += f"- {skipped_files_header}\n"
        for file in skipped_files:
            if output_format == "txt":
                output_text += f"      - {file}\n" 
            elif output_format == "markdown":
                output_text += f"    - {file}\n"

    if errors:
        errors_header = Translations.get("output_errors_header")
        if output_format == "txt":
            output_text += f"{errors_header}\n" 
        elif output_format == "markdown":
            output_text += f"- {errors_header}\n" 
        for error_item, error_msg in errors.items():
            # Su dung key tu app_logic de dich loi (vi error_msg la tieng Viet MD)
            if error_msg == Translations.get("applogic_folder_not_exist_val", lang=Translations.LANG_VI) or \
               error_msg == Translations.get("applogic_file_not_found_val", lang=Translations.LANG_VI):
                output_text += f"    - {Translations.get('output_error_not_found', item=error_item)}\n"
            elif error_msg == Translations.get("applogic_permission_denied_val", lang=Translations.LANG_VI):
                output_text += f"    - {Translations.get('output_error_permission', item=error_item)}\n"
            else:
                # Neu loi khac, co the hien thi truc tiep error_msg (da co san tieng Viet)
                # Hoac co mot mapping tong quat hon
                actual_error_msg = error_msg # MD la tieng Viet
                if Translations.current_lang != Translations.LANG_VI:
                    # Co gang tim key goc neu error_msg la 1 value trong translations
                    found_key = None
                    if Translations.get("applogic_os_error_val", error="X", lang=Translations.LANG_VI).replace("X","") in error_msg:
                        # Trich xuat phan loi thuc te
                        actual_err_part = error_msg.replace(Translations.get("applogic_os_error_val", error="", lang=Translations.LANG_VI),"").strip()
                        actual_error_msg = Translations.get("applogic_os_error_val", error=actual_err_part)
                    # Them cac case khac neu can
                
                output_text += f"    - {Translations.get('output_error_generic_item',item=error_item, msg=actual_error_msg)}\n"
    return output_text