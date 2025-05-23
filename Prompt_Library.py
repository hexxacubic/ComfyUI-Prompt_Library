import os
import folder_paths

class Prompt_Library:
    """
    • project dropdown: '<category>/<project>' choices at init
    • index slider: free int from 1 to 99 (no dynamic cap)
    • file reloaded every get_prompt
    """

    def __init__(self):
        self.base = os.path.join(folder_paths.models_dir, "prompts")

    @classmethod
    def INPUT_TYPES(s):
        base = os.path.join(folder_paths.models_dir, "prompts")
        # build combined list at node-load
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
                "project": (proj_choices,),
                "index":   ("INT", {"default": 1, "min": 1, "max": 99}),
            }
        }

    RETURN_TYPES = ("STRING","STRING","STRING","INT")
    FUNCTION     = "get_prompt"
    OUTPUT_NODE  = True
    CATEGORY     = "hexxacubic"

    def get_prompt(self, project, index):
        # project = "category/name"
        try:
            cat, name = project.split("/", 1)
        except ValueError:
            return ("", "", project, index)

        path = os.path.join(self.base, cat, name + ".txt")
        if not os.path.isfile(path):
            return ("", "", project, index)

        sections = {}
        current = None
        with open(path, encoding="utf-8") as f:
            for raw in f:
                line = raw.rstrip("\n")
                if line.startswith("###"):
                    try:
                        num = int(line[3:])
                        current = num
                        sections[current] = []
                    except:
                        current = None
                elif current is not None:
                    sections[current].append(line)

        lines = sections.get(index, [])
        if '---' in lines:
            sep = lines.index('---')
            pos = "\n".join(lines[:sep]).strip()
            neg = "\n".join(lines[sep+1:]).strip()
        else:
            pos = "\n".join(lines).strip()
            neg = ""

        return (pos, neg, project, index)


NODE_CLASS_MAPPINGS = {"Prompt_Library": Prompt_Library}
NODE_DISPLAY_NAME_MAPPINGS = {"Prompt Library": "Prompt_Library"}
