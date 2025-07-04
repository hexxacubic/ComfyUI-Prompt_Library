from .Prompt_Library import Prompt_Library
from .Simple_Prompt_Library import Simple_Prompt_Library
from .Prompt_Extender import Prompt_Extender
from .Double_Prompt_Encode import Double_Prompt_Encode
from .Multi_Wildcard_Loader import Multi_Wildcard_Loader

NODE_CLASS_MAPPINGS = {
    "Prompt_Library": Prompt_Library,
    "Simple_Prompt_Library": Simple_Prompt_Library,
    "Prompt_Extender": Prompt_Extender,
    "Double_Prompt_Encode": Double_Prompt_Encode,
    "Multi_Wildcard_Loader": Multi_Wildcard_Loader,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "Prompt_Library": "Prompt Library",
    "Simple_Prompt_Library": "Simple Prompt Library",
    "Prompt_Extender": "Prompt Extender",
    "Double_Prompt_Encode": "Double Prompt Encode",
    "Multi_Wildcard_Loader": "Multi Wildcard Loader",
}
