from dataclasses import dataclass, field

@dataclass
class NotebookConfig:
    target_column:str = ""
    feature_columns: list[str] = field(default_factory=list)
    #number of plots to show in describing data (0-3)
    resume_plots:int = 3
    algorithms: list[str] = field(default_factory=list)
    type:str = ""

