import os
import folder_paths

class Prompt_Library:
    """
    ComfyUI node that lets you pick:
      • a category (folder under models/prompts/)
      • a project file (TXT under that folder, suffix .txt omitted in UI)
      • an index (1–99)
    and then parses that file for the positive vs. negative prompt.
    Outputs: pos_prompt, neg_prompt, category_name, index
    """

    def __init__(self):
        # base dir for your prompt libraries
        self.base_dir = os.path.join(folder_paths.models_dir, "prompts")

    @classmethod
    def INPUT_TYPES(s):
        base = os.path.join(folder_paths.models_dir, "prompts")
        # alle Kategorien ermitteln
        cats = []
        if os.path.isdir(base):
            for d in os.listdir(base):
                if os.path.isdir(os.path.join(base, d)):
                    cats.append(d)
        # alle Projekte (TXT-Dateien) aus allen Kategorien sammeln
        projects = []
        for cat in cats:
            folder = os.path.join(base, cat)
            for f in os.listdir(folder):
                if f.lower().endswith(".txt"):
                    projects.append(f[:-4])
        return {
            "required": {
                "category": (
                    "STRING", {
                        "default": cats[0] if cats else "",
                        "choices": cats
                    }
                ),
                "project": (
                    "STRING", {
                        "default": projects[0] if projects else "",
                        "choices": projects
                    }
                ),
                "index": (
                    "INT", {
                        "default": 1,
                        "min": 1,
                        "max": 99
                    }
                ),
            }
        }

    RETURN_TYPES = ("STRING", "STRING", "STRING", "INT")
    FUNCTION     = "get_prompt"
    OUTPUT_NODE  = True
    CATEGORY     = "hexxacubic"

    def get_prompt(self, category, project, index):
        folder = os.path.join(self.base_dir, category)
        path   = os.path.join(folder, project + ".txt")
        if not os.path.isfile(path):
            return ("", "", category, index)

        projects = {}
        current  = None
        with open(path, encoding="utf-8") as f:
            for raw in f:
                line = raw.rstrip("\n")
                if line.startswith("###"):
                    try:
                        num = int(line[3:])
                        current = num
                        projects[current] = []
                    except:
                        current = None
                elif current is not None:
                    projects[current].append(line)

        lines = projects.get(index, [])
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
