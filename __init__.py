from .Prompt_Library import Prompt_Library
from .Simple_Prompt_Library import Simple_Prompt_Library
from .Prompt_Extender import Prompt_Extender
from .Double_Prompt_Encode import Double_Prompt_Encode
from .Multi_Wildcard_Loader import Multi_Wildcard_Loader
from .Random_Line import RandomLineNode
from .Parameter_Animation import ParameterAnimationNode
from .Five_Random_Lines import FiveRandomLinesNode
from .Twelve_Random_Lines import TwelveRandomLinesNode
from .text_save import TextSaveNode

NODE_CLASS_MAPPINGS = {
   "Prompt_Library": Prompt_Library,
   "Simple_Prompt_Library": Simple_Prompt_Library,
   "Prompt_Extender": Prompt_Extender,
   "Double_Prompt_Encode": Double_Prompt_Encode,
   "Multi_Wildcard_Loader": Multi_Wildcard_Loader,
   "RandomLine": RandomLineNode,
   "ParameterAnimation": ParameterAnimationNode,
   "FiveRandomLines": FiveRandomLinesNode,
   "TwelveRandomLines": TwelveRandomLinesNode,
   "TextSave": TextSaveNode,
}

NODE_DISPLAY_NAME_MAPPINGS = {
   "Prompt_Library": "Prompt Library",
   "Simple_Prompt_Library": "Simple Prompt Library",
   "Prompt_Extender": "Prompt Extender",
   "Double_Prompt_Encode": "Double Prompt Encode",
   "Multi_Wildcard_Loader": "Multi Wildcard Loader",
   "RandomLine": "Random Line",
   "ParameterAnimation": "Parameter Animation",
   "FiveRandomLines": "Five Random Lines",
   "TwelveRandomLines": "Twelve Random Lines",
   "TextSave": "Text Save",
}

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']
