import os
import re
import time
import random
import sys
import subprocess
import folder_paths


class Prompt_Library:
    """
    Prompt Library - File-based prompt management

    • project: Select prompt file from dropdown
    • index: Choose prompt project within file (1-999)
    • randomize_index: When enabled, index is randomly selected

    File Syntax:
    - Empty lines separate projects
    - A separator made of 3 or more hyphens splits positive/negative prompts
    - The separator may appear anywhere in the text, not only on its own line
    - ### at line start marks comments/notes (will be ignored)

    Outputs:
    - double_prompt
    - positive_prompt
    - negative_prompt
    """

    def __init__(self):
        self.base = os.path.join(folder_paths.models_dir, "prompts")
        self.refresh_projects()

    def refresh_projects(self):
        base = self.base
        if not os.path.exists(base):
            os.makedirs(base)

        cats = [d for d in os.listdir(base) if os.path.isdir(os.path.join(base, d))]
        proj_choices = []

        for cat in sorted(cats):
            folder = os.path.join(base, cat)
            for fn in sorted(os.listdir(folder)):
                if fn.lower().endswith(".txt"):
                    name = fn[:-4]
                    proj_choices.append(f"{cat}/{name}")

        self._proj_choices = proj_choices if proj_choices else ["No projects found"]

    def load_file_content(self, project):
        try:
            category, name = project.split("/", 1)
            path = os.path.join(self.base, category, name + ".txt")
            if os.path.isfile(path):
                with open(path, encoding="utf-8") as f:
                    return f.read()
        except Exception:
            pass
        return ""

    @staticmethod
    def split_positive_negative(section_text):
        match = re.search(r"-{3,}", section_text)
        if not match:
            pos = section_text.strip()
            neg = ""
            return pos, neg

        pos = section_text[:match.start()].strip()
        neg = section_text[match.end():].strip()
        return pos, neg

    @classmethod
    def INPUT_TYPES(cls):
        instance = cls()
        instance.refresh_projects()

        return {
            "required": {
                "project": (instance._proj_choices,),
                "index": ("INT", {"default": 1, "min": 1, "max": 999}),
                "randomize_index": ("BOOLEAN", {"default": False}),
                "random_seed": ("INT", {"default": -1, "min": -1, "max": 0xffffffffffffffff}),
            }
        }

    RETURN_TYPES = ("STRING", "STRING", "STRING")
    RETURN_NAMES = ("double_prompt", "positive_prompt", "negative_prompt")
    FUNCTION = "get_prompt"
    OUTPUT_NODE = True
    CATEGORY = "hexxacubic"

    @staticmethod
    def ui_open_prompts_folder():
        base = os.path.join(folder_paths.models_dir, "prompts")
        if sys.platform == "win32":
            os.startfile(base)
        elif sys.platform == "darwin":
            subprocess.Popen(["open", base])
        else:
            subprocess.Popen(["xdg-open", base])
        return "Prompts folder opened."

    def ui_refresh_projects(self):
        self.refresh_projects()
        return "Project list refreshed."

    @classmethod
    def UI_BUTTONS(cls):
        return [
            {"label": "📁 Prompts Folder", "method": "ui_open_prompts_folder"},
            {"label": "🔄 Refresh List", "method": "ui_refresh_projects"},
        ]

    def get_prompt(self, project, index, randomize_index, random_seed):
        self.refresh_projects()

        if project == "No projects found":
            return ("", "", "")

        file_content = self.load_file_content(project)
        if not file_content.strip():
            return ("", "", "")

        sections = []
        current_lines = []

        for line in file_content.splitlines():
            if line.strip().startswith("###"):
                continue

            if not line.strip():
                if current_lines:
                    sections.append("\n".join(current_lines).strip())
                    current_lines = []
            else:
                current_lines.append(line)

        if current_lines:
            sections.append("\n".join(current_lines).strip())

        if not sections:
            return ("", "", "")

        available_indices = list(range(1, len(sections) + 1))

        if randomize_index:
            actual_seed = int(time.time() * 1000000) % 0xffffffffffffffff if random_seed == -1 else random_seed
            gen = random.Random(actual_seed)
            used_idx = gen.choice(available_indices)
        else:
            used_idx = available_indices[(index - 1) % len(available_indices)]

        section_text = sections[used_idx - 1]
        pos, neg = self.split_positive_negative(section_text)

        if pos and neg:
            double_prompt = f"{pos}\n---\n{neg}"
        elif pos:
            double_prompt = pos
        elif neg:
            double_prompt = f"\n---\n{neg}"
        else:
            double_prompt = ""

        return (double_prompt, pos, neg)

    @classmethod
    def IS_CHANGED(cls, project, index, randomize_index, random_seed):
        if randomize_index:
            return float("nan")
        return hash((project, index, random_seed))
