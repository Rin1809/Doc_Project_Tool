
import sys
import os
import json


current_script_path = os.path.abspath(__file__)
core_dir = os.path.dirname(current_script_path)
project_root_dir = os.path.dirname(core_dir)


if project_root_dir not in sys.path:
    sys.path.insert(0, project_root_dir)

from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon


from Core.translations import Translations
from Core.main_app import ProjectDocApp
from Core.constants import ASSETS_DIR_NAME, DEFAULT_ICON_NAME, CONFIG_FILE_NAME, DEFAULT_LANGUAGE

IS_WINDOWS = os.name == 'nt'
if IS_WINDOWS:
    try:
        import ctypes
        myappid = u'mycompany.docprojecttool.pyside6.1_0_0'
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    except (ImportError, AttributeError, Exception):
        pass

def load_initial_language_setting(path_to_core_dir): 
    config_path = os.path.join(path_to_core_dir, CONFIG_FILE_NAME)
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

    
    load_initial_language_setting(core_dir) 

    icon_path_app_level = os.path.join(project_root_dir, ASSETS_DIR_NAME, DEFAULT_ICON_NAME)
    if os.path.exists(icon_path_app_level):
        app.setWindowIcon(QIcon(icon_path_app_level))
    else:
        print(f"Application icon not found: {icon_path_app_level}")

    window = ProjectDocApp(project_root_dir)
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":

    main()