from tkinter.constants import X
from gettext import gettext as _
import yaml
from ttkbootstrap.dialogs import Messagebox

import ttkbootstrap as ttk
from pathlib import Path


class configurationWindow:
    def __init__(self, translator, config=None):
        self.params = {}
        self.config = config
        self.font_size = self.config['font_size']
        self._ = translator
        self.create_btn_style = 'secondary'
        # ---CONFIGURATION WINDOW---
        self.root = ttk.Toplevel()
        self.root.title(self._("PERSONALIZATION-GUI-TITLE"))
        self.screen_width = self.font_size * 155
        self.root.geometry(str(self.screen_width // 2) + "x800")
        style = ttk.Style()
        style.configure('.', font=('Segoe UI', self.font_size))
        self.row1 = ttk.Frame(self.root)
        self.row1.pack(fill=X, pady=50, padx=50)

        BASE_DIR = Path(__file__).resolve().parent.parent
        CONFIG_FILE = BASE_DIR / "Config" / "user_config.yml"

        with CONFIG_FILE.open("r", encoding="utf-8") as f:
            self.configFile = yaml.safe_load(f)

        # ----AVALIABLE OPTIONS----
        self.fontsizes = {
            "10-Small": 10,
            "11": 11,
            "12-Medium": 12,
            "13": 13,
            "14-Large": 14
        }
        self.themes = {
            "light-yeti": 'yeti',
            "light-morph": 'morph',
            "light-simplex": 'simplex',
            "light-pulse": 'pulse',
            "dark-solar": 'solar',
            "dark-superhero": 'superhero',
            "dark-cyborg": 'cyborg',
            "dark-vapor": 'vapor'
        }
        self.languages = {
            "Español": 'es',
            "English": 'en'
        }
        self.allOptionsCombobox = {'font_size': self.fontsizes,
                                   'theme': self.themes,
                                   'language': self.languages}
        self.config_options = {
            'font_size': {
                'label': 'fontszie-lbl',
                'menu': 'combobox',
                'options': self.fontsizes,
                'default': self.configFile['font_size']
            },
            'theme': {
                'label': 'theme-lbl',
                'menu': 'combobox',
                'options': self.themes,
                'default': self.configFile['theme']
            },
            'language': {
                'label': 'language-lbl',
                'menu': 'combobox',
                'options': self.languages,
                'default': self.configFile['language']
            },
            'ignore_warnings_create_nb': {
                'label': 'ignore-warnings-lbl',
                'menu': 'checkbox',
                'default': self.configFile['ignore_warnings_create_nb']
            },
            'ignore_tooltips': {
                'label': 'ignore-tooltips-lbl',
                'menu': 'checkbox',
                'default': self.configFile['ignore_tooltips']
            },
            'ignore_rescaling_size': {
                'label': 'ignore-rescaling-lbl',
                'menu': 'checkbox',
                'default': self.configFile['ignore_rescaling_size']
            }
        }

        # ---CREATE OPTIONS MENU---
        for x, configOption in enumerate(self.configFile):
            option = self.config_options[configOption]
            label = ttk.Label(self.row1, text=self._(option['label']), width=30 , wraplength=270 + len(self._(option['label'])*2),
                              anchor='w' if len(self._(option['label'])) > 20 else 'e')
            label.grid(row=x, column=0, pady=(7, 7), padx=5)

            if option['menu'] == 'combobox':
                listOptions = self.allOptionsCombobox[configOption]
                self.createCombobox(row=x, current=self.getPositionInMap(listOptions, option['default']),
                                    map=option['options'], key=configOption)
            elif option['menu'] == 'checkbox':
                self.createCheckbox(current=option['default'], row=x, key=configOption)

        # ---SAVE AND CANCEL BUTTONS---
        row2 = ttk.Frame(self.root)
        row2.pack(fill=X, pady=30)
        row2.columnconfigure(0, weight=1)
        row2.columnconfigure(1, weight=0)
        row2.columnconfigure(2, weight=0)
        row2.columnconfigure(3, weight=1)
        self.cancel_btn = ttk.Button(row2, text=self._("CANCEL-BTN"), bootstyle='danger', command=self.closeWindow,
                                     width=20)
        self.cancel_btn.grid(column=0, row=0, padx=(100, 10))
        self.save_btn = ttk.Button(row2, text=self._("SAVE-BTN"), bootstyle='success',
                                   command=self.onSave,
                                   width=20)
        self.save_btn.grid(column=1, row=0, padx=(10, 0))

    def onSave(self):
        for key, value in self.params.items():
            self.configFile[key] = value

            with open('Config/user_config.yml', "w", encoding="utf-8") as f:
                yaml.safe_dump(self.configFile, f, allow_unicode=True, sort_keys=False)

        Messagebox.show_info(self._("RESTART-APP-MSG"), 'info')
        self.closeWindow()

    def closeWindow(self):
        self.root.destroy()

    def getPositionInMap(self, map, value):
        valuesList = list(map.values())
        return valuesList.index(value)

    def createCombobox(self, map, row, current, key):
        combo = ttk.Combobox(self.row1, values=list(map.keys()), state="readonly",
                             font=('Helvetica', self.font_size))

        def toggle(event, k=key):
            v = event.widget.get()
            self.params[k] = map[v]

        combo.bind("<<ComboboxSelected>>", toggle)
        combo.grid(row=row, column=1, sticky="ew", padx=(20, 10), pady=20)
        combo.current(current)

    def createCheckbox(self, current, row, key):
        if not hasattr(self, "checkbox_vars"):
            self.checkbox_vars = {}
        var = ttk.BooleanVar(value=bool(current))
        self.checkbox_vars[key] = var

        def toggle(k=key, v=var):
            self.params[k] = v.get()

        checkbutton = ttk.Checkbutton(
            self.row1,
            text="",
            variable=var,
            onvalue=True,
            offvalue=False,
            bootstyle="square-toggle",
            command=lambda: toggle(key, var)
        )
        checkbutton.grid(row=row, column=1, padx=5, pady=5, sticky='ew')

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = configurationWindow(translator=_)
    app.run()
