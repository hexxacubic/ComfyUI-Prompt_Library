import os
import folder_paths
import random
import sys
import subprocess

class Prompt_Library:
    """
    • project dropdown: '<category>/<project>' choices at init  
    • index slider: free int from 1 to 99  
    • randomize flag: integer 0 oder 1 für Zufall  
    • editor_content: Textfeld zum Bearbeiten (wird nicht in Projekten gespeichert)
    • "Prompts Folder" Button öffnet den Prompt-Ordner  
    • "Refresh" Button aktualisiert die Liste der Prompt-Dateien  
    • "Load File" Button lädt die ausgewählte Datei ins Textfeld
    • "Save to File" Button speichert Änderungen in die Datei
    """

    def __init__(self):
        self.base = os.path.join(folder_paths.models_dir, "prompts")
        self.refresh_projects()
        self.current_file_path = None
        self.editor_content = ""  # Interner Editor-Inhalt

    def refresh_projects(self):
        # Lese die Projekte jedes Mal neu ein
        base = self.base
        cats = [d for d in os.listdir(base) if os.path.isdir(os.path.join(base, d))]
        proj_choices = []
        for cat in sorted(cats):
            folder = os.path.join(base, cat)
            for fn in sorted(os.listdir(folder)):
                if fn.lower().endswith(".txt"):
                    name = fn[:-4]
                    proj_choices.append(f"{cat}/{name}")
        self._proj_choices = proj_choices

    def load_file_content(self, project):
        """Lädt den Inhalt der ausgewählten Datei"""
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
                "project":   (instance._proj_choices,),
                "index":     ("INT",  {"default": 1, "min": 1, "max": 99}),
                "randomize": ("INT",  {"default": 0, "min": 0, "max": 1}),
                "editor_content": ("STRING", {"multiline": True, "default": "", "dynamicPrompts": False}),
            }
        }

    RETURN_TYPES = ("STRING", "STRING", "STRING", "INT")
    FUNCTION     = "get_prompt"
    OUTPUT_NODE  = True
    CATEGORY     = "hexxacubic"

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
        return "Prompts-Ordner geöffnet."

    def ui_refresh_projects(self):
        self.refresh_projects()
        return "Prompt-Liste aktualisiert."

    def ui_load_file(self, project):
        """Lädt den Inhalt der ausgewählten Datei ins Textfeld"""
        content = self.load_file_content(project)
        self.editor_content = content
        return {"editor_content": content}

    def ui_save_to_file(self, project, editor_content):
        """Speichert den Editor-Inhalt in die ausgewählte Datei"""
        try:
            category, name = project.split("/", 1)
            path = os.path.join(self.base, category, name + ".txt")
            with open(path, "w", encoding="utf-8") as f:
                f.write(editor_content)
            self.editor_content = editor_content
            return f"Gespeichert: {name}.txt"
        except Exception as e:
            return f"Fehler beim Speichern: {str(e)}"

    @classmethod
    def UI_BUTTONS(cls):
        return [
            {"label": "Prompts Folder", "method": "ui_open_prompts_folder"},
            {"label": "Refresh", "method": "ui_refresh_projects"},
            {"label": "Load File", "method": "ui_load_file", "params": ["project"]},
            {"label": "Save to File", "method": "ui_save_to_file", "params": ["project", "editor_content"]},
        ]

    def get_prompt(self, project, index, randomize, editor_content):
        # Nach jedem Render automatisch neu einlesen
        self.refresh_projects()

        # split 'category/project'
        try:
            category, name = project.split("/", 1)
        except ValueError:
            return "", "", project, index

        path = os.path.join(self.base, category, name + ".txt")
        self.current_file_path = path
        
        if not os.path.isfile(path):
            return "", "", project, index

        # Verwende Editor-Inhalt wenn vorhanden, sonst lade aus Datei
        if editor_content.strip():
            content_to_parse = editor_content
        else:
            # Lade aus Datei wenn Editor leer ist
            content_to_parse = self.load_file_content(project)

        # Parse sections - auto-numbered based on ### markers
        sections = {}
        current_num = 0
        current_lines = []
        
        for line in content_to_parse.split('\n'):
            line = line.rstrip("\n")
            if line.startswith("###"):
                # Save previous section if exists
                if current_num > 0 and current_lines:
                    sections[current_num] = current_lines
                # Start new section
                current_num += 1
                current_lines = []
            else:
                if current_num > 0:  # Only collect lines after first ###
                    current_lines.append(line)
        
        # Save last section if exists
        if current_num > 0 and current_lines:
            sections[current_num] = current_lines

        # determine final idx
        if sections:
            max_idx = len(sections)
            if randomize == 1:
                idx = random.randint(1, max_idx)
            else:
                idx = min(index, max_idx)
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

        # Global prompt (first section) voranstellen
        if idx != 1 and 1 in sections:
            global_lines = sections[1]
            if '---' in global_lines:
                sep = global_lines.index('---')
                global_pos = "\n".join(global_lines[:sep]).strip()
                global_neg = "\n".join(global_lines[sep+1:]).strip()
            else:
                global_pos = "\n".join(global_lines).strip()
                global_neg = ""
            
            # Global prompts mit Komma anhängen
            if global_pos:
                pos = global_pos + ", " + pos if pos else global_pos
            if global_neg:
                neg = global_neg + ", " + neg if neg else global_neg

        return pos, neg, project, idx

    @classmethod
    def IS_CHANGED(s, project, index, randomize, editor_content):
        # Wichtig für ComfyUI um zu erkennen wenn sich Parameter ändern
        return f"{project}_{index}_{randomize}_{hash(editor_content)}"
