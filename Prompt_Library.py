import os
import folder_paths

class Prompt_Library:
    """
    • project dropdown: '<category>/<project>' choices at init
    • index dropdown: only ###N entries in the chosen file
    • file reloaded every get_prompt
    """

    def __init__(self):
        self.base = os.path.join(folder_paths.models_dir, "prompts")

    @classmethod
    def INPUT_TYPES(s):
        # build combined list at node-load
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
                "project": (proj_choices,),
                "index":   ([],),
            },
            "callbacks": {
                "on_ui_set": {
                    "project": "cb_project",
                }
            }
        }

    RETURN_TYPES = ("STRING","STRING","STRING","INT")
    FUNCTION     = "get_prompt"
    OUTPUT_NODE  = True
    CATEGORY     = "hexxacubic"

    @classmethod
    def cb_project(cls, project):
        # project is "category/name"
        cat,name = project.split("/",1)
        path = os.path.join(folder_paths.models_dir, "prompts", cat, name + ".txt")
        idxs = []
        if os.path.isfile(path):
            with open(path, encoding="utf-8") as f:
                for L in f:
                    if L.startswith("###"):
                        try:
                            n = int(L[3:])
                            if n not in idxs: idxs.append(n)
                        except: pass
            idxs.sort()
        return {"index": idxs}

    def get_prompt(self, project, index):
        cat,name = project.split("/",1)
        path = os.path.join(self.base, cat, name + ".txt")
        if not os.path.isfile(path):
            return ("","","",index)
        sections, cur = {}, None
        with open(path, encoding="utf-8") as f:
            for raw in f:
                L = raw.rstrip("\n")
                if L.startswith("###"):
                    try:
                        num = int(L[3:]); cur = num; sections[cur]=[]
                    except: cur=None
                elif cur is not None:
                    sections[cur].append(L)
        lines = sections.get(index, [])
        if '---' in lines:
            s = lines.index('---')
            pos = "\n".join(lines[:s]).strip()
            neg = "\n".join(lines[s+1:]).strip()
        else:
            pos,neg = "\n".join(lines).strip(), ""
        return (pos, neg, project, index)

NODE_CLASS_MAPPINGS = {"Prompt_Library":Prompt_Library}
NODE_DISPLAY_NAME_MAPPINGS = {"Prompt Library":"Prompt_Library"}
