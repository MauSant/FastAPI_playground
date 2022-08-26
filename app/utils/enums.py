from enum import Enum

class LanguageEnum(str,Enum):
    br: str = "Brasil"
    en: str = "Inglês"

    class Config:  
        use_enum_values = True 