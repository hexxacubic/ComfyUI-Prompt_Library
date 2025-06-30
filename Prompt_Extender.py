import re

class Prompt_Extender:
    """
    A ComfyUI node for extending double prompts.
    Takes a double prompt input and adds extensions to both positive and negative parts.
    """
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "double_prompt": ("STRING", {"forceInput": True}),
                "prompt_additions": ("STRING", {
                    "multiline": True, 
                    "default": "beautiful, high quality\n---\nblurry, low quality"
                }),
            }
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("double_prompt",)
    FUNCTION = "extend_prompts"
    CATEGORY = "hexxacubic"

    def extend_prompts(self, double_prompt, prompt_additions):
        # Parse input double prompt
        positive_prompt, negative_prompt = self._parse_double_prompt(double_prompt)
        
        # Parse additions
        positive_addition, negative_addition = self._parse_double_prompt(prompt_additions)
        
        # Combine the prompts
        combined_positive = self._combine_prompts(positive_prompt, positive_addition)
        combined_negative = self._combine_prompts(negative_prompt, negative_addition)
        
        # Return as double prompt format
        if combined_positive and combined_negative:
            return (f"{combined_positive}\n---\n{combined_negative}",)
        elif combined_positive:
            return (combined_positive,)
        elif combined_negative:
            return (f"\n---\n{combined_negative}",)
        else:
            return ("",)
    
    def _parse_double_prompt(self, text):
        """Parse double prompt format into positive and negative parts"""
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
            positive = "\n".join(lines[:separator_idx]).strip()
            negative = "\n".join(lines[separator_idx+1:]).strip()
        else:
            positive = text.strip()
            negative = ""
            
        return positive, negative
    
    def _combine_prompts(self, base_prompt, addition):
        """Intelligently combines base prompt and addition"""
        base_prompt = base_prompt.strip()
        addition = addition.strip()
        
        if not base_prompt:
            return addition
        if not addition:
            return base_prompt
        
        # Add comma between prompts if none exists
        if base_prompt and addition:
            if not base_prompt.endswith(',') and not base_prompt.endswith('.'):
                return f"{base_prompt}, {addition}"
            else:
                return f"{base_prompt} {addition}"
        
        return base_prompt
