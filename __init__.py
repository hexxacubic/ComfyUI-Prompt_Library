from .Simple_Prompt_Library import Simple_Prompt_Library
from .Prompt_Extender import Prompt_Extender
from .Double_Prompt_Encode import Double_Prompt_Encode
from .Five_Random_Lines import FiveRandomLinesNode
from .Random_Line import RandomLineNode
from .Prompt_Library import Prompt_Library

NODE_CLASS_MAPPINGS = {
    "Simple_Prompt_Library": Simple_Prompt_Library,
    "Prompt_Extender": Prompt_Extender,
    "Double_Prompt_Encode": Double_Prompt_Encode,
    "FiveRandomLines": FiveRandomLinesNode,
    "RandomLine": RandomLineNode,
    "Prompt_Library": Prompt_Library,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "Simple_Prompt_Library": "Simple Prompt Library",
    "Prompt_Extender": "Prompt Extender",
    "Double_Prompt_Encode": "Double Prompt Encode",
    "FiveRandomLines": "Five Random Lines",
    "RandomLine": "Random Line",
    "Prompt_Library": "Prompt Library",
}

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]
