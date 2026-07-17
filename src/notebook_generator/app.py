import ttkbootstrap as ttk

def start():
    ttk.Style.instance = None
    from src.notebook_generator.gui.main_window import MainWindow
    from i18n.manager import load_language
    import yaml

    with open('Config/user_config.yml', 'r', encoding='utf-8') as f:
        configFile = yaml.safe_load(f)

    _ = load_language(configFile['language'])

    main = MainWindow(_=_,config=configFile)
    main.run()

if __name__ == "__main__":
    start()
