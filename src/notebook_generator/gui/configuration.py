from tkinter.constants import X

import ttkbootstrap as ttk

class configurationWindow:
    def __init__(self):
        self.font_size = 10
        self.ingnore_wearnings = False
        self.create_btn_style = 'secondary'
        # ---CONFIGURATION WINDOW---
        self.root = ttk.Window(themename="superhero")
        self.root.title("Personalizacion")
        self.screen_width = self.font_size * 155
        self.root.geometry(str(self.screen_width//2) + "x800")
        style = ttk.Style()
        style.configure('.', font=('Segoe UI', self.font_size))
        #---FONT SIZE---
        self.row1 = ttk.Frame(self.root)
        self.row1.pack(fill=X, pady=30)
        self.fontsize_lbl = ttk.Label(self.row1, text="Tamaño de fuente:", width=15)
        self.fontsize_lbl.grid(row=0,column=0)
        self.fontsizes = {
            "Small": 10,
            "Medium": 11,
            "Large": 12
        }
        self.fontsize_cb = ttk.Combobox(self.row1, values=list(self.fontsizes.keys()), state="readonly",
                                      font=('Helvetica', self.font_size))
        self.fontsize_cb.grid(row=0, column=1, sticky="ew", padx=(20, 10))
        self.fontsize_cb.current(0)


    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = configurationWindow()
    app.run()
