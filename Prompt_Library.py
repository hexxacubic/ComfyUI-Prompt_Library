import os
import folder_paths

class Prompt_Library:
    """
    • Category dropdown: lists all folders under /models/prompts/
    • Project dropdown: lists .txt files based on selected category or all if none selected
    • Index dropdown: lists only indices (###N) present in the selected file
    • File is reloaded on each get_prompt call to reflect external changes
    """

    def __init__(self):
        self.base_dir = os.path.join(folder_paths.models_dir, "prompts")

    @classmethod
    def INPUT_TYPES(s):
        base = os.path.join(folder_paths.models_dir, "prompts")
        # find all categories
        cats = [d for d in os.listdir(base) if os.path.isdir(os.path.join(base, d))]
        # initial project list (all projects)
        projs = []
        for cat in cats:
            folder = os.path.join(base, cat)
            for f in os.listdir(folder):
                if f.lower().endswith(".txt"):
                    projs.append(f[:-4])
        return {
            "required": {
                "category": (cats,),
                "project":  (projs,),
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
        """Update project list and clear index when category changes"""
        base = os.path.join(folder_paths.models_dir, "prompts")
        if not category:
            # no category selected: include all projects
            projs = []
            for cat in os.listdir(base):
                path = os.path.join(base, cat)
                if os.path.isdir(path):
                    for f in os.listdir(path):
                        if f.lower().endswith(".txt"):
                            projs.append(f[:-4])
        else:
            # projects from selected category only
            folder = os.path.join(base, category)
            projs = [f[:-4] for f in os.listdir(folder) if f.lower().endswith(".txt")]
        return {"project": projs, "index": []}

    @classmethod
    def cb_project(cls, category, project):
        """Generate index list from '###' entries in the selected file"""
        base = os.path.join(folder_paths.models_dir, "prompts")
        path = os.path.join(base, category or "", project + ".txt")
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
        path = os.path.join(self.base_dir, category or "", project + ".txt")
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
