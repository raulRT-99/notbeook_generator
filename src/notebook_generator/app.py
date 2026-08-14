import sys
from pathlib import Path

import ttkbootstrap as ttk

APP_DIR = Path(sys.argv[0]).resolve().parent

BUNDLED_DIR = Path(__file__).resolve().parent

EXTERNAL_CONFIG_DIR = APP_DIR / "Config"
EXTERNAL_CONFIG_FILE = EXTERNAL_CONFIG_DIR / "user_config.yml"

BUNDLED_CONFIG_FILE = BUNDLED_DIR / "Config" / "user_config.yml"

EXTERNAL_CONFIG_DIR.mkdir(parents=True, exist_ok=True)

config_file = {
    "font_size": 12,
    "theme": "superhero",
    "language": "es",
    "ignore_warnings_create_nb": False,
    "ignore_tooltips": False,
    "ignore_rescaling_size": False
}


def start():
    ttk.Style.instance = None
    from src.notebook_generator.gui.main_window import MainWindow
    from src.notebook_generator.i18n.manager import load_language
    import yaml

    BASE_DIR = Path(__file__).resolve().parent
    CONFIG_FILE = BASE_DIR / "Config" / "user_config.yml"

    if not CONFIG_FILE.exists():
        with CONFIG_FILE.open("w", encoding="utf-8") as f:
            yaml.safe_dump(config_file, f, allow_unicode = True, sort_keys = False)

    with CONFIG_FILE.open("r", encoding="utf-8") as f:
        configFile = yaml.safe_load(f)

    _ = load_language(configFile['language'])

    main = MainWindow(_=_, config=configFile)
    main.run()

if __name__ == "__main__":
    start()
