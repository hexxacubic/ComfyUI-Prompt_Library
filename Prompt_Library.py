import os
import folder_paths

class Prompt_Library:
    """
    • Category dropdown: lists all folders under /models/prompts/
    • Project dropdown: lists files in selected category (empty until category chosen)
    • Index dropdown: lists only indices (###N) present in selected project file
    • File reloaded on each get_prompt call to reflect external changes
    """

    def __init__(self):
        self.base_dir = os.path.join(folder_paths.models_dir, "prompts")

    @classmethod
    def INPUT_TYPES(s):
        base = os.path.join(folder_paths.models_dir, "prompts")
        # allow empty selection + all folder names
        cats = [""] + sorted([d for d in os.listdir(base) if os.path.isdir(os.path.join(base, d))])
        return {
            "required": {
                "category": (cats,),
                "project":  ([],),
                "index":    ([],),
            },
            "callbacks": {
                "on_ui_set": {
                    "category": "cb_category",
                    "project":  "cb_project",
                }
            }
        }

    RETURN_TYPES = ("STRING", "STRING", "STRING", "INT")
    FUNCTION     = "get_prompt"
    OUTPUT_NODE  = True
    CATEGORY     = "hexxacubic"

    @classmethod
    def cb_category(cls, category):
        # reset project list & clear index when category changes
        base = os.path.join(folder_paths.models_dir, "prompts")
        if not category:
            projs = []
        else:
            folder = os.path.join(base, category)
            projs = sorted(f[:-4] for f in os.listdir(folder) if f.lower().endswith(".txt"))
        return {"project": projs, "index": []}

    @classmethod
    def cb_project(cls, category, project):
        # build index list from ### entries in the selected file
        base = os.path.join(folder_paths.models_dir, "prompts")
        path = os.path.join(base, category, project + ".txt")
        indices = []
        if os.path.isfile(path):
            with open(path, encoding="utf-8") as f:
                for line in f:
                    if line.startswith("###"):
                        try:
                            idx = int(line[3:])
                            if idx not in indices:
                                indices.append(idx)
                        except:
                            pass
            indices.sort()
        return {"index": indices}

    def get_prompt(self, category, project, index):
        # reload file on each call
        path = os.path.join(self.base_dir, category, project + ".txt")
        if not os.path.isfile(path):
            return ("", "", category, index)

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

        return (pos, neg, category, index)


NODE_CLASS_MAPPINGS = {
    "Prompt_Library": Prompt_Library,
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "Prompt Library": "Prompt_Library",
}
