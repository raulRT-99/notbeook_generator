import pathlib
from tkinter.filedialog import askdirectory

import ttkbootstrap as ttk
from ttkbootstrap.constants import *

class MainWindow:
    def __init__(self,_):
        self.root = ttk.Window(themename="superhero")
        self.root.title("Mi aplicación")
        self.root.geometry("1300x800")

        self.buttonbar = ttk.Frame(self.root, style="primary.TFrame")
        self.buttonbar.pack(side=TOP, fill=X)

        self.container = ttk.Frame(self.root, padding=0)
        self.container.pack(side=TOP, fill=BOTH, expand=YES)

        self.topButtonBar()

        _path = pathlib.Path().absolute().as_posix()
        self.path_var = ttk.StringVar(value=_path)
        self.option_lf = ttk.Labelframe(self.root, text="dawdawd", padding=15)
        self.option_lf.pack(fill=X, expand=YES, anchor=N)
        self.create_path_row()


        title = ttk.Label(self.container, text="Página principal", font=("Segoe UI", 20, "bold"))
        title.pack(pady=20)

    def topButtonBar(self):
        btn = ttk.Button(self.buttonbar, text="Option 1", command=self.option1)
        btn.pack(side=LEFT, padx=5, pady=5)

    def option1(self):
        print("clicked")

    def create_path_row(self):
        """Add path row to labelframe"""
        path_row = ttk.Frame(self.option_lf)
        path_row.pack(fill=X, expand=YES)
        path_lbl = ttk.Label(path_row, text="Path", width=8)
        path_lbl.pack(side=LEFT, padx=(15, 0))
        path_ent = ttk.Entry(path_row, textvariable=self.path_var)
        path_ent.pack(side=LEFT, fill=X, expand=YES, padx=5)
        browse_btn = ttk.Button(
            master=path_row,
            text="Browse",
            command = self.on_browse,
            width=8
        )
        browse_btn.pack(side=LEFT, padx=5)

    def on_browse(self):
        """Callback for directory browse"""
        path = askdirectory(title="Browse directory")
        if path:
            self.path_var.set(path)


    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = MainWindow()
    app.run()