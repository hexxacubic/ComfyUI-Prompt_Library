class Double_Prompt_Encode:
    """
    Double Prompt Encode - Splits text into positive/negative conditioning
    • double_prompt: Multi-line text with positive and negative prompts
    • Separator: --- or ---- divides positive/negative prompts
    • Separator can appear anywhere in the text (not restricted to own line)
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
        # Initialize positive and negative text
        positive_text = ""
        negative_text = ""

        # Find separator (--- or ----) anywhere in the text
        separator = None
        if '----' in double_prompt:
            separator = '----'
        elif '---' in double_prompt:
            separator = '---'

        # Split based on separator
        if separator:
            positive_text, negative_text = double_prompt.split(separator, 1)
            positive_text = positive_text.strip()
            negative_text = negative_text.strip()
        else:
            positive_text = double_prompt.strip()
            negative_text = ""

        # Encode prompts using the standard CLIP text encode method
        # This ensures compatibility with all ComfyUI versions
        
        # Positive conditioning
        if positive_text:
            tokens = clip.tokenize(positive_text)
            cond, pooled = clip.encode_from_tokens(tokens, return_pooled=True)
            positive_conditioning = [[cond, {"pooled_output": pooled}]]
        else:
            tokens = clip.tokenize("")
            cond, pooled = clip.encode_from_tokens(tokens, return_pooled=True)
            positive_conditioning = [[cond, {"pooled_output": pooled}]]
        
        # Negative conditioning
        if negative_text:
            tokens = clip.tokenize(negative_text)
            cond, pooled = clip.encode_from_tokens(tokens, return_pooled=True)
            negative_conditioning = [[cond, {"pooled_output": pooled}]]
        else:
            tokens = clip.tokenize("")
            cond, pooled = clip.encode_from_tokens(tokens, return_pooled=True)
            negative_conditioning = [[cond, {"pooled_output": pooled}]]

        return (positive_conditioning, negative_conditioning)

    @classmethod
    def IS_CHANGED(s, clip, double_prompt):
        return hash(double_prompt)
