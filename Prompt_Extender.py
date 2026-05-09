# Prompt_Extender.py
import re

class Prompt_Extender:
    """
    A ComfyUI node for building double prompts from two text fields.
    Can also extend existing prompts when connected.
    Can prepend or append the additions based on the prepend_mode setting.
    
    Features:
    - Supports separator (---, ----, -----) anywhere: own line or mid-text
    - Output: always clean --- on its own line
    - Intelligent tag merging: deduplication, comma-separated
    - Preserves positive/negative separation
    """
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt_additions": ("STRING", {
                    "multiline": True, 
                    "default": "beautiful, high quality\n---\nblurry, low quality"
                }),
                "prepend_mode": ("BOOLEAN", {
                    "default": False,
                    "label_on": "Prepend",
                    "label_off": "Append"
                }),
            },
            "optional": {
                "double_prompt": ("STRING", {"forceInput": True}),
            }
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("double_prompt",)
    FUNCTION = "extend_prompts"
    CATEGORY = "hexxacubic"

    def extend_prompts(self, prompt_additions, prepend_mode, double_prompt=""):
        # If no input connected, return additions as-is
        if not double_prompt:
            return (prompt_additions.strip(),)
        
        # Parse both inputs
        positive_prompt, negative_prompt = self._parse_double_prompt(double_prompt)
        positive_addition, negative_addition = self._parse_double_prompt(prompt_additions)
        
        # Combine based on mode
        if prepend_mode:
            combined_positive = self._combine_prompts(positive_addition, positive_prompt)
            combined_negative = self._combine_prompts(negative_addition, negative_prompt)
        else:
            combined_positive = self._combine_prompts(positive_prompt, positive_addition)
            combined_negative = self._combine_prompts(negative_prompt, negative_addition)
        
        # Format output with clean separator
        return (self._format_double_prompt(combined_positive, combined_negative),)
    
    def _parse_double_prompt(self, text):
        """Parse double prompt: supports --- anywhere in text (mid-line or own line)"""
        if not text or not text.strip():
            return "", ""
        
        # Match ---, ----, -----, ----- (with optional spaces/dashes)
        pattern = r'\s*[-—]{3,}\s*'  # includes en-dash, em-dash
        match = re.search(pattern, text)
        
        if match:
            sep_start = match.start()
            sep_end = match.end()
            positive = text[:sep_start].strip()
            negative = text[sep_end:].strip()
        else:
            positive = text.strip()
            negative = ""
        
        return positive, negative
    
    def _split_tags(self, text):
        """Split prompt into clean list of tags (by comma, semicolon, or newline)"""
        if not text:
            return []
        # Split by comma, semicolon, or newline
        parts = re.split(r'[,;\n]+', text)
        tags = [p.strip() for p in parts if p.strip()]
        return tags
    
    def _combine_prompts(self, base, addition):
        """Combine two prompt parts: deduplicate, comma-separated"""
        base = base.strip()
        addition = addition.strip()
        
        if not base:
            return addition
        if not addition:
            return base
        
        base_tags = self._split_tags(base)
        add_tags = self._split_tags(addition)
        
        # Merge and deduplicate (preserve base order, then additions)
        seen = set()
        combined = []
        for tag in base_tags + add_tags:
            if tag not in seen:
                seen.add(tag)
                combined.append(tag)
        
        return ", ".join(combined)
    
    def _format_double_prompt(self, positive, negative):
        """Format positive and negative into clean double prompt with --- on own line"""
        positive = positive.strip()
        negative = negative.strip()
        
        if positive and negative:
            return f"{positive}\n---\n{negative}"
        elif positive:
            return positive
        elif negative:
            return f"\n---\n{negative}"
        else:
            return ""
    
    @classmethod
    def IS_CHANGED(cls, prompt_additions, prepend_mode, double_prompt=""):
        """Cache busting based on all inputs"""
        return hash(prompt_additions + str(prepend_mode) + double_prompt)
