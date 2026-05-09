from .Simple_Prompt_Library import Simple_Prompt_Library
from .Prompt_Extender import Prompt_Extender
from .Double_Prompt_Encode import Double_Prompt_Encode
from .Five_Random_Lines import FiveRandomLinesNode
from .Random_Line import RandomLineNode

NODE_CLASS_MAPPINGS = {
   "Simple_Prompt_Library": Simple_Prompt_Library,
   "Prompt_Extender": Prompt_Extender,
   "Double_Prompt_Encode": Double_Prompt_Encode,
   "FiveRandomLines": FiveRandomLinesNode,
   "RandomLine": RandomLineNode,

}

NODE_DISPLAY_NAME_MAPPINGS = {
   "Simple_Prompt_Library": "Simple Prompt Library",
   "Prompt_Extender": "Prompt Extender",
   "Double_Prompt_Encode": "Double Prompt Encode",
   "FiveRandomLinesNode": "Five Random Lines",
   "RandomLine": "Random Line",

}

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']
