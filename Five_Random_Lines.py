import random
import re

class FiveRandomLinesNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "global_prompt": ("STRING", {"multiline": True, "default": "", "placeholder": "Enter static global prompt (positive --- negative)"}),
                "text_1": ("STRING", {"multiline": True, "default": "", "placeholder": "Enter lines (positive --- negative), one per line"}),
                "text_2": ("STRING", {"multiline": True, "default": "", "placeholder": "Enter lines (positive --- negative), one per line"}),
                "text_3": ("STRING", {"multiline": True, "default": "", "placeholder": "Enter lines (positive --- negative), one per line"}),
                "text_4": ("STRING", {"multiline": True, "default": "", "placeholder": "Enter lines (positive --- negative), one per line"}),
                "text_5": ("STRING", {"multiline": True, "default": "", "placeholder": "Enter lines (positive --- negative), one per line"}),
                "prepend_mode": ("BOOLEAN", {"default": False, "label_on": "Prepend Global", "label_off": "Append Global"}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("double_prompt",)
    FUNCTION = "combine_random_lines"
    CATEGORY = "hexxacubic"

    def _parse_double_prompt(self, text):
        """Parse a text into positive and negative prompts using '---' as separator."""
        if not text.strip():
            return "", ""
        # Split by '---' whether inline or on a new line
        parts = re.split(r'\s*---\s*', text.strip(), maxsplit=1)
        positive = parts[0].strip() if parts else ""
        negative = parts[1].strip() if len(parts) > 1 else ""
        return positive, negative

    def _combine_prompts(self, base_prompt, addition):
        """Combine two prompts, ensuring proper comma separation."""
        base_prompt = base_prompt.strip()
        addition = addition.strip()
        if not base_prompt:
            return addition
        if not addition:
            return base_prompt
        # Add comma if needed
        if not base_prompt.endswith(',') and not base_prompt.endswith('.'):
            return f"{base_prompt}, {addition}"
        return f"{base_prompt} {addition}"

    def combine_random_lines(self, global_prompt, text_1, text_2, text_3, text_4, text_5, prepend_mode):
        texts = [text_1, text_2, text_3, text_4, text_5]
        positive_lines = []
        negative_lines = []

        # Parse global prompt (static, no random selection)
        global_positive, global_negative = self._parse_double_prompt(global_prompt)

        # Process random text fields
        for text in texts:
            lines = [line.strip() for line in text.strip().split('\n') if line.strip()]
            if lines:
                # Randomly select a line without a seed
                selected_line = random.choice(lines)
                # Parse the selected line for positive and negative parts
                positive, negative = self._parse_double_prompt(selected_line)
                if positive:
                    positive_lines.append(positive)
                if negative:
                    negative_lines.append(negative)

        # Combine prompts based on prepend_mode
        combined_positive = ""
        combined_negative = ""
        
        if prepend_mode:
            # Global prompt first
            if global_positive:
                positive_lines.insert(0, global_positive)
            if global_negative:
                negative_lines.insert(0, global_negative)
        else:
            # Global prompt last
            if global_positive:
                positive_lines.append(global_positive)
            if global_negative:
                negative_lines.append(global_negative)

        # Combine all positive and negative prompts
        for pos in positive_lines:
            combined_positive = self._combine_prompts(combined_positive, pos)
        for neg in negative_lines:
            combined_negative = self._combine_prompts(combined_negative, neg)

        # Format output in double-prompt style
        if combined_positive and combined_negative:
            return (f"{combined_positive}\n---\n{combined_negative}",)
        elif combined_positive:
            return (combined_positive,)
        elif combined_negative:
            return (f"\n---\n{combined_negative}",)
        return ("",)

NODE_CLASS_MAPPINGS = {
    "FiveRandomLines": FiveRandomLinesNode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "FiveRandomLines": "Five Random Lines with Global Prompt"
}
