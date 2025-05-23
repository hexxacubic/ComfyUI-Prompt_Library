import os
import folder_paths

class Prompt_Library:
    """
    ComfyUI node that lets you pick:
      • a category (folder under models/prompts/)
      • a project file (TXT under that folder, suffix .txt omitted in UI)
      • an index (based on actual ### markers in file)
    Outputs: pos_prompt, neg_prompt, category_name, index
    """

    def __init__(self):
        self.base_dir = os.path.join(folder_paths.models_dir, "prompts")

    @classmethod
    def INPUT_TYPES(cls):
        base = os.path.join(folder_paths.models_dir, "prompts")
        cats = []
        projects = []

        if os.path.isdir(base):
            for d in os.listdir(base):
                full_path = os.path.join(base, d)
                if os.path.isdir(full_path):
                    cats.append(d)
                    for f in os.listdir(full_path):
                        if f.lower().endswith(".txt"):
                            projects.append(f[:-4])

        return {
            "required": {
                "category": (cats,) if cats else ("",),
                "project": (projects,) if projects else ("",),
                "index": ("INT", {"default": 1, "min": 1, "max": 999}),
            }
        }

    RETURN_TYPES = ("STRING", "STRING", "STRING", "INT")
    FUNCTION = "get_prompt"
    OUTPUT_NODE = True
    CATEGORY = "hexxacubic"

    def get_prompt(self, category, project, index):
        folder = os.path.join(self.base_dir, category)
        path = os.path.join(folder, project + ".txt")

        if not os.path.isfile(path):
            return ("", "", category, index)

        prompts = {}
        current = None

        with open(path, encoding="utf-8") as f:
            for raw in f:
                line = raw.rstrip("\n")
                if line.startswith("###"):
                    try:
                        num = int(line[3:])
                        current = num
                        prompts[current] = []
                    except:
                        current = None
                elif current is not None:
                    prompts[current].append(line)

        if index not in prompts:
            valid_indexes = sorted(prompts.keys())
            next_index = next((i for i in valid_indexes if i > index), None)
            if next_index is None and valid_indexes:
                index = valid_indexes[0]
            elif next_index:
                index = next_index
            else:
                return ("", "", category, index)

        lines = prompts.get(index, [])
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
