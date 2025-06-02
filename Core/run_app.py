
import sys
import os
import json
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon

IS_WINDOWS = os.name == 'nt'
if IS_WINDOWS:
    try:
        import ctypes
        myappid = u'mycompany.docprojecttool.pyside6.1_0_0' 
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    except (ImportError, AttributeError, Exception):
        pass 

from .translations import Translations 
from .main_app import ProjectDocApp 
from .constants import ASSETS_DIR_NAME, DEFAULT_ICON_NAME, CONFIG_FILE_NAME, DEFAULT_LANGUAGE # Them import const

def load_initial_language_setting(base_app_path_core):
    config_path = os.path.join(base_app_path_core, CONFIG_FILE_NAME)
    lang = DEFAULT_LANGUAGE
    try:
        if os.path.exists(config_path):
            with open(config_path, 'r', encoding='utf-8') as f:
                config_data = json.load(f)
            lang = config_data.get("language", DEFAULT_LANGUAGE)
        Translations.set_language(lang)
    except Exception as e:
        print(f"Error loading language from config for run_app: {e}. Using default: {DEFAULT_LANGUAGE}")
        Translations.set_language(DEFAULT_LANGUAGE)


def main():
    app = QApplication(sys.argv)
 
    current_file_dir = os.path.dirname(os.path.abspath(__file__)) # Day la thu muc Core
    base_app_path = os.path.dirname(current_file_dir) # Day la Doc_Project_Tool
    
    # Load ngon ngu truoc khi tao cua so chinh
    load_initial_language_setting(current_file_dir) # Truyen vao path toi Core

    icon_path_app_level = os.path.join(base_app_path, ASSETS_DIR_NAME, DEFAULT_ICON_NAME)
    if os.path.exists(icon_path_app_level):
        app.setWindowIcon(QIcon(icon_path_app_level))
    else:
        print(f"Application icon not found: {icon_path_app_level}") 


    window = ProjectDocApp(base_app_path)
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()