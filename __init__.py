from .Prompt_Library import Prompt_Library
from .Random_Project import Random_Project
from .Simple_Prompt_Library import Simple_Prompt_Library

NODE_CLASS_MAPPINGS = {
    "Prompt_Library": Prompt_Library,
    "Random_Project": Random_Project,
    "Simple_Prompt_Library": Simple_Prompt_Library,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "Prompt_Library": "Prompt Library",
    "Random_Project": "Random Project",
    "Simple_Prompt_Library": "Simple Prompt Library",
}
