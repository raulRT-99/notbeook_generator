import pathlib
from tkinter.filedialog import askdirectory, askopenfilename
from ttkbootstrap.scrolled import ScrolledFrame

import ttkbootstrap as ttk
from ttkbootstrap.constants import *


class MainWindow:
    def __init__(self, _):
        self.font_size = 10
        # ---MAIN WINDOW---
        self.root = ttk.Window(themename="superhero")
        self.root.title("Mi aplicación")
        self.root.geometry(str(self.font_size*155)+"x1000")
        style = ttk.Style()
        style.configure('.', font=('Segoe UI', self.font_size))
        # ---TOP BUTTOM BAR---
        self.buttonbar = ttk.Frame(self.root, style="primary.TFrame")
        self.buttonbar.pack(side=TOP, fill=X)
        # ---SCROLLED FRAME---
        self.sf = ScrolledFrame(self.root, autohide=True)
        self.sf.pack(fill=BOTH, expand=YES, padx=10, pady=10)
        # ADD TOP BUTTOM BAR
        self.topButtonBar()

        self.row = ttk.Frame(self.sf)
        self.row.pack(fill=X, pady=30)

        # ---NAME---
        labelOutput = ttk.Label(self.row, text="Nombre de salida:", width=15)
        labelOutput.grid(row=0, column=0, padx=(0, 10), sticky="w")
        self.output_name = ttk.Entry(self.row, width=30, font=('Helvetica', self.font_size))
        self.output_name.grid(row=0, column=1, sticky="ew", padx=(20, 10))
        # ---SELECT FOLDER---
        self.output_folder = None
        output_directory = pathlib.Path().absolute().as_posix()
        self.output_path_var = ttk.StringVar(value=output_directory)
        self.option_rg = ttk.Label(self.row, text="trad-select folder", padding=10)
        self.option_rg.grid(row=0, column=2, sticky="w")
        self.create_path_row('directory')
        # ---------------------------
        self.separator = ttk.Separator(self.sf, bootstyle='warning')
        self.separator.pack(fill='x')
        # ---------------------------
        # ---SELECT FILE---
        self.row2 = ttk.Frame(self.sf)
        self.row2.pack(fill=X, pady=30)
        self.init_file = None
        file_directory = pathlib.Path().absolute().as_posix()
        self.file_path_var = ttk.StringVar(value=file_directory)
        self.option_lf = ttk.Label(self.row2, text="trad-select file", padding=10)
        self.option_lf.grid(row=0, column=0, sticky="w")
        self.create_path_row('file')
        # ---SEPARATOR IN FILE---
        label_sep = ttk.Label(self.row2, text="trad-separator", width=15)
        label_sep.grid(row=0, column=1, padx=(20, 10), sticky="w")
        self.output_sep = ttk.Entry(self.row2, width=35)
        self.output_sep.grid(row=0, column=2, sticky="ew", padx=(0, 10))
        # ---------------------------
        self.separator2 = ttk.Separator(self.sf, bootstyle='warning')
        self.separator2.pack(fill='x')
        # ---------------------------
        row3 = ttk.Frame(self.sf)
        row3.pack(fill=X, pady=30)
        # ---TYPE OF DATASET---
        label_sep = ttk.Label(row3, text="trad-type of dataset", width=20)
        label_sep.grid(row=0, column=0, padx=(0, 10), sticky="w")
        self.dataframe_type_map = {
            "Clasificación": "classification",
            "Regresión": "regression"
        }
        self.dftype_cb = ttk.Combobox(row3, values=list(self.dataframe_type_map.keys()), state="readonly", font=('Helvetica', self.font_size))
        self.dftype_cb.grid(row=0, column=1, sticky="ew", padx=(20, 10))
        self.dftype_cb.current(0)
        # ---FEATURES---
        labelFeatures = ttk.Label(row3, text="trad-features:", width=12)
        labelFeatures.grid(row=0, column=2, padx=(20, 5), sticky="w")
        self.feature_names = ttk.Entry(row3, width=70, font=('Helvetica', self.font_size))
        self.feature_names.grid(row=0, column=3, sticky="ew", padx=(20, 10))
        # ---TARGET CLASS---
        labelTarget = ttk.Label(row3, text="trad-target:", width=12)
        labelTarget.grid(row=1, column=0, padx=(0, 10), sticky="w", pady=(30, 0))
        self.target_feature = ttk.Entry(row3, width=25, font=('Helvetica', self.font_size))
        self.target_feature.grid(row=1, column=1, sticky="ew", padx=(0, 10), pady=(30, 0))
        # ---------------------------
        self.separator2 = ttk.Separator(self.sf, bootstyle='warning')
        self.separator2.pack(fill='x')
        # ---------------------------
        # ***DESCRIBE OPTIONS***
        row4 = ttk.Frame(self.sf)
        row4.pack(fill=X, pady=30)
        self.describe_val = ttk.BooleanVar(row4, value=False)
        # --DESCRIBE?--
        self.enable_resume = ttk.Checkbutton(
            row4,
            text="trad-Describe data",
            variable=self.describe_val,
            command=lambda: self.toggle_enable_cb_options(self.describe_val, self.enable_describe_options_frame)
        )
        # --RESUME PLOTS--
        self.enable_resume.grid(row=0, column=0, padx=5, pady=5)
        self.enable_describe_options_frame = ttk.Frame(row4)
        ttk.Label(self.enable_describe_options_frame, text="trad-Number of plots").grid(row=0, column=0, padx=5, pady=5)
        self.resume_plots_cb = ttk.Combobox(self.enable_describe_options_frame, values=[0, 1, 2, 3, 4],
                                            state="readonly", font=('Helvetica', self.font_size))
        self.resume_plots_cb.grid(row=0, column=1, padx=5, pady=5)
        self.resume_plots_cb.current(0)
        # ***PREPROCESSING***
        row5 = ttk.Frame(self.sf)
        row5.pack(fill=X, pady=30)
        # --ENABLE PREPROCESSING?--
        self.preprocessing_val = ttk.BooleanVar(row5, value=False)
        self.enable_preprocessing = ttk.Checkbutton(
            row5,
            text="trad-Enable preprocessing",
            variable=self.preprocessing_val,
            command=lambda: self.toggle_enable_cb_options(self.preprocessing_val,
                                                          self.enable_preprocessing_options_frame)
        )
        # --NORMALIZING TYPE
        self.enable_preprocessing.grid(row=0, column=0, padx=5, pady=5)
        self.enable_preprocessing_options_frame = ttk.Frame(row5)
        ttk.Label(self.enable_preprocessing_options_frame, text="trad-Normalize type").grid(row=0, column=0, padx=5,
                                                                                            pady=5)
        self.resume_plots_cb = ttk.Combobox(self.enable_preprocessing_options_frame,
                                            values=['MinMaxScaler', 'StandardScaler', 'Normalizer'],
                                            state="readonly", font=('Helvetica', self.font_size))
        self.resume_plots_cb.grid(row=0, column=1, padx=5, pady=5)
        self.resume_plots_cb.current(0)
        #---ENABLE FEATURE SELECTION---
        row6 = ttk.Frame(self.sf)
        row6.pack(fill=X, pady=30)
        self.enable_feature_selection = ttk.Checkbutton(row6,text="trad-Enable feature selection")
        self.enable_feature_selection.grid(row=0, column=0,padx=5, pady=5)
        #---ENABLE PREDICTIONS---
        self.enable_prediction = ttk.Checkbutton(row6, text="trad-Enable prediction")
        self.enable_prediction.grid(row=0, column=1, padx=(50,0), pady=5)














        self.container = ttk.Frame(self.sf, padding=0)
        self.container.pack(side=TOP, fill=BOTH, expand=YES)
        title = ttk.Label(self.container, text="Página principal", font=("Segoe UI", 20, "bold"))
        title.pack(pady=20)

    def topButtonBar(self):
        btn = ttk.Button(self.buttonbar, text="Option 1", command=self.option1)
        btn.pack(side=LEFT, padx=5, pady=5)

    def option1(self):
        print("clicked")
        self.change_separator()

    def create_path_row(self, type):
        if type == 'directory':
            output_path_row = ttk.Frame(self.option_rg)
            output_path_row.grid(row=0, column=0, sticky="ew")
            path_lbl = ttk.Label(output_path_row,
                                 text="trad-Ubicacion final",
                                 width=20)
            path_lbl.grid(row=0, column=0, padx=(0, 10), pady=5, sticky="w")
            self.output_folder = ttk.Entry(output_path_row, textvariable=self.output_path_var, width=50, font=('Helvetica', self.font_size))
            self.output_folder.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
            browse_btn = ttk.Button(
                output_path_row,
                text="tradBrowse",
                command=lambda: self.on_browse(type),
                width=self.font_size
            )
            browse_btn.grid(row=0, column=2, padx=5, pady=5, sticky="w")
            output_path_row.columnconfigure(1, weight=1)
        else:
            file_path_row = ttk.Frame(self.option_lf)
            file_path_row.grid(row=0, column=0, sticky="ew")
            path_lbl = ttk.Label(file_path_row,
                                 text='trad-Ubicacion archivo',
                                 width=20)
            path_lbl.grid(row=0, column=0, padx=(0, 10), pady=5, sticky="w")
            self.init_file = ttk.Entry(file_path_row, textvariable=self.file_path_var, width=50,
                                 font=('Helvetica', self.font_size))
            self.init_file.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
            browse_btn = ttk.Button(
                file_path_row,
                text="tradBrowse",
                command=lambda: self.on_browse(type),
                width=self.font_size
            )
            browse_btn.grid(row=0, column=2, padx=5, pady=5, sticky="w")
            file_path_row.columnconfigure(1, weight=1)


    def on_browse(self, type):
        if type == 'directory':
            path = askdirectory(title="trad-Browse directory")
        else:
            path = askopenfilename(
                title="trad-Selecciona un archivo",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
            )
        if path:
            self.output_path_var.set(path)

    def run(self):
        self.sf.mainloop()

    def change_separator(self):
        self.separator.configure(bootstyle="success")

    def toggle_enable_cb_options(self, boolean_value_cb, options_frame):
        if boolean_value_cb.get():
            options_frame.grid(row=1, column=0, sticky="ew", pady=10)
        else:
            options_frame.grid_forget()


if __name__ == "__main__":
    app = MainWindow()
    app.run()
