class Double_Prompt_Encode:
    """
    Double Prompt Encode - Splits text into positive/negative conditioning
    • double_prompt: Multi-line text with positive and negative prompts
    • Separator: --- (or ---- or -----) divides positive/negative prompts
    • Everything before separator becomes positive conditioning
    • Everything after separator becomes negative conditioning
    • If no separator found, entire text becomes positive (negative empty)
    """

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "clip": ("CLIP",),
                "double_prompt": ("STRING", {"forceInput": True}),
            }
        }

    RETURN_TYPES = ("CONDITIONING", "CONDITIONING")
    RETURN_NAMES = ("positive", "negative")
    FUNCTION = "encode_prompts"
    CATEGORY = "hexxacubic"

    def encode_prompts(self, clip, double_prompt):
        # Parse text into positive and negative parts
        lines = double_prompt.split('\n')
        
        # Find separator (---, ----, or -----)
        separator_idx = -1
        for i, line in enumerate(lines):
            if line.strip() in ["---", "----", "-----"]:
                separator_idx = i
                break
        
        # Split based on separator
        if separator_idx != -1:
            positive_text = "\n".join(lines[:separator_idx]).strip()
            negative_text = "\n".join(lines[separator_idx+1:]).strip()
        else:
            positive_text = double_prompt.strip()
            negative_text = ""
        
        # Encode positive prompt
        if positive_text:
            positive_tokens = clip.tokenize(positive_text)
            positive_cond, positive_pooled = clip.encode_from_tokens(positive_tokens, return_pooled=True)
            positive_conditioning = [[positive_cond, {"pooled_output": positive_pooled}]]
        else:
            # Empty positive prompt
            empty_tokens = clip.tokenize("")
            empty_cond, empty_pooled = clip.encode_from_tokens(empty_tokens, return_pooled=True)
            positive_conditioning = [[empty_cond, {"pooled_output": empty_pooled}]]
        
        # Encode negative prompt
        if negative_text:
            negative_tokens = clip.tokenize(negative_text)
            negative_cond, negative_pooled = clip.encode_from_tokens(negative_tokens, return_pooled=True)
            negative_conditioning = [[negative_cond, {"pooled_output": negative_pooled}]]
        else:
            # Empty negative prompt
            empty_tokens = clip.tokenize("")
            empty_cond, empty_pooled = clip.encode_from_tokens(empty_tokens, return_pooled=True)
            negative_conditioning = [[empty_cond, {"pooled_output": empty_pooled}]]
        
        return (positive_conditioning, negative_conditioning)

    @classmethod
    def IS_CHANGED(s, clip, double_prompt):
        return hash(double_prompt)
