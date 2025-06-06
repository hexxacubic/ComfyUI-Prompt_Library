import random

class Simple_Prompt_Library:
    """
    Simple Prompt Library - Nur Textfeld und Index
    • prompt_text: Mehrzeiliges Textfeld für Prompts
    • index: Wählt das Prompt-Projekt (### Marker)
    • randomize_index: Wenn aktiviert, wird index zufällig gesetzt
    • Syntax: ### markiert neues Projekt, --- trennt positive/negative
    """

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "prompt_text": ("STRING", {"multiline": True, "default": ""}),
                "index": ("INT", {"default": 1, "min": 1, "max": 99}),
                "randomize_index": ("BOOLEAN", {"default": False}),
            }
        }

    RETURN_TYPES = ("STRING", "STRING", "INT")
    RETURN_NAMES = ("positive", "negative", "used_index")
    FUNCTION = "get_prompt"
    CATEGORY = "hexxacubic"

    def get_prompt(self, prompt_text, index, randomize_index):
        if not prompt_text.strip():
            return "", "", index

        # Parse sections - auto-numbered based on ### markers
        # Index 0 = Global Prompt, Index 1-99 = normale Projekte
        sections = {}
        current_num = -1  # Start bei -1, wird bei erster ### zu 0
        current_lines = []
        
        for line in prompt_text.split('\n'):
            line = line.rstrip("\n")
            if line.startswith("###"):
                # Save previous section if exists
                if current_num >= 0 and current_lines:
                    sections[current_num] = current_lines
                # Start new section
                current_num += 1
                current_lines = []
            else:
                if current_num >= 0:  # Collect lines after first ###
                    current_lines.append(line)
        
        # Save last section if exists
        if current_num >= 0 and current_lines:
            sections[current_num] = current_lines

        # Determine final index
        if sections:
            # Verfügbare Indizes: 1 bis max (ohne 0 = Global Prompt)
            available_indices = [idx for idx in sections.keys() if idx > 0]
            
            if available_indices:
                if randomize_index:
                    # Zufälligen Index aus verfügbaren wählen (ohne Global Prompt)
                    used_idx = random.choice(available_indices)
                else:
                    # Verwende den gegebenen Index, mit Wrapping wenn nötig
                    if index in available_indices:
                        used_idx = index
                    else:
                        # Wrapping mit Modulo auf verfügbare Indizes
                        used_idx = available_indices[(index - 1) % len(available_indices)]
            else:
                # Keine normalen Projekte vorhanden
                used_idx = 1
        else:
            used_idx = 1

        # Extract prompts from selected section
        lines = sections.get(used_idx, [])
        if '---' in lines:
            sep = lines.index('---')
            pos = "\n".join(lines[:sep]).strip()
            neg = "\n".join(lines[sep+1:]).strip()
        else:
            pos = "\n".join(lines).strip()
            neg = ""

        # Global prompt (index 0) voranstellen
        if used_idx != 0 and 0 in sections:
            global_lines = sections[0]
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

        return pos, neg, used_idx

    @classmethod
    def IS_CHANGED(s, prompt_text, index, randomize_index):
        # Bei Randomize immer als geändert markieren
        if randomize_index:
            return float("nan")
        return hash(prompt_text + str(index))
