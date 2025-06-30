class Double_Prompt_Encode:
    """
    Double Prompt Encode - Splits text into positive/negative conditioning
    • text: Multi-line text with positive and negative prompts
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
                "double_prompt": ("STRING", {"multiline": True, "default": "masterpiece, best quality\n---\nworst quality, low quality"}),
            }
        }

    RETURN_TYPES = ("CONDITIONING", "CONDITIONING")
    RETURN_NAMES = ("positive", "negative")
    FUNCTION = "encode_prompts"
    CATEGORY = "hexxacubic"

    def encode_prompts(self, clip, text):
        # Parse text into positive and negative parts
        lines = text.split('\n')
        
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
            positive_text = text.strip()
            negative_text = ""
        
        # Encode positive prompt
        if positive_text:
            positive_tokens = clip.tokenize(positive_text)
            positive_cond = clip.encode_from_tokens(positive_tokens, return_pooled=True)
        else:
            # Empty positive prompt
            empty_tokens = clip.tokenize("")
            positive_cond = clip.encode_from_tokens(empty_tokens, return_pooled=True)
        
        # Encode negative prompt
        if negative_text:
            negative_tokens = clip.tokenize(negative_text)
            negative_cond = clip.encode_from_tokens(negative_tokens, return_pooled=True)
        else:
            # Empty negative prompt
            empty_tokens = clip.tokenize("")
            negative_cond = clip.encode_from_tokens(empty_tokens, return_pooled=True)
        
        return (positive_cond, negative_cond)

    @classmethod
    def IS_CHANGED(s, clip, text):
        return hash(text)
