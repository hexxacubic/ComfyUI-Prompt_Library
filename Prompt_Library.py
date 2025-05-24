import os
import folder_paths
import random

class Prompt_Library:
    """
    • project dropdown: '<category>/<project>' choices at init  
    • index slider: free int from 1 to 99  
    • randomize flag: integer 0 or 1 to choose random index when 1  
    • file reloaded every get_prompt call to reflect external changes  
    """

    def __init__(self):
        self.base = os.path.join(folder_paths.models_dir, "prompts")

    @classmethod
    def INPUT_TYPES(s):
        base = os.path.join(folder_paths.models_dir, "prompts")
        cats = [d for d in os.listdir(base) if os.path.isdir(os.path.join(base, d))]
        proj_choices = []
        for cat in sorted(cats):
            folder = os.path.join(base, cat)
            for fn in sorted(os.listdir(folder)):
                if fn.lower().endswith(".txt"):
                    name = fn[:-4]
                    proj_choices.append(f"{cat}/{name}")
        return {
            "required": {
                "project":   (proj_choices,),
                "index":     ("INT",  {"default": 1, "min": 1, "max": 99}),
                "randomize": ("INT",  {"default": 0, "min": 0, "max": 1}),
            }
        }

    RETURN_TYPES = ("STRING", "STRING", "STRING", "INT")
    FUNCTION     = "get_prompt"
    OUTPUT_NODE  = True
    CATEGORY     = "hexxacubic"

    def get_prompt(self, project, index, randomize):
        # split 'category/project'
        try:
            category, name = project.split("/", 1)
        except ValueError:
            return "", "", project, index

        path = os.path.join(self.base, category, name + ".txt")
        if not os.path.isfile(path):
            return "", "", project, index

        # parse file sections keyed by '###N'
        sections = {}
        current = None
        with open(path, encoding="utf-8") as f:
            for line in f:
                line = line.rstrip("\n")
                if line.startswith("###"):
                    try:
                        num = int(line[3:])
                        current = num
                        sections[current] = []
                    except:
                        current = None
                elif current is not None:
                    sections[current].append(line)

        # determine final idx via formula
        if sections and randomize in (0, 1):
            max_idx = max(sections.keys())
            idx = randomize * random.randint(1, max_idx) + (1 - randomize) * index
            idx = int(idx)
        else:
            idx = index

        # extract prompts
        lines = sections.get(idx, [])
        if '---' in lines:
            sep = lines.index('---')
            pos = "\n".join(lines[:sep]).strip()
            neg = "\n".join(lines[sep+1:]).strip()
        else:
            pos = "\n".join(lines).strip()
            neg = ""

        return pos, neg, project, idx
