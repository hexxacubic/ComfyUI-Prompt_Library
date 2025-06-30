import random

class Simple_Prompt_Library:
    """
    Simple Prompt Library - Text field and index only
    • prompt_text: Multi-line text field for prompts
    • index: Selects the prompt project (1-999)
    • randomize_index: When enabled, index is randomly selected
    • Global Prompt: When enabled, the first project is used as Global Prompt
    • Syntax: 
      - Empty lines separate projects
      - --- (or ---- or -----) separates positive/negative prompts
      - ### at line start marks comments/notes (will be ignored)
    """

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "prompt_text": ("STRING", {"multiline": True, "default": "### Global Prompt\nhigh quality, depth of field\n---\nworst quality, ugly"}),
                "index": ("INT", {"default": 1, "min": 1, "max": 999}),
                "randomize_index": ("BOOLEAN", {"default": False}),
                "Global Prompt": ("BOOLEAN", {"default": True}),
            }
        }

    RETURN_TYPES = ("STRING", "INT")
    RETURN_NAMES = ("double_prompt", "used_index")
    FUNCTION = "get_prompt"
    CATEGORY = "hexxacubic"

    def get_prompt(self, prompt_text, index, randomize_index, **kwargs):
        # Access "Global Prompt" parameter with space in name
        global_prompt_enabled = kwargs.get("Global Prompt", True)
        
        if not prompt_text.strip():
            return ("", index)

        # Parse sections - separated by empty lines
        sections = []
        current_lines = []
        
        for line in prompt_text.split('\n'):
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
            return ("", "", index)

        # Determine the index to use
        if global_prompt_enabled:
            # With Global Prompt: Index 0 is global, normal projects start at 1
            available_indices = list(range(1, len(sections)))
            global_idx = 0
        else:
            # Without Global Prompt: All sections are normal projects (index 1 to n)
            available_indices = list(range(1, len(sections) + 1))
            global_idx = None
        
        if not available_indices:
            return ("", "", index)
            
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
        if global_prompt_enabled:
            section_idx = used_idx  # Projects start at 1, sections at 0
        else:
            section_idx = used_idx - 1  # Without global prompt, index 1 corresponds to first section
            
        if section_idx >= len(sections):
            return ("", "", used_idx)
            
        lines = sections[section_idx]
        
        # Find separator (---, ----, or -----)
        separator_idx = -1
        for i, line in enumerate(lines):
            stripped = line.strip()
            if stripped in ["---", "----", "-----"]:
                separator_idx = i
                break
        
        if separator_idx != -1:
            pos = "\n".join(lines[:separator_idx]).strip()
            neg = "\n".join(lines[separator_idx+1:]).strip()
        else:
            pos = "\n".join(lines).strip()
            neg = ""

        # Prepend global prompt if enabled
        if global_prompt_enabled and global_idx is not None and used_idx > 0:
            if len(sections) > 0:
                global_lines = sections[0]
                
                # Find separator in global section
                global_separator_idx = -1
                for i, line in enumerate(global_lines):
                    stripped = line.strip()
                    if stripped in ["---", "----", "-----"]:
                        global_separator_idx = i
                        break
                
                if global_separator_idx != -1:
                    global_pos = "\n".join(global_lines[:global_separator_idx]).strip()
                    global_neg = "\n".join(global_lines[global_separator_idx+1:]).strip()
                else:
                    global_pos = "\n".join(global_lines).strip()
                    global_neg = ""
                
                # Append global prompts with comma
                if global_pos:
                    pos = global_pos + ", " + pos if pos else global_pos
                if global_neg:
                    neg = global_neg + ", " + neg if neg else global_neg

        # Combine positive and negative with separator
        if pos and neg:
            double_prompt = f"{pos}\n---\n{neg}"
        elif pos:
            double_prompt = pos
        elif neg:
            double_prompt = f"\n---\n{neg}"
        else:
            double_prompt = ""

        return (double_prompt, used_idx)

    @classmethod
    def IS_CHANGED(s, prompt_text, index, randomize_index, **kwargs):
        global_prompt = kwargs.get("Global Prompt", True)
        # Always mark as changed when randomize is enabled
        if randomize_index:
            return float("nan")
        return hash(prompt_text + str(index) + str(global_prompt))
