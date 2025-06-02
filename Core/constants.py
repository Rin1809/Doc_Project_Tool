# Hang so cho UD

# --- Ngon ngu ---
DEFAULT_LANGUAGE = "vi" # Ngon ngu mac dinh neu config ko co
CONFIG_FILE_NAME = "doc_tool_config.json" # Ten file config

# Fonts (Kich thuoc co the dung cho QSS)
TITLE_FONT_SIZE = 18 
HEADER_FONT_SIZE = 14
NORMAL_FONT_SIZE = 10 
SMALL_FONT_SIZE = 9

# Mau sac (Dung cho QSS, co the dat ten theo vai tro)
PRIMARY_COLOR = "rgb(75, 80, 115)" 
ACCENT_COLOR = "rgb(96, 125, 199)" 
HOVER_COLOR = "rgb(116, 145, 219)" 
SUCCESS_COLOR = "rgb(90, 180, 90)"  
WARNING_COLOR = "rgb(220, 160, 70)" 
ERROR_COLOR = "rgb(200, 80, 80)"   

TEXT_COLOR = "rgb(238, 235, 245)"
SUBTEXT_COLOR = "rgb(175, 170, 185)"
INPUT_BG_COLOR = "rgba(12, 15, 28, 0.92)"
INPUT_BORDER_COLOR = "rgba(170, 150, 200, 0.55)"
INPUT_FOCUS_BORDER_COLOR = "rgb(210, 190, 250)"
WINDOW_BG_COLOR = "rgb(10, 12, 22)" 
CONTAINER_BG_COLOR = "rgba(20, 24, 40, 0.88)" 
TITLE_BAR_BG_COLOR = "rgba(15, 18, 30, 0.9)"

# Loai tru MD
DEFAULT_EXCLUDED_SUBDIRS = ["__pycache__", "moitruongao", "venv", ".git", ".vscode", "bieutuong", "memory", "node_modules", "uploads", "chats", "package-lock.json", "dist", "build", "assets"] 
DEFAULT_EXCLUDED_FILES = [".pyc", "desktop.ini", ".rar", "ex.json", ".jpg", ".mp3", ".png", ".ico", ".jpeg", ".gif"] 

# Ten tep & TM MD
DEFAULT_OUTPUT_DIR = "."
DEFAULT_BASE_FILENAME = "tai_lieu_du_an"

# File ext ho tro
SUPPORTED_FILE_EXTENSIONS = ('.py', '.js', '.java', '.cpp', '.html', '.css', '.bat', '.sh', '.txt', '.env', '.tsx', '.mjs', '.json', '.ts', 'Dockerfile', '.qss', '.md') 

# Lich su
HISTORY_FILE = "doc_tool_history.json" 
MAX_HISTORY_ITEMS = 15 

# UI PySide6
WINDOW_DEFAULT_WIDTH = 1000
WINDOW_DEFAULT_HEIGHT = 800
WINDOW_MIN_WIDTH = 800
WINDOW_MIN_HEIGHT = 700
RESIZE_MARGIN = 10
NO_EDGE, TOP_EDGE, BOTTOM_EDGE, LEFT_EDGE, RIGHT_EDGE = 0x0, 0x1, 0x2, 0x4, 0x8
TOP_LEFT_CORNER, TOP_RIGHT_CORNER = TOP_EDGE | LEFT_EDGE, TOP_EDGE | RIGHT_EDGE
BOTTOM_LEFT_CORNER, BOTTOM_RIGHT_CORNER = BOTTOM_EDGE | LEFT_EDGE, BOTTOM_EDGE | RIGHT_EDGE

# Paths
ASSETS_DIR_NAME = "assets"
DEFAULT_ICON_NAME = "icon.ico"
DEFAULT_BACKGROUND_NAME = "background.jpg"
