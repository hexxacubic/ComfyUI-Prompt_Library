import os
import folder_paths
import random
import sys
import subprocess

class Prompt_Library:
    """
    Prompt Library - File-based prompt management
    • project: Select prompt file from dropdown
    • index: Choose prompt project within file (1-999)
    • randomize_index: When enabled, index is randomly selected
    • global_prompt: Text field for global prompt (applied to all non-first projects)
    • File Syntax: 
      - Empty lines separate projects
      - --- (or ---- or -----) separates positive/negative prompts
      - ### at line start marks comments/notes (will be ignored)
    """

    def __init__(self):
        self.base = os.path.join(folder_paths.models_dir, "prompts")
        self.refresh_projects()

    def refresh_projects(self):
        # Read projects each time
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
        """Load content of selected file"""
        try:
            category, name = project.split("/", 1)
            path = os.path.join(self.base, category, name + ".txt")
            if os.path.isfile(path):
                with open(path, encoding="utf-8") as f:
                    return f.read()
        except:
            pass
        return ""

    @classmethod
    def INPUT_TYPES(s):
        instance = s()
        instance.refresh_projects()
        
        return {
            "required": {
                "project": (instance._proj_choices,),
                "index": ("INT", {"default": 1, "min": 1, "max": 999}),
                "randomize_index": ("BOOLEAN", {"default": False}),
                "global_prompt": ("STRING", {"multiline": True, "default": "high quality, depth of field\n---\nworst quality, ugly"}),
            }
        }

    RETURN_TYPES = ("STRING", "INT")
    RETURN_NAMES = ("double_prompt", "used_index")
    FUNCTION = "get_prompt"
    OUTPUT_NODE = True
    CATEGORY = "hexxacubic"

    # --- BUTTON UI ---
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

    def parse_prompt_text(self, text):
        """Parse text into positive and negative prompts"""
        if not text.strip():
            return "", ""
            
        lines = text.split('\n')
        
        # Find separator (---, ----, or -----)
        separator_idx = -1
        for i, line in enumerate(lines):
            if line.strip() in ["---", "----", "-----"]:
                separator_idx = i
                break
        
        if separator_idx != -1:
            pos = "\n".join(lines[:separator_idx]).strip()
            neg = "\n".join(lines[separator_idx+1:]).strip()
        else:
            pos = text.strip()
            neg = ""
            
        return pos, neg

    def get_prompt(self, project, index, randomize_index, global_prompt):
        # Refresh projects list
        self.refresh_projects()
        
        if project == "No projects found":
            return "", "", index

        # Load file content
        file_content = self.load_file_content(project)
        if not file_content.strip():
            return "", "", index

        # Parse sections - separated by empty lines
        sections = []
        current_lines = []
        
        for line in file_content.split('\n'):
            # Remove lines starting with ### (comments)
            if line.strip().startswith("###"):
                continue
                
            # Check if line is empty
            if not line.strip():
                # Save current section if it has content
                if current_lines:
                    sections.append(current_lines)
                    current_lines = []
            else:
                current_lines.append(line)
        
        # Save last section if present
        if current_lines:
            sections.append(current_lines)

        if not sections:
            return "", "", index

        # All sections are projects (1 to n)
        available_indices = list(range(1, len(sections) + 1))
        
        # Choose final index
        if randomize_index:
            used_idx = random.choice(available_indices)
        else:
            if index in available_indices:
                used_idx = index
            else:
                # Wrapping with modulo
                used_idx = available_indices[(index - 1) % len(available_indices)]

        # Extract prompts from chosen section
        section_idx = used_idx - 1  # Convert to 0-based
        lines = sections[section_idx]
        
        # Find separator in section
        separator_idx = -1
        for i, line in enumerate(lines):
            if line.strip() in ["---", "----", "-----"]:
                separator_idx = i
                break
        
        if separator_idx != -1:
            pos = "\n".join(lines[:separator_idx]).strip()
            neg = "\n".join(lines[separator_idx+1:]).strip()
        else:
            pos = "\n".join(lines).strip()
            neg = ""

        # Apply global prompt from text field (but not to first project)
        if global_prompt.strip() and used_idx > 1:
            global_pos, global_neg = self.parse_prompt_text(global_prompt)
            
            # Prepend global prompts with comma
            if global_pos:
                pos = global_pos + ", " + pos if pos else global_pos
            if global_neg:
                neg = global_neg + ", " + neg if neg else global_neg

        return pos, neg, used_idx

    @classmethod
    def IS_CHANGED(s, project, index, randomize_index, global_prompt):
        # Always mark as changed when randomize is enabled
        if randomize_index:
            return float("nan")
        return hash(project + str(index) + global_prompt)