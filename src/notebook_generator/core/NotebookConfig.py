from dataclasses import dataclass, field

@dataclass
class NotebookConfig:
    target_column:str = ""
    feature_columns: list[str] = field(default_factory=list)
    separator:str = ""
    #'\s+'
    #number of plots to show in describing data (0-4)
    resume_plots:int = 3
    #classification, regression
    type:str = ""
    #MinMaxScaler, StandardScaler, Normalizer
    normalizer:str = ""
    #features to be normalizer that have negative data, None = there is no negative data
    normalize_negative_data: list[str] = field(default_factory=list)



