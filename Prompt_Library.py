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
        # list all subfolders under models/prompts
        cats = []
        if os.path.isdir(os.path.join(folder_paths.models_dir, "prompts")):
            for d in os.listdir(os.path.join(folder_paths.models_dir, "prompts")):
                full = os.path.join(folder_paths.models_dir, "prompts", d)
                if os.path.isdir(full):
                    cats.append(d)

        return {
            "required": {
                "category": ("STRING", {"default": cats[0] if cats else ""}),
                "project":  ("STRING", {"default": ""}),      # just name, no .txt
                "index":    ("INT",    {"default": 1, "min": 1, "max": 99}),
            }
        }

    RETURN_TYPES = ("STRING", "STRING", "STRING", "INT")
    FUNCTION     = "get_prompt"
    OUTPUT_NODE  = True
    CATEGORY     = "prompt"

    def get_prompt(self, category, project, index):
        # build path
        folder = os.path.join(self.base_dir, category)
        path   = os.path.join(folder, project + ".txt")

        if not os.path.isfile(path):
            # missing file → empty outputs
            return ("", "", category, index)

        # parse “###N” sections and “---” separator
        projects = {}
        current  = None
        with open(path, encoding="utf-8") as f:
            for raw in f:
                line = raw.rstrip("\n")
                if line.startswith("###"):
                    try:
                        num = int(line[3:])
                    except:
                        current = None
                    else:
                        current = num
                        projects[current] = []
                elif current is not None:
                    projects[current].append(line)

        lines = projects.get(index, [])
        # split at ‘---’
        if '---' in lines:
            sep = lines.index('---')
            pos = "\n".join(lines[:sep]).strip()
            neg = "\n".join(lines[sep+1:]).strip()
        else:
            pos = "\n".join(lines).strip()
            neg = ""

        return (pos, neg, category, index)


# node registration
NODE_CLASS_MAPPINGS = {
    "Prompt_Library": Prompt_Library,
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "Prompt Library": "Prompt_Library",
}
