from tkinter.filedialog import askdirectory, askopenfilename
from src.notebook_generator.gui.preCreate import onCreate
from src.notebook_generator.generators.algorithms.base.algorithms_properties import ML_ALGORITHMS
from src.notebook_generator.gui.configuration import configurationWindow
from gettext import gettext as _
import webbrowser
from ttkbootstrap.tooltip import ToolTip
from pathlib import Path
import requests

from ttkbootstrap.dialogs import Messagebox

import ttkbootstrap as ttk
from ttkbootstrap.constants import *


class MainWindow:
    def __init__(self, _, config=None):
        self.config = config
        self._ = _
        self.lang = self._("language")
        self.predict_params = {}
        self.predictionAlgorithms = {}
        self.font_size = config['font_size']
        self.ignore_warnings = config['ignore_warnings_create_nb']
        self.create_btn_style = 'secondary'
        self.ignore_rescaling = config['ignore_rescaling_size']
        # ---MAIN WINDOW---
        self.root = ttk.Window(themename=self.config['theme'])
        self.root.title("Notebook Generator")
        self.screen_width = min(self.font_size * 155, 1900 if not self.ignore_rescaling else 9999)
        self.screen_height = min(self.font_size * 90, 1000 if not self.ignore_rescaling else 9999)
        self.root.geometry(str(self.screen_width) + "x" + str(self.screen_height))
        style = ttk.Style()
        style.configure('.', font=('Segoe UI', self.font_size))

        self.root.option_add('*TCombobox*Listbox.font', ('Segoe UI', self.font_size))
        self.root.option_add('*TCombobox*Font', ('Segoe UI', self.font_size))
        # ---TOP BUTTOM BAR---
        self.buttonbar = ttk.Frame(self.root, style="primary.TFrame")
        self.buttonbar.pack(side=TOP, fill=X)

        # ---SCROLLED FRAME---
        self.container = ttk.Frame(self.root)
        self.container.pack(fill=BOTH, expand=YES, padx=10, pady=10)

        self.canvas = ttk.Canvas(self.container)
        self.canvas.grid(row=0, column=0, sticky="nsew")

        self.vbar = ttk.Scrollbar(self.container, orient=VERTICAL, command=self.canvas.yview)
        self.vbar.grid(row=0, column=1, sticky="ns")

        self.hbar = ttk.Scrollbar(self.container, orient=HORIZONTAL, command=self.canvas.xview)
        self.hbar.grid(row=1, column=0, sticky="ew")

        self.canvas.configure(yscrollcommand=self.vbar.set, xscrollcommand=self.hbar.set)

        self.sf = ttk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.sf, anchor="nw")

        self.sf.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        # ADD TOP BUTTOM BAR
        self.topButtonBar()

        self.row = ttk.Frame(self.sf)
        self.row.pack(fill=X, pady=30)

        # ---NAME---
        labelOutput = ttk.Label(self.row, text=self._("labelOutput"), width=17,
                                wraplength=180 + len(self._("labelOutput")))
        labelOutput.grid(row=0, column=0, padx=(0, 10), sticky="w")
        self.output_name = ttk.Entry(self.row, width=30, font=('Helvetica', self.font_size))
        self.output_name.grid(row=0, column=1, sticky="ew", padx=(10, 50))
        # ---SELECT FOLDER---
        self.output_folder = None
        output_directory = ''
        self.output_path_var = ttk.StringVar(value=output_directory)
        self.select_folder_lbl = ttk.Label(self.row, text=self._("select_folder_lbl"), padding=10)
        self.select_folder_lbl.grid(row=0, column=2, sticky="w")
        self.create_path_row('directory')
        # ---------------------------
        self.separator1 = ttk.Separator(self.sf, bootstyle='light')
        self.separator1.pack(fill='x')
        # ---------------------------
        # ---SELECT FILE---
        self.row2 = ttk.Frame(self.sf)
        self.row2.pack(fill=X, pady=30)
        self.init_file = None
        file_directory = ''
        self.file_path_var = ttk.StringVar(value=file_directory)
        self.select_file_lbl = ttk.Label(self.row2, text=self._("select_file_lbl"), padding=10)
        self.select_file_lbl.grid(row=0, column=0, sticky="w")
        self.create_path_row('file')
        # ---SEPARATOR IN FILE---
        separator_lbl = ttk.Label(self.row2, text=self._("separator_lbl"), width=15, wraplength=200)
        separator_lbl.grid(row=0, column=1, padx=(20, 10), sticky="w")
        self.file_separator_str = ttk.Entry(self.row2, width=30)
        self.file_separator_str.grid(row=0, column=2, sticky="ew", padx=(0, 10))
        # ---------------------------
        self.separator2 = ttk.Separator(self.sf, bootstyle='light')
        self.separator2.pack(fill='x')
        # ---------------------------
        row3 = ttk.Frame(self.sf)
        row3.pack(fill=X, pady=30)
        # ---TYPE OF DATASET---
        dataset_type_lbl = ttk.Label(row3, text=self._("dataset_type_lbl"), width=20)
        dataset_type_lbl.grid(row=0, column=0, padx=(0, 10), sticky="w")

        dataframe_type_map_es = {
            "Clasificación": "classification",
            "Regresión": "regression"
        }
        dataframe_type_map_en = {
            "Classification": "classification",
            "Regression": "regression"
        }

        self.dataframe_type_map = dataframe_type_map_es if self.lang == 'es' else dataframe_type_map_en
        self.dftype_cb = ttk.Combobox(row3, values=list(self.dataframe_type_map.keys()), state="readonly",
                                      font=('Helvetica', self.font_size))
        self.dftype_cb.grid(row=0, column=1, sticky="ew", padx=(20, 10))
        self.dftype_cb.current(0)
        # ---FEATURES---
        labelFeatures = ttk.Label(row3, text=self._("labelFeatures"), width=15,
                                  wraplength=160 + len(self._("labelFeatures")))
        labelFeatures.grid(row=0, column=2, padx=(20, 5), sticky="w")
        self.feature_names = ttk.Entry(row3, width=65, font=('Helvetica', self.font_size))
        self.feature_names.grid(row=0, column=3, sticky="ew", padx=(20, 10))
        # ---TARGET CLASS---
        labelTarget = ttk.Label(row3, text=self._("labelTarget"), width=15)
        labelTarget.grid(row=1, column=0, padx=(0, 10), sticky="w", pady=(30, 0))
        self.target_feature = ttk.Entry(row3, width=25, font=('Helvetica', self.font_size))
        self.target_feature.grid(row=1, column=1, sticky="ew", padx=(0, 10), pady=(30, 0))
        # ---------------------------
        self.separator3 = ttk.Separator(self.sf, bootstyle='light')
        self.separator3.pack(fill='x')
        # ---------------------------
        # ***DESCRIBE OPTIONS***
        row4 = ttk.Frame(self.sf)
        row4.pack(fill=X, pady=30)
        self.describe_val = ttk.BooleanVar(row4, value=False)
        # --DESCRIBE?--
        self.enable_resume = ttk.Checkbutton(
            row4,
            text=self._("enable_resume_txt"),
            variable=self.describe_val,
            command=lambda: self.toggle_enable_cb_options(self.describe_val, self.enable_describe_options_frame, 1)
        )
        # --RESUME PLOTS--
        self.enable_resume.grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.enable_describe_options_frame = ttk.Frame(row4)
        ttk.Label(self.enable_describe_options_frame, text=self._("plots_number_lbl")).grid(row=0, column=0, padx=5,
                                                                                            pady=5)
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
            text=self._("enable_preprocessing_txt"),
            variable=self.preprocessing_val,
            command=lambda: (self.toggle_enable_cb_options(self.preprocessing_val,
                                                           self.enable_preprocessing_options_frame, 1),
                             self.describeNormalizingType(), self.toggle_enable_cb_options(
                ttk.BooleanVar(self.enable_preprocessing_options_frame, value=False),
                self.enable_negative_data_options_frame, 3), self.negative_data_val.set(False))
        )
        # --NORMALIZING TYPE--
        self.enable_preprocessing.grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.enable_preprocessing_options_frame = ttk.Frame(row5)
        ttk.Label(self.enable_preprocessing_options_frame, text=self._("normalize_type_lbl")).grid(row=0, column=0,
                                                                                                   padx=5,
                                                                                                   pady=5, sticky='w')
        self.normalize_type_cb = ttk.Combobox(self.enable_preprocessing_options_frame,
                                              values=['MinMaxScaler', 'StandardScaler', 'Normalizer'],
                                              state="readonly", font=('Helvetica', self.font_size))
        self.normalize_type_cb.grid(row=0, column=1, padx=5, pady=5, sticky='w')
        self.normalize_type_cb.current(0)
        self.describe_normalizing_type_lbl = ttk.Label(self.enable_preprocessing_options_frame,
                                                       text='',
                                                       wraplength=900,
                                                       justify="left")
        self.describe_normalizing_type_lbl.grid(row=0, column=2, padx=(50, 5))
        self.normalize_type_cb.bind("<<ComboboxSelected>>", self.describeNormalizingType)
        # -NEGATIVE DATA-
        self.negative_data_val = ttk.BooleanVar(self.enable_preprocessing_options_frame, value=False)
        self.enable_negative_data = ttk.Checkbutton(
            self.enable_preprocessing_options_frame,
            text=self._("negative_data_txt"),
            variable=self.negative_data_val,
            command=lambda: self.toggle_enable_cb_options(self.negative_data_val,
                                                          self.enable_negative_data_options_frame, 3)
        )
        self.enable_negative_data_options_frame = ttk.Frame(row5)
        self.enable_negative_data.grid(row=2, column=0, padx=5, pady=5, sticky='w')
        # NEGATIVE FEATURES
        labelNegativeFeatures = ttk.Label(self.enable_negative_data_options_frame, text=self._("labelNegativeFeatures"),
                                          width=15, wraplength=200)
        labelNegativeFeatures.grid(row=0, column=0, padx=5, sticky="w")
        self.negative_feature_names = ttk.Entry(self.enable_negative_data_options_frame, width=60,
                                                font=('Helvetica', self.font_size))
        self.negative_feature_names.grid(row=0, column=1, sticky="w", padx=(20, 10))
        # ---------------------------
        self.separator4 = ttk.Separator(self.sf, bootstyle='light')
        self.separator4.pack(fill='x')
        # ---------------------------
        # ---ENABLE FEATURE SELECTION---
        row6 = ttk.Frame(self.sf)
        row6.pack(fill=X, pady=30)
        self.feature_selection_val = ttk.BooleanVar(row6, value=False)
        self.enable_feature_selection = ttk.Checkbutton(row6, variable=self.feature_selection_val,
                                                        text=self._("feature_selection_txt"))
        self.enable_feature_selection.grid(row=0, column=0, padx=5, pady=5)
        # ---MULTINOTEBOOK---
        self.multinotebook_val = ttk.BooleanVar(row6, value=False)
        self.enable_multinotebook = ttk.Checkbutton(row6, variable=self.multinotebook_val,
                                                    text=self._("multinotebook_txt"))
        self.enable_multinotebook.grid(row=0, column=2, padx=(50, 0), pady=5)
        # -----------------------
        row7 = ttk.Frame(self.sf)
        row7.pack(fill=X, pady=30)
        # ***ENABLE PREDICTIONS***
        self.prediction_val = ttk.BooleanVar(row4, value=False)
        self.enable_prediction = ttk.Checkbutton(
            row7,
            text=self._("predictions_txt"),
            variable=self.prediction_val,
            command=lambda: self.toggle_enable_cb_options(self.prediction_val, self.enable_prediction_options, 1)
        )
        self.enable_prediction.grid(row=0, column=0, padx=(5, 0), pady=5)

        # --PREDICTION SETTINGS--
        self.enable_prediction_options = ttk.Frame(row7)
        self.predictionSettings(self.enable_prediction_options)

        self.container = ttk.Frame(self.sf, padding=0)
        self.container.pack(side=TOP, fill=BOTH, expand=YES)
        # ---VALIDATE AND CREATE BUTTONS---
        row7 = ttk.Frame(self.sf)
        row7.pack(fill=X, pady=30)
        row7.columnconfigure(0, weight=1)
        row7.columnconfigure(1, weight=0)
        row7.columnconfigure(2, weight=0)
        row7.columnconfigure(3, weight=1)
        self.validate_btn = ttk.Button(row7, text=self._("VALIDATE-BTN"), bootstyle='primary', command=self.onValidate,
                                       width=20)
        self.validate_btn.grid(column=0, row=0, padx=(200, 10))
        self.create_nb_btn = ttk.Button(row7, text=self._("CREATE-NOTEBOOK-BTN"), bootstyle='secondary',
                                        command=lambda: self.onCreateNotebook(_),
                                        width=20, state='disable')
        self.create_nb_btn.grid(column=1, row=0, padx=(10, 0))
        # ---TOOLTIPS---
        if not self.config['ignore_tooltips']:
            self.tooltips()

    def tooltips(self):
        delay = 700
        wraplenght = 700
        ToolTip(self.output_name, text=self._("output_name_tooltip"), delay=delay, wraplength=wraplenght)
        ToolTip(self.output_folder, text=self._("output_folder_tooltip"), delay=delay, wraplength=wraplenght)
        ToolTip(self.init_file, text=self._("init_file_tooltip"), delay=delay, wraplength=wraplenght)
        ToolTip(self.dftype_cb, text=self._("dftype_cb_tooltip"), delay=delay, wraplength=wraplenght)
        ToolTip(self.file_separator_str, text=self._("file_separator_str_tooltip"), delay=delay, wraplength=wraplenght)
        ToolTip(self.target_feature, text=self._("target_column_tooltip"), delay=delay, wraplength=wraplenght)
        ToolTip(self.feature_names, text=self._("feature_names_tooltip"), delay=delay, wraplength=wraplenght)
        ToolTip(self.enable_resume, text=self._("enable_resume_tooltip"), delay=delay, wraplength=wraplenght)
        ToolTip(self.enable_preprocessing, text=self._("enable_preprocessing_tooltip"), delay=delay,
                wraplength=wraplenght)
        ToolTip(self.enable_negative_data, text=self._("enable_negative_data_tooltip"), delay=delay,
                wraplength=wraplenght)
        ToolTip(self.negative_feature_names, text=self._("negative_feature_names_tooltip"), delay=delay,
                wraplength=wraplenght)
        ToolTip(self.enable_feature_selection, text=self._("enable_feature_selection_tooltip"), delay=delay,
                wraplength=wraplenght)
        ToolTip(self.enable_multinotebook, text=self._("enable_multinotebook_tooltip"), delay=delay,
                wraplength=wraplenght)
        ToolTip(self.enable_prediction, text=self._("enable_prediction_tooltip"), delay=delay, wraplength=wraplenght)

    def predictionSettings(self, frame):
        self.predict_params = {}
        self.param_vars = {}

        for alg in ML_ALGORITHMS:
            alg_name = alg['name']
            row = ttk.Frame(frame)
            row.pack(fill=X, pady=30)

            alg_val = ttk.BooleanVar(value=False)
            enable_params_frame = ttk.Frame(row)
            self.param_vars[alg_name] = {}

            def toggle_alg(a=alg_name, v=alg_val, f=enable_params_frame):
                self.toggle_enable_cb_options(v, f, 1)
                if v.get():
                    self.predict_params[a] = {}
                    for pname, info in self.param_vars[a].items():
                        self.predict_params[a][pname] = str(info["var"].get())
                else:
                    self.predict_params.pop(a, None)

            enable_alg = ttk.Checkbutton(
                row,
                text=alg_name,
                variable=alg_val,
                command=toggle_alg
            )
            enable_alg.grid(row=0, column=0, padx=(5, 0), pady=5, sticky="w")

            for x, param in enumerate(alg['parameters']):
                param_name = param['back_name']
                ttk.Label(enable_params_frame, text=param['show_name']).grid(
                    row=0, column=x * 2, padx=10, pady=5, sticky='w'
                )

                match param['option_type']:
                    case 'combobox':
                        var = ttk.StringVar(value=param['options'][param['default']])
                        combobox = ttk.Combobox(
                            enable_params_frame,
                            values=param['options'],
                            textvariable=var,
                            state="readonly",
                            font=('Helvetica', self.font_size)
                        )
                        combobox.grid(row=0, column=x * 2 + 1, padx=10, pady=5)

                        def on_combo(event=None, a=alg_name, p=param_name, v=var, enabled=alg_val):
                            if enabled.get():
                                self.predict_params.setdefault(a, {})
                                self.predict_params[a][p] = str(v.get())

                        combobox.bind("<<ComboboxSelected>>", on_combo)
                        combobox.current(param['default'])

                        self.param_vars[alg_name][param_name] = {"var": var, "widget": str(combobox)}

                    case 'incremental':
                        var = ttk.StringVar(value=str(param['default']))
                        spinbox = ttk.Spinbox(
                            enable_params_frame,
                            from_=param['options'][0],
                            to=param['options'][1],
                            increment=param['options'][2],
                            bootstyle="success",
                            textvariable=var
                        )
                        spinbox.grid(row=0, column=x * 2 + 1, padx=10, pady=5)
                        spinbox.set(param['default'])

                        def on_spin(a=alg_name, p=param_name, v=var, enabled=alg_val):
                            if enabled.get():
                                self.predict_params.setdefault(a, {})
                                self.predict_params[a][p] = str(v.get())

                        spinbox.configure(command=on_spin)
                        self.param_vars[alg_name][param_name] = {"var": var, "widget": str(spinbox)}

                    case 'range':
                        var = ttk.DoubleVar(value=float(param['default']))
                        scale = ttk.Scale(
                            enable_params_frame,
                            from_=param['options'][0],
                            to=param['options'][1],
                            orient="horizontal",
                            bootstyle="info",
                            length=200
                        )
                        scale.grid(row=0, column=x * 2 + 1, padx=10, pady=5)
                        scale.set(param['default'])

                        def on_scale(value, a=alg_name, p=param_name, v=var, enabled=alg_val):
                            v.set(float(value))
                            if enabled.get():
                                self.predict_params.setdefault(a, {})
                                self.predict_params[a][p] = str(v.get())

                        scale.configure(command=on_scale)
                        self.param_vars[alg_name][param_name] = {"var": var, "widget": str(int(scale.get()))}

            enable_params_frame.grid(row=1, column=0, columnspan=2, sticky="w", padx=5, pady=5)
            enable_params_frame.grid_forget()

    def describeNormalizingType(self, event=None):
        text = ''
        match self.normalize_type_cb.get():
            case 'MinMaxScaler':
                text = self._("MinMaxScaler_description")
            case 'StandardScaler':
                text = self._("StandardScaler_description")
            case 'Normalizer':
                text = self._("Normalizer_description")
        self.describe_normalizing_type_lbl.config(text=text)

    def onCreateNotebook(self, _):
        answer = None
        self.onValidate()
        if not self.ignore_warnings:
            match self.create_btn_style:
                case 'warning':
                    answer = Messagebox.yesno(
                        self._("warning_msg"),
                        self._("confirm_txt_msgbox"))
                case 'danger':
                    answer = Messagebox.yesno(
                        self._("danger_msg"),
                        self._("confirm_txt_msgbox"))

            if (answer == 'Yes' or answer == 'Sí') or self.create_btn_style == 'success':
                response = onCreate(self, _)
                self.showResponseMsg(response)
        else:
            response = onCreate(self, _)
            self.showResponseMsg(response)

    def showResponseMsg(self, response):
        if True in response:
            Messagebox.show_info(response[True], self._("success_msg_msgbox"))
        else:
            Messagebox.show_error(response[False], self._("error_msg_msgbox"))

    def onValidate(self):
        warning_bool = not self.output_name.get() or self.output_name.get().strip() == '' or not self.output_folder.get() or self.output_folder.get().strip() == ''
        warning2_bool = self.negative_data_val.get() and (
                not self.negative_feature_names.get() or self.negative_feature_names.get().strip() == '')
        danger1_bool = not self.init_file.get() or self.init_file.get().strip() == '' or not self.file_separator_str.get() or self.file_separator_str.get().strip() == ''
        danger2_bool = not self.feature_names.get() or self.feature_names.get().strip() == '' or not self.target_feature.get() or self.target_feature.get().strip() == ''

        if warning_bool:
            self.change_separator(self.separator1, 'warning')
        else:
            self.change_separator(self.separator1, 'success')

        if warning2_bool:
            self.change_separator(self.separator4, 'warning')
        else:
            self.change_separator(self.separator4, 'success')

        if danger1_bool:
            self.change_separator(self.separator2, 'danger')
        else:
            self.change_separator(self.separator2, 'success')

        if danger2_bool:
            self.change_separator(self.separator3, 'danger')
        else:
            self.change_separator(self.separator3, 'success')

        if (warning2_bool or warning_bool) and (not danger1_bool and not danger2_bool):
            self.changeStyleCreateNotebookBtn('warning')
            self.create_btn_style = 'warning'
        elif danger1_bool or danger2_bool:
            self.changeStyleCreateNotebookBtn('danger')
            self.create_btn_style = 'danger'
        elif not (warning_bool and danger1_bool and danger2_bool):
            self.changeStyleCreateNotebookBtn('success')
            self.create_btn_style = 'success'
        else:
            self.changeStyleCreateNotebookBtn('secondary')
            self.create_btn_style = 'secondary'

    def changeStyleCreateNotebookBtn(self, style):
        self.create_nb_btn.configure(bootstyle=style)
        if style == 'secondary':
            self.create_nb_btn.configure(state='disabled')
        else:
            self.create_nb_btn.configure(state='enable')

    def topButtonBar(self):
        rowX = ttk.Frame(self.buttonbar, bootstyle='dark')
        rowX.pack(side=TOP, fill=X, expand=YES)

        # ---MENU 1---
        menu1 = ttk.Menubutton(rowX, text=self._("barmenu_options_menu"), bootstyle='dark')
        menu1.grid(row=0, column=0, sticky='w')
        submenu1 = ttk.Menu(menu1, tearoff=0)
        submenu1.add_command(label=self._("barmenu_config_submenu"),
                             command=lambda: configurationWindow(translator=self._, config=self.config),
                             font=('Segoe UI', self.font_size - 1))
        submenu1.add_command(label="---------------", font=('Segoe UI', self.font_size - 1), state="disabled")
        submenu1.add_command(label="Salir", command=lambda: self.root.quit(), font=('Segoe UI', self.font_size - 1))
        menu1["menu"] = submenu1

        # ---MENU 2---
        menu2 = ttk.Menubutton(rowX, text=self._("barmenu_help_menu"), bootstyle='dark')
        menu2.grid(row=0, column=1, sticky='w')
        submenu2 = ttk.Menu(menu2, tearoff=0)
        submenu2.add_command(label=self._("barmenu_help_submenu"), command=self.openDocumentation,
                             font=('Segoe UI', self.font_size - 1))
        submenu2.add_command(label=self._("barmenu_about_submenu"), command=self.showAbout,
                             font=('Segoe UI', self.font_size - 1))
        submenu2.add_command(label=self._("barmenu_version_submenu"), command=self.on_check_update,
                             font=('Segoe UI', self.font_size - 1))
        menu2["menu"] = submenu2

    def openDocumentation(self):
        url = "https://github.com/raulRT-99/notbeook_generator/wiki"
        webbrowser.open(url)

    def get_local_version(self):
        version_file = Path('./Config/VERSION')
        return version_file.read_text(encoding="utf-8").strip()

    def get_remote_version(self):
        url = "https://raw.githubusercontent.com/raulRT-99/notbeook_generator/refs/heads/in-progress/src/notebook_generator/Config/VERSION"
        resp = requests.get(url, timeout=5)
        resp.raise_for_status()
        return resp.text.strip()

    def is_update_available(self):
        local = self.get_local_version()
        remote = self.get_remote_version()
        return local != remote, remote

    def on_check_update(self):
        try:
            available, version = self.is_update_available()
            if available:
                answer = Messagebox.yesno(self._("AVAILABLE-VERSION-TXT") % {"version": version}, self._("AVAILABLE-VERSION-TITLE-TXT"))
                if answer == "Yes"  or answer == "Sí":
                    self.goToRepository()
            else:
                Messagebox.show_info(self._("UPDATED-VERSION-TXT"), self._("UPDATED-VERSION-TITLE-TXT"))
        except Exception as e:
            Messagebox.show_error(self._("UPDATE-VERSION-ERROR") % {"error":e}, "ERROR")

    def showAbout(self):
        msg = Messagebox.okcancel(
            "Version: " + self.get_local_version() + "\n\n" + self._("showAbout_txt"), self._("barmenu_about_submenu"))
        if msg == 'OK':
            self.goToRepository()

    def goToRepository(self):
        url = "https://github.com/raulRT-99/notbeook_generator"
        webbrowser.open(url)

    def create_path_row(self, type):
        if type == 'directory':
            output_path_row = ttk.Frame(self.select_folder_lbl)
            output_path_row.grid(row=0, column=0, sticky="ew")
            path_lbl = ttk.Label(output_path_row,
                                 text=self._("select_folder_lbl"),
                                 width=15)
            path_lbl.grid(row=0, column=0, padx=(0, 10), pady=5, sticky="w")
            self.output_folder = ttk.Entry(output_path_row, textvariable=self.output_path_var, width=50,
                                           font=('Helvetica', self.font_size))
            self.output_folder.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
            browse_btn = ttk.Button(
                output_path_row,
                text=self._("browse_txt"),
                command=lambda: self.on_browse(type),
                width=self.font_size
            )
            browse_btn.grid(row=0, column=2, padx=5, pady=5, sticky="w")
            output_path_row.columnconfigure(1, weight=1)
        else:
            file_path_row = ttk.Frame(self.select_file_lbl)
            file_path_row.grid(row=0, column=0, sticky="ew")
            path_lbl = ttk.Label(file_path_row,
                                 text=self._("select_file_lbl"),
                                 width=20,
                                 wraplength=200 + len(self._("select_file_lbl")))
            path_lbl.grid(row=0, column=0, padx=(0, 10), pady=5, sticky="w")
            self.init_file = ttk.Entry(file_path_row, textvariable=self.file_path_var, width=50,
                                       font=('Helvetica', self.font_size))
            self.init_file.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
            browse_btn = ttk.Button(
                file_path_row,
                text=self._("browse_txt"),
                command=lambda: self.on_browse(type),
                width=self.font_size
            )
            browse_btn.grid(row=0, column=2, padx=5, pady=5, sticky="w")
            file_path_row.columnconfigure(1, weight=1)

    def on_browse(self, type):
        if type == 'directory':
            path = askdirectory(title=self._("browse_directory_txt"))
            self.output_path_var.set(path)
        else:
            path = askopenfilename(
                title=self._("browse_file_txt"),
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
            )
            self.file_path_var.set(path)

    def run(self):
        self.sf.mainloop()

    def change_separator(self, separator, type):
        separator.configure(bootstyle=type)

    def toggle_enable_cb_options(self, boolean_value_cb, options_frame, row):
        if boolean_value_cb.get():
            options_frame.grid(row=row, column=0, sticky="ew", pady=10)
        else:
            options_frame.grid_forget()


if __name__ == "__main__":
    app = MainWindow(_=_)
    app.run()
