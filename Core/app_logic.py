import os
import time
from .constants import SUPPORTED_FILE_EXTENSIONS 
from .translations import Translations 

# Ham chinh tao TLDA
def tao_tai_lieu_du_an(duong_dan_thu_muc, thu_muc_con_loai_tru=None, tep_loai_tru=None, ten_tep_co_so="tai_lieu_du_an", thu_muc_dau_ra=".", verbose=False, output_format="txt"):
    # KTr dau vao
    if not isinstance(duong_dan_thu_muc, (list, tuple)):
        raise TypeError(Translations.get("applogic_err_path_type")) 
    if not duong_dan_thu_muc:
        raise ValueError(Translations.get("applogic_err_path_empty")) 
    if output_format not in ("txt", "markdown"):
        raise ValueError(Translations.get("applogic_err_output_format")) 

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
    all_output_paths = []

    for duong_dan in duong_dan_thu_muc: 
        if not os.path.isdir(duong_dan):
            all_errors[duong_dan] = Translations.get("applogic_folder_not_exist_val") # Dich
            continue

        ten_thu_muc_du_an = os.path.basename(duong_dan)
        thu_muc_dau_ra_du_an = os.path.join(thu_muc_dau_ra, ten_thu_muc_du_an)
        os.makedirs(thu_muc_dau_ra_du_an, exist_ok=True)

        file_extension = ".txt" if output_format == "txt" else ".md"
        ten_file = os.path.join(thu_muc_dau_ra_du_an, f"{ten_tep_co_so}{file_extension}")

        count = 1
        while os.path.exists(ten_file): 
            ten_file = os.path.join(thu_muc_dau_ra_du_an, f"{ten_tep_co_so} {count}{file_extension}")
            count += 1
        all_output_paths.append(os.path.abspath(ten_file))

        num_files_processed = 0
        num_folders_processed = 0
        errors = {}
        skipped_files_list = []
        skipped_folders_list = []

        with open(ten_file, "w", encoding="utf-8") as outfile: 
            if output_format == "markdown":
                outfile.write(Translations.get("applogic_project_title_md", project_name=ten_thu_muc_du_an) + "\n\n") # Dich
            else:
                outfile.write(Translations.get("applogic_project_title_txt", project_name=ten_thu_muc_du_an) + "\n\n") # Dich

            def viet_cau_truc_thu_muc(thu_muc_goc, indent_level=0): 
                nonlocal num_folders_processed
                thut_le = ("│   " * indent_level + "├── ") if output_format == "txt" else ("    " * indent_level + "- ")

                try:
                    entries = sorted(os.scandir(thu_muc_goc), key=lambda e: (not e.is_dir(), e.name.lower())) 
                    for entry in entries:
                        if entry.is_dir(follow_symlinks=False):
                            if entry.name in thu_muc_con_loai_tru_set:
                                outfile.write(thut_le + f"{entry.name}{Translations.get('applogic_excluded_suffix')}\n") # Dich
                                skipped_folders_list.append(os.path.relpath(entry.path, duong_dan))
                                continue
                            outfile.write(thut_le + f"{entry.name}/\n")
                            num_folders_processed += 1
                            viet_cau_truc_thu_muc(entry.path, indent_level + 1)
                        elif entry.is_file(follow_symlinks=False):
                            if entry.name.endswith(tuple(tep_loai_tru)) or entry.name in tep_loai_tru_set:
                                skipped_files_list.append(os.path.relpath(entry.path, duong_dan))
                                continue
                            outfile.write(thut_le + f"{entry.name}\n")
                except FileNotFoundError:
                    outfile.write(thut_le + f"{os.path.basename(thu_muc_goc)}{Translations.get('applogic_dir_not_found_suffix')}\n") # Dich
                    errors[os.path.basename(thu_muc_goc)] = Translations.get("applogic_folder_not_exist_val") # Dich
                except PermissionError:
                    outfile.write(thut_le + f"{os.path.basename(thu_muc_goc)}{Translations.get('applogic_dir_permission_suffix')}\n") # Dich
                    errors[os.path.basename(thu_muc_goc)] = Translations.get("applogic_permission_denied_val") # Dich
                except OSError as e:
                    outfile.write(thut_le + f"{os.path.basename(thu_muc_goc)}{Translations.get('applogic_dir_os_error_suffix', error=e)}\n") # Dich
                    errors[os.path.basename(thu_muc_goc)] = Translations.get("applogic_os_error_val", error=e) # Dich

            def viet_noi_dung_tep(thu_muc_goc): 
                nonlocal num_files_processed
                try:
                    entries = sorted(os.scandir(thu_muc_goc), key=lambda e: (not e.is_dir(), e.name.lower())) 
                    for entry in entries:
                        if entry.is_dir(follow_symlinks=False):
                            if entry.name in thu_muc_con_loai_tru_set:
                                continue
                            viet_noi_dung_tep(entry.path)
                        elif entry.is_file(follow_symlinks=False):
                            if entry.name.endswith(tuple(tep_loai_tru)) or entry.name in tep_loai_tru_set:
                                if os.path.relpath(entry.path, duong_dan) not in skipped_files_list:
                                     skipped_files_list.append(os.path.relpath(entry.path, duong_dan))
                                continue
                            if entry.name.endswith(SUPPORTED_FILE_EXTENSIONS):
                                outfile.write(f"\n**{os.path.relpath(entry.path, duong_dan)}**\n\n") 
                                outfile.write("```")
                                lang = ""
                                if entry.name.endswith('.py'): lang = "python"
                                outfile.write(f"{lang}\n")

                                try:
                                    with open(entry.path, "r", encoding="utf-8", errors="surrogateescape") as infile: 
                                        outfile.write(infile.read())
                                    num_files_processed += 1
                                except UnicodeDecodeError: 
                                    try:
                                        with open(entry.path, "r", encoding="latin-1") as infile:
                                            outfile.write(infile.read())
                                        num_files_processed += 1
                                        outfile.write(Translations.get("applogic_encoding_warning_note")) # Dich
                                    except Exception as e_latin:
                                        outfile.write(Translations.get("applogic_cannot_read_file_note_generic", path=entry.path, error=e_latin) + "\n") # Dich
                                        errors[entry.path] = str(e_latin)
                                except FileNotFoundError:
                                    outfile.write(Translations.get("applogic_file_not_found_note", path=entry.path) + "\n") # Dich
                                    errors[entry.path] = Translations.get("applogic_file_not_found_val") # Dich
                                except PermissionError:
                                    outfile.write(Translations.get("applogic_permission_denied_note", path=entry.path) + "\n") # Dich
                                    errors[entry.path] = Translations.get("applogic_permission_denied_val") # Dich
                                except OSError as e_os:
                                    outfile.write(Translations.get("applogic_os_error_reading_file_note", path=entry.path, error=e_os) + "\n") # Dich
                                    errors[entry.path] = Translations.get("applogic_os_error_val", error=e_os) # Dich
                                outfile.write("\n```\n\n")
                except FileNotFoundError:
                    errors[thu_muc_goc] = Translations.get("applogic_dir_not_found_content_val") # Dich
                except PermissionError:
                    errors[thu_muc_goc] = Translations.get("applogic_dir_permission_content_val") # Dich
                except OSError as e:
                    errors[thu_muc_goc] = Translations.get("applogic_os_error_content_val", error=e) # Dich

            outfile.write(f"{os.path.basename(duong_dan)}/\n") 
            viet_cau_truc_thu_muc(duong_dan)
            outfile.write("\n--- START CONTENT ---\n") 
            viet_noi_dung_tep(duong_dan)
            outfile.write("\n--- END CONTENT ---\n\n")

        total_files_processed += num_files_processed
        total_folders_processed += num_folders_processed
        all_errors.update(errors)
        all_skipped_files.extend(list(set(skipped_files_list)))
        all_skipped_folders.extend(list(set(skipped_folders_list)))

    end_time = time.time()
    execution_time = end_time - start_time
    message = Translations.get("applogic_docs_created_in_msg", output_dir=thu_muc_dau_ra) # Dich
    if verbose:
        message += Translations.get("applogic_verbose_processed_msg", files=total_files_processed, folders=total_folders_processed) # Dich

    output_paths_str = ", ".join(all_output_paths)
    return (message, execution_time, total_files_processed, total_folders_processed,
            all_errors, all_skipped_files, all_skipped_folders, output_paths_str)
