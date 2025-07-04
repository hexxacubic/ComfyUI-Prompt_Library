import random

class Simple_Prompt_Library:
    """
    Simple Prompt Library - Text field and index only
    • prompt_text: Multi-line text field for prompts
    • index: Selects the prompt project (1-999)
    • randomize_index: When enabled, index is randomly selected
    • Syntax: 
      - Empty lines separate projects
      - --- (or ---- or -----) separates positive/negative prompts
      - ### at line start marks comments/notes (will be ignored)
    """

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "prompt_text": ("STRING", {
                    "multiline": True, 
                    "default": "### Example Project\nhigh quality, depth of field\n---\nworst quality, ugly"
                }),
                "index": ("INT", {"default": 1, "min": 1, "max": 999}),
                "randomize_index": ("BOOLEAN", {"default": False}),
            }
        }

    RETURN_TYPES = ("STRING", "INT")
    RETURN_NAMES = ("double_prompt", "used_index")
    FUNCTION = "get_prompt"
    CATEGORY = "hexxacubic"

    def get_prompt(self, prompt_text, index, randomize_index, **kwargs):
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
            return ("", index)

        # All sections are normal projects (index 1 to n)
        available_indices = list(range(1, len(sections) + 1))
        
        if not available_indices:
            return ("", index)
            
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
        section_idx = used_idx - 1  # Convert to 0-based index
            
        if section_idx >= len(sections):
            return ("", used_idx)
            
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

        # Combine positive and negative with separator
        if pos and neg:
            double_prompt = f"{pos}\n---\n{neg}"
        elif pos:
            double_prompt = pos
        elif neg:
            # Even if only negative prompt exists, include separator
            double_prompt = f"\n---\n{neg}"
        else:
            double_prompt = ""

        return (double_prompt, used_idx)

    @classmethod
    def IS_CHANGED(s, prompt_text, index, randomize_index, **kwargs):
        # Always mark as changed when randomize is enabled
        if randomize_index:
            return float("nan")
        return hash(prompt_text + str(index))
