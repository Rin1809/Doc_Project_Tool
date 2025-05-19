import os
import time
from .constants import SUPPORTED_FILE_EXTENSIONS # Import hang

# Ham chinh tao TLDA
def tao_tai_lieu_du_an(duong_dan_thu_muc, thu_muc_con_loai_tru=None, tep_loai_tru=None, ten_tep_co_so="tai_lieu_du_an", thu_muc_dau_ra=".", verbose=False, output_format="txt"):
    # Tao doc tu 1+ TM nguon.
    # Args:
    #   duong_dan_thu_muc (list/tuple): DS duong dan TMDA.
    #   thu_muc_con_loai_tru (list, opt): DS ten TM con loai tru. MD None.
    #   tep_loai_tru (list, opt): DS duoi tep/ten tep loai tru. MD None.
    # Returns:
    #   tuple: (thong bao, t_gian_thuc_thi, so_tep_xu_ly, so_TM_xu_ly, loi, tep_bo_qua, TM_bo_qua, duong_dan_tep_dau_ra)
    # Raises:
    #   TypeError, ValueError

    # KTr dau vao
    if not isinstance(duong_dan_thu_muc, (list, tuple)):
        raise TypeError("duong_dan_thu_muc phai la list/tuple") # Loi kieu
    if not duong_dan_thu_muc:
        raise ValueError("duong_dan_thu_muc khong rong") # Loi DS rong
    if output_format not in ("txt", "markdown"):
        raise ValueError("output_format phai la 'txt'/'markdown'") # Loi fmt

    start_time = time.time() # Ghi tg start

    if thu_muc_con_loai_tru is None:
        thu_muc_con_loai_tru = [] # Khoi tao DS TM loai tru
    if tep_loai_tru is None:
        tep_loai_tru = [] # Khoi tao DS tep loai tru

    # Tao set tim nhanh
    tep_loai_tru_set = set(tep_loai_tru)
    thu_muc_con_loai_tru_set = set(thu_muc_con_loai_tru)

    os.makedirs(thu_muc_dau_ra, exist_ok=True) # Tao TM out

    total_files_processed = 0
    total_folders_processed = 0
    all_errors = {}
    all_skipped_files = []
    all_skipped_folders = []
    all_output_paths = []

    for duong_dan in duong_dan_thu_muc: # Lap tung path
        if not os.path.isdir(duong_dan):
            all_errors[duong_dan] = "Thu muc khong ton tai"
            continue

        ten_thu_muc_du_an = os.path.basename(duong_dan)
        thu_muc_dau_ra_du_an = os.path.join(thu_muc_dau_ra, ten_thu_muc_du_an)
        os.makedirs(thu_muc_dau_ra_du_an, exist_ok=True)

        file_extension = ".txt" if output_format == "txt" else ".md"
        ten_file = os.path.join(thu_muc_dau_ra_du_an, f"{ten_tep_co_so}{file_extension}")

        count = 1
        while os.path.exists(ten_file): # Tranh ghi de
            ten_file = os.path.join(thu_muc_dau_ra_du_an, f"{ten_tep_co_so} {count}{file_extension}")
            count += 1
        all_output_paths.append(os.path.abspath(ten_file))

        num_files_processed = 0
        num_folders_processed = 0
        errors = {}
        skipped_files_list = []
        skipped_folders_list = []

        with open(ten_file, "w", encoding="utf-8") as outfile: # Mo tep out
            if output_format == "markdown":
                outfile.write(f"# Du an: {ten_thu_muc_du_an} - ...\n\n") # Tieu de md
            else:
                outfile.write(f"Du an: {ten_thu_muc_du_an} - ...\n\n") # Tieu de txt

            def viet_cau_truc_thu_muc(thu_muc_goc, indent_level=0): # De quy CT TM
                nonlocal num_folders_processed
                thut_le = ("│   " * indent_level + "├── ") if output_format == "txt" else ("    " * indent_level + "- ")

                try:
                    entries = sorted(os.scandir(thu_muc_goc), key=lambda e: (not e.is_dir(), e.name.lower())) # Sap xep
                    for entry in entries:
                        if entry.is_dir(follow_symlinks=False):
                            if entry.name in thu_muc_con_loai_tru_set:
                                outfile.write(thut_le + f"{entry.name}/ (Ko liet ke)\n")
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
                    outfile.write(thut_le + f"{os.path.basename(thu_muc_goc)}/ (Khong tim thay)\n")
                    errors[os.path.basename(thu_muc_goc)] = "Khong tim thay thu muc"
                except PermissionError:
                    outfile.write(thut_le + f"{os.path.basename(thu_muc_goc)}/ (Khong co quyen)\n")
                    errors[os.path.basename(thu_muc_goc)] = "Khong co quyen truy cap"
                except OSError as e:
                    outfile.write(thut_le + f"{os.path.basename(thu_muc_goc)}/ (Loi HDH: {e})\n")
                    errors[os.path.basename(thu_muc_goc)] = f"Loi he thong: {e}"

            def viet_noi_dung_tep(thu_muc_goc): # De quy ND tep
                nonlocal num_files_processed
                try:
                    entries = sorted(os.scandir(thu_muc_goc), key=lambda e: (not e.is_dir(), e.name.lower())) # Sap xep
                    for entry in entries:
                        if entry.is_dir(follow_symlinks=False):
                            if entry.name in thu_muc_con_loai_tru_set:
                                continue
                            viet_noi_dung_tep(entry.path)
                        elif entry.is_file(follow_symlinks=False):
                            if entry.name.endswith(tuple(tep_loai_tru)) or entry.name in tep_loai_tru_set:
                                # Da skip o viet_cau_truc, nhung check lai cho chac
                                if os.path.relpath(entry.path, duong_dan) not in skipped_files_list:
                                     skipped_files_list.append(os.path.relpath(entry.path, duong_dan))
                                continue
                            if entry.name.endswith(SUPPORTED_FILE_EXTENSIONS):
                                outfile.write(f"\n**{os.path.relpath(entry.path, duong_dan)}**\n\n") # Path tuong doi voi TM goc DA
                                outfile.write("```")
                                lang = ""
                                if entry.name.endswith('.py'): lang = "python"
                                # Them cac lang khac neu can
                                outfile.write(f"{lang}\n")

                                try:
                                    with open(entry.path, "r", encoding="utf-8", errors="surrogateescape") as infile: # errors='surrogateescape'
                                        outfile.write(infile.read())
                                    num_files_processed += 1
                                except UnicodeDecodeError: # Neu surrogateescape van loi
                                    try:
                                        with open(entry.path, "r", encoding="latin-1") as infile:
                                            outfile.write(infile.read())
                                        num_files_processed += 1
                                        outfile.write("\n\n_(Luu y: Tep co the ko ma hoa UTF-8, ND doc bang latin-1)_\n")
                                    except Exception as e_latin:
                                        outfile.write(f"Khong the doc tep {entry.path}: {e_latin}\n")
                                        errors[entry.path] = str(e_latin)
                                except FileNotFoundError:
                                    outfile.write(f"Khong tim thay tep {entry.path}...\n")
                                    errors[entry.path] = "Khong tim thay tep"
                                except PermissionError:
                                    outfile.write(f"Khong co quyen truy cap tep {entry.path}...\n")
                                    errors[entry.path] = "Khong co quyen truy cap"
                                except OSError as e_os:
                                    outfile.write(f"Loi doc tep {entry.path}: {e_os}\n")
                                    errors[entry.path] = f"Loi he thong: {e_os}"
                                outfile.write("\n```\n\n")
                except FileNotFoundError:
                    errors[thu_muc_goc] = "Khong tim thay thu muc (khi doc ND)" # Phan biet loi
                except PermissionError:
                    errors[thu_muc_goc] = "Khong co quyen truy cap (khi doc ND)"
                except OSError as e:
                    errors[thu_muc_goc] = f"Loi he thong (khi doc ND): {e}"

            outfile.write(f"{os.path.basename(duong_dan)}/\n") # Ghi ten TM goc
            viet_cau_truc_thu_muc(duong_dan)
            outfile.write("\n--- START CONTENT ---\n") # Phan cach CT TM va ND
            viet_noi_dung_tep(duong_dan)
            outfile.write("\n--- END CONTENT ---\n\n")

        total_files_processed += num_files_processed
        total_folders_processed += num_folders_processed
        all_errors.update(errors)
        all_skipped_files.extend(list(set(skipped_files_list)))
        all_skipped_folders.extend(list(set(skipped_folders_list)))

    end_time = time.time()
    execution_time = end_time - start_time
    message = f"Tai lieu du an da tao trong {thu_muc_dau_ra}"
    if verbose:
        message += f"\nDa xu ly {total_files_processed} tep va {total_folders_processed} thu muc."

    output_paths_str = ", ".join(all_output_paths)
    return (message, execution_time, total_files_processed, total_folders_processed,
            all_errors, all_skipped_files, all_skipped_folders, output_paths_str)