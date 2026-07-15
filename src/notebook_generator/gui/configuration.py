from tkinter.constants import X
from gettext import gettext as _
import yaml

import ttkbootstrap as ttk


class configurationWindow:
    def __init__(self, translator):
        self.params = {}
        self.font_size = 12
        self._ = translator
        self.ingnore_wearnings = False
        self.create_btn_style = 'secondary'
        # ---CONFIGURATION WINDOW---
        self.root = ttk.Toplevel()
        self.root.title("Personalizacion")
        self.screen_width = self.font_size * 155
        self.root.geometry(str(self.screen_width // 2) + "x800")
        style = ttk.Style()
        style.configure('.', font=('Segoe UI', self.font_size))
        self.row1 = ttk.Frame(self.root)
        self.row1.pack(fill=X, pady=50, padx=50)
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
        self.config_options = {
            'font_size': {
                'label': 'trad-fontszie',
                'menu': 'combobox',
                'options': self.fontsizes
            },
            'theme': {
                'label': 'trad-theme',
                'menu': 'combobox',
                'options': self.themes
            },
            'language': {
                'label': 'trad-language',
                'menu': 'combobox',
                'options': self.languages
            },
            'ignore_warnings_create_nb': {
                'label': 'trad-ignore warnings',
                'menu': 'checkbox'
            },
            'ignore_tooltips': {
                'label': 'trad-ignore tooltips',
                'menu': 'checkbox'
            },
            'ignore_rescaling_size': {
                'label': 'trad-ignore rescaling',
                'menu': 'checkbox'
            }
        }

        with open('Config/user_config.yml', 'r', encoding='utf-8') as f:
            configFile = yaml.safe_load(f)

        #---CREATE OPTIONS MENU---
        for x, configOption in enumerate(configFile):
            option = self.config_options[configOption]
            label = ttk.Label(self.row1, text=option['label'], width=18)
            label.grid(row=x, column=0)

            if option['menu'] == 'combobox':
                self.createCombobox(row=x, current=0, map=option['options'])
            elif option['menu'] == 'checkbox':
                self.createCheckbox(current=False, row=x)


    def createCombobox(self, map, row, current):
        combo = ttk.Combobox(self.row1, values=list(map.keys()), state="readonly",
                                     font=('Helvetica', self.font_size))
        combo.grid(row=row, column=1, sticky="ew", padx=(20, 10), pady=20)
        combo.current(current)

    def createCheckbox(self, current, row):
        value = ttk.BooleanVar(self.row1, value=current)
        checkbutton = ttk.Checkbutton(
            self.row1,
            variable=value
        )
        checkbutton.grid(row=row, column=1, padx=5, pady=5, sticky='ew')

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = configurationWindow(translator=_)
    app.run()
