import sys
import os
import json

# __file__ la file run_app.py nam o thu muc goc cua du an
project_root_dir = os.path.dirname(os.path.abspath(__file__)) # TM goc cua DA
core_module_dir = os.path.join(project_root_dir, "Core") # Duong dan den TM Core

# Them TM goc vao sys.path de import dc cac module trong Core
if project_root_dir not in sys.path:
    sys.path.insert(0, project_root_dir)

from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon

# Cac module trong Core gio co the import truc tiep
from Core.translations import Translations
from Core.main_app import ProjectDocApp
from Core.constants import ASSETS_DIR_NAME, DEFAULT_ICON_NAME, CONFIG_FILE_NAME, DEFAULT_LANGUAGE

IS_WINDOWS = os.name == 'nt'
if IS_WINDOWS:
    try:
        import ctypes
        myappid = u'mycompany.docprojecttool.pyside6.1_0_0' # Dat app id cho Windows
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    except (ImportError, AttributeError, Exception):
        # Bo qua neu ko set dc app id (vd: ko co ctypes)
        pass

def load_initial_language_setting(path_to_core_dir_containing_config): 
    # file config nam trong TM Core
    config_path = os.path.join(path_to_core_dir_containing_config, CONFIG_FILE_NAME)
    lang = DEFAULT_LANGUAGE
    try:
        if os.path.exists(config_path):
            with open(config_path, 'r', encoding='utf-8') as f:
                config_data = json.load(f)
            lang = config_data.get("language", DEFAULT_LANGUAGE)
        Translations.set_language(lang)
    except Exception as e:
        print(f"Error loading language from config for run_app: {e}. Using default: {DEFAULT_LANGUAGE}")
        Translations.set_language(DEFAULT_LANGUAGE) # Mac dinh neu loi

def main():
    app = QApplication(sys.argv)
    
    # Load ngon ngu tu config trong TM Core
    load_initial_language_setting(core_module_dir) 

    # Icon cua UD nam trong assets/ o TM goc
    icon_path_app_level = os.path.join(project_root_dir, ASSETS_DIR_NAME, DEFAULT_ICON_NAME)
    if os.path.exists(icon_path_app_level):
        app.setWindowIcon(QIcon(icon_path_app_level))
    else:
        # Su dung Translations.get neu an toan, hoac print don gian
        print(Translations.get("run_app_icon_not_found_console", path=icon_path_app_level))


    # Khoi tao cua so chinh, truyen vao duong dan TM goc
    window = ProjectDocApp(project_root_dir)
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()